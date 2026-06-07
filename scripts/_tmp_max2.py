import json
from pathlib import Path
ROOT = Path(r"C:/Users/Amanda/Developer/ryoko-owari/scripts")

def all_ids(path):
    d = json.loads(path.read_text(encoding="utf-8"))
    if "lines" in d:
        return [r["id"] for r in d["lines"]]
    ent = d.get("entries")
    if isinstance(ent, dict):
        return list(ent.keys())
    if isinstance(ent, list):
        return [e["id"] if isinstance(e, dict) else e for e in ent]
    return []

def max_nums(id_list):
    mx = {"toa": 0, "kaoru": 0, "narrator": 0}
    for vid in id_list:
        for p in mx:
            if str(vid).startswith(p + "_"):
                mx[p] = max(mx[p], int(str(vid).split("_", 1)[1]))
    return mx

allv = []
for fname in ["voice_manifest.json", "narrator_manifest.json", "voice_performance_manifest.json"]:
    ids = all_ids(ROOT / fname)
    mx = max_nums(ids)
    print(fname, len(ids), mx)
    allv.extend(ids)
print("COMBINED", max_nums(allv))
