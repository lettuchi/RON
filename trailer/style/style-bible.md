# Cel-Shaded Trailer — Style Bible

The look for the Ryoko Owari proof-of-concept trailer. This locks the cel aesthetic so the
generated hand-drawn cuts (technique `handdrawn_cel`), the AI-motion cuts (`ai_video`), and the
Ken-Burns stills (`procedural`) all read as one piece. It extends, and must stay consistent with,
[docs/cg-style-prompt-block.md](../../docs/cg-style-prompt-block.md).

## North star

Animated Hakuoki-style otome OP. Think the opening of a dark romance anime: painterly cel shading,
clean colored linework, lantern-lit canal noir, red-string-of-fate motif, beat-synced cuts on the
techno remix of `opening_op.mp3`. Polished, not photoreal; moody, not garish.

## Cel-look targets (all techniques must match)

- Linework: clean, confident colored line; medium weight; no thick meme outlines, no vector trace.
- Shading: 2-3 readable cel tone bands per form (base / shadow / occasional rim). Soft painterly
  edge on the shadow step, not airbrushed photo gradients.
- Palette: lantern reds/golds against wet blue-black canal night; warm key + cool fill. The grade
  pass (`warm_noir`) pushes amber highlights and teal-ish shadows; keep source plates neutral so the
  grade lands consistently.
- Eyes: large, expressive, anime; crisp catchlights.
- Lighting: illustrated lantern glow, NOT lens flare; rim light to separate hair from dark BGs.
- Motion-blur/DOF: none baked into plates (the grade + grain pass handles atmosphere).

## Frame-rate intent (hand-drawn cuts)

- Timeline 24 fps. Hero cel cuts are authored as 3 key drawings and machine-inbetweened, so they
  read as animation "on 2s/3s" (8-12 effective drawings/sec) rather than a slideshow. Keep
  consecutive keyframes close in framing/lighting so the inbetween morph stays clean.

## Character anchors (keep identical across a cut's keyframes)

- Toa: white hair, grey eyes, white eyelashes; cheerful adult woman; black kosode (standard sleeves,
  NOT furisode), gold crane-bird obi, white hakama. Charm point = warm sweetness.
- Kaoru: mid-thirties, brown hair slicked back (short ponytail), grey eyes; opulent gold/maroon
  magistrate robes; NO mask, NO oni/demon imagery; faces slightly right. Tone = cold, predatory charm.

## Hero cut choreography (the `handdrawn_cel` shots)

- `s04_toa_fan` — Toa raises and snaps open a folding fan, chin lifting, eyes rising to camera.
  Keyframes: (1) fan closed, gaze down/aside; (2) fan half-open, arm rising; (3) fan fully open
  across the lower face, eyes up and bright. Lantern backlight, rain bokeh behind.
- `s07_kaoru_turn` — Kaoru turns from a cold three-quarter-away to a slow predatory smirk at camera.
  Keyframes: (1) looking off, jaw set, cold; (2) mid-turn, eyes cutting toward us; (3) full smirk,
  candle/lantern uplight, magistrate robes catching gold.
- `s15_toa_dance` — Toa mid crane dance, sleeve/obi trailing. Keyframes: (1) arms gathered low; (2)
  arms sweeping up and open; (3) extended arabesque-like reach, fan or sleeve trailing. Silhouetted
  against bridge lanterns; keep it readable, not busy.

## Prompt skeleton for generated keyframes

Use the mandatory prefix/suffix/negative from [cg-style-prompt-block.md](../../docs/cg-style-prompt-block.md).
Attach references in this order: `game/images/reference/style-painterly-reference.png`, the matching
character sprite (`game/images/sprites/toa/toa-neutral.png` or `.../kaoru/kaoru-smirk.png`), and — for
frames 2 and 3 of a cut — the previously generated frame of the same cut, so pose continuity holds.

## Compositing pass (build_trailer.py)

- Letterbox: thin cinematic bars (~5.5% top/bottom).
- Vignette: soft edge darkening.
- Grade `warm_noir`: lift amber in highlights, cool the shadows, gentle S-curve contrast.
- Grain: light film grain (~0.06) over everything to fuse AI/cel/still sources into one texture.
- Cuts: beat-synced; `dissolve` default, `fadewhite` on character reveals and the title, `fadered`
  on the red-string climax beats.
- Lower-third English lyric subtitles + upper-third character name cards mirror the in-game OP
  (`game/opening.rpy`).
