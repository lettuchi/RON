# Modern AU character references

**Purpose:** Stop AU CG drift into L5R kimono. Canon sprites (`toa-neutral.png`, `kaoru-smirk.png`) are **face and hair only** for Modern AU — body outfit comes from the AU reference sheets below.

**Design context:** [au-modern-wrong-floor-design.md](au-modern-wrong-floor-design.md)

---

## Reference images (mandatory for AU CGs)

| Character | Full / 3/4 | Turnaround (2×2) | Waist-up (closeups) |
|-----------|------------|------------------|---------------------|
| **Kakita Toa** | `docs/art-references/au-modern/toa-au-modern-tracksuit-reference.png` | `docs/art-references/au-modern/toa-au-modern-tracksuit-turnaround-reference.png` | `docs/art-references/au-modern/toa-au-modern-tracksuit-waistup-reference.png` |
| **Kitsu Kaoru** | `docs/art-references/au-modern/kaoru-au-modern-suit-reference.png` | `docs/art-references/au-modern/kaoru-au-modern-suit-turnaround-reference.png` | `docs/art-references/au-modern/kaoru-au-modern-suit-waistup-reference.png` |

---

## Mandatory attire (Modern AU)

### Kakita Toa

- **Default:** Black zip tracksuit (jacket + pants) with **gold side stripes** and **gold crane logo on chest** (Crane Conservatory / sponsorship motif — not obi).
- **Alt (scene-appropriate):** Smart casual with crane motif on jacket or tee; raincoat over tracksuit; studio leotard + warm-up jacket (still contemporary, never kosode).
- **Build:** Contemporary ballet / dance graduate, 5'11" / 180 cm.
- **Face/hair:** White hair, grey eyes, white eyelashes — match canon sprite face only.
- **Never:** Kimono, kosode, furisode, hakama, obi, zori, tabi.

### Kitsu Kaoru

- **Default:** Charcoal grey **deputy director suit** (jacket + trousers), white dress shirt, dark tie; optional clipboard, municipal ID lanyard, stamp.
- **Alt:** Suit without jacket (rolled sleeves, vest); raincoat over suit; break-room casual = shirt sleeves only (still western office wear).
- **Build:** 5'8", mid-thirties, brown hair slicked back (short ponytail).
- **Face/hair:** Grey eyes, dry smirk — match canon sprite face only.
- **Never:** Magistrate robes, maroon/gold kimono, hakama, oni mask, L5R props on body.

---

## Negative prompt block (AU only)

Append to every Modern AU CG prompt (GenerateImage or NovelAI):

```
kimono, kosode, furisode, hakama, obi, zori, tabi, geta, magistrate robes, maroon gold robes, crane obi embroidery, tatami room unless script explicitly modernized, shoji unless scene is AU office glass, Emerald Magistrate, jade sphere banner, L5R period dress, feudal Japan costume, samurai armor
```

For GenerateImage, also keep canon anti-drift negatives from [cg-style-prompt-block.md](cg-style-prompt-block.md) but **remove** `western clothing, modern dress` from that block when generating AU scenes.

---

## GenerateImage — always attach these paths

**Order matters.** Use AU outfit refs for body; canon sprites optional for face lock only.

```
reference_image_paths:
  1. docs/art-references/au-modern/toa-au-modern-tracksuit-reference.png   # when Toa appears
  2. docs/art-references/au-modern/kaoru-au-modern-suit-reference.png      # when Kaoru appears
  3. game/images/reference/style-painterly-reference.png                   # style mood
  4. game/images/cg/cg-case2-festival-kiss.png                             # duo lighting gold standard (composition only; ignore canon outfits)
```

**Closeups / bust shots:** swap full-body AU refs for waist-up variants:

- `docs/art-references/au-modern/toa-au-modern-tracksuit-waistup-reference.png`
- `docs/art-references/au-modern/kaoru-au-modern-suit-waistup-reference.png`

**Do not** use `game/images/sprites/toa/toa-neutral.png` or `kaoru-smirk.png` as the **only** character ref for AU CGs — they will pull kosode/obi/robes. If attached at all, treat as face/hair anchor only alongside AU outfit refs above.

---

## Prompt anchors (embed in scene line)

**Toa (AU):** white hair, grey eyes, white eyelashes, cheerful adult woman, black zip tracksuit gold stripes gold crane logo on chest, contemporary dancer build 5'11", port city rain mood, municipal arts sponsorship applicant.

**Kaoru (AU):** mid-thirties, brown hair slicked back short ponytail, grey eyes, charcoal grey deputy director suit white shirt dark tie, dry bureaucratic smirk, clipboard or stamp optional, Ryoko Port tower municipal licensing.

**Setting:** 21st-century port city — glass tower lobbies, badge readers, Zoom monitors, mirror studios, service elevators, harbor rain. No L5R terms on props.

---

## Copy-paste workflow

1. Read [scripts/au_modern_cg_prompt_block.txt](../scripts/au_modern_cg_prompt_block.txt) — prefix, character tags, negative block.
2. Attach AU reference PNGs per table above.
3. Add scene-specific line (parking lot, elevator, contract desk, etc.) from [au-modern-wrong-floor-design.md](au-modern-wrong-floor-design.md) CG list.
4. Run GenerateImage; if kimono appears, regen with **only** AU refs (drop canon sprites) or lower sprite ref weight.
5. Optional hand QA: `python scripts/check_cg_hands.py --path game/images/cg/<new>.png`
6. Save to `game/images/cg/cg-au-modern-*.png`; register in `game/images/cgs-au-modern.rpy` or `cgs-au-modern-case1.rpy`.

---

## Proof regen (drift-prone CG)

**Recommended test:** `cg-au-modern-studio-audition.png` — full-body dance + suit witness; historically kimono-prone.

**Steps:**

1. Prompt: studio mirror, barre, Toa in tracksuit port de bras, Kaoru in charcoal suit with clipboard at mirror edge, rain on high windows.
2. Refs: both full-body AU sheets + style-painterly-reference + festival kiss (composition).
3. Negatives: AU block above + no kimono/kosode/obi.
4. Output: `game/images/cg/versions/au-modern-ref-test-YYYY-MM-DD/cg-au-modern-studio-audition.png`
5. Compare to prior `cg-au-modern-studio-audition.png`; promote only if attire correct.

*(Not run in this pass — workflow documented for next regen batch.)*

---

## Related files

| Path | Role |
|------|------|
| `scripts/au_modern_cg_prompt_block.txt` | Copy-paste tags for GenerateImage / NovelAI |
| `scripts/novelai_prompts.json` → `_meta.au_modern_*` | NovelAI AU character tags and ref paths |
| `.cursor/skills/vn-art-pipeline/SKILL.md` | Modern AU section pointer |
| `docs/cg-closeup-intimate-2026-06-04.md` | Closeup pass — use AU waist-up refs for AU scenes |
