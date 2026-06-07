# CG style prompt block (GenerateImage)

Copy-paste blocks for **every** Ryoko Owari CG, OP/ED still, background, and reference sheet generated via Cursor `GenerateImage`. Prevents drift into photorealistic / 3D / photographic output.

**Gold standard (match these):** `game/images/cg/cg-case2-festival-kiss.png`, `game/images/op/op-festival.png`

**NovelAI note:** `scripts/novelai_prompts.json` `_meta.style_tags` includes `semi-realistic` — that tag set is for NovelAI only. For GenerateImage, use the blocks below instead; do not copy NovelAI `style_tags` verbatim into GenerateImage prompts.

---

## Mandatory prefix (prepend to every prompt)

```
2D anime visual novel illustration, Hakuoki otome style, polished shoujo anime, painterly cel shading, clean colored linework, hand-painted anime illustration, NOT photorealistic, NOT 3D render, NOT photography, NOT hyperrealistic skin, NOT Unreal Engine, NOT octane render, Legend of the Five Rings Ryoko Owari corrupt canal city aesthetic, wide landscape 16:9 composition, no text, no watermark
```

---

## Mandatory suffix (append after scene description)

```
, anime CG event illustration, soft painterly shadows with readable cel steps, expressive anime eyes, simplified fabric folds, illustrated lantern glow not lens flare, mood: dark romantic otome visual novel
```

---

## Negative cues (append to prompt as “Avoid:” line, or weave into description)

```
Avoid: photorealistic, realistic photo, 3D render, CGI, Unreal Engine, octane, ray tracing, hyperrealistic skin pores, DSLR, bokeh photography, stock photo, lifelike, cinematic realism, plastic skin, airbrushed photograph, depth-of-field blur, volumetric fog realism, game engine screenshot, flat chibi, super deformed, moe child proportions, thick meme outlines, vector trace, western clothing, modern dress, oni mask, demon mask, furisode long swinging sleeves on Toa unless scene explicitly requires furisode, text, watermark, logo, signature
```

---

## Reference images (`reference_image_paths`)

**Always attach (in this order):**

| Priority | Path | Role |
|----------|------|------|
| 1 | `game/images/reference/style-painterly-reference.png` | Painterly mood / brush (regen when drifted) |
| 2 | `game/images/cg/cg-case2-festival-kiss.png` | Duo + lighting gold standard |
| 3 | `game/images/op/op-festival.png` | Festival duo gold standard |

**When Toa and/or Kaoru appear:**

| Character | Path |
|-----------|------|
| Kakita Toa | `game/images/sprites/toa/toa-neutral.png` |
| Kitsu Kaoru | `game/images/sprites/kaoru/kaoru-smirk.png` |

**Office / magistrate scenes:** also mention Emerald Magistrate jade sphere banner (kiku in gold-rimmed green orb) — not Kakita crane mon on wall hangings.

---

## Character anchors (embed in scene line)

**Toa:** white hair, grey eyes, white eyelashes, cheerful adult woman; default black kosode (standard sleeves, not furisode unless scene says furisode), gold crane bird obi embroidery, white hakama. Case 3.5 prep: black furisode with spring cherry/grape hyacinth, rose-gold obi when script calls furisode.

**Kaoru:** mid-thirties, brown hair slicked back short ponytail, grey eyes, opulent gold/maroon magistrate robes, no mask, faces slightly right in two-shots.

---

## Output settings

- **Size:** 1536×1024 landscape (state in prompt; resize with Pillow if tool returns another aspect)
- **Filename:** kebab-case `.png`; promote to `game/images/cg/`, `game/images/op/`, `game/images/ed/`, or `game/images/reference/`
- **Before overwrite:** copy prior file to `game/images/cg/versions/style-fix-2026-06-03/` (or matching subfolder mirror)

## In-game display

Story CGs are **1536×1024 (3:2)**. In Ren'Py they use the `fit_cg` transform (`ui_layout.rpy`): `fit "contain"` into 1280×720 so the **entire illustration** is visible, with black letterbox bars on the sides. Location backgrounds keep `fit_screen` (`fit "cover"`) to fill 16:9. The CG gallery viewer uses the same contain framing. Do not crop PNGs for framing — adjust display transforms only.

---

## Full template (copy-paste skeleton)

```
[PREFIX]

[SCENE: one paragraph — who, pose, location, lighting, emotion]

[CHARACTER ANCHORS if applicable]

[SUFFIX]

Avoid: [NEGATIVE CUES]
```

**Example (two-shot CG):**

```
2D anime visual novel illustration, Hakuoki otome style, polished shoujo anime, painterly cel shading, clean colored linework, hand-painted anime illustration, NOT photorealistic, NOT 3D render, NOT photography, NOT hyperrealistic skin, NOT Unreal Engine, NOT octane render, Legend of the Five Rings Ryoko Owari corrupt canal city aesthetic, wide landscape 16:9 composition, no text, no watermark

1girl 1boy, Kakita Toa white hair grey eyes black kosode gold crane obi, Kitsu Kaoru brown ponytail maroon gold magistrate robes, festival kiss on wooden balcony, warm lantern town below, soft fireworks in night sky, intimate tender otome romance, faces close

, anime CG event illustration, soft painterly shadows with readable cel steps, expressive anime eyes, simplified fabric folds, illustrated lantern glow not lens flare, mood: dark romantic otome visual novel

Avoid: photorealistic, 3D render, CGI, hyperrealistic skin, DSLR bokeh, lens flare realism, flat chibi, oni mask, text watermark
```

---

## Hand prompt lines (reduce extra/missing fingers)

Append to scene description when hands are prominent (grab, embrace, dance, grip):

```
, anatomically correct hands, five fingers each hand, natural hand pose, clearly defined fingers and knuckles, no extra fingers, no fused fingers, no malformed hands
```

Add to **Avoid:** line:

```
malformed hands, extra fingers, missing fingers, fused fingers, claw hands, mangled anatomy, too many hands
```

---

## Hand QA (MediaPipe)

Optional **advisory** post-gen check for visible hands. Anime stylization often confuses the detector — review warnings manually; use `--strict` only when you want CI-style hard fails.

**Install:**

```bash
pip install -r requirements-cg-qa.txt
```

**Usage (one-liner after saving a new CG):**

```bash
python scripts/check_cg_hands.py --path game/images/cg/<new-cg>.png
```

Batch all CGs, strict mode, or JSON output:

```bash
python scripts/check_cg_hands.py --path "game/images/cg/*.png"
python scripts/check_cg_hands.py --path game/images/cg/cg-choice-grab-rebuke.png --strict --min-confidence 0.6 --json
```

See `scripts/check_cg_hands.py` docstring for flags (`--strict`, `--expect-hands`, `--json-out`).

---

## Audit checklist (reject & regen if any apply)

- Looks like a photo, Unreal still, or 3D cinematic render
- No visible illustration linework; forms defined only by photo-like gradients
- Hyper-detailed skin pores, individual hair-strand realism, or plastic specular highlights
- Background busier than Hakuoki festival kiss CG (gold standard)
- Style reference `style-painterly-reference.png` itself looks photographic → regen reference first using gold-standard CGs only
- Malformed or extra-finger hands in a close-up pose → regen with hand prompt lines above; optionally run MediaPipe hand QA

---

## Related docs

- [.cursor/skills/vn-art-pipeline/SKILL.md](../.cursor/skills/vn-art-pipeline/SKILL.md) — Anti-drift section
- [novelai-image-pipeline.md](novelai-image-pipeline.md) — NovelAI Precise Reference (separate toolchain)
