# ===========================================================================
# game/toa_image_song.rpy ,  Toa image song montage 「赤い糸の灯」
# ===========================================================================
#
# Heroine image song (audio/bgm/toa_image_song.mp3, ~213 s planned; Hakuoki-style).
# Eighteen montage stills (game/images/ts/). Subtitle timing is approximate
# (~10–11 s beats, ~12% faster cuts); refine with faster-whisper on the mp3 when needed.
#
# Callable from CG Gallery → Music: gallery_play_music_cinematic().
# ===========================================================================

## --- Art (game/images/ts/) -------------------------------------------------
image ts_canal_lanterns   = At("images/ts/ts-canal-lanterns.png", fit_screen)
image ts_thread_hands     = At("images/ts/ts-toa-thread-hands.png", fit_screen)
image ts_lantern_closeup  = At("images/ts/ts-lantern-closeup.png", fit_screen)
image ts_dance_bridge     = At("images/ts/ts-dance-bridge.png", fit_screen)
image ts_bridge_dance_rear = At("images/ts/ts-bridge-dance-rear.png", fit_screen)
image ts_canal_overlook   = At("images/ts/ts-canal-gaze.png", fit_screen)
image ts_crane_obi        = At("images/ts/ts-crane-obi-detail.png", fit_screen)
image ts_permit_desk      = At("images/ts/ts-permit-desk.png", fit_screen)
image ts_umbrella_rain    = At("images/ts/ts-umbrella-rain.png", fit_screen)
image ts_rain_run         = At("images/ts/ts-rain-run.png", fit_screen)
image ts_sweets_umbrella  = At("images/ts/ts-sweets-umbrella.png", fit_screen)
image ts_magistrate_hall  = At("images/ts/ts-magistrate-hall.png", fit_screen)
image ts_magistrate_back  = At("images/ts/ts-office-threshold.png", fit_screen)
image ts_smile_lantern    = At("images/ts/ts-toa-smile-close.png", fit_screen)
image ts_hopeful_dawn_img = At("images/ts/ts-hopeful-dawn.png", fit_screen)
image ts_dawn_canal       = At("images/ts/ts-night-embankment.png", fit_screen)
image ts_tearful_smile    = At("images/ts/ts-tearful-smile.png", fit_screen)
image ts_portrait_close   = At("images/ts/ts-white-hair-wind.png", fit_screen)

image ts_title_text = Text(
    "{font=fonts/YujiSyuku-Regular.ttf}赤い糸の灯\n{size=30}Lantern of the Red Thread{/size}{/font}",
    size=72, text_align=0.5, xalign=0.5, color="#faf5ff",
    outlines=[(3, "#000000cc", 0, 0), (6, "#4a2840aa", 0, 0)])

image ts_end_text = Text(
    "{font=fonts/YujiSyuku-Regular.ttf}かきた　とあ\n{size=36}Kakita Toa{/size}{/font}",
    size=120, text_align=0.5, xalign=0.5, color="#faf8f5",
    outlines=[(3, "#000000cc", 0, 0), (7, "#5a3048aa", 0, 0)])


## --- Transitions -----------------------------------------------------------
define ts_dissolve      = Dissolve(1.0)
define ts_dissolve_long = Dissolve(2.0)
define ts_dip = Fade(1.2, 0.2, 1.2, color="#0a0810")


## --- Ken Burns (~26 s sweeps; scenes cut earlier at ~10 s beats) ------------
transform ts_kb_in:
    subpixel True
    zoom 1.05 xalign 0.5 yalign 0.5
    linear 26.0 zoom 1.18

transform ts_kb_out:
    subpixel True
    zoom 1.18 xalign 0.5 yalign 0.5
    linear 26.0 zoom 1.05

transform ts_kb_pan_r:
    subpixel True
    zoom 1.12 xalign 0.32 yalign 0.5
    linear 26.0 xalign 0.68

transform ts_kb_pan_l:
    subpixel True
    zoom 1.12 xalign 0.68 yalign 0.5
    linear 26.0 xalign 0.32

transform ts_kb_rise:
    subpixel True
    zoom 1.14 xalign 0.5 yalign 0.66
    linear 26.0 yalign 0.34 zoom 1.06

transform ts_kb_settle:
    subpixel True
    zoom 1.08 xalign 0.5 yalign 0.5
    linear 26.0 zoom 1.16


transform ts_title_in:
    xalign 0.5 yalign 0.28
    alpha 0.0 yoffset -8
    easein 1.2 alpha 1.0 yoffset 0

transform ts_end_drop:
    xalign 0.5 yalign 0.5
    alpha 0.0 zoom 1.08 yoffset 14
    easein_quart 1.4 alpha 1.0 zoom 1.0 yoffset 0


transform ts_sub_anim:
    on show, replace:
        alpha 0.0 yoffset 8
        easein 0.22 alpha 1.0 yoffset 0
    on hide:
        easeout 0.28 alpha 0.0


screen ts_subtitle(english="", n=0):
    zorder 70
    frame:
        at ts_sub_anim
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


default _ts_sub_n = 0

init python:
    TS_SUB_LEAD = 0.28
    TS_SUB_LAG = 0.04

    def ts_sub(english=""):
        store._ts_sub_n += 1
        renpy.show_screen("ts_subtitle", english=english, n=store._ts_sub_n)

    def ts_sub_clear():
        renpy.hide_screen("ts_subtitle")


screen ts_escape_menu():
    zorder 200
    key "game_menu" action [
        Stop("music", fadeout=0.5),
        Hide("ts_subtitle"),
        MainMenu(confirm=False),
    ]


label toa_image_song_sequence:
    $ enable_cinematic_music()
    show screen ts_escape_menu
    scene black with None
    $ ts_sub_clear()
    play music audio.bgm_toa_image noloop fadein 2.0

    # ~213 s planned, eighteen montage beats (~10 s, faster cuts).

    scene ts_canal_lanterns at ts_kb_in with Dissolve(2.5)
    show ts_title_text at ts_title_in with Dissolve(1.0)
    pause 3.0
    $ ts_sub("Canal lanterns, one, then another")
    hide ts_title_text with Dissolve(0.8)
    pause 3.0

    scene ts_thread_hands at ts_kb_rise with None
    $ ts_sub("I wind the red thread around my fingertips")
    pause 4.7

    scene ts_lantern_closeup at ts_kb_pan_r with None
    $ ts_sub("The red thread is invisible, but surely tied deep in my chest")
    pause 4.7

    scene ts_dance_bridge at ts_kb_pan_r with None
    $ ts_sub("City of lies, the water is a mirror; every face hides the truth")
    pause 4.7
    $ ts_sub("Black sleeves, the crane on my obi swims; I thought the dance was over")
    pause 4.7

    scene ts_bridge_dance_rear at ts_kb_pan_l with None
    $ ts_sub("Your smile, a cold door, still my fingers won't let go")
    pause 4.7
    $ ts_sub("I know it isn't kindness, still I want it")
    pause 4.7

    scene ts_canal_overlook at ts_kb_pan_l with None
    $ ts_sub("I still tie this thread; I light a lamp on lying nights")
    pause 4.7
    $ ts_sub("Closed doors, cruel words, I know you, and I still return")
    pause 4.7

    scene ts_crane_obi at ts_kb_rise with None
    $ ts_sub("The crane obi sways in the wind")
    pause 4.7
    $ ts_sub("Your back overlooking the canal, far is fine, I want to be here")
    pause 4.7

    scene ts_permit_desk at ts_kb_settle with None
    $ ts_sub("The one who carries the ledger is fragile as glass")
    pause 4.7

    scene ts_umbrella_rain at ts_kb_in with None
    $ ts_sub("Rain on cobblestones, under one umbrella we shared something sweet")
    pause 4.7

    scene ts_rain_run at ts_kb_pan_r with None
    $ ts_sub("Don't call me a tool, even if you do, I won't hide my tears")
    pause 4.7

    scene ts_sweets_umbrella at ts_kb_pan_l with None
    $ ts_sub("My only lie is \"I'm fine\", I'm not fine")
    pause 4.7

    scene ts_magistrate_hall at ts_kb_in with None
    $ ts_sub("I know it isn't kindness, still I want it")
    pause 4.7

    scene ts_magistrate_back at ts_kb_settle with None
    $ ts_sub("Even if it snaps, I tie it again, not fate, I chose this")
    pause 4.7

    scene ts_smile_lantern at ts_kb_rise with None
    $ ts_sub("Even if the whole city lies, I want my feeling alone to be true")
    pause 4.7
    $ ts_sub("Without calling your name, I'm still here")
    pause 4.7

    scene ts_hopeful_dawn_img at ts_kb_pan_l with None
    $ ts_sub("I still tie the red thread; on a lying dawn, the color of hope")
    pause 4.7

    scene ts_dawn_canal at ts_kb_pan_r with None
    $ ts_sub("Doors stay shut, my lantern won't go out")
    pause 4.7

    scene ts_tearful_smile at ts_kb_settle with None
    $ ts_sub("Far is fine, still tied")
    pause 4.7

    scene ts_portrait_close at ts_kb_in with None
    pause 4.3

    $ ts_sub_clear()
    scene black with ts_dip
    show ts_end_text at ts_end_drop with Dissolve(1.0)
    pause 4.3
    $ ts_sub("Another canal lantern, still, I tie")
    pause 4.3
    stop music fadeout 3.5
    hide ts_end_text with Dissolve(2.0)
    scene black with Dissolve(1.0)
    pause 1.0

    $ ts_sub_clear()
    hide ts_end_text
    hide ts_title_text
    hide screen ts_escape_menu
    $ finish_cinematic_music()
    return
