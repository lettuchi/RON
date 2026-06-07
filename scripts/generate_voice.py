#!/usr/bin/env python3
"""Generate ElevenLabs voiceover MP3s for Ryoko Owari Nights.

Builds scripts/voice_manifest.json from the four voiced .rpy files (dedup by id,
first appearance wins) and synthesizes any missing game/audio/voice/{id}.mp3
files via the ElevenLabs text-to-speech REST API.

Secrets come from the environment (never hardcode keys):

    ELEVENLABS_API_KEY     (required for real generation)
    ELEVENLABS_VOICE_TOA   (default: Carla         l32B8XDoylOsZKiSdfhE)
    ELEVENLABS_VOICE_KAORU (default: Jax Meridian  iB0m5bo5Htdz0t9yE0xq)
    ELEVENLABS_MODEL_ID    (default: eleven_multilingual_v2)

A local scripts/.env (gitignored) is loaded automatically if present.

Examples (run from the project root):
    python scripts/generate_voice.py --rebuild --dry-run   # rebuild manifest, plan only
    python scripts/generate_voice.py --check               # API key / voice / quota probe
    python scripts/generate_voice.py                        # generate all missing
    python scripts/generate_voice.py --ids toa_001,kaoru_152
    python scripts/generate_voice.py --ids @scripts/missing_voice_ids.txt
    python scripts/generate_voice.py --force                # regenerate even if present
"""
from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
import threading
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from urllib import error, request

ROOT = Path(__file__).resolve().parents[1]
GAME_DIR = ROOT / "game"
VOICE_DIR = GAME_DIR / "audio" / "voice"
SCRIPTS_DIR = ROOT / "scripts"
MANIFEST = SCRIPTS_DIR / "voice_manifest.json"
MISSING_FILE = SCRIPTS_DIR / "missing_voice_ids.txt"
ENV_FILE = SCRIPTS_DIR / ".env"

# Scanned in first-appearance order; order matters for dedup tie-breaks.
RPY_FILES = [
    GAME_DIR / "prologue.rpy",
    GAME_DIR / "prologue_canon_encounter.rpy",
    GAME_DIR / "case1_companion.rpy",
    GAME_DIR / "case1_investigation.rpy",
]

API_BASE = "https://api.elevenlabs.io"

DEFAULT_VOICES = {
    "toa": "l32B8XDoylOsZKiSdfhE",    # Carla
    "kaoru": "iB0m5bo5Htdz0t9yE0xq",  # Jax Meridian
}
DEFAULT_MODEL = "eleven_multilingual_v2"


# ---------------------------------------------------------------------------
# Environment / config
# ---------------------------------------------------------------------------
def load_env_file(path: Path) -> None:
    """Minimal .env loader: KEY=VALUE lines, # comments allowed. Real env wins."""
    if not path.exists():
        return
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, val = line.partition("=")
        os.environ.setdefault(key.strip(), val.strip().strip('"').strip("'"))


def voice_for(entry: dict, voices: dict) -> str:
    return entry.get("voice_id") or voices[entry["character"]]


# ---------------------------------------------------------------------------
# Manifest building (parse .rpy)
# ---------------------------------------------------------------------------
VOICE_RE = re.compile(r'voice\s+"audio/voice/([A-Za-z0-9_]+)\.mp3"')
SAY_RE = re.compile(r'^\s*(toa|kaoru)\b\s*(.*)$')
TEXT_TAG_RE = re.compile(r"\{[^}]*\}")  # Ren'Py text tags like {i}...{/i}


def _extract_text(say_body: str) -> str:
    first, last = say_body.find('"'), say_body.rfind('"')
    if first == -1 or last <= first:
        return ""
    text = say_body[first + 1:last]
    text = text.replace('\\"', '"').replace("\\'", "'")
    text = text.replace("\\n", " ").replace("\\\\", "\\")
    text = TEXT_TAG_RE.sub("", text)
    return re.sub(r"\s+", " ", text).strip()


def build_manifest() -> dict:
    lines: list[dict] = []
    by_id: dict[str, dict] = {}
    conflicts: list[dict] = []

    for rpy in RPY_FILES:
        if not rpy.is_file():
            print(f"  WARNING: missing script file {rpy}", file=sys.stderr)
            continue
        content = rpy.read_text(encoding="utf-8").splitlines()
        for i, line in enumerate(content):
            m = VOICE_RE.search(line)
            if not m:
                continue
            voice_id = m.group(1)
            say_line = next((content[j] for j in range(i + 1, min(i + 4, len(content)))
                             if content[j].strip()), None)
            if say_line is None:
                conflicts.append({"id": voice_id, "file": rpy.name, "line": i + 1,
                                  "issue": "no say line found"})
                continue
            say_m = SAY_RE.match(say_line)
            if not say_m:
                conflicts.append({"id": voice_id, "file": rpy.name, "line": i + 1,
                                  "issue": f"next line not a say stmt: {say_line.strip()!r}"})
                continue
            speaker = say_m.group(1)
            text = _extract_text(say_m.group(2))
            prefix = voice_id.split("_", 1)[0]
            if prefix != speaker:
                conflicts.append({"id": voice_id, "file": rpy.name, "line": i + 1,
                                  "issue": f"id prefix {prefix!r} != speaker {speaker!r}"})
            if voice_id in by_id:
                if by_id[voice_id]["text"] != text:
                    conflicts.append({
                        "id": voice_id, "file": rpy.name, "line": i + 1,
                        "issue": "duplicate id with differing text (kept first appearance)",
                        "first_text": by_id[voice_id]["text"], "this_text": text})
                continue  # first appearance wins
            entry = {"id": voice_id, "character": speaker, "text": text}
            by_id[voice_id] = entry
            lines.append(entry)

    n_toa = sum(1 for e in lines if e["character"] == "toa")
    n_kaoru = sum(1 for e in lines if e["character"] == "kaoru")
    return {
        "description": ("Voiced dialogue extracted from prologue.rpy, "
                        "prologue_canon_encounter.rpy, case1_companion.rpy, "
                        "case1_investigation.rpy. Deduplicated by id; first appearance wins."),
        "ordering": "first_appearance",
        "counts": {"total": len(lines), "toa": n_toa, "kaoru": n_kaoru},
        "conflicts": conflicts,
        "lines": lines,
    }


def write_manifest(manifest: dict) -> None:
    SCRIPTS_DIR.mkdir(parents=True, exist_ok=True)
    MANIFEST.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
                        encoding="utf-8")


# ---------------------------------------------------------------------------
# ElevenLabs API
# ---------------------------------------------------------------------------
class GenerationHalted(Exception):
    """Conditions that require user action and should stop the whole batch:
    quota/credit exhaustion, rate-limit exhaustion, or plan-tier restriction."""


def synthesize(text: str, voice_id: str, model_id: str, api_key: str,
               max_retries: int = 5) -> bytes:
    url = f"{API_BASE}/v1/text-to-speech/{voice_id}"
    body = json.dumps({"text": text, "model_id": model_id}).encode("utf-8")
    headers = {"xi-api-key": api_key, "Content-Type": "application/json",
               "Accept": "audio/mpeg"}
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
            # Plan-tier restriction (e.g. free account using library voices).
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
    tmp = path.with_suffix(path.suffix + ".part")
    tmp.write_bytes(data)
    tmp.replace(path)


# ---------------------------------------------------------------------------
# Commands
# ---------------------------------------------------------------------------
def cmd_check(voices, model_id, api_key) -> int:
    if not api_key:
        print("ERROR: ELEVENLABS_API_KEY is not set.", file=sys.stderr)
        return 2
    print("Checking ElevenLabs account access...")
    try:
        sub = api_get("/v1/user/subscription", api_key)
        used, limit, tier = sub.get("character_count"), sub.get("character_limit"), sub.get("tier")
        remaining = None if limit is None else limit - (used or 0)
        print(f"  subscription: tier={tier} used={used} limit={limit} remaining={remaining}")
    except Exception as e:  # noqa: BLE001
        print(f"  subscription lookup failed: {e}", file=sys.stderr)
    try:
        data = api_get("/v1/voices", api_key)
        ids = {v.get("voice_id"): v.get("name") for v in data.get("voices", [])}
        for tag, vid in voices.items():
            print(f"  voice {tag}: {vid} -> "
                  + (f"OK ({ids[vid]})" if vid in ids
                     else "NOT in /v1/voices list (may need adding to account)"))
    except Exception as e:  # noqa: BLE001
        print(f"  /v1/voices lookup failed: {e}", file=sys.stderr)
    # Definitive proof of access: one tiny synthesis per voice.
    rc = 0
    for tag, vid in voices.items():
        try:
            audio = synthesize("Test.", vid, model_id, api_key)
            print(f"  synth {tag} ({vid}): OK, {len(audio)} bytes")
        except Exception as e:  # noqa: BLE001
            print(f"  synth {tag} ({vid}): FAILED -> {e}", file=sys.stderr)
            rc = 1
    return rc


def parse_ids_arg(ids_arg: str) -> list[str]:
    if ids_arg.startswith("@"):
        raw = Path(ids_arg[1:]).read_text(encoding="utf-8")
        tokens = re.split(r"[,\s]+", raw)
    else:
        tokens = ids_arg.split(",")
    return [t.strip() for t in tokens if t.strip()]


def select_entries(manifest, ids_arg):
    lines = manifest["lines"]
    if not ids_arg:
        return lines
    by_id = {e["id"]: e for e in lines}
    out = []
    for w in parse_ids_arg(ids_arg):
        if w not in by_id:
            print(f"WARN: id {w!r} not in manifest; skipping", file=sys.stderr)
            continue
        out.append(by_id[w])
    return out


def main() -> int:
    ap = argparse.ArgumentParser(description="Generate ElevenLabs voice MP3s.")
    ap.add_argument("--dry-run", action="store_true",
                    help="Show what would be generated; make no API calls.")
    ap.add_argument("--ids", default="",
                    help="Comma-separated ids, or @file with ids, to (re)generate.")
    ap.add_argument("--force", action="store_true",
                    help="Regenerate even if a non-empty MP3 already exists.")
    ap.add_argument("--rebuild", action="store_true",
                    help="Re-parse the .rpy files and overwrite the manifest.")
    ap.add_argument("--check", action="store_true",
                    help="Verify API key, voice access, and quota; then exit.")
    ap.add_argument("--concurrency", type=int, default=4,
                    help="Max concurrent API requests (default 4).")
    args = ap.parse_args()

    load_env_file(ENV_FILE)
    api_key = os.environ.get("ELEVENLABS_API_KEY", "").strip()
    model_id = os.environ.get("ELEVENLABS_MODEL_ID", DEFAULT_MODEL).strip()
    voices = {
        "toa": os.environ.get("ELEVENLABS_VOICE_TOA", DEFAULT_VOICES["toa"]).strip(),
        "kaoru": os.environ.get("ELEVENLABS_VOICE_KAORU", DEFAULT_VOICES["kaoru"]).strip(),
    }

    if args.rebuild or not MANIFEST.is_file():
        canonical = SCRIPTS_DIR / "build_manifest.py"
        if canonical.is_file():
            # Defer to the project's canonical builder to preserve its schema.
            print(f"rebuilding manifest via {canonical.name} ...")
            subprocess.run([sys.executable, str(canonical)], check=True)
            manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
        else:
            manifest = build_manifest()
            write_manifest(manifest)
            c = manifest["counts"]
            print(f"manifest built -> {MANIFEST}")
            print(f"  total={c['total']} toa={c['toa']} kaoru={c['kaoru']} "
                  f"conflicts={len(manifest['conflicts'])}")
            for conf in manifest["conflicts"]:
                print(f"    conflict: {conf}")
    else:
        manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))

    VOICE_DIR.mkdir(parents=True, exist_ok=True)

    if args.check:
        return cmd_check(voices, model_id, api_key)

    entries = select_entries(manifest, args.ids)

    def needs_gen(e):
        p = VOICE_DIR / f"{e['id']}.mp3"
        return args.force or (not p.exists()) or p.stat().st_size == 0

    todo = [e for e in entries if needs_gen(e)]
    skip = [e for e in entries if not needs_gen(e)]
    total_chars = sum(len(e["text"]) for e in todo)

    print(f"manifest lines: {len(manifest['lines'])}")
    print(f"selected: {len(entries)}  already present (skip): {len(skip)}  to generate: {len(todo)}")
    print(f"approx characters to synthesize: {total_chars}")
    print(f"model: {model_id}  voices: toa={voices['toa']} kaoru={voices['kaoru']}")

    if args.dry_run:
        for e in todo:
            print(f"  WOULD GEN {e['id']} ({e['character']}, {len(e['text'])} chars)")
        return 0

    if not todo:
        print("Nothing to generate. All selected files already present.")
        if MISSING_FILE.exists() and not args.ids:
            MISSING_FILE.unlink()
        return 0

    if not api_key:
        print("ERROR: ELEVENLABS_API_KEY is not set. Aborting.", file=sys.stderr)
        return 2

    stop = threading.Event()
    lock = threading.Lock()
    done_ids: list[str] = []
    failed: dict[str, str] = {}
    halt_msg = {"text": ""}

    def worker(e):
        if stop.is_set():
            return
        vid = voice_for(e, voices)
        try:
            audio = synthesize(e["text"], vid, model_id, api_key)
            if not audio:
                raise RuntimeError("empty audio response")
            write_atomic(VOICE_DIR / f"{e['id']}.mp3", audio)
            with lock:
                done_ids.append(e["id"])
                n = len(done_ids)
            print(f"  [{n}/{len(todo)}] {e['id']} ok ({len(audio)} bytes)")
        except GenerationHalted as ge:
            stop.set()
            with lock:
                if not halt_msg["text"]:
                    halt_msg["text"] = str(ge)
                failed[e["id"]] = f"halted: {ge}"
            print(f"  HALTED on {e['id']}: {ge}", file=sys.stderr)
        except Exception as ex:  # noqa: BLE001
            with lock:
                failed[e["id"]] = str(ex)
            print(f"  FAIL {e['id']}: {ex}", file=sys.stderr)

    with ThreadPoolExecutor(max_workers=max(1, args.concurrency)) as pool:
        futures = [pool.submit(worker, e) for e in todo]
        for _ in as_completed(futures):
            pass

    generated = set(done_ids)
    remaining = [e["id"] for e in todo if e["id"] not in generated]

    if remaining:
        MISSING_FILE.write_text("\n".join(remaining) + "\n", encoding="utf-8")
    elif MISSING_FILE.exists() and not args.ids:
        MISSING_FILE.unlink()

    print()
    print(f"generated: {len(generated)}")
    print(f"failed/remaining: {len(remaining)}")
    if remaining:
        if halt_msg["text"]:
            print(f"STOPPED early (quota/plan/rate limit): {halt_msg['text'][:300]}")
        print(f"missing ids written to: {MISSING_FILE}")
        print("Resume with:")
        print(f"  python scripts/generate_voice.py --ids @{MISSING_FILE.as_posix()}")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
