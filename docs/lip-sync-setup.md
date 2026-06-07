# Lip sync setup (Rhubarb + RenPy Lip Sync Plugin)

**Status:** Scaffold only — plugin files are in `game/lip-sync-plugin/` but **no dialogue uses `lipsync()` yet**. Toa/Kaoru `layeredimage` defs have **no mouth attribute group** (phase 2 art).

**Upstream:** [RenPy-Lipsync-Plugin](https://github.com/Wendy-Nam/RenPy-Lipsync-Plugin) (MIT) · [Rhubarb Lip Sync](https://github.com/DanielSWolf/rhubarb-lip-sync) (MIT)

## What is installed

| Path | Purpose |
|------|---------|
| `game/lip-sync-plugin/lipsync_module.rpy` | `lipsync()` function, `lipsync` audio channel |
| `game/lip-sync-plugin/generate_lipsync_data.py` | Batch Rhubarb → TSV timing files |
| `game/lip-sync-plugin/lip-sync-data/<character>/` | Generated `.txt` timing (empty until you run Rhubarb) |

Rhubarb binaries are **not** committed (large, OS-specific). Download and place them yourself (see below).

## Rhubarb (required for data generation)

1. Download the latest release for your OS from [rhubarb-lip-sync releases](https://github.com/DanielSWolf/rhubarb-lip-sync/releases) (e.g. `Rhubarb-Lip-Sync-1.13.0-Windows.zip`).
2. Extract into `game/lip-sync-plugin/` (e.g. `game/lip-sync-plugin/Rhubarb-Lip-Sync-1.13.0-Win32/rhubarb.exe`).
3. Edit **line 10** of `game/lip-sync-plugin/generate_lipsync_data.py` to point at your executable:

   ```python
   # Windows example:
   rhubarb_path = os.path.join(script_dir, "Rhubarb-Lip-Sync-1.13.0-Win32", "rhubarb.exe")
   ```

4. Run from `game/lip-sync-plugin/`:

   ```bash
   python generate_lipsync_data.py
   ```

Mouth shape reference: [Rhubarb mouth shapes](https://github.com/DanielSWolf/rhubarb-lip-sync#mouth-shapes) (A–H, X).

## Audio format limitations

| Topic | Detail |
|-------|--------|
| **Rhubarb input** | `.wav` or `.ogg` only — **not `.mp3`**. Convert VO before generation (`ffmpeg -i line.mp3 line.wav`). |
| **This project today** | Dialogue uses `voice "audio/voice/toa_129.mp3"` etc. — flat files under `game/audio/voice/`, **not** per-character subfolders. |
| **Plugin layout** | Upstream expects `game/audio/voice/<character>/<file>.wav` and `lip-sync-data/<character>/<basename>.txt`. |
| **Existing `voice` lines** | Unchanged — Ren'Py `voice` + `config.has_voice` still work; lip sync is a **separate** code path (`$ lipsync(...)`), not wired globally. |

**Phase 2 — before enabling in-game lip sync:**

1. Add a `group mouth:` to each `layeredimage` (sprites A–H + closed X per expression set).
2. Reorganize or symlink VO into `audio/voice/toa/`, `audio/voice/kaoru/` (or adjust `generate_lipsync_data.py` for flat filenames).
3. Generate timing data, then call `lipsync(character, "filename.wav", "Displayed line")` on test labels only until art is complete.

## Example integration (do not enable in main story yet)

```renpy
layeredimage toa:
    at sprite_highlight('toa')
    group expression:
        ...
    group mouth:
        attribute mouth_X default:
            "images/sprites/toa/mouth/toa-mouth-X.png"
        # mouth_A … mouth_H when art exists

# $ lipsync(toa, "some_line.wav", "Line text shown during sync")
```

## Skip / voice interaction

The plugin plays audio on the `lipsync` channel and stops on skip/click. It does not replace `voice` statements; plan either lip-sync-only scenes or a single audio source to avoid double playback.
