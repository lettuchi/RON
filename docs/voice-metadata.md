# Voice v2 (Toa + Kaoru + narrator) and per-line metadata

This pass regenerates **Toa**, **Kaoru**, and **narrator** lines with ElevenLabs voices **without deleting or overwriting** existing `game/audio/voice/*.mp3` files.

## Voice assignment

| Ren'Py speaker | Default voice ID | Env override |
|----------------|------------------|--------------|
| **toa** | `Ylb1ch6nQEKvpaUivWj6` | `ELEVENLABS_VOICE_V2_TOA` |
| **kaoru** | `zyxAdkuEJWvr177AyQPs` | `ELEVENLABS_VOICE_V2_KAORU` |
| **narrator** (bare `"..."` lines) | `giAoKpl5weRTCJK7uB9b` | `ELEVENLABS_VOICE_V2_NARRATOR` |

Kaoru dialogue uses the `kaoru_*` IDs from `scripts/voice_manifest.json`. Narrator uses `narrator_*` from `scripts/narrator_manifest.json`. Display names in the manifest come from the ElevenLabs API when regenerating.

Legacy generation (`generate_voice.py` / `generate_narrator_voice.py`) still targets `game/audio/voice/` and the game’s current `.rpy` paths (`audio/voice/{id}.mp3`).

## Folder layout

```
game/audio/voice/                    # LEGACY — left untouched by v2 script
  toa_001.mp3
  kaoru_001.mp3
  narrator_001.mp3
  v2/
    eve-donovan-2026-06-02/          # dated folder (default subdir name)
      toa_001.mp3
      kaoru_001.mp3
      narrator_001.mp3
```

Tooling manifest (JSON, all generated v2 lines):

```
scripts/voice_v2_metadata_manifest.json
```

Resume list after quota stop:

```
scripts/missing_voice_v2_ids.txt
```

## Embedded MP3 metadata (ID3)

Each v2 MP3 is tagged with **mutagen** so you can regen one line without opening `.rpy`:

| Frame | Purpose |
|-------|---------|
| `TIT2` | Line id (`toa_001`, `narrator_042`, …) |
| `TXXX:renpy_line` | Full spoken text (TTS input) |
| `TXXX:renpy_character` | `toa` \| `kaoru` \| `narrator` |
| `TXXX:elevenlabs_voice_id` | ElevenLabs voice id used |
| `TXXX:renpy_id` | Same as line id |
| `TXXX:renpy_source` | Script location when known (`prologue.rpy:13`) |
| `COMM:renpy_v2` | JSON blob with all fields above |

### Sidecar manifest entry (example)

```json
{
  "id": "kaoru_002",
  "character": "kaoru",
  "voice_name": "Kaoru",
  "voice_id": "zyxAdkuEJWvr177AyQPs",
  "text": "Wrong door. Again.",
  "source_file": "prologue.rpy:28",
  "path": "game/audio/voice/v2/eve-donovan-2026-06-02/kaoru_002.mp3",
  "renpy_audio_path": "audio/voice/v2/eve-donovan-2026-06-02/kaoru_002.mp3",
  "manifest": "voice_manifest.json"
}
```

## Setup

```bash
python -m venv scripts/.venv
scripts/.venv/Scripts/pip install -r requirements-voice.txt   # Windows
# scripts/.venv/bin/pip install -r requirements-voice.txt   # macOS/Linux
```

Set `ELEVENLABS_API_KEY` in `scripts/.env` (see `scripts/.env.example`).

Optional overrides (v2 script only — does **not** read legacy `ELEVENLABS_VOICE_TOA` / `KAORU` from `.env`):

```env
ELEVENLABS_VOICE_V2_TOA=Ylb1ch6nQEKvpaUivWj6
ELEVENLABS_VOICE_V2_KAORU=zyxAdkuEJWvr177AyQPs
ELEVENLABS_VOICE_V2_NARRATOR=giAoKpl5weRTCJK7uB9b
```

## Expressive tags (v3)

Tagged delivery text is maintained separately from Ren'Py in `scripts/voice_performance_manifest.json`. Regeneration uses `tts_text` when that file is present. See [voice-performance-manifest.md](voice-performance-manifest.md).

## Commands

From project root (use your venv Python if created):

```bash
# Verify API + both voices (no files written)
python scripts/regenerate_voice_with_metadata.py --check

# Plan full batch (~394 unique lines: 127 Toa + 160 Kaoru + 107 narrator)
python scripts/regenerate_voice_with_metadata.py --dry-run

# Audition sample (one per speaker + extras)
python scripts/regenerate_voice_with_metadata.py --sample 5

# Full v2 regeneration (plain manifest text)
python scripts/regenerate_voice_with_metadata.py

# v3 + performance tags (set ELEVENLABS_MODEL_ID=eleven_v3 in scripts/.env)
python scripts/regenerate_voice_with_metadata.py --model eleven_v3

# Single line by id
python scripts/regenerate_voice_with_metadata.py --ids kaoru_002 --force

# Single line by dialogue text (exact match)
python scripts/regenerate_voice_with_metadata.py --text "Wrong door. Again." --force

# Resume after quota
python scripts/regenerate_voice_with_metadata.py --ids @scripts/missing_voice_v2_ids.txt

# Read tags from an existing v2 file
python scripts/regenerate_voice_with_metadata.py --read-metadata game/audio/voice/v2/eve-donovan-2026-06-02/toa_001.mp3
```

## Switching the game to v2 audio

The game still references `voice "audio/voice/{id}.mp3"`. There is **no** central Ren'Py manifest switch. Options:

1. **Bulk path update** — replace `audio/voice/` with `audio/voice/v2/eve-donovan-YYYY-MM-DD/` in `.rpy` files (only after you approve the new takes).
2. **Copy into legacy folder** — copy approved v2 MP3s over `game/audio/voice/{id}.mp3` (backs up old files first if you want to keep them elsewhere).
3. **Leave legacy active** — keep playing old audio until you swap manually.

Do not point the game at v2 until you have listened to the new files.

## Counts (manifests, May 2026)

| Set | Unique lines |
|-----|-------------:|
| Toa (`voice_manifest.json`) | 127 |
| Kaoru | 160 |
| Narrator (`narrator_manifest.json`) | 107 |
| **v2 total** | **394** |

See also [voice-setup.md](voice-setup.md) for original Carla / Jax Meridian workflow.
