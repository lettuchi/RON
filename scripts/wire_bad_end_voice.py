#!/usr/bin/env python3
"""One-shot: insert voice lines for bad-end scenes; emit bad_end_voice_ids.txt."""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GAME = ROOT / "game"

NEXT = {"kaoru": 225, "toa": 192, "narrator": 183}
text_to_id: dict[tuple[str, str], str] = {}


def alloc(speaker: str, text: str) -> str:
    key = (speaker, re.sub(r"\s+", " ", text.strip()))
    if key in text_to_id:
        return text_to_id[key]
    n = NEXT[speaker]
    NEXT[speaker] = n + 1
    vid = f"{speaker}_{n:03d}"
    text_to_id[key] = vid
    return vid


VOICE_RE = re.compile(r'^\s*voice\s+"audio/voice/')
SAY_RE = re.compile(r'^(\s*)(kaoru|toa)\s+"(.*)"\s*$')
NARR_RE = re.compile(r'^(\s*)"((?:\\.|[^"\\])*)"\s*$')
SKIP_PREFIX = ("menu", "centered", "scene", "show", "hide", "play", "stop", "$", "jump", "call", "return", "label", "image", "define", "default", "pause", "window", "if ", "elif ", "else:", "#", "python:")


def insert_voice_before(lines: list[str], idx: int, vid: str) -> None:
    indent = re.match(r"^(\s*)", lines[idx]).group(1)
    voice_line = f'{indent}voice "audio/voice/{vid}.mp3"'
    if idx > 0 and VOICE_RE.match(lines[idx - 1]):
        return
    lines.insert(idx, voice_line)


def process_label_block(lines: list[str], start: int, end: int) -> None:
    targets: list[tuple[int, str, str]] = []
    for i in range(start, end):
        line = lines[i]
        if line.strip().startswith(SKIP_PREFIX):
            continue
        m = SAY_RE.match(line)
        if m:
            if i > 0 and VOICE_RE.match(lines[i - 1]):
                continue
            targets.append((i, m.group(2), m.group(3)))
            continue
        m2 = NARR_RE.match(line)
        if m2 and not line.strip().startswith('"{'):
            raw = m2.group(2)
            if i > 0 and VOICE_RE.match(lines[i - 1]):
                continue
            if raw.startswith("\\"):
                continue
            targets.append((i, "narrator", raw))
    for i, sp, text in reversed(targets):
        vid = alloc(sp, text.replace('\\"', '"'))
        insert_voice_before(lines, i, vid)


def process_file(rel: str, labels: list[str]) -> None:
    path = GAME / rel
    text = path.read_text(encoding="utf-8")
    raw_lines = text.splitlines()
    joined = "\n".join(raw_lines)
    label_positions = {}
    for m in re.finditer(r"^label (\w+):", joined, re.M):
        label_positions[m.group(1)] = joined[: m.start()].count("\n")
    label_order = sorted(label_positions.items(), key=lambda x: x[1])
    for idx, (lab, start_line) in enumerate(label_order):
        if lab not in labels:
            continue
        end_line = label_order[idx + 1][1] if idx + 1 < len(label_order) else len(raw_lines)
        process_label_block(raw_lines, start_line + 1, end_line)
    path.write_text("\n".join(raw_lines) + ("\n" if text.endswith("\n") else ""), encoding="utf-8")


LABELS_BY_FILE = {
    "case_endings.rpy": [
        "case1_bad_end_kaoru_punishment",
        "gameover_case1_canal",
        "gameover_case2_alley",
        "gameover_case3_injury",
        "gameover_case4_abandon",
        "gameover_case4_slayn",
        "gameover_case4_5_boat",
    ],
    "prologue.rpy": ["prologue_bad_end_kaoru"],
    "epilogue_rain_gameover.rpy": ["gameover_rain", "prologue_bad_end_brothel"],
    "case3_investigation.rpy": ["case3_bad_end_injury_warning", "case3_bad_end_injury"],
    "case4_investigation.rpy": ["case4_bad_end_toa_slain_warning", "case4_bad_end_toa_slain"],
    "case4_5_boat.rpy": ["case4_5_boat_bad_end_warning", "case4_5_bad_end_boat"],
}

for rel, labs in LABELS_BY_FILE.items():
    process_file(rel, labs)

# merge with already-voiced bad-end ids
EXISTING = {
    "kaoru_049", "kaoru_050", "kaoru_051", "kaoru_052",
    "narrator_018", "narrator_019", "narrator_039",
    "narrator_103", "narrator_104", "narrator_105", "narrator_106",
    "toa_038", "toa_039", "toa_040", "toa_041",
}
all_ids = sorted(EXISTING | set(text_to_id.values()))
out = ROOT / "scripts" / "bad_end_voice_ids.txt"
out.write_text("\n".join(all_ids) + "\n", encoding="utf-8")
print(f"New allocations: {len(text_to_id)}")
print(f"Total bad_end_voice_ids: {len(all_ids)}")
print(f"Next counters: {NEXT}")
