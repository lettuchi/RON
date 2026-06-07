# 3D Character Specification — Kakita Toa & Kitsu Kaoru

**Purpose:** Canonical measurements, colors, outfit variants, and export targets for anyone building 3D models (Blender, Tripo, Meshy, VRChat, etc.) from the Ryoko Owari VN 2D art.

**Status:** This repo ships **2D sprites and CGs only**. There are no production rigged anime meshes in-tree. See `assets/3d/` for labeled low-poly **placeholders** and `scripts/3d_model_request_template.md` for an external image-to-3D workflow.

---

## Canonical 2D references (attach to every generation)

| Role | Path |
|------|------|
| Toa — witness / default outfit | `game/images/sprites/toa/toa-neutral.png` |
| Toa — Case 3.5 date furisode | `game/images/reference/case3_5-toa-date-lock.png` |
| Toa — date sprite set | `game/images/sprites/toa/date/toa-date-neutral.png` |
| Kaoru — default smirk (faces **right**) | `game/images/sprites/kaoru/kaoru-smirk.png` |
| Duo lighting / wardrobe gold standard | `game/images/cg/cg-case2-festival-kiss.png` |
| Case 3.5 duo (date outfits) | `game/images/cg/cg-case3_5-date-kaiseki-duo.png` |
| Painterly style anchor | `game/images/reference/style-painterly-reference.png` |

**Sprite staging (Ren'Py):** Toa faces **left**; Kaoru faces **right** — they converse across the dialog box. Preserve this yaw in any 3D staging used for VN parity tests.

---

## Proportions & measurements

Use **real-world cm** as the rig scale; 1 Blender unit = 1 m is recommended.

| | Kakita Toa | Kitsu Kaoru |
|---|------------|-------------|
| Height | 180 cm (5′11″) | 173 cm (5′8″) |
| Build | Adult woman; dancer’s grace; not child/moe proportions | Adult man; mid-thirties; lean magistrate |
| Head height ratio | ~1 : 7.5 (anime-leaning, not chibi) | ~1 : 7.5 |
| Eye line from floor | ~165 cm | ~158 cm |
| Shoulder width (approx.) | 38 cm | 44 cm |

**Hair volume (approx. bounding boxes for blocking):**

- **Toa:** White hair, shoulder-to-mid-back length when loose; witness outfit often down; date furisode uses **pinned updo + kanzashi** (add ~6 cm height).
- **Kaoru:** Brown, slicked back, **short ponytail** at nape; low profile above skull, tail ~15 cm.

---

## Color palette (hex)

Derived from VN dialogue colors, art-direction docs, and CG outfit locks. Sample from reference PNGs for final PBR albedo — these are **starting values**, not subsurface-skin truth.

### Shared

| Swatch | Hex | Use |
|--------|-----|-----|
| Grey eyes | `#8a9099` | Both characters |
| Skin (anime neutral) | `#f0ddd0` | Base skin tone; adjust in post to match 2D cel look |

### Kakita Toa

| Swatch | Hex | Use |
|--------|-----|-----|
| Hair | `#f5f5f5` | White hair |
| Eyelashes | `#f0f0f0` | Match hair |
| Dialogue UI | `#c0c0c0` | Ren'Py name color |
| Kosode (witness) | `#1a1a1a` | Black kimono body |
| Crane obi embroidery | `#d4af37` | Gold crane bird in flight on obi |
| Hakama (witness) | `#fafafa` | White pleated hakama |
| Furisode base (date) | `#141414` | Black spring furisode |
| Cherry blossom accent | `#ffb7c5` | Embroidery |
| Grape hyacinth accent | `#7b68a6` | Embroidery at hem |
| Rose-gold obi (date) | `#b8860b` | Heavy brocade musubi |
| Zori / geta wood | `#8b6914` | Footwear |

### Kitsu Kaoru

| Swatch | Hex | Use |
|--------|-----|-----|
| Hair | `#5c4033` | Brown, slicked |
| Dialogue UI | `#d4af37` | Ren'Py name color |
| Haori gold (festival / date lock) | `#c9a227` | Mustard-gold magistrate haori |
| Haori maroon base | `#6b1c2a` | Under-robe / trim |
| Gold leaf pattern | `#e6c200` | Brocade highlights |
| Dark kimono under-layer | `#2a1810` | Inner kosode |

---

## Outfit variants

### Toa — `work` (default witness)

- Black **kosode** with **standard sleeves** — **NOT furisode**, NOT long swinging sleeves.
- **Gold Kakita mon on obi:** crane bird **in flight** (spread wings, readable silhouette).
- White **hakama**, zori.
- White hair down or loosely styled; white eyelashes.
- Used across magistrate office, investigation, most of game (`characters.rpy` → `group outfit: work`).

### Toa — `date` (Case 3.5 interlude)

- Black **spring furisode** — cherry tree + grape hyacinth embroidery, petals on sleeves.
- **Rose-gold obi** brocade, trailing musubi.
- **Kanzashi** with bell-like tinkling (accessory mesh).
- Pinned updo; light rouge on lips/eyes per script.
- **No hakama** — full kimono layers, zori.
- Toggle in Ren'Py: `$ set_toa_outfit("date")` / `"work"`.
- Master lock: `game/images/reference/case3_5-toa-date-lock.png`.

### Kaoru — magistrate (all scenes)

- Opulent **gold/maroon magistrate robes**; gold leaf brocade.
- **Gold/mustard ochre haori** for festival and Case 3.5 date CG lock (match `cg-case2-festival-kiss.png`).
- Worn investigation catalog (prop — separate mesh).
- **NO oni mask, NO demon mask, NO face coverings, NO Kitsu spirit imagery** on character mesh.

---

## Orthographic reference views (recommended blocking)

When modeling in Blender, import the canonical PNGs as **front / side / back** image planes (scale to height above):

```
Front:  sprite PNG, character centered, feet on ground line
Side:   derive from CG or mirror sprite with ¾ note in doc
Back:   furisode obi trail (date) or hakama pleats (work) from CG refs
```

Suggested plane setup (Blender):

1. Empty at origin; child planes at Y = 0 (feet).
2. Front plane: +Y normal; Side: +X normal.
3. Scale plane height to character cm ÷ 100.

---

## Export targets

| Target | Format | Notes |
|--------|--------|-------|
| Blender editing | `.blend` | Master scene; armature + shape keys live here |
| Game / web / Godot / Ren'Py 3D tests | **glTF 2.0 binary (`.glb`)** | Preferred interchange |
| Unity | `.fbx` or `.glb` via Blender export | Humanoid avatar mapping |
| VRChat | `.fbx` + Unity SDK | Separate performance rank doc required |

**glTF 2.0 settings (Blender):**

- +Y up, apply transforms, include armature, export skinning, no Draco for VN toolchain simplicity.
- Textures: PNG, max 2K for body, 1K for hair cards if used.
- Name meshes: `Toa_Body`, `Toa_Hair`, `Toa_Kosode`, etc.

---

## Rig notes (VN / Blender / VR)

### Skeleton (minimum)

- **Humanoid biped:** spine ×3, neck, head, clavicle ×2, arm ×2 (upper/lower/hand), leg ×2 (upper/lower/foot), fingers optional (VN bust shots rarely need full hand FK).
- **Kimono deformation:** secondary bones or corrective shape keys for sleeve cuffs and obi knot; furisode needs **extra sleeve chain** (2–3 bones per long sleeve).
- **Hair:** bone chains or mesh strips with stiffness; Toa white volume vs Kaoru low ponytail.

### Ren'Py 3D (if ever used)

- Ren'Py 7/8 supports Model displayables and glTF via community patterns; this project is **2D layeredimage** today — 3D is for future experiments (menu, VR gallery, etc.), not shipped sprite replacement.
- Match **sprite facing:** Toa root yaw ≈ +15° to screen-left; Kaoru ≈ −15° to screen-right.

### Blend shapes (optional)

Map to existing expression names in `characters.rpy`:

- Toa: `neutral`, `happy`, `sad`, `angry`, `surprised`, `flustered`, `worried`, `thinking`, `determined`, `soft`, (+ date-only: `bashful`, `embarrassed`, `twitterpated`)
- Kaoru: `smirk`, `cold`, `charm`, `cruel`, `angry`, … (see `game/images/characters.rpy`)

---

## What exists in-repo today

| Asset | Path | Description |
|-------|------|-------------|
| Placeholder mannequins | `assets/3d/toa-placeholder.glb`, `assets/3d/kaoru-placeholder.glb` | Low-poly colored blocks; **not** anime meshes |
| Generator | `scripts/generate_3d_placeholders.py` | Regenerates placeholders (requires `trimesh`, `numpy`) |
| External pipeline doc | `scripts/3d_model_request_template.md` | Tripo / Meshy / Blender workflow |

---

## Realistic production path (outside this repo)

1. **Image-to-3D** (Tripo SR, Meshy, Rodin) using locked reference PNGs above — generate separate passes for body, hair, kimono if needed.
2. **Blender cleanup:** retopology to anime-friendly edge flow, UV unwrap, fix hands/feet.
3. **Outfit variants:** duplicate base body; model kosode vs furisode as alternate mesh groups or shape-key swap.
4. **Rig:** Rigify or custom humanoid; weight paint kimono with automatic weights + manual obi/sleeve fixes.
5. **Texture:** hand-paint or project from 2D refs; cel-shade material optional for VN-adjacent look.
6. **Export glTF 2.0** → validate in [glTF Viewer](https://gltf-viewer.donmccurdy.com/) or Blender re-import.

Estimated effort for **production-quality rigged anime duo:** skilled 3D artist, **40–120+ hours** depending on outfit count, hair method, and expression shape keys.
