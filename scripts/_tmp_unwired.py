import re
from pathlib import Path

ROOT = Path(r"C:/Users/Amanda/Developer/ryoko-owari")

SPEAK_RE = [
    re.compile(r'^\s*(kaoru|toa|narrator)\s+"'),
    re.compile(r'^\s*"\s*'),  # narrator anonymous?
]
VOICE_RE = re.compile(r'^\s*voice\s+"audio/voice/(\w+)\.mp3"')

def is_dialogue(line):
    s = line.strip()
    if not s or s.startswith("#"):
        return False, None
    m = re.match(r'^\s*(kaoru|toa|narrator)\s+"', line)
    if m:
        return True, m.group(1)
    # character say via quotes only after voice - skip
    return False, None

def scan(path):
    lines = (ROOT / path).read_text(encoding="utf-8").splitlines()
    unwired = []
    for i, line in enumerate(lines):
        ok, who = is_dialogue(line)
        if not ok:
            continue
        prev_voice = False
        for j in range(i - 1, max(-1, i - 6), -1):
            pj = lines[j].strip()
            if not pj or pj.startswith("#"):
                continue
            if VOICE_RE.match(lines[j]):
                prev_voice = True
                break
            # stop at another dialogue line
            if is_dialogue(lines[j])[0]:
                break
            if pj.startswith(("menu", "label ", "jump ", "if ", "elif ", "else:")):
                break
        if not prev_voice:
            unwired.append((i + 1, who, line.strip()[:90]))
    return unwired

for p in ["game/case1_companion.rpy", "game/case1_investigation.rpy"]:
    u = scan(p)
    print(p, len(u))
    for x in u:
        print(" ", x)
