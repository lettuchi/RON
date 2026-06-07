#!/usr/bin/env python3
"""Merge unvoiced continuation say lines into the preceding voiced chunk.

Ren'Py plays `voice` only on the immediately following say statement. The 2026-06-07
text-overflow split left extra bare-string (or same-character) lines after a voiced
first chunk; those clicks are silent. This folds continuations into the voiced line
so one voice clip covers the full utterance (manifest sync + regen follow separately).

Only merges lines directly after a voice-wired first say in the same speaker block:
  voice + narrator "..." + bare "..." continuations
  voice + kaoru/toa "..." + bare "..." continuations

Does not merge separate character statements (kaoru then another kaoru line) or
unvoiced-only narration blocks.
"""
from __future__ import annotations

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

VOICE_RE = re.compile(r'^\s*voice\s+"audio/voice/\w+\.mp3"\s*$')
DIALOGUE_RE = re.compile(r'^(\s*)(kaoru|toa)\s+"(.*)"\s*$')
NARRATION_RE = re.compile(r'^(\s+)"(.*)"\s*$')
STOP_RE = re.compile(
    r"^\s*(voice\s+|menu\s|label\s|\$\s|show\s|scene\s|play\s|stop\s|pause\s|"
    r"jump\s|if\s|elif\s|else\b|return\b|hide\s|with\s|default\s|centered\s)"
)

NARRATION_PROSE_RE = re.compile(
    r"\b(He|She|They|Toa|Kaoru|Kitsu)\b.*\b(he|she|they|her|his|him)\b",
    re.I,
)


def looks_like_narration(text: str) -> bool:
    return bool(NARRATION_PROSE_RE.search(text))


def is_continuation_line(line: str, speaker: str | None) -> bool:
    stripped = line.strip()
    if not stripped or stripped.startswith("#"):
        return False
    if STOP_RE.match(line):
        return False
    dm = DIALOGUE_RE.match(line)
    if dm:
        return dm.group(2) == speaker
    nm = NARRATION_RE.match(line)
    if not nm:
        return False
    if speaker == "narrator":
        return True
    # bare string after a character: only if it is dialogue, not omniscient narration
    return not looks_like_narration(nm.group(2))


def join_chunks(parts: list[str]) -> str:
    text = parts[0]
    for part in parts[1:]:
        if text.endswith(("-", "—")):
            text = text + part.lstrip()
        elif text.endswith((",", ";", ":")):
            text = text + " " + part
        else:
            text = text + " " + part
    return text


def process_file(path: Path) -> tuple[int, list[str]]:
    lines = path.read_text(encoding="utf-8").splitlines()
    out: list[str] = []
    merges = 0
    i = 0
    while i < len(lines):
        line = lines[i]
        if not VOICE_RE.match(line):
            out.append(line)
            i += 1
            continue

        out.append(line)
        i += 1
        if i >= len(lines):
            break

        first = lines[i]
        dm = DIALOGUE_RE.match(first)
        nm = NARRATION_RE.match(first) if not dm else None
        if not dm and not nm:
            out.append(first)
            i += 1
            continue

        if dm:
            indent, char, text = dm.group(1), dm.group(2), dm.group(3)
            speaker = char
            chunks = [text]
            i += 1
            while i < len(lines):
                if not lines[i].strip():
                    i += 1
                    continue
                if not is_continuation_line(lines[i], speaker):
                    break
                cont = NARRATION_RE.match(lines[i])
                dm_cont = DIALOGUE_RE.match(lines[i])
                if cont:
                    chunks.append(cont.group(2))
                    i += 1
                elif dm_cont and dm_cont.group(2) == speaker:
                    chunks.append(dm_cont.group(3))
                    i += 1
                else:
                    break
            merged = join_chunks(chunks)
            if len(chunks) > 1:
                merges += len(chunks) - 1
            out.append(f'{indent}{char} "{merged}"')
            continue

        # narrator first line
        indent, text = nm.group(1), nm.group(2)
        speaker = "narrator"
        chunks = [text]
        i += 1
        while i < len(lines):
            if not lines[i].strip():
                i += 1
                continue
            if not is_continuation_line(lines[i], speaker):
                break
            cont = NARRATION_RE.match(lines[i])
            dm_cont = DIALOGUE_RE.match(lines[i])
            if cont:
                chunks.append(cont.group(2))
                i += 1
            elif dm_cont and dm_cont.group(2) == speaker:
                chunks.append(dm_cont.group(3))
                i += 1
            else:
                break
        merged = join_chunks(chunks)
        if len(chunks) > 1:
            merges += len(chunks) - 1
        out.append(f'{indent}"{merged}"')

    return merges, out


def main() -> int:
    total = 0
    for fn in AU_FILES:
        path = GAME / fn
        merges, out = process_file(path)
        if merges:
            path.write_text("\n".join(out) + "\n", encoding="utf-8")
            print(f"{fn}: merged {merges} continuation line(s)")
            total += merges
        else:
            print(f"{fn}: no continuation merges needed")
    print(f"total continuation lines merged: {total}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
