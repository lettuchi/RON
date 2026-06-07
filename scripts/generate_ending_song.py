#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Generate the ENDING / credits SONG for Ryoko Owari Nights via Eleven Music.

Track: 嘘つきの糸  (Usotsuki no Ito / "The Liar's String") — Kaoru's POV.
The dark counterpart to the opening song 「嘘の街の赤い糸」 (Toa's POV).

A sung VOCAL track (Japanese lyrics), NOT instrumental. The exact, locked &
approved lyrics live in docs/ending-song-lyrics.md and are reproduced verbatim
below in a `composition_plan` so the model sings THOSE words, in order:

    Intro -> Verse 1 -> Pre-Chorus -> Chorus -> Verse 2 -> Chorus -> Bridge
          -> Final Chorus

Two configs:
  v1 (default)  the original take. Deep/velvety baritone, respect_durations=False.
  v2 (--v2)     the A/B retake the user requested:
                  * register: a WARM LOW BARITONE — lower than a tenor, but NOT a
                    deep bass; rich, controlled, velvety, noir.
                  * Japanese held tight the whole way: respect_sections_durations
                    = True, per-section durations right-sized to each section's
                    mora count (so no section runs long and forces the model to
                    vamp / ad-lib filler — the suspected cause of back-half drift),
                    and explicit positive/negative style strings that pin the
                    vocal to the written Japanese (no English, no ad-libs/scat).
                  * everything else (slow noir piano ballad with pulse/energy,
                    mood, structure) stays the same.
                  * writes ending_song_v2.mp3 (NEVER overwrites v1's ending_song.mp3).

------------------------------------------------------------------------------
Eleven Music API (confirmed working pattern, mirrors scripts/generate_music.py):
    POST https://api.elevenlabs.io/v1/music?output_format=mp3_44100_128
    Header: xi-api-key: <key>
    JSON body for a sung track:
        {
          "composition_plan": { positive/negative_global_styles, sections[...] },
          "model_id": "music_v1",
          "respect_sections_durations": <bool>
        }
    Each section: section_name (1-100 chars), positive_local_styles (<=50),
    negative_local_styles (<=50), duration_ms (3000-120000), lines (<=30, <=200
    chars each). `force_instrumental` is intentionally OMITTED (it is only valid
    with a plain `prompt`, and we WANT vocals — vocals come from the `lines`).
    Response: raw audio bytes (mp3).

Eleven Music requires a PAID subscription.

NOTE: This script deliberately makes NO call to GET /v1/user/subscription
(that endpoint 401s/hangs on the current key). The only network call is the
single POST /v1/music generation. It also does not run Ren'Py lint.

API KEY: read ONLY from the real environment variable ELEVENLABS_API_KEY
(never scripts/.env, never hardcoded). In PowerShell:
    $env:ELEVENLABS_API_KEY = "sk_..."

Usage (run from the project root):
    python scripts/generate_ending_song.py --dry-run        # print v1 plan as JSON, no API call
    python scripts/generate_ending_song.py --v2 --dry-run   # print v2 plan as JSON, no API call
    python scripts/generate_ending_song.py --v2             # generate ending_song_v2.mp3 (the retake)
    python scripts/generate_ending_song.py                  # generate the original ending_song.mp3
    python scripts/generate_ending_song.py --v2 --regen      # overwrite an existing ending_song_v2.mp3
    python scripts/generate_ending_song.py --v2 --out game/audio/bgm/ending_song_v3.mp3
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import time
from pathlib import Path
from urllib import error, request

ROOT = Path(__file__).resolve().parents[1]
BGM_DIR = ROOT / "game" / "audio" / "bgm"
OUT_FILE = BGM_DIR / "ending_song.mp3"        # v1 (the take the user liked — never overwrite)
OUT_FILE_V2 = BGM_DIR / "ending_song_v2.mp3"  # v2 retake

API_BASE = "https://api.elevenlabs.io"
MUSIC_MODEL = "music_v1"
OUTPUT_FORMAT = "mp3_44100_128"  # codec_samplerate_bitrate; Ren'Py-supported mp3

# ---------------------------------------------------------------------------
# Locked & approved lyrics (verbatim from docs/ending-song-lyrics.md).
# The JAPANESE is authoritative — we sing the Japanese, never the romaji.
# Shared by v1 and v2. The Chorus appears twice; defined once to avoid drift.
# ---------------------------------------------------------------------------
INTRO_LINES = [
    "墨より暗い この街で",
    "お前だけが 朱に光る",
]
VERSE1_LINES = [
    "嘘で築いた 俺の城に",
    "土足で入った 馬鹿な女",
    "仮面を剥がす その指を",
    "まだ 許した覚えはない",
]
PRECHORUS_LINES = [
    "それなのに なぜ 手が伸びる",
    "朱肉のように 染まってゆく",
]
CHORUS_LINES = [
    "赤い糸で お前を縛る",
    "結び目をひとつ また ひとつ",
    "返し方など 知らないが",
    "この糸だけは 解かせない",
    "俺の印を お前に捺す",
]
VERSE2_LINES = [
    "逃げてみろ 追いかけてやる",
    "鳥籠の戸は 開けたまま",
    "それでも戻る お前の馬鹿さを",
    "俺は きっと 愛と呼ぶ",
]
BRIDGE_LINES = [
    "墨が乾けば 嘘も真",
    "判を捺すたび 手が震えた",
    "お前の名を 書いた夜",
    "消せないように 何度も なぞる",
]
FINAL_CHORUS_LINES = [
    "赤い糸は 切らせはしない",
    "お前が 知らなくても いい",
    "言葉にすれば 嘘になる",
    "だから 何も言わずに",
    "お前の眠りに 口づけて",
    "糸を もう一度 結ぶ",
]

# ===========================================================================
# v1 (original) — kept for reproducibility / A-B. Deep velvety baritone,
# respect_sections_durations=False.
# ===========================================================================
_GLOBAL_POSITIVE_V1 = [
    "slow noir piano ballad with a subtle rhythmic pulse and forward motion",
    "smoky cinematic jazz-noir: intimate grand piano, low strings (cello, contrabass)",
    "warm upright bass and tasteful brushed drums / soft heartbeat pulse",
    "MALE lead vocal singing in Japanese",
    "deep, low, velvety baritone; a storyteller's voice with gravitas and weight",
    "emotive, intimate and restrained, with a thread of controlled menace",
    "dark-romantic, cinematic, film-noir torch song",
    "tasteful dynamic build that swells into the choruses, never a static dirge",
    "clear, expressive lead vocal mixed forward",
]
_GLOBAL_NEGATIVE_V1 = [
    "female vocals",
    "high-pitched, light, or idol voice",
    "childish anime ani-goe timbre",
    "bright cheerful J-pop, upbeat dance-pop",
    "fast tempo, EDM, four-on-the-floor, techno",
    "lifeless static dirge with no rhythm or pulse",
    "rap or spoken word",
    "screaming, harsh or metal vocals",
    "heavy autotune, robotic or vocoder vocals",
    "instrumental only / no vocals",
    "lo-fi, muffled, distorted",
]
SECTIONS_V1 = [
    {"section_name": "Intro",
     "positive_local_styles": ["sparse atmospheric intro", "lone smoky grand piano, soft contrabass",
                               "low velvety male vocal entrance, intimate and close-mic'd", "slow, brooding, cinematic"],
     "negative_local_styles": ["full drums", "loud", "bright", "up-tempo"],
     "duration_ms": 16000, "lines": INTRO_LINES},
    {"section_name": "Verse 1",
     "positive_local_styles": ["intimate restrained verse", "brushed drums and walking upright bass enter softly",
                               "deep velvety baritone storytelling", "smoky, controlled, noir"],
     "negative_local_styles": ["loud belting", "over-busy", "bright pop"],
     "duration_ms": 26000, "lines": VERSE1_LINES},
    {"section_name": "Pre-Chorus",
     "positive_local_styles": ["rising pre-chorus, growing tension", "strings swell, pulse tightens",
                               "crescendo and lift toward the chorus"],
     "negative_local_styles": ["flat dynamics", "static"],
     "duration_ms": 14000, "lines": PRECHORUS_LINES},
    {"section_name": "Chorus",
     "positive_local_styles": ["fuller, dramatic noir-ballad chorus", "lush low strings and rich piano",
                               "powerful yet velvety baritone, dark-romantic emotional hook", "soft driving pulse, cinematic swell"],
     "negative_local_styles": ["thin", "frantic", "idol vocal", "harsh"],
     "duration_ms": 27000, "lines": CHORUS_LINES},
    {"section_name": "Verse 2",
     "positive_local_styles": ["verse, slightly fuller than verse one", "steady noir groove, brushed drums",
                               "intimate deep baritone with restrained menace"],
     "negative_local_styles": ["over-busy", "loud belting", "bright pop"],
     "duration_ms": 26000, "lines": VERSE2_LINES},
    {"section_name": "Chorus (repeat)",
     "positive_local_styles": ["fuller, dramatic noir-ballad chorus", "lush low strings and rich piano",
                               "powerful yet velvety baritone, dark-romantic emotional hook", "soft driving pulse, cinematic swell"],
     "negative_local_styles": ["thin", "frantic", "idol vocal", "harsh"],
     "duration_ms": 27000, "lines": CHORUS_LINES},
    {"section_name": "Bridge",
     "positive_local_styles": ["emotional bridge, intimate breakdown then build", "vulnerable, trembling baritone",
                               "piano and aching strings forward"],
     "negative_local_styles": ["same as chorus", "monotone", "loud"],
     "duration_ms": 23000, "lines": BRIDGE_LINES},
    {"section_name": "Final Chorus",
     "positive_local_styles": ["climactic final chorus, the biggest and most cinematic",
                               "full but tasteful noir arrangement, soaring yet controlled baritone",
                               "dark-romantic catharsis", "resolves to a tender, intimate close"],
     "negative_local_styles": ["abrupt cut mid-word", "fade to silence mid-phrase"],
     "duration_ms": 31000, "lines": FINAL_CHORUS_LINES},
]
COMPOSITION_PLAN_V1 = {
    "positive_global_styles": _GLOBAL_POSITIVE_V1,
    "negative_global_styles": _GLOBAL_NEGATIVE_V1,
    "sections": SECTIONS_V1,
}

# ===========================================================================
# v2 (retake) — two targeted changes vs v1:
#   (1) register lowered to a WARM LOW BARITONE (lower than tenor, not deep bass)
#   (2) Japanese pinned the whole way through (respect_sections_durations=True,
#       mora-right-sized durations, explicit "stay in Japanese / no ad-libs" styles)
# Everything else (arrangement, mood, structure) is unchanged from v1.
#
# Per-section durations are budgeted to each section's MORA count so the model
# has enough time to sing every written line at a slow, sustained pace WITHOUT a
# long empty tail that invites improvisation. (mora counts are approximate.)
#   Intro ~23, Verse1 ~51, Pre ~25, Chorus ~64, Verse2 ~50, Bridge ~51, Final ~71
# Total ~190s (matches the take the user liked), within the requested 180-200s.
# ===========================================================================
_GLOBAL_POSITIVE_V2 = [
    "slow noir piano ballad with a subtle rhythmic pulse and forward motion",
    "smoky cinematic jazz-noir: intimate grand piano, low strings (cello, contrabass)",
    "warm upright bass and tasteful brushed drums / soft heartbeat pulse",
    "male lead vocal, warm low baritone — lower than a tenor but not a deep bass; rich, controlled, velvety, noir",
    "sung entirely in Japanese, clear native Japanese diction, follows the written lyrics exactly",
    "emotive, intimate and restrained, with a thread of controlled menace",
    "dark-romantic, cinematic, film-noir torch song",
    "tasteful dynamic build that swells into the choruses, never a static dirge",
    "clear, expressive lead vocal mixed forward",
]
_GLOBAL_NEGATIVE_V2 = [
    "English lyrics",
    "improvised vocals, ad-libs, scat, vocalizations or syllables not in the written lyrics",
    "gibberish, made-up language",
    "falsetto, high tenor",
    "deep bass, basso profondo",
    "female vocals",
    "high-pitched, light, or idol voice",
    "childish anime ani-goe timbre",
    "bright cheerful J-pop, upbeat dance-pop, EDM, four-on-the-floor, techno",
    "instrumental only / no vocals",
    "screaming, harsh or metal vocals; heavy autotune, robotic or vocoder vocals",
    "lo-fi, muffled, distorted",
]

# Anti-drift negatives reused on the back-half sections most prone to improvising.
_NO_ADLIB = [
    "wordless humming, oohs and aahs in place of the lyrics",
    "ad-libbed runs or improvised vocals",
    "English words", "scat singing", "made-up syllables",
    "instrumental vamping with no vocal",
    "repeating, skipping or reordering the written lines",
]

SECTIONS_V2 = [
    {"section_name": "Intro",
     "positive_local_styles": ["sparse atmospheric intro: lone smoky grand piano and soft contrabass",
                               "brief instrumental opening, then the written Japanese lines sung",
                               "warm low baritone entrance, intimate and close-mic'd", "slow, brooding, cinematic"],
     "negative_local_styles": ["full drums", "loud", "bright", "up-tempo",
                               "wordless oohs and aahs in place of the lyrics", "high tenor", "falsetto"],
     "duration_ms": 16000, "lines": INTRO_LINES},
    {"section_name": "Verse 1",
     "positive_local_styles": ["intimate restrained verse", "brushed drums and walking upright bass enter softly",
                               "warm low baritone storytelling, every written line clear", "smoky, controlled, noir"],
     "negative_local_styles": ["loud belting", "over-busy", "bright pop", "high tenor", "falsetto"],
     "duration_ms": 24000, "lines": VERSE1_LINES},
    {"section_name": "Pre-Chorus",
     "positive_local_styles": ["rising pre-chorus, growing tension", "strings swell, pulse tightens",
                               "crescendo and lift toward the chorus, baritone stays low and warm"],
     "negative_local_styles": ["flat dynamics", "static", "falsetto", "high tenor"],
     "duration_ms": 14000, "lines": PRECHORUS_LINES},
    {"section_name": "Chorus",
     "positive_local_styles": ["fuller, dramatic noir-ballad chorus", "lush low strings and rich piano, soft driving pulse",
                               "powerful yet velvety low baritone, dark-romantic emotional hook", "cinematic swell"],
     "negative_local_styles": ["thin", "frantic", "idol vocal", "harsh", "high tenor", "falsetto"],
     "duration_ms": 29000, "lines": CHORUS_LINES},
    {"section_name": "Verse 2",
     "positive_local_styles": ["verse, slightly fuller than verse one", "steady noir groove, brushed drums",
                               "intimate warm low baritone with restrained menace, every written line clear"],
     "negative_local_styles": ["over-busy", "loud belting", "bright pop", "high tenor", "falsetto"],
     "duration_ms": 23000, "lines": VERSE2_LINES},
    {"section_name": "Chorus (repeat)",
     "positive_local_styles": ["fuller, dramatic noir-ballad chorus", "lush low strings and rich piano, soft driving pulse",
                               "powerful yet velvety low baritone, dark-romantic emotional hook", "cinematic swell"],
     "negative_local_styles": ["thin", "frantic", "idol vocal", "harsh", "high tenor", "falsetto"],
     "duration_ms": 29000, "lines": CHORUS_LINES},
    {"section_name": "Bridge",
     "positive_local_styles": ["emotional bridge, intimate breakdown then build",
                               "vulnerable, trembling low baritone — still warm and controlled",
                               "piano and aching strings forward",
                               "sing every written Japanese line clearly and in order"],
     "negative_local_styles": ["same as chorus", "monotone", "loud", "high tenor", "falsetto"] + _NO_ADLIB,
     "duration_ms": 24000, "lines": BRIDGE_LINES},
    {"section_name": "Final Chorus",
     "positive_local_styles": ["climactic final chorus, the biggest and most cinematic",
                               "full but tasteful noir arrangement, soaring yet controlled low baritone",
                               "dark-romantic catharsis",
                               "sing every written Japanese line clearly and in order, then resolve to a tender, intimate close"],
     "negative_local_styles": ["abrupt cut mid-word", "high tenor", "falsetto"] + _NO_ADLIB,
     "duration_ms": 31000, "lines": FINAL_CHORUS_LINES},
]
COMPOSITION_PLAN_V2 = {
    "positive_global_styles": _GLOBAL_POSITIVE_V2,
    "negative_global_styles": _GLOBAL_NEGATIVE_V2,
    "sections": SECTIONS_V2,
}


class GenerationHalted(Exception):
    """Plan / permission / quota / rate-limit conditions needing user action."""


def get_api_key() -> str:
    """Read the key ONLY from the real environment (never scripts/.env)."""
    key = os.environ.get("ELEVENLABS_API_KEY", "").strip()
    if not key:
        print("ERROR: ELEVENLABS_API_KEY is not set in the environment.\n"
              "       In PowerShell: $env:ELEVENLABS_API_KEY = \"sk_...\"",
              file=sys.stderr)
        raise SystemExit(2)
    return key


def _post_music(payload: dict, api_key: str, max_retries: int = 4) -> tuple[bytes, dict]:
    """POST /v1/music with a ready-made JSON payload. Returns (audio, headers).

    This is the ONLY network call the script makes (no subscription lookup)."""
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


def compose_plan(plan: dict, api_key: str, respect_durations: bool) -> tuple[bytes, dict]:
    """Composition-plan (explicit lyrics) generation — vocals on."""
    return _post_music({
        "composition_plan": plan,
        "model_id": MUSIC_MODEL,
        "respect_sections_durations": respect_durations,
    }, api_key)


def write_atomic(path: Path, data: bytes) -> None:
    tmp = path.with_suffix(path.suffix + ".part")
    tmp.write_bytes(data)
    tmp.replace(path)


def mp3_probe(data: bytes) -> tuple[dict | None, int, float]:
    """Pure-Python MP3 header/duration check (no ffprobe/mutagen, no network).

    Walks frame headers; returns (first_frame_info, frame_count, duration_s)."""
    n = len(data)
    i = 0
    if data[:3] == b"ID3" and n >= 10:
        size = ((data[6] & 0x7F) << 21) | ((data[7] & 0x7F) << 14) \
            | ((data[8] & 0x7F) << 7) | (data[9] & 0x7F)
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
            first = {"version": vname.get(ver), "layer": "III", "bitrate_kbps": br // 1000,
                     "samplerate": sr, "channel_mode": ch[cm]}
        total += samples / sr
        frames += 1
        i += flen
    return first, frames, total


def _print_plan_summary(label: str, plan: dict, respect: bool, out: Path) -> None:
    sections = plan["sections"]
    total_ms = sum(s["duration_ms"] for s in sections)
    n_lines = sum(len(s["lines"]) for s in sections)
    print(f"=== Ending song [{label}]: 嘘つきの糸 (Usotsuki no Ito) — Kaoru's POV ===")
    print(f"  endpoint : POST {API_BASE}/v1/music?output_format={OUTPUT_FORMAT}")
    print(f"  model    : {MUSIC_MODEL}  (vocals ON; force_instrumental omitted)")
    print(f"  sections : {len(sections)} ({n_lines} lyric lines), "
          f"planned total ~{total_ms/1000:.0f}s, respect_sections_durations={respect}")
    print(f"  output   : {out}")
    for s in sections:
        print(f"    - {s['section_name']:<16} {s['duration_ms']/1000:>5.1f}s  ({len(s['lines'])} line(s))")


def main() -> int:
    ap = argparse.ArgumentParser(
        description="Generate the sung Japanese ENDING song (嘘つきの糸) for Ryoko Owari Nights.")
    ap.add_argument("--v2", action="store_true",
                    help="Use the v2 retake config (warm low baritone, respect_durations=True, "
                         "right-sized durations) and write ending_song_v2.mp3.")
    ap.add_argument("--out", default=None, help="Override the output path.")
    ap.add_argument("--regen", "--force", dest="regen", action="store_true",
                    help="Overwrite the output file if it already exists.")
    ap.add_argument("--respect-durations", dest="respect", action="store_true", default=None,
                    help="Force respect_sections_durations=True (default: True for --v2, False for v1).")
    ap.add_argument("--no-respect-durations", dest="respect", action="store_false",
                    help="Force respect_sections_durations=False.")
    ap.add_argument("--dry-run", action="store_true",
                    help="Print the selected composition_plan as JSON and exit (no API call).")
    args = ap.parse_args()

    if args.v2:
        plan, default_out, label = COMPOSITION_PLAN_V2, OUT_FILE_V2, "v2"
        respect = True if args.respect is None else args.respect
    else:
        plan, default_out, label = COMPOSITION_PLAN_V1, OUT_FILE, "v1"
        respect = False if args.respect is None else args.respect

    out = Path(args.out) if args.out else default_out

    # Safety: never let a v2 run clobber the v1 file the user wants to keep for A/B.
    if args.v2 and out.resolve() == OUT_FILE.resolve():
        print(f"ERROR: refusing to write v2 output over the v1 file ({OUT_FILE.name}).",
              file=sys.stderr)
        return 2

    _print_plan_summary(label, plan, respect, out)

    if args.dry_run:
        print("\n--- composition_plan (dry run, no API call) ---")
        print(json.dumps(plan, ensure_ascii=False, indent=2))
        return 0

    api_key = get_api_key()

    if out.exists() and out.stat().st_size > 0 and not args.regen:
        print(f"\nREFUSING to overwrite existing {out.name} "
              f"({out.stat().st_size} bytes). Use --regen to regenerate.", file=sys.stderr)
        return 0

    BGM_DIR.mkdir(parents=True, exist_ok=True)
    print("\n[gen] composing sung Japanese ending song (single POST, no subscription lookup) ...")
    t0 = time.time()
    try:
        audio, hdrs = compose_plan(plan, api_key, respect_durations=respect)
    except GenerationHalted as ge:
        print(f"\n[gen] HALTED — access/plan/quota issue:\n  {ge}", file=sys.stderr)
        return 3
    except Exception as ex:  # noqa: BLE001
        print(f"\n[gen] FAILED: {ex}", file=sys.stderr)
        return 1
    if not audio:
        print("[gen] FAILED: empty audio", file=sys.stderr)
        return 1

    write_atomic(out, audio)
    song_id = hdrs.get("song-id") or hdrs.get("Song-Id")
    print(f"[gen] OK: wrote {len(audio)} bytes in {time.time()-t0:.0f}s -> {out}  (song-id={song_id})")

    info, frames, dur = mp3_probe(audio)
    print(f"[verify] valid MP3: {info}")
    print(f"[verify] frames={frames}  duration={dur:.2f}s  ({int(dur//60)}:{dur%60:05.2f})")
    print(f"[verify] size={len(audio)} bytes  byte-rate-est={len(audio)*8/128000:.1f}s")
    cost = {k: v for k, v in hdrs.items()
            if any(t in k.lower() for t in ("cost", "credit", "char"))}
    if cost:
        print(f"[gen] cost-related headers: {cost}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
