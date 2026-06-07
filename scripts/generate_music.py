#!/usr/bin/env python3
"""Generate instrumental BGM tracks for Ryoko Owari Nights via the Eleven Music API.

Endpoint: POST https://api.elevenlabs.io/v1/music
  - JSON body: {"prompt": ..., "music_length_ms": ..., "model_id": "music_v1",
                "force_instrumental": true}
  - Query:     output_format=mp3_44100_128  (codec_samplerate_bitrate)
  - Header:    xi-api-key: <key>
  - Response:  raw audio bytes (application/octet-stream)

Eleven Music requires a PAID subscription. The key is read from the environment
(real env wins over the gitignored scripts/.env). Never hardcode keys.

Vocal tracks (e.g. the main-menu opening song) use a composition_plan so the
model sings exact, locked lyrics. force_instrumental is omitted there (it is only
valid with `prompt`); vocals come from the composition_plan `lines`.

Run from the project root:
    python scripts/generate_music.py --test          # one short (5s) probe, no track files
    python scripts/generate_music.py                   # generate all 3 instrumental themes
    python scripts/generate_music.py --ids toa,bad     # subset
    python scripts/generate_music.py --menu            # sung Japanese main-menu song only
    python scripts/generate_music.py --op              # higher-energy techno remix OP only
    python scripts/generate_music.py --force           # overwrite existing
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
SCRIPTS_DIR = ROOT / "scripts"
ENV_FILE = SCRIPTS_DIR / ".env"

API_BASE = "https://api.elevenlabs.io"
MUSIC_MODEL = "music_v1"
OUTPUT_FORMAT = "mp3_44100_128"  # safe on any paid tier; Ren'Py-supported mp3

# L5R / Hakuoki cinematic, Japanese instrumentation, instrumental only.
# Motifs echo docs/garageband-bgm-guide.md + the Toa/Kaoru GarageBand sessions.
TRACKS = {
    "toa": {
        "filename": "toa_theme_new.mp3",
        "length_ms": 90000,
        "prompt": (
            "Instrumental Japanese cinematic theme for a graceful former Crane-clan "
            "dancer in a feudal-Japan visual novel, Hakuoki / Legend of the Five Rings "
            "aesthetic. Bright, warm and elegant with a hopeful rising melody carrying a "
            "gentle bittersweet undercurrent. Lead koto and bamboo flute trade an "
            "ascending, dance-like phrase (rises then resolves), supported by light high "
            "strings, soft shamisen plucks, and delicate woodblock / hand percussion. "
            "Key of D major, tempo around 100 BPM, lively but never frantic, refined and "
            "graceful. No vocals, no lyrics, no drums kit, no synths. Seamless loop-"
            "friendly: steady feel throughout, no big fade-out, ending that flows back to "
            "the opening."
        ),
    },
    "kaoru": {
        "filename": "kaoru_theme_new.mp3",
        "length_ms": 90000,
        "prompt": (
            "Instrumental Japanese cinematic theme for a dangerous, refined Emerald "
            "Magistrate in a feudal-Japan visual novel, Hakuoki / Legend of the Five "
            "Rings aesthetic. Dark, controlled and seductive: coercive imperial power "
            "with slow-burning menace and restraint, tense but elegant, not horror. Low "
            "sustained cello and contrabass carry a slow descending minor phrase, with "
            "sparse, felt taiko hits and a lonely shakuhachi flute answering in call-and-"
            "response. Sparse biwa / koto single-note accents. Minor key (A minor), tempo "
            "around 78 BPM, deliberate and weighty. No vocals, no lyrics, no jump scares, "
            "no dissonant clusters, no battle drums. Seamless loop-friendly: steady, no "
            "big fade-out, ending that returns smoothly to the opening."
        ),
    },
    "bad": {
        "filename": "bad_ending.mp3",
        "length_ms": 95000,
        "prompt": (
            "Instrumental tragic, rain-soaked and lonely cinematic theme for the somber "
            "'game over' bad ending of a feudal-Japan visual novel set in a corrupt canal "
            "city, Hakuoki / Legend of the Five Rings aesthetic. Mournful and slow: a "
            "fragile solo piano melody over aching, sustained strings, as the dark city "
            "swallows the last of the light. Sparse, spacious and desolate, with distant "
            "soft shakuhachi and the faint feeling of falling rain. Deep minor key, very "
            "slow tempo around 60 BPM, grief and resignation, cinematic and intimate. No "
            "vocals, no lyrics, no percussion beat, no synths. Loop-friendly: gentle and "
            "continuous, no abrupt cut, ending that drifts back toward the opening."
        ),
    },
    "corridor": {
        "filename": "corridor.mp3",
        "length_ms": 75000,
        "prompt": (
            "Instrumental Japanese cinematic ambient bed for a feudal-Japan visual novel corridor scene. "
            "Endless magistrate-quarter hallway at night: distant paper lanterns, hushed nobility, ink and cedar in the air. "
            "Sparse koto harmonics and a soft breathy sho-like pad, occasional single woodblock or wind-chime color, very slow harmonic motion around 80 BPM or almost pulseless. "
            "Mysterious but not scary, quiet anticipation. "
            "No vocals, no lyrics, no modern drums, no synth EDM, no battle percussion. "
            "Seamless loop-friendly: steady texture, no big ending crash, last bar flows back to the first. "
            "Traditional Japanese aesthetics. "
        ),
    },
    "office": {
        "filename": "office.mp3",
        "length_ms": 80000,
        "prompt": (
            "Instrumental Japanese cinematic tension bed for an Emerald Magistrate's office in a corrupt canal city, "
            "Hakuoki / Legend of the Five Rings visual novel. Low string drone in a minor modal color, subtle felt "
            "taiko heartbeat far in the mix, sparse biwa or koto single-note accents like a seal waiting to fall. "
            "Mood: ink, cedar, stacked permits, lamplight on lacquer — authority and paperwork, not combat. Tempo "
            "around 75 BPM, restrained and elegant. No vocals, no lyrics, no busy melody, no horror clusters, no modern "
            "kit. Loop-friendly: continuous unease, gentle crossfade at loop point, no fade-to-silence ending."
        ),
    },
    "street": {
        "filename": "street.mp3",
        "length_ms": 85000,
        "prompt": (
            "Instrumental Japanese cinematic street theme for a canal city at night. "
            "Warm shamisen or biwa riff over light hand percussion and soft taiko on beats 1 and 3, distant lantern ambience. "
            "Tempo around 88 to 92 BPM, walking pace, worldly and slightly tense but not battle. "
            "Textures suggesting fish, copper, and rain on stone in the mix, not literal sound effects. "
            "No vocals, no lyrics, no EDM four-on-the-floor, no heroic fanfare. "
            "Loop-friendly: repeating 8-bar street motif, steady energy, ending connects to opening motif. "
        ),
    },
    "canon_intimate": {
        "filename": "canon_intimate.mp3",
        "length_ms": 75000,
        "prompt": (
            "Instrumental Japanese cinematic romantic aftermath bed inspired by feudal Japan visual novels. "
            "Warm, tender, gentle closeness without explicit sensuality: slow koto melody and soft string pads in D major or gentle modal major, 70 to 72 BPM, breathing room like paper screens and shared tea. "
            "Bittersweet undercurrent, two people choosing trust despite doubt. "
            "No vocals, no lyrics, no heavy percussion, no modern pop ballad cliches. "
            "Loop-friendly: soft continuous arc, loop point on a sustained chord, no dramatic stop. "
        ),
    },
    "case1_barge": {
        "filename": "case1_barge.mp3",
        "length_ms": 80000,
        "prompt": (
            "Instrumental Japanese cinematic noir investigation theme for a smuggler's canal and river barge at night, "
            "Legend of the Five Rings Ryoko Owari corrupt trade city. Low pulsing strings, muted shamisen ostinato, "
            "occasional wooden boat creak texture very subtle in the mix, rain-ready harmonic minor color. Mood: manifest "
            "lines, Scorpion paint, witness pride before the water — suspense not combat. 82 BPM, loop-friendly, no "
            "vocals, no lyrics, no modern synth bass, no battle taiko rolls. Seamless loop for visual novel investigation "
            "dialogue."
        ),
    },
    "case2_festival": {
        "filename": "case2_festival.mp3",
        "length_ms": 85000,
        "prompt": (
            "Instrumental Japanese festival night theme inspired by a feudal canal-city matsuri. "
            "Lively but refined taiko festival rhythms softened for dialogue, shamisen and fue motifs, warm paper-lantern harmonies. "
            "95 BPM feel without overwhelming voice acting, subtle tension suggesting hidden intrigue. "
            "No vocals, no lyrics, no EDM drops, no arcade chiptune. "
            "Loop-friendly with a repeating festival hook every 8 bars and steady energy. "
        ),
    },
    "case3_fabric": {
        "filename": "case3_fabric.mp3",
        "length_ms": 80000,
        "prompt": (
            "Instrumental Japanese cinematic suspense for a cramped fabric shop and bolt room in a corrupt city, Hakuoki / "
            "L5R visual novel. Close-in texture: plucked koto in tight repeating pattern, low cello pedal, rare sharp biwa "
            "accents like scissors — claustrophobic, witness-in-danger, not slasher horror. 78 BPM, minor key, loop-friendly "
            "for long dialogue under threat. No vocals, no lyrics, no screaming strings, no modern thriller pulses."
        ),
    },
    "case3_5_date": {
        "filename": "case3_5_date.mp3",
        "length_ms": 75000,
        "prompt": (
            "Instrumental Japanese cinematic date-night bed for a private inn with hidden biwa music through shoji, feudal Japan otome atmosphere. "
            "Intimate and slightly nervous: soft koto, distant biwa phrase like music through a wall, warm shakuhachi echo, gentle hand percussion like tea service, 68 to 74 BPM. "
            "Romance with stakes, quiet evening not public festival. "
            "No vocals, no lyrics, no club beats, no comedic slapstick. "
            "Loop-friendly, tender continuous mood. "
        ),
    },
    "case4_dock": {
        "filename": "case4_dock.mp3",
        "length_ms": 70000,
        "prompt": (
            "Instrumental Japanese cinematic action-tension bed for a rainy lower dock and imminent duel tension. "
            "Driving shamisen and low taiko in restrained pulses for dialogue and choice menus, not a full anime battle track. "
            "Harmonic minor scale, 100 to 108 BPM feel, rain-heavy atmosphere in the mix. "
            "No vocals, no lyrics, no Hollywood trailer horns, no EDM. "
            "Loop-friendly for investigation. "
        ),
    },
    "case4_5_kobune": {
        "filename": "case4_5_kobune.mp3",
        "length_ms": 75000,
        "prompt": (
            "Instrumental Japanese cinematic bed for a small kobune fishing boat at night on a canal, feudal-Japan otome "
            "visual novel. Gentle hull-rocking pulse in low strings, water-like koto harmonics, intimate warmth mixed with "
            "danger — two people alone on water, magistrate and witness. 72 BPM, minor-to-modal color shift, not horror. "
            "No vocals, no lyrics, no heavy battle taiko, no modern boat engine SFX dominating. Loop-friendly for long boat "
            "scenes."
        ),
    },
    "bad_end_rain": {
        "filename": "bad_end_rain.mp3",
        "length_ms": 28000,
        "prompt": (
            "Instrumental short Japanese cinematic cue: heavy rain on stone and canal water, lonely runner in a corrupt "
            "city at night, Hakuoki tragedy. Sparse piano drops like rain, cold string pad, no percussion grid, 55 BPM, "
            "20–30 seconds of emotional collapse that can loop quietly under narration. No vocals, no lyrics, no thunder "
            "cliché hits, no horror screams."
        ),
    },
    "bad_end_brothel": {
        "filename": "bad_end_brothel.mp3",
        "length_ms": 25000,
        "prompt": (
            "Instrumental Japanese cinematic tragedy stinger for an implied off-screen fate, feudal visual novel bad end, "
            "extremely restrained horror-tragedy without gore. Single descending piano phrase, detuned koto harmonic, airless "
            "string cluster resolving to emptiness, 50 BPM, 25 seconds, no vocals, no lyrics, no scream sound effects, no "
            "modern horror jump sting. Suitable for fade-to-black narration."
        ),
    },
    "bad_end_punishment": {
        "filename": "bad_end_punishment.mp3",
        "length_ms": 60000,
        "prompt": (
            "Instrumental Japanese cinematic dread bed for a sealed official office at night. "
            "Low cello ostinato, single taiko heartbeats, sparse biwa, 65 BPM, claustrophobic solemn mood. "
            "No vocals, no lyrics, no screaming, no impact sound effects. "
            "Loop-friendly under long narration. "
        ),
    },
    "case5_tease": {
        "filename": "case5_tease.mp3",
        "length_ms": 70000,
        "prompt": (
            "Instrumental Japanese cinematic mystery hook for an unfinished investigation — missing pleasure-quarter seal, "
            "feudal magistrate visual novel, Ryoko Owari corrupt city. Office tension meets distant shamisen from the quarter: "
            "low strings, ink-and-incense mood, a single ascending koto question motif like a file line not yet written, 76 BPM. "
            "Hope and danger balanced — sequel tease, not resolution. No vocals, no lyrics. Loop-friendly."
        ),
    },
}

# ---------------------------------------------------------------------------
# Main-menu opening SONG — sung Japanese vocals (vocal track, NOT instrumental).
# Uses a composition_plan so the model sings THESE exact, locked & approved
# lyrics in order. force_instrumental is omitted (only valid with `prompt`).
# Vocal direction: warm, grounded, genuinely feminine "Toa is singing" lead —
# emotive, slightly mature 2000s anime-OP vocal, NOT a high idol "ani-goe".
# respect_sections_durations=False lets the model rebalance for natural pacing
# while preserving the total (~150s) length so every section fits musically.
# ---------------------------------------------------------------------------
_MENU_GLOBAL_POSITIVE = [
    "2000s anime opening theme",
    "Japanese J-pop rock",
    "female lead vocal singing in Japanese",
    "warm, grounded, genuinely feminine voice; slightly mature; emotive and heartfelt",
    "driving but bittersweet, hopeful and cinematic",
    "strong memorable melodic hook, anthemic chorus",
    "band arrangement: electric guitar, piano, lush strings, live drums, bass",
    "clear, expressive lead vocal mixed forward",
]
_MENU_GLOBAL_NEGATIVE = [
    "high-pitched cutesy idol voice",
    "childish anime ani-goe timbre",
    "squeaky or shrill vocals",
    "chiptune",
    "rap or spoken word",
    "male vocals",
    "instrumental only / no vocals",
    "heavy autotune, robotic vocals",
    "screaming, harsh metal",
    "lo-fi, muffled",
]

MENU_SONG = {
    "filename": "main_menu_song.mp3",
    "respect_durations": False,
    "plan": {
        "positive_global_styles": _MENU_GLOBAL_POSITIVE,
        "negative_global_styles": _MENU_GLOBAL_NEGATIVE,
        "sections": [
            {
                "section_name": "Intro",
                "positive_local_styles": [
                    "soft atmospheric intro", "sparse piano and strings",
                    "tender solo female vocal entrance", "building anticipation",
                ],
                "negative_local_styles": ["full drums", "loud", "shouting"],
                "duration_ms": 12000,
                "lines": [
                    "嘘ばかりのこの街で",
                    "あなたに出会ってしまった",
                ],
            },
            {
                "section_name": "Verse 1",
                "positive_local_styles": [
                    "intimate restrained verse", "steady gentle beat enters",
                    "warm mid-range female vocal", "emotive storytelling",
                ],
                "negative_local_styles": ["over-busy", "high belting"],
                "duration_ms": 19000,
                "lines": [
                    "提灯の赤 滲む雨",
                    "運河に揺れる嘘の灯り",
                    "冷たい指先 触れた夜",
                    "それでも離せなかった",
                ],
            },
            {
                "section_name": "Pre-Chorus 1",
                "positive_local_styles": [
                    "rising pre-chorus", "crescendo and lift", "growing intensity",
                ],
                "negative_local_styles": ["flat dynamics"],
                "duration_ms": 11000,
                "lines": [
                    "あなたの優しさも 残酷さも",
                    "全部まるごと 受け止めるから",
                ],
            },
            {
                "section_name": "Chorus 1",
                "positive_local_styles": [
                    "soaring anthemic chorus", "full band, big drums and strings",
                    "powerful but warm female vocal", "strong emotional hook",
                    "bittersweet yet hopeful",
                ],
                "negative_local_styles": ["thin", "quiet", "sparse"],
                "duration_ms": 20000,
                "lines": [
                    "赤い糸が 結んでる",
                    "嘘の街で みつけた本当",
                    "返されなくても この愛は本物",
                    "あなたが知らなくても 赤に染まるこの想い",
                ],
            },
            {
                "section_name": "Verse 2",
                "positive_local_styles": [
                    "verse, slightly fuller than verse one", "steady groove",
                    "warm female vocal", "intimate",
                ],
                "negative_local_styles": ["over-busy", "high belting"],
                "duration_ms": 19000,
                "lines": [
                    "仮面の下の素顔を",
                    "私だけが知っている",
                    "赤に濡れたこの街で",
                    "あなたの嘘さえ 愛しい",
                ],
            },
            {
                "section_name": "Pre-Chorus 2",
                "positive_local_styles": [
                    "rising pre-chorus", "crescendo and lift", "growing intensity",
                ],
                "negative_local_styles": ["flat dynamics"],
                "duration_ms": 11000,
                "lines": [
                    "あなたの優しさも 残酷さも",
                    "全部まるごと 受け止めるから",
                ],
            },
            {
                "section_name": "Chorus 2",
                "positive_local_styles": [
                    "soaring anthemic chorus", "full band, big drums and strings",
                    "powerful but warm female vocal", "strong emotional hook",
                    "bittersweet yet hopeful",
                ],
                "negative_local_styles": ["thin", "quiet", "sparse"],
                "duration_ms": 20000,
                "lines": [
                    "赤い糸が 結んでる",
                    "嘘の街で みつけた本当",
                    "返されなくても この愛は本物",
                    "あなたが知らなくても 赤に染まるこの想い",
                ],
            },
            {
                "section_name": "Bridge",
                "positive_local_styles": [
                    "emotional bridge", "breakdown then build", "vulnerable, aching vocal",
                    "piano and strings forward",
                ],
                "negative_local_styles": ["same as chorus", "monotone"],
                "duration_ms": 18000,
                "lines": [
                    "どんなに冷たくても 離れない",
                    "だけど 壊さないで",
                    "戻れないほど 傷つけないで",
                    "あなたの心の壁を",
                    "私の愛が 溶かしてゆく",
                ],
            },
            {
                "section_name": "Final Chorus",
                "positive_local_styles": [
                    "climactic final chorus, biggest and most triumphant",
                    "full band, soaring female vocal", "triumphant yet bittersweet",
                    "resolved ending that can loop back to the intro",
                ],
                "negative_local_styles": ["abrupt cut", "fade to silence mid-phrase"],
                "duration_ms": 20000,
                "lines": [
                    "赤い糸は 切れない",
                    "返されなくても この愛は本物",
                    "いつかあなたも 気づくはず",
                    "そばにいるよ ずっと",
                    "赤に染まる 私たちの運命",
                ],
            },
        ],
    },
}


def _menu_lines(section_name: str) -> list:
    """Return the exact locked lyric lines for a MENU_SONG section by name.

    The OP reuses the menu song's approved Japanese verbatim, so we pull the
    lines straight from MENU_SONG instead of retyping them (avoids drift)."""
    for sec in MENU_SONG["plan"]["sections"]:
        if sec["section_name"] == section_name:
            return list(sec["lines"])
    raise KeyError(f"MENU_SONG section not found: {section_name!r}")


# ---------------------------------------------------------------------------
# Opening sequence ("OP") track — a higher-energy TECHNO/EDM remix of the menu
# song 「嘘の街の赤い糸」. Same theme + EXACT locked lyrics (pulled from MENU_SONG),
# but uptempo, four-on-the-floor, synth-driven — a classic anime-OP "TV size"
# cut (~90s). Same warm/grounded feminine "Toa is singing" vocal (NOT ani-goe).
# A composition_plan (vocals; force_instrumental omitted) so it sings the words.
# Sections chosen so the Japanese isn't rushed at the faster tempo:
#   Intro hook -> Verse 1 -> Pre-Chorus -> Chorus -> Final Chorus tag.
# ---------------------------------------------------------------------------
_OP_GLOBAL_POSITIVE = [
    "high-energy anime opening theme, TV-size OP cut",
    "uptempo J-pop rock fused with driving techno / EDM",
    "four-on-the-floor electronic kick, pulsing synth bass, bright arpeggiated synths",
    "propulsive and danceable, around 140 BPM, anthemic and cinematic",
    "female lead vocal singing in Japanese",
    "warm, grounded, genuinely feminine voice; slightly mature; emotive and powerful",
    "driving but bittersweet, hopeful, soaring chorus with a strong hook",
    "live drums layered with electronic beat, electric guitar, sweeping strings",
    "clear expressive lead vocal mixed forward over the synths",
]
_OP_GLOBAL_NEGATIVE = [
    "high-pitched cutesy idol voice",
    "childish anime ani-goe timbre",
    "squeaky or shrill vocals",
    "slow ballad, sparse, low energy",
    "rap or spoken word",
    "male vocals",
    "instrumental only / no vocals",
    "heavy autotune, robotic vocals",
    "screaming, harsh metal",
    "lo-fi, muffled",
]

OP_SONG = {
    "filename": "opening_op.mp3",
    "respect_durations": False,
    "plan": {
        "positive_global_styles": _OP_GLOBAL_POSITIVE,
        "negative_global_styles": _OP_GLOBAL_NEGATIVE,
        "sections": [
            {
                "section_name": "Intro Hook",
                "positive_local_styles": [
                    "electronic intro hook, synth arpeggio and rising riser",
                    "beat drops in, energetic", "vocal enters with attitude",
                ],
                "negative_local_styles": ["slow fade-in", "ambient drift"],
                "duration_ms": 12000,
                "lines": _menu_lines("Intro"),
            },
            {
                "section_name": "Verse 1",
                "positive_local_styles": [
                    "driving verse over four-on-the-floor beat",
                    "syncopated synth bass", "warm mid-range female vocal, propulsive",
                ],
                "negative_local_styles": ["sparse", "low energy"],
                "duration_ms": 18000,
                "lines": _menu_lines("Verse 1"),
            },
            {
                "section_name": "Pre-Chorus",
                "positive_local_styles": [
                    "rising pre-chorus with build and riser", "snare roll into the drop",
                    "growing intensity",
                ],
                "negative_local_styles": ["flat dynamics"],
                "duration_ms": 12000,
                "lines": _menu_lines("Pre-Chorus 1"),
            },
            {
                "section_name": "Chorus",
                "positive_local_styles": [
                    "explosive anthemic chorus, the drop", "full electronic + band wall of sound",
                    "powerful soaring female vocal", "huge hook, bittersweet yet euphoric",
                ],
                "negative_local_styles": ["thin", "quiet", "sparse"],
                "duration_ms": 24000,
                "lines": _menu_lines("Chorus 1"),
            },
            {
                "section_name": "Final Chorus",
                "positive_local_styles": [
                    "climactic final chorus, biggest and most triumphant drop",
                    "full electronic band, soaring female vocal", "triumphant yet bittersweet",
                    "strong resolved ending suitable to button an OP",
                ],
                "negative_local_styles": ["abrupt cut mid-word", "fade to silence mid-phrase"],
                "duration_ms": 24000,
                "lines": _menu_lines("Final Chorus"),
            },
        ],
    },
}


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


class GenerationHalted(Exception):
    """Plan/permission/quota/rate-limit conditions that require user action."""


def _subscription(api_key: str) -> dict | None:
    req = request.Request(f"{API_BASE}/v1/user/subscription",
                          headers={"xi-api-key": api_key})
    try:
        with request.urlopen(req, timeout=60) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except Exception as e:  # noqa: BLE001
        print(f"  (subscription lookup failed: {e})", file=sys.stderr)
        return None


def _post_music(payload: dict, api_key: str,
                max_retries: int = 4) -> tuple[bytes, dict]:
    """POST /v1/music with a ready-made JSON payload. Returns (audio, headers)."""
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
                raise GenerationHalted(
                    f"HTTP {e.code} plan/permission block: {payload_txt}")
            if e.code == 429:
                if "quota" in low or "credit" in low:
                    raise GenerationHalted(f"HTTP 429 quota/credits: {payload_txt}")
                if attempt > max_retries:
                    raise GenerationHalted(
                        f"HTTP 429 after {max_retries} retries: {payload_txt}")
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


def compose(prompt: str, length_ms: int, api_key: str) -> tuple[bytes, dict]:
    """Prompt-based (instrumental) generation."""
    return _post_music({
        "prompt": prompt,
        "music_length_ms": length_ms,
        "model_id": MUSIC_MODEL,
        "force_instrumental": True,
    }, api_key)


def compose_plan(plan: dict, api_key: str,
                 respect_durations: bool = False) -> tuple[bytes, dict]:
    """Composition-plan (explicit lyrics) generation.

    force_instrumental is intentionally omitted — it is only valid with `prompt`,
    and we WANT vocals. respect_sections_durations=False lets the model rebalance
    section lengths for better quality while preserving the total song duration.
    """
    return _post_music({
        "composition_plan": plan,
        "model_id": MUSIC_MODEL,
        "respect_sections_durations": respect_durations,
    }, api_key)


def write_atomic(path: Path, data: bytes) -> Path:
    tmp = path.with_suffix(path.suffix + ".part")
    tmp.write_bytes(data)
    try:
        tmp.replace(path)
        return path
    except PermissionError:
        alt = path.with_name(path.stem + "_regen" + path.suffix)
        if alt.exists():
            alt.unlink()
        tmp.replace(alt)
        print(f"  WARN: {path.name} locked; wrote {alt.name} instead", file=sys.stderr)
        return alt


def _fmt_sub(sub: dict | None) -> str:
    if not sub:
        return "unknown"
    return (f"tier={sub.get('tier')} char_used={sub.get('character_count')} "
            f"char_limit={sub.get('character_limit')}")


def main() -> int:
    ap = argparse.ArgumentParser(description="Generate Eleven Music BGM tracks.")
    ap.add_argument("--test", action="store_true",
                    help="One short 5s probe to confirm access; writes no track files.")
    ap.add_argument("--ids", default="",
                    help="Comma-separated subset of: " + ", ".join(TRACKS))
    ap.add_argument("--force", action="store_true",
                    help="Regenerate even if the target file already exists.")
    ap.add_argument("--menu", action="store_true",
                    help="Generate ONLY the sung Japanese main-menu song (vocal track) "
                         "from the locked composition_plan; skips the instrumental tracks.")
    ap.add_argument("--op", action="store_true",
                    help="Generate ONLY the higher-energy techno/EDM remix OP track "
                         "(opening_op.mp3, vocals, ~90s TV-size cut) from OP_SONG.")
    args = ap.parse_args()

    load_env_file(ENV_FILE)
    api_key = os.environ.get("ELEVENLABS_API_KEY", "").strip()
    if not api_key:
        print("ERROR: ELEVENLABS_API_KEY is not set.", file=sys.stderr)
        return 2

    BGM_DIR.mkdir(parents=True, exist_ok=True)

    if args.test:
        print("=== Eleven Music access probe (5s instrumental) ===")
        print(f"  endpoint: POST {API_BASE}/v1/music?output_format={OUTPUT_FORMAT}")
        print(f"  model: {MUSIC_MODEL}")
        sub_before = _subscription(api_key)
        print(f"  subscription (before): {_fmt_sub(sub_before)}")
        try:
            audio, hdrs = compose(
                "A short, calm instrumental Japanese koto phrase, solo, no vocals.",
                5000, api_key)
        except GenerationHalted as ge:
            print(f"\nHALTED — access/plan/quota issue:\n  {ge}", file=sys.stderr)
            return 3
        except Exception as ex:  # noqa: BLE001
            print(f"\nFAILED: {ex}", file=sys.stderr)
            return 1
        print(f"  SUCCESS: received {len(audio)} bytes of audio.")
        cost_hdrs = {k: v for k, v in hdrs.items()
                     if any(t in k.lower() for t in ("cost", "credit", "char", "song-id"))}
        if cost_hdrs:
            print(f"  cost-related headers: {cost_hdrs}")
        sub_after = _subscription(api_key)
        print(f"  subscription (after):  {_fmt_sub(sub_after)}")
        if sub_before and sub_after:
            delta = (sub_after.get("character_count") or 0) - (sub_before.get("character_count") or 0)
            print(f"  character_count delta: {delta}")
        return 0

    if args.menu:
        out = BGM_DIR / MENU_SONG["filename"]
        plan = MENU_SONG["plan"]
        total_ms = sum(s["duration_ms"] for s in plan["sections"])
        print(f"[menu] composing sung Japanese main-menu song -> {out.name}")
        print(f"[menu] {len(plan['sections'])} sections, planned total ~{total_ms/1000:.0f}s, "
              f"respect_sections_durations={MENU_SONG['respect_durations']}")
        if out.exists() and out.stat().st_size > 0 and not args.force:
            print(f"[menu] exists, skipping ({out.name}, {out.stat().st_size} bytes); "
                  f"use --force to regenerate")
            return 0
        try:
            audio, hdrs = compose_plan(plan, api_key, MENU_SONG["respect_durations"])
        except GenerationHalted as ge:
            print(f"[menu] HALTED: {ge}", file=sys.stderr)
            return 3
        except Exception as ex:  # noqa: BLE001
            print(f"[menu] FAILED: {ex}", file=sys.stderr)
            return 1
        if not audio:
            print("[menu] FAILED: empty audio", file=sys.stderr)
            return 1
        write_atomic(out, audio)
        song_id = hdrs.get("song-id") or hdrs.get("Song-Id")
        print(f"[menu] OK: {len(audio)} bytes -> {out}  (song-id={song_id})")
        return 0

    if args.op:
        out = BGM_DIR / OP_SONG["filename"]
        plan = OP_SONG["plan"]
        total_ms = sum(s["duration_ms"] for s in plan["sections"])
        print(f"[op] composing higher-energy techno remix OP -> {out.name}")
        print(f"[op] {len(plan['sections'])} sections, planned total ~{total_ms/1000:.0f}s, "
              f"respect_sections_durations={OP_SONG['respect_durations']}")
        if out.exists() and out.stat().st_size > 0 and not args.force:
            print(f"[op] exists, skipping ({out.name}, {out.stat().st_size} bytes); "
                  f"use --force to regenerate")
            return 0
        try:
            audio, hdrs = compose_plan(plan, api_key, OP_SONG["respect_durations"])
        except GenerationHalted as ge:
            print(f"[op] HALTED: {ge}", file=sys.stderr)
            return 3
        except Exception as ex:  # noqa: BLE001
            print(f"[op] FAILED: {ex}", file=sys.stderr)
            return 1
        if not audio:
            print("[op] FAILED: empty audio", file=sys.stderr)
            return 1
        write_atomic(out, audio)
        song_id = hdrs.get("song-id") or hdrs.get("Song-Id")
        print(f"[op] OK: {len(audio)} bytes -> {out}  (song-id={song_id})")
        return 0

    ids = [s.strip() for s in args.ids.split(",") if s.strip()] or list(TRACKS)
    bad = [i for i in ids if i not in TRACKS]
    if bad:
        print(f"ERROR: unknown ids {bad}; valid: {list(TRACKS)}", file=sys.stderr)
        return 2

    sub_before = _subscription(api_key)
    print(f"subscription (before): {_fmt_sub(sub_before)}")

    rc = 0
    for tid in ids:
        spec = TRACKS[tid]
        out = BGM_DIR / spec["filename"]
        if out.exists() and out.stat().st_size > 0 and not args.force:
            print(f"[{tid}] exists, skipping ({out.name}, {out.stat().st_size} bytes)")
            continue
        print(f"[{tid}] generating {spec['length_ms']/1000:.0f}s -> {out.name} ...")
        try:
            audio, hdrs = compose(spec["prompt"], spec["length_ms"], api_key)
        except GenerationHalted as ge:
            print(f"[{tid}] HALTED: {ge}", file=sys.stderr)
            return 3
        except Exception as ex:  # noqa: BLE001
            print(f"[{tid}] FAILED: {ex}", file=sys.stderr)
            rc = 1
            continue
        if not audio:
            print(f"[{tid}] FAILED: empty audio", file=sys.stderr)
            rc = 1
            continue
        out_written = write_atomic(out, audio)
        print(f"[{tid}] OK: {len(audio)} bytes -> {out_written}")

    sub_after = _subscription(api_key)
    print(f"subscription (after):  {_fmt_sub(sub_after)}")
    if sub_before and sub_after:
        delta = (sub_after.get("character_count") or 0) - (sub_before.get("character_count") or 0)
        print(f"character_count delta: {delta}")
    return rc


if __name__ == "__main__":
    raise SystemExit(main())
