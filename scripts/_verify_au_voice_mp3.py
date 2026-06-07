#!/usr/bin/env python3
"""Report wired AU Modern voice IDs missing legacy MP3 (and v2)."""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GAME = ROOT / "game"
LEGACY = ROOT / "game/audio/voice"
V2 = LEGACY / "v2/eve-donovan-2026-06-04"
VOICE_RE = re.compile(r'^\s*voice\s+"audio/voice/(\w+)\.mp3"\s*$', re.M)

wired: set[str] = set()
for rpy in GAME.glob("au_modern*.rpy"):
    text = rpy.read_text(encoding="utf-8")
    for m in VOICE_RE.finditer(text):
        wired.add(m.group(1))

missing_legacy = sorted(i for i in wired if not (LEGACY / f"{i}.mp3").is_file())
missing_v2 = sorted(i for i in wired if not (V2 / f"{i}.mp3").is_file())
missing_both = sorted(i for i in wired if not (LEGACY / f"{i}.mp3").is_file() and not (V2 / f"{i}.mp3").is_file())

print(f"au_wired_ids: {len(wired)}")
print(f"missing_legacy: {len(missing_legacy)}")
print(f"missing_v2: {len(missing_v2)}")
print(f"missing_both: {len(missing_both)}")
if missing_both:
    print("missing_both_sample:", missing_both[:30])
if missing_legacy and not missing_both:
    print("legacy_missing_but_v2_ok:", len(missing_legacy), "(promote needed)")
