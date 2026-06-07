# ===========================================================================
# game/transforms_op_ed.rpy ,  Shared OP / ED cinematic polish
# ===========================================================================
#
# Ken Burns, dissolves, vignette/letterbox overlay, and subtle color grade for
# opening_sequence (opening.rpy) and ed_sequence (ed_sequence.rpy).
# Resolution: 1280×720 (gui.init in gui.rpy).
# ===========================================================================

## --- Shared transitions ---------------------------------------------------
define op_ed_dissolve       = Dissolve(0.55)
define op_ed_dissolve_mid   = Dissolve(1.0)
define op_ed_dissolve_long  = Dissolve(2.0)
define op_ed_dissolve_soft  = Dissolve(0.35)

define op_ed_dip            = Fade(1.0, 0.18, 1.0, color="#0a0608")
define op_ed_dip_slow       = Fade(1.2, 0.25, 1.2, color="#0a0608")

# OP beat flashes (also used on chorus hits)
define op_flash             = Fade(0.10, 0.0, 0.30, color="#ffffff")
define op_redflash          = Fade(0.10, 0.05, 0.35, color="#2a0008")

# ED aliases (same family, tuned for ending montage)
define ed_dissolve          = op_ed_dissolve_mid
define ed_dissolve_mid      = Dissolve(1.5)
define ed_dissolve_long     = op_ed_dissolve_long
define ed_dip               = op_ed_dip_slow


## --- Montage overlay (letterbox + edge vignette) --------------------------
transform cinematic_overlay_breathe:
    subpixel True
    parallel:
        ease 6.0 zoom 1.0
        ease 6.0 zoom 1.008
        repeat

transform cinematic_overlay_fadein:
    alpha 0.0
    easein 1.8 alpha 1.0

transform cinematic_overlay_combined:
    subpixel True
    alpha 0.0
    easein 1.8 alpha 1.0
    parallel:
        ease 6.0 zoom 1.0
        ease 6.0 zoom 1.008
        repeat

screen cinematic_montage_overlay():
    zorder 54
    fixed at cinematic_overlay_combined:
        add Solid("#000000") xalign 0.5 yalign 0.0 xsize 1280 ysize 40
        add Solid("#000000") xalign 0.5 yalign 1.0 xsize 1280 ysize 40
        add Solid("#08040677") xalign 0.0 yalign 0.5 xsize 96 ysize 720
        add Solid("#08040677") xalign 1.0 yalign 0.5 xsize 96 ysize 720
        add Solid("#00000044") xalign 0.5 yalign 0.0 xsize 1280 ysize 72
        add Solid("#00000044") xalign 0.5 yalign 1.0 xsize 1280 ysize 72


## --- Staggered fade-in (hard-cut friendly; no extra pause drift) ----------
transform cinematic_fade_in:
    alpha 0.0
    easein 0.52 alpha 1.0

transform cinematic_fade_in_slow:
    alpha 0.0
    easein 0.82 alpha 1.0

transform cinematic_fade_in_delayed:
    alpha 0.0
    pause 0.07
    easein 0.58 alpha 1.0


## --- Subtle color grade (matrixcolor on montage stills) -------------------
transform cinematic_grade_warm:
    matrixcolor TintMatrix("#ffe8d8") * SaturationMatrix(1.06) * ContrastMatrix(1.02)

transform cinematic_grade_golden:
    matrixcolor TintMatrix("#f5e6c8") * SaturationMatrix(1.04) * BrightnessMatrix(0.015)

transform cinematic_grade_crimson:
    matrixcolor TintMatrix("#ffd0d8") * SaturationMatrix(1.08) * ContrastMatrix(1.03)


## --- OP Ken Burns (~11 s sweeps, faster EDM montage) ----------------------
transform op_kb_in:
    subpixel True
    matrixcolor TintMatrix("#ffe0d8") * SaturationMatrix(1.07)
    alpha 0.0
    parallel:
        easein 0.48 alpha 1.0
    parallel:
        zoom 1.06 xalign 0.5 yalign 0.5
        linear 11.0 zoom 1.20

transform op_kb_out:
    subpixel True
    matrixcolor TintMatrix("#ffe0d8") * SaturationMatrix(1.07)
    alpha 0.0
    parallel:
        easein 0.48 alpha 1.0
    parallel:
        zoom 1.22 xalign 0.5 yalign 0.5
        linear 11.0 zoom 1.06

transform op_kb_pan:
    subpixel True
    matrixcolor TintMatrix("#ffe0d8") * SaturationMatrix(1.07)
    alpha 0.0
    parallel:
        easein 0.48 alpha 1.0
    parallel:
        zoom 1.18 xalign 0.30 yalign 0.5
        linear 11.0 xalign 0.70

transform op_kb_pan_l:
    subpixel True
    matrixcolor TintMatrix("#ffe0d8") * SaturationMatrix(1.07)
    alpha 0.0
    parallel:
        easein 0.48 alpha 1.0
    parallel:
        zoom 1.16 xalign 0.72 yalign 0.5
        linear 11.0 xalign 0.28

transform op_kb_rise:
    subpixel True
    matrixcolor TintMatrix("#ffd8e0") * SaturationMatrix(1.08)
    alpha 0.0
    parallel:
        easein 0.50 alpha 1.0
    parallel:
        zoom 1.14 xalign 0.5 yalign 0.62
        linear 11.0 yalign 0.38 zoom 1.08

transform op_kb_settle:
    subpixel True
    matrixcolor TintMatrix("#f5e0c8") * SaturationMatrix(1.05)
    alpha 0.0
    parallel:
        easein 0.65 alpha 1.0
    parallel:
        zoom 1.06 xalign 0.5 yalign 0.5
        linear 14.0 zoom 1.14

transform op_punch:
    subpixel True
    matrixcolor TintMatrix("#ffd0d8") * SaturationMatrix(1.10)
    alpha 0.0
    parallel:
        easein 0.35 alpha 1.0
    parallel:
        zoom 1.30 xalign 0.5 yalign 0.5
        linear 2.6 zoom 1.12

transform op_title_drop:
    xalign 0.5 yalign 0.42
    alpha 0.0 zoom 1.22 yoffset -26
    easein_quart 0.6 alpha 1.0 zoom 1.0 yoffset 0


## --- ED Ken Burns (~26 s sweeps, reflective ending montage) ---------------
transform ed_kb_in:
    subpixel True
    matrixcolor TintMatrix("#f5e6c8") * SaturationMatrix(1.05)
    alpha 0.0
    parallel:
        easein 0.55 alpha 1.0
    parallel:
        zoom 1.05 xalign 0.5 yalign 0.5
        linear 26.0 zoom 1.18

transform ed_kb_out:
    subpixel True
    matrixcolor TintMatrix("#f5e6c8") * SaturationMatrix(1.05)
    alpha 0.0
    parallel:
        easein 0.55 alpha 1.0
    parallel:
        zoom 1.18 xalign 0.5 yalign 0.5
        linear 26.0 zoom 1.05

transform ed_kb_pan_r:
    subpixel True
    matrixcolor TintMatrix("#f5e6c8") * SaturationMatrix(1.05)
    alpha 0.0
    parallel:
        easein 0.55 alpha 1.0
    parallel:
        zoom 1.12 xalign 0.32 yalign 0.5
        linear 26.0 xalign 0.68

transform ed_kb_pan_l:
    subpixel True
    matrixcolor TintMatrix("#f5e6c8") * SaturationMatrix(1.05)
    alpha 0.0
    parallel:
        easein 0.55 alpha 1.0
    parallel:
        zoom 1.12 xalign 0.68 yalign 0.5
        linear 26.0 xalign 0.32

transform ed_kb_rise:
    subpixel True
    matrixcolor TintMatrix("#f5e0c8") * SaturationMatrix(1.06)
    alpha 0.0
    parallel:
        easein 0.58 alpha 1.0
    parallel:
        zoom 1.14 xalign 0.5 yalign 0.66
        linear 26.0 yalign 0.34 zoom 1.06

transform ed_kb_settle:
    subpixel True
    matrixcolor TintMatrix("#f5e6c8") * SaturationMatrix(1.04)
    alpha 0.0
    parallel:
        easein 0.62 alpha 1.0
    parallel:
        zoom 1.08 xalign 0.5 yalign 0.5
        linear 30.0 zoom 1.16

transform ed_title_in:
    xalign 0.5 yalign 0.28
    alpha 0.0 yoffset -8
    easein 1.2 alpha 1.0 yoffset 0

transform ed_end_drop:
    xalign 0.5 yalign 0.5
    alpha 0.0 zoom 1.08 yoffset 14
    easein_quart 1.4 alpha 1.0 zoom 1.0 yoffset 0


## --- Screen ATL (subtitle / card fades) -----------------------------------
transform op_sub_anim:
    on show, replace:
        alpha 0.0 yoffset 12
        easein 0.30 alpha 1.0 yoffset 0
    on hide:
        easeout 0.30 alpha 0.0

transform op_card_anim:
    on show, replace:
        alpha 0.0 xoffset 28
        easein 0.35 alpha 1.0 xoffset 0
    on hide:
        easeout 0.30 alpha 0.0

transform ed_sub_anim:
    on show, replace:
        alpha 0.0 yoffset 8
        easein 0.22 alpha 1.0 yoffset 0
    on hide:
        easeout 0.28 alpha 0.0
