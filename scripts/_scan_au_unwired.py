#!/usr/bin/env python3
"""Scan au_modern*.rpy for say/narration lines without preceding voice stmt."""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GAME = ROOT / "game"
VOICE_RE = re.compile(r'voice\s+"audio/voice/(\w+)\.mp3"')
SAY_RE = re.compile(r'^\s*(kaoru|toa|narrator)\s+"(.*)"\s*$')
NARR_RE = re.compile(r'^\s+"(.*)"\s*$')
SKIP_RE = re.compile(
    r'^\s*(menu\s|label\s|\$\s|show\s|scene\s|play\s|pause\s|jump\s|if\s|return\b|centered\s)'
)

unwired = []
for rpy in sorted(GAME.glob("au_modern*.rpy")):
    lines = rpy.read_text(encoding="utf-8").splitlines()
    for i, line in enumerate(lines):
        dm = SAY_RE.match(line)
        nm = None if dm else NARR_RE.match(line)
        if not dm and not nm:
            continue
        who = dm.group(1) if dm else "narrator"
        text = dm.group(2) if dm else nm.group(1)
        prev_voice = False
        j = i - 1
        while j >= 0:
            s = lines[j].strip()
            if not s or s.startswith("#"):
                j -= 1
                continue
            if VOICE_RE.search(lines[j]):
                prev_voice = True
            break
        if not prev_voice:
            unwired.append((rpy.name, i + 1, who, text[:100]))

print(f"Total unwired: {len(unwired)}")
for u in unwired:
    print(f"  {u[0]}:{u[1]} {u[2]} | {u[3]}")
