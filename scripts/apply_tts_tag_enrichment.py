#!/usr/bin/env python3
"""Add or enrich Eleven v3 tags on voice_performance_manifest tts_text only.

game_text must mirror Ren'Py display lines (plain prose). ElevenLabs bracket tags belong
on tts_text only — not on game_text or voice_manifest.json text fields. This script warns
on stderr when game_text still contains performance tags (see warn_game_text_tags).

Targets entries with no leading tag or only 0-1 tags. Uses performance_tagging.tag_line
on plain game_text (bracket tags stripped for heuristics). Appends tags_notes marker.

Examples (project root):
    python scripts/apply_tts_tag_enrichment.py --dry-run
    python scripts/apply_tts_tag_enrichment.py
    python scripts/apply_tts_tag_enrichment.py --sidecar docs/script-rewrite-2026-06-04/tts-tag-enrichment.json
    python scripts/apply_tts_tag_enrichment.py --from-sidecar docs/script-rewrite-2026-06-04/tts-tag-enrichment.json
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

from performance_tagging import count_tags, tag_line
from voice_performance_lib import PERFORMANCE_MANIFEST

ROOT = Path(__file__).resolve().parents[1]
PASS_NOTE = "tts tag pass 2026-06-04"
TAG_RE = re.compile(r"\[[^\]]+\]\s*")
# Ren'Py substitution tokens in dialogue — not ElevenLabs performance tags.
GAME_VAR_BRACKET_RE = re.compile(r"^\[(case\d+_|suspect|player)[^\]]*\]", re.I)


def game_text_has_performance_tags(text: str) -> bool:
    """True when bracket segments look like ElevenLabs tags, not [case4_suspect_name] vars."""
    if not text:
        return False
    if GAME_VAR_BRACKET_RE.match(text.strip()):
        return False
    return strip_performance_tags(text) != text.strip()


def warn_game_text_tags(data: dict) -> int:
    """Print stderr warnings for entries whose game_text still contains TTS tags."""
    n = 0
    for entry in data.get("entries", []):
        gt = entry.get("game_text", "")
        if game_text_has_performance_tags(gt):
            print(
                f"WARN: {entry.get('id')} game_text contains performance tags; "
                "strip before sync (tags belong on tts_text only).",
                file=sys.stderr,
            )
            n += 1
    return n


def strip_performance_tags(text: str) -> str:
    """Remove bracket tags for heuristic tagging; preserve spoken words."""
    return TAG_RE.sub("", text).strip()


def append_pass_note(notes: str) -> str:
    notes = (notes or "").strip()
    if PASS_NOTE.lower() in notes.lower():
        return notes
    return f"{notes}; {PASS_NOTE}" if notes else PASS_NOTE


def spoken_matches_game(tts: str, game_text: str) -> bool:
    return strip_performance_tags(tts) == strip_performance_tags(game_text)


def needs_enrichment(tts: str) -> bool:
    if not (tts or "").startswith("["):
        return True
    return count_tags(tts) <= 1


def _update_counts(data: dict) -> None:
    from performance_tagging import MIN_TAGS_PER_LINE

    entries = data.get("entries", [])
    by_char: dict[str, int] = {}
    for e in entries:
        c = e.get("character", "?")
        by_char[c] = by_char.get(c, 0) + 1
    data["counts"] = {
        "total": len(entries),
        "toa": by_char.get("toa", 0),
        "kaoru": by_char.get("kaoru", 0),
        "narrator": by_char.get("narrator", 0),
        "tagged_tts": sum(1 for e in entries if e.get("tts_text") != e.get("game_text")),
        "min_two_tags": sum(1 for e in entries if count_tags(e.get("tts_text", "")) >= MIN_TAGS_PER_LINE),
        "orphans": data.get("counts", {}).get("orphans", 0),
    }


def apply_from_sidecar(data: dict, sidecar_path: Path) -> int:
    rows = json.loads(sidecar_path.read_text(encoding="utf-8"))
    by_id = {e["id"]: e for e in data.get("entries", [])}
    changed = 0
    for row in rows:
        lid = row["id"]
        entry = by_id.get(lid)
        if not entry:
            print(f"WARN: missing id {lid}", file=sys.stderr)
            continue
        new_tts = row["tts_text"]
        if entry.get("tts_text") == new_tts:
            continue
        if not spoken_matches_game(new_tts, entry.get("game_text", "")):
            print(f"WARN: {lid} tts spoken text != game_text", file=sys.stderr)
            continue
        entry["tts_text"] = new_tts
        entry["tags_notes"] = append_pass_note(entry.get("tags_notes", ""))
        entry["model_hint"] = "eleven_v3"
        changed += 1
    return changed


def enrich_manifest(data: dict, *, dry_run: bool) -> tuple[int, list[dict]]:
    changed_rows: list[dict] = []
    changed = 0
    for entry in data.get("entries", []):
        old_tts = entry.get("tts_text", entry.get("game_text", ""))
        if not needs_enrichment(old_tts):
            continue
        game_text = entry.get("game_text", "")
        plain = strip_performance_tags(game_text)
        lid = entry.get("id", "")
        character = entry.get("character", "")
        source = entry.get("source", "")
        new_tts, _notes, model = tag_line(character, plain, lid, source)
        if not spoken_matches_game(new_tts, game_text):
            # tag_line may have altered words; fall back to plain + tags only on lead
            from performance_tagging import ensure_min_tags

            body = plain
            new_tts = ensure_min_tags(old_tts if old_tts.startswith("[") else body, character, lid, plain)
            if not new_tts.startswith("["):
                new_tts = ensure_min_tags(body, character, lid, plain)
            model = "eleven_v3" if count_tags(new_tts) > 0 else entry.get("model_hint", "eleven_v3")
        if new_tts == old_tts:
            continue
        changed += 1
        changed_rows.append({"id": lid, "tts_text": new_tts})
        if not dry_run:
            entry["tts_text"] = new_tts
            entry["tags_notes"] = append_pass_note(entry.get("tags_notes", ""))
            entry["model_hint"] = model
    return changed, changed_rows


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument(
        "--sidecar",
        type=Path,
        help="Write {id, tts_text} rows instead of updating manifest (unless --from-sidecar).",
    )
    ap.add_argument(
        "--from-sidecar",
        type=Path,
        help="Apply a previously written sidecar to the manifest.",
    )
    ap.add_argument("--manifest", type=Path, default=PERFORMANCE_MANIFEST)
    args = ap.parse_args()

    data = json.loads(args.manifest.read_text(encoding="utf-8"))
    warn_game_text_tags(data)

    if args.from_sidecar:
        changed = apply_from_sidecar(data, args.from_sidecar)
        if not args.dry_run:
            _update_counts(data)
            args.manifest.write_text(
                json.dumps(data, ensure_ascii=False, indent=2) + "\n",
                encoding="utf-8",
            )
        print(f"applied sidecar: {changed} entries")
        return 0

    changed, rows = enrich_manifest(data, dry_run=args.dry_run)

    if args.sidecar:
        args.sidecar.parent.mkdir(parents=True, exist_ok=True)
        args.sidecar.write_text(
            json.dumps(rows, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
        print(f"sidecar written: {args.sidecar} ({len(rows)} rows)")

    if not args.dry_run and not args.sidecar:
        _update_counts(data)
        args.manifest.write_text(
            json.dumps(data, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )

    print(f"{'would change' if args.dry_run else 'changed'}: {changed}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
