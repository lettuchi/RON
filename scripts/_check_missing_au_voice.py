#!/usr/bin/env python3
import re
from pathlib import Path

GAME = Path(__file__).resolve().parents[1] / "game"
VOICE_DIR = GAME / "audio" / "voice"
VOICE_RE = re.compile(r'voice\s+"audio/voice/(\w+)\.mp3"')
missing = []
for rpy in sorted(GAME.glob("au_modern*.rpy")):
    for m in VOICE_RE.finditer(rpy.read_text(encoding="utf-8")):
        vid = m.group(1)
        if not (VOICE_DIR / f"{vid}.mp3").exists():
            missing.append((rpy.name, vid))
print(f"missing count: {len(missing)}")
for name, vid in sorted(set(missing)):
    print(f"  {name}: {vid}")
