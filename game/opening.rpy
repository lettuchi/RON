# ===========================================================================
# game/opening.rpy ,  Otome-style OPENING SEQUENCE ("OP")
# ===========================================================================
#
# An "almost-video" animated montage set to the higher-energy techno/EDM remix
# of the menu song 「嘘の街の赤い糸」 (audio/bgm/opening_op.mp3, sung Japanese vocals).
#
# Track length (read back from the rendered mp3): 90.044 s (3447 MPEG-1 L3 frames).
# Subtitles + cuts are anchored to MEASURED vocal onsets (faster-whisper "small"
# transcription of opening_op.mp3, see docs/op-timing/transcribe_op.py and
# docs/op-timing/op_timing.json), NOT an even per-section estimate. Measured line
# onsets (seconds):
#     Intro   : 7.9, 14.6
#     Verse 1 : 22.0, 24.6, 28.6, 31.8
#     Pre-Ch  : 34.8, 40.1            (instrumental gap 44.9–49.7)
#     Chorus  : 49.7, 52.7, 56.9, 60.0
#     Final   : 64.7, 66.7, 70.3, 74.3, 75.9   (vocals end ~79.7)
#     Title drop rides the instrumental outro ~80–90 s.
# Each beat's `pause` already SUBTRACTS its transition duration so the next line
# lands on its onset; the totals sum to 90.04 s. Frame-accurate sync may still
# want a small by-ear nudge, but this tracks the vocals far better than the
# earlier even-distribution pass.
#
# OP techniques applied (researched from Hakuoki OPs, Izayoi Namida / Maikaze , 
# and Otomate OPs such as Collar x Malice / Code:Realize):
#   • Ken Burns pans/zooms (op_kb_* in transforms_op_ed.rpy) on every still
#   • beat-synced cuts with white/red flashes (op_flash / op_redflash) + hpunch
#   • letterbox + edge vignette overlay (cinematic_montage_overlay screen)
#   • warm matrixcolor grade + staggered ATL fade-in baked into kb transforms
#   • character intro NAME CARDS (Toa, then Kaoru) in the upper third
#   • a chorus "everyone/story" CG montage of rapid cuts
#   • duotone red-string hero shots (op_duo)
#   • motif inserts: red string of fate, lanterns/rain, the mask of lies
#   • timed English song SUBTITLES in the lower third (translation only)
#   • a final Yuji Syuku game-title drop (subtitles suppressed under it)
#
# Skippable: built entirely from `pause` beats, so Ren'Py's normal skip
# (Ctrl / Tab) fast-forwards it and a click advances each beat, the player is
# never trapped. Music is stopped (fadeout) at the end and all OP screens are
# hidden before `return`.
#
# This file owns ONLY OP art defs (op_* / images/op/*) and the OP label/screens.
# It reuses fit_screen (ui_layout.rpy), cinematic transforms (transforms_op_ed.rpy),
# and existing bg/CG art by file path; it does not edit any externally-owned file.
# ===========================================================================

## --- OP art image defs ---------------------------------------------------
# New OP-specific art (game/images/op/, generated for this sequence).
image op_title_backdrop = At("images/op/op-title-backdrop.png", fit_screen)
image op_toa_scrolls_office = At("images/op/op-toa-scrolls-office.png", fit_screen)
image op_lanterns       = At("images/op/op-lanterns-rain.png", fit_screen)
image op_toa_card       = At("images/op/op-toa-card.png", fit_screen)
image op_kaoru_card     = At("images/op/op-kaoru-card.png", fit_screen)
image op_duo            = At("images/op/op-duo-silhouette.png", fit_screen)

# New OP two-shot art (game/images/op/, generated to break up repeated CGs).
image op_festival = At("images/op/op-festival.png", fit_screen)
image op_kotatsu  = At("images/op/op-kotatsu-mikan.png", fit_screen)
image op_umbrella = At("images/op/op-umbrella-rain.png", fit_screen)

# Canal-investigation art (game/images/op/) so EVERY montage beat is a unique
# image, no shot repeats anywhere in the OP, and the noh mask is gone.
image op_canal_confront   = At("images/op/op-canal-confront.png", fit_screen)
image op_bridge_lantern   = At("images/op/op-bridge-lantern.png", fit_screen)
image op_licensed_quarter = At("images/op/op-licensed-quarter.png", fit_screen)
image op_scorpion_comb    = At("images/op/op-scorpion-comb.png", fit_screen)

# OP expansion stills (assets/op-ed-cg-drafts/ → game/images/op/)
image op_canal_dawn       = At("images/op/op-canal-dawn.png", fit_screen)
image op_toa_dance_sil    = At("images/op/op-toa-dance-silhouette.png", fit_screen)
image op_magistrate_qtr   = At("images/op/op-magistrate-quarter.png", fit_screen)

# Reused existing art (referenced by file path; defs prefixed op_ to avoid
# colliding with the externally-owned image names).
image op_chair    = At("images/cg/cg-first-scene-chair-tension.png", fit_screen)
image op_dance    = At("images/cg/cg-first-scene-office-dance.png", fit_screen)
image op_embrace  = At("images/cg/cg-canon-embrace.png", fit_screen)
image op_pull     = At("images/cg/cg-canon-pull-close.png", fit_screen)
image op_canal    = At("images/cg/cg-case1-canal-body.png", fit_screen)

# Title drop, game name in the Yuji Syuku font (matches script.rpy styling).
image op_title_text = Text(
    "{font=fonts/YujiSyuku-Regular.ttf}Ryoko Owari Nights\n{size=44}the city of lies{/size}{/font}",
    size=92, text_align=0.5, xalign=0.5,
    outlines=[(3, "#000000dd", 0, 0), (7, "#5e0010aa", 0, 0)])


## --- Timed lyric subtitle (lower third: English translation only) -------
screen op_subtitle(romaji="", english="", n=0):
    zorder 70
    if english:
        frame:
            at op_sub_anim
            xalign 0.5
            yalign 0.90
            background "#000000a6"
            padding (36, 16)
            text english:
                xalign 0.5
                text_align 0.5
                xmaximum 1120
                size 28
                italic True
                color "#f3dada"
                outlines [(2, "#000000cc", 0, 0)]


## --- Character intro name card (upper third, left or right) --------------
screen op_namecard(name_main="", name_sub="", xa=0.06, ta=0.0, n=0):
    zorder 65
    vbox:
        at op_card_anim
        xalign xa
        yalign 0.16
        spacing 1
        text name_main:
            xalign ta
            font "fonts/YujiSyuku-Regular.ttf"
            size 54
            color "#ffffff"
            outlines [(3, "#7a0014dd", 0, 0), (6, "#00000088", 0, 0)]
        text name_sub:
            xalign ta
            size 22
            color "#f0d2d2"
            outlines [(2, "#000000cc", 0, 0)]


## --- Subtitle / name-card helpers (re-fire fade by bumping a counter) ----
default _op_sub_n = 0
default _op_card_n = 0

init python:
    def op_sub(romaji="", english=""):
        """Show a timed lower-third lyric subtitle (English translation only)."""
        store._op_sub_n += 1
        renpy.show_screen("op_subtitle", romaji=romaji, english=english,
                          n=store._op_sub_n)

    def op_sub_clear():
        renpy.hide_screen("op_subtitle")

    def op_namecard(name_main="", name_sub="", xa=0.06, ta=0.0):
        """Show a character intro name card in the upper third."""
        store._op_card_n += 1
        renpy.show_screen("op_namecard", name_main=name_main, name_sub=name_sub,
                          xa=xa, ta=ta, n=store._op_card_n)

    def op_namecard_clear():
        renpy.hide_screen("op_namecard")


## --- Escape → main menu (Replay Opening from title; call_in_new_context) ---
screen op_escape_menu():
    zorder 200
    # Non-modal: Ctrl/Tab skip and click-to-advance still reach the label.
    key "game_menu" action [
        Stop("music", fadeout=0.5),
        Hide("op_subtitle"),
        Hide("op_namecard"),
        MainMenu(confirm=False),
    ]


## ===========================================================================
## label opening_sequence ,  cleanly callable (a "Replay Opening" menu button
## can simply `call opening_sequence` later; that wiring is deferred to the
## parent since it needs screens.rpy).
## ===========================================================================
label opening_sequence:
    $ enable_cinematic_music()
    show screen op_escape_menu
    show screen cinematic_montage_overlay
    # Clean slate; SFX stays muted, music channel is on (see options.rpy).
    scene black with None
    $ op_sub_clear()
    $ op_namecard_clear()
    play music audio.bgm_opening noloop fadein 0.5

    # Cue model: `$ op_sub(...)` is placed just BEFORE its scene/transition so the
    # subtitle fades in on the vocal onset; each `pause` = (onset gap − transition
    # duration). Trailing comment = measured absolute onset (s).

    # === INTRO HOOK ========================================================
    scene op_lanterns at op_kb_in with op_ed_dissolve_mid
    pause 6.88                                                  # vocal in @ ~7.9
    $ op_sub("Uso bakari no kono machi de", "In this city full of lies")
    pause 6.72                                                  # @ ~14.6
    $ op_sub("Anata ni deatte shimatta", "I ended up meeting you")
    scene op_toa_scrolls_office at op_kb_rise with op_ed_dissolve_soft
    pause 3.65                                                  # @ ~18.3 (−0.05 for longer dissolve)
    $ op_sub_clear()
    scene op_canal_dawn at op_kb_in with op_ed_dissolve_soft       # expansion: dawn canals / cranes
    pause 3.40                                                  # instrumental @ ~18.6

    # === VERSE 1, Toa intro + the rainy canal world =======================
    $ op_sub("Chōchin no aka, nijimu ame", "Lantern-red bleeding into the rain")
    $ op_namecard("Kakita Toa", "Crane dancer, sharper eyes", xa=0.06, ta=0.0)
    scene op_toa_card at op_kb_out with op_flash
    pause 2.20                                                  # @ ~22.0
    $ op_sub("Unga ni yureru uso no akari", "Lies' light swaying on the canal")
    $ op_namecard_clear()
    scene op_festival at op_kb_pan with op_ed_dissolve_soft
    pause 3.61                                                  # @ ~24.6
    $ op_sub("Tsumetai yubisaki, fureta yoru", "The night your cold fingertips touched me")
    scene op_umbrella at op_kb_pan_l with op_ed_dissolve_soft
    pause 2.89                                                  # @ ~28.6
    $ op_sub("Soredemo hanasenakatta", "And still, I couldn't let go")
    scene op_kotatsu at op_kb_out with op_ed_dissolve_soft
    pause 2.67                                                  # @ ~31.8

    # === PRE-CHORUS, Kaoru intro, the mask of lies ========================
    $ op_sub("Anata no yasashisa mo, zankokusa mo", "Your tenderness, and your cruelty too")
    $ op_namecard("Kitsu Kaoru", "Emerald Magistrate", xa=0.94, ta=1.0)
    scene op_kaoru_card at op_kb_out with op_flash
    pause 4.86                                                  # @ ~34.8
    $ op_sub("Zenbu marugoto, uketomeru kara", "I'll take all of it, every part")
    $ op_namecard_clear()
    scene op_canal_confront at op_kb_in with op_ed_dissolve_soft
    pause 4.47                                                  # @ ~40.1
    $ op_sub_clear()
    pause 4.76                                                  # instrumental build @ ~44.9

    # === CHORUS (the drop) =================================================
    $ op_sub("Akai ito ga, musunderu", "A red string binds us together")
    scene op_duo at op_punch with op_flash
    pause 2.66                                                  # @ ~49.7
    $ op_sub("Uso no machi de, mitsuketa hontō", "the one true thing I found in the city of lies")
    scene op_embrace at op_kb_out with op_ed_dissolve_soft
    pause 3.83                                                  # @ ~52.7
    $ op_sub("Kaesarenakutemo, kono ai wa honmono", "Love doesn't need to be returned to be real")
    scene op_pull at op_kb_rise with hpunch
    pause 2.78                                                  # @ ~56.9  (key line)
    $ op_sub("Anata ga shiranakutemo, aka ni somaru kono omoi", "Even if you never know, this feeling, dyed in red")
    scene op_canal at op_kb_in with op_redflash
    pause 3.24                                                  # @ ~60.0 (−1.0 → longer bridge beat @ 64.7)

    # === FINAL CHORUS, climax =============================================
    $ op_sub("Akai ito wa, kirenai", "The red string will never break")
    scene op_bridge_lantern at op_kb_out with op_flash
    pause 2.56                                                  # @ ~64.7 (+1.0 on-screen hold; dance still @ 66.7)
    $ op_sub("Kaesarenakutemo, kono ai wa honmono", "Even unreturned, this love is real")
    scene op_toa_dance_sil at op_kb_pan with op_ed_dissolve_soft
    pause 3.29                                                  # @ ~66.7
    $ op_sub("Itsuka anata mo, kizuku hazu", "Someday, you too will realize")
    scene op_chair at op_kb_pan_l with op_ed_dissolve_soft
    pause 3.59                                                  # @ ~70.3
    $ op_sub("Soba ni iru yo, zutto", "I'll be by your side, always")
    scene op_licensed_quarter at op_kb_in with op_ed_dissolve_soft
    pause 1.33                                                  # @ ~74.3
    $ op_sub("Aka ni somaru, watashitachi no unmei", "our fate, dyed in red")
    scene op_scorpion_comb at op_kb_rise with op_redflash
    pause 3.26                                                  # @ ~75.9  (vocals end ~79.7)

    # === TITLE DROP (instrumental outro; subtitles suppressed) =============
    $ op_sub_clear()
    pause 0.50                                                  # @ ~79.7
    scene op_title_backdrop at op_kb_settle with op_ed_dissolve
    show op_title_text at op_title_drop with hpunch
    pause 5.35                                                  # title holds @ ~80.2
    stop music fadeout 2.0
    scene black with op_ed_dissolve_long
    pause 1.54                                                  # end @ ~90.0

    # Clean up every OP layer so the story starts fresh.
    $ op_sub_clear()
    $ op_namecard_clear()
    hide op_title_text
    hide screen cinematic_montage_overlay
    hide screen op_escape_menu
    $ finish_cinematic_music()
    return
