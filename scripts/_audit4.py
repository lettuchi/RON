from pathlib import Path
legacy = Path('game/audio/voice')
def check_range(prefix, start, end):
    miss = [f'{prefix}_{n}' for n in range(start, end+1) if not (legacy/f'{prefix}_{n}.mp3').exists()]
    return miss
for args in [('kaoru',374,383),('toa',308,317),('narrator',297,303),('kaoru',335,400),('toa',281,320),('narrator',272,310)]:
    m = check_range(*args)
    print(args, 'missing', len(m), m[:10])
# case5 comment stubs - sample high ids
import re
from pathlib import Path
for fn in ['case5_investigation.rpy','epilogue_romance_bonus.rpy']:
    t = Path('game')/fn
    if t.exists():
        ids = re.findall(r'voice "audio/voice/([^"]+)\.mp3"', t.read_text(encoding='utf-8'))
        miss = [i for i in ids if not (legacy/(i+'.mp3')).exists()]
        print(fn, 'wired in file', len(set(ids)), 'missing mp3', len(set(miss)))
