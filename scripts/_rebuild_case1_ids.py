from pathlib import Path
import re
ROOT=Path('.')
# rebuild clean case1 id list
ids=[]
for rel in ['game/case1_companion.rpy','game/case1_investigation.rpy']:
    for m in re.finditer(r'voice "audio/voice/(\w+)\.mp3"', (ROOT/rel).read_text(encoding='utf-8')):
        vid = m.group(1)
        if vid.startswith(('toa_3','kaoru_4')) and int(vid.split('_')[1])>=319:
            ids.append(vid)
ids=sorted(set(ids), key=lambda x:(x.split('_')[0], int(x.split('_')[1])))
Path('scripts/case1_unwired_voice_ids.txt').write_text('\n'.join(ids)+'\n', encoding='utf-8')
print(len(ids))
