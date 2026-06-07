#!/usr/bin/env python3
"""Batch hand QA on wired canon CGs; outputs JSON for report."""
from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GAME = ROOT / "game"
CG_DIR = GAME / "images" / "cg"
INVENTORY = ROOT / "docs" / "_canon_cg_inventory.txt"
OUT = ROOT / "docs" / "_canon_hand_audit.json"

# No visible humans — skip hand count
NO_HUMAN_KEYWORDS = (
    "establishing",
    "landscape",
    "fireworks",
    "docket",
    "ledger",
    "scroll",
    "fabric",
    "candle",
    "lantern_implied",
    "lash_rain",
    "throw_splash",
    "canal_night",
    "hearing_hall",
    "licensed-quarter",
    "registry",
    "warehouse",
    "gritty",
    "hill",
    "curry_stall",
    "inn_exterior",
    "arrival",
    "tatami_lanterns",
    "sake_cup",
    "silk_fabric",
    "hanko_pot",
    "redacted",
    "rain_alley_door",
    "rain-run",
    "rain-alone",
    "rain-flee",
    "quarter_cage",
    "chained",
    "false_exit",
    "epilogue_week",
    "kotatsu_warmth",
)

HIGH_RISK_KEYWORDS = (
    "embrace",
    "intimate",
    "kiss",
    "grab",
    "hands",
    "wrist",
    "touch",
    "undress",
    "afterglow",
    "pull",
    "dance",
    "punishment",
    "grasp",
    "oath_seal",
    "almost_hands",
    "collar_hands",
    "gunwale",
    "defend",
    "fight",
    "boat_duo",
    "morning",
    "proposition",
    "signing",
    "bedroom",
    "kotatsu",
    "lesson",
    "walk_duo",
    "reassurance",
    "office_touch",
    "sponsorship",
    "barge",
    "curry_bowl",
    "shoji",
    "quilt",
    "tear",
)


def parse_wired_pngs() -> list[tuple[str, str]]:
    text = INVENTORY.read_text(encoding="utf-8")
    in_wired = False
    rows: list[tuple[str, str]] = []
    for line in text.splitlines():
        if line == "=== WIRED ===":
            in_wired = True
            continue
        if line.startswith("=== ") and in_wired:
            break
        if not in_wired or not line.strip() or line.startswith("registry_"):
            continue
        if "\t" not in line:
            continue
        tag, png = line.split("\t", 1)
        if png == "MISSING" or tag == "<tag>":
            continue
        rows.append((tag, png))
    # dedupe by png keeping first tag
    seen: set[str] = set()
    out: list[tuple[str, str]] = []
    for tag, png in rows:
        if png not in seen:
            seen.add(png)
            out.append((tag, png))
    return out


def needs_humans(png: str) -> bool:
    low = png.lower()
    return not any(k in low for k in NO_HUMAN_KEYWORDS)


def is_high_risk(png: str) -> bool:
    low = png.lower()
    return any(k in low for k in HIGH_RISK_KEYWORDS)


def run_mediapipe(png_path: Path) -> dict:
    cmd = [
        sys.executable,
        str(ROOT / "scripts" / "check_cg_hands.py"),
        "--path",
        str(png_path),
        "--json-out",
        str(png_path.with_suffix(".hands.json")),
    ]
    try:
        subprocess.run(cmd, capture_output=True, text=True, timeout=120, cwd=ROOT)
        jpath = png_path.with_suffix(".hands.json")
        if jpath.exists():
            return json.loads(jpath.read_text(encoding="utf-8"))
    except Exception as e:
        return {"error": str(e)}
    return {}


def main() -> None:
    rows = parse_wired_pngs()
    results = []
    for tag, png_name in rows:
        png_path = CG_DIR / png_name
        entry = {
            "tag": tag,
            "png": png_name,
            "exists": png_path.exists(),
            "humans_expected": needs_humans(png_name),
            "high_risk": is_high_risk(png_name),
            "mediapipe": None,
            "visual_status": "PENDING",
            "hand_counts": None,
            "notes": "",
        }
        if png_path.exists() and entry["humans_expected"]:
            mp = run_mediapipe(png_path)
            entry["mediapipe"] = mp
            if isinstance(mp, dict) and "files" in mp:
                fi = mp["files"][0] if mp["files"] else {}
                entry["mediapipe_hands"] = fi.get("hands_detected")
                entry["mediapipe_warnings"] = fi.get("warnings", [])
        results.append(entry)
    OUT.write_text(json.dumps(results, indent=2), encoding="utf-8")
    human = [r for r in results if r["humans_expected"]]
    high = [r for r in human if r["high_risk"]]
    print(f"wired_unique_pngs={len(rows)}")
    print(f"human_expected={len(human)} high_risk={len(high)}")
    print(f"wrote {OUT}")


if __name__ == "__main__":
    main()
