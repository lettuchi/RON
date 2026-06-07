#!/usr/bin/env python3
"""Build case1-updates.json from baseline vs current .rpy + TTS tag heuristics."""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASELINE = ROOT / "docs" / "script-rewrite-2026-06-04" / "_case1-baseline.json"
OUT = ROOT / "docs" / "script-rewrite-2026-06-04" / "case1-updates.json"

# Manual mood overrides (id -> leading ElevenLabs tags)
MOOD: dict[str, list[str]] = {
    "toa_102": ["cheerfully", "nervously"],
    "toa_106": ["firmly", "nervously"],
    "toa_116": ["sad", "softly"],
    "toa_127": ["surprised", "firmly"],
    "kaoru_138": ["coldly", "sternly"],
    "kaoru_155": ["warmly", "amused"],
    "kaoru_149": ["warmly", "matter-of-fact"],
    "toa_090": ["happy", "breathless"],
    "kaoru_105": ["warmly", "amused"],
    "narrator_099": ["softly", "tender"],
}


def extract_current() -> dict[str, dict]:
    import importlib.util

    spec = importlib.util.spec_from_file_location(
        "extract", ROOT / "scripts" / "_extract_case1_voices.py"
    )
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    rows: dict[str, dict] = {}
    for path in mod.FILES:
        for line_no, vid, char, text in mod.extract(path):
            rows[vid] = {"character": char, "game_text": text, "line": line_no}
    return rows


def guess_mood(character: str, text: str) -> list[str]:
    t = text.lower()
    if character == "narrator":
        if any(w in t for w in ("blood", "strangled", "corpse", "dead", "murder", "killed")):
            return ["dramatic", "coldly"]
        if any(w in t for w in ("kiss", "warm", "tender", "flushed")):
            return ["softly", "tender"]
        return ["dramatic"]
    if character == "kaoru":
        if "?" in text and any(w in t for w in ("to-chan", "toa", "companion")):
            return ["teasing", "amused"]
        if any(w in t for w in ("cruel", "punish", "drown", "knife", "threat")):
            return ["coldly", "sternly"]
        if any(w in t for w in ("good", "wise", "better", "approve")):
            return ["warmly", "matter-of-fact"]
        if "!" in text:
            return ["firmly", "sternly"]
        return ["matter-of-fact", "dismissive"]
    # toa
    if any(w in t for w in ("thank", "want the room", "stay")):
        return ["softly", "tender"]
    if "!" in text or any(w in t for w in ("won't", "don't dare")):
        return ["firmly", "angry"]
    if "?" in text:
        return ["nervously", "firmly"]
    return ["firmly", "matter-of-fact"]


def add_pauses(tts: str) -> str:
    if len(tts) < 100:
        return tts
    parts = re.split(r"(\. )", tts)
    out = []
    sentence_count = 0
    for i, p in enumerate(parts):
        out.append(p)
        if p == ". ":
            sentence_count += 1
            if sentence_count == 1:
                out.append("[short pause] ")
    return "".join(out)


def make_tts(character: str, vid: str, game_text: str) -> str:
    tags = MOOD.get(vid) or guess_mood(character, game_text)
    body = add_pauses(game_text)
    prefix = " ".join(f"[{t}]" for t in tags)
    if "[short pause]" not in body and len(game_text) > 70:
        # mid-line pause before contrast clauses
        body = re.sub(
            r"(\. )(But |And |So |Then |Which |You |I )",
            r". [short pause] \2",
            body,
            count=1,
        )
    return f"{prefix} {body}".strip()


def main() -> None:
    baseline = {r["id"]: r["game_text"] for r in json.loads(BASELINE.read_text(encoding="utf-8"))}
    current = extract_current()
    out_rows = []
    for vid in sorted(current.keys(), key=lambda x: (current[x]["character"], x)):
        cur = current[vid]
        new_text = cur["game_text"]
        old_text = baseline.get(vid, "")
        if new_text == old_text:
            continue
        out_rows.append(
            {
                "id": vid,
                "character": cur["character"],
                "game_text": new_text,
                "tts_text": make_tts(cur["character"], vid, new_text),
            }
        )
    OUT.write_text(json.dumps(out_rows, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"wrote {len(out_rows)} changed lines to {OUT}")


if __name__ == "__main__":
    main()
