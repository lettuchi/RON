from pathlib import Path
import re
ROOT=Path('.')
ids=[]
for rel in ['game/case1_companion.rpy','game/case1_investigation.rpy']:
    for m in re.finditer(r'voice "audio/voice/(\w+)\.mp3"', (ROOT/rel).read_text(encoding='utf-8')):
        vid = m.group(1)
        if int(re.search(r'\d+', vid).group()) >= 319 and vid.split('_')[0] in ('toa','kaoru'):
            ids.append(vid)
ids=sorted(set(ids), key=lambda x:(x.split('_')[0], int(x.split('_')[1])))
wired_high = len(ids)
missing=[i for i in ids if not (ROOT/f'game/audio/voice/{i}.mp3').exists()]
print('wired_high_band', wired_high)
print('missing', len(missing))
