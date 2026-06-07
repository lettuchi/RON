import json
from pathlib import Path
d=json.loads(Path(r"C:/Users/Amanda/Developer/ryoko-owari/scripts/voice_performance_manifest.json").read_text(encoding="utf-8"))
e=d["entries"]
if isinstance(e, list):
    print("list", e[0].keys(), e[0])
else:
    k=next(iter(e))
    print("dict sample key", k, e[k])
