#!/usr/bin/env python3
"""Sync manifests for canon witness / Case 5 clarity pass (manifest-only, no MP3 regen).

Reads IDs from scripts/canon_witness_case5_clarity_regen_ids.txt, pulls on-screen
text from canon game/*.rpy, updates voice_manifest.json / narrator_manifest.json /
voice_performance_manifest.json, and mirrors tts into voice_v2_metadata_manifest.json
when rows exist. Preserves leading emotion/delivery tags and [short pause] pacing.

Run from project root:
    python scripts/sync_canon_witness_case5_clarity.py --audit
    python scripts/sync_canon_witness_case5_clarity.py
"""
from __future__ import annotations

import argparse
import importlib.util
import json
import re
import subprocess
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
GAME = ROOT / "game"
IDS_PATH = SCRIPTS / "canon_witness_case5_clarity_regen_ids.txt"
VM_PATH = SCRIPTS / "voice_manifest.json"
NM_PATH = SCRIPTS / "narrator_manifest.json"
PM_PATH = SCRIPTS / "voice_performance_manifest.json"
V2_PATH = SCRIPTS / "voice_v2_metadata_manifest.json"
SYNC_NOTE = "canon witness case5 clarity sync 2026-06-07"

CANON_FILES = [
    "script.rpy",
    "prologue.rpy",
    "prologue_canon_encounter.rpy",
    "kaoru_pro_prologue.rpy",
    "case1_investigation.rpy",
    "case1_companion.rpy",
    "case1_5_romance_interlude.rpy",
    "case2_investigation.rpy",
    "case2_festival.rpy",
    "case3_investigation.rpy",
    "case3_5_date_interlude.rpy",
    "case4_investigation.rpy",
    "case4_5_boat.rpy",
    "case5_investigation.rpy",
    "case_endings.rpy",
    "epilogue_romance_bonus.rpy",
    "epilogue_rain_gameover.rpy",
]

VOICE_RE = re.compile(r'voice\s+"audio/voice/(\w+)\.mp3"')
DIALOGUE_RE = re.compile(r'^\s*(kaoru|toa|narrator)\s+"(.*)"\s*$')
NARRATION_RE = re.compile(r'^\s+"(.*)"\s*$')


def load_id_list(path: Path) -> list[str]:
    return [
        ln.strip()
        for ln in path.read_text(encoding="utf-8").splitlines()
        if ln.strip() and not ln.startswith("#")
    ]


def extract_canon_rows() -> dict[str, dict]:
    rows: dict[str, dict] = {}
    for name in CANON_FILES:
        path = GAME / name
        if not path.is_file():
            continue
        lines = path.read_text(encoding="utf-8").splitlines()
        pending: str | None = None
        for i, line in enumerate(lines, start=1):
            vm = VOICE_RE.search(line)
            if vm:
                pending = vm.group(1)
                continue
            if not pending:
                continue
            dm = DIALOGUE_RE.match(line)
            if dm:
                char, text = dm.group(1), dm.group(2)
                if pending not in rows:
                    rows[pending] = {
                        "character": char,
                        "game_text": text,
                        "source": f"game/{name}:{i}",
                    }
                pending = None
                continue
            nm = NARRATION_RE.match(line)
            if nm and pending.startswith("narrator_"):
                if pending not in rows:
                    rows[pending] = {
                        "character": "narrator",
                        "game_text": nm.group(1),
                        "source": f"game/{name}:{i}",
                    }
                pending = None
    return rows


def load_resync_helpers():
    spec = importlib.util.spec_from_file_location(
        "au_sync", SCRIPTS / "sync_au_modern_manifests.py"
    )
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.load_make_tts, mod.resync_tts, mod.lead_prefix


def drift_for_ids(target_ids: list[str], rpy_rows: dict[str, dict]) -> dict[str, int]:
    vm = {r["id"]: r["text"] for r in json.loads(VM_PATH.read_text(encoding="utf-8"))["lines"]}
    nm = {r["id"]: r["text"] for r in json.loads(NM_PATH.read_text(encoding="utf-8"))["lines"]}
    pm = {
        e["id"]: e
        for e in json.loads(PM_PATH.read_text(encoding="utf-8"))["entries"]
    }
    out = {"vm": 0, "nm": 0, "pm_game": 0, "pm_tts_stale": 0, "missing_rpy": 0}
    for vid in target_ids:
        r = rpy_rows.get(vid)
        if not r:
            out["missing_rpy"] += 1
            continue
        gt = r["game_text"]
        if vm.get(vid) != gt:
            out["vm"] += 1
        if r["character"] == "narrator" and nm.get(vid) != gt:
            out["nm"] += 1
        pe = pm.get(vid)
        if not pe:
            continue
        if pe.get("game_text") != gt:
            out["pm_game"] += 1
        old_tts = pe.get("tts_text", "")
        old_game = pe.get("game_text", "")
        if old_game != gt and old_tts and old_tts.replace(old_game, gt) == old_tts:
            # tts still contains old body verbatim (no resync yet)
            if old_tts != gt and not old_tts.endswith(gt):
                out["pm_tts_stale"] += 1
    return out


def main() -> int:
    ap = argparse.ArgumentParser(description="Sync canon witness/Case5 clarity manifests.")
    ap.add_argument("--audit", action="store_true", help="Print drift counts only.")
    args = ap.parse_args()

    target_ids = load_id_list(IDS_PATH)
    rpy_rows = extract_canon_rows()
    pre = drift_for_ids(target_ids, rpy_rows)

    if args.audit:
        print(f"target ids: {len(target_ids)}")
        for k, v in pre.items():
            print(f"{k}: {v}")
        for vid in target_ids:
            r = rpy_rows.get(vid)
            if not r:
                print(f"MISSING rpy: {vid}")
                continue
            vm = {
                row["id"]: row["text"]
                for row in json.loads(VM_PATH.read_text(encoding="utf-8"))["lines"]
            }
            if vm.get(vid) != r["game_text"]:
                print(f"DRIFT {vid}")
                print(f"  manifest: {vm.get(vid, '')[:120]}")
                print(f"  rpy:      {r['game_text'][:120]}")
        return 0

    make_tts, resync_tts, lead_prefix = load_resync_helpers()

    vm = json.loads(VM_PATH.read_text(encoding="utf-8"))
    nm = json.loads(NM_PATH.read_text(encoding="utf-8"))
    pm = json.loads(PM_PATH.read_text(encoding="utf-8"))
    v2 = json.loads(V2_PATH.read_text(encoding="utf-8")) if V2_PATH.is_file() else {"entries": []}

    vm_by = {r["id"]: r for r in vm["lines"]}
    nm_by = {r["id"]: r for r in nm["lines"]}
    pm_by = {e["id"]: e for e in pm["entries"]}
    v2_by = {e["id"]: e for e in v2.get("entries", [])}

    vm_updated = nm_updated = pm_game = pm_tts = v2_updated = 0
    tags_preserved = 0
    lost_lead_tag: list[str] = []
    report: list[dict] = []

    for vid in target_ids:
        r = rpy_rows.get(vid)
        if not r:
            print(f"ERROR: no rpy row for {vid}", file=sys.stderr)
            return 1
        char = r["character"]
        new_game = r["game_text"]
        source = r["source"]
        old_pm = pm_by.get(vid, {})
        old_game = old_pm.get("game_text", "")
        old_tts = old_pm.get("tts_text", "")
        old_lead = lead_prefix(old_tts)

        new_tts = resync_tts(char, vid, old_tts, old_game, new_game, make_tts)
        if old_lead and lead_prefix(new_tts) == old_lead:
            tags_preserved += 1
        if old_tts and not (new_tts or "").strip().startswith("["):
            lost_lead_tag.append(vid)

        if vid in vm_by:
            if vm_by[vid].get("text") != new_game:
                vm_by[vid]["text"] = new_game
                vm_updated += 1
            if source:
                vm_by[vid]["source"] = source
        else:
            vm["lines"].append(
                {"id": vid, "character": char, "text": new_game, "source": source}
            )
            vm_by[vid] = vm["lines"][-1]
            vm_updated += 1

        if char == "narrator":
            if vid in nm_by:
                if nm_by[vid].get("text") != new_game:
                    nm_by[vid]["text"] = new_game
                    nm_updated += 1
                if source:
                    nm_by[vid]["source"] = source
            else:
                nm["lines"].append(
                    {
                        "id": vid,
                        "character": "narrator",
                        "text": new_game,
                        "source": source,
                    }
                )
                nm_by[vid] = nm["lines"][-1]
                nm_updated += 1

        if vid in pm_by:
            e = pm_by[vid]
            if e.get("game_text") != new_game:
                e["game_text"] = new_game
                pm_game += 1
            if e.get("tts_text") != new_tts:
                e["tts_text"] = new_tts
                pm_tts += 1
            if source:
                e["source"] = source
            note = e.get("tags_notes", "") or ""
            if SYNC_NOTE not in note:
                e["tags_notes"] = (note + "; " + SYNC_NOTE) if note else SYNC_NOTE
            e["model_hint"] = "eleven_v3"
        else:
            pm["entries"].append(
                {
                    "id": vid,
                    "character": char,
                    "source": source,
                    "game_text": new_game,
                    "tts_text": new_tts,
                    "tags_notes": SYNC_NOTE,
                    "model_hint": "eleven_v3",
                }
            )
            pm_by[vid] = pm["entries"][-1]
            pm_game += 1
            pm_tts += 1

        if vid in v2_by:
            e = v2_by[vid]
            if e.get("game_text") != new_game or e.get("text") != new_tts:
                e["game_text"] = new_game
                e["text"] = new_tts
                v2_updated += 1

        report.append(
            {
                "id": vid,
                "old_game": old_game,
                "new_game": new_game,
                "old_tts_lead": old_lead.strip(),
                "new_tts_lead": lead_prefix(new_tts).strip(),
                "tag_preserved": bool(old_lead and lead_prefix(new_tts) == old_lead),
            }
        )

    VM_PATH.write_text(json.dumps(vm, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    NM_PATH.write_text(json.dumps(nm, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    PM_PATH.write_text(json.dumps(pm, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    if V2_PATH.is_file():
        V2_PATH.write_text(json.dumps(v2, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    subprocess.run(
        [sys.executable, str(SCRIPTS / "sync_voice_performance_manifest.py")],
        cwd=ROOT,
        check=True,
    )

    post = drift_for_ids(target_ids, rpy_rows)

    print("=== sync_canon_witness_case5_clarity ===")
    print(f"ids: {target_ids}")
    print(f"pre drift (vs rpy): vm={pre['vm']} nm={pre['nm']} pm_game={pre['pm_game']}")
    print(f"post drift (vs rpy): vm={post['vm']} nm={post['nm']} pm_game={post['pm_game']}")
    print(f"vm updated: {vm_updated}  nm updated: {nm_updated}")
    print(f"pm game_text updated: {pm_game}  pm tts_text updated: {pm_tts}")
    print(f"v2 updated: {v2_updated}  tags preserved: {tags_preserved}/{len(target_ids)}")
    for row in report:
        print(f"\n{row['id']}:")
        print(f"  lead tags: {row['old_tts_lead']!r} -> {row['new_tts_lead']!r} preserved={row['tag_preserved']}")
        if row["old_game"] != row["new_game"]:
            print(f"  game: ...{row['old_game'][-60:]!r}")
            print(f"     -> ...{row['new_game'][-60:]!r}")
    if lost_lead_tag:
        print(f"\nWARNING: lost leading tag on: {lost_lead_tag}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
