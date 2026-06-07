import json
from pathlib import Path

vm = json.loads(Path("scripts/voice_manifest.json").read_text(encoding="utf-8"))
ids = [l["id"] for l in vm["lines"]]

def maxn(p):
    nums = [int(i.split("_")[1]) for i in ids if i.startswith(p + "_")]
    return max(nums) if nums else 0

print("toa", maxn("toa"), "kaoru", maxn("kaoru"), "narrator", maxn("narrator"))
