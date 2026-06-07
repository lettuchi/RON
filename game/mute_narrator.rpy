## ===========================================================================
## game/mute_narrator.rpy , VOICE PREFERENCE DEFAULTS (one-time migration)
## ===========================================================================
##
## Purpose:
##   Set the INITIAL default for the two in-game voice toggles, then get out of
##   the way. The toggles live in the Preferences screen (game/screens.rpy):
##     * "Character Voices" -> voice_tag "character" (Toa, Kaoru, ...)
##     * "Narrator Voice"   -> voice_tag "narrator"  (bare-string narration)
##   Both are backed by Ren'Py's persistent._voice_mute set (a tag in the set =
##   muted). The Preferences toggles are the SINGLE SOURCE OF TRUTH for voice
##   muting; this file only seeds a sane default the very first time a player
##   runs a build that has the toggles, and never overrides their choice again.
##
## Why this changed:
##   This file used to FORCE-add / FORCE-discard "narrator" in persistent.
##   _voice_mute on EVERY start and after_load. That made narration mute state
##   non-configurable and would clobber the new Preferences toggle on every load.
##   Now narration VO is shipping enabled, the player can mute character voices
##   and/or narration independently from Preferences, and that choice persists.
##
## How it works (verified against the Ren'Py 8.5.3 SDK, renpy/common/00voice.rpy):
##   * game/images/characters.rpy tags speakers:
##         toa / kaoru ... voice_tag="character"
##         narrator    ... voice_tag="narrator"
##     A bare `voice` statement inherits the tag of the character who speaks the
##     next line, so narration plays under "narrator" and Toa/Kaoru lines play
##     under "character".
##   * voice_interact() silences the voice channel when the current line's tag is
##     in persistent._voice_mute:
##         if (not volume) or (_voice.tag in persistent._voice_mute):
##             renpy.sound.stop(channel="voice")
##   * The Preferences screen drives that set with ToggleVoiceMute(tag, True)
##     (invert=True => the checkbox is "selected" when the tag is NOT muted, i.e.
##     ON / audible). persistent._voice_mute is created at init -1500 in
##     00voice.rpy and persists across save/load and restart.
##
## Default for a brand-NEW player: both Character Voices and Narrator Voice = ON
## (audible). The mute set starts empty, so "new player = everything audible"
## needs no action beyond marking the one-time migration done. Existing players'
## choices are preserved: after the migration flag is set we never touch the set.
##
## TO FULLY REVERT (undo the voice-tagging feature):
##   1. Delete this file (game/mute_narrator.rpy).
##   2. In game/images/characters.rpy remove voice_tag="character" from toa/kaoru
##      and the voice_tag="narrator" narrator define block.
##   3. Remove the "Voice" toggle vbox from the preferences screen in
##      game/screens.rpy.
##   Untagged voice lines are never muted, so audio fully restores.
## ===========================================================================

## DEPRECATED / RETIRED: kept only so any stray external reference still resolves.
## This flag no longer does anything. Narration muting is now controlled entirely
## by the "Narrator Voice" toggle in Preferences (persistent._voice_mute). Do not
## reintroduce a forced-mute callback here; it would clobber the player's choice.
define MUTE_NARRATOR_VOICE = False

init 100 python:

    def _seed_voice_pref_defaults(*args, **kwargs):
        # persistent._voice_mute is created in 00voice.rpy (init -1500); guard anyway.
        if persistent._voice_mute is None:
            persistent._voice_mute = set()

        # ONE-TIME migration. For a player who has never had the voice toggles,
        # seed the default (both Character Voices and Narrator Voice = ON, i.e.
        # neither tag muted), then mark it done. After this, the Preferences
        # toggles are authoritative and we never override the player's choice.
        if not persistent._ryoko_voice_prefs_initialized:
            persistent._voice_mute.discard("narrator")
            persistent._voice_mute.discard("character")
            persistent._ryoko_voice_prefs_initialized = True

    # Run once at startup (before the first interaction). It is also harmless on
    # later starts/loads because the migration flag makes it a no-op, so existing
    # saves are covered too without ever clobbering a deliberately-muted tag.
    _seed_voice_pref_defaults()
    config.start_callbacks.append(_seed_voice_pref_defaults)
    config.after_load_callbacks.append(_seed_voice_pref_defaults)
