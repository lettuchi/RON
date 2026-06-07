from pathlib import Path
import re, json, importlib.util

ROOT = Path('.')
# fix duplicate voice in companion
comp = ROOT / 'game/case1_companion.rpy'
lines = comp.read_text(encoding='utf-8').splitlines()
out = []
skip_next_dup = False
for i, line in enumerate(lines):
    if i > 0 and line.strip() == 'voice "audio/voice/kaoru_426.mp3"' and lines[i-1].strip() == 'voice "audio/voice/kaoru_430.mp3"':
        continue  # drop duplicate kaoru_426
    out.append(line)
if out != lines:
    comp.write_text('\n'.join(out) + '\n', encoding='utf-8')
    print('fixed duplicate voice')

# wire merge path in investigation
inv = ROOT / 'game/case1_investigation.rpy'
lines = inv.read_text(encoding='utf-8').splitlines()
targets = []
for idx, line in enumerate(lines):
    if line.strip().startswith('toa "A flower-named Scorpion'):
        if idx > 0 and 'voice ' not in lines[idx-1]:
            targets.append((idx, 'toa_338', 'toa'))
    if line.strip().startswith('kaoru "The registry book, okami'):
        if idx > 0 and 'voice ' not in lines[idx-1]:
            targets.append((idx, 'kaoru_449', 'kaoru'))

if targets:
    spec = importlib.util.spec_from_file_location('g', ROOT/'scripts/generate_case1_sidecar.py')
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    vm = json.loads((ROOT/'scripts/voice_manifest.json').read_text(encoding='utf-8'))
    pm = json.loads((ROOT/'scripts/voice_performance_manifest.json').read_text(encoding='utf-8'))
    existing = {l['id'] for l in vm['lines']}
    perf = {e['id'] for e in pm['entries']}
    for idx, vid, char in sorted(targets, reverse=True):
        line = lines[idx]
        m = re.match(r'^(\s*)(kaoru|toa)\s+"(.*)"\s*$', line)
        indent, _, text = m.group(1), m.group(2), m.group(3)
        lines.insert(idx, f'{indent}voice "audio/voice/{vid}.mp3"')
        if vid not in existing:
            vm['lines'].append({'id': vid, 'character': char, 'text': text})
            existing.add(vid)
        if vid not in perf:
            tts = mod.make_tts(char, vid, text)
            pm['entries'].append({'id': vid, 'character': char, 'source': f'game/case1_investigation.rpy:{idx+1}', 'game_text': text, 'tts_text': tts, 'tags_notes': 'case1 merge-path wire 2026-06-04', 'model_hint': 'eleven_v3'})
            perf.add(vid)
        print('wired', vid, 'at', idx+1)
    inv.write_text('\n'.join(lines) + '\n', encoding='utf-8')
    (ROOT/'scripts/voice_manifest.json').write_text(json.dumps(vm, indent=2, ensure_ascii=False)+'\n', encoding='utf-8')
    (ROOT/'scripts/voice_performance_manifest.json').write_text(json.dumps(pm, indent=2, ensure_ascii=False)+'\n', encoding='utf-8')
else:
    print('merge path already wired or not found')

# rebuild id lists
cz = [f'narrator_{i}' for i in range(312,366)] + [f'kaoru_{i}' for i in range(387,426)]
(ROOT/'scripts/case_zero_voice_ids.txt').write_text('\n'.join(cz)+'\n', encoding='utf-8')
ids=[]
for rel in ['game/case1_companion.rpy','game/case1_investigation.rpy']:
    for m in re.finditer(r'voice "audio/voice/(\w+)\.mp3"', (ROOT/rel).read_text(encoding='utf-8')):
        vid = m.group(1)
        if not (ROOT/f'game/audio/voice/{vid}.mp3').exists():
            ids.append(vid)
ids = sorted(set(ids), key=lambda x:(x.split('_')[0], int(x.split('_')[1])))
(ROOT/'scripts/case1_unwired_voice_ids.txt').write_text('\n'.join(ids)+'\n', encoding='utf-8')
print('case_zero ids', len(cz))
print('case1 regen ids', len(ids))
