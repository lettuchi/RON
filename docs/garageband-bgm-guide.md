# GarageBand BGM guide — Ryoko Owari Nights

Actionable specs for composing background music in **GarageBand** and dropping exports into the Ren'Py project. Placeholders are procedural (`scripts/synthesize_bgm.py`); replace them with your own tracks when ready.

## Quick reference — file names

Drop finished exports into `game/audio/bgm/` using **exact** filenames (Ren'Py defines in `game/audio/music.rpy`):

| Track ID | Filename | When it plays |
|----------|----------|---------------|
| Main menu | `main_menu.ogg` | Title screen (`config.main_menu_music`) |
| Corridor | `corridor.ogg` | Opening corridor, verbal ending corridor |
| Office | `office.ogg` | Magistrate office dialogue |
| Street | `street.ogg` | Walkout ending — canal district exterior |
| Toa theme | `toa_theme.ogg` | Office dance / Toa performance beats |
| Kaoru theme | `kaoru_theme.ogg` | Kaoru entrance, grab moment, tension |
| Canon intimate | `canon_intimate.ogg` | Canon route fade / afterglow |

Ren'Py also accepts `.mp3` and `.wav`. If you export MP3, update the paths in `game/audio/music.rpy` (e.g. `"audio/bgm/toa_theme.mp3"`).

---

## GarageBand setup

1. **New project** → Empty Project → choose **Software Instrument** track.
2. Set project tempo and key in the LCD (top center) before recording.
3. **Project settings** (click the tempo/key area → Project settings):
   - Sample rate: **44.1 kHz** (matches Ren'Py defaults)
   - Resolution: 24-bit is fine; export will convert.
4. Enable the **Cycle / loop region** for your 32-bar loop while composing.

### Recommended instrument patches (GarageBand)

Search the library for these starting points:

| Role | Search terms | Notes |
|------|--------------|-------|
| Koto / pluck | "Koto", "Pipa", "Gu Zheng", "Plucked" | Toa theme, corridor plucks |
| Shamisen | "Shamisen", "Biwa" | Street, Toa accents |
| Strings | "String Ensemble", "Slow Strings", "Orchestral Strings" | Kaoru low bed, canon warmth |
| Taiko / drums | "Taiko", "Japanese Drum", "Frame Drum" | Kaoru pulse, street rhythm |
| Ambient / pad | "Ambient Pad", "Dark Pad", "Atmosphere" | Corridor mystery, office tension |
| Shō / breath | "Sho", "Flute Pad", "Air Pad" | Office lantern mood (subtle) |

GarageBand's **World** and **Orchestral** categories are the best starting points. Layer 2–4 tracks per piece; avoid busy mixes that compete with voice acting.

---

## Track specs

### Toa theme — `toa_theme.ogg`

**Character:** Kakita Toa — bright Crane dancer; warmth, stubborn cheer, movement and grace.

| Parameter | Value |
|-----------|-------|
| Key | **D major** or **G major** (modal/bright) |
| Tempo | **90–110 BPM** |
| Mood | Energetic, elegant, not frantic |
| Lead | Koto or shamisen plucks — ascending motifs, dance-like 8th-note patterns |
| Support | Light strings (high register), optional soft bells / woodblock |
| Avoid | Heavy taiko, minor-key doom, vocals |

**Motif idea:** 8-note phrase that rises then resolves (e.g. D–E–F#–A–B–A–F#–D). Repeat with variation every 8 bars.

**Wired in:** `prologue_office_dance` (dance CG and performance menu).

---

### Kaoru theme — `kaoru_theme.ogg`

**Character:** Kitsu Kaoru — Emerald Magistrate; controlled menace, imperial formality.

| Parameter | Value |
|-----------|-------|
| Key | **A minor** or **D minor** |
| Tempo | **70–85 BPM** |
| Mood | Tension, authority — **not horror** |
| Lead | Low celli / contrabass sustains |
| Rhythm | Soft taiko on beats 1 and 3 (quiet, felt not loud) |
| Accent | Occasional koto or biwa single notes — sparse |
| Avoid | Jump scares, dissonant clusters, battle drums |

**Motif idea:** Slow descending minor third (A→F→E) with a held fifth underneath.

**Wired in:** Kaoru first appearance, `prologue_grab_moment`, chair tension buildup.

---

### Location beds

#### Corridor — `corridor.ogg`

- **Mood:** Mysterious, endless noble-quarter hallway; lantern light.
- **Tempo:** ~80 BPM or no obvious pulse (ambient).
- **Texture:** Sparse koto harmonics, soft pad, distant wind/chime one-shots.
- **Wired in:** Prologue start, verbal ending corridor.

#### Office — `office.ogg`

- **Mood:** Magistrate tension — ink, cedar, paper, lamplight.
- **Tempo:** ~75 BPM.
- **Texture:** Low string drone, very subtle paper-like noise (field recording or filtered noise), minimal melody.
- **Wired in:** Entering magistrate office through dance aftermath.

#### Street — `street.ogg`

- **Mood:** Ryoko Owari canal district / night market — honest, outside the noble quarter.
- **Tempo:** ~88–95 BPM.
- **Texture:** Shamisen riff, light taiko, warm night ambience.
- **Wired in:** Walkout ending exterior scene.

#### Main menu — `main_menu.ogg`

- Blend corridor mystery with hints of Toa (bright pluck) and Kaoru (low string) — the game's "title card" identity.
- ~85 BPM, loopable, slightly more polished than raw location beds.

#### Canon intimate — `canon_intimate.ogg`

- **Mood:** Warm aftermath; tender, implied intimacy (PG-13).
- **Tempo:** ~70–72 BPM.
- **Key:** D major or soft modal major.
- **Texture:** Slow koto, warm pads, no percussion-heavy taiko.
- **Wired in:** `prologue_canon_ending` (fade to black through signing).

---

## Loop structure (all tracks)

Compose for seamless looping:

```
[Intro 8 bars — optional, can be trimmed on export]
[Loop body 32 bars — this is what repeats in-game]
```

1. Set cycle region to **32 bars** (or 40 bars if you keep an 8-bar intro that fades in once).
2. Ensure bar 33 connects musically to bar 1 (match chord, avoid reverb tail at loop point).
3. **Cut reverb / delay tails** at the loop boundary — bounce dry, add reverb in moderation.
4. Target length: **60–120 seconds** total (Ren'Py loops automatically with `loop`).

---

## Export from GarageBand → Ren'Py

### Step-by-step

1. **Mix down:** Share → Export Song to Disk…
2. **Format:** MP3 or AAC at **44.1 kHz** (GarageBand default). MP3 is fine for development.
3. **Quality:** Higher quality (192 kbps+ for MP3).
4. **Convert to OGG (recommended for release builds):**

   ```bash
   # If you install ffmpeg (brew install ffmpeg):
   ffmpeg -i ~/Desktop/toa_theme.mp3 -c:a libvorbis -q:a 4 game/audio/bgm/toa_theme.ogg
   ```

   Or export WAV from GarageBand and convert:

   ```bash
   ffmpeg -i toa_theme.wav -c:a libvorbis -q:a 4 game/audio/bgm/toa_theme.ogg
   ```

5. **Copy** the file to:

   ```
   ryoko-owari/game/audio/bgm/{track_id}.ogg
   ```

6. **Launch the game** — no script changes needed if the filename matches `game/audio/music.rpy`.

### Replace placeholders checklist

- [ ] Export all seven tracks with exact filenames above
- [ ] Drop into `game/audio/bgm/` (overwrite procedural placeholders)
- [ ] Launch game → Main Menu should play your `main_menu.ogg`
- [ ] Play prologue → verify corridor → Kaoru → office → dance → canon/walkout transitions
- [ ] Adjust volumes in `prologue.rpy` (`volume 0.xx` on `play music` lines) if needed

---

## Alternative generators (optional)

| Method | Command | Notes |
|--------|---------|-------|
| Procedural placeholders | `.venv-sprite/bin/python scripts/synthesize_bgm.py` | No API; numpy/scipy/soundfile |
| ElevenLabs Music API | `scripts/.venv/bin/python scripts/generate_bgm.py` | Paid plan required; prompts in `scripts/bgm_manifest.json` |

Do **not** commit `.env` or paste API keys into docs.

---

## Ren'Py wiring reference

Defines (`game/audio/music.rpy`):

```renpy
define audio.bgm_toa_theme = "audio/bgm/toa_theme.ogg"
```

Usage pattern:

```renpy
play music audio.bgm_corridor fadein 2.5 loop volume 0.65
play music audio.bgm_kaoru_theme fadein 1.5 loop volume 0.6
stop music fadeout 2.5
```

Main menu (`game/options.rpy`):

```renpy
define config.main_menu_music = audio.bgm_main_menu
```

Mixer: `config.has_music = True` — players adjust Music volume in Preferences.

See also: [audio-setup.md](audio-setup.md) for SFX and voice.
