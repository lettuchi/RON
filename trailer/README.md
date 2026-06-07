# Ryoko Owari — Cel-Shaded Trailer Pipeline

A ~90 s, 1920×1080 / 24 fps proof-of-concept trailer cut to the techno remix of the
opening song (`game/audio/bgm/opening_op.mp3`). It fuses three kinds of shot into one
piece: **procedural** Ken-Burns moves over existing stills, **hand-drawn cel** hero cuts
(3 keyframes, machine-inbetweened), and optional **AI-motion** clips from fal.ai. The
look is locked in [`style/style-bible.md`](style/style-bible.md), which extends
[`docs/cg-style-prompt-block.md`](../docs/cg-style-prompt-block.md).

Source of truth for the edit is [`shotlist.json`](shotlist.json) (timings, plates,
techniques, subtitles, name cards). Run everything from the **repo root**.

---

## Order of operations

```powershell
# 1. Audio bed  ->  trailer/audio/trailer_bed.m4a
#    OP song spine + ducked voice lines + SFX from trailer/audio_overlays.json
python scripts/build_audio_bed.py

# 2. Cel keyframes  ->  trailer/frames/*.png   (the hand-drawn hero cuts)
#    toa-fan-{1,2,3}, kaoru-turn-{1,2,3}, toa-dance-{1,2,3}
#    (generated per style/style-bible.md; see the vn-art-pipeline skill)

# 3. (OPTIONAL) AI motion  ->  trailer/clips/<shot_id>.mp4
#    Upgrade any hero/embrace shot from procedural/cel to real interpolated video
python scripts/generate_video_clip.py --list-presets
python scripts/generate_video_clip.py --preset toa_fan

# 4. Compose the trailer  ->  trailer/out/ryoko-owari-trailer-v1.mp4 + .webm
python scripts/build_trailer.py
```

Steps 1–2 are required; step 3 is the optional upgrade (below); step 4 produces the
final files. `build_trailer.py` and `build_audio_bed.py` are stdlib-only and shell out
to **ffmpeg/ffprobe 8.x**.

---

## Two-phase model: procedural now, fal.ai upgrade later

The trailer is designed to look complete **without spending a cent**, then improve in
place as you add real motion:

- **Phase 1 (free, default).** `build_trailer.py` renders every shot procedurally:
  Ken-Burns pan/zoom over each shot's `plate`, and for the hero cuts it
  machine-inbetweens the cel keyframes in `trailer/frames/`. No network, no cost.
- **Phase 2 (paid, optional).** For a hero shot you render a real image-to-video clip
  with `scripts/generate_video_clip.py` and drop it at `trailer/clips/<shot_id>.mp4`.
  On the next `build_trailer.py` run that shot is swapped for true AI motion.

`build_trailer.py` simply **looks for `trailer/clips/<shot_id>.mp4` and uses it if
present, otherwise falls back to the procedural/cel render** — so you can upgrade one
shot at a time and rerun, with no edits to the shotlist.

How `build_trailer.py` reads each shot (from `shotlist.json`):

| `technique`     | Source                                   | If the upgrade clip is missing            |
|-----------------|------------------------------------------|-------------------------------------------|
| `procedural`    | Ken-Burns move over `plate`              | n/a                                        |
| `handdrawn_cel` | inbetween the 3 `frames`                 | Ken-Burns over `fallback_plate`            |
| `ai_video`      | `trailer/clips/<shot_id>.mp4`            | Ken-Burns over the first frame / plate     |

It then applies the finishing pass to fuse all sources: ~5.5% letterbox, soft vignette,
the `warm_noir` grade, ~0.06 film grain, beat-synced transitions (`dissolve` default,
`fadewhite` on character reveals + the title, `fadered` on the red-string climax),
lower-third English subtitles and upper-third name cards, and muxes
`trailer/audio/trailer_bed.m4a`. Outputs land at `config.out_mp4` / `config.out_webm`
in `shotlist.json` (`trailer/out/ryoko-owari-trailer-v1.mp4` and `.webm`).

---

## fal.ai setup (only needed for Phase 2)

1. Sign up at <https://fal.ai> and create an API key at
   <https://fal.ai/dashboard/keys>. fal keys are formatted **`<key_id>:<key_secret>`**.
2. Copy `scripts/.env.example` to `scripts/.env` and set:

   ```
   FAL_KEY=<key_id>:<key_secret>
   ```

   `scripts/.env` is gitignored — never commit it. `generate_video_clip.py` loads it
   with the same `.env` loader as `scripts/generate_novelai_image.py`.
3. Verify offline (no network, no spend):

   ```powershell
   python scripts/generate_video_clip.py --list-presets
   python scripts/generate_video_clip.py --dry-run --preset toa_fan
   ```

**Rough cost.** Budget about **$10–40** to finish the trailer's hero clips including
retries. Image-to-video is billed per generated second; the default Kling model is a
few-dollars-per-clip tier, and you will usually re-roll a couple of shots to get clean
motion. Start with one preset, confirm the result, then do the rest. Dry-run is free and
prints the exact request JSON.

---

## Upgrading a shot to real AI video

`generate_video_clip.py` uses the fal **queue** REST API (stdlib `urllib` only): it
submits to `https://queue.fal.run/<model>`, polls the returned `status_url`, fetches the
`response_url`, and downloads the resulting MP4. Local start/end frames are uploaded to
fal storage (with a base64 `data:` URI fallback — the script logs which path it used).

Presets live in [`video_presets.json`](video_presets.json). Each maps a hero shot to its
keyframes, prompt, and output clip:

| `--preset`   | start → end frame                              | writes                         |
|--------------|------------------------------------------------|--------------------------------|
| `toa_fan`    | `frames/toa-fan-1.png` → `toa-fan-3.png`       | `clips/s04_toa_fan.mp4`        |
| `kaoru_turn` | `frames/kaoru-turn-1.png` → `kaoru-turn-3.png` | `clips/s07_kaoru_turn.mp4`     |
| `toa_dance`  | `frames/toa-dance-1.png` → `toa-dance-3.png`   | `clips/s15_toa_dance.mp4`      |
| `embrace`    | `game/images/cg/cg-canon-embrace.png` (subtle) | `clips/s11_embrace.mp4`        |

The default model `fal-ai/kling-video/v2/standard/image-to-video` interpolates
**start frame → end frame** (`image_url` + `tail_image_url`), so a hero cut's keyframe-1
morphs into keyframe-3 with true inbetween motion. The open-weights alternative
`fal-ai/wan-i2v` (single start frame) is also on fal — pass `--model fal-ai/wan-i2v
--no-end-image`.

Upgrade loop:

```powershell
# 1. Render the clip to its trailer/clips/<shot_id>.mp4 target
python scripts/generate_video_clip.py --preset kaoru_turn

# 2. Recompose: build_trailer.py auto-detects the new clip and swaps it in
python scripts/build_trailer.py
```

Handy flags (`--help` for all): `--dry-run`, `--list-presets`, `--prompt`, `--duration`
(default 5), `--start-image` / `--end-image`, `--no-end-image` (drop the tail frame),
`--model`, `--out` (default `trailer/clips/<preset>.mp4`), `--prefer-data-uri`. On HTTP
errors it explains 401 (bad/missing `FAL_KEY`), 402 (out of credits), 422 (bad params —
try `--no-end-image`), and 429 (rate limited).

---

## Watching the trailer in-game (Ren'Py)

[`game/trailer.rpy`](../game/trailer.rpy) adds a **"Watch Trailer"** entry that plays
`trailer/out/ryoko-owari-trailer-v1.webm` fullscreen via a Ren'Py `Movie` displayable.
It is skippable (click anywhere or press **Escape** → Main Menu) and auto-returns to the
menu when the ~90 s clip ends, mirroring the `opening_sequence` / image-song replays.

It is **non-invasive**:

- The render lives at `trailer/out/` (outside `game/`), so `trailer.rpy` appends the
  project base dir to `config.searchpath` instead of moving the file or editing engine
  files. (Prefer a webm: VP9/VP8 + Opus/Vorbis is the most compatible Ren'Py format.)
- Before the trailer is built, the menu entry shows a friendly "not rendered yet" notice
  instead of erroring.
- The **"Watch Trailer"** button is injected through a main-menu-only overlay screen
  (`config.overlay_screens`), so **`screens.rpy` is not edited**.

**Optional:** if you'd rather list it in the normal nav instead of the overlay, delete
the overlay block at the bottom of `game/trailer.rpy` and add this one line inside
`screen navigation():` in `game/screens.rpy`, in the `if main_menu:` branch:

```renpy
textbutton _("Watch Trailer") action Function(renpy.call_in_new_context, "trailer_play")
```

---

## Layout

```
trailer/
  README.md            # this file
  shotlist.json        # edit source of truth (timings, plates, techniques, subtitles)
  audio_overlays.json  # voice/SFX events mixed onto the OP song spine
  video_presets.json   # fal.ai image-to-video presets (Phase 2 upgrades)
  style/style-bible.md # the locked cel look
  frames/              # hand-drawn cel keyframes (toa-fan-*, kaoru-turn-*, toa-dance-*)
  clips/               # optional AI-motion clips: <shot_id>.mp4 (auto-picked by build)
  audio/               # trailer_bed.m4a (from build_audio_bed.py)
  out/                 # ryoko-owari-trailer-v1.mp4 / .webm (final render)

scripts/
  build_audio_bed.py      # step 1  (stdlib + ffmpeg)
  generate_video_clip.py  # step 3, optional  (stdlib urllib; fal.ai queue API)
  build_trailer.py        # step 4  (stdlib + ffmpeg)
```
