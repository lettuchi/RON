# Background music, placeholders from scripts/synthesize_bgm.py
# Replace with GarageBand exports (see docs/garageband-bgm-guide.md)

# Main-menu opening song, sung Japanese vocals (Eleven Music composition_plan).
# The procedural placeholder main_menu.ogg is kept on disk but no longer referenced.
define audio.bgm_main_menu     = "audio/bgm/main_menu_song.mp3"
define audio.bgm_corridor        = "audio/bgm/corridor.ogg"
# Eleven Music export (2026-06-04). Legacy office.ogg remains on disk but was file-locked during regen.
define audio.bgm_office          = "audio/bgm/office.mp3"
define audio.bgm_street          = "audio/bgm/street.ogg"
# Case-specific instrumental beds (Eleven Music, see docs/elevenlabs-music-prompts.md).
define audio.bgm_case1_barge       = "audio/bgm/case1_barge.mp3"
define audio.bgm_case2_festival    = "audio/bgm/case2_festival.mp3"
define audio.bgm_case3_fabric      = "audio/bgm/case3_fabric.mp3"
define audio.bgm_case3_5_date      = "audio/bgm/case3_5_date.mp3"
define audio.bgm_case4_dock        = "audio/bgm/case4_dock.mp3"
define audio.bgm_case4_5_kobune    = "audio/bgm/case4_5_kobune.mp3"
define audio.bgm_case5_tease       = "audio/bgm/case5_tease.mp3"
define audio.bgm_case5_hearing     = "audio/bgm/case5_tease.mp3"  # reuse until dedicated hearing bed exists
define audio.bgm_bad_end_rain      = "audio/bgm/bad_end_rain.mp3"
define audio.bgm_bad_end_brothel   = "audio/bgm/bad_end_brothel.mp3"
define audio.bgm_bad_end_punishment = "audio/bgm/bad_end_punishment.mp3"
define audio.bgm_toa_theme       = "audio/bgm/toa_theme_new.mp3"
define audio.bgm_kaoru_theme     = "audio/bgm/kaoru_theme_new.mp3"
define audio.bgm_canon_intimate  = "audio/bgm/canon_intimate.ogg"
define audio.bgm_bad_ending      = "audio/bgm/bad_ending.mp3"
# Opening sequence ("OP"), higher-energy techno/EDM remix of the menu song with
# sung Japanese vocals (used by game/opening.rpy → label opening_sequence).
define audio.bgm_opening         = "audio/bgm/opening_op.mp3"
# Ending sequence ("ED"), slow noir piano ballad 「嘘つきの糸」/ "The Liar's String"
# (Kaoru's POV, 190.01 s) with sung Japanese vocals; used by
# game/ed_sequence.rpy → label ed_sequence.
define audio.bgm_ending          = "audio/bgm/ending_song.mp3"
# Kaoru image song: 「権利の帳」 / Kenri no Chō (primary + optional archived gens).
# Used by game/kaoru_image_song.rpy → label kaoru_image_song_sequence.
# See docs/kaoru-image-song-versions.md
define audio.bgm_kaoru_kenri     = "audio/bgm/kaoru_image_song_kenri.mp3"  # primary (~222 s, latest)
# Toa image song: 「赤い糸の灯」 / Akai Ito no Hi (heroine image song).
# Used by game/toa_image_song.rpy → label toa_image_song_sequence.
# See docs/toa-image-song-versions.md
define audio.bgm_toa_image       = "audio/bgm/toa_image_song.mp3"
# Toa + Kaoru duet: 「嘘の夜を走れ」 / Uso no Yoru o Hashire (high-energy anime duet).
# Used by game/duet_song.rpy → label duet_song_sequence.
# See docs/duet-song-versions.md
define audio.bgm_duet            = "audio/bgm/duet_song.mp3"

init -1 python:
    for _attr, _fname in (
        ("bgm_kaoru_kenri_v1", "kaoru_image_song_kenri_v1_original.mp3"),
        ("bgm_kaoru_kenri_v2", "kaoru_image_song_kenri_v2_energetic.mp3"),
        ("bgm_kaoru_kenri_v3", "kaoru_image_song_kenri_v3_hakuoki.mp3"),
    ):
        _path = "audio/bgm/" + _fname
        if renpy.loadable(_path):
            setattr(store.audio, _attr, _path)
