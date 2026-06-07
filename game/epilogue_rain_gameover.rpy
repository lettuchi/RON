# Epilogue, Rain Game Over (bad end).
#
# Trigger: prologue_refuse_bad_end → "Leave the magistrate's office."
# Toa refuses the dance, walks out without a seal, and flees into the rain.
# After the rain CG sequence, ronin corner her; implied brothel sale (fade-to-black).
#
# Conventions reused from prologue.rpy / scene_layering.rpy:
#   * `$ show_cg_scene("<tag>")` shows full-screen `cg <tag>` and shrinks sprites.
#   * `$ set_expression("toa", "<expr>")` keeps the full sprite offstage and only
#     updates the textbox bust, used for dialogue over a CG.
#   * Endings end on a black `centered` title card then `return` (to main menu).
#
# DEV content warning: implied abduction / trafficking, horror-tragedy tone only;
# no graphic scenes, no new explicit CGs.
#
# Only Toa sprite attributes defined in game/images/characters.rpy are used:
#   neutral / happy / sad / angry / surprised / flustered / worried /
#   thinking / determined / soft. (Kaoru is not present in the rain.)
#
# NEW flag owned by this epilogue (stats.rpy is owned by another agent):
default seen_gameover_rain = False

# --- Bad-end CGs (1920x1080, no text). PNGs live in images/cg/. ---
# GenerateImage prompts for each beat are recorded above each definition so the
# parent agent can regenerate them. Reference image: the canonical Toa sprite
# game/images/sprites/toa/toa-neutral.png (per vn-art-pipeline skill).
#
# cg-gameover-rain-flee.png:
#   Anime otome visual novel CG, Hakuoki-style polished shoujo art, cinematic
#   lighting, painterly background. Kakita Toa: tall slender woman, white hair,
#   white eyelashes, grey eyes, bright expressive face; black kosode kimono
#   (standard sleeves, NOT furisode), gold obi embroidered with a crane bird in
#   flight (spread wings), white hakama, zori. Toa bursting out through a sliding
#   shoji doorway of an Emerald Magistrate's office into a rainy night, mid-stride,
#   clutching a permit book to her chest, brave determined mask cracking toward
#   fear, hair and kimono starting to soak. Warm lantern light behind her, cold
#   blue rain ahead. Legend of the Five Rings Ryoko Owari aesthetic, corrupt
#   Scorpion canal city at night. Wide 16:9, 1920x1080, no text, no watermark, no UI.
image cg gameover_rain_flee = At("images/cg/cg-gameover-rain-flee.png", fit_cg)

# cg-gameover-rain-run.png:
#   Anime otome visual novel CG, Hakuoki-style polished shoujo art, cinematic
#   lighting, painterly background. Same Kakita Toa (white hair, white eyelashes,
#   grey eyes, black kosode kimono, gold crane-in-flight obi, white hakama).
#   Toa running down a lantern-lit canal street in heavy rain at night, full of
#   motion, rain-soaked hair and kimono clinging, reflections of orange paper
#   lanterns in black canal water, wet cobblestones, narrow Scorpion-district
#   wooden buildings. Dynamic running pose, bittersweet desperate energy. Legend
#   of the Five Rings Ryoko Owari aesthetic. Wide 16:9, 1920x1080, no text, no UI.
image cg gameover_rain_run = At("images/cg/cg-gameover-rain-run.png", fit_cg)

# cg-gameover-rain-alone.png:
#   Anime otome visual novel CG, Hakuoki-style polished shoujo art, cinematic
#   lighting, painterly background. Same Kakita Toa (white hair, white eyelashes,
#   grey eyes, black kosode kimono, gold crane-in-flight obi, white hakama).
#   Toa alone and small in a downpour at the edge of lantern light on a deserted
#   canal street at night, seen from a distance, shoulders set with stubborn pride
#   but isolated and lost, rain blurring the city into grey, a single guttering
#   paper lantern. Melancholy bittersweet bad-end framing, lots of negative space.
#   Legend of the Five Rings Ryoko Owari aesthetic. Wide 16:9, 1920x1080, no text, no UI.
image cg gameover_rain_alone = At("images/cg/cg-gameover-rain-alone.png", fit_cg)

# Brothel-path bad end (prologue_bad_end_brothel), see cgs-badend-prologue.rpy for defs.


label gameover_rain:

    # Arrives from prologue_refuse_bad_end → "Leave the magistrate's office."
    $ seen_gameover_rain = True
    play music audio.bgm_bad_end_rain fadein 2.0 loop volume 0.6

    scene bg street_exterior with fade
    show toa sad at right

    voice "audio/voice/narrator_039.mp3"
    "Outside, the canal district smells honest, fish, copper, rain on stone."

    # Beat 1, into the rain (refuse-leave skips flee CG; corridor_lost already shown)
    $ show_cg_scene("gameover_rain_run", fade)
    play sound audio.footsteps_corridor volume 0.7

    voice "audio/voice/narrator_103.mp3"
    "Down the canal road the lanterns bleed orange into black water. Copper and cheap incense, wet stone and old smoke, Ryoko Owari breathing on the back of her neck."

    voice "audio/voice/narrator_104.mp3"
    "Scorpion country doesn't shout. It watches a soaked Crane girl splash past, decides she is no one worth a second glance, and lets the rain do the rest."

    $ set_expression("toa", "worried")
    voice "audio/voice/toa_204.mp3"
    toa "No seal. No patron. No permit that means anything. By morning a gate guard asks for paper, and I have a wet book and a very good bow."

    # Beat 2, alone in the downpour
    $ show_cg_scene("gameover_rain_alone")

    voice "audio/voice/narrator_105.mp3"
    "She slows where the lamplight gives out. Past it the city is only rain and the shape of rain."

    voice "audio/voice/narrator_106.mp3"
    "She kept her pride. She picked it up off the magistrate's desk, whole, and carried it out under her arm. Tonight it is the only thing she owns in Ryoko Owari."

    $ set_expression("toa", "soft")
    voice "audio/voice/toa_203.mp3"
    toa "...Snacks first. Pride second. I finally got the order right."

    $ set_expression("toa", "sad")
    voice "audio/voice/toa_202.mp3"
    toa "Pity there was never a third."

    jump prologue_bad_end_brothel


# --- DEV: content warning; implied abduction / trafficking; fade-to-black only. ---

label prologue_bad_end_brothel:

    play music audio.bgm_bad_end_brothel fadein 2.5 loop volume 0.5

    $ show_cg_scene("badend_brothel_crying", fade)

    voice "audio/voice/narrator_226.mp3"
    "The lamplight ends. What is left is rain on white hair and a bow that will not hold."

    voice "audio/voice/narrator_225.mp3"
    "On stage she could make grief look graceful. Here there is no audience, only the canal breathing back her own shaking."

    $ show_cg_scene("badend_brothel_tears")

    $ set_expression("toa", "worried")
    voice "audio/voice/toa_210.mp3"
    toa "Crane don't... Crane don't break in public."

    voice "audio/voice/toa_209.mp3"
    toa "Mother taught me the spine first. The smile second. I kept both until tonight."

    voice "audio/voice/narrator_224.mp3"
    "She presses her forehead to the permit book. The paper is pulp. The crane on the obi is the only thing still dry enough to pretend it flies."

    $ show_cg_scene("badend_brothel_permit")

    $ set_expression("toa", "sad")
    voice "audio/voice/toa_208.mp3"
    toa "Three provinces of ink, and not one line that says I may sleep indoors."

    voice "audio/voice/narrator_223.mp3"
    "She tries to flatten the pages with her palm. The rain wins. Somewhere a magistrate's hanko dries by his stove while she dissolves on a corner stone."

    play sound audio.footsteps_corridor volume 0.55
    voice "audio/voice/narrator_222.mp3"
    "A side alley mouths open between two shuttered tea houses, dry enough to stand, narrow enough to trap."

    voice "audio/voice/narrator_221.mp3"
    "She stumbles in to wipe her face. Her reflection in a puddle is a stranger's, smaller, older, already bargaining."

    $ show_cg_scene("badend_brothel_ronin")

    voice "audio/voice/narrator_220.mp3"
    "Boots scrape stone behind her. Two ronin, hired by the cut of their silence, not the color of their haori."

    "\"Wrong quarter for a Crane without a chop, little bird.\""

    "\"Pretty hair. Wet obi. No magistrate's escort. The okami at the House of Falling Lanterns pays coin for that bargain.\""

    $ set_expression("toa", "angry")
    voice "audio/voice/toa_207.mp3"
    toa "I'm Kakita. I'm not inventory."

    voice "audio/voice/toa_206.mp3"
    toa "Touch me and I'll memorize your face for when I'm allowed a sword again."

    "\"Everything without a seal is for sale.\""

    "\"Hold her arms.\""

    $ show_cg_scene("badend_brothel_grasp")

    voice "audio/voice/narrator_219.mp3"
    "A hand on her shoulder. Another on the permit book, tearing it free like spoiled fruit."

    $ set_expression("toa", "worried")
    voice "audio/voice/toa_205.mp3"
    toa "Please... the book... that's all I..."

    "\"Paper don't pay the okami. You do.\""

    voice "audio/voice/narrator_218.mp3"
    "She twists. Crane training was for stages and polite duels, not alley brawls. They have the numbers. She has pride, and pride does not block three men."

    centered "{size=-2}This ending is brutal. Implied violence ahead.{/size}"

    menu:
        "Continue.":
            pass

        "Return to title.":
            stop music fadeout 1.5
            return

    window hide
    $ show_cg_scene("badend_brothel_cart", fade)

    voice "audio/voice/narrator_217.mp3"
    "A fist in her obi. A gag that tastes of cheap sake and river mud."

    voice "audio/voice/narrator_216.mp3"
    "The alley becomes a cart under oilcloth. The cart becomes a door that smells of incense too sweet to be prayer, rouge and bruised plums and someone else's laughter behind thin walls."

    pause 0.6

    voice "audio/voice/narrator_215.mp3"
    "They write her name the way the city writes drowning: not on a funeral stone, but on a ledger line."

    voice "audio/voice/narrator_214.mp3"
    "Kakita Toa will not be asked to sign it."

    pause 0.5

    stop music fadeout 3.0
    scene black with fade
    pause 0.6

    centered "{size=+14}Game Over{/size}"
    pause 0.4

    centered "{size=+4}The End{/size}\n{size=-4}Kakita Toa kept her pride.\nRyoko Owari sold what the magistrate would not stamp.{/size}"

    return
