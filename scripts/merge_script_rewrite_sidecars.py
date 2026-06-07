#!/usr/bin/env python3
"""Merge conversational rewrite sidecars into voice manifests.

Loads docs/script-rewrite-2026-06-04/case*-updates.json and caseendings-updates.json,
updates voice_performance_manifest.json, voice_manifest.json, and narrator_manifest.json.

Examples (project root):
    python scripts/merge_script_rewrite_sidecars.py
    python scripts/merge_script_rewrite_sidecars.py --dry-run
    python scripts/merge_script_rewrite_sidecars.py --sidecar-dir docs/script-rewrite-2026-06-04
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_SIDECAR_DIR = ROOT / "docs" / "script-rewrite-2026-06-04"
PERFORMANCE_MANIFEST = ROOT / "scripts" / "voice_performance_manifest.json"
VOICE_MANIFEST = ROOT / "scripts" / "voice_manifest.json"
NARRATOR_MANIFEST = ROOT / "scripts" / "narrator_manifest.json"

SIDECAR_GLOB = "case*-updates.json"
OPTIONAL_SIDECARS = ("case1-updates.json",)
REWRITE_NOTE_RE = re.compile(
    r"case(?:\s+\d+|\s+endings)? conversational rewrite 2026-06-04",
    re.I,
)


def rewrite_note_for_path(path: Path) -> str:
    name = path.stem  # case2-updates -> case2-updates
    m = re.match(r"case(\d+)-updates", name)
    if m:
        return f"case {m.group(1)} conversational rewrite 2026-06-04"
    if name.startswith("caseendings"):
        return "case endings conversational rewrite 2026-06-04"
    if name.startswith("case1"):
        return "case 1 conversational rewrite 2026-06-04"
    return "conversational rewrite 2026-06-04"


def append_note(existing: str, note: str) -> str:
    existing = (existing or "").strip()
    if not existing:
        return note
    if note.lower() in existing.lower():
        return existing
    return f"{existing}; {note}"


def load_sidecars(sidecar_dir: Path) -> tuple[dict[str, dict], dict[str, str], list[str], dict[str, int]]:
    """Return merged updates, id -> source file label, warnings, per-file counts."""
    merged: dict[str, dict] = {}
    id_source: dict[str, str] = {}
    warnings: list[str] = []
    per_file: dict[str, int] = {}

    paths: list[Path] = sorted(sidecar_dir.glob(SIDECAR_GLOB))
    for optional in OPTIONAL_SIDECARS:
        p = sidecar_dir / optional
        if p.is_file() and p not in paths:
            paths.append(p)
    paths = sorted(set(paths), key=lambda p: p.name)

    if not paths:
        warnings.append(f"No sidecar files matching {SIDECAR_GLOB} in {sidecar_dir}")
        return merged, id_source, warnings, per_file

    for path in paths:
        if path.name == "case1-updates.json" and not path.is_file():
            continue
        if not path.is_file():
            if path.name in OPTIONAL_SIDECARS:
                per_file[path.name] = 0
            continue
        rows = json.loads(path.read_text(encoding="utf-8"))
        if not isinstance(rows, list):
            warnings.append(f"{path.name}: expected JSON array")
            continue
        per_file[path.name] = len(rows)
        note = rewrite_note_for_path(path)
        for row in rows:
            vid = row.get("id")
            if not vid:
                warnings.append(f"{path.name}: row missing id")
                continue
            if vid in merged:
                prev_src = id_source[vid]
                warnings.append(
                    f"duplicate id {vid}: {prev_src} and {path.name} (later file wins)"
                )
            merged[vid] = {
                "id": vid,
                "character": row.get("character", ""),
                "game_text": row["game_text"],
                "tts_text": row["tts_text"],
                "_rewrite_note": note,
            }
            id_source[vid] = path.name

    return merged, id_source, warnings, per_file


def apply_performance(
    data: dict, updates: dict[str, dict]
) -> tuple[int, list[str]]:
    by_id = {e["id"]: e for e in data.get("entries", [])}
    missing: list[str] = []
    changed = 0
    for vid, row in sorted(updates.items()):
        entry = by_id.get(vid)
        if not entry:
            missing.append(vid)
            continue
        note = row["_rewrite_note"]
        if entry.get("game_text") != row["game_text"]:
            entry["game_text"] = row["game_text"]
            changed += 1
        elif entry.get("tts_text") != row["tts_text"]:
            pass
        else:
            changed += 1  # still count tag note / tts-only updates
        entry["tts_text"] = row["tts_text"]
        entry["tags_notes"] = append_note(entry.get("tags_notes", ""), note)
        if entry.get("tts_text") != entry.get("game_text"):
            entry["model_hint"] = "eleven_v3"
    data["entries"] = sorted(by_id.values(), key=lambda e: e["id"])
    return changed, missing


def apply_voice_manifest(data: dict, updates: dict[str, dict]) -> tuple[int, list[str]]:
    by_id = {line["id"]: line for line in data.get("lines", [])}
    missing: list[str] = []
    changed = 0
    for vid, row in sorted(updates.items()):
        if row["character"] == "narrator":
            continue
        line = by_id.get(vid)
        if not line:
            missing.append(vid)
            continue
        if line.get("text") != row["game_text"]:
            line["text"] = row["game_text"]
            changed += 1
    return changed, missing


def apply_narrator_manifest(data: dict, updates: dict[str, dict]) -> tuple[int, list[str]]:
    by_id = {line["id"]: line for line in data.get("lines", [])}
    missing: list[str] = []
    changed = 0
    for vid, row in sorted(updates.items()):
        if row["character"] != "narrator":
            continue
        line = by_id.get(vid)
        if not line:
            missing.append(vid)
            continue
        if line.get("text") != row["game_text"]:
            line["text"] = row["game_text"]
            changed += 1
    return changed, missing


def main() -> int:
    ap = argparse.ArgumentParser(description="Merge script rewrite sidecars into manifests.")
    ap.add_argument(
        "--sidecar-dir",
        type=Path,
        default=DEFAULT_SIDECAR_DIR,
        help=f"Directory with case*-updates.json (default: {DEFAULT_SIDECAR_DIR.relative_to(ROOT)})",
    )
    ap.add_argument("--dry-run", action="store_true", help="Print summary without writing files.")
    args = ap.parse_args()
    sidecar_dir = args.sidecar_dir.resolve()

    updates, id_source, warnings, per_file = load_sidecars(sidecar_dir)
    case1_path = sidecar_dir / "case1-updates.json"
    case1_missing = not case1_path.is_file()

    print(f"Sidecar dir: {sidecar_dir}")
    for name in sorted(per_file):
        print(f"  {name}: {per_file[name]} rows")
    if case1_missing:
        print("  case1-updates.json: (not present, skipped)")
    print(f"Merged unique ids: {len(updates)}")
    if warnings:
        print("Warnings:")
        for w in warnings:
            print(f"  - {w}")

    if not updates:
        return 1

    perf = json.loads(PERFORMANCE_MANIFEST.read_text(encoding="utf-8"))
    voice = json.loads(VOICE_MANIFEST.read_text(encoding="utf-8"))
    narrator = json.loads(NARRATOR_MANIFEST.read_text(encoding="utf-8"))

    perf_changed, perf_missing = apply_performance(perf, updates)
    voice_changed, voice_missing = apply_voice_manifest(voice, updates)
    narr_changed, narr_missing = apply_narrator_manifest(narrator, updates)

    print(f"Performance manifest: {perf_changed} entries touched, {len(perf_missing)} ids missing")
    print(f"Voice manifest (character): {voice_changed} lines updated, {len(voice_missing)} ids missing")
    print(f"Narrator manifest: {narr_changed} lines updated, {len(narr_missing)} ids missing")

    all_missing = sorted(set(perf_missing) | set(voice_missing) | set(narr_missing))
    if all_missing:
        print(f"Missing from manifests ({len(all_missing)}): {', '.join(all_missing[:20])}")
        if len(all_missing) > 20:
            print(f"  ... and {len(all_missing) - 20} more")

    if args.dry_run:
        print("(dry-run: no files written)")
        return 0

    PERFORMANCE_MANIFEST.write_text(
        json.dumps(perf, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    VOICE_MANIFEST.write_text(
        json.dumps(voice, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    NARRATOR_MANIFEST.write_text(
        json.dumps(narrator, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print("Wrote manifests.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
