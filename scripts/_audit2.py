import json, re
from pathlib import Path
root = Path('.')
legacy = root/'game'/'audio'/'voice'
pat = re.compile(r'voice "audio/voice/([^"]+)\.mp3"')
wired = set()
for p in (root/'game').rglob('*.rpy'):
    wired.update(pat.findall(p.read_text(encoding='utf-8', errors='replace')))
# not wired in manifest
for name in ['voice_manifest.json','narrator_manifest.json']:
    data = json.loads((root/'scripts'/name).read_text(encoding='utf-8'))
    entries = data['lines'] if 'lines' in data else data
    ids = [e['id'] for e in entries if isinstance(e, dict) and e.get('id')]
    nw = sorted(set(ids) - wired)
    print(name, 'not_wired sample', nw[:15], 'count', len(nw))
# performance not wired
perf = json.loads((root/'scripts'/'voice_performance_manifest.json').read_text(encoding='utf-8'))
ids = [e.get('id') for e in perf if isinstance(e, dict)]
nw = sorted(set(str(i) for i in ids if i) - wired)
print('perf not_wired', len(nw))
print('sample', nw[:20])
# toa_312
print('toa_312 legacy exists', (legacy/'toa_312.mp3').exists())
print('toa_312 wired', 'toa_312' in wired)
v2 = root/'game'/'audio'/'voice'/'v2'/'eve-donovan-2026-06-04'/'toa_312.mp3'
print('v2 exists', v2.exists())
# find narrator_NNN
for p in (root/'game').rglob('*.rpy'):
    if 'narrator_NNN' in p.read_text(encoding='utf-8', errors='replace'):
        print('NNN in', p)
