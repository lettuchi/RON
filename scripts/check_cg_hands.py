#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Optional post-generation QA: detect hands in Ryoko Owari CG PNGs via MediaPipe.

Uses the MediaPipe Tasks **Hand Landmarker** API (current stable; legacy
``mp.solutions.hands`` was removed in mediapipe 0.10.x).

**Anime caveat:** painterly 2D anime hands often confuse landmark detectors.
Treat results as **advisory** — review warnings and re-prompt if something
looks wrong. Only use exit code 1 as a hard blocker with ``--strict``.

Install (project root)::

    pip install -r requirements-cg-qa.txt

Usage::

    python scripts/check_cg_hands.py --path game/images/cg/cg-choice-grab-rebuke.png
    python scripts/check_cg_hands.py --path "game/images/cg/*.png"
    python scripts/check_cg_hands.py --path game/images/cg/ --strict --min-confidence 0.6
    python scripts/check_cg_hands.py --path assets/new_cg.png --expect-hands 2 --json-out report.json

Exit codes:
    0 — pass, or warnings only (default advisory mode)
    1 — one or more files hit **fail** thresholds (always when ``--strict`` and any warning)
"""
from __future__ import annotations

import argparse
import json
import sys
import urllib.error
import urllib.request
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import cv2
import mediapipe as mp
import numpy as np
from mediapipe.tasks.python import BaseOptions
from mediapipe.tasks.python.vision import HandLandmarker, HandLandmarkerOptions, RunningMode

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_MODEL_PATH = Path(__file__).resolve().parent / "models" / "hand_landmarker.task"
MODEL_URL = (
    "https://storage.googleapis.com/mediapipe-models/hand_landmarker/"
    "hand_landmarker/float16/latest/hand_landmarker.task"
)
DEFAULT_CG_GLOB = "game/images/cg/*.png"

# Filename tokens suggesting visible hands (heuristic only).
HAND_SCENE_KEYWORDS = (
    "grab",
    "grasp",
    "embrace",
    "hold",
    "hand",
    "wrist",
    "grip",
    "touch",
    "kiss",
    "dance",
    "pull",
    "reach",
    "clasp",
    "brothel",
)

# Scenes where hands may legitimately be off-frame or occluded.
SKIP_ZERO_HAND_FAIL_KEYWORDS = (
    "portrait",
    "face",
    "closeup",
    "bust",
    "establishing",
    "background",
    "landscape",
)


@dataclass
class HandDetection:
    label: str
    confidence: float


@dataclass
class FileResult:
    path: str
    hand_count: int
    hands: list[HandDetection] = field(default_factory=list)
    min_confidence: float | None = None
    max_confidence: float | None = None
    expected_hands: int | None = None
    warnings: list[str] = field(default_factory=list)
    status: str = "pass"  # pass | warn | fail


def ensure_model(model_path: Path) -> Path:
    """Download Hand Landmarker task bundle if missing."""
    if model_path.is_file():
        return model_path
    model_path.parent.mkdir(parents=True, exist_ok=True)
    print(f"Downloading MediaPipe model to {model_path} ...", file=sys.stderr)
    try:
        with urllib.request.urlopen(MODEL_URL, timeout=120) as resp:
            model_path.write_bytes(resp.read())
    except (urllib.error.URLError, TimeoutError) as exc:
        raise SystemExit(
            f"Could not download hand landmarker model: {exc}\n"
            f"Fetch manually from {MODEL_URL}\n"
            f"and save to {model_path}"
        ) from exc
    return model_path


def resolve_paths(path_arg: str) -> list[Path]:
    """Expand a file path, directory, or glob to sorted PNG paths."""
    raw = Path(path_arg)
    if any(ch in path_arg for ch in "*?[]"):
        base = Path(path_arg)
        if not base.is_absolute():
            base = ROOT / path_arg
        parent = base.parent
        pattern = base.name
        if not parent.is_dir():
            parent = ROOT / Path(path_arg).parent
            pattern = Path(path_arg).name
        return sorted(p for p in parent.glob(pattern) if p.is_file())
    if not raw.is_absolute():
        raw = ROOT / raw
    if raw.is_dir():
        return sorted(raw.glob("*.png"))
    if raw.is_file():
        return [raw]
    raise SystemExit(f"Path not found: {path_arg}")


def filename_expects_hands(path: Path) -> bool:
    stem = path.stem.lower()
    if any(k in stem for k in SKIP_ZERO_HAND_FAIL_KEYWORDS):
        return False
    return any(k in stem for k in HAND_SCENE_KEYWORDS)


def build_landmarker(model_path: Path, min_confidence: float) -> HandLandmarker:
    options = HandLandmarkerOptions(
        base_options=BaseOptions(model_asset_path=str(model_path)),
        running_mode=RunningMode.IMAGE,
        num_hands=4,
        min_hand_detection_confidence=min_confidence,
        min_hand_presence_confidence=min_confidence,
        min_tracking_confidence=min_confidence,
    )
    return HandLandmarker.create_from_options(options)


def detect_hands(
    landmarker: HandLandmarker,
    image_path: Path,
) -> list[HandDetection]:
    bgr = cv2.imread(str(image_path))
    if bgr is None:
        raise ValueError(f"Could not read image: {image_path}")
    rgb = cv2.cvtColor(bgr, cv2.COLOR_BGR2RGB)
    mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=np.ascontiguousarray(rgb))
    result = landmarker.detect(mp_image)
    hands: list[HandDetection] = []
    if result.handedness:
        for hand_list in result.handedness:
            if hand_list:
                cat = hand_list[0]
                hands.append(HandDetection(label=cat.category_name, confidence=cat.score))
    return hands


def evaluate_file(
    image_path: Path,
    hands: list[HandDetection],
    *,
    min_confidence: float,
    expect_hands: int | None,
    strict: bool,
) -> FileResult:
    confidences = [h.confidence for h in hands]
    min_conf = min(confidences) if confidences else None
    max_conf = max(confidences) if confidences else None
    expected = expect_hands
    if expected is None and filename_expects_hands(image_path):
        expected = 2

    warnings: list[str] = []
    count = len(hands)

    if count == 0:
        warnings.append("zero_hands: no hands detected")
        if expected is not None:
            warnings.append(f"zero_hands_expected: filename/heuristic expects ~{expected} visible hand(s)")

    if count > 2:
        warnings.append(f"too_many_hands: detected {count} (suspicious for typical duo CG)")

    if expected is not None and count > 0 and count != expected:
        warnings.append(
            f"hand_count_mismatch: detected {count}, expected {expected}"
        )

    if min_conf is not None and min_conf < min_confidence:
        warnings.append(
            f"low_confidence: weakest hand score {min_conf:.3f} < threshold {min_confidence:.3f}"
        )

    status = "pass"
    if warnings:
        status = "fail" if strict else "warn"

    return FileResult(
        path=str(image_path.relative_to(ROOT)) if image_path.is_relative_to(ROOT) else str(image_path),
        hand_count=count,
        hands=hands,
        min_confidence=min_conf,
        max_confidence=max_conf,
        expected_hands=expected,
        warnings=warnings,
        status=status,
    )


def format_report(
    results: list[FileResult],
    *,
    strict: bool,
    min_confidence: float,
) -> str:
    passes = sum(1 for r in results if r.status == "pass")
    warns = sum(1 for r in results if r.status == "warn")
    fails = sum(1 for r in results if r.status == "fail")
    lines = [
        "=== CG Hand QA (MediaPipe Hand Landmarker) ===",
        f"Mode: {'strict (warnings are fails)' if strict else 'advisory (warnings only)'}",
        f"Min confidence threshold: {min_confidence:.2f}",
        f"Files: {len(results)} | pass: {passes} | warn: {warns} | fail: {fails}",
        "",
    ]
    for r in results:
        conf_part = ""
        if r.min_confidence is not None:
            conf_part = f"  confidence: min={r.min_confidence:.3f} max={r.max_confidence:.3f}"
        elif r.hand_count == 0:
            conf_part = "  confidence: n/a"
        hand_labels = ", ".join(f"{h.label}({h.confidence:.2f})" for h in r.hands) or "none"
        lines.append(f"{r.path}  [{r.status.upper()}]")
        lines.append(f"  hands: {r.hand_count} ({hand_labels}){conf_part}")
        if r.expected_hands is not None:
            lines.append(f"  expected (heuristic): ~{r.expected_hands}")
        for w in r.warnings:
            lines.append(f"  - {w}")
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="MediaPipe hand-check QA for Ryoko Owari CG PNGs (advisory by default).",
    )
    parser.add_argument(
        "--path",
        default=DEFAULT_CG_GLOB,
        help=f"PNG file, directory, or glob (default: {DEFAULT_CG_GLOB})",
    )
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Treat warnings as failures (exit 1 if any warning).",
    )
    parser.add_argument(
        "--min-confidence",
        type=float,
        default=0.5,
        metavar="FLOAT",
        help="Detection threshold and low-confidence warning cutoff (default: 0.5).",
    )
    parser.add_argument(
        "--expect-hands",
        type=int,
        default=None,
        metavar="N",
        help="Expected visible hand count for all inputs (overrides filename heuristic).",
    )
    parser.add_argument(
        "--model",
        type=Path,
        default=DEFAULT_MODEL_PATH,
        help=f"Path to hand_landmarker.task (default: {DEFAULT_MODEL_PATH})",
    )
    parser.add_argument(
        "--json-out",
        type=Path,
        default=None,
        help="Write full JSON report to this path (also prints JSON to stdout if --json).",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Print JSON report to stdout after the human-readable summary.",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    if not 0.0 <= args.min_confidence <= 1.0:
        raise SystemExit("--min-confidence must be between 0 and 1")

    paths = resolve_paths(args.path)
    if not paths:
        raise SystemExit(f"No PNG files matched: {args.path}")

    model_path = ensure_model(args.model.resolve())
    landmarker = build_landmarker(model_path, args.min_confidence)
    try:
        results: list[FileResult] = []
        for image_path in paths:
            try:
                hands = detect_hands(landmarker, image_path)
            except ValueError as exc:
                results.append(
                    FileResult(
                        path=str(image_path),
                        hand_count=0,
                        warnings=[f"read_error: {exc}"],
                        status="fail" if args.strict else "warn",
                    )
                )
                continue
            results.append(
                evaluate_file(
                    image_path,
                    hands,
                    min_confidence=args.min_confidence,
                    expect_hands=args.expect_hands,
                    strict=args.strict,
                )
            )
    finally:
        landmarker.close()

    payload: dict[str, Any] = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "mode": "strict" if args.strict else "advisory",
        "min_confidence": args.min_confidence,
        "summary": {
            "files": len(results),
            "pass": sum(1 for r in results if r.status == "pass"),
            "warn": sum(1 for r in results if r.status == "warn"),
            "fail": sum(1 for r in results if r.status == "fail"),
        },
        "results": [
            {
                **{k: v for k, v in asdict(r).items() if k != "hands"},
                "hands": [asdict(h) for h in r.hands],
            }
            for r in results
        ],
    }

    report_text = format_report(results, strict=args.strict, min_confidence=args.min_confidence)
    print(report_text, end="")

    if args.json:
        print(json.dumps(payload, indent=2))

    if args.json_out:
        out = args.json_out if args.json_out.is_absolute() else ROOT / args.json_out
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
        print(f"Wrote JSON report to {out}", file=sys.stderr)

    return 1 if payload["summary"]["fail"] > 0 else 0


if __name__ == "__main__":
    raise SystemExit(main())
