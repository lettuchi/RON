import json, re
from pathlib import Path

ROOT = Path(".")
SCRIPTS = ROOT / "scripts"
REWRITE = ROOT / "docs" / "script-rewrite-2026-06-04"

def load_manifest_ids():
    ids = set()
    vm = json.loads((SCRIPTS / "voice_manifest.json").read_text(encoding="utf-8"))
    for row in vm.get("lines", []):
        if row.get("id"):
            ids.add(row["id"])
    nm = json.loads((SCRIPTS / "narrator_manifest.json").read_text(encoding="utf-8"))
    for row in nm.get("lines", []):
        if row.get("id"):
            ids.add(row["id"])
    pm = json.loads((SCRIPTS / "voice_performance_manifest.json").read_text(encoding="utf-8"))
    for row in pm.get("entries", []):
        if row.get("id"):
            ids.add(row["id"])
    return ids

def keys_from_sidecar(path: Path):
    data = json.loads(path.read_text(encoding="utf-8"))
    if isinstance(data, list):
        return sorted({row["id"] for row in data if isinstance(row, dict) and row.get("id")})
    return []

manifest_ids = load_manifest_ids()
print("manifest id count", len(manifest_ids))

sidecars = [
    ("staged_regen_stage3_case1_ids.txt", "case1-updates.json"),
    ("staged_regen_stage4_case2_ids.txt", "case2-updates.json"),
    ("staged_regen_stage5_case3_ids.txt", "case3-updates.json"),
    ("staged_regen_stage6_case4_ids.txt", "case4-updates.json"),
    ("staged_regen_stage7_caseendings_ids.txt", "caseendings-updates.json"),
]
report = {}
for outname, jname in sidecars:
    keys = keys_from_sidecar(REWRITE / jname)
    use = sorted(k for k in keys if k in manifest_ids)
    missing = sorted(k for k in keys if k not in manifest_ids)
    (SCRIPTS / outname).write_text("\n".join(use) + "\n", encoding="utf-8")
    report[outname] = {"keys": len(keys), "written": len(use), "missing_manifest": len(missing), "sample_missing": missing[:5]}

c15 = REWRITE / "case1_5-updates.json"
if c15.exists():
    extra = sorted(k for k in keys_from_sidecar(c15) if k in manifest_ids)
    s1path = SCRIPTS / "staged_regen_stage1_case1_5_ids.txt"
    s1 = set(s1path.read_text(encoding="utf-8").split())
    s1 |= set(extra)
    s1path.write_text("\n".join(sorted(s1)) + "\n", encoding="utf-8")
    report["stage1_after_c15"] = len(s1)

print(json.dumps(report, indent=2))
