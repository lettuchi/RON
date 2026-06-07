#!/usr/bin/env python3
"""Sync manifests for canon review-fix voice changes.

Diffs the edited canon .rpy files against the pre-review backup
(backups/ryoko-owari-2026-06-05-pre-review-fixes/) to find every voiced line
whose on-screen text changed (or is newly added), excluding the Modern AU /
Wrong Floor voice-ID ranges. Writes the changed-id list and updates the three
manifests (voice_manifest.json text, narrator_manifest.json text,
voice_performance_manifest.json game_text + tts_text via make_tts).

Run from project root:  python scripts/sync_canon_review_fixes.py
"""
from __future__ import annotations

import importlib.util
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GAME = ROOT / "game"
BACKUP_GAME = ROOT / "backups" / "ryoko-owari-2026-06-05-pre-review-fixes" / "game"
IDS_OUT = ROOT / "scripts" / "canon_review_fixes_voice_ids.txt"

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


def is_au_id(vid: str) -> bool:
    """Exclude Modern AU + Wrong Floor reserved ranges (do not touch)."""
    try:
        char, num = vid.rsplit("_", 1)
        n = int(num)
    except ValueError:
        return False
    if char == "toa" and 417 <= n <= 434:
        return True
    if char == "kaoru" and 548 <= n <= 565:
        return True
    if char == "narrator" and 420 <= n <= 439:
        return True
    return False


def extract(path: Path) -> dict[str, tuple[str, str]]:
    """Return {id: (character, on_screen_text)} for first appearance of each id."""
    rows: dict[str, tuple[str, str]] = {}
    if not path.is_file():
        return rows
    lines = path.read_text(encoding="utf-8").splitlines()
    pending: str | None = None
    for line in lines:
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
                rows[pending] = (char, text)
            pending = None
            continue
        nm = NARRATION_RE.match(line)
        if nm and pending.startswith("narrator_"):
            if pending not in rows:
                rows[pending] = ("narrator", nm.group(1))
            pending = None
            continue
        # Any other line (show/set_expression/$/scene) keeps pending until the
        # text line arrives; a blank or stray line just drops the pending id.
        if line.strip() and not line.lstrip().startswith(("show ", "$", "play ", "scene ", "hide ", "pause", "set_expression", "menu", "#")):
            pending = None
    return rows


def make_tts_fn():
    spec = importlib.util.spec_from_file_location(
        "gen_case1", ROOT / "scripts" / "generate_case1_sidecar.py"
    )
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.make_tts


def main() -> None:
    make_tts = make_tts_fn()

    current: dict[str, tuple[str, str]] = {}
    backup: dict[str, tuple[str, str]] = {}
    for name in CANON_FILES:
        for vid, row in extract(GAME / name).items():
            current.setdefault(vid, row)
        for vid, row in extract(BACKUP_GAME / name).items():
            backup.setdefault(vid, row)

    changed: dict[str, tuple[str, str]] = {}
    for vid, (char, text) in current.items():
        if is_au_id(vid):
            continue
        old = backup.get(vid)
        if old is None or old[1] != text:
            changed[vid] = (char, text)

    def sort_key(v: str):
        c, n = v.rsplit("_", 1)
        return (c, int(n))

    ids_sorted = sorted(changed.keys(), key=sort_key)
    IDS_OUT.write_text("\n".join(ids_sorted) + "\n", encoding="utf-8")

    # --- Sync manifests ---
    vm_path = ROOT / "scripts" / "voice_manifest.json"
    nm_path = ROOT / "scripts" / "narrator_manifest.json"
    pm_path = ROOT / "scripts" / "voice_performance_manifest.json"
    vm = json.loads(vm_path.read_text(encoding="utf-8"))
    nm = json.loads(nm_path.read_text(encoding="utf-8"))
    pm = json.loads(pm_path.read_text(encoding="utf-8"))

    vm_by = {r["id"]: r for r in vm["lines"]}
    nm_by = {r["id"]: r for r in nm["lines"]}
    pm_by = {e["id"]: e for e in pm["entries"]}

    new_ids, updated_ids = [], []
    for vid in ids_sorted:
        char, text = changed[vid]
        tts = make_tts(char, vid, text)
        # voice_manifest (all characters incl narrator are listed here)
        if vid in vm_by:
            if vm_by[vid].get("text") != text:
                vm_by[vid]["text"] = text
                updated_ids.append(vid)
        else:
            vm["lines"].append({"id": vid, "character": char, "text": text})
            new_ids.append(vid)
        # narrator_manifest (narrator only)
        if char == "narrator":
            if vid in nm_by:
                nm_by[vid]["text"] = text
            else:
                nm["lines"].append({"id": vid, "text": text})
        # performance manifest
        if vid in pm_by:
            pm_by[vid]["game_text"] = text
            pm_by[vid]["tts_text"] = tts
        else:
            pm["entries"].append({
                "id": vid,
                "character": char,
                "source": "game/*.rpy (canon review fixes 2026-06-05)",
                "game_text": text,
                "tts_text": tts,
                "tags_notes": "canon review fixes 2026-06-05",
                "model_hint": "eleven_v3",
            })

    vm_path.write_text(json.dumps(vm, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    nm_path.write_text(json.dumps(nm, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    pm_path.write_text(json.dumps(pm, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    print(f"changed/added canon voiced IDs: {len(ids_sorted)}")
    print(f"  new manifest entries: {len(new_ids)} -> {new_ids}")
    print(f"  updated text entries: {len(updated_ids)}")
    print(f"IDs list: {IDS_OUT}")


if __name__ == "__main__":
    main()
