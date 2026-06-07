import re
from pathlib import Path
root = Path('game')
# Find menu branches with dialogue lacking voice on first lines
issues = []
for p in root.rglob('*.rpy'):
    lines = p.read_text(encoding='utf-8', errors='replace').splitlines()
    i = 0
    while i < len(lines):
        if re.match(r'^\s*menu\b', lines[i]):
            i += 1
            while i < len(lines):
                line = lines[i]
                if line.strip().startswith('#'):
                    i += 1
                    continue
                m = re.match(r'^\s+"([^"]+)":\s*$', line)
                if m:
                    choice = m.group(1)
                    i += 1
                    branch_unvoiced = []
                    while i < len(lines):
                        l = lines[i]
                        if re.match(r'^\s+"[^"]+":\s*$', l):
                            break
                        if re.match(r'^\s*\w+\s*:', l) and not l.strip().startswith('$'):
                            break
                        if re.match(r'^\s*(kaoru|toa|narrator)\s+"', l):
                            if not any('voice "audio/voice/' in x for x in lines[max(i-3,0):i]):
                                branch_unvoiced.append(l.strip()[:70])
                        if re.match(r'^\s+"', l) and not re.match(r'^\s+"[^"]+":', l):
                            if not any('voice "audio/voice/' in x for x in lines[max(i-3,0):i]):
                                branch_unvoiced.append('(narr) '+l.strip()[:60])
                        if re.match(r'^\s*jump\s+', l) or re.match(r'^\s*return\b', l):
                            break
                        i += 1
                    if branch_unvoiced:
                        issues.append((p.name, choice[:50], branch_unvoiced[:3]))
                    continue
                if line and not line[0].isspace():
                    break
                i += 1
            continue
        i += 1
print('menu branches with unvoiced dialogue lines:', len(issues))
for row in issues[:20]:
    print(row[0], '|', row[1], '|', row[2])
