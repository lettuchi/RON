#!/usr/bin/env python3
"""Build scripts/voice_manifest.json by parsing the voiced .rpy script files.

For every line of the form:

    voice "audio/voice/{id}.mp3"
    toa "Some spoken line."

the VERY NEXT line is the say statement whose first token is the character tag
(toa / kaoru) and whose quoted string is the text to synthesize.

IDs are emitted in first-appearance order across the files (the project's
convention). Duplicate IDs (the same line reused in multiple branches) are kept
only once. If a duplicate id carries different text, the first appearance wins
and the conflict is recorded.

Run:  python scripts/build_manifest.py
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GAME = ROOT / "game"
MANIFEST = ROOT / "scripts" / "voice_manifest.json"

# Parsed in first-appearance order; this is also the project's documented order.
SCRIPT_FILES = [
    "script.rpy",
    "prologue.rpy",
    "prologue_canon_encounter.rpy",
    "case1_companion.rpy",
    "case1_investigation.rpy",
    "case2_investigation.rpy",
    "case2_festival.rpy",
    "case3_5_date_interlude.rpy",
    "case4_5_boat.rpy",
    "case_endings.rpy",
    "epilogue_rain_gameover.rpy",
    "case3_investigation.rpy",
    "case4_investigation.rpy",
]

VOICE_RE = re.compile(r'^\s*voice\s+"audio/voice/(?P<id>[^"]+?)\.mp3"\s*$')


def parse_say(line: str):
    """Return (speaker_tag, text) for a Ren'Py say line, or (tag, None)."""
    s = line.strip()
    m = re.match(r"^(?P<tag>\w+)\b", s)
    tag = m.group("tag") if m else None
    first = s.find('"')
    last = s.rfind('"')
    if first == -1 or last == first:
        return tag, None
    text = s[first + 1 : last]
    # Unescape Ren'Py string escapes that matter for plain spoken text.
    text = text.replace('\\"', '"').replace("\\\\", "\\")
    # Collapse any literal newline escapes into spaces for natural TTS.
    text = re.sub(r"\\n", " ", text)
    # Strip Ren'Py text tags like {i}...{/i} and interpolation [var] (defensive;
    # the voiced lines currently contain none).
    text = re.sub(r"\{[^}]*\}", "", text)
    text = re.sub(r"\s+", " ", text).strip()
    return tag, text


def main() -> int:
    lines: list[dict] = []
    by_id: dict[str, dict] = {}
    conflicts: list[dict] = []
    occurrences = 0

    for fname in SCRIPT_FILES:
        fpath = GAME / fname
        src = fpath.read_text(encoding="utf-8").splitlines()
        for i, line in enumerate(src):
            m = VOICE_RE.match(line)
            if not m:
                continue
            occurrences += 1
            vid = m.group("id")
            say_line = src[i + 1] if i + 1 < len(src) else ""
            tag, text = parse_say(say_line)

            char = vid.split("_", 1)[0]
            if tag and tag != char:
                # Trust the say-statement speaker if it disagrees with prefix.
                print(
                    f"WARN {fname}:{i+1} id={vid} prefix={char} but speaker={tag}",
                    file=sys.stderr,
                )
                char = tag
            if text is None:
                print(
                    f"WARN {fname}:{i+1} id={vid} could not parse text from: {say_line!r}",
                    file=sys.stderr,
                )
                continue

            if vid in by_id:
                if by_id[vid]["text"] != text:
                    conflicts.append(
                        {
                            "id": vid,
                            "kept_text": by_id[vid]["text"],
                            "kept_source": by_id[vid]["source"],
                            "ignored_text": text,
                            "ignored_source": f"{fname}:{i+1}",
                        }
                    )
                continue

            entry = {"id": vid, "character": char, "text": text}
            by_id[vid] = {"text": text, "source": f"{fname}:{i+1}"}
            lines.append(entry)

    toa = sum(1 for e in lines if e["character"] == "toa")
    kaoru = sum(1 for e in lines if e["character"] == "kaoru")
    other = len(lines) - toa - kaoru

    manifest = {
        "description": (
            "Voice lines extracted from script.rpy, prologue.rpy, "
            "prologue_canon_encounter.rpy, case1_companion.rpy, case1_investigation.rpy, "
            "case2_investigation.rpy, case2_festival.rpy, case3_5_date_interlude.rpy, "
            "case4_5_boat.rpy. Deduplicated by id in "
            "first-appearance order; branch duplicates share one MP3."
        ),
        "ordering": "first_appearance",
        "model_id": "eleven_multilingual_v2",
        "voices": {
            "toa": "l32B8XDoylOsZKiSdfhE",
            "kaoru": "iB0m5bo5Htdz0t9yE0xq",
        },
        "stats": {
            "occurrences": occurrences,
            "unique": len(lines),
            "toa": toa,
            "kaoru": kaoru,
            "other": other,
            "conflicts": len(conflicts),
        },
        "conflicts": conflicts,
        "lines": lines,
    }

    MANIFEST.write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    print(f"occurrences={occurrences} unique={len(lines)} toa={toa} kaoru={kaoru} other={other}")
    if conflicts:
        print(f"CONFLICTS ({len(conflicts)}):")
        for c in conflicts:
            print(f"  {c['id']}: kept {c['kept_source']!r} vs {c['ignored_source']!r}")
    print(f"wrote {MANIFEST}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
