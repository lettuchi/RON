import re
from pathlib import Path
root = Path('.')
pat = re.compile(r'^\s*voice "audio/voice/([^"]+)\.mp3"', re.M)
pat_comment = re.compile(r'^\s*#.*voice "audio/voice/')
wired = set()
comment_false = set()
for p in (root/'game').rglob('*.rpy'):
    text = p.read_text(encoding='utf-8', errors='replace')
    for line in text.splitlines():
        m = re.search(r'voice "audio/voice/([^"]+)\.mp3"', line)
        if not m:
            continue
        if line.lstrip().startswith('#'):
            comment_false.add(m.group(1))
            continue
        if re.match(r'^\s*voice ', line):
            wired.add(m.group(1))
legacy = root/'game'/'audio'/'voice'
missing = sorted(i for i in wired if not (legacy/(i+'.mp3')).exists())
print('wired executable', len(wired))
print('comment false positives', comment_false)
print('missing', missing)
