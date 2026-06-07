# Case 4.5, Stress Reduction and Small Boats (舟の帳).
# Discord: docs/discord-threads-raw.md § Stress Reduction and Small Boats.
# Entry: case4_post_case4_bridge when case4_5_boat_interlude_eligible().
# Exit: case5_investigation_start (or gameover_case4_5_boat on throw-fight bad end).
# VOICED: Case 4.5 manifest pass (2026-06-03). toa_173-191, kaoru_206-224, narrator_174-182.

label case4_5_boat_interlude:

    $ case4_5_boat_interlude_seen = True

    scene bg magistrate_office with dissolve
    play music audio.bgm_office fadein 1.5 loop volume 0.45
    show kaoru commanding at left
    show toa determined at right

    voice "audio/voice/narrator_174.mp3"
    "Case Four's ink is barely dry. The first hard cold has come early off the bay, and with it the season's Scorpion raids have the harbor clerks lying about grain again, and Teardrop Island's marina still owes a witness line from the dock spill."

    voice "audio/voice/toa_173.mp3"
    toa "Magistrate-sama, I can take the island manifest before dawn. The ferry masters always file late when they are frightened."

    show kaoru smirk
    voice "audio/voice/kaoru_206.mp3"
    kaoru "Good. Wear a cloak. Leave the ledger. If the watch asks, you are inventory I chose not to file yet."

    show toa flustered
    voice "audio/voice/toa_174.mp3"
    toa "That is not how permits work, and you know it."

    show kaoru charm
    voice "audio/voice/kaoru_207.mp3"
    kaoru "Permits are just paper. Boats are honest. With me, To-chan."

    scene black with fade
    pause 0.6

    $ show_cg_scene("case4_5_boat_canal_night", fade)
    play music audio.bgm_case4_5_kobune fadein 2.5 loop volume 0.48

    voice "audio/voice/narrator_175.mp3"
    "Teardrop Island's marina is nothing like the licensed quarter's polished stone. Just frost-bitten ribs and broken pilings. The first winter wind off the bay cuts straight through the rubble. A small kobune rocks at the tide line, its paint scarred from somebody else's war."

    scene black with fade
    pause 0.4

    voice "audio/voice/narrator_176.mp3"
    "She peers out from behind a split mooring post, witness notes tucked into her sleeve. Then a familiar voice cracks across the cold."

    show kaoru cold at center
    voice "audio/voice/kaoru_208.mp3"
    kaoru "Can just ONE thing go right tonight?!"

    "He is soaked to the bone, bay water and not rain. He runs the kobune aground and kicks the hull once, hard, like the wood personally betrayed him."

    hide kaoru
    show toa surprised at center

    voice "audio/voice/narrator_177.mp3"
    "The Emerald Magistrate, soaked and furious, in a boat, in this freezing cold?"

    show toa determined
    voice "audio/voice/toa_175.mp3"
    toa "Magistrate-sama!"

    "She scrambles over the marina wreckage, hair loose, dry kosode whipping in the shore wind."

    $ show_cg_scene("case4_5_boat_duo_tense", fade)

    show kaoru cold at left
    show toa soft at right

    voice "audio/voice/toa_176.mp3"
    toa "Gods, are you alright? What in the world happened to you?"

    "Her grey eyes search his face, and her warm fingertips brush his chilled cheeks before she can think better of it."

    show kaoru cold
    "He holds up one hand. A glare, not a dismissal. He keeps wringing out his robes, plain working attire, nothing court-fine. He does not tell her to leave."

    show toa sad
    "She steps back, arms falling to her sides. The ache in her stomach rises like a levy she cannot hold."

    voice "audio/voice/narrator_178.mp3"
    "A sniffle. Then a whimper. Tears spill down her wind-reddened cheeks, concern he will not let her offer, and she still does not know if he is whole."

    show kaoru cold
    voice "audio/voice/kaoru_209.mp3"
    kaoru "Bad day for you too, then?"

    "He strips out of the soaked layers right there on the cold shore, not for show, only to survive. The scene spares what the bay already stole."

    show toa sad
    voice "audio/voice/toa_177.mp3"
    toa "A bad day? Yes. Yes, it has been a bad day!"

    show toa sad
    voice "audio/voice/toa_178.mp3"
    toa "Calamity and hunger and suffering, and that spooky nonsense in the wards, and now you, you almost sank a boat, and it is so cold, and you could have died..."

    "She crumples, and a wordless wail slips out between hitched breaths."

    show kaoru cold
    voice "audio/voice/kaoru_210.mp3"
    kaoru "I'm fine, To-chan. Just cold."

    show toa soft
    voice "audio/voice/toa_179.mp3"
    toa "...why are you even out here in a boat?"

    show kaoru cold
    voice "audio/voice/kaoru_211.mp3"
    kaoru "There's no other way to reach Teardrop Island. Obviously."

    "He wraps his arms around himself, furious, exposed, well past politeness now."

    show kaoru hungry
    voice "audio/voice/kaoru_212.mp3"
    kaoru "Stand there gawking or come warm me. It has been a bad day, To-chan, and you are the only fire on this pier."

    menu case4_5_boat_warm_menu:
        "Step into him, wide sleeves, the warmth he wants.":
            $ case4_5_boat_choice = "trust_warm"
            jump case4_5_boat_trust_warm

        "Hold back, mouth shut, until he asks you properly.":
            $ case4_5_boat_choice = "defy_cold"
            jump case4_5_boat_defy_cold


label case4_5_boat_trust_warm:

    show toa soft
    voice "audio/voice/toa_180.mp3"
    toa "Yes, Magistrate-sama."

    "She wipes her face once and folds him into a hug. Her wide sleeves drape over him like a blanket, and she is just slightly taller, so the warmth finally crosses the gap between witness and man."

    jump case4_5_boat_drag_to_kobune


label case4_5_boat_defy_cold:

    show toa determined
    voice "audio/voice/toa_181.mp3"
    toa "I am not cargo to haul around on your bad night."

    show kaoru amused
    voice "audio/voice/kaoru_213.mp3"
    kaoru "Crane spine, even on a frozen pier. Brave. Foolish. Mine either way."

    show toa sad
    voice "audio/voice/toa_182.mp3"
    toa "Then ask. Do not order. Not when you need me."

    show kaoru hungry
    voice "audio/voice/kaoru_214.mp3"
    kaoru "I asked with the boat and the bay. And you are still here, aren't you."

    "She exhales, her pride losing to the cold and to his shaking shoulders, and she steps in anyway."

    jump case4_5_boat_drag_to_kobune


label case4_5_boat_drag_to_kobune:

    show kaoru satisfied at left
    show toa flustered at right

    voice "audio/voice/kaoru_215.mp3"
    kaoru "Almost enough. But not quite."

    "He drags her toward the kobune. She does not resist, only hopes, foolishly, for a careful step and a hand on the gunwale."

    show toa thinking
    voice "audio/voice/toa_183.mp3"
    toa "The deck of a boat is not a tatami mat."

    show kaoru smirk
    voice "audio/voice/kaoru_216.mp3"
    kaoru "Worse."

    "He sends her over the side, into the hull, not into the canal. The kobune rocks hard. Water slaps at the strakes."

    $ show_cg_scene("case4_5_boat_throw_splash", fade)

    menu case4_5_boat_fall_menu:
        "Go limp and let the hull take you.":
            $ case4_5_boat_fall_choice = "trust_fall"
            jump case4_5_boat_survive_throw

        "Fight the throw and land rigid on the thwart.":
            $ case4_5_boat_fall_choice = "fight_fall"
            jump case4_5_boat_bad_end_warning


label case4_5_boat_survive_throw:

    $ case4_5_boat_survived = True

    play sound audio.footsteps_corridor volume 0.35
    voice "audio/voice/narrator_179.mp3"
    "Knees, hips, shoulder, all wet wood. Pain and surprise in a single breath. The roll of the boat underneath is wrong, almost dizzying."

    show kaoru cold at left
    show toa flustered at right

    voice "audio/voice/kaoru_217.mp3"
    kaoru "You are on top today. I am too cold to manage you, and you have feelings to work through besides. Get to it. File them on my hull."

    show toa soft
    voice "audio/voice/toa_184.mp3"
    toa "O-oh. Alright then."

    scene black with fade
    pause 0.9

    $ show_cg_scene("case4_5_boat_lash_rain", fade)
    pause 2.0

    voice "audio/voice/narrator_308.mp3"
    "Rain needles the strakes. One closed eye, white lashes wet as paper, silver hair stuck to her temple. Lantern bokeh bleeds gold across the gunwale while she holds still for him."

    $ show_cg_scene("case4_5_boat_hands_gunwale", fade)
    pause 2.0

    voice "audio/voice/narrator_309.mp3"
    "His tanned grip finds her pale wrist on wet wood. Kimono cuffs, shallow depth, the kobune rocking like a clerk trying to lie under pressure."

    $ show_cg_scene("case4_5_boat_lantern_implied", fade)

    voice "audio/voice/narrator_180.mp3"
    "The hull rocks. His palms brace the gunwales whenever the boat threatens to tip. Good girl, breathed against her hair, implied, never filed, a hunger the ledger has no column for."

    pause 0.8

    voice "audio/voice/narrator_181.mp3"
    "When the rhythm finally ends, they are a single knot of warmth and borrowed robes. The bay cold waits just outside the strakes like a witness who was never summoned."

    show kaoru charm at left
    show toa soft at right

    show toa determined
    voice "audio/voice/toa_185.mp3"
    toa "...You didn't, though. You didn't find me."

    "She lifts her head, grey eyes locking onto his."

    voice "audio/voice/toa_186.mp3"
    toa "I found you. Do you remember?"

    show kaoru charm
    voice "audio/voice/kaoru_218.mp3"
    kaoru "Hm? Oh. I suppose that is true. Were you really looking for someone like me, though?"

    show toa flustered
    voice "audio/voice/toa_187.mp3"
    toa "I went looking for a magistrate to handle my paperwork. But I found Kitsu Kaoru, the man."

    "His full name leaves her mouth before she can swallow it back. She looks away, and for once he does not scold her."

    show kaoru satisfied
    voice "audio/voice/kaoru_219.mp3"
    kaoru "I keep wondering what I did to deserve the one witness who lets a man like me bully her toward the warm side of the boat."

    show toa soft
    voice "audio/voice/toa_188.mp3"
    toa "Your color is coming back. Can we please go home now?"

    show kaoru charm
    voice "audio/voice/kaoru_220.mp3"
    kaoru "Fiiiiiiiine."

    show toa happy
    voice "audio/voice/toa_189.mp3"
    toa "A bath, and mikan under the kotatsu. That is the treaty."

    show kaoru smirk
    voice "audio/voice/kaoru_221.mp3"
    kaoru "Toa-san? Next time I will have you again behind my screen, in a proper bath, where the bay cannot watch. The marina was never the place for it."

    jump case4_5_boat_bridge


label case4_5_boat_bad_end_warning:

    centered "{size=-2}This ending is tragic. Grave injury implied, hospital fade, no graphic gore.{/size}"

    menu case4_5_boat_injury_warning_menu:
        "Continue.":
            pass

        "Return to title.":
            stop music fadeout 1.5
            return

    jump case4_5_bad_end_boat


label case4_5_bad_end_boat:

    $ case4_5_bad_end_boat_injury = True
    jump gameover_case4_5_boat


label case4_5_boat_bridge:

    scene bg magistrate_office with dissolve
    play music audio.bgm_street fadein 2.0 loop volume 0.42
    show kaoru commanding at left
    show toa soft at right

    voice "audio/voice/narrator_182.mp3"
    "They ferry back before the watch can invent a drowning. Steam and citrus fill the magistrate wing, the bath, the kotatsu, mikan peeled in a silence that is almost domestic."

    show kaoru charm
    voice "audio/voice/kaoru_222.mp3"
    kaoru "Case Five will not wait just because you bruised your knees on my kobune."

    show toa soft
    voice "audio/voice/toa_190.mp3"
    toa "Yes, Magistrate-sama. The witness line is written."

    show kaoru satisfied
    voice "audio/voice/kaoru_223.mp3"
    kaoru "And To-chan, do your sulking in private if you must. The marina saw quite enough of us tonight."

    jump case5_investigation_start
