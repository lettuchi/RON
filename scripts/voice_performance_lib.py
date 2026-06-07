"""Shared helpers for voice performance manifest (TTS tags vs game text)."""
from __future__ import annotations

import json
import re
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = ROOT / "scripts"
GAME_DIR = ROOT / "game"
CHAR_MANIFEST = SCRIPTS_DIR / "voice_manifest.json"
NARRATOR_MANIFEST = SCRIPTS_DIR / "narrator_manifest.json"
PERFORMANCE_MANIFEST = SCRIPTS_DIR / "voice_performance_manifest.json"

VOICE_RE = re.compile(r'^\s*voice\s+"audio/voice/(?P<id>[^"]+?)\.mp3"\s*$')
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
    "case4_investigation.rpy",
    "case5_investigation.rpy",
    "epilogue_romance_bonus.rpy",
    "case_endings.rpy",
]
NARRATOR_RPY_FILES = [
    "prologue.rpy",
    "prologue_canon_encounter.rpy",
    "case1_companion.rpy",
    "case1_investigation.rpy",
    "case2_investigation.rpy",
    "case2_festival.rpy",
    "epilogue_rain_gameover.rpy",
    "case3_5_date_interlude.rpy",
    "case4_5_boat.rpy",
    "case4_investigation.rpy",
    "case5_investigation.rpy",
    "epilogue_romance_bonus.rpy",
    "case_endings.rpy",
]
NARRATOR_RE = re.compile(r'^"((?:\\.|[^"\\])*)"\s*$')


def parse_say(line: str) -> tuple[str | None, str | None]:
    s = line.strip()
    m = re.match(r"^(?P<tag>\w+)\b", s)
    tag = m.group("tag") if m else None
    first = s.find('"')
    last = s.rfind('"')
    if first == -1 or last == first:
        return tag, None
    text = s[first + 1 : last]
    text = text.replace('\\"', '"').replace("\\\\", "\\")
    text = re.sub(r"\\n", " ", text)
    text = re.sub(r"\{[^}]*\}", "", text)
    text = re.sub(r"\s+", " ", text).strip()
    return tag, text


def clean_narrator_raw(raw: str) -> str:
    text = raw.replace('\\"', '"').replace("\\'", "'")
    text = text.replace("\\n", " ").replace("\\\\", "\\")
    text = re.sub(r"\{[^}]*\}", "", text)
    return re.sub(r"\s+", " ", text).strip()


def discover_from_rpy() -> dict[str, dict]:
    """Scan game scripts; return id -> {character, game_text, source}."""
    by_id: dict[str, dict] = {}

    for fname in SCRIPT_FILES:
        fpath = GAME_DIR / fname
        if not fpath.is_file():
            continue
        src = fpath.read_text(encoding="utf-8").splitlines()
        for i, line in enumerate(src):
            m = VOICE_RE.match(line)
            if not m:
                continue
            vid = m.group("id")
            say_line = src[i + 1] if i + 1 < len(src) else ""
            tag, text = parse_say(say_line)
            if text is None:
                continue
            char = vid.split("_", 1)[0]
            if tag and tag != char:
                char = tag
            if vid not in by_id:
                by_id[vid] = {
                    "id": vid,
                    "character": char,
                    "game_text": text,
                    "source": f"{fname}:{i + 1}",
                }

    for fname in NARRATOR_RPY_FILES:
        fpath = GAME_DIR / fname
        if not fpath.is_file():
            continue
        src = fpath.read_text(encoding="utf-8").splitlines()
        for i, line in enumerate(src):
            m = NARRATOR_RE.match(line.strip())
            if not m:
                continue
            text = clean_narrator_raw(m.group(1))
            if not text:
                continue
            # Narrator lines without voice id are not keyed here; manifests hold ids.
            _ = text  # noqa: F841 â€” discovery for narrator uses manifests

    return by_id


def load_merged_voice_lines() -> list[dict]:
    """Canonical line list for performance manifest (deduped by id).

    - toa / kaoru from voice_manifest.json
    - narrator from narrator_manifest.json (authoritative source hints)
    """
    by_id: dict[str, dict] = {}

    if CHAR_MANIFEST.is_file():
        char = json.loads(CHAR_MANIFEST.read_text(encoding="utf-8"))
        for e in char.get("lines", []):
            if e["character"] not in ("toa", "kaoru"):
                continue
            by_id[e["id"]] = {
                "id": e["id"],
                "character": e["character"],
                "game_text": e["text"],
                "source": e.get("source", ""),
            }

    if NARRATOR_MANIFEST.is_file():
        narr = json.loads(NARRATOR_MANIFEST.read_text(encoding="utf-8"))
        for e in narr.get("lines", []):
            by_id[e["id"]] = {
                "id": e["id"],
                "character": "narrator",
                "game_text": e["text"],
                "source": e.get("source", ""),
            }

    # Narrator ids only in character manifest (wired voice, no narrator_manifest row).
    if CHAR_MANIFEST.is_file():
        char = json.loads(CHAR_MANIFEST.read_text(encoding="utf-8"))
        for e in char.get("lines", []):
            if e["character"] != "narrator" or e["id"] in by_id:
                continue
            by_id[e["id"]] = {
                "id": e["id"],
                "character": "narrator",
                "game_text": e["text"],
                "source": e.get("source", ""),
            }

    discovered = discover_from_rpy()
    for vid, row in discovered.items():
        if vid in by_id:
            if not by_id[vid].get("source"):
                by_id[vid]["source"] = row["source"]
        elif row["character"] in ("toa", "kaoru"):
            by_id[vid] = row

    return sorted(by_id.values(), key=lambda e: e["id"])


def load_performance_by_id(path: Path | None = None) -> dict[str, dict]:
    path = path or PERFORMANCE_MANIFEST
    if not path.is_file():
        return {}
    data = json.loads(path.read_text(encoding="utf-8"))
    return {e["id"]: e for e in data.get("entries", [])}


def default_meta() -> dict:
    return {
        "version": 1,
        "description": (
            "Parallel TTS performance text for ElevenLabs v3 audio tags. "
            "game_text mirrors Ren'Py display lines; tts_text is never written into game/*.rpy."
        ),
        "last_synced": date.today().isoformat(),
        "instructions": (
            "Edit tts_text only in this file. Run sync_voice_performance_manifest.py after "
            "adding voice lines to the game. Regenerate with regenerate_voice_with_metadata.py "
            "and ELEVENLABS_MODEL_ID=eleven_v3 (or --model eleven_v3)."
        ),
        "tag_reference": "docs/elevenlabs-audio-tags.md",
        "default_model_hint": "eleven_v3",
        "legacy_batch_model": "eleven_multilingual_v2",
    }
