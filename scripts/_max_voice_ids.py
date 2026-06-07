#!/usr/bin/env python3
import json
from pathlib import Path

vm = json.loads((Path(__file__).resolve().parents[1] / "scripts/voice_manifest.json").read_text(encoding="utf-8"))
ids = [r["id"] for r in vm["lines"]]

def maxn(p):
    nums = [int(x.split("_")[1]) for x in ids if x.startswith(p + "_")]
    return max(nums) if nums else 0

for p in ("toa", "kaoru", "narrator"):
    print(p, maxn(p))
