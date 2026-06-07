#!/usr/bin/env python3
"""Wire Modern AU Case 1 Compliance voice lines into manifests."""
from __future__ import annotations

import importlib.util
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RPY = ROOT / "game" / "au_modern_case1_compliance.rpy"
VOICE_RE = re.compile(r'voice\s+"audio/voice/(\w+)\.mp3"')
DIALOGUE_RE = re.compile(r'^\s*(kaoru|toa|narrator)\s+"(.*)"\s*$')
NARRATION_RE = re.compile(r'^\s+"(.*)"\s*$')


def load_make_tts():
    spec = importlib.util.spec_from_file_location(
        "gen_case1", ROOT / "scripts" / "generate_case1_sidecar.py"
    )
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.make_tts


def extract_lines() -> list[dict]:
    lines = RPY.read_text(encoding="utf-8").splitlines()
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
                    "file": "game/au_modern_case1_compliance.rpy",
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
                    "file": "game/au_modern_case1_compliance.rpy",
                    "line": i,
                }
            )
            pending_id = None
    return rows


def main() -> None:
    make_tts = load_make_tts()
    targets = extract_lines()
    vm_path = ROOT / "scripts" / "voice_manifest.json"
    nm_path = ROOT / "scripts" / "narrator_manifest.json"
    pm_path = ROOT / "scripts" / "voice_performance_manifest.json"

    vm = json.loads(vm_path.read_text(encoding="utf-8"))
    nm = json.loads(nm_path.read_text(encoding="utf-8"))
    pm = json.loads(pm_path.read_text(encoding="utf-8"))

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
                    "tags_notes": "au modern case1 compliance wire 2026-06-04",
                    "model_hint": "eleven_v3",
                }
            )
            pm_ids.add(vid)

    vm_path.write_text(json.dumps(vm, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    nm_path.write_text(json.dumps(nm, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    pm_path.write_text(json.dumps(pm, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    ids_path = ROOT / "scripts" / "au_modern_case1_voice_ids.txt"
    ids_path.write_text("\n".join(t["id"] for t in targets) + "\n", encoding="utf-8")

    print(f"Wired {len(targets)} lines ({added} new voice_manifest entries)")
    print(f"IDs list: {ids_path}")


if __name__ == "__main__":
    main()
