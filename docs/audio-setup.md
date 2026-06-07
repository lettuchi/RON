# Audio setup — prologue SFX

Sound effects for **Ryoko Owari Nights** prologue beats. Voice lines are documented in [voice-setup.md](voice-setup.md).

## Quick start

SFX are already wired in `game/prologue.rpy` and registered in `game/audio.rpy`.

Regenerate procedural fallbacks (no API required):

```bash
.venv-sprite/bin/python scripts/synthesize_sfx.py
```

Upgrade to ElevenLabs when your API key has **sound_generation** permission:

```bash
scripts/.venv/bin/python scripts/generate_sfx.py
```

Requires `ELEVENLABS_API_KEY` in `.env` (same key as voice). If you get HTTP 401 `missing_permissions`, use `synthesize_sfx.py` or enable SFX on your ElevenLabs plan.

## Prologue SFX inventory

| ID | File | Source | Wired to |
|----|------|--------|----------|
| `door_slam` | `game/audio/sfx/door_slam.wav` | synthesized | Wrong door — "The door shuts with finality" |
| `knock_formal` | `game/audio/sfx/knock_formal.wav` | synthesized | Formal knock (two strikes) entering office |
| `knock_single` | `game/audio/sfx/knock_single.wav` | synthesized | Patient single knock (`wait_quietly` branch) |
| `sliding_door_open` | `game/audio/sfx/sliding_door_open.wav` | synthesized | Scene change to magistrate office |
| `sliding_door_close` | `game/audio/sfx/sliding_door_close.wav` | synthesized | Door closes behind Toa; canon latch |
| `footsteps_corridor` | `game/audio/sfx/footsteps_corridor.wav` | synthesized | Opening corridor; walkout boots echo |
| `paper_shuffle` | `game/audio/sfx/paper_shuffle.wav` | synthesized | Permit on desk; canon signing prep |
| `hanko_stamp` | `game/audio/sfx/hanko_stamp.wav` | synthesized | Canon seal press |
| `hanko_case_click` | `game/audio/sfx/hanko_case_click.wav` | synthesized | Refuse-dance bad end case snap |
| `fan_open` | `game/audio/sfx/fan_open.wav` | synthesized | Formal fan dance branch |
| `obijime_bells` | `game/audio/sfx/obijime_bells.wav` | synthesized | Flirtatious dance branch |
| `cushion_slide` | `game/audio/sfx/cushion_slide.wav` | synthesized | Cushion pushed across desk |
| `chair_creak` | `game/audio/sfx/chair_creak.wav` | synthesized | "Unless?" chair tension CG |

**Total:** 13 files, ~750 KB (WAV 44.1 kHz mono/stereo).

## Ren'Py registration

`game/audio.rpy`:

```renpy
define audio.door_slam = "audio/sfx/door_slam.wav"
# ...
```

Usage in script:

```renpy
play sound audio.door_slam
play sound audio.knock_formal volume 0.8
```

Ren'Py accepts `.wav`, `.ogg`, and `.mp3`. Prefer `.ogg` for release builds if you convert later with ffmpeg:

```bash
ffmpeg -i game/audio/sfx/door_slam.wav -c:a libvorbis -q:a 4 game/audio/sfx/door_slam.ogg
```

Then update the `define` paths in `audio.rpy`.

## Adding new SFX

1. Add an entry to `scripts/sfx_manifest.json` (`id`, `text` prompt, optional `duration_seconds`).
2. Add a synthesizer function in `scripts/synthesize_sfx.py` **or** run `scripts/generate_sfx.py` (ElevenLabs).
3. Register `define audio.{id}` in `game/audio.rpy`.
4. Insert `play sound audio.{id}` at the story beat in the relevant `.rpy` file.
5. Update the inventory table in this doc.

## Mixer settings

`config.has_sound = True` and `config.has_music = True` are set in `game/options.rpy`. Players adjust SFX / Music volume via preferences.

## Background music (BGM)

Placeholder loops live in `game/audio/bgm/*.ogg` (procedural — `scripts/synthesize_bgm.py`).

| ID | File | Wired in prologue |
|----|------|-------------------|
| `bgm_main_menu` | `main_menu.ogg` | Main menu (`config.main_menu_music`) |
| `bgm_corridor` | `corridor.ogg` | Opening corridor, verbal ending |
| `bgm_office` | `office.ogg` | Magistrate office |
| `bgm_street` | `street.ogg` | Walkout exterior |
| `bgm_toa_theme` | `toa_theme.ogg` | Office dance |
| `bgm_kaoru_theme` | `kaoru_theme.ogg` | Kaoru entrance, grab moment |
| `bgm_canon_intimate` | `canon_intimate.ogg` | Canon route |

Regenerate placeholders:

```bash
.venv-sprite/bin/python scripts/synthesize_bgm.py
```

Optional ElevenLabs Music API (paid plan):

```bash
scripts/.venv/bin/python scripts/generate_bgm.py
```

**Replace with GarageBand exports:** see [garageband-bgm-guide.md](garageband-bgm-guide.md).

Defines: `game/audio/music.rpy`. Usage:

```renpy
play music audio.bgm_corridor fadein 2.5 loop volume 0.65
stop music fadeout 2.5
```

## Manifest files

| File | Purpose |
|------|---------|
| `scripts/sfx_manifest.json` | Prompts / metadata for each SFX id |
| `scripts/bgm_manifest.json` | Prompts for ElevenLabs Music API tracks |
| `scripts/generate_sfx.py` | ElevenLabs text-to-sound API batch generator |
| `scripts/generate_bgm.py` | ElevenLabs Music API batch generator |
| `scripts/synthesize_sfx.py` | Offline numpy/scipy fallback (`.venv-sprite`) |
| `scripts/synthesize_bgm.py` | Offline procedural BGM loops (`.venv-sprite`) |

Do not commit `.env` or echo API keys in docs or chat.
