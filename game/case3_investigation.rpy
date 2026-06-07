# Case 3, Kimono fabric shop (絹屋の帳 / Ledger of the Bolt Room).
# Entry: case2_post_case2_bridge → case3_investigation_start (canon vertical slice).
# Vertical slice: one investigation beat + accident setpiece + rescue / injury bad end.

label case3_investigation_start:

    if case3_closed:
        return

    $ case3_started = True
    $ case3_briefing_choice = ""
    $ case3_clue_bolt = False
    $ case3_clue_clerk = False
    $ case3_clue_shelf = False
    $ case3_accident_choice = ""

    scene bg magistrate_office with fade
    play music audio.bgm_office fadein 2.0 loop volume 0.55
    show kaoru commanding at left
    show toa determined at right

    voice "audio/voice/narrator_247.mp3"
    "Case Two's ash is barely a day cold, still clinging to the duplicate charter, when the outer bell rings again. Cloth this time, not blood. A bolt merchant's runner, and the seal in his hand smells of Scorpion wax."

    voice "audio/voice/kaoru_283.mp3"
    kaoru "Case Three. That Chrysanthemum factor from Case One did not drown with his barge after all. His cousin sells kimono behind a borrowed Crane name, and the bolt counts never quite agree with the tax lines."

    voice "audio/voice/toa_246.mp3"
    toa "Fabric instead of dead men in canals. That is almost civilized, Magistrate-sama."

    show kaoru cold
    voice "audio/voice/kaoru_284.mp3"
    kaoru "Civilized is how this city hides its knives. You wanted a witness note that outlives the clerks who file it. Earn it in the bolt room, or lose it on my desk."

    if live_in_companion:
        show kaoru charm
        voice "audio/voice/kaoru_285.mp3"
        kaoru "You sleep on the other side of my office wall now. So today you walk the shop at my side. Not ahead of me, not alone."

        show toa flustered
        voice "audio/voice/toa_247.mp3"
        toa "I heard every word at the festival. Surely Case Three can wait until the tea cools."

        show kaoru smirk
        voice "audio/voice/kaoru_286.mp3"
        kaoru "The tea cooled yesterday. The file did not."

    else:
        show kaoru smirk
        voice "audio/voice/kaoru_287.mp3"
        kaoru "Your permit survived Case Two. Case Three decides whether a single soul in the Academy still believes your name means anything."

    $ show_cg_scene("moment case3_briefing_menu")

    menu case3_briefing_menu:
        "Start with the tax ledger. See if the bolt counts match the warehouse receipts.":
            $ case3_briefing_choice = "ledger"
            $ insight += 2
            show toa thinking
            voice "audio/voice/toa_248.mp3"
            toa "If the bolts lie on paper, the shelves lie in the room. I want the numbers before I want any names."

            show kaoru satisfied
            voice "audio/voice/kaoru_288.mp3"
            kaoru "Numbers before names. The Academy did teach you something after all. Bring me a line I can paste straight into the file without crossing out half your adjectives."

        "Talk to the clerk before I touch anything. Find out who signed the last night count.":
            $ case3_briefing_choice = "witness"
            $ composure += 2
            $ honor += 1
            show toa neutral
            voice "audio/voice/toa_249.mp3"
            toa "A clerk lies with his mouth and tells the truth with his hands. I will watch both."

            show kaoru commanding
            voice "audio/voice/kaoru_289.mp3"
            kaoru "Discipline. Good. Ask him who profits when a bolt room happens to collapse on a Crane witness."

        "Follow the Scorpion dye thread. Case One's flower never finished blooming.":
            $ case3_briefing_choice = "scorpion_thread"
            $ insight += 1
            $ honor += 1
            show toa determined
            voice "audio/voice/toa_250.mp3"
            toa "Chrysanthemum patron, a forged writ, now silk. Someone keeps braiding Case One straight into my obi."

            show kaoru cold
            voice "audio/voice/kaoru_290.mp3"
            kaoru "Then do not braid poetry on my desk to match. Tag it, bag it, witness it."

    jump case3_fabric_shop_arrival


label case3_fabric_shop_arrival:

    scene bg fabric_shop with fade
    play music audio.bgm_case3_fabric fadein 2.0 loop volume 0.42
    show toa determined at right
    show kaoru cold at left

    $ show_cg_scene("case3_fabric_shop", fade)

    voice "audio/voice/narrator_248.mp3"
    "The shop smells of camphor and indigo. Bolts lean against the walls like courtiers dozing through a dull recital, and the paper tags flutter every time the street door breathes. A clerk in Crane colors bows a touch too low, smiles a touch too fast."

    voice "audio/voice/kaoru_291.mp3"
    kaoru "Magistrate's custody. Open the bolt room. No one lays a finger on the top shelf until my witness has signed the count."

    voice "audio/voice/toa_251.mp3"
    toa "The third bell has not even rung, and this clerk is already sweating through his Crane collar. He is afraid of the room, Magistrate-sama, not of us."

    show kaoru thinking
    voice "audio/voice/kaoru_292.mp3"
    kaoru "Because someone wanted the inventory to come down the moment the right person stood beneath it. Ask your questions. I will be at the street door. Close enough to hear you scream, far enough that the clerks still think you are alone."

    show toa worried
    voice "audio/voice/toa_252.mp3"
    toa "You are leaving me alone in the aisle."

    show kaoru charm
    voice "audio/voice/kaoru_293.mp3"
    kaoru "I am handing you a clerk who will talk to a dancer and lie to a magistrate. Use that."

    hide kaoru with dissolve

    $ show_cg_scene("moment case3_investigation_menu")

    menu case3_investigation_menu:
        "Match the dye tags on the bolt ends against the ledger, find the mislabeled Scorpion lot.":
            $ case3_clue_bolt = True
            $ insight += 2
            voice "audio/voice/narrator_249.mp3"
            "Crimson, tagged Crane on the outside. But the inner thread carries the six-legged mark of a Scorpion factor's private vat. Someone switched the labels before the tax count ever happened."

            show toa surprised
            voice "audio/voice/toa_253.mp3"
            toa "This bolt belongs in Case One's file, not on some merchant's shelf."

        "Lean on the clerk about the second ledger hidden under the counter.":
            $ case3_clue_clerk = True
            $ composure += 1
            $ insight += 1
            voice "audio/voice/narrator_250.mp3"
            "His hands start shaking the moment she asks for the wax. A thin book surfaces from somewhere, night counts that will never match the day book Kaoru is about to seize at the door."

            show toa determined
            voice "audio/voice/toa_254.mp3"
            toa "You signed two different truths. Decide now which one drowns when the magistrate reads them both."

        "Look closer at the shelf brace. That is scoring, not age.":
            $ case3_clue_shelf = True
            $ honor += 1
            $ insight += 1
            voice "audio/voice/narrator_251.mp3"
            "Beneath the old lacquer the brace shows a clean saw kerf. Deliberate. Recent. And the top shelf already leans a finger's width out toward the aisle."

            show toa angry
            voice "audio/voice/toa_255.mp3"
            toa "This isn't a storeroom. It's a deadfall someone stacked with silk."

    voice "audio/voice/narrator_252.mp3"
    "The clerk excuses himself to fetch 'fresh seals.' The street door latches behind him. Somewhere overhead, rope begins to groan, too much weight resting on too fresh a cut."

    play sound audio.chair_creak volume 0.7
    voice "audio/voice/narrator_253.mp3"
    "A lantern sways. The top bolt shifts, pale silk spilling loose like a white serpent uncoiling, and the shelf timber starts to scream."

    jump case3_accident_climax


label case3_accident_climax:

    $ show_cg_scene("case3_accident_moment", fade)
    play music audio.bgm_case3_fabric fadein 0.8 loop volume 0.65

    voice "audio/voice/narrator_254.mp3"
    "The shelf gives. Silk slams the air, dust turns to falling snow. Toa has exactly one breath and two bad choices: scream for the man at the door, or prove Crane training can still save her on its own."

    $ show_cg_scene("moment case3_accident_menu")

    menu case3_accident_menu:
        "Trust Kaoru. Scream for him.":
            $ case3_accident_choice = "trust_kaoru"
            jump case3_kaoru_rescue

        "Dodge it alone. Refuse his help.":
            $ case3_accident_choice = "dodge_alone"
            jump case3_bad_end_injury_warning


label case3_kaoru_rescue:

    $ case3_accident_avoided = True
    $ case3_kaoru_rescue = True

    play sound audio.footsteps_corridor volume 0.75
    voice "audio/voice/narrator_255.mp3"
    "He is already moving. Not at the street door at all, but inside the line of the fall, magistrate's coat thrown back, one arm hooking hard under her obi."

    $ show_cg_scene("case3_kaoru_rescue", fade)
    play music audio.bgm_canon_intimate fadein 2.0 loop volume 0.45

    voice "audio/voice/narrator_256.mp3"
    "They hit the mat together, sideways, silk dragging across her cheek, his breath hot against her temple, his heartbeat suddenly louder than any of the clerk's lies."

    show kaoru cold at left
    show toa flustered at right

    voice "audio/voice/kaoru_294.mp3"
    kaoru "Up. Now. Before that clerk invents a story where you died clumsy."

    voice "audio/voice/toa_256.mp3"
    toa "You... your hands are shaking."

    show kaoru cold
    voice "audio/voice/kaoru_295.mp3"
    kaoru "A draft, from the alley. Nerves. Stand."

    voice "audio/voice/narrator_257.mp3"
    "For one whole heartbeat his grip does not loosen. Grey eyes locked on hers, too honest, every ounce of performance stripped away."

    voice "audio/voice/kaoru_296.mp3"
    kaoru "If that shelf had taken you, there would be no bolt room left. No quarter. Nothing but the canal and my apology to it."

    show toa soft
    voice "audio/voice/toa_257.mp3"
    toa "Magistrate-sama..."

    show kaoru cold
    voice "audio/voice/kaoru_297.mp3"
    kaoru "Forget I said that. Witness note: shelf sabotage, clerk detained. You are breathing. That is the only romance this file requires."

    show toa flustered
    voice "audio/voice/toa_258.mp3"
    toa "I am not, that is not what, I-I will write the shelf line first."

    show kaoru smirk
    voice "audio/voice/kaoru_298.mp3"
    kaoru "Good. Devotion stays on paper until I say otherwise."

    jump case3_milestone_end


label case3_bad_end_injury_warning:

    scene bg fabric_shop with dissolve
    show toa determined at center

    voice "audio/voice/narrator_227.mp3"
    "She twists, Crane footwork in a space built for counting merchants, not dancers. Pride swears the roll will clear. Physics disagrees."

    centered "{size=-2}This ending is tragic. Grave injury implied, hospital fade, no graphic gore.{/size}"

    menu case3_injury_warning_menu:
        "Continue.":
            pass

        "Return to title.":
            stop music fadeout 1.5
            return

    jump case3_bad_end_injury


label case3_bad_end_injury:

    $ case3_bad_end_injury = True
    jump gameover_case3_injury


label case3_milestone_end:

    scene bg magistrate_office with dissolve
    play music audio.bgm_office fadein 2.0 loop volume 0.5
    show kaoru commanding at left
    show toa determined at right

    play sound audio.paper_shuffle volume 0.4
    voice "audio/voice/narrator_258.mp3"
    "By afternoon the clerk has given up the Chrysanthemum cousin's runner, the runner has given up a payment for the shelf, and Kaoru inks a custody chit thick enough to survive one jealous factor's lawyers."

    voice "audio/voice/kaoru_299.mp3"
    kaoru "Case Three is not closed. It is pinned. Like the bolt that almost killed my witness."

    if case3_clue_bolt:
        show kaoru satisfied
        voice "audio/voice/kaoru_300.mp3"
        kaoru "The mistagged lot ties straight back to Case One's flower. Good. Paste that line into the file before some Scorpion lawyer buys the clerk's silence."

    if case3_clue_clerk:
        show toa determined
        voice "audio/voice/toa_437.mp3"
        toa "The clerk's second ledger is the thread. Night counts in one hand, day counts in the other, both his. He will trade the Chrysanthemum's name before he lets his own hang for the bolt room."

    if case3_clue_shelf:
        show toa thinking
        voice "audio/voice/toa_259.mp3"
        toa "Someone paid good money for that saw kerf. I want the name that signed for the brace, not the boy who only held the saw."

    show toa flustered
    voice "audio/voice/toa_260.mp3"
    toa "I still hear the shelf coming down every time I close my eyes. Thank you for, for being at the door."

    show kaoru cold
    voice "audio/voice/kaoru_301.mp3"
    kaoru "I was at the mat, not the door. Do not make poetry of it. Case Four will knock soon enough, the moment the rain comes back."

    $ case3_closed = True

    voice "audio/voice/narrator_259.mp3"
    "Case Three's first line is written into the file. The city still lies, but she is still breathing in Ryoko Owari."

    "The mistagged bolts tie the cousin's silk ledger to the same false cargo math Jiro died for. Pinned beside Case One's seal and Case Two's charter, not closed, like every file this season."

    jump case3_post_case3_bridge
