import json, re
from pathlib import Path

ROOT = Path(r"C:/Users/Amanda/Developer/ryoko-owari")

def max_ids():
    for fname in ["voice_manifest.json", "narrator_manifest.json"]:
        data = json.loads((ROOT / "scripts" / fname).read_text(encoding="utf-8"))
        lines = data.get("lines", data) if isinstance(data, dict) else data
        mx = {"toa": 0, "kaoru": 0, "narrator": 0}
        for row in lines:
            vid = row.get("id", row) if isinstance(row, dict) else row
            for p in mx:
                if str(vid).startswith(p + "_"):
                    try:
                        n = int(str(vid).split("_", 1)[1])
                        mx[p] = max(mx[p], n)
                    except ValueError:
                        pass
        print(fname, mx)

def scan_menu_gaps(rpy_path):
    text = (ROOT / rpy_path).read_text(encoding="utf-8")
    lines = text.splitlines()
    results = []
    menu_stack = []
    for i, line in enumerate(lines):
        if line.strip().startswith("#"):
            continue
        if re.match(r"^\s*menu\s*:", line):
            menu_stack.append(i)
        # choice block entry "Label":
        if menu_stack and re.match(r'^\s+"[^"]+":\s*$', line):
            pass
        m = re.match(r'^\s*(kaoru|toa|narrator)\s+"', line)
        if m and menu_stack:
            # only if we're after a menu started and before next menu at same level? simplified: after any menu in file
            has_v = False
            for j in range(max(0, i - 4), i):
                if re.match(r'^\s*voice\s+"', lines[j]) and not lines[j].strip().startswith("#"):
                    has_v = True
            if not has_v:
                results.append((i + 1, m.group(1), line.strip()[:100]))
    return results

max_ids()
for p in ["game/case1_companion.rpy", "game/case1_investigation.rpy"]:
    g = scan_menu_gaps(p)
    print(p, "unwired_after_menu", len(g))
    for row in g:
        print(" ", row)
