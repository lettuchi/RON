import re
from pathlib import Path
# Analyze menus: after menu:, choice strings rarely have voice on choice text
root = Path('game')
for p in root.rglob('*.rpy'):
    lines = p.read_text(encoding='utf-8', errors='replace').splitlines()
    for i, line in enumerate(lines):
        if re.match(r'^\s*menu\s*:', line):
            block = lines[i:i+80]
            choices = [l for l in block if re.match(r'^\s+"[^"]+":', l)]
            voices = [l for l in block if 'voice "audio/voice/' in l and not l.lstrip().startswith('#')]
            print(p.name, 'line', i+1, 'choices', len(choices), 'voices in block', len(voices))
