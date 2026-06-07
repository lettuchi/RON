"""Wire Case 1 menu-branch and merge-path dialogue missing voice statements."""
from __future__ import annotations

import importlib.util
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VOICE_RE = re.compile(r'^\s*voice\s+"audio/voice/(\w+)\.mp3"')
DIALOGUE_RE = re.compile(r'^\s*(kaoru|toa|narrator)\s+"(.*)"\s*$')
CHOICE_RE = re.compile(r'^\s+"([^"]+)":\s*$')

# Extra companion lines (pre-menu + post-menu merge) by 1-based line number
COMPANION_EXTRA_LINES = {94, 97, 100, 130, 133, 136, 139, 142}


def load_tts_helpers():
    spec = importlib.util.spec_from_file_location(
        "gen_case1", ROOT / "scripts" / "generate_case1_sidecar.py"
    )
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.make_tts, mod.guess_mood


def scan_menu_gaps(rel: str) -> list[tuple[int, str, str]]:
    lines = (ROOT / rel).read_text(encoding="utf-8").splitlines()
    gaps: list[tuple[int, str, str]] = []
    i = 0
    while i < len(lines):
        if re.match(r"^\s*menu\s+", lines[i]) or lines[i].strip() == "menu:":
            menu_indent = len(lines[i]) - len(lines[i].lstrip())
            i += 1
            while i < len(lines):
                if lines[i].strip() and not lines[i].strip().startswith("#"):
                    ind = len(lines[i]) - len(lines[i].lstrip())
                    if ind <= menu_indent and not CHOICE_RE.match(lines[i]):
                        break
                m = CHOICE_RE.match(lines[i])
                if m:
                    i += 1
                    while i < len(lines):
                        if not lines[i].strip():
                            i += 1
                            continue
                        ind = len(lines[i]) - len(lines[i].lstrip())
                        if CHOICE_RE.match(lines[i]) and ind > menu_indent:
                            break
                        if ind <= menu_indent:
                            break
                        dm = DIALOGUE_RE.match(lines[i])
                        if dm and not lines[i].strip().startswith("#"):
                            has_v = any(VOICE_RE.match(lines[j]) for j in range(max(0, i - 4), i))
                            if not has_v:
                                gaps.append((i + 1, dm.group(1), dm.group(2)))
                        i += 1
                    continue
                i += 1
            continue
        i += 1
    return gaps


def collect_targets() -> list[dict]:
    targets: list[dict] = []
    for rel in ["game/case1_companion.rpy", "game/case1_investigation.rpy"]:
        path = ROOT / rel
        lines = path.read_text(encoding="utf-8").splitlines()
        seen: set[int] = set()
        for ln, who, text in scan_menu_gaps(rel):
            if ln not in seen:
                seen.add(ln)
                targets.append({"file": rel, "line": ln, "character": who, "game_text": text})
        if rel.endswith("case1_companion.rpy"):
            for ln in COMPANION_EXTRA_LINES:
                if ln in seen:
                    continue
                line = lines[ln - 1]
                dm = DIALOGUE_RE.match(line)
                if dm:
                    targets.append(
                        {"file": rel, "line": ln, "character": dm.group(1), "game_text": dm.group(2)}
                    )
    targets.sort(key=lambda t: (t["file"], t["line"]))
    return targets


def next_ids(n_toa: int, n_kaoru: int, n_narr: int) -> dict[str, int]:
    counters = {"toa": 318, "kaoru": 425, "narrator": 365}

    def bump(char: str) -> str:
        counters[char] += 1
        return f"{char}_{counters[char]}"

    return {"toa": bump, "kaoru": bump, "narrator": bump, "counters": counters}


def allocate_ids(targets: list[dict]) -> None:
    ctr = {"toa": 318, "kaoru": 425, "narrator": 365}
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
            src = f"{t['file']}:{t['line']}"
            pm["entries"].append(
                {
                    "id": vid,
                    "character": char,
                    "source": src,
                    "game_text": game_text,
                    "tts_text": tts,
                    "tags_notes": "case1 menu-branch wire 2026-06-04",
                    "model_hint": "eleven_v3",
                }
            )
            perf_ids.add(vid)

    vm_path.write_text(json.dumps(vm, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    nm_path.write_text(json.dumps(nm, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    pm_path.write_text(json.dumps(pm, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def main() -> int:
    make_tts, _ = load_tts_helpers()
    targets = collect_targets()
    allocate_ids(targets)
    patch_rpy(targets)
    append_manifests(targets, make_tts)

    ids_path = ROOT / "scripts" / "case1_unwired_voice_ids.txt"
    ids_path.write_text(
        "\n".join(t["id"] for t in targets) + "\n",
        encoding="utf-8",
    )
    print(f"wired {len(targets)} lines")
    for t in targets:
        print(f"  {t['id']} {t['file']}:{t['line']} {t['character']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
