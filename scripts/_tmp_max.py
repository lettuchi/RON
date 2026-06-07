import json
from pathlib import Path
ROOT = Path(r"C:/Users/Amanda/Developer/ryoko-owari/scripts")

def ids_from_manifest(path):
    d = json.loads(path.read_text(encoding="utf-8"))
    if "lines" in d:
        return [r["id"] for r in d["lines"]]
    return list(d["entries"].keys())

def max_nums(ids):
    mx = {"toa": 0, "kaoru": 0, "narrator": 0}
    for vid in ids:
        for p in mx:
            if vid.startswith(p + "_"):
                mx[p] = max(mx[p], int(vid.split("_", 1)[1]))
    return mx

for fname in ["voice_manifest.json", "narrator_manifest.json", "voice_performance_manifest.json"]:
    mx = max_nums(ids_from_manifest(ROOT / fname))
    print(fname, mx)
