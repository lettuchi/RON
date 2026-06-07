#!/usr/bin/env python3
"""Re-apply performance_tagging to specific line ids in voice_performance_manifest.json."""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

from performance_tagging import tag_line
from voice_performance_lib import PERFORMANCE_MANIFEST, load_merged_voice_lines

ROOT = Path(__file__).resolve().parents[1]


def parse_ids_arg(ids_arg: str) -> list[str]:
    if ids_arg.startswith("@"):
        raw = Path(ids_arg[1:]).read_text(encoding="utf-8")
        tokens = re.split(r"[,\s]+", raw)
    else:
        tokens = ids_arg.split(",")
    return [t.strip() for t in tokens if t.strip()]


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--ids", required=True, help="Comma list or @file.txt")
    args = ap.parse_args()
    want = set(parse_ids_arg(args.ids))
    by_id = {r["id"]: r for r in load_merged_voice_lines()}
    data = json.loads(PERFORMANCE_MANIFEST.read_text(encoding="utf-8"))
    updated = 0
    for entry in data.get("entries", []):
        lid = entry.get("id")
        if lid not in want:
            continue
        row = by_id.get(lid)
        if not row:
            print(f"WARN: {lid} not in manifests", file=sys.stderr)
            continue
        game_text = row["game_text"]
        entry["game_text"] = game_text
        source = entry.get("source") or row.get("source", "")
        tts, notes, model = tag_line(row["character"], game_text, lid, source)
        entry["tts_text"] = tts
        entry["tags_notes"] = notes
        entry["model_hint"] = model
        updated += 1
    PERFORMANCE_MANIFEST.write_text(
        json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(f"retagged: {updated}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
