#!/usr/bin/env python3
"""Post-sync sanity checks for Modern AU manifests."""
from __future__ import annotations

import json
import re
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
PM_PATH = SCRIPTS / "voice_performance_manifest.json"
OVERFLOW = SCRIPTS / "au_text_overflow_regen_ids.txt"
INTIMACY = SCRIPTS / "au_intimacy_prose_regen_ids.txt"
TAG_RE = re.compile(r"\[[^\]]+\]")
WORD_TOA = re.compile(r"\bToa\b")


def load_ids(path: Path) -> list[str]:
    return [
        ln.strip()
        for ln in path.read_text(encoding="utf-8").splitlines()
        if ln.strip() and not ln.startswith("#")
    ]


def main() -> int:
    pm = {
        e["id"]: e
        for e in json.loads(PM_PATH.read_text(encoding="utf-8"))["entries"]
    }
    au = [e for e in pm.values() if "au_modern" in (e.get("source") or "")]
    no_lead = [e["id"] for e in au if not (e.get("tts_text") or "").strip().startswith("[")]
    thin = [e["id"] for e in au if len(TAG_RE.findall(e.get("tts_text") or "")) < 1]
    narr_toa_plain = []
    for e in au:
        if e["character"] != "narrator":
            continue
        if WORD_TOA.search(e.get("game_text", "")) and WORD_TOA.search(e.get("tts_text", "")):
            narr_toa_plain.append(e["id"])

    print(f"AU performance entries: {len(au)}")
    print(f"no leading tag: {len(no_lead)} -> {no_lead}")
    print(f"0 tags: {len(thin)} -> {thin}")
    print(f"narrator Toa lines still plain Toa in tts (should be Toe-uh): {len(narr_toa_plain)}")
    if narr_toa_plain:
        print(f"  {narr_toa_plain}")

    overflow = load_ids(OVERFLOW)
    mismatch = [
        vid
        for vid in overflow
        if vid in pm and pm[vid].get("tts_text") == pm[vid].get("game_text")
    ]
    print(f"overflow ids with untagged tts (tts==game): {len(mismatch)}")

    print("\n=== intimacy prose ids ===")
    for vid in load_ids(INTIMACY):
        e = pm.get(vid)
        if not e:
            print(f"{vid} MISSING")
            continue
        lead = (e.get("tts_text") or "").strip().startswith("[")
        toe = "Toe-uh" in (e.get("tts_text") or "")
        print(f"{vid} lead={lead} toe-uh={toe} tags={len(TAG_RE.findall(e.get('tts_text','')))}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
