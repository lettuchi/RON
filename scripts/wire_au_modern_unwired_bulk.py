#!/usr/bin/env python3
"""Wire all unwired AU Modern say/narration lines and allocate fresh voice IDs."""
from __future__ import annotations

import importlib.util
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GAME = ROOT / "game"
AU_FILES = [
    "au_modern_wrong_floor.rpy",
    "au_modern_case1_compliance.rpy",
    "au_modern_case2_island_weekend.rpy",
    "au_modern_case3_permits_hr.rpy",
    "au_modern_epilogue.rpy",
]

VOICE_RE = re.compile(r'^\s*voice\s+"audio/voice/(\w+)\.mp3"\s*$')
SAY_RE = re.compile(r'^\s*(kaoru|toa|narrator)\s+"(.*)"\s*$')
NARR_RE = re.compile(r'^\s+"(.*)"\s*$')


def load_make_tts():
    spec = importlib.util.spec_from_file_location(
        "gen_case1", ROOT / "scripts" / "generate_case1_sidecar.py"
    )
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.make_tts


def max_id(prefix: str, ids: set[str]) -> int:
    nums = [int(x.split("_")[1]) for x in ids if x.startswith(prefix + "_")]
    return max(nums) if nums else 0


def scan_file(rel: str) -> list[dict]:
    lines = (GAME / rel).read_text(encoding="utf-8").splitlines()
    gaps: list[dict] = []
    for i, line in enumerate(lines):
        dm = SAY_RE.match(line)
        nm = None if dm else NARR_RE.match(line)
        if not dm and not nm:
            continue
        who = dm.group(1) if dm else "narrator"
        text = dm.group(2) if dm else nm.group(1)
        prev_voice = False
        j = i - 1
        while j >= 0:
            s = lines[j].strip()
            if not s or s.startswith("#"):
                j -= 1
                continue
            if VOICE_RE.match(lines[j]):
                prev_voice = True
            break
        if not prev_voice:
            gaps.append(
                {
                    "file": f"game/{rel}",
                    "line": i + 1,
                    "character": who,
                    "game_text": text,
                }
            )
    return gaps


def allocate_ids(targets: list[dict], vm_ids: set[str]) -> None:
    ctr = {
        "toa": max_id("toa", vm_ids),
        "kaoru": max_id("kaoru", vm_ids),
        "narrator": max_id("narrator", vm_ids),
    }
    for t in targets:
        c = t["character"]
        ctr[c] += 1
        t["id"] = f"{c}_{ctr[c]}"


def patch_rpy(targets: list[dict]) -> None:
    by_file: dict[str, list[dict]] = {}
    for t in targets:
        by_file.setdefault(t["file"], []).append(t)
    for rel, rows in by_file.items():
        path = ROOT / rel
        lines = path.read_text(encoding="utf-8").splitlines()
        for t in sorted(rows, key=lambda x: x["line"], reverse=True):
            idx = t["line"] - 1
            indent = lines[idx][: len(lines[idx]) - len(lines[idx].lstrip())]
            lines.insert(idx, f'{indent}voice "audio/voice/{t["id"]}.mp3"')
        path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def append_manifests(targets: list[dict], make_tts) -> None:
    vm_path = ROOT / "scripts" / "voice_manifest.json"
    nm_path = ROOT / "scripts" / "narrator_manifest.json"
    pm_path = ROOT / "scripts" / "voice_performance_manifest.json"

    vm = json.loads(vm_path.read_text(encoding="utf-8"))
    nm = json.loads(nm_path.read_text(encoding="utf-8"))
    pm = json.loads(pm_path.read_text(encoding="utf-8"))

    existing = {r["id"] for r in vm["lines"]}
    narr_existing = {r["id"] for r in nm["lines"]}
    perf_ids = {e["id"] for e in pm["entries"]}

    for t in targets:
        vid = t["id"]
        char = t["character"]
        game_text = t["game_text"]
        if "\u2014" in game_text or "—" in game_text:
            game_text = game_text.replace("\u2014", ", ").replace("—", ", ")
            t["game_text"] = game_text
        tts = make_tts(char, vid, game_text)
        if vid not in existing:
            vm["lines"].append({"id": vid, "character": char, "text": game_text})
            existing.add(vid)
        if char == "narrator" and vid not in narr_existing:
            nm["lines"].append({"id": vid, "text": game_text})
            narr_existing.add(vid)
        if vid not in perf_ids:
            pm["entries"].append(
                {
                    "id": vid,
                    "character": char,
                    "source": f"{t['file']}:{t['line']}",
                    "game_text": game_text,
                    "tts_text": tts,
                    "tags_notes": "au modern unwired bulk wire 2026-06-07",
                    "model_hint": "eleven_v3",
                }
            )
            perf_ids.add(vid)

    vm_path.write_text(json.dumps(vm, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    nm_path.write_text(json.dumps(nm, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    pm_path.write_text(json.dumps(pm, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def main() -> int:
    make_tts = load_make_tts()
    vm = json.loads((ROOT / "scripts/voice_manifest.json").read_text(encoding="utf-8"))
    vm_ids = {r["id"] for r in vm["lines"]}

    targets: list[dict] = []
    for fn in AU_FILES:
        targets.extend(scan_file(fn))

    if not targets:
        print("no unwired lines")
        return 0

    allocate_ids(targets, vm_ids)
    patch_rpy(targets)
    append_manifests(targets, make_tts)

    ids_path = ROOT / "scripts" / "au_modern_unwired_new_ids.txt"
    ids_path.write_text("\n".join(t["id"] for t in targets) + "\n", encoding="utf-8")

    by_char: dict[str, list[str]] = {}
    for t in targets:
        by_char.setdefault(t["character"], []).append(t["id"])

    print(f"wired {len(targets)} lines")
    for c in ("toa", "kaoru", "narrator"):
        ids = by_char.get(c, [])
        if ids:
            print(f"  {c}: {ids[0]}..{ids[-1]} ({len(ids)})")
    print(f"IDs list: {ids_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
