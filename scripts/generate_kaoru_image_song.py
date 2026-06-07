#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Generate Kaoru's image song 「権利の帳」 (Kenri no Chō) via Eleven Music.

Character image song — polished otome-route energy (Hakuoki-style image song:
smooth baritone, ~128–132 BPM, pop-rock/orchestral sheen), NOT the slow ED ballad
「嘘つきの糸」 and NOT raspy metal/screaming. Locked lyrics:
docs/kaoru-image-song-kenri-lyrics.md.

Writes: game/audio/bgm/kaoru_image_song_kenri.mp3 (primary; latest generation).
Never overwrites ending_song.mp3 or ending_song_v2.mp3.

Before replacing an existing primary MP3, backs up to
game/audio/bgm/versions/kaoru_image_song_kenri_backup_YYYYMMDD_HHMMSS.mp3
unless --no-backup. Keep named copies (v2_energetic, v3_hakuoki, etc.) manually
or via docs/kaoru-image-song-versions.md.

API key: ELEVENLABS_API_KEY (environment; scripts/.env loaded like generate_music.py).

Usage (project root):
    python scripts/generate_kaoru_image_song.py --dry-run
    python scripts/generate_kaoru_image_song.py
    python scripts/generate_kaoru_image_song.py --regen
    python scripts/generate_kaoru_image_song.py --regen --no-backup
    python scripts/generate_kaoru_image_song.py --regen --model v2   # Eleven Music v2 (default)
    python scripts/generate_kaoru_image_song.py --regen --model v1   # fallback to music_v1

PowerShell (if key not in scripts/.env):
    $env:ELEVENLABS_API_KEY = "sk_..."
    python scripts/generate_kaoru_image_song.py
"""
from __future__ import annotations

import argparse
import json
import os
import shutil
import sys
import time
from datetime import datetime
from pathlib import Path
from urllib import error, request

ROOT = Path(__file__).resolve().parents[1]
BGM_DIR = ROOT / "game" / "audio" / "bgm"
VERSIONS_DIR = BGM_DIR / "versions"
OUT_FILE = BGM_DIR / "kaoru_image_song_kenri.mp3"
SCRIPTS_DIR = ROOT / "scripts"
ENV_FILE = SCRIPTS_DIR / ".env"

API_BASE = "https://api.elevenlabs.io"
MUSIC_MODEL_V1 = "music_v1"
MUSIC_MODEL_V2 = "music_v2"
MUSIC_MODEL_DEFAULT = MUSIC_MODEL_V2
OUTPUT_FORMAT = "mp3_44100_128"

# Locked lyrics (docs/kaoru-image-song-kenri-lyrics.md)
INTRO_LINES = [
    "記録は嘘を裁かない。裁くのは、私だ。",
]
VERSE1_LINES = [
    "夜の運河　灯りは泳ぐ",
    "帳の背表紙　指先が慣れた",
    "師の名を借り　印を押せば",
    "誰かの明日が　今日の遊びになる",
    "石畳の響き　靴底が笑う",
    "帳の重さだけ　先を行けば",
    "この街は正直　嘘しか吐かない",
    "だから正直に　欲しいものを奪う",
]
PRECHORUS_LINES = [
    "恥？　隠す理由がない",
    "権利は　見えている者のもの",
]
CHORUS_LINES = [
    "帳を閉じない　まだ足りない",
    "甘い声も　涙も　証拠の一部",
    "裁きの夜に　踊れ　踊れ",
    "「拒む」なんて　可愛い嘘",
    "権利の帳　ページを増やせ",
    "君の沈黙も　署名に変えて",
    "この街の王は　いない——",
    "いるのは　私だけ",
]
VERSE2_LINES = [
    "翡翠の印　菊の布が揺れる",
    "奉行の帳　一枚が全て",
    "墨の夜に　ページを増やせ",
    "笑いながら　先を行く",
    "女の肌は　紙より薄い？",
    "違う　紙の方が　よく嘘をつく",
    "官の腕は　長い　長い",
    "届く場所まで　全部　預かりなさい",
]
BRIDGE_LINES = [
    "冠の教え？　勉強はした",
    "実行は　もっと単純だ",
    "好きなものを　好きなだけ",
    "後悔は　他人の仕事",
    "……さあ、次の名前を",
]
FINAL_CHORUS_LINES = [
    "帳を閉じない　まだ足りない",
    "嘘の街で　本当を遊ぶ",
    "裁きの夜に　踊れ　踊れ",
    "逃げ道も　用意してあげる",
    "権利の帳　血もインクも",
    "乾く前に　次の章へ",
    "王はいない——",
    "奉行　橘　薫",
]
OUTRO_LINES = [
    "記録は残る。君も、残すか？",
]

_GLOBAL_POSITIVE = [
    "Hakuoki-style otome character image song, polished Japanese male vocal",
    "smooth baritone with emotional clarity, NOT raspy or gravelly",
    "tempo 128-132 BPM steady, restrained drums and bass, strings and cinematic pop-rock sheen",
    "subtle shamisen accents only, dramatic but smooth, bishonen route energy",
    "predatory magistrate charm without metal aggression, not melancholic ballad",
    "MALE lead vocal singing in Japanese, crisp consonants, warm controlled delivery",
    "sung entirely in Japanese, clear diction, follows the written lyrics exactly",
    "Legend of the Five Rings Emerald Magistrate aesthetic, orchestral otome OP polish",
    "clear expressive lead vocal mixed forward",
]
_GLOBAL_NEGATIVE = [
    "raspy gravel voice, harsh metal screaming, aggressive punk",
    "slow noir piano ballad, torch song, 60-80 BPM dirge",
    "female vocals, idol voice, high tenor falsetto",
    "English lyrics, improvised ad-libs, scat, gibberish",
    "instrumental only / no vocals",
    "bright cheerful J-pop without menace",
    "heavy autotune, robotic vocals, lo-fi muddy mix",
    "overly hyped EDM drop, 140 BPM metal rush",
]

_NO_ADLIB = [
    "wordless humming in place of lyrics",
    "ad-libbed runs or improvised vocals",
    "English words", "scat singing",
]

SECTIONS = [
    {
        "section_name": "Intro",
        "positive_local_styles": [
            "brief tense intro, ledger pages rustle feel",
            "male baritone speaks-sings the written Japanese lines with cruel smile",
            "building into the first verse",
        ],
        "negative_local_styles": [
            "slow ballad", "female vocal", "instrumental only",
            "long atmospheric build",
        ],
        "duration_ms": 9000,
        "lines": INTRO_LINES,
    },
    {
        "section_name": "Verse 1",
        "positive_local_styles": [
            "controlled forward motion, warm smooth baritone, clear lyric delivery",
            "128-132 BPM steady groove, slight lift not shout, room to grow into chorus",
            "subtle strings and restrained drums, every written line clear and forward",
        ],
        "negative_local_styles": [
            "full intensity from bar one", "raspy shout", "metal scream verse",
            "sparse ballad", "slow dirge", "soft whisper verse",
        ],
        "duration_ms": 29000,
        "lines": VERSE1_LINES,
    },
    {
        "section_name": "Pre-Chorus",
        "positive_local_styles": [
            "rising pre-chorus, tension lift toward chorus",
            "baritone confident and predatory",
        ],
        "negative_local_styles": ["flat dynamics"],
        "duration_ms": 12000,
        "lines": PRECHORUS_LINES,
    },
    {
        "section_name": "Chorus",
        "positive_local_styles": [
            "anthemic polished chorus, orchestral brass and strings, full but smooth band",
            "powerful smooth baritone hook, dramatic judgment-night energy without metal rasp",
        ],
        "negative_local_styles": ["thin", "quiet ballad", "raspy metal scream"],
        "duration_ms": 32000,
        "lines": CHORUS_LINES,
    },
    {
        "section_name": "Verse 2",
        "positive_local_styles": [
            "verse slightly fuller than verse one, steady driving groove",
            "baritone storytelling with restrained menace",
        ],
        "negative_local_styles": ["slow ballad"],
        "duration_ms": 30000,
        "lines": VERSE2_LINES,
    },
    {
        "section_name": "Pre-Chorus (repeat)",
        "positive_local_styles": [
            "rising pre-chorus, tension lift",
            "baritone confident",
        ],
        "negative_local_styles": ["flat dynamics"],
        "duration_ms": 12000,
        "lines": PRECHORUS_LINES,
    },
    {
        "section_name": "Chorus (repeat)",
        "positive_local_styles": [
            "full polished anthemic chorus, brass strings and restrained drums",
            "smooth powerful baritone hook, no raspy metal",
        ],
        "negative_local_styles": ["thin", "quiet", "raspy shout"],
        "duration_ms": 32000,
        "lines": CHORUS_LINES,
    },
    {
        "section_name": "Bridge",
        "positive_local_styles": [
            "half-time bridge, colder and more controlled",
            "intimate baritone then dark laugh energy into final chorus",
            "sing every written Japanese line clearly",
        ],
        "negative_local_styles": ["same as chorus", "up-tempo dance drop"],
        "duration_ms": 22000,
        "lines": BRIDGE_LINES,
    },
    {
        "section_name": "Final Chorus",
        "positive_local_styles": [
            "climactic final chorus, biggest arrangement",
            "baritone triumphant cruel magistrate declaration",
            "resolved ending suitable for image song",
        ],
        "negative_local_styles": ["abrupt cut mid-word"],
        "duration_ms": 34000,
        "lines": FINAL_CHORUS_LINES,
    },
    {
        "section_name": "Outro",
        "positive_local_styles": [
            "outro fade, baritone speaks-sings the written closing line",
            "instrumental tail, not abrupt silence",
        ],
        "negative_local_styles": ["new verse", "female vocal"],
        "duration_ms": 10000,
        "lines": OUTRO_LINES,
    },
]

COMPOSITION_PLAN = {
    "positive_global_styles": _GLOBAL_POSITIVE,
    "negative_global_styles": _GLOBAL_NEGATIVE,
    "sections": SECTIONS,
}


def load_env_file(path: Path) -> None:
    if not path.exists():
        return
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, val = line.partition("=")
        os.environ.setdefault(key.strip(), val.strip().strip('"').strip("'"))


class GenerationHalted(Exception):
    pass


def get_api_key() -> str:
    load_env_file(ENV_FILE)
    key = os.environ.get("ELEVENLABS_API_KEY", "").strip()
    if not key:
        print(
            "ERROR: ELEVENLABS_API_KEY is not set.\n"
            "  Set in PowerShell: $env:ELEVENLABS_API_KEY = \"sk_...\"\n"
            "  Or add to scripts/.env (gitignored).",
            file=sys.stderr,
        )
        raise SystemExit(2)
    return key


def _post_music(payload: dict, api_key: str, max_retries: int = 4) -> tuple[bytes, dict]:
    url = f"{API_BASE}/v1/music?output_format={OUTPUT_FORMAT}"
    body = json.dumps(payload).encode("utf-8")
    headers = {"xi-api-key": api_key, "Content-Type": "application/json"}
    attempt = 0
    while True:
        attempt += 1
        req = request.Request(url, data=body, headers=headers, method="POST")
        try:
            with request.urlopen(req, timeout=600) as resp:
                return resp.read(), dict(resp.headers)
        except error.HTTPError as e:
            payload_txt = e.read().decode("utf-8", "replace")
            low = payload_txt.lower()
            if e.code in (401, 403) or e.code == 402 or "paid" in low or "subscription" in low:
                raise GenerationHalted(f"HTTP {e.code} plan/permission block: {payload_txt}")
            if e.code == 429:
                if "quota" in low or "credit" in low:
                    raise GenerationHalted(f"HTTP 429 quota/credits: {payload_txt}")
                if attempt > max_retries:
                    raise GenerationHalted(f"HTTP 429 after {max_retries} retries: {payload_txt}")
                retry_after = e.headers.get("retry-after")
                time.sleep(float(retry_after) if retry_after else min(2 ** attempt, 30))
                continue
            if 500 <= e.code < 600 and attempt <= max_retries:
                time.sleep(min(2 ** attempt, 30))
                continue
            raise RuntimeError(f"HTTP {e.code}: {payload_txt}")
        except error.URLError as e:
            if attempt <= max_retries:
                time.sleep(min(2 ** attempt, 15))
                continue
            raise RuntimeError(f"network error: {e}")


def cli_model_to_id(choice: str) -> str:
    if choice == "v1":
        return MUSIC_MODEL_V1
    if choice == "v2":
        return MUSIC_MODEL_V2
    raise ValueError(f"unknown model choice: {choice!r}")


def _is_unknown_model_error(code: int, payload_txt: str) -> bool:
    if code not in (400, 422):
        return False
    low = payload_txt.lower()
    return any(tok in low for tok in ("model", "model_id", "unknown", "invalid", "not found", "unsupported"))


def _is_v2_unavailable_error(exc: BaseException) -> bool:
    err = str(exc).lower()
    if "music_v2" in err or "music v2" in err:
        return True
    if "feature_not_available" in err and ("music" in err or "v2" in err):
        return True
    if "limited_access" in err and "v2" in err:
        return True
    return False


def compose_plan(
    plan: dict,
    api_key: str,
    model_id: str = MUSIC_MODEL_DEFAULT,
    respect_durations: bool = True,
) -> tuple[bytes, dict]:
    return _post_music({
        "composition_plan": plan,
        "model_id": model_id,
        "respect_sections_durations": respect_durations,
    }, api_key)


def _http_error_code(exc: RuntimeError) -> int:
    err = str(exc)
    if not err.startswith("HTTP "):
        return 0
    try:
        return int(err.split(":", 1)[0].replace("HTTP ", "").strip())
    except ValueError:
        return 0


def _fallback_to_v1(reason: str, model_id: str) -> None:
    print(
        f"[gen] {reason}; retrying once with {MUSIC_MODEL_V1!r} ...",
        file=sys.stderr,
    )


def compose_plan_with_fallback(
    plan: dict,
    api_key: str,
    model_id: str,
    respect_durations: bool = True,
) -> tuple[bytes, dict, str]:
    """Compose audio; on v2 rejection/unavailability, retry once with music_v1."""
    try:
        audio, hdrs = compose_plan(plan, api_key, model_id=model_id, respect_durations=respect_durations)
        return audio, hdrs, model_id
    except GenerationHalted as ex:
        if model_id == MUSIC_MODEL_V1 or not _is_v2_unavailable_error(ex):
            raise
        _fallback_to_v1(f"music_v2 unavailable ({str(ex).split(':', 1)[0]})", model_id)
    except RuntimeError as ex:
        err = str(ex)
        if model_id == MUSIC_MODEL_V1:
            raise
        if _is_v2_unavailable_error(ex):
            _fallback_to_v1(f"music_v2 unavailable ({err.split(':', 1)[0]})", model_id)
        elif _is_unknown_model_error(_http_error_code(ex), err):
            _fallback_to_v1(f"model {model_id!r} rejected ({err.split(':', 1)[0]})", model_id)
        else:
            raise

    audio, hdrs = compose_plan(plan, api_key, model_id=MUSIC_MODEL_V1, respect_durations=respect_durations)
    return audio, hdrs, MUSIC_MODEL_V1


def write_atomic(path: Path, data: bytes) -> None:
    tmp = path.with_suffix(path.suffix + ".part")
    tmp.write_bytes(data)
    tmp.replace(path)


def backup_existing_primary(skip_backup: bool) -> Path | None:
    """Copy current primary MP3 into versions/ before overwrite."""
    if skip_backup or not OUT_FILE.exists():
        return None
    if OUT_FILE.stat().st_size <= 0:
        return None
    VERSIONS_DIR.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    dest = VERSIONS_DIR / f"kaoru_image_song_kenri_backup_{stamp}.mp3"
    shutil.copy2(OUT_FILE, dest)
    return dest


def mp3_probe(data: bytes) -> tuple[dict | None, int, float]:
    n = len(data)
    i = 0
    if data[:3] == b"ID3" and n >= 10:
        size = ((data[6] & 0x7F) << 21) | ((data[7] & 0x7F) << 14) | ((data[8] & 0x7F) << 7) | (data[9] & 0x7F)
        i = 10 + size
    v1 = [0, 32, 40, 48, 56, 64, 80, 96, 112, 128, 160, 192, 224, 256, 320, 0]
    v2 = [0, 8, 16, 24, 32, 40, 48, 56, 64, 80, 96, 112, 128, 144, 160, 0]
    srt = {3: [44100, 48000, 32000, 0], 2: [22050, 24000, 16000, 0], 0: [11025, 12000, 8000, 0]}
    vname = {3: "MPEG1", 2: "MPEG2", 0: "MPEG2.5"}
    ch = ["stereo", "joint_stereo", "dual", "mono"]
    total = 0.0
    frames = 0
    first = None
    while i + 4 <= n:
        if data[i] != 0xFF or (data[i + 1] & 0xE0) != 0xE0:
            i += 1
            continue
        b1, b2, b3 = data[i + 1], data[i + 2], data[i + 3]
        ver = (b1 >> 3) & 3
        layer = (b1 >> 1) & 3
        bi = (b2 >> 4) & 0xF
        sri = (b2 >> 2) & 3
        pad = (b2 >> 1) & 1
        cm = (b3 >> 6) & 3
        if ver == 1 or layer != 1 or bi in (0, 15) or sri == 3:
            i += 1
            continue
        br = (v1[bi] if ver == 3 else v2[bi]) * 1000
        samples = 1152 if ver == 3 else 576
        sr = srt[ver][sri]
        if br == 0 or sr == 0:
            i += 1
            continue
        flen = (samples // 8 * br) // sr + pad
        if flen <= 0:
            i += 1
            continue
        if first is None:
            first = {"version": vname.get(ver), "bitrate_kbps": br // 1000, "samplerate": sr,
                     "channel_mode": ch[cm]}
        total += samples / sr
        frames += 1
        i += flen
    return first, frames, total


def main() -> int:
    ap = argparse.ArgumentParser(description="Generate Kaoru image song Kenri no Chō.")
    ap.add_argument("--regen", "--force", dest="regen", action="store_true",
                    help="Overwrite existing output.")
    ap.add_argument("--dry-run", action="store_true", help="Print plan JSON; no API call.")
    ap.add_argument(
        "--model",
        choices=("v1", "v2"),
        default="v2",
        help="Eleven Music model: v2 (music_v2, default) or v1 (music_v1). v2 falls back to v1 on unknown-model errors.",
    )
    ap.add_argument(
        "--no-backup",
        action="store_true",
        help="Skip timestamped backup in game/audio/bgm/versions/ before overwriting primary.",
    )
    args = ap.parse_args()

    model_id = cli_model_to_id(args.model)
    plan = COMPOSITION_PLAN
    total_ms = sum(s["duration_ms"] for s in plan["sections"])
    print("=== Kaoru image song: Kenri no Cho ===")
    print(f"  output   : {OUT_FILE}")
    print(f"  model    : {model_id} (--model {args.model})")
    print(f"  sections : {len(plan['sections'])}, planned ~{total_ms/1000:.0f}s")
    for s in plan["sections"]:
        print(f"    - {s['section_name']:<20} {s['duration_ms']/1000:>5.1f}s  ({len(s['lines'])} lines)")

    if args.dry_run:
        print(json.dumps(plan, ensure_ascii=False, indent=2))
        return 0

    api_key = get_api_key()
    if OUT_FILE.exists() and OUT_FILE.stat().st_size > 0 and not args.regen:
        info, _, dur = mp3_probe(OUT_FILE.read_bytes())
        print(f"\nExists ({OUT_FILE.stat().st_size} bytes, ~{dur:.1f}s). Use --regen to replace.")
        return 0

    BGM_DIR.mkdir(parents=True, exist_ok=True)
    print(f"\n[gen] composing (single POST, model={model_id}) ...")
    t0 = time.time()
    model_used = model_id
    v2_worked = model_id == MUSIC_MODEL_V2
    try:
        audio, hdrs, model_used = compose_plan_with_fallback(
            plan, api_key, model_id=model_id, respect_durations=True,
        )
        v2_worked = args.model == "v2" and model_used == MUSIC_MODEL_V2
    except GenerationHalted as ge:
        print(f"[gen] HALTED: {ge}", file=sys.stderr)
        return 3
    except Exception as ex:  # noqa: BLE001
        print(f"[gen] FAILED: {ex}", file=sys.stderr)
        if args.model == "v2":
            print("[gen] music_v2 did not produce output; see error above.", file=sys.stderr)
        return 1
    if not audio:
        print("[gen] FAILED: empty audio", file=sys.stderr)
        return 1

    if args.regen or not OUT_FILE.exists() or OUT_FILE.stat().st_size == 0:
        backed = backup_existing_primary(args.no_backup)
        if backed:
            print(f"[backup] {OUT_FILE.name} -> {backed.relative_to(ROOT)}")
        elif OUT_FILE.exists() and OUT_FILE.stat().st_size > 0 and args.no_backup:
            print("[backup] skipped (--no-backup)")

    write_atomic(OUT_FILE, audio)
    song_id = hdrs.get("song-id") or hdrs.get("Song-Id")
    info, frames, dur = mp3_probe(audio)
    print(f"[gen] OK: {len(audio)} bytes in {time.time()-t0:.0f}s -> {OUT_FILE}")
    print(f"[verify] model_used={model_used}  v2_ok={v2_worked}")
    print(f"[verify] {info}  frames={frames}  duration={dur:.2f}s ({int(dur//60)}:{dur%60:05.2f})")
    print(f"[verify] song-id={song_id}")
    if model_used != model_id:
        print(f"[verify] requested {model_id}; API accepted {model_used} for final file.")
    print(
        "\n[note] If montage sync drifts, re-run faster-whisper on this MP3 and "
        "update timings in game/kaoru_image_song.rpy."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
