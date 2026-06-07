import json, re
from pathlib import Path
root = Path('.')
pat = re.compile(r'voice "audio/voice/([^"]+)\.mp3"')
wired = set()
menu_blocks = 0
menu_with_voice_near = 0
for p in (root/'game').rglob('*.rpy'):
    lines = p.read_text(encoding='utf-8', errors='replace').splitlines()
    wired.update(pat.findall('\n'.join(lines)))
    in_menu = False
    for i, line in enumerate(lines):
        if re.match(r'^\s*menu\s*:', line):
            in_menu = True
            menu_blocks += 1
        elif in_menu and line.strip() and not line.strip().startswith('#'):
            if not line[0].isspace() and not line.strip().startswith('"'):
                in_menu = False
        if in_menu and re.match(r'^\s+"', line):
            # choice line - check voice within next 5 lines in same block? simplistic
            pass
legacy = root/'game'/'audio'/'voice'
stub_ids = []
for spec in [
    'kaoru_37{}'.format(i) for i in range(4,10)
]:
    pass
# explicit stub ranges from user
ranges = []
for prefix, start, end in [('kaoru',374,383),('toa',308,317),('narrator',297,303)]:
    for n in range(start, end+1):
        ranges.append(f'{prefix}_{n}')
for i in ranges:
    if not (legacy/(i+'.mp3')).exists():
        stub_ids.append(i)
print('wired', len(wired))
print('stub_range_missing', len(stub_ids), stub_ids[:20])
print('placeholder narrator_NNN wired', 'narrator_NNN' in wired)
# manifests
wired_in_rpy = wired
for name in ['voice_manifest.json','narrator_manifest.json','voice_performance_manifest.json']:
    p = root/'scripts'/name
    data = json.loads(p.read_text(encoding='utf-8'))
    if isinstance(data, dict):
        if 'lines' in data:
            entries = data['lines']
        elif 'entries' in data:
            entries = data['entries']
        else:
            entries = [v for v in data.values() if isinstance(v, dict)]
    else:
        entries = data
    ids = []
    for e in entries:
        if isinstance(e, dict):
            ids.append(e.get('id') or e.get('line_id'))
    ids = [str(i) for i in ids if i]
    no_mp3 = [i for i in ids if not (legacy/(i+'.mp3')).exists()]
    not_wired = [i for i in ids if i not in wired_in_rpy]
    print(name, 'entries', len(ids), 'no_mp3', len(no_mp3), 'not_wired', len(not_wired))
