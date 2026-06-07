# ===========================================================================
# game/trailer.rpy , "Watch Trailer" , fullscreen, skippable cel-trailer player
# ===========================================================================
#
# Plays the rendered proof-of-concept trailer (trailer/out/ryoko-owari-trailer-v1.webm,
# built by scripts/build_trailer.py) fullscreen via a Ren'Py Movie displayable. The
# clip carries its own audio bed (music + voice, see trailer/audio_overlays.json), so
# the menu BGM is stopped while it plays and restored on return.
#
# Skippable, exactly like opening_sequence / the image-song replays: click anywhere
# or press Escape -> back to the Main Menu. It also returns to the menu on its own
# when the ~90 s trailer finishes.
#
# NON-INVASIVE BY DESIGN:
#   * The "Watch Trailer" button is added via a main-menu-only OVERLAY screen
#     (config.overlay_screens), so this file does NOT edit screens.rpy.
#   * If you would rather put the entry in the normal nav list, delete the overlay
#     block below and add this ONE line inside `screen navigation():` (screens.rpy),
#     in the `if main_menu:` branch (see trailer/README.md):
#
#         textbutton _("Watch Trailer") action Function(renpy.call_in_new_context, "trailer_play")
#
#   * The render lives at <basedir>/trailer/out/ , OUTSIDE game/ , so we add the
#     project base dir to config.searchpath (append-only) instead of moving the file
#     into game/ or editing any externally-owned file.
#
# This file owns ONLY the trailer Movie defs, its label, and its screens.
# It reuses config.main_menu_music (options.rpy) and the MainMenu()/key "game_menu"
# escape pattern (opening.rpy); it does not edit any externally-owned file.
# ===========================================================================

## --- Config: where the rendered trailer lives + how long it runs -----------
# Paths are relative to the project base dir (added to config.searchpath below).
define TRAILER_WEBM = "trailer/out/ryoko-owari-trailer-v1.webm"
define TRAILER_MP4 = "trailer/out/ryoko-owari-trailer-v1.mp4"
# Trailer length matches trailer/shotlist.json config.duration (the OP track length).
define TRAILER_DURATION = 90.044

init python:
    import os

    # Make <basedir>/trailer/out/* loadable by Movie() without moving the file into
    # game/. Append the base dir to the search path and clear the dir-file cache so
    # the new directory is indexed. Append-only and idempotent.
    _trailer_basedir = getattr(renpy.config, "basedir", None)
    if _trailer_basedir and _trailer_basedir not in config.searchpath:
        config.searchpath.append(_trailer_basedir)
        try:
            renpy.loader.cleardirfiles()
        except Exception:
            pass

    def _trailer_source():
        """Loadable trailer path (webm preferred, mp4 fallback), or None if unbuilt."""
        for rel in (TRAILER_WEBM, TRAILER_MP4):
            try:
                if renpy.loadable(rel):
                    return rel
            except Exception:
                pass
        return None


## --- Fullscreen player screen ----------------------------------------------
# Modal so the player's own click/Escape handling drives skipping (the trailer's
# audio is on the auto-selected movie channel; hiding the Movie stops it).
screen trailer_player(src):
    zorder 100
    modal True

    add Solid("#000000")

    # 16:9 trailer scaled to the 16:9 game surface; loop off so it plays once.
    add Movie(play=src, size=(config.screen_width, config.screen_height), loop=False):
        xalign 0.5
        yalign 0.5

    # Escape -> Main Menu (mirrors op_escape_menu in opening.rpy).
    key "game_menu" action [Stop("movie", fadeout=0.3), MainMenu(confirm=False)]

    # Click anywhere -> Main Menu.
    button:
        xfill True
        yfill True
        background None
        action [Stop("movie", fadeout=0.3), MainMenu(confirm=False)]

    text _("Click or Esc to skip"):
        xalign 0.985
        yalign 0.965
        size 18
        color "#ffffffcc"
        outlines [(2, "#000000aa", 0, 0)]


## --- "Trailer not built yet" notice (graceful pre-render fallback) ----------
screen trailer_missing():
    zorder 100
    modal True
    key "game_menu" action Return()
    add Solid("#0a1215")
    vbox:
        align (0.5, 0.5)
        spacing gui.scale(18)
        xmaximum gui.scale(900)
        text _("The trailer hasn't been rendered yet."):
            xalign 0.5
            font "fonts/YujiSyuku-Regular.ttf"
            size gui.scale(34)
            color "#e8d5a3"
            outlines [(3, "#0a1218cc", 0, 0)]
        text _("Build it with:  python scripts/build_trailer.py\n(see trailer/README.md for the full pipeline)"):
            xalign 0.5
            text_align 0.5
            size gui.scale(20)
            color "#9ab0b3"
            outlines [(2, "#000000aa", 0, 0)]
        textbutton _("Back"):
            xalign 0.5
            action Return()
            text_size gui.scale(24)


## ===========================================================================
## label trailer_play , cleanly callable (the menu hooks call it via
## renpy.call_in_new_context, so its play/stop stay isolated and `return`
## lands back on the main menu with config.main_menu_music restored).
## ===========================================================================
label trailer_play:
    $ enable_cinematic_music()
    stop music fadeout 0.5
    $ _trailer_src = _trailer_source()
    if _trailer_src is None:
        call screen trailer_missing
        $ finish_cinematic_music()
        return
    window hide
    show screen trailer_player(_trailer_src)
    # Modal player eats clicks, so this pause only ends on the trailer's natural
    # length; Escape/click skip to the menu through the screen handlers above.
    $ _trailer_runtime = TRAILER_DURATION + 0.5
    pause _trailer_runtime
    hide screen trailer_player
    stop movie
    $ finish_cinematic_music()
    return


## --- Main-menu-only "Watch Trailer" overlay (no screens.rpy edit) -----------
# Shown only while the main_menu screen itself is up (not in-game, not submenus).
screen trailer_menu_overlay():
    if renpy.get_screen("main_menu"):
        textbutton _("Watch Trailer"):
            style "main_menu_nav_button"
            xalign 1.0
            xoffset gui.scale(-55)
            yalign 0.9
            action Function(renpy.call_in_new_context, "trailer_play")

init python:
    if "trailer_menu_overlay" not in config.overlay_screens:
        config.overlay_screens.append("trailer_menu_overlay")
