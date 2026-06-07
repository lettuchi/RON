#!/usr/bin/env python3
"""Wire Modern AU Epilogue ("Effective Immediately") voice lines into manifests.

Mirrors scripts/wire_au_modern_case3_voice.py:
  * extracts every `voice "audio/voice/<id>.mp3"` + following spoken line from
    game/au_modern_epilogue.rpy and appends new manifest rows;
  * ALSO re-syncs the deferred rerecord kaoru_546 (game/au_modern_case2_island_weekend.rpy)
    whose on-screen text changed in the AU coherence pass
    ("I am listed as your deputy" -> "I am listed as the signatory of record");
  * writes the COMBINED regen list scripts/au_modern_epilogue_voice_ids.txt
    (new epilogue IDs + kaoru_546) so audio is regenerated in one pipeline run.
"""
from __future__ import annotations

import importlib.util
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RPY = ROOT / "game" / "au_modern_epilogue.rpy"
CASE2_RPY = ROOT / "game" / "au_modern_case2_island_weekend.rpy"
DEFERRED_RERECORD_ID = "kaoru_546"
VOICE_RE = re.compile(r'voice\s+"audio/voice/(\w+)\.mp3"')
DIALOGUE_RE = re.compile(r'^\s*(kaoru|toa|narrator)\s+"(.*)"\s*$')
NARRATION_RE = re.compile(r'^\s+"(.*)"\s*$')

WIRE_NOTE = "au modern epilogue effective immediately wire 2026-06-05"


def load_make_tts():
    spec = importlib.util.spec_from_file_location(
        "gen_case1", ROOT / "scripts" / "generate_case1_sidecar.py"
    )
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.make_tts


def extract_lines(path: Path, rel_file: str) -> list[dict]:
    lines = path.read_text(encoding="utf-8").splitlines()
    rows: list[dict] = []
    pending_id: str | None = None
    for i, line in enumerate(lines, start=1):
        vm = VOICE_RE.search(line)
        if vm:
            pending_id = vm.group(1)
            continue
        dm = DIALOGUE_RE.match(line)
        if dm and pending_id:
            char, text = dm.group(1), dm.group(2)
            vid = pending_id
            pending_id = None
            prefix = vid.rsplit("_", 1)[0]
            if prefix != char:
                raise SystemExit(f"ID/character mismatch line {i}: {vid} vs {char}")
            rows.append(
                {
                    "id": vid,
                    "character": char,
                    "game_text": text,
                    "file": rel_file,
                    "line": i,
                }
            )
            continue
        nm = NARRATION_RE.match(line)
        if nm and pending_id and pending_id.startswith("narrator_"):
            rows.append(
                {
                    "id": pending_id,
                    "character": "narrator",
                    "game_text": nm.group(1),
                    "file": rel_file,
                    "line": i,
                }
            )
            pending_id = None
    return rows


def find_line_text(rows: list[dict], vid: str) -> dict:
    for r in rows:
        if r["id"] == vid:
            return r
    raise SystemExit(f"{vid} not found in {CASE2_RPY}")


def main() -> None:
    make_tts = load_make_tts()
    targets = extract_lines(RPY, "game/au_modern_epilogue.rpy")

    vm_path = ROOT / "scripts" / "voice_manifest.json"
    nm_path = ROOT / "scripts" / "narrator_manifest.json"
    pm_path = ROOT / "scripts" / "voice_performance_manifest.json"
    v2_path = ROOT / "scripts" / "voice_v2_metadata_manifest.json"

    vm = json.loads(vm_path.read_text(encoding="utf-8"))
    nm = json.loads(nm_path.read_text(encoding="utf-8"))
    pm = json.loads(pm_path.read_text(encoding="utf-8"))
    v2 = json.loads(v2_path.read_text(encoding="utf-8"))

    vm_ids = {r["id"] for r in vm["lines"]}
    nm_ids = {r["id"] for r in nm["lines"]}
    pm_ids = {e["id"] for e in pm["entries"]}

    added = 0
    for t in targets:
        vid = t["id"]
        char = t["character"]
        game_text = t["game_text"]
        tts = make_tts(char, vid, game_text)
        if vid not in vm_ids:
            vm["lines"].append({"id": vid, "character": char, "text": game_text})
            vm_ids.add(vid)
            added += 1
        if char == "narrator" and vid not in nm_ids:
            nm["lines"].append({"id": vid, "text": game_text})
            nm_ids.add(vid)
        if vid not in pm_ids:
            pm["entries"].append(
                {
                    "id": vid,
                    "character": char,
                    "source": f"{t['file']}:{t['line']}",
                    "game_text": game_text,
                    "tts_text": tts,
                    "tags_notes": WIRE_NOTE,
                    "model_hint": "eleven_v3",
                }
            )
            pm_ids.add(vid)

    # --- Deferred rerecord: re-sync kaoru_546 text from the current case2 .rpy ---
    case2_rows = extract_lines(CASE2_RPY, "game/au_modern_case2_island_weekend.rpy")
    k546 = find_line_text(case2_rows, DEFERRED_RERECORD_ID)
    new_text = k546["game_text"]
    new_tts = make_tts("kaoru", DEFERRED_RERECORD_ID, new_text)
    synced = []

    for r in vm["lines"]:
        if r["id"] == DEFERRED_RERECORD_ID and r.get("text") != new_text:
            r["text"] = new_text
            synced.append("voice_manifest")
    for e in pm["entries"]:
        if e["id"] == DEFERRED_RERECORD_ID:
            if e.get("game_text") != new_text or e.get("tts_text") != new_tts:
                e["game_text"] = new_text
                e["tts_text"] = new_tts
                e["source"] = (
                    f"game/au_modern_case2_island_weekend.rpy:{k546['line']}"
                )
                synced.append("performance_manifest")
    for e in v2.get("entries", []):
        if e["id"] == DEFERRED_RERECORD_ID:
            if e.get("game_text") != new_text or e.get("text") != new_tts:
                e["game_text"] = new_text
                e["text"] = new_tts
                synced.append("v2_metadata_manifest")

    vm_path.write_text(json.dumps(vm, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    nm_path.write_text(json.dumps(nm, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    pm_path.write_text(json.dumps(pm, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    v2_path.write_text(json.dumps(v2, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    # Combined regen list: new epilogue ids + the deferred kaoru_546 rerecord.
    combined = [t["id"] for t in targets] + [DEFERRED_RERECORD_ID]
    ids_path = ROOT / "scripts" / "au_modern_epilogue_voice_ids.txt"
    ids_path.write_text("\n".join(combined) + "\n", encoding="utf-8")

    print(f"Wired {len(targets)} epilogue lines ({added} new voice_manifest entries)")
    print(f"kaoru_546 re-sync touched: {sorted(set(synced)) or 'nothing (already current)'}")
    print(f"Combined regen IDs ({len(combined)}): {ids_path}")


if __name__ == "__main__":
    main()
