## ===========================================================================
## game/story_music_mute.rpy ,  selective story BGM mute (mixer-based)
## ===========================================================================
##
## Purpose:
##   Keep the music mixer audible only for the main menu theme, opening
##   cinematic, and ending cinematic. All other `play music` lines in story
##   scripts still run but are inaudible (mixer at 0.0). SFX remains muted via
##   game/mute_audio.rpy. Do not re-enable sound there.
##
## Mechanism:
##   - config.default_music_volume = 0.5 (game/options.rpy) for fresh profiles
##   - start/after_load callbacks force the "music" preference mixer to 0.0
##   - screen main_menu on "show" sets mixer to 1.0 for config.main_menu_music
##   - opening_sequence / ed_sequence / kaoru_image_song_sequence /
##     toa_image_song_sequence / duet_song_sequence call
##     enable_cinematic_music() at entry and
##     finish_cinematic_music() before return (restores menu volume when replayed
##     from the title via _cinematic_from_menu)
##   - Modern AU bonus episodes set au_episode_active = True (their story BGM is
##     meant to be audible); the start/after_load callback keeps the mixer at 1.0
##     while that flag is set, then the AU hub (au_modern_hub_menu) clears it
##
## TO REVERT (restore story BGM everywhere):
##   1. Delete this file (game/story_music_mute.rpy).
##   2. In game/options.rpy, set: define config.default_music_volume = 1.0
##   3. Remove enable/finish lines from opening.rpy, ed_sequence.rpy,
##      kaoru_image_song.rpy, toa_image_song.rpy
##   4. Remove main_menu on "show" and SetVariable replay actions from screens.rpy
##   5. Restore game/mute_audio.rpy header if you edited it for this feature
## ===========================================================================

default _cinematic_from_menu = False

## True only while a Modern AU bonus episode is running. Saved with the game, so
## loading a mid-AU save resumes with story BGM audible (see _apply_story_music_mute).
## Set True in each au_modern_*_start label; cleared at the AU hub (au_modern_hub_menu).
default au_episode_active = False

init python:

    STORY_MUSIC_VOLUME = 0.0
    CINEMATIC_MUSIC_VOLUME = 1.0

    def enable_cinematic_music():
        renpy.game.preferences.set_volume("music", CINEMATIC_MUSIC_VOLUME)

    def disable_cinematic_music():
        renpy.game.preferences.set_volume("music", STORY_MUSIC_VOLUME)

    def finish_cinematic_music():
        disable_cinematic_music()
        if store._cinematic_from_menu:
            store._cinematic_from_menu = False
            enable_cinematic_music()

    def _apply_story_music_mute(*args, **kwargs):
        ## Runs at game start and after every load. Canon story BGM stays muted
        ## (mixer 0.0); but a Modern AU episode wants its story BGM audible, so when
        ## au_episode_active is set (incl. when restored from a mid-AU save) keep the
        ## mixer at cinematic volume instead of muting.
        if getattr(store, "au_episode_active", False):
            enable_cinematic_music()
        else:
            disable_cinematic_music()

    config.start_callbacks.append(_apply_story_music_mute)
    config.after_load_callbacks.append(_apply_story_music_mute)


## Modern AU hub, driven from the rollback-enabled root/game context ###########
##
## The Modern AU bonus episodes used to launch from the au_modern_hub screen via
## renpy.call_in_new_context(...). That spawns a NON-rollback context whose
## saves belong to the parked main-menu context, so inside an AU episode the
## Back button / rollback did nothing and a mid-AU save could not resume.
##
## Now the main-menu "Bonus: Modern AU" entry does Start("au_modern_hub_menu"),
## which jumps OUT of the menu context into the root/game context (rollback
## enabled, the real save context) at this label. The hub is shown with
## `call screen au_modern_hub`, the chosen episode runs in this same context, and
## each episode's return path jumps back here. Because everything lives in the
## rollback-enabled root context, Back/rollback works and mid-AU saves resume.
##
## Music isolation is preserved here: clear au_episode_active (we are at the
## menu, not in an episode) and restore the audible menu theme; each episode
## re-arms au_episode_active and plays its own story BGM.

label au_modern_hub_menu:

    $ au_episode_active = False
    $ enable_cinematic_music()
    $ renpy.music.play(config.main_menu_music, if_changed=True, fadein=config.main_menu_music_fadein)

    call screen au_modern_hub

    ## "Back" (or any non-label result): leave the AU hub. A top-level return in
    ## the root context drops us back to the main menu, exactly like the canon
    ## endings' "Return to title".
    if _return == "__au_hub_back__" or not isinstance(_return, str):
        return

    ## Otherwise launch the chosen episode (or dev menu) in this same context.
    jump expression _return
