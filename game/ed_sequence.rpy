# ===========================================================================
# game/ed_sequence.rpy ,  Otome-style ENDING SEQUENCE ("ED")
# ===========================================================================
#
# Reflective golden-hour montage to 「嘘つきの糸」/ "The Liar's String"
# (audio/bgm/ending_song.mp3, Kaoru POV, ~190 s).
#
# ~31 unique montage stills (game/images/ed/): office / canal / bridge beats;
# each scene line uses a distinct PNG (replacements in ed_* chorus/bridge block).
# Art: assets/cg-build/build_ed_cgs.py (GenerateImage + compositor).
#
# ---------------------------------------------------------------------------
# SUBTITLE TIMING (measured vocal onsets, same method as opening.rpy):
#   faster-whisper "small" on ending_song.mp3 (VAD + no-VAD tail pass).
#   Whisper text is rough; onsets are mapped to docs/ending-song-lyrics.md.
#   See docs/ed-timing/ed_timing.json and tmp_ed_analysis/ed-timing-map.md.
#   Cue model: `$ ed_sub` then `pause` = gap − ED_SUB_LEAD + ED_SUB_LAG (0.22 /
#   0.06, middle between prior fast/slow passes). Lyric cuts use `scene … with
#   None` (ATL fade-in on ed_kb_* for soft crossfade). Section breaks use dissolves.
# ---------------------------------------------------------------------------
#
# Skippable via `pause` beats. Escape overlay: key "game_menu" → MainMenu(confirm=False).
# Callable from main menu: Function(renpy.call_in_new_context, "ed_sequence").
# ===========================================================================

## --- ED art (~20 montage stills) ------------------------------------------
# Canal / bridge (existing)
image ed_canal_dusk     = At("images/ed/ed-canal-dusk-vista.png", fit_screen)
image ed_canal_walk     = At("images/ed/ed-kaoru-embankment-walk.png", fit_screen)
image ed_bridge         = At("images/ed/ed-kaoru-bridge-crossing.png", fit_screen)
image ed_glance_back    = At("images/ed/ed-kaoru-glance-back.png", fit_screen)
image ed_mikan_thread   = At("images/ed/ed-bridge-red-thread.png", fit_screen)
image ed_toa_bridge_far = At("images/ed/ed-toa-bridge-run-distant.png", fit_screen)
image ed_toa_bridge_mid = At("images/ed/ed-toa-bridge-run-closer-v2.png", fit_screen)
image ed_toa_bridge_near = At("images/ed/ed-toa-bridge-approach.png", fit_screen)
image ed_bridge_reunion = At("images/ed/ed-bridge-two-shot.png", fit_screen)

# ED chorus / bridge replacements (unique beats; no file reuse in montage)
image ed_canal_pursuit       = At("images/ed/ed-kaoru-canal-pursuit.png", fit_screen)
image ed_watches_return      = At("images/ed/ed-kaoru-watches-return.png", fit_screen)
image ed_bridge_chorus       = At("images/ed/ed-kaoru-bridge-red-bind.png", fit_screen)
image ed_thread_second_knot  = At("images/ed/ed-hands-second-knot.png", fit_screen)
image ed_toa_bridge_mid_b    = At("images/ed/ed-toa-bridge-run-mid-chorus.png", fit_screen)
image ed_canal_twilight      = At("images/ed/ed-canal-twilight-ink.png", fit_screen)
image ed_canal_night         = At("images/ed/ed-kaoru-canal-night-lantern.png", fit_screen)
image ed_name_retrace        = At("images/ed/ed-office-name-retrace.png", fit_screen)
image ed_toa_bridge_far_b    = At("images/ed/ed-toa-bridge-instrumental.png", fit_screen)
image ed_toa_bridge_final_cho = At("images/ed/ed-toa-bridge-final-chorus.png", fit_screen)
image ed_toa_bridge_hesitant = At("images/ed/ed-toa-bridge-hesitant.png", fit_screen)
image ed_sleep_red_thread    = At("images/ed/ed-office-sleep-red-thread.png", fit_screen)

# ED expansion stills (assets/op-ed-cg-drafts/ → game/images/ed/)
image ed_canal_lantern_peace = At("images/ed/ed-canal-lantern-peaceful.png", fit_screen)
image ed_toa_red_thread_cu   = At("images/ed/ed-toa-red-thread.png", fit_screen)
image ed_bench_hill_dawn     = At("images/ed/ed-bench-hill.png", fit_screen)
image ed_canal_walk_away     = At("images/ed/ed-canal-walk-away.png", fit_screen)

# Office / domestic (generated for expanded ED)
image ed_office_desk        = At("images/ed/ed-office-desk.png", fit_screen)
image ed_office_tea         = At("images/ed/ed-office-tea.png", fit_screen)
image ed_office_scrolls     = At("images/ed/ed-office-scrolls.png", fit_screen)
image ed_office_window      = At("images/ed/ed-office-window.png", fit_screen)
image ed_office_seal        = At("images/ed/ed-office-seal.png", fit_screen)
image ed_office_mikan       = At("images/ed/ed-office-mikan.png", fit_screen)
image ed_office_night_desk  = At("images/ed/ed-office-night-desk.png", fit_screen)
image ed_office_lantern     = At("images/ed/ed-office-lantern.png", fit_screen)
image ed_office_name_trace  = At("images/ed/ed-office-name-trace.png", fit_screen)
image ed_office_sleep_kiss  = At("images/ed/ed-office-sleep-kiss.png", fit_screen)

image ed_title_text = Text(
    "{font=fonts/YujiSyuku-Regular.ttf}嘘つきの糸\n{size=30}The Liar's String{/size}{/font}",
    size=72, text_align=0.5, xalign=0.5, color="#f5e6c8",
    outlines=[(3, "#000000dd", 0, 0), (7, "#3a1500aa", 0, 0)])

image ed_end_text = Text(
    "{font=fonts/YujiSyuku-Regular.ttf}終わり\n{size=40}The End{/size}{/font}",
    size=150, text_align=0.5, xalign=0.5, color="#f3e3c8",
    outlines=[(3, "#000000dd", 0, 0), (8, "#5e0010aa", 0, 0)])


## --- Subtitle screen (transforms in transforms_op_ed.rpy) -----------------


screen ed_subtitle(english="", n=0):
    zorder 70
    frame:
        at ed_sub_anim
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


default _ed_sub_n = 0

init python:
    # gap − lead + lag (English-only subs; slight fast nudge vs prior 0.22/0.06).
    ED_SUB_LEAD = 0.28
    ED_SUB_LAG = 0.04

    def ed_sub(english=""):
        store._ed_sub_n += 1
        renpy.show_screen("ed_subtitle", english=english, n=store._ed_sub_n)

    def ed_sub_clear():
        renpy.hide_screen("ed_subtitle")


screen ed_escape_menu():
    zorder 200
    key "game_menu" action [
        Stop("music", fadeout=0.5),
        Hide("ed_subtitle"),
        MainMenu(confirm=False),
    ]


label ed_sequence:
    show screen ed_escape_menu
    show screen cinematic_montage_overlay
    scene black with None
    $ ed_sub_clear()
    play music audio.bgm_ending noloop fadein 2.0

    # Cue model: $ed_sub before scene/transition; pause = onset gap − trans.
    # Lyric-synced cuts stay `with None`; ATL fade-in on ed_kb_* gives crossfade feel.
    # Section breaks / instrumentals use ed_dissolve* (pause unchanged, extra beat absorbed).

    # === INTRO, canal dusk =================================================
    scene ed_canal_dusk at ed_kb_in with op_ed_dissolve_long              # @ 0.0
    show ed_title_text at ed_title_in with op_ed_dissolve_mid
    pause 6.74                                                    # @ 6.98
    $ ed_sub("In this city, darker than ink")
    pause 2.54                                                    # @ 9.76
    $ ed_sub("you alone glow vermillion")
    hide ed_title_text with op_ed_dissolve
    pause 7.16                                                    # @ 17.96

    # === VERSE 1, office desk, patrol, bridge ================================
    $ ed_sub("Into the castle I built from lies")
    scene ed_office_desk at ed_kb_pan_r with None                    # @ 17.96
    pause 4.08                                                    # @ 22.28
    $ ed_sub("you barged in, shoes still on, foolish woman")
    pause 3.06                                                    # @ 25.58
    $ ed_sub("those fingers that peel off my mask...")
    scene ed_canal_walk at ed_kb_pan_r with None                     # @ 25.58
    pause 3.66                                                    # @ 29.48
    $ ed_sub("I don't recall ever permitting that")
    scene ed_bridge at ed_kb_pan_l with None                         # @ 29.48
    pause 4.22                                                    # @ 33.94

    # === PRE-CHORUS, tea, glance, red thread ===============================
    $ ed_sub("And yet, why does my hand reach for you?")
    scene ed_office_tea at ed_kb_in with None                        # @ 33.94
    pause 3.98                                                    # @ 38.0 (instr)
    scene ed_glance_back at ed_kb_rise with None                       # @ 38.0
    pause 4.48                                                    # @ 42.40
    $ ed_sub("staining red, like seal-ink")
    scene ed_toa_red_thread_cu at ed_kb_settle with None             # expansion; alt: ed_mikan_thread @ 42.40
    pause 6.58                                                    # @ 49.22

    # === CHORUS 1, office window → scrolls → seal → mikan → night ==========
    $ ed_sub("With the red string, I bind you")
    scene ed_office_window at ed_kb_rise with None                   # @ 49.22
    pause 7.26                                                    # @ 56.72
    $ ed_sub("one knot, and then another")
    scene ed_office_scrolls at ed_kb_pan_l with None                 # @ 56.72
    pause 6.6                                                    # @ 63.56
    $ ed_sub("I don't know how to give it back, but...")
    scene ed_office_seal at ed_kb_in with None                       # @ 63.56
    pause 5.08                                                    # @ 68.88
    $ ed_sub("this string, I will never let be untied")
    scene ed_office_mikan at ed_kb_settle with None                  # @ 68.88
    pause 4.28                                                    # @ 73.40
    $ ed_sub("I press my seal into your skin")
    scene ed_office_night_desk at ed_kb_out with None                # @ 73.40
    pause 5.36                                                    # @ 79.0 (instr)
    $ ed_sub_clear()
    scene ed_canal_pursuit at ed_kb_pan_l with op_ed_dissolve_soft                  # @ 79.0
    pause 2.84                                                    # @ 82.08
    $ ed_sub("Try to run; I'll hunt you down")
    pause 4                                                    # @ 86.32
    scene ed_office_lantern at ed_kb_in with None                    # @ 86.32
    $ ed_sub("the birdcage door, left open")
    pause 3.4                                                    # @ 89.96
    scene ed_watches_return at ed_kb_out with None                   # @ 89.96
    $ ed_sub("and still you return, that foolishness of yours,")
    pause 4.34                                                    # @ 94.54
    scene ed_toa_bridge_far at ed_kb_pan_r with None                 # @ 94.54
    $ ed_sub("I will, surely, call it love")
    pause 4.5                                                    # @ 99.28

    # === CHORUS 2, bridge, thread, Toa run v2, near ========================
    scene ed_bridge_chorus at ed_kb_in with op_ed_dissolve_soft                     # @ 99.28
    $ ed_sub("With the red string, I bind you")
    pause 5.98                                                    # @ 105.50
    scene ed_thread_second_knot at ed_kb_settle with None              # @ 105.50
    $ ed_sub("one knot, and then another")
    pause 7.6                                                    # @ 113.34
    scene ed_toa_bridge_mid at ed_kb_pan_l with None                 # @ 113.34
    $ ed_sub("I don't know how to give it back, but...")
    pause 3.42                                                    # @ 117.00
    scene ed_toa_bridge_mid_b at ed_kb_pan_l with None               # @ 117.00
    $ ed_sub("this string, I will never let be untied")
    pause 4.14                                                    # @ 121.38
    scene ed_toa_bridge_near at ed_kb_in with None                   # @ 121.38
    $ ed_sub("I press my seal into your skin")
    pause 6.78                                                    # @ 128.40

    # === BRIDGE, dusk, name trace, patrol, thread ==========================
    $ ed_sub_clear()
    scene ed_canal_twilight at ed_kb_pan_r with op_ed_dissolve_mid                   # @ 128.40
    $ ed_sub("once the ink dries, even a lie becomes truth")
    pause 2.9                                                    # @ 131.54
    scene ed_office_name_trace at ed_kb_in with None                 # @ 131.54
    $ ed_sub("each time I pressed the seal, my hand trembled")
    pause 5.24                                                    # @ 137.02
    scene ed_canal_lantern_peace at ed_kb_out with None              # expansion; alt: ed_canal_night @ 137.02
    $ ed_sub("the night I wrote your name")
    pause 1.98                                                    # @ 139.24
    scene ed_name_retrace at ed_kb_settle with None                  # @ 139.24
    $ ed_sub("I trace it over, and over, so it can never be erased")
    pause 5.18                                                    # @ 144.5

    # === INSTRUMENTAL BREAK, Toa far =======================================
    $ ed_sub_clear()
    scene ed_bench_hill_dawn at ed_kb_settle with ed_dissolve_mid    # expansion; alt: ed_toa_bridge_far_b @ 144.5
    pause 9.3                                                    # @ 155.04

    # === FINAL CHORUS, near → sleep kiss =====================================
    scene ed_toa_bridge_final_cho at ed_kb_pan_l with op_ed_dissolve_soft           # @ 155.04
    $ ed_sub("I won't let this red string be cut")
    pause 4.46                                                    # @ 159.74
    $ ed_sub("it's fine if you never know")
    pause 4.02                                                    # @ 164.00
    scene ed_toa_bridge_hesitant at ed_kb_pan_l with None             # @ 164.00
    $ ed_sub("put into words, it would only turn to a lie")
    pause 3.3                                                    # @ 167.54
    $ ed_sub("so, saying nothing,")
    pause 3.02                                                    # @ 170.80
    scene ed_office_sleep_kiss at ed_kb_settle with None             # @ 170.80
    $ ed_sub("I kiss your sleeping form")
    pause 3.54                                                    # @ 174.58
    scene ed_sleep_red_thread at ed_kb_settle with None              # @ 174.58
    $ ed_sub("and tie the string once more")
    pause 5.18                                                    # @ 180.0

    # === OUTRO, two-shot reunion, then 終わり ================================
    $ ed_sub_clear()
    scene ed_bridge_reunion at ed_kb_settle with ed_dissolve_long    # @ 180.0
    # alt expansion outro: scene ed_canal_walk_away at ed_kb_pan_r with ed_dissolve_long
    pause 3.92                                                     # @ 184.0
    scene black with ed_dip
    show ed_end_text at ed_end_drop with op_ed_dissolve_mid
    pause 2.92
    stop music fadeout 3.5
    hide ed_end_text with op_ed_dissolve_long
    scene black with op_ed_dissolve_mid
    pause 0.92

    $ ed_sub_clear()
    hide ed_end_text
    hide ed_title_text
    hide screen cinematic_montage_overlay
    hide screen ed_escape_menu
    return
