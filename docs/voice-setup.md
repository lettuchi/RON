# Voice setup (ElevenLabs → Ren'Py)

## Quick start

1. Copy secrets: `cp .env.example .env` and set `ELEVENLABS_API_KEY`.
2. Install deps (venv recommended on macOS):

   ```bash
   python3 -m venv scripts/.venv
   scripts/.venv/bin/pip install -r requirements-voice.txt
   ```

3. Generate audio: `scripts/.venv/bin/python scripts/generate_voice.py`
4. Wire dialogue in `.rpy` (see below).

`.env` is gitignored — never commit API keys.

## v2 pass (Toa + Kaoru + narrator, embedded metadata)

To regenerate **without overwriting** existing `game/audio/voice/*.mp3`, use
`scripts/regenerate_voice_with_metadata.py` (writes to `game/audio/voice/v2/eve-donovan-YYYY-MM-DD/`,
embeds dialogue text in ID3 tags, maintains `scripts/voice_v2_metadata_manifest.json`).

See **[voice-metadata.md](voice-metadata.md)** for voice IDs, folder layout, and single-line regen commands.

## Environment variables

| Variable | Purpose |
|----------|---------|
| `ELEVENLABS_API_KEY` | Required — from [ElevenLabs API settings](https://elevenlabs.io/app/settings/api-keys) |
| `ELEVENLABS_VOICE_V2_TOA` | v2 Toa (`regenerate_voice_with_metadata.py`; default `Ylb1ch6nQEKvpaUivWj6`) |
| `ELEVENLABS_VOICE_V2_KAORU` | v2 Kaoru (default `zyxAdkuEJWvr177AyQPs`) |
| `ELEVENLABS_VOICE_V2_NARRATOR` | v2 narrator (default `giAoKpl5weRTCJK7uB9b`) |
| `ELEVENLABS_VOICE_TOA` | Legacy Toa (`generate_voice.py`; default **Carla** `l32B8XDoylOsZKiSdfhE`) |
| `ELEVENLABS_VOICE_KAORU` | Legacy Kaoru (default **Jax Meridian** `iB0m5bo5Htdz0t9yE0xq`) |
| `ELEVENLABS_VOICE_NARRATOR` | Legacy narrator (`generate_narrator_voice.py`) |
| `ELEVENLABS_MODEL_ID` | Optional model (default `eleven_multilingual_v2`) |

Per-line `voice_id` in the manifest overrides env defaults.

## Manifest

Edit `scripts/voice_manifest.json`. Each line needs `id`, `character`, and `text`.

**Full script (Jun 2026):** 388 unique voice IDs across prologue + canon encounter + Case 1 — **128 Toa**, **161 Kaoru**. Sources: `prologue.rpy`, `prologue_canon_encounter.rpy`, `case1_companion.rpy`, `case1_investigation.rpy`. IDs are assigned in **first-appearance order**; branch duplicates share one MP3. Reused IDs with different dialogue must get a new ID (e.g. Case 1 `kaoru_161` vs prologue `kaoru_080`).

| Status | Count |
|--------|------:|
| Manifest lines | 287 |
| MP3s on disk (manifest) | 206 / 287 |
| Orphan MP3 (`toa_069`, old manifest) | 1 |
| **Total MP3 files** | **207** |
| Still to generate | 81 |

Resume after quota reset:

```bash
ids=$(paste -sd, scripts/missing_voice_ids.txt)
scripts/.venv/bin/python scripts/generate_voice.py --ids "$ids"
```

```json
{
  "description": "Full prologue voice lines from game/prologue.rpy — deduplicated by (character, text) in first-appearance order",
  "ordering": "first_appearance",
  "lines": [
    { "id": "toa_001", "character": "toa", "text": "..." },
    { "id": "kaoru_001", "character": "kaoru", "text": "..." }
  ]
}
```

Regenerate from script (after editing `prologue.rpy`):

```bash
# Re-extract dialogue into manifest (manual or script), then:
python scripts/generate_voice.py

# Subset
python scripts/generate_voice.py --ids toa_001,kaoru_001

# Preview without API calls
python scripts/generate_voice.py --dry-run
```

Output: `game/audio/voice/{id}.mp3` (~11 MB prologue; ~18 MB when all 287 lines are generated)

## Ren'Py integration

`config.has_voice = True` is already set in `game/options.rpy`.

Attach voice to a spoken line — **`voice` on its own line before the say statement**:

```renpy
voice "audio/voice/toa_001.mp3"
toa "I was sure the clerk said third hall, fourth door on the left. Or was it the right?"
```

Narration (`"..."` without a character), menus, and `"Clerk"` lines stay unvoiced. Use the same `id` in the manifest and filename for traceability; branch duplicates can share one MP3.

Optional test clip in options:

```renpy
define config.sample_voice = "audio/voice/toa_001.mp3"
```

Players adjust volume under Preferences → Voice.

## Voice recommendations (ElevenLabs library)

Browse [Voice Library](https://elevenlabs.io/voice-library) and paste IDs into `.env`.

| Character | Direction | Project default |
|-----------|-----------|-----------------|
| **Toa** | Bright, energetic Crane dancer | **Carla** `l32B8XDoylOsZKiSdfhE` (legacy) · custom `Ylb1ch6nQEKvpaUivWj6` (v2) |
| **Kaoru** | Lower, controlled, dangerous magistrate | **Jax Meridian** `iB0m5bo5Htdz0t9yE0xq` (legacy) · custom `zyxAdkuEJWvr177AyQPs` (v2) |

Alternatives to audition in the [Voice Library](https://elevenlabs.io/voice-library): **Jessica** `cgSgspJ2msm6clMCkdW9` (Toa) · **Josh** `TxGEqnHWrfWFTfGW9XjX` or **Arnold** `VR6AewLTigWG4xSOukaG` (Kaoru).

Voice IDs vary by account; list yours with the API or the ElevenLabs app, then set `.env`.

Tune in the ElevenLabs UI, then copy the voice ID. For Japanese honorifics (`sochira-no-kata`), `eleven_multilingual_v2` handles mixed EN/JP better than monolingual models.

## Scaling to full script

1. Export dialogue from `game/prologue.rpy` (and later routes) into manifest rows.
2. Batch generate: `python scripts/generate_voice.py` (watch API quota; 287 lines ≈ plan-dependent; resume with `--ids` from `scripts/missing_voice_ids.txt` if quota is hit).
3. Add `voice "audio/voice/..."` on the line **before** each voiced say statement in `.rpy`.
4. Run `renpy.sh <project> lint` to verify script syntax.
5. Commit **only** `game/audio/voice/*.mp3` and the manifest — not `.env`.

## Security

If an API key was pasted in chat, **rotate it** in ElevenLabs settings and update `.env`.
