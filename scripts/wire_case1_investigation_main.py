"""Wire Case 1 investigation main-path dialogue (registry → barge) missing voice."""
from __future__ import annotations

import importlib.util
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VOICE_RE = re.compile(r'^\s*voice\s+"audio/voice/(\w+)\.mp3"')
DIALOGUE_RE = re.compile(r'^\s*(kaoru|toa|narrator)\s+"(.*)"\s*$')


def load_tts_helpers():
    spec = importlib.util.spec_from_file_location(
        "gen_case1", ROOT / "scripts" / "generate_case1_sidecar.py"
    )
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.make_tts


def is_dialogue(line: str) -> tuple[bool, str | None]:
    m = DIALOGUE_RE.match(line)
    if m and not line.strip().startswith("#"):
        return True, m.group(1)
    return False, None


def scan_unwired(rel: str) -> list[tuple[int, str, str]]:
    lines = (ROOT / rel).read_text(encoding="utf-8").splitlines()
    gaps: list[tuple[int, str, str]] = []
    for i, line in enumerate(lines):
        ok, who = is_dialogue(line)
        if not ok:
            continue
        prev_voice = False
        for j in range(i - 1, max(-1, i - 6), -1):
            pj = lines[j].strip()
            if not pj or pj.startswith("#"):
                continue
            if VOICE_RE.match(lines[j]):
                prev_voice = True
                break
            if is_dialogue(lines[j])[0]:
                break
            if pj.startswith(("menu", "label ", "jump ", "if ", "elif ", "else:")):
                break
        if not prev_voice:
            gaps.append((i + 1, who, DIALOGUE_RE.match(line).group(2)))
    return gaps


def allocate_ids(targets: list[dict]) -> None:
    ctr = {"toa": 337, "kaoru": 448, "narrator": 365}
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
            voice_line = f'{indent}voice "audio/voice/{t["id"]}.mp3"'
            lines.insert(idx, voice_line)
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
                    "tags_notes": "case1 investigation main-path wire 2026-06-04",
                    "model_hint": "eleven_v3",
                }
            )
            perf_ids.add(vid)

    vm_path.write_text(json.dumps(vm, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    nm_path.write_text(json.dumps(nm, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    pm_path.write_text(json.dumps(pm, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def main() -> int:
    make_tts = load_tts_helpers()
    rel = "game/case1_investigation.rpy"
    targets = [
        {"file": rel, "line": ln, "character": who, "game_text": text}
        for ln, who, text in scan_unwired(rel)
    ]
    if not targets:
        print("no unwired lines")
        return 0

    allocate_ids(targets)
    patch_rpy(targets)
    append_manifests(targets, make_tts)

    ids_path = ROOT / "scripts" / "case1_investigation_main_voice_ids.txt"
    ids_path.write_text("\n".join(t["id"] for t in targets) + "\n", encoding="utf-8")
    print(f"wired {len(targets)} lines")
    toa_ids = [t["id"] for t in targets if t["character"] == "toa"]
    kaoru_ids = [t["id"] for t in targets if t["character"] == "kaoru"]
    if toa_ids:
        print(f"  toa range: {toa_ids[0]}-{toa_ids[-1]} ({len(toa_ids)})")
    if kaoru_ids:
        print(f"  kaoru range: {kaoru_ids[0]}-{kaoru_ids[-1]} ({len(kaoru_ids)})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
