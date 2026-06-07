# ElevenLabs instrumental BGM — prompts (no generation)

Prompt library for **looping instrumental themes** used in *Ryoko Owari Nights*. Do **not** call the API from this doc; when ready, use `scripts/generate_music.py` (extend `TRACKS`) or paste prompts into ElevenLabs Music UI / Suno / GarageBand.

**Status (generated 2026-06-04 via `scripts/generate_music.py`, log `scripts/music_generation_2026-06-03.log`):** Eleven Music **creator** tier; probe OK; no 402/403. Seven prompts initially hit ToS (`bad_prompt`); retried with sanitized prompts (no L5R/Hakuoki/corrupt/coercive wording). **`game/audio/music.rpy` wired 2026-06-04:** all case/optional beds have `define audio.bgm_*` lines; obvious `play music` swaps applied in case scripts (see **Wired in Ren'Py** below). `bgm_office` → `office.mp3` (legacy `office.ogg` still on disk, file-locked during regen). Shipped instrumental files under `game/audio/bgm/`:

- `bad_end_brothel.mp3`
- `bad_end_punishment.mp3`
- `bad_end_rain.mp3`
- `bad_ending.mp3`
- `canon_intimate.mp3`
- `canon_intimate.ogg`
- `case1_barge.mp3`
- `case2_festival.mp3`
- `case3_5_date.mp3`
- `case3_fabric.mp3`
- `case4_5_kobune.mp3`
- `case4_dock.mp3`
- `case5_tease.mp3`
- `corridor.mp3`
- `corridor.ogg`
- `kaoru_theme_new.mp3`
- `office.mp3`
- `street.mp3`
- `street.ogg`
- `toa_theme_new.mp3`

Duplicate `kaoru_theme_new_regen.mp3` can be deleted after verifying `kaoru_theme_new.mp3`.

### Wired in Ren'Py (`music.rpy` + scripts)

| Define | File | Script swap (if any) |
|--------|------|----------------------|
| `bgm_case1_barge` | `case1_barge.mp3` | `case1_investigation.rpy` — `case1_investigation_canal`, `case1_barge_start` |
| `bgm_case2_festival` | `case2_festival.mp3` | `case2_festival.rpy` — festival interlude opening |
| `bgm_case3_fabric` | `case3_fabric.mp3` | `case3_investigation.rpy` — fabric shop + accident climax |
| `bgm_case3_5_date` | `case3_5_date.mp3` | `case3_5_date_interlude.rpy` — Tear Drop arrival |
| `bgm_case4_dock` | `case4_dock.mp3` | `case4_investigation.rpy` — dock raid / confrontation / swordfight |
| `bgm_case4_5_kobune` | `case4_5_kobune.mp3` | `case4_5_boat.rpy` — canal night CG |
| `bgm_case5_tease` | `case5_tease.mp3` | `case4_5_boat.rpy` — `case5_stub_tease` |
| `bgm_bad_end_rain` | `bad_end_rain.mp3` | `epilogue_rain_gameover.rpy` — `gameover_rain` |
| `bgm_bad_end_brothel` | `bad_end_brothel.mp3` | `epilogue_rain_gameover.rpy` — `prologue_bad_end_brothel` |
| `bgm_bad_end_punishment` | `bad_end_punishment.mp3` | `case_endings.rpy` — `case1_bad_end_kaoru_punishment` |

**Still on legacy beds** (swap `play music` manually where desired): Case 1 departure / Plum quarter (`bgm_street`); Case 2 festival bridge exit (`bgm_street`); Case 3.5 lantern walk (`bgm_street`); Case 2/3/4 investigations office briefings (`bgm_office`); generic `gameover_*` except rain/brothel/punishment (`bgm_bad_ending`); `corridor`/`street`/`canon_intimate` core loops unchanged.

---

## Which ElevenLabs API?

| API | Endpoint | Use for this project |
|-----|----------|----------------------|
| **Eleven Music** | `POST https://api.elevenlabs.io/v1/music?output_format=mp3_44100_128` | **Instrumental BGM** (`prompt` + `force_instrumental: true`) and **vocal songs** (`composition_plan`; no `force_instrumental`) |
| **Text-to-Speech** | `/v1/text-to-speech/...` | Dialogue only (`scripts/generate_voice.py`) — **not** BGM |
| **Sound Effects** | Sound generation API (`scripts/generate_sfx.py`) | Short SFX (door, stamp, rain hit) — **not** 60–90 s themes |

**Instrumental themes:** Eleven Music **can** produce full instrumental loops. The project already uses it for `toa_theme_new.mp3`, `kaoru_theme_new.mp3`, `bad_ending.mp3` (`scripts/generate_music.py`). **Paid subscription required** (402/403 if not).

**Request shape (instrumental):**

```json
{
  "prompt": "<full prompt text>",
  "music_length_ms": 75000,
  "model_id": "music_v1",
  "force_instrumental": true
}
```

**Limits / caveats:**

- Typical generation length in scripts: **5 s (probe)** to **~95 s** per request; Ren'Py loops in-game.
- Loop seams are **not guaranteed perfect** — audition loop points; trim in a DAW if needed.
- Export as **MP3 44.1 kHz** (`mp3_44100_128`) or convert to OGG for release (`ffmpeg`).
- `force_instrumental` is **only** valid with `prompt`, not with `composition_plan`.
- Vocal OP/ED/image songs use separate scripts (`generate_music.py --menu`, `generate_ending_song.py`, etc.) — **out of scope** below.

**If Music API quality or quota blocks you:** GarageBand (`docs/garageband-bgm-guide.md`), **Suno/Udio** (paste prompts below), or **stock** (Artlist, Epidemic) with “Japanese cinematic / no vocals” filters. Keep the same filenames in `game/audio/music.rpy`.

**Generation command (when approved):**

```bash
# Probe access (5 s, no files)
python scripts/generate_music.py --test

# After adding tracks to TRACKS in generate_music.py:
python scripts/generate_music.py --ids corridor,office
```

---

## Current Ren'Py wiring (instrumental loops)

| Track ID | File (`music.rpy`) | Primary use |
|----------|-------------------|-------------|
| `bgm_corridor` | `corridor.ogg` | Prologue opening corridor; verbal ending corridor |
| `bgm_office` | `office.mp3` | Magistrate office, investigations (Case 5 stub uses `bgm_case5_tease`) |
| `bgm_street` | `street.ogg` | Canal district exteriors, festival approach, dock tension |
| `bgm_toa_theme` | `toa_theme_new.mp3` | Prologue dance; Case 1 Kaoru beats |
| `bgm_kaoru_theme` | `kaoru_theme_new.mp3` | Prologue Kaoru entrance; Case 1 companion |
| `bgm_canon_intimate` | `canon_intimate.ogg` | Canon encounters, case endings, dates, boat intimacy |
| `bgm_bad_ending` | `bad_ending.mp3` | Most game-over labels; prologue refuse (after brothel stinger) |
| `bgm_case1_barge` | `case1_barge.mp3` | Case 1 canal + barge finale |
| `bgm_case2_festival` | `case2_festival.mp3` | Case 2 festival interlude |
| `bgm_case3_fabric` | `case3_fabric.mp3` | Case 3 fabric shop / accident |
| `bgm_case3_5_date` | `case3_5_date.mp3` | Case 3.5 Tear Drop date |
| `bgm_case4_dock` | `case4_dock.mp3` | Case 4 lower dock / fight |
| `bgm_case4_5_kobune` | `case4_5_kobune.mp3` | Case 4.5 kobune night |
| `bgm_case5_tease` | `case5_tease.mp3` | Case 5 stub tease |
| `bgm_bad_end_rain` | `bad_end_rain.mp3` | `gameover_rain` flee |
| `bgm_bad_end_brothel` | `bad_end_brothel.mp3` | `prologue_bad_end_brothel` |
| `bgm_bad_end_punishment` | `bad_end_punishment.mp3` | `case1_bad_end_kaoru_punishment` |

**Not listed below (vocal / one-shot):** `bgm_main_menu`, `bgm_opening`, `bgm_ending`, `bgm_kaoru_kenri`, `bgm_toa_image`, `bgm_duet`.

---

## Track prompts

**Convention:** Duration = Ren'Py loop target. **Mood keywords** are comma-separated tags for search/UI. **Negative / avoid** = paste as second paragraph in Eleven UI or append to prompt.

---

### `bgm_corridor` — Prologue / noble-quarter hallway

| Field | Value |
|-------|--------|
| **Use in game** | `prologue.rpy` start; corridor return before bad end |
| **Duration target** | **75 s** loop-friendly |
| **Mood keywords** | mysterious, lantern-lit, L5R noble quarter, Hakuoki VN, ambient, no pulse |

**ElevenLabs prompt:**

Instrumental Japanese cinematic ambient bed for a feudal-Japan visual novel corridor scene, Hakuoki / Legend of the Five Rings Ryoko Owari aesthetic. Endless magistrate-quarter hallway at night: distant paper lanterns, hushed nobility, ink and cedar in the air. Sparse koto harmonics and a soft breathy shō-like pad, occasional single woodblock or wind-chime color, very slow harmonic motion around 80 BPM or almost pulseless. Mysterious but not scary — anticipation before power meets the dancer. No vocals, no lyrics, no modern drums, no synth EDM, no battle percussion. Seamless loop-friendly: steady texture, no big ending crash, last bar flows back to the first.

**Negative / avoid:** horror stingers, jump scares, heavy taiko, trap beats, piano ballad grief, English vocals, cinematic trailer braams.

---

### `bgm_office` — Magistrate office / Case investigations hub

| Field | Value |
|-------|--------|
| **Use in game** | Prologue office; `case1_*`, `case2_investigation`, `case3_*`, `case4_*`, `case4_5_boat` briefings; `case5_stub_tease` |
| **Duration target** | **80 s** loop-friendly |
| **Mood keywords** | magistrate tension, cedar ink lamplight, Emerald office, otome power imbalance |

**ElevenLabs prompt:**

Instrumental Japanese cinematic tension bed for an Emerald Magistrate's office in a corrupt canal city, Hakuoki / Legend of the Five Rings visual novel. Low string drone in a minor modal color, subtle felt taiko heartbeat far in the mix, sparse biwa or koto single-note accents like a seal waiting to fall. Mood: ink, cedar, stacked permits, lamplight on lacquer — authority and paperwork, not combat. Tempo around 75 BPM, restrained and elegant. No vocals, no lyrics, no busy melody, no horror clusters, no modern kit. Loop-friendly: continuous unease, gentle crossfade at loop point, no fade-to-silence ending.

**Negative / avoid:** romantic love theme, festival energy, full battle drums, comedic pizzicato, synth pads, nightclub bass.

---

### `bgm_street` — Ryoko Owari canal district / exteriors

| Field | Value |
|-------|--------|
| **Use in game** | Case 1 canal walks; Case 2 festival approach; Case 3–4 exteriors; `gameover_rain` (rain flee); dock approach |
| **Duration target** | **85 s** loop-friendly |
| **Mood keywords** | canal night market, Scorpion city, shamisen, honest grime, investigation walk |

**ElevenLabs prompt:**

Instrumental Japanese cinematic street theme for a corrupt canal city at night, Hakuoki / Legend of the Five Rings Ryoko Owari. Warm shamisen or biwa riff over light hand percussion and soft taiko on 1 and 3, distant lantern ambience, 88–92 BPM — walking pace, worldly and slightly dangerous but not battle. Scorpion trade-city honesty: fish, copper, rain on stone implied in the mix texture, not literal sound effects. No vocals, no lyrics, no EDM four-on-the-floor, no heroic fanfare. Loop-friendly: repeating 8-bar street motif, steady energy, ending connects to opening motif.

**Negative / avoid:** magistrate office drone only, intimate bedroom softness, game-over piano tragedy, modern city pop.

---

### `bgm_toa_theme` — Kakita Toa (Crane dancer)

| Field | Value |
|-------|--------|
| **Use in game** | `prologue.rpy` office dance; `case1_investigation.rpy` / `case1_companion.rpy` Kaoru beats |
| **Duration target** | **90 s** loop-friendly |
| **Mood keywords** | bright Crane grace, koto flute, hopeful bittersweet, performance |

**ElevenLabs prompt:** *(matches `scripts/generate_music.py` — regen or refine here)*

Instrumental Japanese cinematic theme for a graceful former Crane-clan dancer in a feudal-Japan visual novel, Hakuoki / Legend of the Five Rings aesthetic. Bright, warm and elegant with a hopeful rising melody carrying a gentle bittersweet undercurrent. Lead koto and bamboo flute trade an ascending, dance-like phrase (rises then resolves), supported by light high strings, soft shamisen plucks, and delicate woodblock / hand percussion. Key of D major, tempo around 100 BPM, lively but never frantic, refined and graceful. No vocals, no lyrics, no drums kit, no synths. Seamless loop-friendly: steady feel throughout, no big fade-out, ending that flows back to the opening.

**Negative / avoid:** dark magistrate menace, horror, heavy taiko battle, idol pop vocals, trap beats.

---

### `bgm_kaoru_theme` — Kitsu Kaoru (Emerald Magistrate)

| Field | Value |
|-------|--------|
| **Use in game** | Prologue Kaoru entrance / grab; Case 1 companion tension |
| **Duration target** | **90 s** loop-friendly |
| **Mood keywords** | controlled menace, seductive authority, minor key, shakuhachi, otome LI |

**ElevenLabs prompt:** *(matches `scripts/generate_music.py`)*

Instrumental Japanese cinematic theme for a dangerous, refined Emerald Magistrate in a feudal-Japan visual novel, Hakuoki / Legend of the Five Rings aesthetic. Dark, controlled and seductive: coercive imperial power with slow-burning menace and restraint, tense but elegant, not horror. Low sustained cello and contrabass carry a slow descending minor phrase, with sparse, felt taiko hits and a lonely shakuhachi flute answering in call-and-response. Sparse biwa / koto single-note accents. Minor key (A minor), tempo around 78 BPM, deliberate and weighty. No vocals, no lyrics, no jump scares, no dissonant clusters, no battle drums. Seamless loop-friendly: steady, no big fade-out, ending that returns smoothly to the opening.

**Negative / avoid:** cute comedy, bright festival, game-over grief piano, explicit battle climax.

---

### `bgm_canon_intimate` — Canon route / romance aftermath

| Field | Value |
|-------|--------|
| **Use in game** | `prologue_canon_encounter.rpy`; case good endings; Case 2 festival intimacy; Case 3–4 rescue beats; Case 3.5 date; Case 4.5 boat |
| **Duration target** | **75 s** loop-friendly |
| **Mood keywords** | tender aftermath, PG-13 intimacy, warm koto, D major, otome |

**ElevenLabs prompt:**

Instrumental Japanese cinematic romantic aftermath bed for a feudal-Japan otome visual novel, Hakuoki / Legend of the Five Rings. Warm, tender, implied intimacy without explicit sensuality: slow koto melody and soft string pads in D major or gentle modal major, 70–72 BPM, breathing room like paper screens and shared tea. Bittersweet undercurrent — two people who should not trust each other still choosing closeness. No vocals, no lyrics, no heavy percussion, no erotic R&B, no modern piano pop ballad clichés. Loop-friendly: soft continuous arc, loop point on a sustained chord, no dramatic stop.

**Negative / avoid:** magistrate threat motif, festival crowd energy, horror, battle drums, nightclub bass.

---

### `bgm_case1_waterline` — Case 1 investigation / barge & canal *(proposed)*

| Field | Value |
|-------|--------|
| **Use in game** | `case1_investigation.rpy` — canal + barge (`bgm_case1_barge`); other Case 1 exteriors may still use `bgm_street` |
| **Ren'Py name** | `audio.bgm_case1_barge` → `case1_barge.mp3` |
| **Duration target** | **80 s** loop-friendly |
| **Mood keywords** | opium canal, barge manifest, Scorpion grey, investigation noir |

**ElevenLabs prompt:**

Instrumental Japanese cinematic noir investigation theme for a smuggler's canal and river barge at night, Legend of the Five Rings Ryoko Owari corrupt trade city. Low pulsing strings, muted shamisen ostinato, occasional wooden boat creak texture very subtle in the mix, rain-ready harmonic minor color. Mood: manifest lines, Scorpion paint, witness pride before the water — suspense not combat. 82 BPM, loop-friendly, no vocals, no lyrics, no modern synth bass, no battle taiko rolls. Seamless loop for visual novel investigation dialogue.

**Negative / avoid:** bright festival, office paperwork drone only, romantic canon warmth, jump-scare horror.

---

### `bgm_case2_festival` — Case 2 festival night *(proposed)*

| Field | Value |
|-------|--------|
| **Use in game** | `case2_festival.rpy` opening (`bgm_case2_festival`); hill intimacy still `bgm_canon_intimate` |
| **Duration target** | **85 s** loop-friendly |
| **Mood keywords** | matsuri lanterns, yatai, dancers, celebration hiding knives |

**ElevenLabs prompt:**

Instrumental Japanese festival night theme for a feudal canal-city matsuri, Hakuoki otome visual novel, Legend of the Five Rings Ryoko Owari. Lively but refined: taiko festival pulse softened for dialogue, shamisen and fue motifs, paper-lantern warmth in the harmony, 95 BPM feel without overwhelming voice acting. Undercurrent of danger — celebration as cover for Scorpion business. No vocals, no lyrics, no EDM drop, no arcade chiptune. Loop-friendly: repeating festival hook every 8 bars, steady energy.

**Negative / avoid:** empty street loneliness, magistrate office drone, tragic game-over piano, explicit battle music.

---

### `bgm_case3_silk_room` — Case 3 fabric shop / bolt room tension *(proposed)*

| Field | Value |
|-------|--------|
| **Use in game** | `case3_investigation.rpy` — fabric shop + accident (`bgm_case3_fabric`); rescue still `bgm_canon_intimate` |
| **Duration target** | **80 s** loop-friendly |
| **Mood keywords** | silk bolts, claustrophobic shop, witness trap, tense rescue |

**ElevenLabs prompt:**

Instrumental Japanese cinematic suspense for a cramped fabric shop and bolt room in a corrupt city, Hakuoki / L5R visual novel. Close-in texture: plucked koto in tight repeating pattern, low cello pedal, rare sharp biwa accents like scissors — claustrophobic, witness-in-danger, not slasher horror. 78 BPM, minor key, loop-friendly for long dialogue under threat. No vocals, no lyrics, no screaming strings, no modern thriller pulses.

**Negative / avoid:** outdoor canal walk theme, tender romance bed, festival joy, full swordfight climax.

---

### `bgm_case3_5_date` — Case 3.5 Tear Drop inn date *(proposed)*

| Field | Value |
|-------|--------|
| **Use in game** | `case3_5_date_interlude.rpy` — Tear Drop arrival (`bgm_case3_5_date`); lantern walk may still use `bgm_street` |
| **Duration target** | **75 s** loop-friendly |
| **Mood keywords** | private inn, biwa thread, candlelight date, otome romance |

**ElevenLabs prompt:**

Instrumental Japanese cinematic date-night bed for a private inn with hidden biwa music through shoji, feudal-Japan otome visual novel, Ryoko Owari. Intimate and slightly nervous: soft koto, distant biwa phrase like music through a wall, warm shakuhachi echo, gentle hand percussion like tea service, 68–74 BPM. Romance with stakes — magistrate and witness alone, not public festival. No vocals, no lyrics, no club beats, no comedic slapstick. Loop-friendly, tender continuous mood.

**Negative / avoid:** magistrate menace theme, crowd festival, game-over grief, explicit sensual R&B.

---

### `bgm_case4_dock` — Case 4 lower dock / swordfight *(proposed)*

| Field | Value |
|-------|--------|
| **Use in game** | `case4_investigation.rpy` — dock raid through swordfight (`bgm_case4_dock`); `gameover_case4_slayn` still `bgm_bad_ending` |
| **Duration target** | **70 s** loop-friendly (or **25 s** stinger variant for game-over only — see note) |
| **Mood keywords** | rain pier, blade tension, dock arithmetic, noir action |

**ElevenLabs prompt:**

Instrumental Japanese cinematic action-tension bed for a rainy lower dock and imminent sword confrontation, Legend of the Five Rings Ryoko Owari, Hakuoki-style visual novel. Driving shamisen and low taiko in **restrained** pulses — tension for dialogue and choice menus, not a full anime battle track. Harmonic minor, 100–108 BPM feel, rain-heavy atmosphere in the mix. No vocals, no lyrics, no Hollywood trailer horns, no EDM. Loop-friendly for investigation; if used for game-over, accept a shorter 20–30 s generate and loop once in Ren'Py.

**Negative / avoid:** tender canon intimacy, festival celebration, office paperwork drone, long tragic piano elegy.

---

### `bgm_case4_5_kobune` — Case 4.5 kobune boat *(proposed)*

| Field | Value |
|-------|--------|
| **Use in game** | `case4_5_boat.rpy` — canal night (`bgm_case4_5_kobune`); post-intimacy beats may still use `bgm_canon_intimate` |
| **Duration target** | **75 s** loop-friendly |
| **Mood keywords** | rocking hull, river night, intimate danger, private water |

**ElevenLabs prompt:**

Instrumental Japanese cinematic bed for a small kobune fishing boat at night on a canal, feudal-Japan otome visual novel. Gentle hull-rocking pulse in low strings, water-like koto harmonics, intimate warmth mixed with danger — two people alone on water, magistrate and witness. 72 BPM, minor-to-modal color shift, not horror. No vocals, no lyrics, no heavy battle taiko, no modern boat engine SFX dominating. Loop-friendly for long boat scenes.

**Negative / avoid:** public street festival, open dock battle drive, brothel tragedy piano, office drone.

---

### `bgm_bad_ending` — Generic game over

| Field | Value |
|-------|--------|
| **Use in game** | All `gameover_*` and `case1_bad_end_*` labels; prologue refuse punishment tone |
| **Duration target** | **95 s** loop-friendly (or stop before loop on `stop music fadeout`) |
| **Mood keywords** | game over, grief, rain-soaked canal city, resignation, piano |

**ElevenLabs prompt:** *(matches `scripts/generate_music.py`)*

Instrumental tragic, rain-soaked and lonely cinematic theme for the somber 'game over' bad ending of a feudal-Japan visual novel set in a corrupt canal city, Hakuoki / Legend of the Five Rings aesthetic. Mournful and slow: a fragile solo piano melody over aching, sustained strings, as the dark city swallows the last of the light. Sparse, spacious and desolate, with distant soft shakuhachi and the faint feeling of falling rain. Deep minor key, very slow tempo around 60 BPM, grief and resignation, cinematic and intimate. No vocals, no lyrics, no percussion beat, no synths. Loop-friendly: gentle and continuous, no abrupt cut, ending that drifts back toward the opening.

**Negative / avoid:** hope, battle energy, romantic warmth, jump scares, triumphant anime chorus.

---

### `bgm_bad_ending_rain` — Rain flee / exile tone *(optional stinger)*

| Field | Value |
|-------|--------|
| **Use in game** | `gameover_rain` (`bgm_bad_end_rain`) |
| **Duration target** | **20–30 s** stinger or **60 s** soft loop |
| **Mood keywords** | downpour, alone in canal, pride breaking, blue rain |

**ElevenLabs prompt:**

Instrumental short Japanese cinematic cue: heavy rain on stone and canal water, lonely runner in a corrupt city at night, Hakuoki tragedy. Sparse piano drops like rain, cold string pad, no percussion grid, 55 BPM, 20–30 seconds of emotional collapse that can loop quietly under narration. No vocals, no lyrics, no thunder cliché hits, no horror screams.

**Negative / avoid:** festival shamisen, office tension, romantic warmth, battle drums.

---

### `bgm_bad_ending_brothel` — Implied trafficking fade *(optional)*

| Field | Value |
|-------|--------|
| **Use in game** | `prologue_bad_end_brothel` (`bgm_bad_end_brothel`) |
| **Duration target** | **25 s** stinger → hand off to generic bad end |
| **Mood keywords** | lamplight ends, horror-tragedy, hollow, no graphic |

**ElevenLabs prompt:**

Instrumental Japanese cinematic tragedy stinger for an implied off-screen fate, feudal visual novel bad end, extremely restrained horror-tragedy without gore. Single descending piano phrase, detuned koto harmonic, airless string cluster resolving to emptiness, 50 BPM, 25 seconds, no vocals, no lyrics, no scream sound effects, no modern horror jump sting. Suitable for fade-to-black narration.

**Negative / avoid:** sensual romance, festival energy, heroic hope, explicit violence foley.

---

### `bgm_bad_ending_punishment` — Case 1 office punishment *(optional)*

| Field | Value |
|-------|--------|
| **Use in game** | `case1_bad_end_kaoru_punishment` (`bgm_bad_end_punishment`) |
| **Duration target** | **30 s** tense loop or **60 s** under CG sequence |
| **Mood keywords** | cedar office, magistrate power, coercive, shoji sealed |

**ElevenLabs prompt:**

Instrumental Japanese cinematic dread bed for a sealed magistrate office, power imbalance bad end, Hakuoki / L5R otome — coercive authority, not slasher gore. Low cello ostinato, single taiko heartbeats, sparse biwa, 65 BPM, claustrophobic. No vocals, no lyrics, no screaming, no explicit impact SFX. Loop-friendly under long CG narration.

**Negative / avoid:** romantic canon theme, outdoor rain runner, festival, comedy.

---

### `bgm_case5_tease` — Case 5 stub / pleasure-quarter seal *(proposed)*

| Field | Value |
|-------|--------|
| **Use in game** | `case5_stub_tease` (`bgm_case5_tease`) |
| **Duration target** | **70 s** loop-friendly |
| **Mood keywords** | Case Five tease, missing seal, pleasure quarter, sequel hook |

**ElevenLabs prompt:**

Instrumental Japanese cinematic mystery hook for an unfinished investigation — missing pleasure-quarter seal, feudal magistrate visual novel, Ryoko Owari corrupt city. Office tension meets distant shamisen from the quarter: low strings, ink-and-incense mood, a single ascending koto question motif like a file line not yet written, 76 BPM. Hope and danger balanced — sequel tease, not resolution. No vocals, no lyrics. Loop-friendly.

**Negative / avoid:** full festival, full game-over elegy, tender post-intimacy bed, battle climax.

---

## Implementation checklist (after audio exists)

1. ~~Export to `game/audio/bgm/` with filenames matching `define` lines in `game/audio/music.rpy`.~~ **Done (2026-06-04).**
2. ~~Wire obvious `play music` swaps in case scripts.~~ **Done** — see **Wired in Ren'Py** above; remaining `bgm_street` / `bgm_office` / `bgm_bad_ending` lines: swap manually where a dedicated bed helps.
3. Run game → verify fadein/loop volumes (`volume 0.42–0.7` in case scripts).
4. Extend `scripts/generate_music.py` `TRACKS` dict with ids → filename → prompt → `length_ms` for batch regen.
5. Do **not** commit `scripts/.env`.

---

## Track count

| Category | Count |
|----------|------:|
| Core beds (`corridor`, `office`, `street`, `canon_intimate`) | 4 |
| Character themes (`toa`, `kaoru`) | 2 |
| Case-specific proposed | 6 |
| Bad end (`generic` + 3 optional) | 4 |
| Case 5 tease proposed | 1 |
| **Total prompts in this doc** | **17** |

*Vocal tracks (menu, OP, ED, image songs, duet) use `composition_plan` scripts — not counted.*
