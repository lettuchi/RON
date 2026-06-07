#!/usr/bin/env python3
"""Sync Modern AU voice manifests from current .rpy (manifest-only, no MP3 regen).

Updates game_text in voice_manifest.json, narrator_manifest.json, and
voice_performance_manifest.json from the five au_modern_*.rpy files. Resyncs
tts_text to match new wording while preserving:

  * leading eleven_v3 emotion/delivery tag prefixes ([dry], [flustered], …)
  * [short pause] / [pause] pacing tags when the old line had them
  * narrator Toe-uh pronunciation for on-screen "Toa"

Also mirrors tts into voice_v2_metadata_manifest.json when rows exist.

Examples (project root):
    python scripts/sync_au_modern_manifests.py --audit
    python scripts/sync_au_modern_manifests.py
    python scripts/sync_au_modern_manifests.py --write-regen-list
"""
from __future__ import annotations

import argparse
import importlib.util
import json
import re
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GAME = ROOT / "game"
SCRIPTS = ROOT / "scripts"
VM_PATH = SCRIPTS / "voice_manifest.json"
NM_PATH = SCRIPTS / "narrator_manifest.json"
PM_PATH = SCRIPTS / "voice_performance_manifest.json"
V2_PATH = SCRIPTS / "voice_v2_metadata_manifest.json"
OVERFLOW_IDS = SCRIPTS / "au_text_overflow_regen_ids.txt"
INTIMACY_IDS = SCRIPTS / "au_intimacy_prose_regen_ids.txt"
NARR_REWRITE_IDS = SCRIPTS / "au_modern_narrator_rewrite_regen_ids.txt"
REGEN_OUT = SCRIPTS / "au_modern_voice_regen_ids.txt"

AU_FILES = [
    "au_modern_wrong_floor.rpy",
    "au_modern_case1_compliance.rpy",
    "au_modern_case2_island_weekend.rpy",
    "au_modern_case3_permits_hr.rpy",
    "au_modern_epilogue.rpy",
]

VOICE_RE = re.compile(r'voice\s+"audio/voice/(\w+)\.mp3"')
DIALOGUE_RE = re.compile(r"^\s*(kaoru|toa|narrator)\s+\"(.*)\"\s*$")
NARRATION_RE = re.compile(r'^(\s+)"(.*)"\s*$')
TAG_RE = re.compile(r"\[[^\]]+\]")
LEAD_TAGS_RE = re.compile(r"^(?:\s*\[[^\]]+\])+\s*")
WORD_TOA = re.compile(r"\bToa\b")
RESPELL = "Toe-uh"
SYNC_NOTE = "au modern manifest sync 2026-06-07"


def load_make_tts():
    spec = importlib.util.spec_from_file_location(
        "gen_case1", SCRIPTS / "generate_case1_sidecar.py"
    )
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.make_tts


def extract_au_rows() -> dict[str, dict]:
    rows: dict[str, dict] = {}
    for fn in AU_FILES:
        lines = (GAME / fn).read_text(encoding="utf-8").splitlines()
        pending = None
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
                prefix = pending.rsplit("_", 1)[0]
                if prefix != char:
                    raise SystemExit(f"ID/char mismatch {fn}:{i}: {pending} vs {char}")
                rows[pending] = {
                    "character": char,
                    "game_text": text,
                    "source": f"game/{fn}:{i}",
                }
                pending = None
                continue
            nm = NARRATION_RE.match(line)
            if nm and pending.startswith("narrator_"):
                rows[pending] = {
                    "character": "narrator",
                    "game_text": nm.group(2),
                    "source": f"game/{fn}:{i}",
                }
                pending = None
    return rows


def lead_prefix(tts: str) -> str:
    m = LEAD_TAGS_RE.match(tts or "")
    return m.group(0) if m else ""


def had_short_pause(tts: str) -> bool:
    return bool(re.search(r"\[short pause\]", tts or "", re.I))


def apply_first_sentence_pause(text: str) -> str:
    if "[short pause]" in text or ". " not in text:
        return text
    return text.replace(". ", ". [short pause] ", 1)


def normalize_toa_spellings(text: str) -> str:
    text = text.replace("Toh-ah", "Toa").replace("Toh\u2011ah", "Toa")
    return WORD_TOA.sub(RESPELL, text)


def resync_tts(
    char: str,
    vid: str,
    old_tts: str,
    old_game: str,
    new_game: str,
    make_tts,
) -> str:
    if old_game == new_game and old_tts:
        return old_tts

    if not old_tts or old_tts == old_game or not TAG_RE.search(old_tts or ""):
        if char == "narrator":
            prefix = lead_prefix(old_tts) or "[dry] "
            body = apply_first_sentence_pause(new_game)
            return (prefix + normalize_toa_spellings(body)).strip()
        return make_tts(char, vid, new_game)

    prefix = lead_prefix(old_tts)
    body = new_game
    if had_short_pause(old_tts):
        body = apply_first_sentence_pause(body)
    if char == "narrator":
        body = normalize_toa_spellings(body)
    return (prefix + body).strip()


def load_id_list(path: Path) -> list[str]:
    if not path.is_file():
        return []
    return [
        ln.strip()
        for ln in path.read_text(encoding="utf-8").splitlines()
        if ln.strip() and not ln.startswith("#")
    ]


def idnum(vid: str) -> int:
    return int(re.search(r"(\d+)$", vid).group(1))


def write_atomic(path: Path, text: str) -> None:
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(text, encoding="utf-8")
    tmp.replace(path)


def audit(rows: dict[str, dict]) -> dict[str, int]:
    vm = {
        r["id"]: r["text"]
        for r in json.loads(VM_PATH.read_text(encoding="utf-8"))["lines"]
    }
    nm = {
        r["id"]: r["text"]
        for r in json.loads(NM_PATH.read_text(encoding="utf-8"))["lines"]
    }
    pm = {
        e["id"]: e
        for e in json.loads(PM_PATH.read_text(encoding="utf-8"))["entries"]
    }
    out = {
        "au_ids": len(rows),
        "vm_drift": 0,
        "nm_drift": 0,
        "pm_drift": 0,
        "pm_missing": 0,
    }
    for vid, r in rows.items():
        gt = r["game_text"]
        if vid in vm and vm[vid] != gt:
            out["vm_drift"] += 1
        if r["character"] == "narrator" and vid in nm and nm[vid] != gt:
            out["nm_drift"] += 1
        if vid not in pm:
            out["pm_missing"] += 1
        elif pm[vid].get("game_text") != gt:
            out["pm_drift"] += 1
    return out


def main() -> int:
    ap = argparse.ArgumentParser(description="Sync Modern AU manifests from .rpy.")
    ap.add_argument("--audit", action="store_true", help="Print drift counts only.")
    ap.add_argument(
        "--write-regen-list",
        action="store_true",
        help="Write merged au_modern_voice_regen_ids.txt from changed AU ids.",
    )
    args = ap.parse_args()

    rows = extract_au_rows()
    if args.audit:
        stats = audit(rows)
        for k, v in stats.items():
            print(f"{k}: {v}")
        overflow = load_id_list(OVERFLOW_IDS)
        pm = {
            e["id"]: e
            for e in json.loads(PM_PATH.read_text(encoding="utf-8"))["entries"]
        }
        of_ok = sum(
            1
            for vid in overflow
            if vid in rows and vid in pm and pm[vid].get("game_text") == rows[vid]["game_text"]
        )
        print(f"overflow_ids: {len(overflow)}")
        print(f"overflow_synced: {of_ok}")
        return 0

    make_tts = load_make_tts()
    pre = audit(rows)

    vm = json.loads(VM_PATH.read_text(encoding="utf-8"))
    nm = json.loads(NM_PATH.read_text(encoding="utf-8"))
    pm = json.loads(PM_PATH.read_text(encoding="utf-8"))
    v2 = json.loads(V2_PATH.read_text(encoding="utf-8")) if V2_PATH.is_file() else {"entries": []}

    vm_by = {r["id"]: r for r in vm["lines"]}
    nm_by = {r["id"]: r for r in nm["lines"]}
    pm_by = {e["id"]: e for e in pm["entries"]}
    v2_by = {e["id"]: e for e in v2.get("entries", [])}

    vm_updated = nm_updated = pm_game_updated = pm_tts_updated = added = v2_updated = 0
    tags_preserved = 0
    lost_lead_tag: list[str] = []
    changed_ids: list[str] = []

    for vid, r in sorted(rows.items(), key=lambda x: idnum(x[0])):
        char = r["character"]
        new_game = r["game_text"]
        source = r["source"]
        old_pm = pm_by.get(vid)
        old_game = old_pm.get("game_text", "") if old_pm else ""
        old_tts = old_pm.get("tts_text", "") if old_pm else ""

        if vid in vm_by:
            if vm_by[vid].get("text") != new_game:
                vm_by[vid]["text"] = new_game
                vm_updated += 1
            vm_by[vid]["source"] = source
        else:
            vm["lines"].append(
                {"id": vid, "character": char, "text": new_game, "source": source}
            )
            vm_by[vid] = vm["lines"][-1]
            added += 1

        if char == "narrator":
            if vid in nm_by:
                if nm_by[vid].get("text") != new_game:
                    nm_by[vid]["text"] = new_game
                    nm_updated += 1
                nm_by[vid]["source"] = source
            else:
                entry = {"id": vid, "character": "narrator", "text": new_game, "source": source}
                nm["lines"].append(entry)
                nm_by[vid] = entry
                added += 1

        new_tts = resync_tts(char, vid, old_tts, old_game, new_game, make_tts)
        if old_tts and lead_prefix(old_tts) and lead_prefix(new_tts) == lead_prefix(old_tts):
            tags_preserved += 1

        if not (new_tts or "").strip().startswith("["):
            lost_lead_tag.append(vid)

        if vid in pm_by:
            e = pm_by[vid]
            touched = False
            if e.get("game_text") != new_game:
                e["game_text"] = new_game
                pm_game_updated += 1
                touched = True
            if e.get("tts_text") != new_tts:
                e["tts_text"] = new_tts
                pm_tts_updated += 1
                touched = True
            if e.get("source") != source:
                e["source"] = source
            if old_game != new_game or old_tts != new_tts:
                note = e.get("tags_notes", "") or ""
                stamp = SYNC_NOTE
                e["tags_notes"] = (note + "; " + stamp) if note else stamp
                e["model_hint"] = "eleven_v3"
            if touched or old_game != new_game:
                changed_ids.append(vid)
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
            added += 1
            changed_ids.append(vid)

        if vid in v2_by:
            e = v2_by[vid]
            if e.get("game_text") != new_game or e.get("text") != new_tts:
                e["game_text"] = new_game
                e["text"] = new_tts
                v2_updated += 1

    pm.setdefault("counts", {})
    pm["counts"]["total"] = len(pm["entries"])
    pm["counts"]["toa"] = sum(1 for e in pm["entries"] if e["character"] == "toa")
    pm["counts"]["kaoru"] = sum(1 for e in pm["entries"] if e["character"] == "kaoru")
    pm["counts"]["narrator"] = sum(1 for e in pm["entries"] if e["character"] == "narrator")
    pm["counts"]["tagged_tts"] = sum(
        1 for e in pm["entries"] if e.get("tts_text") != e.get("game_text")
    )
    if "_meta" not in pm:
        pm["_meta"] = {}
    pm["_meta"]["last_synced"] = date.today().isoformat()

    write_atomic(VM_PATH, json.dumps(vm, ensure_ascii=False, indent=2) + "\n")
    write_atomic(NM_PATH, json.dumps(nm, ensure_ascii=False, indent=2) + "\n")
    write_atomic(PM_PATH, json.dumps(pm, ensure_ascii=False, indent=2) + "\n")
    if V2_PATH.is_file():
        write_atomic(V2_PATH, json.dumps(v2, ensure_ascii=False, indent=2) + "\n")

    # Re-run performance sync so merged counts/meta stay current (sources now on vm rows).
    import subprocess

    subprocess.run(
        ["python", str(SCRIPTS / "sync_voice_performance_manifest.py")],
        cwd=ROOT,
        check=True,
    )

    post = audit(rows)
    overflow = load_id_list(OVERFLOW_IDS)
    pm_post = {
        e["id"]: e
        for e in json.loads(PM_PATH.read_text(encoding="utf-8"))["entries"]
    }
    of_ok = sum(
        1
        for vid in overflow
        if vid in rows and vid in pm_post and pm_post[vid].get("game_text") == rows[vid]["game_text"]
    )
    intimacy = load_id_list(INTIMACY_IDS)
    narr_rewrite = load_id_list(NARR_REWRITE_IDS)

    if True:
        merged: list[str] = []
        seen: set[str] = set()
        for vid in changed_ids + overflow + intimacy + narr_rewrite:
            if vid not in seen:
                seen.add(vid)
                merged.append(vid)
        merged.sort(key=idnum)
        header = (
            "# Modern AU voice regen ids (merged sync output, 2026-06-07)\n"
            "# Manifest sync only; regenerate MP3s when audio work resumes.\n"
            f"# changed_on_sync={len(changed_ids)} overflow={len(overflow)} "
            f"intimacy={len(intimacy)} narr_rewrite={len(narr_rewrite)}\n"
        )
        REGEN_OUT.write_text(header + "\n".join(merged) + "\n", encoding="utf-8")

    print("=== sync_au_modern_manifests ===")
    print(f"pre:  vm_drift={pre['vm_drift']} nm_drift={pre['nm_drift']} pm_drift={pre['pm_drift']}")
    print(f"post: vm_drift={post['vm_drift']} nm_drift={post['nm_drift']} pm_drift={post['pm_drift']}")
    print(f"vm text updated: {vm_updated}")
    print(f"nm text updated: {nm_updated}")
    print(f"pm game_text updated: {pm_game_updated}")
    print(f"pm tts_text updated: {pm_tts_updated}")
    print(f"new manifest entries: {added}")
    print(f"v2 rows updated: {v2_updated}")
    print(f"tags preserved (lead prefix): {tags_preserved}")
    print(f"overflow synced: {of_ok}/{len(overflow)}")
    print(f"changed ids this run: {len(changed_ids)}")
    print(f"regen list: {REGEN_OUT} ({len(merged)} ids)")
    if lost_lead_tag:
        print(f"WARNING: {len(lost_lead_tag)} lines lack leading tag after sync:")
        for vid in lost_lead_tag[:20]:
            print(f"  {vid}")
        if len(lost_lead_tag) > 20:
            print(f"  ... and {len(lost_lead_tag) - 20} more")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
