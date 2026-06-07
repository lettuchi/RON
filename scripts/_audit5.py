import json
from pathlib import Path
# manifest ids for case1 ranges - unwired with mp3?
import re
wired = set()
pat = re.compile(r'voice "audio/voice/([^"]+)\.mp3"')
for p in Path('game').rglob('*.rpy'):
    for line in p.read_text(encoding='utf-8', errors='replace').splitlines():
        if line.lstrip().startswith('#'):
            continue
        m = pat.search(line)
        if m and re.match(r'^\s*voice ', line):
            wired.add(m.group(1))
legacy = Path('game/audio/voice')
for prefix, lo, hi in [('toa',303,303),('toa',312,312),('toa',319,320)]:
    i = f'{prefix}_{lo}' if lo==hi else None
for spec in ['toa_303','toa_312','toa_319','toa_320'] + [f'kaoru_{n}' for n in range(387,397)]:
    print(spec, 'mp3', (legacy/f'{spec}.mp3').exists(), 'wired', spec in wired)
