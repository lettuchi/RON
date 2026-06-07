# Otome UI layout, Ryoko Owari Nights
#
# Conventions:
#   • Backgrounds: fit_screen (1280×720 cover): full scene behind dialogue.
#   • CG illustrations: fit_cg (1280×720 contain): full 1536×1024 frame, letterboxed.
#   • Full-body sprites: show with `at left` (Kaoru) or `at right` (Toa) on location bgs.
#     scene_layering.rpy auto-applies those defaults when `at` is omitted after a scene clear.
#     On CG scenes, sprites use `cg_left` / `cg_right` (~0.38 zoom) via scene_layering.rpy.
#     `$ set_expression(...)` keeps sprites offstage for bust-only updates when needed.
#   • Bust portraits: `side toa` / `side kaoru` images (Crop from full sprites)
#     appear in the say-screen textbox via SideImage() when a character speaks.
#   • Stage facing: Kaoru on left faces right; Toa on right faces left (toward center).
#
# Asset gap: busts are programmatic crops of full-body PNGs. Dedicated bust art can
# replace side layeredimages later without changing the say screen.

define SPRITE_STAGE_ZOOM = 0.54
define SPRITE_LEFT_XALIGN = 0.22
define SPRITE_RIGHT_XALIGN = 0.78
# Full-body sprites: yanchor 1.0 at screen bottom; negative yoffset lifts feet
# slightly above the textbox top (~200px). -210 floated too high; 0 sat too low.
define SPRITE_STAGE_YOFFSET = -100

define CG_SPRITE_ZOOM = 0.32
define CG_SPRITE_LEFT_XALIGN = 0.12
define CG_SPRITE_RIGHT_XALIGN = 0.88
define CG_SPRITE_YOFFSET = -65

init -10 python:
    # Bust crops from 1536×1024 full-body sprites (Crop x, y, w, h).
    # Measured padded face bbox union (scripts/verify_bust_crops.py, 2026-05-30):
    #   Toa  (faces left):  x578–1020, y1–590  across 10 exprs → 601² @ 168/601
    #   Kaoru (faces right): x183–1016, y0–611 across 20 exprs → 854² @ 168/854
    TOA_BUST_CROP = (568, 0, 601, 601)
    KAORU_BUST_CROP = (173, 0, 854, 854)
    BUST_DISPLAY_ZOOM = 168 / 601.0
    KAORU_BUST_ZOOM = 168 / 854.0

    TOA_EXPRESSIONS = (
        "neutral", "happy", "sad", "angry", "surprised", "flustered",
        "worried", "thinking", "determined", "soft",
    )
    # Case 3.5 date furisode set (images/sprites/toa/date/toa-date-*.png).
    TOA_DATE_EXPRESSIONS = TOA_EXPRESSIONS + (
        "bashful", "embarrassed", "twitterpated",
    )
    KAORU_EXPRESSIONS = (
        "neutral", "smirk", "cold", "charm", "cruel", "angry", "amused",
        "bored", "thinking", "determined", "surprised", "commanding",
        "hungry", "satisfied", "furious", "vicious", "ravenous",
        "threatening", "sadistic",
    )

    def _bust_sprite(path, crop, zoom=None):
        if zoom is None:
            zoom = BUST_DISPLAY_ZOOM
        return Transform(
            Crop(crop, path),
            zoom=zoom,
        )

    def _register_side_busts(char_tag, prefix, folder, expressions, crop, zoom=None):
        for expression in expressions:
            path = "images/sprites/{}/{}-{}.png".format(folder, prefix, expression)
            bust = _bust_sprite(path, crop, zoom)
            renpy.image(("side", char_tag, "expression", expression), bust)
            renpy.image(("side", char_tag, expression), bust)

    def _register_toa_work_side_bust_aliases(expressions):
        """Layeredimage outfit group exposes outfit_work; alias side bust keys."""
        for expression in expressions:
            path = "images/sprites/toa/toa-{}.png".format(expression)
            bust = _bust_sprite(path, TOA_BUST_CROP)
            for outfit_key in ("work", "outfit_work"):
                renpy.image(("side", "toa", outfit_key, expression), bust)
                renpy.image(("side", "toa", outfit_key, "expression", expression), bust)

    _register_side_busts("toa", "toa", "toa", TOA_EXPRESSIONS, TOA_BUST_CROP)
    _register_toa_work_side_bust_aliases(TOA_EXPRESSIONS)

    def _register_toa_date_side_busts():
        for expression in TOA_DATE_EXPRESSIONS:
            path = "images/sprites/toa/date/toa-date-{}.png".format(expression)
            bust = _bust_sprite(path, TOA_BUST_CROP)
            for outfit_key in ("date", "outfit_date"):
                renpy.image(("side", "toa", outfit_key, expression), bust)
                renpy.image(("side", "toa", outfit_key, "expression", expression), bust)

    _register_toa_date_side_busts()
    _register_side_busts(
        "kaoru", "kaoru", "kaoru", KAORU_EXPRESSIONS, KAORU_BUST_CROP, KAORU_BUST_ZOOM
    )

define config.side_image_prefix_tag = "side"

transform fit_screen:
    fit "cover"
    xsize 1280
    ysize 720
    xalign 0.5
    yalign 0.5

# CG event art (1536×1024, 3:2): show entire frame; black bars fill 16:9 gaps.
transform fit_cg:
    fit "contain"
    xsize 1280
    ysize 720
    xalign 0.5
    yalign 0.5

image _cg_letterbox = Solid("#000000", xsize=1280, ysize=720)

transform left:
    xalign SPRITE_LEFT_XALIGN
    yalign 1.0
    yanchor 1.0
    yoffset SPRITE_STAGE_YOFFSET
    zoom SPRITE_STAGE_ZOOM

transform right:
    xalign SPRITE_RIGHT_XALIGN
    yalign 1.0
    yanchor 1.0
    yoffset SPRITE_STAGE_YOFFSET
    zoom SPRITE_STAGE_ZOOM

transform center:
    xalign 0.5
    yalign 1.0
    yanchor 1.0
    yoffset SPRITE_STAGE_YOFFSET
    zoom SPRITE_STAGE_ZOOM

# Smaller stage sprites over CG illustrations: flanking corners, feet at textbox top.
transform cg_left:
    xalign CG_SPRITE_LEFT_XALIGN
    yalign 1.0
    yanchor 1.0
    yoffset CG_SPRITE_YOFFSET
    zoom CG_SPRITE_ZOOM

transform cg_right:
    xalign CG_SPRITE_RIGHT_XALIGN
    yalign 1.0
    yanchor 1.0
    yoffset CG_SPRITE_YOFFSET
    zoom CG_SPRITE_ZOOM

# Hide full-body sprite off-screen but keep expression for side bust portrait.
transform offstage:
    xpos -2000
    ypos 720
    xanchor 0.5
    yanchor 1.0
    zoom SPRITE_STAGE_ZOOM
