#!/usr/bin/env python3
"""Fail if a voice stmt is followed by 2+ say lines before the next code line."""
import re
from pathlib import Path

GAME = Path(__file__).resolve().parents[1] / "game"
VOICE_RE = re.compile(r'^\s*voice\s+"audio/voice/\w+\.mp3"\s*$')
SAY_RE = re.compile(r'^\s+(".*"|(kaoru|toa)\s+".*")\s*$')
CODE_RE = re.compile(
    r"^\s*(menu\s|label\s|\$\s|show\s|scene\s|play\s|pause\s|jump\s|if\s|return\b|centered\s)"
)

violations = []
for rpy in sorted(GAME.glob("au_modern*.rpy")):
    lines = rpy.read_text(encoding="utf-8").splitlines()
    for i, line in enumerate(lines):
        if not VOICE_RE.match(line):
            continue
        says = 0
        j = i + 1
        while j < len(lines):
            s = lines[j].strip()
            if not s or s.startswith("#"):
                j += 1
                continue
            if CODE_RE.match(lines[j]) or VOICE_RE.match(lines[j]):
                break
            if SAY_RE.match(lines[j]):
                says += 1
                j += 1
                continue
            break
        if says > 1:
            violations.append((rpy.name, i + 1, says))

if violations:
    print(f"FAIL: {len(violations)} multi-say voice blocks remain")
    for v in violations[:20]:
        print(f"  {v[0]}:{v[1]} ({v[2]} say lines)")
else:
    print("OK: no voice blocks with multiple say lines")
