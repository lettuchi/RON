#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Generate Toa + Kaoru duet 「嘘の夜を走れ」 via Eleven Music.

High-energy anime duet — all sung, no spoken word. Female soprano + male baritone
with harmonized choruses. J-pop / anime OP polish (~135–142 BPM). Locked lyrics:
docs/duet-song-lyrics.md.

Writes: game/audio/bgm/duet_song.mp3

Backup: game/audio/bgm/versions/duet_song_backup_YYYYMMDD_HHMMSS.mp3 unless --no-backup.

Usage (project root):
    python scripts/generate_duet_song.py --dry-run
    python scripts/generate_duet_song.py --regen
    python scripts/generate_duet_song.py --regen --model v2
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
OUT_FILE = BGM_DIR / "duet_song.mp3"
SCRIPTS_DIR = ROOT / "scripts"
ENV_FILE = SCRIPTS_DIR / ".env"

API_BASE = "https://api.elevenlabs.io"
MUSIC_MODEL_V1 = "music_v1"
MUSIC_MODEL_V2 = "music_v2"
MUSIC_MODEL_DEFAULT = MUSIC_MODEL_V2
OUTPUT_FORMAT = "mp3_44100_128"

INTRO_LINES = [
    "雨音が　鼓膜を叩く",
    "嘘の街で　二人　走り出す",
]
TOA_VERSE1 = [
    "黒い袖　風に鳴る",
    "白い鶴は　夜を刺す",
    "冷たさを　知ってるのに",
    "この視線は　まだ熱い",
]
KAORU_VERSE1 = [
    "笑う夜　雨の先",
    "距離こそが　甘い毒",
    "返さない　逃がさない",
    "それが　二人の　ルール",
]
PRECHORUS = [
    "止まれない　この鼓動",
    "まだ終わらない　この夜",
]
CHORUS = [
    "嘘の夜を走れ　二人で",
    "運河の灯　燃え上がれ",
    "掴めない　離さない",
    "波の上で　歌い合う",
    "残酷でも　朝は来る",
    "嘘の街で　本当の声",
    "嘘の夜を走れ",
]
TOA_VERSE2 = [
    "涙のあと　笑顔で行く",
    "影より先　手を伸ばす",
    "勝ちじゃない　隣の鼓動",
    "走っていたい",
]
KAORU_VERSE2 = [
    "夜は嘘を　並べる",
    "君の沈黙　拍になる",
    "甘い声も　刃にもなる",
    "君は　まだ　ここにいる",
]
BRIDGE_HARMONY = [
    "閉ざす扉　開かなくても",
    "二人の光　消えないから",
    "名を呼ばなくても　わかる",
    "まだ　ここにいる",
]
FINAL_CHORUS = [
    "嘘の夜を走れ　二人で",
    "嘘の朝に　希望の色",
    "閉ざす扉　開かなくても",
    "二人の灯は　消えない",
    "かきた　とあ",
    "橘　薫",
    "まだ　ここにいる",
]
OUTRO_LINES = [
    "夜は　残る",
    "二人で　走れ",
]

_GLOBAL_POSITIVE = [
    "high-energy anime duet OP song, Japanese female soprano and male baritone together",
    "J-pop anime opening polish, 135-142 BPM driving groove, NOT slow ballad",
    "lush harmonized chorus hooks, two-voice blend on every chorus line",
    "female sweet clear vocal and smooth male baritone, NOT raspy or metal scream",
    "forward momentum, drums bass strings synth brass anime sheen",
    "sung entirely in Japanese vocals only, NO spoken word, NO dialogue, NO recitative",
    "Hakuoki otome visual novel duet energy, Ryoko Owari canal night lanterns rain",
    "crisp diction, follows written lyrics exactly, tension and devotion not comedy",
]
_GLOBAL_NEGATIVE = [
    "spoken word, dialogue, musical theatre recitative, narrator speech",
    "slow piano ballad, 60-90 BPM dirge, torch song",
    "single voice only throughout, solo artist no duet",
    "raspy gravel scream, harsh metal, aggressive punk",
    "English lyrics, scat, improvised ad-libs, gibberish",
    "instrumental only no vocals",
    "comedy parody, lo-fi muddy mix, heavy autotune",
]

SECTIONS = [
    {
        "section_name": "Intro (sung)",
        "positive_local_styles": [
            "anime OP intro lift, drums and synth pulse entering",
            "duet sung lines female and male, building energy fast",
            "NO spoken dialogue",
        ],
        "negative_local_styles": ["spoken word", "slow ballad", "quiet piano only"],
        "duration_ms": 10000,
        "lines": INTRO_LINES,
    },
    {
        "section_name": "Verse 1 Toa (sung)",
        "positive_local_styles": [
            "female soprano verse, sweet powerful anime delivery",
            "steady driving 135-142 BPM, strings and drums forward",
        ],
        "negative_local_styles": ["male solo lead", "spoken", "ballad whisper"],
        "duration_ms": 18000,
        "lines": TOA_VERSE1,
    },
    {
        "section_name": "Verse 1 Kaoru (sung)",
        "positive_local_styles": [
            "male baritone verse, smooth controlled anime delivery not shout",
            "same driving tempo, clear lyric forward",
        ],
        "negative_local_styles": ["female solo", "spoken", "raspy metal"],
        "duration_ms": 18000,
        "lines": KAORU_VERSE1,
    },
    {
        "section_name": "Pre-chorus (sung)",
        "positive_local_styles": [
            "rising pre-chorus, both voices sung building to chorus",
            "tension lift, NO speech",
        ],
        "negative_local_styles": ["spoken dialogue", "flat dynamics"],
        "duration_ms": 11000,
        "lines": PRECHORUS,
    },
    {
        "section_name": "Chorus (harmony)",
        "positive_local_styles": [
            "big anime duet chorus, female and male harmonized throughout",
            "anthemic J-pop hook, full band strings drums synth",
            "beautiful close harmony every written line",
        ],
        "negative_local_styles": ["solo only", "spoken", "thin weak harmony", "slow ballad"],
        "duration_ms": 32000,
        "lines": CHORUS,
    },
    {
        "section_name": "Verse 2 Toa (sung)",
        "positive_local_styles": [
            "female verse slightly fuller, driving groove continues",
        ],
        "negative_local_styles": ["male solo", "spoken", "slow down"],
        "duration_ms": 18000,
        "lines": TOA_VERSE2,
    },
    {
        "section_name": "Verse 2 Kaoru (sung)",
        "positive_local_styles": [
            "male baritone verse, emotional controlled power",
        ],
        "negative_local_styles": ["female solo", "spoken"],
        "duration_ms": 18000,
        "lines": KAORU_VERSE2,
    },
    {
        "section_name": "Bridge (harmony)",
        "positive_local_styles": [
            "harmonized bridge, both voices intertwined",
            "brief lift before final chorus, sung only NO speech",
        ],
        "negative_local_styles": ["spoken bridge", "solo only", "ballad break"],
        "duration_ms": 16000,
        "lines": BRIDGE_HARMONY,
    },
    {
        "section_name": "Chorus repeat (harmony)",
        "positive_local_styles": [
            "full duet chorus harmonies repeat, same anime OP energy",
        ],
        "negative_local_styles": ["solo", "spoken", "quiet"],
        "duration_ms": 32000,
        "lines": CHORUS,
    },
    {
        "section_name": "Final chorus (harmony)",
        "positive_local_styles": [
            "climactic final chorus, biggest harmonies and arrangement",
            "female and male on name lines then together on final hook",
            "resolved high-energy anime ending",
        ],
        "negative_local_styles": ["abrupt cut", "solo only", "spoken outro"],
        "duration_ms": 34000,
        "lines": FINAL_CHORUS,
    },
    {
        "section_name": "Outro (sung)",
        "positive_local_styles": [
            "short sung duet tag outro, band fade",
            "NO spoken closing lines",
        ],
        "negative_local_styles": ["spoken dialogue", "new verse", "silence cut"],
        "duration_ms": 8000,
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
        print("ERROR: ELEVENLABS_API_KEY is not set.", file=sys.stderr)
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
    print(f"[gen] {reason}; retrying once with {MUSIC_MODEL_V1!r} ...", file=sys.stderr)


def compose_plan_with_fallback(
    plan: dict,
    api_key: str,
    model_id: str,
    respect_durations: bool = True,
) -> tuple[bytes, dict, str]:
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
    if skip_backup or not OUT_FILE.exists():
        return None
    if OUT_FILE.stat().st_size <= 0:
        return None
    VERSIONS_DIR.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    dest = VERSIONS_DIR / f"duet_song_backup_{stamp}.mp3"
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
    ap = argparse.ArgumentParser(description="Generate Toa/Kaoru anime duet Uso no Yoru o Hashire.")
    ap.add_argument("--regen", "--force", dest="regen", action="store_true")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--model", choices=("v1", "v2"), default="v2")
    ap.add_argument("--no-backup", action="store_true")
    args = ap.parse_args()

    model_id = cli_model_to_id(args.model)
    plan = COMPOSITION_PLAN
    total_ms = sum(s["duration_ms"] for s in plan["sections"])
    print("=== Duet: Uso no Yoru o Hashire (anime OP duet) ===")
    print(f"  output   : {OUT_FILE}")
    print(f"  model    : {model_id} (--model {args.model})")
    print(f"  sections : {len(plan['sections'])}, planned ~{total_ms/1000:.0f}s")
    for s in plan["sections"]:
        print(f"    - {s['section_name']:<28} {s['duration_ms']/1000:>5.1f}s  ({len(s['lines'])} lines)")

    if args.dry_run:
        print(json.dumps(plan, ensure_ascii=False, indent=2))
        return 0

    api_key = get_api_key()
    if OUT_FILE.exists() and OUT_FILE.stat().st_size > 0 and not args.regen:
        _, _, dur = mp3_probe(OUT_FILE.read_bytes())
        print(f"\nExists (~{dur:.1f}s). Use --regen to replace.")
        return 0

    BGM_DIR.mkdir(parents=True, exist_ok=True)
    print(f"\n[gen] composing (model={model_id}) ...")
    t0 = time.time()
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
        return 1
    if not audio:
        print("[gen] FAILED: empty audio", file=sys.stderr)
        return 1

    if args.regen or not OUT_FILE.exists() or OUT_FILE.stat().st_size == 0:
        backed = backup_existing_primary(args.no_backup)
        if backed:
            print(f"[backup] -> {backed.relative_to(ROOT)}")

    write_atomic(OUT_FILE, audio)
    song_id = hdrs.get("song-id") or hdrs.get("Song-Id")
    info, frames, dur = mp3_probe(audio)
    print(f"[gen] OK: {len(audio)} bytes in {time.time()-t0:.0f}s -> {OUT_FILE}")
    print(f"[verify] model_used={model_used}  v2_ok={v2_worked}")
    print(f"[verify] {info}  duration={dur:.2f}s ({int(dur//60)}:{dur%60:05.2f})  song-id={song_id}")
    print("\n[note] Update timings in game/duet_song.rpy if montage drifts.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
