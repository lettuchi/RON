## ===========================================================================

## game/mute_audio.rpy ,  CENTRAL SFX MUTE (sound effects only)

## ===========================================================================

##

## Purpose:

##   Silence ALL sound effects (SFX) while leaving the MUSIC and VOICE channels

##   available. Story BGM is selectively muted via game/story_music_mute.rpy

##   (menu + opening + ending only); this file still only touches the sfx mixer.

##   The scattered `play sound` / `stop` statements in the story scripts are

##   intentionally left in place; SFX is neutralized here so muting is a single-

##   spot, reversible change.

##

## How it works:

##   1. config.default_sfx_volume below sets the initial "sfx" mixer volume to

##      0.0 for FRESH persistent state (a brand-new player profile). Music mixer

##      defaults live in game/options.rpy + story_music_mute.rpy.

##   2. The start/after-load callbacks force the "sfx" mixer volume to 0.0 at

##      runtime, which ALSO covers existing saves / persistent data that already

##      have a non-zero stored volume. Output volume is mixer * secondary, so a

##      0.0 mixer silences the channel no matter what per-line `volume` clauses

##      the scripts pass.

##   3. The "music" and "voice" mixers are not touched here. Music volume is

##      managed by story_music_mute.rpy (story silent; menu/OP/ED audible).

##

## TO REVERT (restore SFX too):

##   1. Delete this file (game/mute_audio.rpy).

##   2. In game/options.rpy, set:

##        define config.has_sound = True

##   3. To also restore all story BGM, follow revert steps in

##      game/story_music_mute.rpy and set config.default_music_volume = 1.0

## ===========================================================================



## Fresh-profile mixer default: SFX silenced. (Music volume is set in

## game/options.rpy + story_music_mute.rpy; voice untouched.)

define config.default_sfx_volume = 0.0



init python:



    def _mute_sfx_audio(*args, **kwargs):

        # Force the sfx mixer to silence, overriding any volume already stored in

        # existing saves / persistent data. Music and voice are deliberately left

        # untouched here (see story_music_mute.rpy for music).

        renpy.game.preferences.set_volume("sfx", 0.0)



    ## Apply on a new game and after loading any save, so every entry point is

    ## covered regardless of pre-existing persistent volumes.

    config.start_callbacks.append(_mute_sfx_audio)

    config.after_load_callbacks.append(_mute_sfx_audio)

