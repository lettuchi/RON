# ===========================================================================
# game/duet_song.rpy ,  Toa + Kaoru duet 「嘘の夜を走れ」
# ===========================================================================
#
# High-energy anime duet (audio/bgm/duet_song.mp3, ~215 s planned). Ten montage
# stills (game/images/ds/). All-sung track, subtitles are sense-translation only.
# Approximate ~18–20 s beats; refine with faster-whisper when needed.
#
# Callable from CG Gallery → Music: gallery_play_music_cinematic().
# ===========================================================================

## --- Art (game/images/ds/) -------------------------------------------------
image ds_canal_two       = At("images/ds/ds-canal-two-lanterns.png", fit_screen)
image ds_duet_run        = At("images/ds/ds-duet-run-canal.png", fit_screen)
image ds_office_faces    = At("images/ds/ds-office-facing.png", fit_screen)
image ds_kaoru_canal     = At("images/ds/ds-kaoru-canal-night.png", fit_screen)
image ds_bridge_two      = At("images/ds/ds-bridge-two-silhouettes.png", fit_screen)
image ds_duet_together   = At("images/ds/ds-duet-together-bridge.png", fit_screen)
image ds_umbrella_two    = At("images/ds/ds-umbrella-two.png", fit_screen)
image ds_lantern_pair    = At("images/ds/ds-lantern-reflection-two.png", fit_screen)
image ds_duet_portrait   = At("images/ds/ds-duet-portrait-canal.png", fit_screen)
image ds_rain_chase      = At("images/ds/ds-duet-rain-chase.png", fit_screen)

image ds_title_text = Text(
    "{font=fonts/YujiSyuku-Regular.ttf}嘘の夜を走れ\n{size=30}Run Through the Lying Night{/size}{/font}",
    size=72, text_align=0.5, xalign=0.5, color="#f8f4ec",
    outlines=[(3, "#000000dd", 0, 0), (7, "#3a2040aa", 0, 0)])

image ds_end_text = Text(
    "{font=fonts/YujiSyuku-Regular.ttf}かきた　とあ　×　橘　薫\n{size=32}Kakita Toa × Kitsu Kaoru{/size}{/font}",
    size=100, text_align=0.5, xalign=0.5, color="#faf8f5",
    outlines=[(3, "#000000dd", 0, 0), (8, "#4a2848aa", 0, 0)])


## --- Transitions -----------------------------------------------------------
define ds_dissolve      = Dissolve(1.0)
define ds_dissolve_long = Dissolve(2.0)
define ds_dip = Fade(1.2, 0.2, 1.2, color="#0a0810")


## --- Ken Burns -------------------------------------------------------------
transform ds_kb_in:
    subpixel True
    zoom 1.05 xalign 0.5 yalign 0.5
    linear 24.0 zoom 1.18

transform ds_kb_pan_r:
    subpixel True
    zoom 1.12 xalign 0.32 yalign 0.5
    linear 24.0 xalign 0.68

transform ds_kb_pan_l:
    subpixel True
    zoom 1.12 xalign 0.68 yalign 0.5
    linear 24.0 xalign 0.32

transform ds_kb_rise:
    subpixel True
    zoom 1.14 xalign 0.5 yalign 0.66
    linear 24.0 yalign 0.34 zoom 1.06

transform ds_kb_settle:
    subpixel True
    zoom 1.08 xalign 0.5 yalign 0.5
    linear 24.0 zoom 1.16


transform ds_title_in:
    xalign 0.5 yalign 0.28
    alpha 0.0 yoffset -8
    easein 1.2 alpha 1.0 yoffset 0

transform ds_end_drop:
    xalign 0.5 yalign 0.5
    alpha 0.0 zoom 1.08 yoffset 14
    easein_quart 1.4 alpha 1.0 zoom 1.0 yoffset 0


transform ds_sub_anim:
    on show, replace:
        alpha 0.0 yoffset 8
        easein 0.22 alpha 1.0 yoffset 0
    on hide:
        easeout 0.28 alpha 0.0


screen ds_subtitle(english="", n=0):
    zorder 70
    frame:
        at ds_sub_anim
        xalign 0.5
        yalign 0.88
        background "#0a0810b3"
        padding (36, 18)
        text english:
            xalign 0.5
            text_align 0.5
            xmaximum 1120
            size 28
            italic True
            color "#faf5f0"
            outlines [(2, "#000000cc", 0, 0)]


default _ds_sub_n = 0

init python:
    DS_SUB_LEAD = 0.28
    DS_SUB_LAG = 0.04

    def ds_sub(english=""):
        store._ds_sub_n += 1
        renpy.show_screen("ds_subtitle", english=english, n=store._ds_sub_n)

    def ds_sub_clear():
        renpy.hide_screen("ds_subtitle")


screen ds_escape_menu():
    zorder 200
    key "game_menu" action [
        Stop("music", fadeout=0.5),
        Hide("ds_subtitle"),
        MainMenu(confirm=False),
    ]


label duet_song_sequence:
    $ enable_cinematic_music()
    show screen ds_escape_menu
    scene black with None
    $ ds_sub_clear()
    play music audio.bgm_duet noloop fadein 2.0

    # ~215 s planned, ten ~18–20 s beats (approximate lyric sync).

    scene ds_canal_two at ds_kb_in with Dissolve(2.5)
    show ds_title_text at ds_title_in with Dissolve(1.0)
    pause 3.5
    $ ds_sub("Rain hammers the eardrums, in the city of lies, the two of us break into a run")
    hide ds_title_text with Dissolve(0.8)
    pause 5.0

    scene ds_duet_run at ds_kb_settle with None
    $ ds_sub("Black sleeves sing in the wind; the white crane pierces the night")
    pause 5.5
    $ ds_sub("I know your coldness, still this gaze burns hot")
    pause 5.5

    scene ds_rain_chase at ds_kb_pan_l with None
    $ ds_sub("A laughing night beyond the rain; distance itself is sweet poison")
    pause 5.5
    $ ds_sub("I won't return you, won't let you go, that's the rule for us two")
    pause 5.5

    scene ds_bridge_two at ds_kb_rise with None
    $ ds_sub("This heartbeat won't stop, this night isn't over yet")
    pause 5.5
    $ ds_sub("Run through the lying night, together, canal lanterns blaze")
    pause 5.5

    scene ds_duet_together at ds_kb_in with None
    $ ds_sub("Can't grasp you, won't release you, we sing across the waves")
    pause 5.5
    $ ds_sub("Cruel as it is, morning comes, in the city of lies, a true voice")
    pause 5.5

    scene ds_kaoru_canal at ds_kb_pan_r with None
    $ ds_sub("Run through the lying night")
    pause 5.0
    $ ds_sub("After tears, go on with a smile; reach past your shadow")
    pause 5.5

    scene ds_umbrella_two at ds_kb_pan_l with None
    $ ds_sub("I don't want victory, I want the heartbeat beside me. I want to keep running")
    pause 5.5
    $ ds_sub("The night lines up lies; your silence becomes the beat")
    pause 5.5

    scene ds_office_faces at ds_kb_settle with None
    $ ds_sub("A sweet voice can be a blade too, you're still here")
    pause 5.5
    $ ds_sub("Doors stay shut, our two lights won't die")
    pause 5.5

    scene ds_lantern_pair at ds_kb_pan_r with None
    $ ds_sub("Without calling your name, I know, still here")
    pause 5.5
    $ ds_sub("Run through the lying night, lying dawn, color of hope")
    pause 5.5

    scene ds_duet_portrait at ds_kb_in with ds_dissolve_long
    $ ds_sub("Our two lights won't go out, Kakita Toa, Kitsu Kaoru, still here")
    pause 6.0
    $ ds_sub("The night remains, run, together")
    pause 5.0

    $ ds_sub_clear()
    scene black with ds_dip
    show ds_end_text at ds_end_drop with Dissolve(1.0)
    pause 5.0
    stop music fadeout 3.5
    hide ds_end_text with Dissolve(2.0)
    scene black with Dissolve(1.0)
    pause 1.0

    $ ds_sub_clear()
    hide ds_end_text
    hide ds_title_text
    hide screen ds_escape_menu
    $ finish_cinematic_music()
    return
