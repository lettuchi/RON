#!/usr/bin/env python3
"""Wire voice tags for Case 3 and Case 4 investigation bodies."""
from __future__ import annotations

import json
import re
import shutil
from collections import Counter
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GAME = ROOT / "game"
SCRIPTS = ROOT / "scripts"
NARRATOR_MANIFEST = SCRIPTS / "narrator_manifest.json"

NEXT = {"toa": 246, "kaoru": 283, "narrator": 247}
text_to_id: dict[tuple[str, str], str] = {}

VOICE_RE = re.compile(r'^\s*voice\s+"audio/voice/')
SAY_RE = re.compile(r'^(\s*)(toa|kaoru)\s+"(.*)"\s*$')
NARR_RE = re.compile(r'^(\s*)"((?:\\.|[^"\\])*)"\s*$')
SKIP_PREFIX = (
    "menu", "centered", "scene", "show", "hide", "play", "stop", "$", "jump",
    "call", "return", "label", "image", "define", "default", "pause", "window",
    "if ", "elif ", "else:", "#", "python:",
)


def alloc(speaker: str, text: str) -> str:
    key = (speaker, re.sub(r"\s+", " ", text.strip()))
    if key in text_to_id:
        return text_to_id[key]
    n = NEXT[speaker]
    NEXT[speaker] = n + 1
    vid = f"{speaker}_{n:03d}"
    text_to_id[key] = vid
    return vid


def insert_voice_before(lines: list[str], idx: int, vid: str) -> None:
    indent = re.match(r"^(\s*)", lines[idx]).group(1)
    voice_line = f'{indent}voice "audio/voice/{vid}.mp3"'
    if idx > 0 and VOICE_RE.match(lines[idx - 1]):
        return
    lines.insert(idx, voice_line)


def process_block(lines: list[str], start: int, end: int) -> None:
    targets: list[tuple[int, str, str]] = []
    for i in range(start, end):
        line = lines[i]
        stripped = line.strip()
        if stripped.startswith(SKIP_PREFIX):
            continue
        m = SAY_RE.match(line)
        if m:
            if i > 0 and VOICE_RE.match(lines[i - 1]):
                continue
            targets.append((i, m.group(2), m.group(3)))
            continue
        m2 = NARR_RE.match(line)
        if m2 and not stripped.startswith('"{'):
            raw = m2.group(2)
            if i > 0 and VOICE_RE.match(lines[i - 1]):
                continue
            if raw.startswith("\\"):
                continue
            targets.append((i, "narrator", raw))
    id_by_index: dict[int, str] = {}
    for i, sp, text in targets:
        id_by_index[i] = alloc(sp, text.replace('\\"', '"'))
    for i, _sp, _text in reversed(targets):
        insert_voice_before(lines, i, id_by_index[i])


def process_whole_file(rel: str) -> None:
    path = GAME / rel
    text = path.read_text(encoding="utf-8")
    raw_lines = text.splitlines()
    process_block(raw_lines, 0, len(raw_lines))
    path.write_text("\n".join(raw_lines) + ("\n" if text.endswith("\n") else ""), encoding="utf-8")


def process_label_block(rel: str, label: str) -> None:
    path = GAME / rel
    text = path.read_text(encoding="utf-8")
    raw_lines = text.splitlines()
    joined = "\n".join(raw_lines)
    label_positions = {}
    for m in re.finditer(r"^label (\w+):", joined, re.M):
        label_positions[m.group(1)] = joined[: m.start()].count("\n")
    label_order = sorted(label_positions.items(), key=lambda x: x[1])
    for idx, (lab, start_line) in enumerate(label_order):
        if lab != label:
            continue
        end_line = label_order[idx + 1][1] if idx + 1 < len(label_order) else len(raw_lines)
        process_block(raw_lines, start_line + 1, end_line)
        break
    path.write_text("\n".join(raw_lines) + ("\n" if text.endswith("\n") else ""), encoding="utf-8")


def backup_rpy() -> None:
    backup_dir = GAME / "versions" / "case34-investigation-voice-2026-06-03"
    backup_dir.mkdir(parents=True, exist_ok=True)
    for rel in ("case3_investigation.rpy", "case4_investigation.rpy"):
        src = GAME / rel
        shutil.copy2(src, backup_dir / f"{rel}.bak")


def append_narrator_manifest() -> None:
    if not NARRATOR_MANIFEST.is_file():
        return
    data = json.loads(NARRATOR_MANIFEST.read_text(encoding="utf-8"))
    existing = {e["id"] for e in data.get("lines", [])}
    added = 0
    for (speaker, text), vid in sorted(text_to_id.items(), key=lambda x: x[1]):
        if speaker != "narrator" or vid in existing:
            continue
        data["lines"].append({
            "id": vid,
            "character": "narrator",
            "text": text,
            "source": "case34 investigation voice wire 2026-06-03",
        })
        added += 1
    if added:
        data.setdefault("stats", {})["unique"] = len(data["lines"])
        data["last_appended"] = date.today().isoformat()
        NARRATOR_MANIFEST.write_text(
            json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )
    print(f"narrator_manifest appended: {added}")


EXCLUDE_LABELS = frozenset({
    "case3_bad_end_injury",
    "case4_bad_end_toa_slain",
})


def process_file_skip_labels(rel: str) -> None:
    path = GAME / rel
    text = path.read_text(encoding="utf-8")
    raw_lines = text.splitlines()
    joined = "\n".join(raw_lines)
    label_positions = {}
    for m in re.finditer(r"^label (\w+):", joined, re.M):
        label_positions[m.group(1)] = joined[: m.start()].count("\n")
    label_order = sorted(label_positions.items(), key=lambda x: x[1])
    skip = set()
    for lab, start_line in label_order:
        if lab in EXCLUDE_LABELS:
            idx = label_order.index((lab, start_line))
            end_line = label_order[idx + 1][1] if idx + 1 < len(label_order) else len(raw_lines)
            skip.update(range(start_line + 1, end_line))
    i = 0
    while i < len(raw_lines):
        if i in skip:
            i += 1
            continue
        seg_start = i
        while i < len(raw_lines) and i not in skip:
            i += 1
        process_block(raw_lines, seg_start, i)
    path.write_text("\n".join(raw_lines) + ("\n" if text.endswith("\n") else ""), encoding="utf-8")


def main() -> None:
    backup_rpy()
    process_file_skip_labels("case3_investigation.rpy")
    process_file_skip_labels("case4_investigation.rpy")
    append_narrator_manifest()

    by_file = Counter()
    for (speaker, _text), vid in text_to_id.items():
        if vid.startswith("toa_"):
            by_file["toa"] += 1
        elif vid.startswith("kaoru_"):
            by_file["kaoru"] += 1
        else:
            by_file["narrator"] += 1

    ids = sorted(text_to_id.values())
    out = SCRIPTS / "case34_investigation_voice_ids.txt"
    out.write_text("\n".join(ids) + "\n", encoding="utf-8")

    print(f"New allocations: {len(text_to_id)}")
    print(f"  toa: {by_file['toa']}  kaoru: {by_file['kaoru']}  narrator: {by_file['narrator']}")
    print(f"  toa range: toa_246–toa_{NEXT['toa'] - 1:03d}")
    print(f"  kaoru range: kaoru_283–kaoru_{NEXT['kaoru'] - 1:03d}")
    print(f"  narrator range: narrator_247–narrator_{NEXT['narrator'] - 1:03d}")
    print(f"Wrote {out}")


if __name__ == "__main__":
    main()
