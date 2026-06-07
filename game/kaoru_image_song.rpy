# ===========================================================================
# game/kaoru_image_song.rpy ,  Kaoru image song montage 「権利の帳」
# ===========================================================================
#
# Cruel magistrate image song (audio/bgm/kaoru_image_song_kenri.mp3, ~222 s; Hakuoki-style v3).
# Twenty montage stills (game/images/ks/; synced + perspective variety 2026-06-02). Subtitle timing is approximate
# (~10–11 s beats across the track); refine with faster-whisper on the mp3 when needed.
#
# Callable from CG Gallery → Music: gallery_play_music_cinematic().
# ===========================================================================

## --- Art (game/images/ks/) -------------------------------------------------
image ks_canal_ledger     = At("images/ks/ks-canal-night-ledger.png", fit_screen)
image ks_rain_alley       = At("images/ks/ks-rain-alley-pursuit.png", fit_screen)
image ks_kaoru_rain_left  = At("images/ks/ks-kaoru-rain-left.png", fit_screen)
image ks_office_seal      = At("images/ks/ks-office-desk-seal.png", fit_screen)
image ks_lantern          = At("images/ks/ks-lantern-closeup.png", fit_screen)
image ks_ledger_close     = At("images/ks/ks-ledger-closeup.png", fit_screen)
image ks_silhouette       = At("images/ks/ks-woman-silhouette-away.png", fit_screen)
image ks_embankment       = At("images/ks/ks-canal-embankment-walk.png", fit_screen)
image ks_sake_cup         = At("images/ks/ks-sake-cup-desk.png", fit_screen)
image ks_jade_banner      = At("images/ks/ks-jade-banner-office.png", fit_screen)
image ks_canal_boat       = At("images/ks/ks-canal-boat-night.png", fit_screen)
image ks_kaoru_canal_back = At("images/ks/ks-kaoru-canal-back.png", fit_screen)
image ks_office_window    = At("images/ks/ks-office-window-city.png", fit_screen)
image ks_seal_wax         = At("images/ks/ks-seal-wax-drip.png", fit_screen)
image ks_bridge_dance     = At("images/ks/ks-bridge-judgment-night.png", fit_screen)
image ks_door_ajar        = At("images/ks/ks-office-door-ajar.png", fit_screen)
image ks_ledger_offer     = At("images/ks/ks-ledger-close-offer.png", fit_screen)
image ks_smirk_close      = At("images/ks/ks-kaoru-smirk-close.png", fit_screen)
image ks_ink_brush        = At("images/ks/ks-ink-brush-desk.png", fit_screen)
image ks_kaoru_desk_front = At("images/ks/ks-kaoru-desk-front.png", fit_screen)
image ks_pages_wind       = At("images/ks/ks-ledger-pages-wind.png", fit_screen)
image ks_moon_canal       = At("images/ks/ks-moonlit-canal-smirk.png", fit_screen)
image ks_hand_ledger      = At("images/ks/ks-hand-offer-ledger.png", fit_screen)
image ks_canal_night      = At("images/ks/ks-canal-night.png", fit_screen)
image ks_seal_press       = At("images/ks/ks-seal-press.png", fit_screen)
image ks_chrysanthemum    = At("images/ks/ks-jade-banner-office.png", fit_screen)
image ks_ledger_stacks    = At("images/ks/ks-ledger-stacks-office.png", fit_screen)
image ks_rain_window      = At("images/ks/ks-rain-window-ledger.png", fit_screen)

image ks_title_text = Text(
    "{font=fonts/YujiSyuku-Regular.ttf}権利の帳\n{size=30}The Ledger of Rights{/size}{/font}",
    size=72, text_align=0.5, xalign=0.5, color="#f5e6c8",
    outlines=[(3, "#000000dd", 0, 0), (7, "#3a1500aa", 0, 0)])

image ks_end_text = Text(
    "{font=fonts/YujiSyuku-Regular.ttf}橘　薫\n{size=36}Kitsu Kaoru{/size}{/font}",
    size=120, text_align=0.5, xalign=0.5, color="#f3e3c8",
    outlines=[(3, "#000000dd", 0, 0), (8, "#5e0010aa", 0, 0)])


## --- Transitions -----------------------------------------------------------
define ks_dissolve      = Dissolve(1.0)
define ks_dissolve_long = Dissolve(2.0)
define ks_dip = Fade(1.2, 0.2, 1.2, color="#0a0608")


## --- Ken Burns (~26 s sweeps; scenes cut earlier at ~10 s beats) ------------
transform ks_kb_in:
    subpixel True
    zoom 1.05 xalign 0.5 yalign 0.5
    linear 26.0 zoom 1.18

transform ks_kb_out:
    subpixel True
    zoom 1.18 xalign 0.5 yalign 0.5
    linear 26.0 zoom 1.05

transform ks_kb_pan_r:
    subpixel True
    zoom 1.12 xalign 0.32 yalign 0.5
    linear 26.0 xalign 0.68

transform ks_kb_pan_l:
    subpixel True
    zoom 1.12 xalign 0.68 yalign 0.5
    linear 26.0 xalign 0.32

transform ks_kb_rise:
    subpixel True
    zoom 1.14 xalign 0.5 yalign 0.66
    linear 26.0 yalign 0.34 zoom 1.06

transform ks_kb_settle:
    subpixel True
    zoom 1.08 xalign 0.5 yalign 0.5
    linear 26.0 zoom 1.16


transform ks_title_in:
    xalign 0.5 yalign 0.28
    alpha 0.0 yoffset -8
    easein 1.2 alpha 1.0 yoffset 0

transform ks_end_drop:
    xalign 0.5 yalign 0.5
    alpha 0.0 zoom 1.08 yoffset 14
    easein_quart 1.4 alpha 1.0 zoom 1.0 yoffset 0


transform ks_sub_anim:
    on show, replace:
        alpha 0.0 yoffset 8
        easein 0.22 alpha 1.0 yoffset 0
    on hide:
        easeout 0.28 alpha 0.0


screen ks_subtitle(english="", n=0):
    zorder 70
    frame:
        at ks_sub_anim
        xalign 0.5
        yalign 0.88
        background "#0a0608b3"
        padding (36, 18)
        text english:
            xalign 0.5
            text_align 0.5
            xmaximum 1120
            size 28
            italic True
            color "#fbeede"
            outlines [(2, "#000000cc", 0, 0)]


default _ks_sub_n = 0

init python:
    KS_SUB_LEAD = 0.28
    KS_SUB_LAG = 0.04

    def ks_sub(english=""):
        store._ks_sub_n += 1
        renpy.show_screen("ks_subtitle", english=english, n=store._ks_sub_n)

    def ks_sub_clear():
        renpy.hide_screen("ks_subtitle")


screen ks_escape_menu():
    zorder 200
    key "game_menu" action [
        Stop("music", fadeout=0.5),
        Hide("ks_subtitle"),
        MainMenu(confirm=False),
    ]


label kaoru_image_song_sequence:
    $ enable_cinematic_music()
    show screen ks_escape_menu
    scene black with None
    $ ks_sub_clear()
    play music audio.bgm_kaoru_kenri noloop fadein 2.0

    # ~222 s, twenty ~10 s montage beats (approximate lyric sync).

    scene ks_canal_ledger at ks_kb_in with Dissolve(2.5)
    show ks_title_text at ks_title_in with Dissolve(1.0)
    pause 3.5
    $ ks_sub("The record doesn't judge lies. I do.")
    pause 5.5
    $ ks_sub("Night canal, lantern light swimming on the water")
    hide ks_title_text with Dissolve(0.8)
    pause 3.5
    $ ks_sub("The ledger's spine, fingers that know it by heart")
    pause 5.5

    scene ks_kaoru_rain_left at ks_kb_pan_l with None
    $ ks_sub("Stamp the seal in the Champion's name, someone's tomorrow becomes tonight's play")
    pause 5.5
    $ ks_sub("Cobblestones laugh under my heels, only the ledger's weight walks ahead")
    pause 5.5
    $ ks_sub("This city is honest: it only speaks lies, so I honestly take what I want")
    pause 5.5

    scene ks_lantern at ks_kb_in with None
    $ ks_sub("Ledger of rights, add pages; turn silence into signature")
    pause 5.5
    $ ks_sub("No king in this city, only me")
    pause 5.5

    scene ks_seal_press at ks_kb_pan_r with None
    $ ks_sub("Stamp the seal, won't close the ledger, not enough yet")
    pause 5.5

    scene ks_kaoru_desk_front at ks_kb_settle with None
    $ ks_sub("Sweet voices, tears, all evidence")
    pause 5.5
    $ ks_sub("Judgment night: dance. \"No\" is a cute lie.")
    pause 5.5

    scene ks_ledger_stacks at ks_kb_settle with None
    $ ks_sub("Jade seal, chrysanthemum banner rippling, one magistrate's ledger is the whole law")
    pause 5.5
    $ ks_sub("Add pages through ink-dark nights; smile and walk ahead")
    pause 5.5

    scene ks_silhouette at ks_kb_rise with None
    $ ks_sub("Paper lies better than skin. The law's arm is long, hand me everything it reaches.")
    pause 5.5
    $ ks_sub("Shame? Nothing to hide. Rights belong to whoever can see them.")
    pause 5.5

    scene ks_canal_night at ks_kb_pan_l with None
    $ ks_sub("The embankment knows every footstep, I walk where the ledger leads")
    pause 5.5

    scene ks_pages_wind at ks_kb_pan_r with None
    $ ks_sub("Pages turn in the wind, sweet voices, tears, all evidence")
    pause 5.5
    $ ks_sub("Judgment night: dance.")
    pause 5.5

    scene ks_rain_window at ks_kb_in with None
    $ ks_sub("Rain on the magistrate's window, studied the Crown's lessons; practice is simpler")
    pause 5.5
    $ ks_sub("No king, only me")
    pause 5.5

    scene ks_chrysanthemum at ks_kb_rise with None
    $ ks_sub("Take what I like; regret is someone else's job")
    pause 5.5

    scene ks_moon_canal at ks_kb_pan_l with None
    $ ks_sub("...Next name.")
    pause 5.5
    $ ks_sub("In this city of lies, I play at truth")
    pause 5.5

    scene ks_kaoru_canal_back at ks_kb_pan_r with None
    $ ks_sub("Won't close the ledger, not enough yet")
    pause 5.5
    $ ks_sub("Judgment night: dance; I'll even prepare your escape route")
    pause 5.5

    scene ks_office_window at ks_kb_settle with None
    $ ks_sub("Ledger of rights, blood and ink alike")
    pause 5.5
    $ ks_sub("Before they dry, on to the next chapter")
    pause 5.5

    scene ks_seal_wax at ks_kb_in with None
    $ ks_sub("No king, Magistrate Kitsu Kaoru")
    pause 5.5

    scene ks_bridge_dance at ks_kb_pan_r with None
    $ ks_sub("The record remains. Will you?")
    pause 5.5

    scene ks_hand_ledger at ks_kb_in with None
    $ ks_sub("Turn silence into signature, take the ledger")
    pause 5.5

    scene ks_door_ajar at ks_kb_pan_l with None
    pause 4.5

    scene ks_ledger_offer at ks_kb_settle with None
    pause 4.5

    scene ks_smirk_close at ks_kb_in with ks_dissolve_long
    pause 12.0
    $ ks_sub_clear()
    scene black with ks_dip
    show ks_end_text at ks_end_drop with Dissolve(1.0)
    pause 6.0
    stop music fadeout 3.5
    hide ks_end_text with Dissolve(2.0)
    scene black with Dissolve(1.0)
    pause 1.0

    $ ks_sub_clear()
    hide ks_end_text
    hide ks_title_text
    hide screen ks_escape_menu
    $ finish_cinematic_music()
    return
