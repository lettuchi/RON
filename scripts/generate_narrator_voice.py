#!/usr/bin/env python3
"""Generate ElevenLabs NARRATOR voiceover MP3s for Ryoko Owari Nights.

This is a *separate* pass from the toa/kaoru character voices in
generate_voice.py: it uses its own ElevenLabs account / voice, its own
manifest (scripts/narrator_manifest.json), and its own missing-ids file
(scripts/missing_narrator_ids.txt). Output MP3s still land in the shared
game/audio/voice/ directory but use the narrator_NNN.mp3 namespace.

"Narration" = a Ren'Py *say* statement with NO character tag: a bare quoted
string on its own line (the implicit narrator). The following are NOT narration
and are excluded:
  * character lines      toa "..."   / kaoru "..."
  * named-speaker lines   "Clerk" "..." / "Okami" "..." / "Suzu" / "Factor" ...
  * menu choice captions  "...":      (and conditional choices "..." if x:)
  * centered title cards  centered "..."

IDs are narrator_001, narrator_002, ... in first-appearance order across the
scanned files. Identical narration text is deduplicated to a single MP3 (the
voice statement is still wired in front of every occurrence).

Secrets come from the environment (never hardcode keys). A local gitignored
scripts/.env is loaded automatically if present:

    ELEVENLABS_API_KEY_NARRATOR   (required for real generation; falls back to
                                   ELEVENLABS_API_KEY if unset)
    ELEVENLABS_VOICE_NARRATOR     (default: AeRdCCKzvd23BpJoofzx)
    ELEVENLABS_MODEL_ID           (default: eleven_multilingual_v2)

Examples (run from the project root):
    python scripts/generate_narrator_voice.py --rebuild --dry-run  # plan only
    python scripts/generate_narrator_voice.py --check              # account probe
    python scripts/generate_narrator_voice.py                      # generate missing
    python scripts/generate_narrator_voice.py --ids narrator_001,narrator_002
    python scripts/generate_narrator_voice.py --ids @scripts/missing_narrator_ids.txt
    python scripts/generate_narrator_voice.py --wire               # insert voice lines
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
from pathlib import Path
from urllib import error, request

ROOT = Path(__file__).resolve().parents[1]
GAME_DIR = ROOT / "game"
VOICE_DIR = GAME_DIR / "audio" / "voice"
SCRIPTS_DIR = ROOT / "scripts"
MANIFEST = SCRIPTS_DIR / "narrator_manifest.json"
PERFORMANCE_MANIFEST = SCRIPTS_DIR / "voice_performance_manifest.json"
MISSING_FILE = SCRIPTS_DIR / "missing_narrator_ids.txt"
ENV_FILE = SCRIPTS_DIR / ".env"

# Story .rpy files scanned in first-appearance order (fixes narrator_NNN assignment).
# Keep in sync with wired narration across prologue, cases 1–5, bad ends, game overs.
RPY_REL_PATHS = [
    "prologue.rpy",
    "prologue_canon_encounter.rpy",
    "case1_companion.rpy",
    "case1_investigation.rpy",
    "case2_investigation.rpy",
    "case2_festival.rpy",
    "epilogue_rain_gameover.rpy",
    "case3_investigation.rpy",
    "case3_5_date_interlude.rpy",
    "case4_investigation.rpy",
    "case4_5_boat.rpy",
    "case_endings.rpy",
]

RPY_SKIP_DIRS = frozenset({"versions", "images"})
RPY_SKIP_NAME_PREFIXES = ("test_",)
RPY_SKIP_NAMES = frozenset({"testcases.rpy", "script.rpy", "mute_narrator.rpy"})

NARRATOR_ID_IN_GAME_RE = re.compile(r"narrator_(\d+)")


def narrator_rpy_files() -> list[Path]:
    """Story .rpy files in first-appearance order (see RPY_REL_PATHS)."""
    return [GAME_DIR / rel for rel in RPY_REL_PATHS]


def discover_unlisted_narrator_rpy() -> list[Path]:
    """game/**/*.rpy with bare narrator says not listed in RPY_REL_PATHS."""
    known = {p.resolve() for p in narrator_rpy_files() if p.is_file()}
    found: list[Path] = []
    for path in sorted(GAME_DIR.rglob("*.rpy")):
        if any(part in RPY_SKIP_DIRS for part in path.parts):
            continue
        if path.name.startswith(RPY_SKIP_NAME_PREFIXES) or path.name in RPY_SKIP_NAMES:
            continue
        if path.resolve() in known:
            continue
        if next(iter_narration(path), None) is not None:
            found.append(path)
    return found


API_BASE = "https://api.elevenlabs.io"
DEFAULT_VOICE = "AeRdCCKzvd23BpJoofzx"
DEFAULT_MODEL = "eleven_multilingual_v2"
ID_PREFIX = "narrator_"

# A bare narrator say line is a line that, once stripped of leading whitespace,
# is exactly one complete double-quoted string and nothing else. This naturally
# rejects: tag-prefixed lines (toa/kaoru/centered), "Name" "Text" two-arg says,
# and menu choices (which end in ':' or carry an `if` condition).
NARRATOR_RE = re.compile(r'^"((?:\\.|[^"\\])*)"\s*$')
TEXT_TAG_RE = re.compile(r"\{[^}]*\}")  # Ren'Py text tags like {i}...{/i}
VOICE_LINE_RE = re.compile(r'^\s*voice\s+"audio/voice/[^"]+\.mp3"\s*$')


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


def clean_text(raw: str) -> str:
    """Normalize a raw quoted-string body into clean TTS text."""
    text = raw.replace('\\"', '"').replace("\\'", "'")
    text = text.replace("\\n", " ").replace("\\\\", "\\")
    text = TEXT_TAG_RE.sub("", text)
    return re.sub(r"\s+", " ", text).strip()


def iter_narration(path: Path):
    """Yield (line_index, indent, clean_text) for each narrator say line."""
    if not path.is_file():
        print(f"  WARNING: missing script file {path}", file=sys.stderr)
        return
    src = path.read_text(encoding="utf-8").splitlines()
    for i, line in enumerate(src):
        stripped = line.strip()
        if not stripped or not stripped.startswith('"'):
            continue
        m = NARRATOR_RE.match(stripped)
        if not m:
            continue
        text = clean_text(m.group(1))
        if not text:
            continue
        indent = line[: len(line) - len(line.lstrip())]
        yield i, indent, text


# ---------------------------------------------------------------------------
# Manifest building
# ---------------------------------------------------------------------------
def build_manifest() -> dict:
    lines: list[dict] = []
    by_text: dict[str, str] = {}      # clean text -> id (dedup)
    collisions: list[dict] = []       # informational: same text reused
    occurrences = 0
    n = 0

    for rpy in narrator_rpy_files():
        for idx, _indent, text in iter_narration(rpy):
            occurrences += 1
            if text in by_text:
                collisions.append({
                    "id": by_text[text],
                    "reused_at": f"{rpy.name}:{idx + 1}",
                    "text": text,
                })
                continue
            n += 1
            vid = f"{ID_PREFIX}{n:03d}"
            by_text[text] = vid
            lines.append({
                "id": vid,
                "character": "narrator",
                "text": text,
                "source": f"{rpy.name}:{idx + 1}",
            })

    scanned = ", ".join(p.name for p in narrator_rpy_files() if p.is_file())
    return {
        "description": (
            "Narrator (no-character) lines extracted from game story .rpy files "
            f"({scanned}). Excludes character/named-speaker lines, menu choices, "
            "and centered cards. Deduplicated by exact text in first-appearance "
            "order; repeated narration shares one MP3."
        ),
        "ordering": "first_appearance",
        "model_id": os.environ.get("ELEVENLABS_MODEL_ID", DEFAULT_MODEL),
        "voice": os.environ.get("ELEVENLABS_VOICE_NARRATOR", DEFAULT_VOICE),
        "stats": {
            "occurrences": occurrences,
            "unique": len(lines),
            "duplicate_occurrences": len(collisions),
        },
        "duplicate_occurrences": collisions,
        "lines": lines,
    }


def write_manifest(manifest: dict) -> None:
    SCRIPTS_DIR.mkdir(parents=True, exist_ok=True)
    MANIFEST.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
                        encoding="utf-8")


def performance_narrator_count() -> int:
    """Narrator line count from voice_performance_manifest.json (0 if missing)."""
    if not PERFORMANCE_MANIFEST.is_file():
        return 0
    data = json.loads(PERFORMANCE_MANIFEST.read_text(encoding="utf-8"))
    counts = data.get("counts") or {}
    n = counts.get("narrator")
    if isinstance(n, int) and n > 0:
        return n
    return sum(
        1 for e in data.get("entries", [])
        if str(e.get("id", "")).startswith(ID_PREFIX)
    )


def max_narrator_id_in_game() -> int:
    """Highest narrator_NNN referenced under game/ (excludes versions/, tests)."""
    highest = 0
    for path in GAME_DIR.rglob("*.rpy"):
        if any(part in RPY_SKIP_DIRS for part in path.parts):
            continue
        if path.name.startswith(RPY_SKIP_NAME_PREFIXES):
            continue
        for match in NARRATOR_ID_IN_GAME_RE.finditer(
                path.read_text(encoding="utf-8")):
            highest = max(highest, int(match.group(1)))
    return highest


def validate_rebuild_scope(manifest: dict, force: bool) -> int:
    """Abort rebuild if scan looks truncated vs project expectations."""
    unique = manifest["stats"]["unique"]
    perf_n = performance_narrator_count()
    max_id = max_narrator_id_in_game()
    # Allow a few IDs to share deduped text (see narrator_manifest duplicates).
    floor = max(perf_n, max_id) - 4 if max_id else perf_n
    if floor and unique < floor and not force:
        print(
            f"ERROR: --rebuild found only {unique} unique narrator lines; "
            f"expected at least ~{floor} (performance manifest: {perf_n}, "
            f"max wired id: narrator_{max_id:03d}).\n"
            "  Expand RPY_REL_PATHS or pass --force to write anyway.",
            file=sys.stderr,
        )
        return 1
    return 0


# ---------------------------------------------------------------------------
# ElevenLabs API
# ---------------------------------------------------------------------------
class GenerationHalted(Exception):
    """Stop the whole batch: quota/credit exhaustion, rate-limit exhaustion,
    or plan-tier restriction (e.g. free account needing a paid plan)."""


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
# Wiring: insert `voice "audio/voice/{id}.mp3"` before each narration line
# ---------------------------------------------------------------------------
def wire_files(manifest: dict, require_mp3: bool = True) -> dict:
    text_to_id = {e["text"]: e["id"] for e in manifest["lines"]}
    summary: dict[str, int] = {}

    for rpy in narrator_rpy_files():
        if not rpy.is_file():
            continue
        src = rpy.read_text(encoding="utf-8").splitlines()
        out: list[str] = []
        inserted = 0
        for i, line in enumerate(src):
            stripped = line.strip()
            is_narr = bool(stripped and stripped.startswith('"')
                           and NARRATOR_RE.match(stripped))
            if is_narr:
                text = clean_text(NARRATOR_RE.match(stripped).group(1))
                vid = text_to_id.get(text)
                already = bool(out) and VOICE_LINE_RE.match(out[-1] or "")
                mp3_ok = (not require_mp3) or (
                    vid is not None and (VOICE_DIR / f"{vid}.mp3").exists()
                    and (VOICE_DIR / f"{vid}.mp3").stat().st_size > 0
                )
                if vid and not already and mp3_ok:
                    indent = line[: len(line) - len(line.lstrip())]
                    out.append(f'{indent}voice "audio/voice/{vid}.mp3"')
                    inserted += 1
            out.append(line)
        if inserted:
            text = "\n".join(out)
            if src and rpy.read_text(encoding="utf-8").endswith("\n"):
                text += "\n"
            rpy.write_text(text, encoding="utf-8")
        summary[rpy.name] = inserted
    return summary


# ---------------------------------------------------------------------------
# Commands
# ---------------------------------------------------------------------------
def cmd_check(voice_id, model_id, api_key) -> int:
    if not api_key:
        print("ERROR: narrator API key is not set "
              "(ELEVENLABS_API_KEY_NARRATOR).", file=sys.stderr)
        return 2
    print("Checking ElevenLabs narrator account access...")
    try:
        sub = api_get("/v1/user/subscription", api_key)
        used, limit, tier = sub.get("character_count"), sub.get("character_limit"), sub.get("tier")
        remaining = None if limit is None else limit - (used or 0)
        print(f"  subscription: tier={tier} used={used} limit={limit} remaining={remaining}")
    except Exception as e:  # noqa: BLE001
        print(f"  subscription lookup failed: {e}", file=sys.stderr)
    try:
        audio = synthesize("Test.", voice_id, model_id, api_key)
        print(f"  synth narrator ({voice_id}): OK, {len(audio)} bytes")
        return 0
    except Exception as e:  # noqa: BLE001
        print(f"  synth narrator ({voice_id}): FAILED -> {e}", file=sys.stderr)
        return 1


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
    ap = argparse.ArgumentParser(description="Generate ElevenLabs narrator voice MP3s.")
    ap.add_argument("--dry-run", action="store_true",
                    help="Show what would be generated; make no API calls.")
    ap.add_argument("--ids", default="",
                    help="Comma-separated ids, or @file with ids, to (re)generate.")
    ap.add_argument("--force", action="store_true",
                    help="Regenerate even if a non-empty MP3 already exists.")
    ap.add_argument("--rebuild", action="store_true",
                    help="Re-parse the .rpy files and overwrite the manifest.")
    ap.add_argument("--check", action="store_true",
                    help="Verify API key + voice access via a tiny synth; then exit.")
    ap.add_argument("--wire", action="store_true",
                    help="Insert `voice` lines before generated narration; then exit.")
    ap.add_argument("--concurrency", type=int, default=4,
                    help="Max concurrent API requests (default 4).")
    args = ap.parse_args()

    load_env_file(ENV_FILE)
    api_key = (os.environ.get("ELEVENLABS_API_KEY_NARRATOR")
               or os.environ.get("ELEVENLABS_API_KEY", "")).strip()
    model_id = os.environ.get("ELEVENLABS_MODEL_ID", DEFAULT_MODEL).strip()
    voice_id = os.environ.get("ELEVENLABS_VOICE_NARRATOR", DEFAULT_VOICE).strip()

    if args.rebuild or not MANIFEST.is_file():
        # WARNING: --rebuild re-parses RPY_REL_PATHS (+ any extra narrator .rpy),
        # reassigns narrator_001..NNN in first-appearance order, and overwrites
        # scripts/narrator_manifest.json. Existing MP3 / voice line IDs in game/
        # will not match unless scan order matches the original wiring pass.
        if args.rebuild:
            print(
                "NOTE: --rebuild overwrites narrator_manifest.json and reassigns "
                "IDs from RPY scan order. Use --dry-run to preview without writing.",
                file=sys.stderr,
            )
        manifest = build_manifest()
        if args.rebuild:
            unlisted = discover_unlisted_narrator_rpy()
            if unlisted:
                names = ", ".join(p.relative_to(GAME_DIR).as_posix() for p in unlisted)
                print(
                    f"WARN: narrator say lines in .rpy not listed in RPY_REL_PATHS: {names}",
                    file=sys.stderr,
                )
            rc = validate_rebuild_scope(manifest, args.force)
            if rc:
                return rc
        if args.dry_run:
            print(f"(dry-run) would write manifest -> {MANIFEST}")
        else:
            write_manifest(manifest)
        s = manifest["stats"]
        label = "manifest built (dry-run)" if args.dry_run else "manifest built"
        print(f"{label} -> {MANIFEST}")
        print(f"  occurrences={s['occurrences']} unique={s['unique']} "
              f"duplicate_occurrences={s['duplicate_occurrences']}")
        for c in manifest["duplicate_occurrences"]:
            print(f"    reuse {c['id']} at {c['reused_at']}")
    else:
        manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))

    VOICE_DIR.mkdir(parents=True, exist_ok=True)

    if args.check:
        return cmd_check(voice_id, model_id, api_key)

    if args.wire:
        summary = wire_files(manifest)
        total = sum(summary.values())
        print(f"wired {total} voice statements:")
        for name, count in summary.items():
            print(f"  {name}: +{count}")
        return 0

    entries = select_entries(manifest, args.ids)

    def needs_gen(e):
        p = VOICE_DIR / f"{e['id']}.mp3"
        return args.force or (not p.exists()) or p.stat().st_size == 0

    todo = [e for e in entries if needs_gen(e)]
    skip = [e for e in entries if not needs_gen(e)]
    total_chars = sum(len(e["text"]) for e in todo)

    print(f"manifest lines: {len(manifest['lines'])}")
    print(f"selected: {len(entries)}  present (skip): {len(skip)}  to generate: {len(todo)}")
    print(f"approx characters to synthesize: {total_chars}")
    print(f"model: {model_id}  voice: {voice_id}")

    if args.dry_run:
        for e in todo:
            print(f"  WOULD GEN {e['id']} ({len(e['text'])} chars)")
        return 0

    if not todo:
        print("Nothing to generate. All selected files already present.")
        if MISSING_FILE.exists() and not args.ids:
            MISSING_FILE.unlink()
        return 0

    if not api_key:
        print("ERROR: narrator API key is not set "
              "(ELEVENLABS_API_KEY_NARRATOR). Aborting.", file=sys.stderr)
        return 2

    stop = threading.Event()
    lock = threading.Lock()
    done_ids: list[str] = []
    failed: dict[str, str] = {}
    halt_msg = {"text": ""}

    def worker(e):
        if stop.is_set():
            return
        try:
            audio = synthesize(e["text"], voice_id, model_id, api_key)
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
        print(f"  python scripts/generate_narrator_voice.py --ids @{MISSING_FILE.as_posix()}")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
