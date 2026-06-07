# Scene layering — backgrounds vs CGs vs sprites

Ryoko Owari Nights uses three visual layers on the **scene** / **master** stack:

| Layer | When | Full-body sprites | Bust in textbox |
|-------|------|-------------------|-----------------|
| **Location bg** (`bg corridor`, `bg magistrate_office`, `bg street_exterior`) | Default dialogue in a place | Show with `at left` / `at right` | Auto via `SideImage()` |
| **Event CG** (`cg corridor_lost`, `cg permit_desk`, …) | Key story beats | **Small** — `cg_left` / `cg_right` (~0.38 zoom) | Auto via `SideImage()` |

## Prologue pattern

```renpy
# Location + sprites (corridor opening, office scenes)
scene bg corridor with fade
show toa worried at right
show kaoru smirk at left

# Key beat — CG carries the scene
$ show_cg_scene("corridor_lost")
show toa worried
toa "Dialogue shows bust in textbox and a small sprite on the CG."

show toa determined
toa "Sprites use cg_left / cg_right so they flank the illustration."

# Bust-only (no visible full-body) when needed:
$ set_expression("toa", "determined")
toa "Offstage sprite; bust still updates."

# Return to location
scene bg magistrate_office with dissolve
show kaoru smirk at left
show toa neutral at right
```

## Background assets

| Tag | File | Use |
|-----|------|-----|
| `bg corridor` | `game/images/bg/corridor.png` | Noble-quarter hallway |
| `bg magistrate_hall` | same as corridor | Alias |
| `bg magistrate_office` | `game/images/bg/magistrate_office.png` | Emerald Magistrate office |
| `bg street_exterior` | `game/images/bg/street_exterior.png` | Ryoko Owari streets / canal district |

All backgrounds use `fit_screen` (1280×720 cover) — see `ui_layout.rpy`.

## Sprites

- **30 expression PNGs** — 10 Toa, 20 Kaoru — RGBA with alpha (`rembg` u2net).
- Regenerate: `scripts/make_sprites_transparent.sh`
- Sprites must composite on bgs without white boxes; verify with `game/test_screenshot.rpy`.

## Helpers (`game/scene_layering.rpy`)

- `hide_stage_sprites()` — hide Toa/Kaoru full-body
- `show_cg_sprite(char, expr)` — small sprite on CG (`cg_left` / `cg_right`)
- `set_expression(char, expr)` — bust-only (offstage sprite) during CG scenes
- `show_cg_scene(cg_tag, transition=None)` — show CG (preferred over raw `scene cg`)
- `restore_location_sprites(bg, kaoru_expr, toa_expr)` — return from CG to bg + both sprites
- `cg_safe_show` — wraps `renpy.show`; maps `show toa`/`show kaoru` to CG transforms while `cg_active`
- `config.scene_callbacks` — clears `cg_active` when master is re-scened (non-CG entry)
