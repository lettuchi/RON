#!/usr/bin/env python3
"""Sync scripts/voice_performance_manifest.json with game / voice manifests.

Keeps game_text aligned with Ren'Py display lines. New lines get tts_text = game_text
until you tag them (or pass --apply-tags to run performance_tagging heuristics).

Examples (project root):
    python scripts/sync_voice_performance_manifest.py
    python scripts/sync_voice_performance_manifest.py --diff
    python scripts/sync_voice_performance_manifest.py --apply-tags
    python scripts/sync_voice_performance_manifest.py --prune-orphans
"""
from __future__ import annotations

import argparse
import json
import sys
from datetime import date
from pathlib import Path

from performance_tagging import count_tags, tag_line
from voice_performance_lib import (
    PERFORMANCE_MANIFEST,
    default_meta,
    load_merged_voice_lines,
    load_performance_by_id,
)

ROOT = Path(__file__).resolve().parents[1]


def build_entry(
    row: dict, existing: dict | None, *, apply_tags: bool, retag_all: bool = False
) -> dict:
    game_text = row["game_text"]
    entry: dict = {
        "id": row["id"],
        "character": row["character"],
        "source": row.get("source", ""),
        "game_text": game_text,
        "tts_text": game_text,
        "tags_notes": "",
        "model_hint": "eleven_multilingual_v2",
    }

    if existing:
        entry["tts_text"] = existing.get("tts_text", game_text)
        entry["tags_notes"] = existing.get("tags_notes", "")
        entry["model_hint"] = existing.get("model_hint", entry["model_hint"])
        if existing.get("game_text") != game_text:
            entry["tags_notes"] = (
                (entry["tags_notes"] + "; " if entry["tags_notes"] else "")
                + "game_text updated on sync"
            )

    force_tag = bool(
        apply_tags
        and (
            retag_all
            or not existing
            or existing.get("tts_text", game_text) == game_text
        )
    )
    if force_tag:
        tts, notes, model = tag_line(
            row["character"], game_text, row["id"], row.get("source", "")
        )
        entry["tts_text"] = tts
        if notes:
            entry["tags_notes"] = notes
        entry["model_hint"] = model
    elif entry["tts_text"] != game_text:
        entry["model_hint"] = "eleven_v3"

    return entry


def main() -> int:
    ap = argparse.ArgumentParser(description="Sync voice performance manifest with game.")
    ap.add_argument("--diff", action="store_true", help="Print game_text drift vs stored manifest.")
    ap.add_argument("--apply-tags", action="store_true",
                    help="Run tagging heuristics on new/untagged lines (tts==game).")
    ap.add_argument("--retag-all", action="store_true",
                    help="With --apply-tags, re-run heuristics on every line (keeps manual ids in performance_tagging).")
    ap.add_argument("--prune-orphans", action="store_true",
                    help="Remove entries whose ids are no longer in game/manifests.")
    ap.add_argument("--output", default=str(PERFORMANCE_MANIFEST),
                    help="Output JSON path (default scripts/voice_performance_manifest.json).")
    args = ap.parse_args()
    retag_all = args.retag_all

    current_rows = load_merged_voice_lines()
    current_ids = {r["id"] for r in current_rows}
    existing_by_id = load_performance_by_id(Path(args.output))

    if args.diff:
        if not existing_by_id:
            print("No performance manifest yet.", file=sys.stderr)
            return 2
        drift = 0
        for row in current_rows:
            ex = existing_by_id.get(row["id"])
            if not ex:
                continue
            if ex.get("game_text") != row["game_text"]:
                drift += 1
                print(f"DRIFT {row['id']} ({row['character']})")
                print(f"  stored: {ex.get('game_text', '')[:100]}")
                print(f"  game:   {row['game_text'][:100]}")
        print(f"drift count: {drift}")
        return 0

    orphans: list[dict] = []
    for oid, ex in sorted(existing_by_id.items()):
        if oid not in current_ids:
            orphans.append(ex)

    entries: list[dict] = []
    added = 0
    for row in current_rows:
        ex = existing_by_id.get(row["id"])
        if ex is None:
            added += 1
        entries.append(
            build_entry(row, ex, apply_tags=args.apply_tags, retag_all=retag_all)
        )

    if orphans:
        if args.prune_orphans:
            print(f"pruned {len(orphans)} orphan id(s)")
        else:
            for ex in orphans:
                marked = {**ex, "orphan": True}
                entries.append(marked)
            print(f"kept {len(orphans)} orphan(s) (use --prune-orphans to drop)", file=sys.stderr)

    meta = default_meta()
    if existing_by_id and Path(args.output).is_file():
        prev = json.loads(Path(args.output).read_text(encoding="utf-8"))
        meta["version"] = prev.get("_meta", {}).get("version", 1)
    meta["last_synced"] = date.today().isoformat()

    tagged = sum(1 for e in entries if e.get("tts_text") != e.get("game_text"))
    min_two = sum(1 for e in entries if count_tags(e.get("tts_text", "")) >= 2)
    out = {
        "_meta": meta,
        "counts": {
            "total": len(entries),
            "toa": sum(1 for e in entries if e["character"] == "toa"),
            "kaoru": sum(1 for e in entries if e["character"] == "kaoru"),
            "narrator": sum(1 for e in entries if e["character"] == "narrator"),
            "tagged_tts": tagged,
            "min_two_tags": min_two,
            "orphans": len(orphans) if not args.prune_orphans else 0,
        },
        "entries": entries,
    }

    path = Path(args.output)
    path.write_text(json.dumps(out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    pct = (100.0 * min_two / len(entries)) if entries else 0.0
    print(f"wrote {path}")
    print(
        f"  total={out['counts']['total']} added={added} tagged_tts={tagged} "
        f"min_two_tags={min_two} ({pct:.1f}%) orphans={len(orphans)}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
