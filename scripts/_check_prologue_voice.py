from pathlib import Path
t=Path('game/kaoru_pro_prologue.rpy').read_text(encoding='utf-8')
ids=[f'narrator_{i}' for i in range(312,366)]+[f'kaoru_{i}' for i in range(387,426)]
miss=[i for i in ids if ('voice "audio/voice/%s.mp3"'%i) not in t]
print('prologue voice lines for case zero ids:', len(ids)-len(miss), '/', len(ids))
print('missing voice stmt:', miss[:5], 'count', len(miss))
