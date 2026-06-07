#!/usr/bin/env python3
"""Weave reaction/pause/delivery tags into voice_performance_manifest.json tts_text."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from performance_tagging import (
    MIN_TAGS_PER_LINE,
    count_reaction_pause_tags,
    count_tags,
    ensure_min_tags,
    has_mid_woven_tag,
    tag_line,
    weave_delivery_tags,
)
from voice_performance_lib import PERFORMANCE_MANIFEST


def _update_counts(data: dict) -> None:
    entries = data.get("entries", [])
    total = len(entries)
    tagged = sum(1 for e in entries if e.get("tts_text") != e.get("game_text"))
    min_two = sum(1 for e in entries if count_tags(e.get("tts_text", "")) >= MIN_TAGS_PER_LINE)
    by_char: dict[str, int] = {}
    for e in entries:
        c = e.get("character", "?")
        by_char[c] = by_char.get(c, 0) + 1
    data["counts"] = {
        "total": total,
        "toa": by_char.get("toa", 0),
        "kaoru": by_char.get("kaoru", 0),
        "narrator": by_char.get("narrator", 0),
        "tagged_tts": tagged,
        "min_two_tags": min_two,
        "orphans": data.get("counts", {}).get("orphans", 0),
        "with_reaction_pause": sum(
            1 for e in entries if count_reaction_pause_tags(e.get("tts_text", "")) > 0
        ),
        "with_mid_woven": sum(1 for e in entries if has_mid_woven_tag(e.get("tts_text", ""))),
    }


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument(
        "--retag",
        action="store_true",
        help="Re-run tag_line (emotion heuristics + weave) on every entry.",
    )
    ap.add_argument(
        "--weave-only",
        action="store_true",
        help="Weave on existing tts_text only (no tag_line). Default if neither flag.",
    )
    args = ap.parse_args()
    retag = args.retag
    weave_only = args.weave_only or not retag

    data = json.loads(PERFORMANCE_MANIFEST.read_text(encoding="utf-8"))
    entries = data.get("entries", [])
    changed = 0
    gained_reaction = 0
    gained_mid = 0

    for entry in entries:
        lid = entry.get("id", "")
        character = entry.get("character", "")
        game_text = entry.get("game_text", "")
        source = entry.get("source", "")
        old_tts = entry.get("tts_text", game_text)
        had_rp = count_reaction_pause_tags(old_tts) > 0
        had_mid = has_mid_woven_tag(old_tts)

        if retag:
            tts, notes, model = tag_line(character, game_text, lid, source)
        else:
            tts = old_tts
            notes = entry.get("tags_notes", "")
            tts, weave_notes = weave_delivery_tags(
                tts, character, game_text, lid, source
            )
            tts = ensure_min_tags(tts, character, lid, game_text)
            if weave_notes:
                notes = f"{notes}; {weave_notes}" if notes else weave_notes
            model = (
                "eleven_v3" if count_tags(tts) > 0 else entry.get("model_hint", "eleven_v3")
            )

        if tts != old_tts:
            changed += 1
        if count_reaction_pause_tags(tts) > 0 and not had_rp:
            gained_reaction += 1
        if has_mid_woven_tag(tts) and not had_mid:
            gained_mid += 1

        entry["tts_text"] = tts
        entry["tags_notes"] = notes
        entry["model_hint"] = model

    _update_counts(data)
    PERFORMANCE_MANIFEST.write_text(
        json.dumps(data, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    c = data["counts"]
    total = c["total"]
    rp = c.get("with_reaction_pause", 0)
    mid = c.get("with_mid_woven", 0)
    pct_rp = (100.0 * rp / total) if total else 0.0
    pct_mid = (100.0 * mid / total) if total else 0.0
    print(f"mode: {'retag' if retag else 'weave-only'}")
    print(f"entries: {total}")
    print(f"changed tts_text: {changed}")
    print(f"new reaction/pause lines: {gained_reaction}")
    print(f"new mid-woven lines: {gained_mid}")
    print(f"lines with reaction/pause tag: {rp} ({pct_rp:.1f}%)")
    print(f"lines with mid-woven tag: {mid} ({pct_mid:.1f}%)")
    print(f"min_two_tags: {c.get('min_two_tags', 0)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
