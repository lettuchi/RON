import json, re
from pathlib import Path
# Lines in rpy: kaoru/toa/narrator dialogue without preceding voice in same block (heuristic)
root = Path('game')
chars = ('kaoru', 'toa', 'narrator')
# skip narrator if only quoted strings with narrator character - also bare strings after label
unvoiced = []
for p in root.rglob('*.rpy'):
    lines = p.read_text(encoding='utf-8', errors='replace').splitlines()
    prev_voice = False
    for i, line in enumerate(lines):
        stripped = line.strip()
        if stripped.startswith('#'):
            continue
        if re.match(r'^\s*voice "audio/voice/', line):
            prev_voice = True
            continue
        m = re.match(r'^\s*(kaoru|toa|narrator)\s+"', line)
        m2 = re.match(r'^\s+"', line) and 'narrator' in str(p)  # bare narrator string
        if m or (re.match(r'^\s+"', line) and not re.match(r'^\s+"[^"]+":', line)):
            if not prev_voice and m:
                unvoiced.append((str(p), i+1, line.strip()[:80]))
            prev_voice = False
        elif stripped and not stripped.startswith('$') and not stripped.startswith('show') and not stripped.startswith('scene'):
            if not re.match(r'^\s+"[^"]+":', line):
                prev_voice = False
print('character lines possibly missing voice (heuristic):', len(unvoiced))
for x in unvoiced[:25]:
    print(x)
