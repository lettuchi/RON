# Character definitions and dialogue sprites.
# Kaoru disdain: use cold (kaoru-cold.png); contempt sprite removed as too extreme.

# VOICE TOGGLES: every non-narrator speaking Character shares voice_tag="character"
# so the in-game Preferences "Character Voices" toggle can mute/unmute them as a
# group (via persistent._voice_mute). The narrator keeps voice_tag="narrator" so
# the separate "Narrator Voice" toggle controls narration independently. See the
# Voice section of game/screens.rpy and the migration in game/mute_narrator.rpy.
define toa = Character("Toa", color="#c0c0c0", image="toa", voice_tag="character", callback=name_callback, cb_name="toa")
define kaoru = Character("Kaoru", color="#d4af37", image="kaoru", voice_tag="character", callback=name_callback, cb_name="kaoru")

# NARRATOR voice tag (drives the "Narrator Voice" preference toggle) -------------
# Replicates Ren'Py 8.5.3's DEFAULT narrator from renpy/common/00definitions.rpy:
#     Character(None, kind=adv, what_style='say_thought')
# and adds voice_tag="narrator" so bare-string "..." narration can be muted as a
# group from Preferences. Bare `voice` statements inherit the narrator tag, so
# every narrator_*.mp3 plays under "narrator". The default state is set once by
# game/mute_narrator.rpy; the Preferences toggle is authoritative thereafter.
define narrator = Character(None, kind=adv, what_style='say_thought', voice_tag="narrator", callback=name_callback, cb_name=None)
# -------------------------------------------------------------------------------

# Toa outfit groups: work = witness kosode (default); date = Case 3.5 furisode set.
# bashful / embarrassed / twitterpated exist only under date: use work flustered/soft if needed elsewhere.
layeredimage toa:
    at sprite_highlight('toa')
    group outfit:
        attribute work default null
        attribute date null
    group expression:
        attribute neutral default:
            "images/sprites/toa/toa-neutral.png"
            when work
        attribute neutral:
            "images/sprites/toa/date/toa-date-neutral.png"
            when date
        attribute happy:
            "images/sprites/toa/toa-happy.png"
            when work
        attribute happy:
            "images/sprites/toa/date/toa-date-happy.png"
            when date
        attribute sad:
            "images/sprites/toa/toa-sad.png"
            when work
        attribute sad:
            "images/sprites/toa/date/toa-date-sad.png"
            when date
        attribute angry:
            "images/sprites/toa/toa-angry.png"
            when work
        attribute angry:
            "images/sprites/toa/date/toa-date-angry.png"
            when date
        attribute surprised:
            "images/sprites/toa/toa-surprised.png"
            when work
        attribute surprised:
            "images/sprites/toa/date/toa-date-surprised.png"
            when date
        attribute flustered:
            "images/sprites/toa/toa-flustered.png"
            when work
        attribute flustered:
            "images/sprites/toa/date/toa-date-flustered.png"
            when date
        attribute worried:
            "images/sprites/toa/toa-worried.png"
            when work
        attribute worried:
            "images/sprites/toa/date/toa-date-worried.png"
            when date
        attribute thinking:
            "images/sprites/toa/toa-thinking.png"
            when work
        attribute thinking:
            "images/sprites/toa/date/toa-date-thinking.png"
            when date
        attribute determined:
            "images/sprites/toa/toa-determined.png"
            when work
        attribute determined:
            "images/sprites/toa/date/toa-date-determined.png"
            when date
        attribute soft:
            "images/sprites/toa/toa-soft.png"
            when work
        attribute soft:
            "images/sprites/toa/date/toa-date-soft.png"
            when date
        attribute bashful:
            "images/sprites/toa/date/toa-date-bashful.png"
            when date
        attribute embarrassed:
            "images/sprites/toa/date/toa-date-embarrassed.png"
            when date
        attribute twitterpated:
            "images/sprites/toa/date/toa-date-twitterpated.png"
            when date

layeredimage kaoru:
    at sprite_highlight('kaoru')
    group expression:
        attribute neutral:
            "images/sprites/kaoru/kaoru-neutral.png"
        attribute smirk default:
            "images/sprites/kaoru/kaoru-smirk.png"
        attribute cold:
            "images/sprites/kaoru/kaoru-cold.png"
        attribute charm:
            "images/sprites/kaoru/kaoru-charm.png"
        attribute cruel:
            "images/sprites/kaoru/kaoru-cruel.png"
        attribute angry:
            "images/sprites/kaoru/kaoru-angry.png"
        attribute amused:
            "images/sprites/kaoru/kaoru-amused.png"
        attribute bored:
            "images/sprites/kaoru/kaoru-bored.png"
        attribute thinking:
            "images/sprites/kaoru/kaoru-thinking.png"
        attribute determined:
            "images/sprites/kaoru/kaoru-determined.png"
        attribute surprised:
            "images/sprites/kaoru/kaoru-surprised.png"
        attribute commanding:
            "images/sprites/kaoru/kaoru-commanding.png"
        attribute hungry:
            "images/sprites/kaoru/kaoru-hungry.png"
        attribute satisfied:
            "images/sprites/kaoru/kaoru-satisfied.png"
        attribute furious:
            "images/sprites/kaoru/kaoru-furious.png"
        attribute vicious:
            "images/sprites/kaoru/kaoru-vicious.png"
        attribute ravenous:
            "images/sprites/kaoru/kaoru-ravenous.png"
        attribute threatening:
            "images/sprites/kaoru/kaoru-threatening.png"
        attribute sadistic:
            "images/sprites/kaoru/kaoru-sadistic.png"

# Stage transforms (left / right / center) live in ui_layout.rpy.
