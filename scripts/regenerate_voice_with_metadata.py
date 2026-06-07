#!/usr/bin/env python3
"""Regenerate Toa / Kaoru / narrator voice MP3s (v2 folder).

Does NOT touch existing game/audio/voice/*.mp3. New files go under:

    game/audio/voice/v2/eve-donovan-YYYY-MM-DD/{id}.mp3

Sidecar manifest (tooling, text lookup, single-line regen):

    scripts/voice_v2_metadata_manifest.json

Voice assignment (ElevenLabs voice IDs → env overrides):
    toa      → custom        Ylb1ch6nQEKvpaUivWj6  ELEVENLABS_VOICE_V2_TOA
    kaoru    → custom        zyxAdkuEJWvr177AyQPs  ELEVENLABS_VOICE_V2_KAORU
    narrator → custom        giAoKpl5weRTCJK7uB9b  ELEVENLABS_VOICE_V2_NARRATOR

The legacy generate_voice.py / generate_narrator_voice.py still write to
game/audio/voice/ and remain the path the game uses until you swap .rpy paths
or copy v2 files over (see docs/voice-metadata.md).

Examples (project root):
    python scripts/regenerate_voice_with_metadata.py --check
    python scripts/regenerate_voice_with_metadata.py --dry-run
    python scripts/regenerate_voice_with_metadata.py --sample 5
    python scripts/regenerate_voice_with_metadata.py
    python scripts/regenerate_voice_with_metadata.py --ids toa_001,kaoru_002
    python scripts/regenerate_voice_with_metadata.py --text "Wrong door. Again."
    python scripts/regenerate_voice_with_metadata.py --read-metadata game/audio/voice/v2/.../toa_001.mp3
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
import threading
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import date
from pathlib import Path
from urllib import error, request

ROOT = Path(__file__).resolve().parents[1]
GAME_DIR = ROOT / "game"
LEGACY_VOICE_DIR = GAME_DIR / "audio" / "voice"
SCRIPTS_DIR = ROOT / "scripts"
ENV_FILE = SCRIPTS_DIR / ".env"
CHAR_MANIFEST = SCRIPTS_DIR / "voice_manifest.json"
NARRATOR_MANIFEST = SCRIPTS_DIR / "narrator_manifest.json"
V2_MANIFEST = SCRIPTS_DIR / "voice_v2_metadata_manifest.json"
PERFORMANCE_MANIFEST = SCRIPTS_DIR / "voice_performance_manifest.json"
MISSING_FILE = SCRIPTS_DIR / "missing_voice_v2_ids.txt"

API_BASE = "https://api.elevenlabs.io"
DEFAULT_MODEL = "eleven_multilingual_v2"

# ElevenLabs voice IDs for this regeneration pass (override via ELEVENLABS_VOICE_V2_*).
VOICE_V2_TOA = "Ylb1ch6nQEKvpaUivWj6"
VOICE_V2_KAORU = "zyxAdkuEJWvr177AyQPs"
VOICE_V2_NARRATOR = "giAoKpl5weRTCJK7uB9b"

V2_SUBDIR = f"v2/eve-donovan-{date.today().isoformat()}"


class GenerationHalted(Exception):
    """Quota, plan restriction, or rate-limit exhaustion."""


def load_env_file(path: Path) -> None:
    if not path.exists():
        return
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, val = line.partition("=")
        os.environ.setdefault(key.strip(), val.strip().strip('"').strip("'"))


def default_voices() -> dict[str, str]:
    """v2 pass voice IDs (not legacy Carla/Jax from scripts/.env).

    Override only with ELEVENLABS_VOICE_V2_* so generate_voice.py can keep using
    ELEVENLABS_VOICE_TOA / ELEVENLABS_VOICE_KAORU for the legacy folder.
    """
    return {
        "toa": os.environ.get("ELEVENLABS_VOICE_V2_TOA", VOICE_V2_TOA).strip(),
        "kaoru": os.environ.get("ELEVENLABS_VOICE_V2_KAORU", VOICE_V2_KAORU).strip(),
        "narrator": os.environ.get("ELEVENLABS_VOICE_V2_NARRATOR", VOICE_V2_NARRATOR).strip(),
    }


def voice_name_for(character: str, voices: dict[str, str] | None = None) -> str:
    """Display label for ID3/manifest; prefer ElevenLabs voice name when cached."""
    if voices is None:
        voices = default_voices()
    names = _voice_display_names(voices)
    return names.get(character, character)


_voice_display_cache: dict[str, str] | None = None


def _voice_display_names(voices: dict[str, str]) -> dict[str, str]:
    global _voice_display_cache
    if _voice_display_cache is not None:
        return _voice_display_cache
    fallback = {"toa": "Toa", "kaoru": "Kaoru", "narrator": "Narrator"}
    api_key = os.environ.get("ELEVENLABS_API_KEY", "").strip()
    if not api_key:
        _voice_display_cache = fallback
        return _voice_display_cache
    resolved: dict[str, str] = {}
    for character, voice_id in voices.items():
        try:
            data = api_get(f"/v1/voices/{voice_id}", api_key)
            resolved[character] = data.get("name") or fallback.get(character, character)
        except Exception:
            resolved[character] = fallback.get(character, character)
    _voice_display_cache = resolved
    return _voice_display_cache


def synthesize(text: str, voice_id: str, model_id: str, api_key: str,
               max_retries: int = 5) -> bytes:
    url = f"{API_BASE}/v1/text-to-speech/{voice_id}"
    body = json.dumps({"text": text, "model_id": model_id}).encode("utf-8")
    headers = {
        "xi-api-key": api_key,
        "Content-Type": "application/json",
        "Accept": "audio/mpeg",
    }
    attempt = 0
    while True:
        attempt += 1
        req = request.Request(url, data=body, headers=headers, method="POST")
        try:
            with request.urlopen(req, timeout=120) as resp:
                return resp.read()
        except error.HTTPError as e:
            payload = e.read().decode("utf-8", "replace")
            low = payload.lower()
            if e.code == 402 or "paid_plan_required" in low or "payment_required" in low:
                raise GenerationHalted(f"HTTP {e.code} plan restriction: {payload}")
            if e.code == 429:
                if "quota" in low or "credit" in low:
                    raise GenerationHalted(f"HTTP 429 quota: {payload}")
                if attempt > max_retries:
                    raise GenerationHalted(f"HTTP 429 after {max_retries} retries: {payload}")
                retry_after = e.headers.get("retry-after")
                time.sleep(float(retry_after) if retry_after else min(2 ** attempt, 30))
                continue
            if e.code in (401, 403) and ("quota" in low or "credit" in low):
                raise GenerationHalted(f"HTTP {e.code} quota: {payload}")
            if 500 <= e.code < 600 and attempt <= max_retries:
                time.sleep(min(2 ** attempt, 30))
                continue
            raise RuntimeError(f"HTTP {e.code} for {voice_id}: {payload}")
        except error.URLError as e:
            if attempt <= max_retries:
                time.sleep(min(2 ** attempt, 15))
                continue
            raise RuntimeError(f"network error for {voice_id}: {e}")


def api_get(path: str, api_key: str) -> dict:
    req = request.Request(f"{API_BASE}{path}", headers={"xi-api-key": api_key})
    with request.urlopen(req, timeout=60) as resp:
        return json.loads(resp.read().decode("utf-8"))


def write_atomic(path: Path, data: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".part")
    tmp.write_bytes(data)
    tmp.replace(path)


def load_performance_texts(path: Path | None = None) -> dict[str, dict]:
    path = path or PERFORMANCE_MANIFEST
    if not path.is_file():
        return {}
    data = json.loads(path.read_text(encoding="utf-8"))
    return {e["id"]: e for e in data.get("entries", []) if not e.get("orphan")}


def resolve_tts_for_entry(
    entry: dict,
    performance: dict[str, dict],
    *,
    use_performance: bool,
) -> tuple[str, bool]:
    """Return (text_for_api, used_performance_manifest)."""
    if not use_performance:
        return entry["text"], False
    perf = performance.get(entry["id"])
    if not perf:
        return entry["text"], False
    tts = (perf.get("tts_text") or "").strip()
    if tts and tts != entry["text"]:
        return tts, True
    if tts:
        return tts, True
    return entry["text"], False


def load_entries() -> list[dict]:
    """Merge character + narrator manifest lines into one regen list."""
    entries: list[dict] = []
    if CHAR_MANIFEST.is_file():
        char = json.loads(CHAR_MANIFEST.read_text(encoding="utf-8"))
        for e in char.get("lines", []):
            entries.append({
                "id": e["id"],
                "character": e["character"],
                "text": e["text"],
                "source_file": e.get("source", ""),
                "manifest": "voice_manifest.json",
            })
    if NARRATOR_MANIFEST.is_file():
        narr = json.loads(NARRATOR_MANIFEST.read_text(encoding="utf-8"))
        for e in narr.get("lines", []):
            entries.append({
                "id": e["id"],
                "character": "narrator",
                "text": e["text"],
                "source_file": e.get("source", ""),
                "manifest": "narrator_manifest.json",
            })
    return entries


def renpy_audio_path(v2_subdir: str, line_id: str) -> str:
    return f"audio/voice/{v2_subdir}/{line_id}.mp3"


def embed_mp3_metadata(path: Path, meta: dict) -> None:
    try:
        from mutagen.id3 import COMM, TIT2, TXXX, ID3
        from mutagen.mp3 import MP3
    except ImportError as exc:
        raise RuntimeError(
            "mutagen is required for ID3 metadata. Install: pip install -r requirements-voice.txt"
        ) from exc

    audio = MP3(path)
    if audio.tags is None:
        audio.add_tags()
    tags = audio.tags
    assert isinstance(tags, ID3)

    tags.delall("TIT2")
    tags.delall("TXXX:renpy_line")
    tags.delall("TXXX:renpy_character")
    tags.delall("TXXX:elevenlabs_voice_id")
    tags.delall("TXXX:renpy_id")
    tags.delall("TXXX:renpy_source")
    tags.delall("COMM")

    tags.add(TIT2(encoding=3, text=meta["id"]))
    tags.add(TXXX(encoding=3, desc="renpy_line", text=meta["text"]))
    tags.add(TXXX(encoding=3, desc="renpy_character", text=meta["character"]))
    tags.add(TXXX(encoding=3, desc="elevenlabs_voice_id", text=meta["voice_id"]))
    tags.add(TXXX(encoding=3, desc="renpy_id", text=meta["id"]))
    if meta.get("source_file"):
        tags.add(TXXX(encoding=3, desc="renpy_source", text=meta["source_file"]))
    tags.add(COMM(encoding=3, lang="eng", desc="renpy_v2", text=json.dumps(meta, ensure_ascii=False)))
    audio.save()


def read_mp3_metadata(path: Path) -> dict:
    try:
        from mutagen.id3 import ID3
        from mutagen.mp3 import MP3
    except ImportError as exc:
        raise RuntimeError("mutagen required: pip install -r requirements-voice.txt") from exc

    audio = MP3(path)
    if not audio.tags:
        return {}
    tags = audio.tags
    out: dict = {"path": str(path)}
    for frame in tags.getall("TXXX:renpy_line"):
        out["text"] = frame.text[0] if frame.text else ""
    for frame in tags.getall("TXXX:renpy_character"):
        out["character"] = frame.text[0] if frame.text else ""
    for frame in tags.getall("TXXX:elevenlabs_voice_id"):
        out["voice_id"] = frame.text[0] if frame.text else ""
    for frame in tags.getall("TXXX:renpy_id"):
        out["id"] = frame.text[0] if frame.text else ""
    for frame in tags.getall("COMM:renpy_v2"):
        try:
            out["embedded_json"] = json.loads(frame.text[0])
        except (json.JSONDecodeError, IndexError):
            pass
    return out


def load_or_init_v2_manifest(v2_dir: Path, v2_subdir: str) -> dict:
    if V2_MANIFEST.is_file():
        data = json.loads(V2_MANIFEST.read_text(encoding="utf-8"))
        if data.get("output_subdir") == v2_subdir:
            return data
    v = default_voices()
    labels = _voice_display_names(v)
    return {
        "description": "v2 voice pass: Toa + Kaoru + narrator. ID3 + JSON for per-line regen.",
        "generated_on": date.today().isoformat(),
        "output_subdir": v2_subdir,
        "output_dir": str(v2_dir.relative_to(ROOT)).replace("\\", "/"),
        "legacy_dir": "game/audio/voice",
        "voices": {
            "toa": {"name": labels["toa"], "voice_id": v["toa"]},
            "kaoru": {"name": labels["kaoru"], "voice_id": v["kaoru"]},
            "narrator": {"name": labels["narrator"], "voice_id": v["narrator"]},
        },
        "entries": [],
    }


def upsert_manifest_entry(manifest: dict, entry: dict) -> None:
    by_id = {e["id"]: i for i, e in enumerate(manifest["entries"])}
    if entry["id"] in by_id:
        manifest["entries"][by_id[entry["id"]]] = entry
    else:
        manifest["entries"].append(entry)
    manifest["entries"].sort(key=lambda e: e["id"])


def write_v2_manifest(manifest: dict) -> None:
    manifest["counts"] = {
        "total": len(manifest["entries"]),
        "toa": sum(1 for e in manifest["entries"] if e["character"] == "toa"),
        "kaoru": sum(1 for e in manifest["entries"] if e["character"] == "kaoru"),
        "narrator": sum(1 for e in manifest["entries"] if e["character"] == "narrator"),
    }
    V2_MANIFEST.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
                           encoding="utf-8")


def parse_ids_arg(ids_arg: str) -> list[str]:
    if ids_arg.startswith("@"):
        raw = Path(ids_arg[1:]).read_text(encoding="utf-8")
        tokens = re.split(r"[,\s]+", raw)
    else:
        tokens = ids_arg.split(",")
    return [t.strip() for t in tokens if t.strip()]


def select_entries(all_entries: list[dict], *, ids_arg: str, text_arg: str,
                   sample: int | None) -> list[dict]:
    if text_arg:
        exact = [e for e in all_entries if e["text"] == text_arg]
        if exact:
            return exact
        sub = [e for e in all_entries if text_arg.lower() in e["text"].lower()]
        if len(sub) == 1:
            return sub
        if not sub:
            print(f"ERROR: no manifest line matches text {text_arg!r}", file=sys.stderr)
            return []
        print(f"ERROR: text matches {len(sub)} lines; use --ids instead:", file=sys.stderr)
        for e in sub[:10]:
            print(f"  {e['id']}: {e['text'][:80]!r}...", file=sys.stderr)
        return []

    if ids_arg:
        by_id = {e["id"]: e for e in all_entries}
        out = []
        for w in parse_ids_arg(ids_arg):
            if w not in by_id:
                print(f"WARN: id {w!r} not in manifests; skipping", file=sys.stderr)
                continue
            out.append(by_id[w])
        return out

    out = list(all_entries)
    if sample is not None and sample > 0:
        # One line per speaker for a quick audition set.
        picks: list[dict] = []
        for ch in ("toa", "kaoru", "narrator"):
            for e in out:
                if e["character"] == ch:
                    picks.append(e)
                    break
        extra = [e for e in out if e not in picks][: max(0, sample - len(picks))]
        out = picks + extra[: sample - len(picks)]
    return out


def cmd_check(voices: dict[str, str], model_id: str, api_key: str) -> int:
    if not api_key:
        print("ERROR: ELEVENLABS_API_KEY is not set.", file=sys.stderr)
        return 2
    print("Checking ElevenLabs (v2 Toa + Kaoru + narrator pass)...")
    try:
        sub = api_get("/v1/user/subscription", api_key)
        used, limit, tier = sub.get("character_count"), sub.get("character_limit"), sub.get("tier")
        remaining = None if limit is None else limit - (used or 0)
        print(f"  subscription: tier={tier} used={used} limit={limit} remaining={remaining}")
    except Exception as e:  # noqa: BLE001
        print(f"  subscription lookup failed: {e}", file=sys.stderr)
    rc = 0
    for tag in ("toa", "kaoru", "narrator"):
        vid = voices[tag]
        try:
            audio = synthesize("Test.", vid, model_id, api_key)
            print(f"  synth {tag} ({voice_name_for(tag, voices)}, {vid}): OK, {len(audio)} bytes")
        except Exception as e:  # noqa: BLE001
            print(f"  synth {tag} ({vid}): FAILED -> {e}", file=sys.stderr)
            rc = 1
    return rc


def main() -> int:
    ap = argparse.ArgumentParser(description="Regenerate v2 voice MP3s with embedded metadata.")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--ids", default="", help="Comma-separated ids or @missing_voice_v2_ids.txt")
    ap.add_argument("--text", default="", help="Regenerate line(s) matching this dialogue text.")
    ap.add_argument("--force", action="store_true", help="Regenerate even if v2 MP3 exists.")
    ap.add_argument("--sample", type=int, default=0,
                    help="Generate only N lines (includes one per speaker when possible).")
    ap.add_argument("--output-subdir", default="",
                    help=f"Override subdir under audio/voice/ (default {V2_SUBDIR}).")
    ap.add_argument("--concurrency", type=int, default=3)
    ap.add_argument("--read-metadata", metavar="MP3",
                    help="Print embedded metadata from a v2 MP3 and exit.")
    ap.add_argument(
        "--performance-manifest",
        default="",
        help=f"JSON with tts_text tags (default {PERFORMANCE_MANIFEST.name}).",
    )
    ap.add_argument(
        "--no-performance",
        action="store_true",
        help="Ignore performance manifest; synthesize manifest game text only.",
    )
    ap.add_argument(
        "--use-performance-text",
        action="store_true",
        help="Alias for default behavior when performance manifest exists.",
    )
    ap.add_argument(
        "--model",
        default="",
        help="Override ELEVENLABS_MODEL_ID (use eleven_v3 for audio tags).",
    )
    args = ap.parse_args()

    load_env_file(ENV_FILE)
    api_key = os.environ.get("ELEVENLABS_API_KEY", "").strip()
    model_id = (
        args.model.strip()
        or os.environ.get("ELEVENLABS_MODEL_ID", DEFAULT_MODEL).strip()
    )
    voices = default_voices()
    if args.performance_manifest:
        perf_path = Path(args.performance_manifest)
        if not perf_path.is_absolute():
            perf_path = ROOT / perf_path
    else:
        perf_path = PERFORMANCE_MANIFEST
    use_performance = not args.no_performance
    performance = load_performance_texts(perf_path) if use_performance else {}

    if args.read_metadata:
        p = Path(args.read_metadata)
        if not p.is_file():
            print(f"ERROR: not found: {p}", file=sys.stderr)
            return 2
        print(json.dumps(read_mp3_metadata(p), ensure_ascii=False, indent=2))
        return 0

    v2_subdir = args.output_subdir.strip() or V2_SUBDIR
    v2_dir = LEGACY_VOICE_DIR / Path(*v2_subdir.split("/"))

    if args.check:
        return cmd_check(voices, model_id, api_key)

    all_entries = load_entries()
    if not all_entries:
        print("ERROR: no manifest entries. Ensure voice_manifest.json and/or "
              "narrator_manifest.json exist.", file=sys.stderr)
        return 2

    selected = select_entries(
        all_entries,
        ids_arg=args.ids,
        text_arg=args.text.strip(),
        sample=args.sample if args.sample > 0 else None,
    )
    if args.text.strip() and not selected:
        return 2

    def needs_gen(e: dict) -> bool:
        p = v2_dir / f"{e['id']}.mp3"
        return args.force or (not p.exists()) or p.stat().st_size == 0

    todo = [e for e in selected if needs_gen(e)]
    skip = [e for e in selected if not needs_gen(e)]

    n_toa = sum(1 for e in all_entries if e["character"] == "toa")
    n_kaoru = sum(1 for e in all_entries if e["character"] == "kaoru")
    n_narr = sum(1 for e in all_entries if e["character"] == "narrator")

    labels = _voice_display_names(voices)
    print("Voice assignment (this script):")
    print(f"  toa ({n_toa} lines)      -> {labels['toa']} ({voices['toa']})")
    print(f"  kaoru ({n_kaoru} lines)   -> {labels['kaoru']} ({voices['kaoru']})")
    print(f"  narrator ({n_narr} lines) -> {labels['narrator']} ({voices['narrator']})")
    print(f"Output: {v2_dir}")
    print(f"Legacy (unchanged): {LEGACY_VOICE_DIR}")
    print(f"manifest lines (total): {len(all_entries)}")
    print(f"model: {model_id}")
    if use_performance:
        n_perf = sum(
            1
            for e in todo
            if resolve_tts_for_entry(e, performance, use_performance=True)[1]
        )
        print(
            f"performance manifest: {perf_path.name} "
            f"({len(performance)} entries, {n_perf} todo lines use tagged tts_text)"
        )
    else:
        print("performance manifest: disabled (--no-performance)")
    print(f"selected: {len(selected)}  skip (already in v2): {len(skip)}  to generate: {len(todo)}")
    tts_lens = [
        len(resolve_tts_for_entry(e, performance, use_performance=use_performance)[0])
        for e in todo
    ]
    print(f"approx characters (TTS input): {sum(tts_lens)}")

    if args.dry_run:
        for e in todo:
            tts_text, used_perf = resolve_tts_for_entry(
                e, performance, use_performance=use_performance
            )
            tag_note = " tagged" if used_perf and tts_text != e["text"] else ""
            print(
                f"  WOULD GEN {e['id']} ({e['character']}, {len(tts_text)} chars{tag_note})"
            )
        return 0

    if not todo:
        print("Nothing to generate in v2 folder.")
        return 0

    if not api_key:
        print("ERROR: ELEVENLABS_API_KEY is not set.", file=sys.stderr)
        return 2

    v2_manifest = load_or_init_v2_manifest(v2_dir, v2_subdir)
    stop = threading.Event()
    lock = threading.Lock()
    done_ids: list[str] = []
    halt_msg = {"text": ""}

    def worker(e: dict) -> None:
        if stop.is_set():
            return
        char = e["character"]
        vid = voices[char]
        mp3_path = v2_dir / f"{e['id']}.mp3"
        tts_text, used_perf = resolve_tts_for_entry(
            e, performance, use_performance=use_performance
        )
        meta = {
            "id": e["id"],
            "character": char,
            "voice_name": voice_name_for(char, voices),
            "voice_id": vid,
            "text": tts_text,
            "game_text": e["text"],
            "used_performance_manifest": used_perf,
            "source_file": e.get("source_file", ""),
            "path": str(mp3_path.relative_to(ROOT)).replace("\\", "/"),
            "renpy_audio_path": renpy_audio_path(v2_subdir, e["id"]),
            "manifest": e.get("manifest", ""),
        }
        try:
            if used_perf and tts_text != e["text"]:
                print(f"  PERF {e['id']}: tagged TTS ({len(tts_text)} chars)")
            audio = synthesize(tts_text, vid, model_id, api_key)
            if not audio:
                raise RuntimeError("empty audio response")
            write_atomic(mp3_path, audio)
            embed_mp3_metadata(mp3_path, meta)
            with lock:
                upsert_manifest_entry(v2_manifest, meta)
                write_v2_manifest(v2_manifest)
                done_ids.append(e["id"])
                n = len(done_ids)
            print(f"  [{n}/{len(todo)}] {e['id']} ok ({len(audio)} bytes)")
        except GenerationHalted as ge:
            stop.set()
            with lock:
                if not halt_msg["text"]:
                    halt_msg["text"] = str(ge)
            print(f"  HALTED on {e['id']}: {ge}", file=sys.stderr)
        except Exception as ex:  # noqa: BLE001
            print(f"  FAIL {e['id']}: {ex}", file=sys.stderr)

    with ThreadPoolExecutor(max_workers=max(1, args.concurrency)) as pool:
        futures = [pool.submit(worker, e) for e in todo]
        for _ in as_completed(futures):
            pass

    generated = set(done_ids)
    remaining = [e["id"] for e in todo if e["id"] not in generated]

    if remaining:
        MISSING_FILE.write_text("\n".join(remaining) + "\n", encoding="utf-8")
        print()
        print(f"generated: {len(generated)}  remaining: {len(remaining)}")
        if halt_msg["text"]:
            print(f"STOPPED: {halt_msg['text'][:300]}")
        print(f"Resume: python scripts/regenerate_voice_with_metadata.py "
              f"--ids @{MISSING_FILE.as_posix()}")
        return 1

    if MISSING_FILE.exists() and not args.ids and not args.text:
        MISSING_FILE.unlink()

    print()
    print(f"generated: {len(generated)}")
    print(f"v2 manifest: {V2_MANIFEST}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
