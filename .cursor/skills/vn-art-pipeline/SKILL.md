---
name: vn-art-pipeline
description: Generates and organizes visual novel art for the Ryoko Owari L5R otome Ren'Py project using GenerateImage, reference sheets, and Ren'Py asset conventions. Use when creating character sprites, CGs, backgrounds, placeholders, or prompt templates for Kakita Toa, Kitsu Kaoru, or Ryoko Owari scenes.
---

# VN Art Pipeline — Ryoko Owari

Personal artistic otome VN. **Hakuoki aesthetic** + **Legend of the Five Rings 5e** (Ryoko Owari). GenerateImage produces **placeholders and concept art**, not final production sprite sheets.

## When to use GenerateImage

Invoke `GenerateImage` when the user asks for:
- Backgrounds, sprites, CGs, UI mockups, mood boards
- Placeholder art for Ren'Py scripting

**Always:**
1. Attach **reference images** when generating Toa or Kaoru (paths below)
2. Save with descriptive `filename` (kebab-case, `.png`)
3. Default output: workspace `assets/` folder (Cursor may use project assets path)

**Do not** use GenerateImage for data charts, diagrams, or tables.

## Reference images (canonical)

| Character | Path |
|-----------|------|
| Kakita Toa (canonical sprite) | `game/images/sprites/toa/toa-neutral.png` |
| Kitsu Kaoru (canonical sprite) | `game/images/sprites/kaoru/kaoru-smirk.png` |

Use these in `reference_image_paths` for every **canon** (L5R) character generation.

### Modern AU (Wrong Floor, Case 1)

For **Modern AU** CGs, do **not** rely on sprites alone (they wear kimono/robes). Attach outfit refs first, then sprites for face/hair:

| Character | AU outfit ref (full) | AU outfit ref (waist-up) |
|-----------|----------------------|--------------------------|
| Toa | `docs/art-references/au-modern/toa-au-modern-tracksuit-reference.png` | `docs/art-references/au-modern/toa-au-modern-tracksuit-waistup-reference.png` |
| Kaoru | `docs/art-references/au-modern/kaoru-au-modern-suit-reference.png` | `docs/art-references/au-modern/kaoru-au-modern-suit-waistup-reference.png` |

Full rules, negatives, and workflow: [docs/au-modern-character-references.md](../../../docs/au-modern-character-references.md). Copy-paste tags: `scripts/au_modern_cg_prompt_block.txt`.

> **Note (Windows migration):** the original Mac design sheets (Toa Discord screenshot, Kaoru concept art) were not included in this export. The in-project sprites above are now the canonical visual references. If you locate the original sheets, drop them in `reference/` and update this table.

## Art direction

**Style:** Polished shoujo anime visual novel (Hakuoki). Cinematic lighting, clean linework, painterly backgrounds. Bishounen men, expressive eyes, ornate period dress.

**Setting:** Ryoko Owari — corrupt trade city, canals, lanterns, rain, opium undertones, Scorpion influence. Not generic fantasy Japan.

**Supernatural tone (A–B):** Mostly human grime; occasional wrongness (charms, haunted districts, spiritual unease). Do not turn every scene paranormal.

## Character specs (prompt anchors)

### Kakita Toa — protagonist
- Honest, cheerful, direct; white hair, grey eyes, 5'11" / 180 cm
- **White eyelashes** (match hair)
- Face: **bright, energetic, cheerful** — lively eyes, warm open smile; innocent sweetness but adult and womanly; sensual elegance subtle — sweetness is the charm point
- Outfit: black **kosode** kimono (standard sleeves — **NOT furisode**, NOT long swinging sleeves), **gold Kakita mon on obi — must read as a crane bird in flight** (spread wings, visible bird silhouette in embroidery), white hakama, zori
- **Office/CG consistency:** Same base outfit across all magistrate-office CGs (black kosode + gold crane obi + white hakama). Obi may loosen for dance/tension scenes but sleeves stay kosode length unless deliberately slipped (both sleeves must remain intact and intentional)
- **Render style:** Match Kaoru reference art — Hakuoki painterly polish, not flat design-sheet cel
- Personality in expressions: warm smile, flustered blush, stubborn determination
- Context: Crane dancer, live-in companion / art patronage with Kaoru; snacks as comfort

### Kitsu Kaoru — primary dark route LI
- Mid-thirties, brown hair slicked back (short ponytail), grey eyes, 5'8"
- Opulent gold/maroon magistrate robes, gold leaf patterns; carries worn investigation catalog
- **Sprite pose: waist-up, facing slightly RIGHT** (Toa faces left — they converse across dialog box)
- **NO oni mask, NO demon mask, NO face coverings, NO Kitsu spirit imagery on sprites**
- **Render style:** Hakuoki painterly polish (match Toa v3 / Kaoru concept art)
- Expression range: smirk, cold appraisal, performative charm, open cruelty + extremes (furious, contempt, vicious, ravenous, threatening, sadistic)
- Route tone: power imbalance, coercion, branching submission/resistance/takedown

## Asset naming

```
assets/
  bg_<location>_<variant>.png       # backgrounds
  toa_<expression>_<scene>.png      # Toa sprites/CGs
  kaoru_<expression>_<scene>.png    # Kaoru sprites/CGs
  cg_<chapter>_<beat>.png           # full event CGs
```

**Expressions (sprites):** `neutral`, `happy`, `sad`, `angry`, `surprised`, `flustered`, `worried`, `thinking`, `determined`, `soft`

**Toa sprite set path:** `assets/sprites/toa/toa-<expression>.png` (see `README.md` and `renpy-images.rpy` in that folder)

**Kaoru sprite set path:** `assets/sprites/kaoru/kaoru-<expression>.png` — default `smirk`, **faces RIGHT**. No oni masks. Standard 14 + extreme 6: `furious`, `contempt`, `vicious`, `ravenous`, `threatening`, `sadistic`. Regen reference: `kaoru-smirk-v2.png`

**Backgrounds (Milestone B):** magistrate office, permit desk, Ryoko Owari street, geisha district alley, canal at night

### Emerald Magistrate office — wall hanging mon

The magistrate office background (`ryoko-owari-magistrate-office-bg.png`) includes a **dark blue vertical banner** on the left wall. Its emblem is the **Emerald Magistrate badge of office** — NOT a crane, NOT a generic clan mon.

**L5R 5e canon:** Emerald Magistrates carry a **jade sphere** as badge of office. In TCG/fan art the symbol is often rendered as a **gold-rimmed jade-green orb/sphere** containing a **sixteen-petal imperial chrysanthemum (kiku)** — the imperial law-enforcement seal.

**Prompt anchor for blue wall hanging:**
```
dark blue vertical banner on wall, large circular emblem: gold-rimmed jade-green sphere with golden imperial chrysanthemum (kiku) inside — Emerald Magistrate badge, NOT crane, NOT Kakita mon
```

Apply this consistently in every magistrate-office CG and background regen.

## Ren'Py layout (when game project exists)

**Project path:** `C:\Users\Amanda\Developer\ryoko-owari\`

```
ryoko-owari/
  game/
    images/
      backgrounds.rpy
      characters.rpy
      bg/           # backgrounds
      sprites/toa/
      sprites/kaoru/
    script.rpy
    stats.rpy
```

Copy finalized assets from cursor `assets/` into `game/images/` subfolders. Character wiring lives in `game/images/characters.rpy`.

**Target resolutions:**
- Backgrounds: 1920×1080 (16:9)
- Sprites: ~800–1200 px tall, character centered, simple background or white (chroma-key in post if needed)
- CGs: 1920×1080 or 1280×720

## Prompt template

```
Anime otome visual novel [sprite|background|CG], Hakuoki-style polished shoujo art.
[CHARACTER or LOCATION description from specs above].
[Expression/pose/mood]. Legend of the Five Rings Ryoko Owari aesthetic.
[For sprites: upper or full body, plain background, no text]
[For backgrounds: wide 16:9, no characters, cinematic lighting]
```

## Anti-drift (photorealistic / 3D)

GenerateImage often drifts toward **photorealistic, 3D-render, or photographic** output. Before every CG, OP/ED still, or reference regen:

1. Read **[docs/cg-style-prompt-block.md](../../../docs/cg-style-prompt-block.md)** and paste the **mandatory prefix + suffix + negative cues** into the prompt.
2. Set `reference_image_paths` to **style + gold-standard CGs + sprites** (see that doc — not sprites alone).
3. Compare output to `game/images/cg/cg-case2-festival-kiss.png` and `game/images/op/op-festival.png`. If it reads like a photo or game-engine still, regen; back up failures under `game/images/cg/versions/style-fix-YYYY-MM-DD/`.

Do **not** reuse NovelAI `_meta.style_tags` (`semi-realistic`, etc.) verbatim in GenerateImage prompts.

## Limitations

- GenerateImage = single static PNG; not layered PSD, not multi-expression sprite sheets
- Cross-image consistency requires reference images + repeated prompt anchors
- Final Hakuoki-quality art may come from external tools or hand-drawn assets
- Label generated files as placeholders in commit messages unless user promotes them

## Hand QA (MediaPipe, optional)

After GenerateImage saves a CG (especially grab, embrace, dance, or grip scenes):

1. Install once: `pip install -r requirements-cg-qa.txt`
2. Run: `python scripts/check_cg_hands.py --path <new_png>`
3. Review the human-readable report (default **advisory** — exit 0 with warnings only).
4. If `--strict` fails or warnings look real (0 hands on a wrist-grab, >2 phantom hands, low confidence): re-prompt with hand lines from [docs/cg-style-prompt-block.md](../../../docs/cg-style-prompt-block.md) and regen.

Do **not** auto-reject solely on MediaPipe warnings for anime art — the detector is a sanity check, not ground truth.

## Workflow checklist

1. Read user request (character, scene, expression)
2. Load this skill + attach correct reference image(s)
3. GenerateImage with full prompt from template (+ hand prompt lines when hands are prominent)
4. Run `python scripts/check_cg_hands.py --path <new_png>` on CG output; review warnings
5. Report saved path under `assets/`
6. If Ren'Py project exists: offer to copy into `game/images/` and wire `show` statements
