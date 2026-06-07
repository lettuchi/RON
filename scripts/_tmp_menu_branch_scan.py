import re
from pathlib import Path

ROOT = Path(r"C:/Users/Amanda/Developer/ryoko-owari")
VOICE_RE = re.compile(r'^\s*voice\s+"audio/voice/(\w+)\.mp3"')
DIALOGUE_RE = re.compile(r'^\s*(kaoru|toa|narrator)\s+"')
CHOICE_RE = re.compile(r'^\s+"([^"]+)":\s*$')

def scan_menus(rel):
    lines = (ROOT / rel).read_text(encoding="utf-8").splitlines()
    i = 0
    branch_gaps = []
    while i < len(lines):
        if re.match(r'^\s*menu\s+', lines[i]) or lines[i].strip() == 'menu:':
            menu_line = i + 1
            menu_indent = len(lines[i]) - len(lines[i].lstrip())
            i += 1
            while i < len(lines):
                cur_indent = len(lines[i]) - len(lines[i].lstrip()) if lines[i].strip() else menu_indent + 4
                if lines[i].strip() and not lines[i].strip().startswith('#'):
                    if cur_indent <= menu_indent and not CHOICE_RE.match(lines[i]):
                        break  # left menu block
                m = CHOICE_RE.match(lines[i])
                if m:
                    choice = m.group(1)[:60]
                    i += 1
                    unwired = []
                    while i < len(lines):
                        if not lines[i].strip():
                            i += 1
                            continue
                        ind = len(lines[i]) - len(lines[i].lstrip())
                        if CHOICE_RE.match(lines[i]) and ind > menu_indent:
                            break  # next choice
                        if ind <= menu_indent and not lines[i].strip().startswith('#'):
                            break  # merge path
                        dm = DIALOGUE_RE.match(lines[i])
                        if dm and not lines[i].strip().startswith('#'):
                            has_v = any(VOICE_RE.match(lines[j]) for j in range(max(0,i-4), i))
                            if not has_v:
                                unwired.append((i+1, dm.group(1), lines[i].strip()[:85]))
                        i += 1
                    if unwired:
                        branch_gaps.append((menu_line, choice, unwired))
                    continue
                i += 1
            continue
        i += 1
    return branch_gaps

total = 0
for p in ["game/case1_companion.rpy", "game/case1_investigation.rpy"]:
    bg = scan_menus(p)
    print("===", p, "branches with gaps:", len(bg))
    for menu_ln, choice, uw in bg:
        total += len(uw)
        print(f"  menu@{menu_ln} choice={choice!r} lines={len(uw)}")
        for u in uw:
            print("   ", u)
print("total unwired lines in menu branches:", total)
