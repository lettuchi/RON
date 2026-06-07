#!/usr/bin/env python3
"""Audit/apply helper for the narrator-Toa pronunciation fix + AU emotion tags.

Read-only by default (--audit). Use --apply to write manifest edits.

Objective 1: respell "Toa" -> "Toh-ah" in tts_text for every NARRATOR line whose
game_text contains "Toa".
Objective 2: ensure every AU voice line (ids referenced in the 5 AU .rpy files)
carries at least one eleven_v3 emotion/audio tag in tts_text.
"""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GAME = ROOT / "game"
SCRIPTS = ROOT / "scripts"
PM_PATH = SCRIPTS / "voice_performance_manifest.json"
VM_PATH = SCRIPTS / "voice_manifest.json"
NM_PATH = SCRIPTS / "narrator_manifest.json"

AU_FILES = [
    "au_modern_wrong_floor.rpy",
    "au_modern_case1_compliance.rpy",
    "au_modern_case2_island_weekend.rpy",
    "au_modern_case3_permits_hr.rpy",
    "au_modern_epilogue.rpy",
]

VOICE_RE = re.compile(r'voice\s+"audio/voice/([\w]+)\.mp3"')
TAG_RE = re.compile(r"\[[^\]]+\]")
TOA_RE = re.compile(r"\bToa\b")
RESPELL = "Toh-ah"
LEAD_TAGS_RE = re.compile(r"^(?:\s*\[[^\]]+\])+\s*")
WORD_RE = re.compile(r"[a-z0-9']+")
# Below this game_text->tts word containment, the tts_text is a desync (wrong prose).
DESYNC_THRESHOLD = 0.6


def lead_prefix(tts: str) -> str:
    m = LEAD_TAGS_RE.match(tts or "")
    return m.group(0) if m else ""


def word_set(s: str) -> set[str]:
    return set(WORD_RE.findall(TAG_RE.sub(" ", s or "").lower()))


def containment(game_text: str, tts_text: str) -> float:
    gw = word_set(game_text)
    if not gw:
        return 1.0
    tw = word_set(tts_text)
    return len(gw & tw) / len(gw)


def respelled(s: str) -> str:
    return TOA_RE.sub(RESPELL, s)

# Pure pacing tags do NOT count as emotion/delivery direction.
PACING_TAGS = {"pause", "short pause", "long pause"}


def count_tags(s: str) -> int:
    return len(TAG_RE.findall(s or ""))


def emotion_tags(s: str) -> list[str]:
    """Bracket tags that convey emotion/delivery (exclude pure pacing)."""
    out = []
    for raw in TAG_RE.findall(s or ""):
        inner = raw[1:-1].strip().lower()
        if inner in PACING_TAGS:
            continue
        out.append(raw)
    return out


def collect_au_ids() -> list[str]:
    ids: list[str] = []
    seen: set[str] = set()
    for fname in AU_FILES:
        fpath = GAME / fname
        for line in fpath.read_text(encoding="utf-8").splitlines():
            m = VOICE_RE.search(line)
            if m:
                vid = m.group(1)
                if vid not in seen:
                    seen.add(vid)
                    ids.append(vid)
    return ids


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--audit", action="store_true")
    ap.add_argument("--list-missing", action="store_true",
                    help="With --audit, dump AU ids missing tags (char, game_text).")
    ap.add_argument("--dump-narr-toa", action="store_true",
                    help="Dump all narrator 'Toa' lines (game_text + tts_text).")
    ap.add_argument("--sample-au", type=int, default=0,
                    help="Print N AU example tts_text per speaker.")
    ap.add_argument("--plan", action="store_true",
                    help="Show per-line containment + planned tts for narrator Toa fix.")
    ap.add_argument("--apply", action="store_true",
                    help="Write tts_text edits to performance manifest + deploy ids file.")
    args = ap.parse_args()

    pm = load_json(PM_PATH)
    pm_by = {e["id"]: e for e in pm["entries"]}

    vm = load_json(VM_PATH)
    vm_ids = {r["id"] for r in vm["lines"]}
    nm = load_json(NM_PATH)
    nm_ids = {r["id"] for r in nm["lines"]}
    regen_eligible = vm_ids | nm_ids

    au_ids = collect_au_ids()
    au_set = set(au_ids)

    # --- Objective 1: narrator lines containing "Toa" ---
    narr_toa = []
    narr_toa_missing_pm = []
    for e in pm["entries"]:
        if e.get("character") != "narrator":
            continue
        if TOA_RE.search(e.get("game_text", "")):
            narr_toa.append(e["id"])
            if not TOA_RE.search(e.get("tts_text", "")):
                narr_toa_missing_pm.append(e["id"])

    # narrator ids only present in manifests but not in performance manifest
    narr_manifest_toa = []
    for r in nm["lines"]:
        if TOA_RE.search(r.get("text", "")) and r["id"] not in pm_by:
            narr_manifest_toa.append(r["id"])

    # --- Objective 2: AU emotion tag audit ---
    au_no_pm = [vid for vid in au_ids if vid not in pm_by]
    au_with_pm = [vid for vid in au_ids if vid in pm_by]
    au_tagged = [vid for vid in au_with_pm if count_tags(pm_by[vid].get("tts_text", "")) >= 1]
    au_untagged = [vid for vid in au_with_pm if count_tags(pm_by[vid].get("tts_text", "")) == 0]
    # Emotion-aware view: lines whose only tags are pacing -> lack emotion direction
    au_emotion = [vid for vid in au_with_pm if emotion_tags(pm_by[vid].get("tts_text", ""))]
    au_pacing_only = [vid for vid in au_with_pm if not emotion_tags(pm_by[vid].get("tts_text", ""))]

    # AU ids not regen-eligible (regen can't select them)
    au_not_eligible = [vid for vid in au_ids if vid not in regen_eligible]
    narr_toa_not_eligible = [vid for vid in narr_toa if vid not in regen_eligible]

    print("=== SCOPE AUDIT ===")
    print(f"AU files: {len(AU_FILES)}")
    print(f"AU voice ids (unique): {len(au_ids)}")
    by_char = {}
    for vid in au_ids:
        c = vid.rsplit("_", 1)[0]
        by_char[c] = by_char.get(c, 0) + 1
    print(f"  by speaker: {by_char}")
    print(f"AU ids in performance manifest: {len(au_with_pm)}")
    print(f"AU ids NOT in performance manifest: {len(au_no_pm)} -> {au_no_pm}")
    print(f"AU ids already tagged (>=1 bracket tag): {len(au_tagged)}")
    print(f"AU ids untagged (0 bracket tags): {len(au_untagged)}")
    pct = 100.0 * len(au_tagged) / len(au_with_pm) if au_with_pm else 0.0
    print(f"  any-tag fraction: {len(au_tagged)}/{len(au_with_pm)} = {pct:.1f}%")
    pct_e = 100.0 * len(au_emotion) / len(au_with_pm) if au_with_pm else 0.0
    print(f"AU ids with EMOTION/delivery tag (excl pacing): {len(au_emotion)} ({pct_e:.1f}%)")
    print(f"AU ids pacing-only (no emotion tag -> need one): {len(au_pacing_only)} -> {au_pacing_only}")
    print(f"AU ids not regen-eligible: {len(au_not_eligible)} -> {au_not_eligible}")
    print()
    print("=== NARRATOR 'Toa' ===")
    print(f"narrator perf entries with 'Toa' in game_text: {len(narr_toa)}")
    print(f"  ...whose tts_text lacks 'Toa' (word diverged): {len(narr_toa_missing_pm)} -> {narr_toa_missing_pm}")
    print(f"narrator_manifest 'Toa' ids NOT in perf manifest: {len(narr_manifest_toa)} -> {narr_manifest_toa}")
    print(f"narrator 'Toa' ids not regen-eligible: {len(narr_toa_not_eligible)} -> {narr_toa_not_eligible}")
    print()

    # Combined deploy preview
    deploy = sorted(set(narr_toa) | set(au_untagged))
    print(f"=== COMBINED DEPLOY PREVIEW ===")
    print(f"narrator Toa ids: {len(narr_toa)}")
    print(f"AU untagged ids (will get tags): {len(au_untagged)}")
    print(f"union (deduped): {len(deploy)}")
    overlap = sorted(set(narr_toa) & set(au_untagged))
    print(f"overlap (AU narrator saying Toa, untagged): {len(overlap)} -> {overlap}")

    if args.list_missing:
        print("\n=== AU PACING-ONLY LINES (candidates for emotion tag) ===")
        for vid in au_pacing_only:
            e = pm_by[vid]
            print(f"{vid}\t{e.get('character')}\ttts={json.dumps(e.get('tts_text',''), ensure_ascii=False)}")

    if args.dump_narr_toa:
        print("\n=== ALL NARRATOR 'Toa' LINES ===")
        for vid in narr_toa:
            e = pm_by[vid]
            print(f"{vid}")
            print(f"  game: {json.dumps(e.get('game_text',''), ensure_ascii=False)}")
            print(f"  tts:  {json.dumps(e.get('tts_text',''), ensure_ascii=False)}")

    if args.sample_au:
        print("\n=== AU EMOTION-TAG SAMPLES ===")
        for ch in ("kaoru", "toa", "narrator"):
            shown = 0
            for vid in au_ids:
                if pm_by[vid].get("character") != ch:
                    continue
                e = pm_by[vid]
                print(f"{vid} ({ch})")
                print(f"  game: {json.dumps(e.get('game_text',''), ensure_ascii=False)}")
                print(f"  tts:  {json.dumps(e.get('tts_text',''), ensure_ascii=False)}")
                shown += 1
                if shown >= args.sample_au:
                    break

    if narr_toa_missing_pm:
        print("\n=== NARRATOR 'Toa' lines where tts_text lacks the word ===")
        for vid in narr_toa_missing_pm:
            e = pm_by[vid]
            print(f"{vid}")
            print(f"  game: {json.dumps(e.get('game_text',''), ensure_ascii=False)}")
            print(f"  tts:  {json.dumps(e.get('tts_text',''), ensure_ascii=False)}")

    # --- Build the planned edit for every narrator 'Toa' line ---
    plan: list[dict] = []
    for vid in narr_toa:
        e = pm_by[vid]
        game = e.get("game_text", "")
        old_tts = e.get("tts_text", "")
        c = containment(game, old_tts)
        if c < DESYNC_THRESHOLD:
            action = "rebuild"
            prefix = lead_prefix(old_tts) or "[pause] [dramatic] "
            new_tts = (prefix + respelled(game)).strip()
        else:
            action = "respell"
            new_tts = respelled(old_tts)
        plan.append({
            "id": vid, "action": action, "containment": round(c, 2),
            "old": old_tts, "new": new_tts, "changed": new_tts != old_tts,
        })

    if args.plan:
        print("\n=== NARRATOR Toa FIX PLAN ===")
        for p in plan:
            print(f"{p['id']}  action={p['action']}  containment={p['containment']}  changed={p['changed']}")
            print(f"  old: {json.dumps(p['old'], ensure_ascii=False)}")
            print(f"  new: {json.dumps(p['new'], ensure_ascii=False)}")
        n_rebuild = sum(1 for p in plan if p["action"] == "rebuild")
        n_respell = sum(1 for p in plan if p["action"] == "respell")
        n_changed = sum(1 for p in plan if p["changed"])
        print(f"\nplan: {len(plan)} narrator Toa lines | respell={n_respell} rebuild={n_rebuild} changed={n_changed}")

    if args.apply:
        n_changed = 0
        for p in plan:
            if not p["changed"]:
                continue
            e = pm_by[p["id"]]
            e["tts_text"] = p["new"]
            note = e.get("tags_notes", "") or ""
            stamp = "toa pronunciation fix 2026-06-05 (Toa->Toh-ah)"
            if p["action"] == "rebuild":
                stamp += "; tts resynced from game_text"
            e["tags_notes"] = (note + "; " + stamp) if note else stamp
            e["model_hint"] = "eleven_v3"
            n_changed += 1
        PM_PATH.write_text(json.dumps(pm, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

        deploy_ids = sorted(set(narr_toa) | set(au_untagged))
        out = SCRIPTS / "voice_emotion_narrator_deploy_ids.txt"
        out.write_text("\n".join(deploy_ids) + "\n", encoding="utf-8")
        print(f"APPLIED: updated {n_changed} narrator tts_text entries in {PM_PATH.name}")
        print(f"deploy ids ({len(deploy_ids)}) -> {out}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
