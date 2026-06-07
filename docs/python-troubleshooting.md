# Python tooling — crashes and fixes

## Symptom: “Python quit unexpectedly” while generating assets

On macOS this is usually a **segmentation fault** in a native library, not a normal Python traceback. Check recent reports:

```bash
ls -lt ~/Library/Logs/DiagnosticReports/Python*.ips | head
```

For this project, crashes at **19:03 on 2026-05-30** were all in **libsndfile’s Vorbis encoder** while running `scripts/synthesize_bgm.py` (stack trace: `vorbis_analysis_wrote` → `sf_writef_float`).

## Virtual environments

| Venv | Python | Purpose |
|------|--------|---------|
| `scripts/.venv` | 3.14 | ElevenLabs voice (`generate_voice.py`) |
| `.venv-sprite` | 3.14 | BGM/SFX synthesis, rembg sprites |
| `.venv-diagram` | 3.14 | Choice-tree diagram (`render_prologue_choice_tree.py`) |

All three were created with Homebrew **Python 3.14.5**. That version is very new; if you see odd native crashes, recreate a venv with 3.12 or 3.13:

```bash
brew install python@3.13
rm -rf .venv-sprite
python3.13 -m venv .venv-sprite
.venv-sprite/bin/pip install -r requirements-sprite.txt
```

## Script-specific notes

### `scripts/synthesize_bgm.py` — **most likely crash**

- Uses **soundfile → libsndfile → Vorbis** to write `.ogg` loops.
- Writing a full ~60 s stereo buffer in one call can **SIGSEGV** on Apple Silicon.
- **Fix (in repo):** `_write()` now streams **1 s chunks** via `sf.SoundFile`.
- Regenerate safely: `.venv-sprite/bin/python scripts/synthesize_bgm.py`
- One track at a time if memory is tight: `--ids toa_theme`

### `scripts/synthesize_sfx.py` — stable

- Writes **WAV** via `scipy.io.wavfile` (no libsndfile Vorbis). Unlikely to segfault.

### `scripts/make_sprites_transparent.sh` — heavy but usually OK

- Loads **rembg + onnxruntime + u2net** (~176 MB model). High RAM; can slow the machine but rarely segfaults.
- Run once after new sprite art; avoid running in parallel with BGM synthesis.
- Needs network on first run to download `~/.u2net/u2net.onnx`.

### `scripts/generate_voice.py` / `generate_sfx.py`

- HTTP API clients only (ElevenLabs). Crashes here are almost always network/auth errors, not segfaults.

### `scripts/render_prologue_choice_tree.py`

- matplotlib only; safe unless the venv is corrupt.

## If crashes continue

1. Recreate `.venv-sprite` with Python 3.13 (see above).
2. Run one asset script at a time; quit other heavy apps.
3. For BGM, export from GarageBand instead — see [garageband-bgm-guide.md](garageband-bgm-guide.md).
4. Check for zombie Python: `ps aux | grep python` — kill stale PIDs if any.

## Ren'Py vs project Python

The game runs on **Ren'Py’s bundled Python 3.12** under `tools/renpy-8.5.3-sdk/`. That is separate from the Homebrew 3.14 venvs used for asset generation.
