# Toa Theme — GarageBand Automation Session

**Date:** 2026-05-30  
**Goal:** Create `game/audio/bgm/toa_theme.ogg` from GarageBand for Kakita Toa's leitmotif.

---

## Executive summary

| Path | Result |
|------|--------|
| GarageBand AppleScript (open, tempo, save) | **Partial success** |
| GarageBand UI automation (export menus) | **Blocked** — needs Accessibility for Terminal/Cursor |
| MIDI composition → GarageBand import | **Success** |
| Procedural OGG fallback | **Success** (placeholder quality, not GarageBand) |

**Current playable file:** `game/audio/bgm/toa_theme.ogg` is a **procedural placeholder** from `scripts/synthesize_bgm.py`. It works in Ren'Py today but is **not** a GarageBand render.

**Best path to finish:** Open the saved project or MIDI in GarageBand (already done once this session), assign World/Orchestral patches, export, convert to OGG.

---

## What we attempted

### 1. Web research

Findings:

- GarageBand has **no public sdef** in the app bundle and **minimal AppleScript** (basic app + document object only).
- **No scriptable export**, track creation, or note insertion.
- UI automation via System Events is the usual workaround for Share → Export, but it requires **Accessibility** permission and is fragile (track solo clicks often fail).
- MIDI **export** from GarageBand is awkward (loop-library workaround / GB2MIDI); **MIDI import** is the practical direction for us.
- Third-party tools (`cli-anything-garageband`, SoundFlow) wrap UI automation — not installed this session.

### 2. AppleScript / sdef probe

```bash
# sdef unavailable without full Xcode; no .sdef in GarageBand.app bundle
osascript -e 'tell application "GarageBand" to get name'   # → GarageBand ✓
```

**Scriptable today (verified):**

| Command | Works? |
|---------|--------|
| `activate` | ✓ |
| `open POSIX file "…/toa_theme.mid"` | ✓ (via `open -a GarageBand` too) |
| `count of documents` | ✓ |
| `front document` → `name`, `path`, `modified` | ✓ |
| `set tempo to 100` on front document | ✓ |
| `set name to "Toa Theme"` | ✓ |
| `save` / `save in POSIX file "…/toa_theme.band"` | ✓ |
| `export` on document | ✗ doesn't understand export |
| `tracks` on document | ✗ not defined |

**System Events UI scripting:**

```
System Events got an error: osascript is not allowed assistive access. (-1719)
```

Export helper script exists but cannot run until Accessibility is granted:

`scripts/garageband_export_toa.applescript`

### 3. MIDI composition (fallback — worked)

Created `scripts/compose_toa_theme_midi.py` using **mido** (installed in `.venv-sprite`).

**Spec implemented:**

- **100 BPM**, **D major**, 4/4
- **40 bars** = 8-bar intro + 32-bar loop (~96 s)
- **4 tracks:** Koto Melody, Shamisen Bass, String Pad, Woodblock
- Motif from [garageband-bgm-guide.md](garageband-bgm-guide.md): D–E–F#–A–B–A–F#–D (+ variations)

**Generate:**

```bash
.venv-sprite/bin/python scripts/compose_toa_theme_midi.py
```

**Output:** `game/audio/bgm/toa_theme.mid`

**Import into GarageBand (automated this session):**

```bash
open -a GarageBand game/audio/bgm/toa_theme.mid
```

After import, AppleScript set tempo to 100 and saved the project.

### 4. GarageBand project saved in repo

```
game/audio/bgm/toa_theme.band   # ~692 KB, renamed "Toa Theme"
```

Also at `~/Music/GarageBand/Untitled.band` (older name before rename).

Re-open either:

```bash
open game/audio/bgm/toa_theme.band
# or
open game/audio/bgm/toa_theme.mid
```

### 5. Procedural audio (last resort — used for current OGG)

```bash
.venv-sprite/bin/python scripts/synthesize_bgm.py --ids toa_theme
```

Produces `toa_theme.ogg` (~47 s loop at 102 BPM). **Honest label: NOT GarageBand** — numpy/scipy pluck synthesis.

---

## Files created / updated

| File | Description |
|------|-------------|
| `game/audio/bgm/toa_theme.mid` | Multi-track MIDI source |
| `game/audio/bgm/toa_theme.band` | GarageBand project (MIDI imported, tempo 100) |
| `game/audio/bgm/toa_theme.ogg` | Procedural placeholder (in-game today) |
| `scripts/compose_toa_theme_midi.py` | MIDI composer |
| `scripts/garageband_export_toa.applescript` | Export UI helper (needs Accessibility) |
| `docs/toa-theme-garageband-session.md` | This report |

---

## Finish in GarageBand (manual steps, ~10 min)

GarageBand should already show **"Toa Theme"** with imported MIDI regions. If not:

1. **Open project:** `open game/audio/bgm/toa_theme.band`
2. **Confirm tempo:** 100 BPM, key D major (LCD top center).
3. **Assign instruments** (Library → World / Orchestral):

   | Track name | Suggested patch |
   |------------|-----------------|
   | Koto Melody | Koto, Pipa, or Gu Zheng |
   | Shamisen Bass | Shamisen or Biwa |
   | String Pad | Slow Strings / String Ensemble |
   | Woodblock | Japanese Drum or Woodblock (optional, low volume) |

4. **Set cycle region** to bars 9–40 (32-bar loop body) or full 40 bars.
5. **Mix:** Keep melody forward; strings bed ~−6 dB; avoid heavy reverb on loop boundary.
6. **Export:** Share → Export Song to Disk → **AIFF or WAV**, 44.1 kHz.
7. **Convert to OGG** (install ffmpeg if needed):

   ```bash
   brew install ffmpeg   # once
   ffmpeg -i ~/Desktop/Toa\ Theme.aiff -c:a libvorbis -q:a 4 \
     game/audio/bgm/toa_theme.ogg
   ```

   Or with built-in `afconvert` to AAC first, then ffmpeg to vorbis.

8. **Launch game** — `music.rpy` already points at `audio/bgm/toa_theme.ogg`.

### Optional: enable export automation

1. **System Settings → Privacy & Security → Accessibility**
2. Add **Terminal** and/or **Cursor** (whatever runs `osascript`).
3. Run:

   ```bash
   osascript scripts/garageband_export_toa.applescript
   ```

   Then convert the exported AIFF as above.

---

## Automation reference (copy-paste)

**Open + configure via AppleScript:**

```applescript
set midiPath to POSIX file "/Users/amanda.yazdani/Downloads/amanda/ryoko-owari/game/audio/bgm/toa_theme.mid"
tell application "GarageBand"
  activate
  open midiPath
  delay 2
  tell front document
    set tempo to 100
    set name to "Toa Theme"
    save in (POSIX file "/Users/amanda.yazdani/Downloads/amanda/ryoko-owari/game/audio/bgm/toa_theme.band")
  end tell
end tell
```

**One-liner shell:**

```bash
open -a GarageBand game/audio/bgm/toa_theme.mid
```

---

## Recommendations

1. **Replace** `toa_theme.ogg` with a GarageBand export when patches are assigned — the MIDI arrangement is already in the `.band` project.
2. **Keep** `toa_theme.mid` in repo as a portable source; re-import if the `.band` file drifts.
3. **Do not** rely on GarageBand AppleScript for export until Apple exposes it; UI scripting + Accessibility is the only macOS-native batch path today.
4. For other BGM tracks, reuse `compose_*_midi.py` pattern or compose directly in GarageBand using [garageband-bgm-guide.md](garageband-bgm-guide.md).

---

## Related docs

- [garageband-bgm-guide.md](garageband-bgm-guide.md) — track specs and export workflow
- [audio-setup.md](audio-setup.md) — Ren'Py audio wiring
