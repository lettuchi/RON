# Kaoru Theme — GarageBand Automation Session

**Date:** 2026-05-30  
**Revision:** **v3 (pleasant minor + shakuhachi echo)** — 2026-05-30  
**Goal:** Create `game/audio/bgm/kaoru_theme.ogg` from GarageBand for Kitsu Kaoru's leitmotif (Emerald Magistrate — controlled menace, imperial formality).

---

## v3 — pleasant minor + shakuhachi echo (2026-05-30)

User feedback on v2: still too discordant. Keep A minor / 78 BPM / formal menace, but make it **musically pleasant** and add **shakuhachi call-and-response**.

| Area | v2 | v3 |
|------|----|----|
| Pad cycle | Am / F / **Dm** / Em | Am / F / **C** / **G** (warmer subdominant area) |
| Pad voicing | Root + 5th stacks | **Root + 3rd + 5th** (consonant triads) |
| Melody | Neighbor zigzag in MOTIF_A (D–E–D) | **Pure descending** lines; steps/minor 3rds only |
| Dynamics | Melody 74, taiko 48 | Melody **68**, pad **40**, taiko **36/32**, echo **~44** |
| Shakuhachi | Sparse chord-tone accents (separate track) | **Shakuhachi Echo** — melody delayed **+1 bar**, 65% velocity, 65% note length |
| Echo scope | — | Bars **1–4** of each 8-bar phrase only; **octave lower** on odd 8-bar phrases |
| Bass | Root + fifth plucks | Root + **3rd + 5th** gentle arpeggio (loop) |

**Regenerated this session:**

```bash
.venv-sprite/bin/python scripts/compose_kaoru_theme_midi.py
osascript -e '...'  # opens MID, tempo 78, saves kaoru_theme.band as "Kaoru Theme"
.venv-sprite/bin/python scripts/synthesize_bgm.py --ids kaoru_theme
```

**Echo implementation (MIDI):** `compose_kaoru_theme_midi.py` collects melody notes, then `_shakuhachi_echo_track()` copies each note with `start + 1 bar`, velocity `int(VEL_MELODY * 0.65)`, duration `beat * 0.65`. Filter: `_section_bar_index(bar) <= 3`. Octave shift when `(bar_index // 8) % 2 == 1`.

**Procedural OGG:** `synth_kaoru_theme()` mirrors Am/F/C/G pads, softer taiko, and `_shakuhachi_breath()` echo at **+1 bar** on phrase bars 0–3.

---

## v2 — less discordant (2026-05-30)

User feedback: keep A minor / 78 BPM / low strings + taiko / formal menace, but **reduce harsh clashes**.

| Area | v1 | v2 |
|------|----|----|
| Pad cycle | Am / F / **G** / Em | Am / F / **Dm** / Em (diatonic A minor) |
| Melody | Wide leaps, MOTIF_C zigzag (F4–E4–F4) | Stepwise/neighbor tones; clean descent in MOTIF_C |
| Note length | ~1.1× beat (overlap → minor 2nds) | ~0.82× beat (Toa-like separation) |
| Bass | Sustained root+fifth stack; octave jump bar 4 | Plucked root; fifth on beat 2 / 1.5 (off melody 1) |
| Taiko | Beats 1 & 3 (with melody downbeats) | Beats **2 & 4** (between melody peaks) |
| Shakuhachi | Chromatic accent pool (E5, B3, …) | **Chord tones only**; every 8 bars, beat 4 |
| Shamisen | Beat 1.5 | Beat **3**, root +12 |

**Regenerated this session:**

```bash
.venv-sprite/bin/python scripts/compose_kaoru_theme_midi.py
osascript -e '...'  # see Automation reference — opens MID, tempo 78, saves .band
.venv-sprite/bin/python scripts/synthesize_bgm.py --ids kaoru_theme
```

---

## Executive summary

| Path | Result |
|------|--------|
| MIDI composition → GarageBand import | **Success** (v3 regenerated) |
| GarageBand AppleScript (open, tempo, save) | **Success** (v3 `.band` re-saved at 78 BPM) |
| GarageBand UI automation (export menus) | **Blocked** — needs Accessibility for Terminal/Cursor |
| Procedural OGG fallback | **Success** (placeholder quality, not GarageBand) |

**Current playable file:** `game/audio/bgm/kaoru_theme.ogg` is a **procedural placeholder** from `scripts/synthesize_bgm.py`. It works in Ren'Py today but is **not** a GarageBand render.

**Best path to finish:** Open the saved project in GarageBand (already done this session), assign World/Orchestral patches (low strings + taiko, **not** koto as lead), export, convert to OGG.

---

## Spec implemented

| Parameter | Value |
|-----------|-------|
| Key | **A minor** |
| Tempo | **78 BPM** |
| Structure | **40 bars** = 8-bar intro + 32-bar loop (~123 s) |
| Motif | Descending minor phrases: **A→F→E** extended with formal imperial weight |
| Mood | Lower, deliberate, dangerous but not horror; power imbalance, cold appraisal |

**6 MIDI tracks (v3):**

| Track name | Role |
|------------|------|
| Low Strings Melody | Lyrical descending A-minor phrases |
| Low Strings Bass | Root + chord-tone arpeggios (off melody downbeats) |
| String Pad | Am / F / C / G triads (v3) |
| Taiko | Sparse hits on beats **2 and 4** |
| Shakuhachi Echo | Melody call-and-response (+1 bar, quieter) |
| Shamisen Undertone | Sparse root accent on beat 3 (not lead) |

---

## What we did

### 1. MIDI composition

Created `scripts/compose_kaoru_theme_midi.py` using **mido** (same pattern as Toa).

**Generate:**

```bash
.venv-sprite/bin/python scripts/compose_kaoru_theme_midi.py
```

**Output:** `game/audio/bgm/kaoru_theme.mid`

### 2. GarageBand import + save (automated)

```bash
open -a GarageBand game/audio/bgm/kaoru_theme.mid
```

AppleScript set tempo to **78**, renamed project **"Kaoru Theme"**, saved:

```
game/audio/bgm/kaoru_theme.band
```

Re-open either:

```bash
open game/audio/bgm/kaoru_theme.band
# or
open game/audio/bgm/kaoru_theme.mid
```

### 3. Procedural placeholder (in-game today)

```bash
.venv-sprite/bin/python scripts/synthesize_bgm.py --ids kaoru_theme
```

Produces `kaoru_theme.ogg` (~61.5 s loop at 78 BPM). **Honest label: NOT GarageBand** — numpy/scipy synthesis.

### 4. Export helper (needs Accessibility)

`scripts/garageband_export_kaoru.applescript` — same UI-automation pattern as Toa. Will fail with `-1719` until Terminal/Cursor has Accessibility permission.

---

## Files created / updated

| File | Description |
|------|-------------|
| `game/audio/bgm/kaoru_theme.mid` | Multi-track MIDI source |
| `game/audio/bgm/kaoru_theme.band` | GarageBand project (MIDI imported, tempo 78) |
| `game/audio/bgm/kaoru_theme.ogg` | Procedural placeholder (in-game today) |
| `scripts/compose_kaoru_theme_midi.py` | MIDI composer |
| `scripts/garageband_export_kaoru.applescript` | Export UI helper (needs Accessibility) |
| `docs/kaoru-theme-garageband-session.md` | This report |

**Ren'Py wiring:** `game/audio/music.rpy` already defines `audio.bgm_kaoru_theme = "audio/bgm/kaoru_theme.ogg"` — no change needed.

---

## Finish in GarageBand (manual steps, ~10 min)

GarageBand should show **"Kaoru Theme"** with imported MIDI regions. If not:

1. **Open project:** `open game/audio/bgm/kaoru_theme.band`
2. **Confirm tempo:** 78 BPM, key A minor (LCD top center).
3. **Assign instruments** (Library → World / Orchestral):

   | Track name | Suggested patch |
   |------------|-----------------|
   | Low Strings Melody | **Cello**, **Contrabass**, or **Slow Strings** (low register) |
   | Low Strings Bass | **Contrabass**, **Upright Bass**, or **Orchestral Strings** (sustain) |
   | String Pad | **String Ensemble** or **Dark Pad** (~−8 dB) |
   | Taiko | **Taiko**, **Japanese Drum**, or **Frame Drum** (quiet, beats **2 & 4**) |
   | Shakuhachi Echo | **Shakuhachi** or **Japanese Flute** (~−12 dB vs melody; assign echo track) |
   | Shamisen Undertone | **Shamisen** or **Biwa** (accent only — **not** the lead) |

   **Do not** use Koto as the primary lead — Kaoru is low strings + taiko weight, not bright plucks.

4. **Set cycle region** to bars 9–40 (32-bar loop body) or full 40 bars.
5. **Mix:** Keep low strings forward but controlled; taiko felt not loud (~−10 dB); shakuhachi barely audible; avoid heavy reverb at loop boundary.
6. **Export:** Share → Export Song to Disk → **AIFF or WAV**, 44.1 kHz.
7. **Convert to OGG:**

   ```bash
   brew install ffmpeg   # once
   ffmpeg -i ~/Desktop/Kaoru\ Theme.aiff -c:a libvorbis -q:a 4 \
     game/audio/bgm/kaoru_theme.ogg
   ```

8. **Launch game** — prologue Kaoru entrance and grab moment already use `audio.bgm_kaoru_theme`.

### Optional: enable export automation

1. **System Settings → Privacy & Security → Accessibility**
2. Add **Terminal** and/or **Cursor**.
3. Run:

   ```bash
   osascript scripts/garageband_export_kaoru.applescript
   ```

   Then convert the exported AIFF as above.

---

## Automation reference (copy-paste)

```applescript
set midiPath to POSIX file "/Users/amanda.yazdani/Downloads/amanda/ryoko-owari/game/audio/bgm/kaoru_theme.mid"
set bandPath to POSIX file "/Users/amanda.yazdani/Downloads/amanda/ryoko-owari/game/audio/bgm/kaoru_theme.band"
tell application "GarageBand"
  activate
  open midiPath
  delay 2
  tell front document
    set tempo to 78
    set name to "Kaoru Theme"
    save in bandPath
  end tell
end tell
```

---

## Motif reference

Primary descent (guide spec): **A → F → E** (minor third + step), embedded in stepwise motion.

MIDI motifs in composer (**v3**):

- **MOTIF_A:** A4–G4–F4–E4–D4–C4–B3–A3 (pure lyrical descent)
- **MOTIF_B:** E4–D4–C4–B3–A3–G3–F3–E3 (deeper appraisal, all steps/minor 3rds)
- **MOTIF_C:** same as MOTIF_A (bar 8 of each loop phrase)

Intro bars 1–4: sparse melody (every other note). **Shakuhachi echo** follows played notes in phrase bars 1–4, one bar later. Taiko enters bar 6+ on beats 2/4. Full loop from bar 9.

---

## Related docs

- [garageband-bgm-guide.md](garageband-bgm-guide.md) — track specs and export workflow
- [toa-theme-garageband-session.md](toa-theme-garageband-session.md) — parallel workflow for Toa
- [audio-setup.md](audio-setup.md) — Ren'Py audio wiring
