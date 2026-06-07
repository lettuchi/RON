# External 3D Model Request Template — Toa & Kaoru

Use this when commissioning or generating models via **Tripo**, **Meshy**, **Rodin**, or manual **Blender** work. Copy sections into tool prompts or artist briefs.

Full measurements and hex colors: [`docs/3d-character-spec-toa-kaoru.md`](../docs/3d-character-spec-toa-kaoru.md).

---

## Locked reference images (always attach)

Upload **all three** for Toa; **two** for Kaoru-only requests:

| File | Why |
|------|-----|
| `game/images/sprites/toa/toa-neutral.png` | Toa witness outfit, face, hair, proportions |
| `game/images/sprites/kaoru/kaoru-smirk.png` | Kaoru default pose, **faces right**, gold robes |
| `game/images/reference/case3_5-toa-date-lock.png` | Toa date furisode + Kaoru gold haori duo lock |

Optional duo / lighting refs:

- `game/images/cg/cg-case2-festival-kiss.png`
- `game/images/cg/cg-case3_5-date-kaiseki-duo.png`

---

## Prompt pack — Kakita Toa (witness / work outfit)

```
Anime-style adult woman, visual novel protagonist, Legend of the Five Rings Crane clan dancer.
White hair, grey eyes, white eyelashes, cheerful mature face (not childlike).
Height 180 cm, slender dancer build, anime proportions (head 1:7.5 body).

Outfit: black kosode kimono with STANDARD sleeves (not furisode, not long swinging sleeves),
gold crane bird embroidery on obi (crane in flight, spread wings),
white hakama pleats, zori sandals.

Style reference: Hakuoki otome visual novel — painterly anime, NOT photorealistic, NOT western clothing.
Standing neutral pose, arms relaxed, facing slightly left.
Clean topology-friendly silhouette for game/VN use.
```

**Negative:** furisode, long swinging sleeves, photorealistic skin, 3D render look, chibi, oni mask, modern clothes, text, watermark.

---

## Prompt pack — Kakita Toa (date / furisode variant)

```
Same character as above (white hair, grey eyes, 180 cm adult woman).

Outfit: black spring furisode kimono with cherry blossom and grape hyacinth embroidery,
rose-gold obi brocade with trailing musubi, formal kanzashi hairpins,
pinned updo hairstyle, light lip rouge.

NOT witness kosode, NOT gold crane obi, NOT white hakama.
Audience pose ( seated or standing formal ), not dance performance pose.
Hakuoki anime visual novel style.
```

**Reference lock:** `game/images/reference/case3_5-toa-date-lock.png`

---

## Prompt pack — Kitsu Kaoru

```
Anime-style adult man, mid-thirties, visual novel love interest, Emerald Magistrate.
Brown hair slicked back with short ponytail at nape, grey eyes.
Height 173 cm (5'8"), lean build, bishounen anime face.

Outfit: opulent gold and maroon magistrate robes, gold leaf brocade patterns,
mustard-gold haori (Case 3.5 / festival scenes), dark kimono under-layer.
Optional prop: worn investigation catalog book.

Facing slightly RIGHT. Smirk expression default.
NO oni mask, NO demon mask, NO face covering, NO fox spirit imagery.
Hakuoki otome anime style, NOT photorealistic.
```

**Negative:** mask, photorealistic, chibi, modern suit, text, watermark.

---

## Tool-specific notes

### Tripo / Meshy (image-to-3D)

1. Upload `toa-neutral.png` or `kaoru-smirk.png` as primary image.
2. Enable **character / humanoid** mode if available.
3. Generate mesh → download `.glb` or `.fbx`.
4. Expect **cleanup required:** fingers, hair, kimono folds, obi knot.
5. Run a **second pass** for date furisode using `case3_5-toa-date-lock.png` (crop to Toa) — do not rely on one mesh for both outfits.

### Blender (manual pipeline)

1. Import reference PNGs as image planes (see spec doc orthographic section).
2. Block mesh to 180 cm / 173 cm scale.
3. Retopo → UV → texture project from sprites.
4. Rigify meta-rig → generate → weight paint (extra attention: sleeves, obi, hakama pleats).
5. Export glTF 2.0 binary → `assets/3d/toa.glb` (replace placeholders when ready).

### Validation checklist

- [ ] Height matches spec within 2 cm
- [ ] Toa witness: kosode sleeves (not furisode)
- [ ] Toa date: furisode + rose-gold obi (separate asset or variant)
- [ ] Kaoru: no mask; ponytail readable from back
- [ ] glTF opens in viewer without errors
- [ ] Optional: 8–12 expression shape keys named per `characters.rpy`

---

## Regenerate in-repo placeholders

Low-poly mannequins (not anime meshes):

```bash
pip install trimesh numpy scipy
python scripts/generate_3d_placeholders.py
```

Output: `assets/3d/toa-placeholder.glb`, `assets/3d/kaoru-placeholder.glb`
