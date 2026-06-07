#!/usr/bin/env python3
import json
from pathlib import Path

data = json.loads(Path("docs/_canon_hand_audit.json").read_text(encoding="utf-8"))
print("=== ALL HIGH RISK HAND COUNTS (MediaPipe) ===")
for r in sorted([x for x in data if x.get("high_risk")], key=lambda x: x["png"]):
    mp = r.get("mediapipe") or {}
    res = mp.get("results", [])
    hc = res[0]["hand_count"] if res else "?"
    w = res[0].get("warnings", []) if res else []
    print(f"{r['png']}\t{hc}\t{w}")

print("\n=== DETECTED > 4 HANDS ===")
for r in data:
    mp = r.get("mediapipe") or {}
    res = mp.get("results", [])
    if not res:
        continue
    hc = res[0]["hand_count"]
    if hc > 4:
        print(r["png"], hc, res[0].get("warnings"))

print("\n=== DETECTED 3-4 ON HIGH RISK ===")
for r in data:
    if not r.get("high_risk"):
        continue
    mp = r.get("mediapipe") or {}
    res = mp.get("results", [])
    if not res:
        continue
    hc = res[0]["hand_count"]
    if 3 <= hc <= 4:
        print(r["png"], hc, res[0].get("warnings"))
