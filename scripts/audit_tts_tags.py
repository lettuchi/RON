#!/usr/bin/env python3
"""Report TTS tag coverage in voice_performance_manifest.json.

Examples (project root):
    python scripts/audit_tts_tags.py
    python scripts/audit_tts_tags.py --prefix case5
    python scripts/audit_tts_tags.py --prefix case1_5 --thin-only
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "scripts" / "voice_performance_manifest.json"
TAG_RE = re.compile(r"\[[^\]]+\]")


def count_tags(tts_text: str) -> int:
    return len(TAG_RE.findall(tts_text or ""))


def source_prefix(source: str) -> str:
    if not source:
        return "unknown"
    base = source.split(":")[0]
    return base.replace(".rpy", "")


def load_entries(path: Path) -> list[dict]:
    data = json.loads(path.read_text(encoding="utf-8"))
    return data.get("entries", [])


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument(
        "--manifest",
        type=Path,
        default=MANIFEST,
        help="Path to voice_performance_manifest.json",
    )
    ap.add_argument(
        "--prefix",
        action="append",
        default=[],
        help="Filter by source file prefix (e.g. case5, case1_5, prologue). Repeatable.",
    )
    ap.add_argument(
        "--thin-only",
        action="store_true",
        help="Only list entries with 0-1 tags (not just missing leading tag).",
    )
    ap.add_argument("--ids", action="store_true", help="Print matching entry ids.")
    args = ap.parse_args()

    entries = load_entries(args.manifest)
    prefixes = tuple(args.prefix)

    no_lead: list[dict] = []
    thin: list[dict] = []

    for entry in entries:
        src = entry.get("source", "")
        if prefixes and not any(source_prefix(src).startswith(p) for p in prefixes):
            continue
        tts = entry.get("tts_text", "")
        n = count_tags(tts)
        if not (tts or "").startswith("["):
            no_lead.append(entry)
        if n <= 1:
            thin.append(entry)

    total = len(entries)
    filtered = [
        e
        for e in entries
        if not prefixes or any(source_prefix(e.get("source", "")).startswith(p) for p in prefixes)
    ]

    print(f"manifest: {args.manifest}")
    print(f"entries (total): {total}")
    if prefixes:
        print(f"entries (filtered {prefixes!r}): {len(filtered)}")
    print(f"no leading tag: {len(no_lead)}")
    print(f"0-1 tags: {len(thin)}")

    by_prefix: dict[str, list[str]] = defaultdict(list)
    for entry in no_lead:
        by_prefix[source_prefix(entry.get("source", ""))].append(entry["id"])

    if by_prefix:
        print("\nno leading tag by source prefix:")
        for key in sorted(by_prefix, key=lambda k: -len(by_prefix[k])):
            print(f"  {key}: {len(by_prefix[key])}")

    show = thin if args.thin_only else no_lead
    if args.ids and show:
        print("\nids:")
        for entry in show:
            n = count_tags(entry.get("tts_text", ""))
            print(f"  {entry['id']} ({n} tags) {entry.get('character')} {entry.get('source', '')[:50]}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
