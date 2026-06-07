# Prologue: full first-scene RP arc (Toa & Kaoru, PG-13/M).
# Beats: corridor → wrong door → permit crisis → audition → unless? → canon or branches.
# Canon (physical "unless?"): amorous encounter (fade) → hanko seal → date +3 days → Case 1.
# Continues into Case 1 via prologue_case1_hook → case1_companion.rpy (canon) or case1_noncanon_start.

label prologue_start:

    # Beat 1, Lost in corridor (generic bg + sprites; CG on key beats only)
    scene bg corridor with fade
    play music audio.bgm_corridor fadein 2.5 loop volume 0.65
    play sound audio.footsteps_corridor volume 0.55

    voice "audio/voice/narrator_001.mp3"
    "Lantern light pools on polished floorboards. Every sliding door looks the same."

    voice "audio/voice/narrator_002.mp3"
    "Toa clutches her permit book and hanko case, turning in a corridor that refuses to end."

    show toa worried at right with dissolve

    voice "audio/voice/toa_001.mp3"
    toa "I was sure the clerk said third hall, fourth door on the left. Or was it the right?"

    voice "audio/voice/narrator_003.mp3"
    "The noble quarter smells of ink and cedar. Somewhere behind these walls, someone holds the seal she needs."

    show toa determined
    voice "audio/voice/toa_002.mp3"
    toa "One more corridor. Then I ask nicely. Very nicely."

    # Beat 2, Wrong door / Kaoru complaint
    hide toa
    show kaoru cruel at left with vpunch
    play music audio.bgm_kaoru_theme fadein 1.5 loop volume 0.6

    voice "audio/voice/kaoru_001.mp3"
    kaoru "Done complaining?"

    show toa surprised at right with dissolve

    voice "audio/voice/toa_003.mp3"
    toa "I wasn't... That is, I apologize for the disturbance, honored sir!"

    show kaoru smirk
    voice "audio/voice/kaoru_002.mp3"
    kaoru "Wrong door. Again."

    play sound audio.door_slam
    voice "audio/voice/narrator_004.mp3"
    "The door shuts with finality. Toa's ears ring."

    jump prologue_door_menu

label prologue_door_menu:

    $ show_cg_scene("prologue_wrong_door", fade)
    pause 1.2

    menu prologue_door_choices:
        "Leave and find another office.":
            $ door_response = "leave"
            $ honor += 1
            jump prologue_door_leave

        "Knock again, properly this time.":
            $ door_response = "knock_again"
            $ composure += 1
            show toa determined
            voice "audio/voice/toa_004.mp3"
            toa "Third time's the charm. Or the magistrate. Hopefully both."
            jump prologue_formal_knock

        "Wait quietly until invited.":
            $ door_response = "wait_quietly"
            $ kaoru_submission += 1
            $ compliance += 1
            show toa neutral
            voice "audio/voice/narrator_005.mp3"
            "Toa straightens her kosode, breathes, and waits."
            pause 1.0
            $ set_expression("kaoru", "smirk")
            voice "audio/voice/kaoru_003.mp3"
            kaoru "Still there? Knock if you want something."
            jump prologue_formal_knock

label prologue_door_leave:

    if not door_left_once:
        $ door_left_once = True
        show toa determined
        voice "audio/voice/toa_005.mp3"
        toa "Fine. I'll find a magistrate with better manners."

        $ show_cg_scene("corridor_lost")

        voice "audio/voice/narrator_006.mp3"
        "Three offices later, a junior clerk squints at her permit book and points back the way she came."

        voice "audio/voice/toa_006.mp3"
        toa "The Emerald Magistrate? That door?"

        "Clerk" "That's the one who stamps interclan renewals. Good luck. Petitioners walk in proud and leave as paperwork."

        $ set_expression("toa", "happy")
        voice "audio/voice/toa_007.mp3"
        toa "I've come too far to be scared off by a reputation."

        $ set_expression("toa", "determined")
        voice "audio/voice/narrator_007.mp3"
        "The corridor loops, of course it loops, and deposits her exactly where she started."

        jump prologue_door_second_chance

    else:
        show toa worried
        voice "audio/voice/toa_008.mp3"
        toa "Every sign points back to this door. Of course it does."
        jump prologue_door_second_chance

label prologue_door_second_chance:

    $ show_cg_scene("moment prologue_door_second_chance")

    menu:
        "Knock again, properly this time.":
            $ door_response = "knock_again"
            $ composure += 1
            show toa determined
            voice "audio/voice/toa_009.mp3"
            toa "Round two. Posture up. Smile optional."
            jump prologue_formal_knock

        "Wait quietly until invited.":
            $ door_response = "wait_quietly"
            $ kaoru_submission += 1
            $ compliance += 1
            show toa neutral
            voice "audio/voice/narrator_008.mp3"
            "Toa folds her hands. No muttering. No pacing. Just breath and patience."
            pause 1.0
            $ set_expression("kaoru", "smirk")
            voice "audio/voice/kaoru_004.mp3"
            kaoru "Smarter the second time. Knock."
            jump prologue_formal_knock

label prologue_formal_knock:

    # Beat 3, Formal knock, permit renewal inquiry
    scene bg magistrate_office with dissolve
    play music audio.bgm_office fadein 2.0 loop volume 0.62
    play sound audio.sliding_door_open volume 0.75
    show kaoru smirk at left
    show toa neutral at right

    if door_response == "wait_quietly":
        play sound audio.knock_single
        voice "audio/voice/narrator_009.mp3"
        "Toa kneels at the threshold and strikes the frame once, crisp, patient."
        show kaoru amused
        voice "audio/voice/kaoru_005.mp3"
        kaoru "Enter. You can knock when you want something. Try standing still next."
    else:
        play sound audio.knock_formal
        voice "audio/voice/narrator_010.mp3"
        "Toa kneels at the threshold and strikes the frame twice, crisp, measured."

    $ show_cg_scene("moment prologue_formality_menu")

    menu prologue_formality_menu:
        "Hyper-formal address.":
            $ formality_tone = "hyper_formal"
            $ kaoru_submission += 1
            show toa worried
            voice "audio/voice/toa_010.mp3"
            toa "Honored magistrate, this unworthy petitioner begs a moment regarding her performer's permit renewal."

            show kaoru bored
            voice "audio/voice/kaoru_006.mp3"
            kaoru "Tedious. Correct, but tedious."

            show kaoru smirk
            voice "audio/voice/kaoru_007.mp3"
            kaoru "At least your bow didn't wobble. Continue, briefly."

        "Direct and plain.":
            $ formality_tone = "direct"
            $ honor += 1
            $ kaoru_resistance += 1
            show toa determined
            voice "audio/voice/toa_011.mp3"
            toa "Magistrate, I need my permit renewed. I have the paperwork."

            show kaoru amused
            voice "audio/voice/kaoru_008.mp3"
            kaoru "Plain speech. You waste less of my evening than most."

            show kaoru commanding
            voice "audio/voice/kaoru_009.mp3"
            kaoru "Names and purpose. Quickly."

        "Light humor, carefully.":
            $ formality_tone = "humorous"
            $ insight += 1
            show toa happy
            voice "audio/voice/toa_012.mp3"
            toa "It is only your corridors I lost my way in, Magistrate, not the law. May I present my renewal?"

            show kaoru smirk
            voice "audio/voice/kaoru_010.mp3"
            kaoru "Humor in my office. Brave or stupid."

            show toa flustered
            voice "audio/voice/toa_013.mp3"
            toa "Crane training says brave. Unicorn roads say stupid is survivable."

            show kaoru amused
            voice "audio/voice/kaoru_011.mp3"
            kaoru "We'll discover which tonight."

    show kaoru cold
    voice "audio/voice/kaoru_012.mp3"
    kaoru "Emerald Magistrate Kitsu Kaoru. You will use my title if you wish to leave with a seal."

    show toa flustered
    voice "audio/voice/toa_014.mp3"
    toa "Forgive me, Emerald Magistrate."

    # Beat 4, Newcomer pitch
    show kaoru commanding
    voice "audio/voice/kaoru_013.mp3"
    kaoru "State your business. Briefly."

    show toa happy
    voice "audio/voice/toa_015.mp3"
    toa "Kakita Toa, dancer of the Kakita family. New to Ryoko Owari."

    show toa determined
    voice "audio/voice/toa_016.mp3"
    toa "Post-gempukku, traveling from Unicorn lands. I mean to establish residence and perform legally."

    show kaoru amused
    voice "audio/voice/kaoru_014.mp3"
    kaoru "Crane hair, Unicorn permit dates. Wrong clan for this desk; wrong week to fix it."

    show toa thinking
    voice "audio/voice/toa_017.mp3"
    toa "The roads taught me flexibility. The Crane taught me posture."

    if formality_tone == "hyper_formal":
        show kaoru smirk
        voice "audio/voice/kaoru_015.mp3"
        kaoru "Posture on the cushion. We'll see if your feet match your bow."
    elif formality_tone == "direct":
        show kaoru cruel
        voice "audio/voice/kaoru_016.mp3"
        kaoru "Flexibility. The roads teach what the Academy cannot. Sit, and show me the rest is more than posture."
    else:
        show kaoru smirk
        voice "audio/voice/kaoru_017.mp3"
        kaoru "Survivable. We'll test that claim before dawn."

    # Beat 5, Interclan gate
    show kaoru cold
    voice "audio/voice/kaoru_018.mp3"
    kaoru "Interclan residence requires Emerald approval. You knew that."

    show toa worried
    voice "audio/voice/toa_018.mp3"
    toa "I was told a private meeting with the local magistrate would suffice."

    show kaoru commanding
    voice "audio/voice/kaoru_019.mp3"
    kaoru "It does. Door."

    play sound audio.sliding_door_close volume 0.8
    voice "audio/voice/narrator_011.mp3"
    "He gestures. The door closes behind her."

    $ show_cg_scene("moment prologue_enter_office_menu")

    menu prologue_enter_office_menu:
        "Comply, eyes forward, no wandering.":
            $ discipline_check = 0
            $ composure += 1
            show toa neutral
            voice "audio/voice/narrator_012.mp3"
            "Toa keeps her gaze on the desk. Not on the shelves lined with case files and curios."

            show kaoru satisfied
            voice "audio/voice/kaoru_020.mp3"
            kaoru "Better. Most Crane can't resist cataloging a room like a museum."

        "Peek at the shelves anyway.":
            $ discipline_check = 1
            $ insight += 1
            show toa thinking
            voice "audio/voice/narrator_013.mp3"
            "Her eyes snag on a row of scrolls, Lion mon here, Emerald seal there, and one writ still bright with fresh wax at this late hour."

            show toa determined
            voice "audio/voice/toa_435.mp3"
            toa "You seal your own renewals after the clerks go home, Magistrate. A man who trusted his office would be asleep by now."

            show kaoru cruel
            voice "audio/voice/kaoru_021.mp3"
            kaoru "I said sit. Not catalog my trophies."

            show kaoru thinking
            voice "audio/voice/kaoru_566.mp3"
            kaoru "...You are not wrong about the clerks. Note it, and say nothing. A read you cannot hold quietly will cost you more than a wobbled bow."

            show toa flustered
            voice "audio/voice/toa_019.mp3"
            toa "Yes, Magistrate."

            show kaoru smirk
            voice "audio/voice/kaoru_022.mp3"
            kaoru "Since you admire my shelves so freely, you may admire the seal from a distance. If you ever earn it."

    show kaoru bored
    voice "audio/voice/kaoru_023.mp3"
    kaoru "Cushion. Floor. You stand too much for someone begging favors."

    voice "audio/voice/narrator_014.mp3"
    "A cushion already waits on the tatami at his knee. He taps it once with one finger. A tall cup of water on the desk waits like a witness."

    $ show_cg_scene("permit_desk")

    play sound audio.paper_shuffle volume 0.65
    voice "audio/voice/narrator_015.mp3"
    "Toa sets her permit book and hanko case on the desk, close enough to show, not close enough to surrender."

    # Beat 6, Expired permit crisis (CG active, bust-only expressions)
    $ set_expression("kaoru", "thinking")
    voice "audio/voice/kaoru_024.mp3"
    kaoru "These dates."

    $ set_expression("toa", "surprised")
    voice "audio/voice/toa_020.mp3"
    toa "They should be current. I checked before leaving..."

    $ set_expression("kaoru", "cold")
    voice "audio/voice/kaoru_025.mp3"
    kaoru "They are not. Your permit expired. Unicorn bureaucracy failed to mention it?"

    $ set_expression("toa", "worried")
    voice "audio/voice/toa_021.mp3"
    toa "If I cannot renew locally, they'll send me back to the Academy. I can't... not yet."

    menu prologue_expired_menu:
        "Accept the Academy trip.":
            $ permit_strategy = "academy_trip"
            $ compliance += 1
            $ kaoru_submission += 1
            $ set_expression("toa", "sad")
            voice "audio/voice/toa_022.mp3"
            toa "If that is the law, I'll... prepare for the journey back."

            $ set_expression("kaoru", "smirk")
            voice "audio/voice/kaoru_026.mp3"
            kaoru "How obedient. The Unicorn taught you to yield before the fight begins."

            $ set_expression("toa", "determined")
            voice "audio/voice/toa_023.mp3"
            toa "The Crane taught me to know when a battle isn't worth the obi."

            $ set_expression("kaoru", "amused")
            voice "audio/voice/kaoru_027.mp3"
            kaoru "Unfortunately for your travel plans, I'm not finished with you."

        "Push for a local fix.":
            $ permit_strategy = "local_fix"
            $ honor += 1
            $ kaoru_resistance += 1
            $ set_expression("toa", "determined")
            voice "audio/voice/toa_024.mp3"
            toa "There must be a remedy short of exile. Emerald Magistrate, what do you require?"

            $ set_expression("kaoru", "amused")
            voice "audio/voice/kaoru_028.mp3"
            kaoru "Requirements. Finally, a useful word."

            $ set_expression("kaoru", "commanding")
            voice "audio/voice/kaoru_029.mp3"
            kaoru "Most petitioners wail. You ask for terms. That almost earns respect."

            $ set_expression("toa", "happy")
            voice "audio/voice/toa_025.mp3"
            toa "Almost is a start. I dance for a living, I know how to build toward a finale."

        "Plead, she has nowhere else.":
            $ permit_strategy = "plead"
            $ composure += 1
            $ set_expression("toa", "worried")
            voice "audio/voice/toa_026.mp3"
            toa "I have no patrons here. No standing. If you turn me out, I sleep in the canal district."

            $ set_expression("kaoru", "cruel")
            voice "audio/voice/kaoru_030.mp3"
            kaoru "Tragic. Continue."

            $ set_expression("toa", "sad")
            voice "audio/voice/toa_027.mp3"
            toa "My pony needs shoes. The innkeeper tolerates me because I fold linens without complaint."

            $ set_expression("kaoru", "smirk")
            voice "audio/voice/kaoru_031.mp3"
            kaoru "A curry shop and borrowed bedding. Ryoko Owari's finest import."

            $ set_expression("toa", "determined")
            voice "audio/voice/toa_028.mp3"
            toa "I'm still here. That counts for something."

            $ set_expression("kaoru", "hungry")
            voice "audio/voice/kaoru_032.mp3"
            kaoru "We'll see what it's worth."

    jump prologue_social_vacuum

label prologue_social_vacuum:

    # Beat 7, Social vacuum (return to bg + sprites after permit-desk CG)
    scene bg magistrate_office with dissolve
    show kaoru smirk at left
    show toa neutral at right

    show kaoru bored
    voice "audio/voice/kaoru_033.mp3"
    kaoru "No local patrons. No endorsements."

    show toa thinking
    voice "audio/voice/toa_029.mp3"
    toa "Only the inn, a pony that needs shoes, and a curry shop where the owner tolerates me."

    show kaoru amused
    voice "audio/voice/kaoru_034.mp3"
    kaoru "High society."

    show toa determined
    voice "audio/voice/toa_030.mp3"
    toa "The month is almost out. By tomorrow I need proof I belong here."

    if permit_strategy == "local_fix":
        show kaoru cold
        voice "audio/voice/kaoru_035.mp3"
        kaoru "Proof requires more than appetite. Tut."
    elif permit_strategy == "academy_trip":
        show kaoru smirk
        voice "audio/voice/kaoru_036.mp3"
        kaoru "Tomorrow is generous. Tut."
    else:
        show kaoru cold
        voice "audio/voice/kaoru_037.mp3"
        kaoru "Tomorrow. Tut."

    voice "audio/voice/narrator_016.mp3"
    "He tutted once. Toa has heard he can manage five."

    # Beat 8, Dance disclosed; lecture
    show toa flustered
    voice "audio/voice/toa_031.mp3"
    toa "I... may have listed dance as my primary art. On the renewal form."

    show kaoru commanding
    voice "audio/voice/kaoru_038.mp3"
    kaoru "May have."

    show kaoru cruel
    voice "audio/voice/kaoru_039.mp3"
    kaoru "Dance listed. Venue missing. Patron column blank. Even a junior clerk can read what that adds to."

    show toa worried
    voice "audio/voice/toa_032.mp3"
    toa "I have training. I have..."

    if discipline_check == 1:
        show kaoru smirk
        voice "audio/voice/kaoru_040.mp3"
        kaoru "You have curiosity. Not yet an audience."

    show kaoru smirk
    voice "audio/voice/kaoru_041.mp3"
    kaoru "Stand."

    voice "audio/voice/narrator_017.mp3"
    "The cushion at her feet does not move. The water cup on the desk does not move. It never does."

    # Beat 9, Audition bargain
    show kaoru hungry
    voice "audio/voice/kaoru_042.mp3"
    kaoru "Proposed remedy?"

    show toa thinking
    voice "audio/voice/toa_033.mp3"
    toa "You want a performance."

    show kaoru satisfied
    voice "audio/voice/kaoru_043.mp3"
    kaoru "Impress me."

    $ show_cg_scene("moment prologue_before_dance_menu")

    menu prologue_before_dance_menu:
        "Negotiate terms first.":
            $ negotiated_terms = True
            $ insight += 1
            show toa determined
            voice "audio/voice/toa_034.mp3"
            toa "If I perform, you sign. No delays, no new conditions after."

            show kaoru charm
            voice "audio/voice/kaoru_044.mp3"
            kaoru "Bold. We'll see if your art matches your contract law."

            show kaoru cold
            voice "audio/voice/kaoru_045.mp3"
            kaoru "I sign when I'm satisfied, not when you're tired. That is the only term."

            show toa angry
            voice "audio/voice/toa_035.mp3"
            toa "Then I'll dance until you're satisfied, or until dawn, whichever gives out first."

            show kaoru satisfied
            voice "audio/voice/kaoru_046.mp3"
            kaoru "Acceptable. Begin."

            jump prologue_office_dance

        "Perform immediately.":
            $ performance_boldness += 1
            $ compliance += 1
            show toa happy
            voice "audio/voice/toa_036.mp3"
            toa "Music optional. Audience of one. Watch closely, Magistrate."

            show kaoru hungry
            voice "audio/voice/kaoru_047.mp3"
            kaoru "No preamble. Good."

            jump prologue_office_dance

        "Refuse, this isn't justice.":
            $ rebuke += 1
            $ kaoru_resistance += 2
            show toa angry
            voice "audio/voice/toa_037.mp3"
            toa "I'm a petitioner, not your evening entertainment."

            show kaoru furious
            voice "audio/voice/kaoru_048.mp3"
            kaoru "Then you may walk back to your curry shop and explain an expired permit to the gate guards."

            jump prologue_refuse_bad_end

label prologue_refuse_bad_end:

    scene bg magistrate_office with dissolve
    show kaoru cold at left
    show toa angry at right

    show toa determined
    voice "audio/voice/toa_038.mp3"
    toa "Justice isn't a private show for magistrates with bored eyes."

    show kaoru cold
    voice "audio/voice/kaoru_049.mp3"
    kaoru "Justice is what I write on the page you didn't earn."

    show toa sad
    play sound audio.hanko_case_click
    voice "audio/voice/narrator_018.mp3"
    "She gathers her permit book. The hanko case clicks shut like a verdict."

    show kaoru smirk
    voice "audio/voice/kaoru_050.mp3"
    kaoru "The gate closes at midnight. The canal district is that way."

    show toa angry
    voice "audio/voice/toa_039.mp3"
    toa "I'll find another seal. Or another city."

    show kaoru amused
    voice "audio/voice/kaoru_051.mp3"
    kaoru "You won't. You'll knock again when hunger wins."

    scene black with fade

    centered "{size=-2}Without a seal, Ryoko Owari has no place for Kakita Toa.{/size}"

    $ show_cg_scene("moment prologue_refuse_retry_menu", fade)

    menu:
        "Try again, swallow your pride.":
            scene bg magistrate_office with dissolve
            show kaoru smirk at left
            show toa flustered at right
            show toa determined
            voice "audio/voice/toa_040.mp3"
            toa "Fine. One dance. One seal. Then I never perform for you again."
            show kaoru hungry
            voice "audio/voice/kaoru_052.mp3"
            kaoru "We'll see about never."
            jump prologue_office_dance

        "Leave the magistrate's office.":
            $ show_cg_scene("corridor_lost", fade)
            voice "audio/voice/toa_041.mp3"
            toa "Snacks first was the plan. Pride second. I got the order wrong."
            voice "audio/voice/narrator_019.mp3"
            "Rain finds the noble quarter anyway. Case One will have to wait for a braver night."
            jump gameover_rain

label prologue_office_dance:

    # Beat 10, Office dance (PG-13); CG carries the scene, no full-body sprites
    $ show_cg_scene("office_dance")
    play music audio.bgm_toa_theme fadein 2.5 loop volume 0.68

    voice "audio/voice/narrator_020.mp3"
    "Lamplight shrinks the room. Toa loosens her obi, not indecent, but deliberate, and lets the silk breathe."

    menu prologue_performance_menu:
        "Formal fan dance, maiden narrative, bells on obijime.":
            $ performance_style = "formal_dance"
            play sound audio.fan_open
            voice "audio/voice/narrator_021.mp3"
            "She unfolds her fan. Steps trace a story, courtship, hesitation, resolve, obijime bells whispering at each turn."

            voice "audio/voice/toa_042.mp3"
            toa "The maiden waits at the gate. The road is long. She walks anyway."

            voice "audio/voice/narrator_022.mp3"
            "Kaoru watches, still as stone. He drinks water without looking away."

            voice "audio/voice/kaoru_053.mp3"
            kaoru "Better. Keep going. I haven't touched the hanko yet."

            voice "audio/voice/narrator_023.mp3"
            "The fan closes on the final beat, not a bow, but a held breath."

        "Flirtatious read, small audience, coquette sway.":
            $ performance_style = "flirtatious"
            $ performance_boldness += 2
            $ kaoru_resistance += 1
            voice "audio/voice/narrator_024.mp3"
            "She plays to one viewer. Hips sway where the kata allows; smile promises more than the room receives."

            voice "audio/voice/toa_043.mp3"
            toa "One person in the room. Might as well make him regret looking away."

            voice "audio/voice/kaoru_054.mp3"
            kaoru "Cheeky."

            play sound audio.obijime_bells volume 0.7
            voice "audio/voice/narrator_025.mp3"
            "She lets the obijime bells laugh once, invitation and challenge in the same sound."

            voice "audio/voice/narrator_026.mp3"
            "The cup sets down softly. His eyes don't blink."

    jump prologue_withheld_signature

label prologue_withheld_signature:

    # Beat 11, Withheld signature
    scene bg magistrate_office with dissolve
    show kaoru smirk at left
    show toa flustered at right

    show toa determined
    voice "audio/voice/toa_044.mp3"
    toa "That earns your seal. You said impress you, I did."

    if negotiated_terms:
        show toa angry
        voice "audio/voice/toa_045.mp3"
        toa "We had terms. No delays."

        show kaoru amused
        voice "audio/voice/kaoru_055.mp3"
        kaoru "Terms are for courts. This is my desk."

    show kaoru satisfied
    voice "audio/voice/kaoru_056.mp3"
    kaoru "Merit enough. Signature... pending."

    show toa angry
    voice "audio/voice/toa_046.mp3"
    toa "Pending?"

    show kaoru cruel
    voice "audio/voice/kaoru_057.mp3"
    kaoru "Continue."

    $ compliance += 1
    show toa soft

    if performance_style == "formal_dance":
        voice "audio/voice/narrator_027.mp3"
        "She continues, the maiden's story unfinished, bells softer now, every turn aimed at the desk."
    elif performance_style == "flirtatious":
        voice "audio/voice/narrator_028.mp3"
        "She continues, coquette sway sharpened to obedience, every glance a question he refuses to answer."
    else:
        voice "audio/voice/narrator_029.mp3"
        "She continues, bells softer, gaze sharper, every turn aimed at the desk and the seal he still withholds."

    show kaoru smirk
    voice "audio/voice/kaoru_058.mp3"
    kaoru "A good performance."

    if performance_style == "flirtatious":
        show kaoru hungry
        voice "audio/voice/kaoru_059.mp3"
        kaoru "Better when you stop pretending the room is empty."

    jump prologue_grab_moment

label prologue_grab_moment:

    # Beat 12, Escalation at grab (fade before explicit); return to bg + sprites
    scene bg magistrate_office with dissolve
    play music audio.bgm_kaoru_theme fadein 1.5 loop volume 0.7
    show kaoru hungry at left
    show toa flustered at right

    voice "audio/voice/narrator_030.mp3"
    "His hand finds her wrist, not painful, not gentle, the grip of a man weighing goods he already assumes are his."

    $ show_cg_scene("moment prologue_grab_menu")

    menu prologue_grab_menu:
        "Rebuke him, pull back.":
            $ rebuke += 2
            $ kaoru_resistance += 1
            show toa angry
            voice "audio/voice/toa_047.mp3"
            toa "Magistrate-sama. That is not in any permit renewal I read."

            show kaoru amused
            voice "audio/voice/kaoru_060.mp3"
            kaoru "No? And yet you're still here."

            show toa determined
            voice "audio/voice/toa_048.mp3"
            toa "I'm here for a seal, not a leash."

            voice "audio/voice/narrator_031.mp3"
            "She spins free and finishes the phrase, defiance as choreography."

            show kaoru smirk
            voice "audio/voice/kaoru_061.mp3"
            kaoru "Defiance suits you. Cheap seals don't."

        "Lean into the moment, don't break the spell.":
            $ compliance += 2
            $ physical_initiative += 1
            show toa flustered
            voice "audio/voice/narrator_032.mp3"
            "She doesn't pull away. The dance uses his grip as counterweight, dangerous, deliberate."

            show toa soft
            voice "audio/voice/toa_049.mp3"
            toa "If you're going to hold me, hold me like you mean the audition."

            show kaoru charm
            voice "audio/voice/kaoru_062.mp3"
            kaoru "Better."

            show kaoru hungry
            voice "audio/voice/kaoru_063.mp3"
            kaoru "Don't stop on my account."

    scene bg magistrate_office with dissolve
    show kaoru satisfied at left
    show toa flustered at right

    voice "audio/voice/kaoru_064.mp3"
    kaoru "Unless?"

    # Beat 13, Cliffhanger; CG carries the unless? menu
    $ show_cg_scene("chair_tension", fade)
    play sound audio.chair_creak volume 0.85

    voice "audio/voice/narrator_033.mp3"
    "The chair creaks. Hakama folds. Two figures, one of them seated like he owns the floor she is standing on, and a single question left hanging between them."

    menu prologue_unless_menu:
        "Answer verbally, name what you want in return.":
            $ unless_branch = "verbal"
            $ insight += 1
            $ honor += 1
            voice "audio/voice/toa_050.mp3"
            toa "Unless you sign before dawn. Unless Ryoko Owari becomes mine to dance in, legally."

            voice "audio/voice/kaoru_065.mp3"
            kaoru "Legally. You learn."

            jump prologue_verbal_ending

        "Answer physically, close the distance.":
            $ unless_branch = "physical"
            $ physical_initiative += 2
            $ compliance += 1
            $ kaoru_submission += 1
            if kaoru_resistance >= 3 or rebuke >= 2:
                voice "audio/voice/narrator_441.mp3"
                "She has argued with him all evening. So she crosses the distance herself, on her terms and not his, and lets the choosing be the answer."
            else:
                voice "audio/voice/narrator_034.mp3"
                "She straddles the chair's arm, not surrender, not retreat. Proximity as punctuation."

            voice "audio/voice/kaoru_066.mp3"
            kaoru "Unless you mean to finish what you started."

            $ show_cg_scene("canon_proposition")
            # Canon contract: prologue_canon_ending (prologue_canon_encounter.rpy) MUST set
            # canon_first_scene = True and fall through to prologue_case1_hook, or the whole
            # canon route silently drops to non-canon. Keep this jump and that label in sync.
            jump prologue_canon_ending

        "Walk out, this crossed a line.":
            $ unless_branch = "walk_out"
            $ rebuke += 2
            $ kaoru_resistance += 2
            voice "audio/voice/toa_051.mp3"
            toa "Unless I find a magistrate who reads dates instead of moods. Good evening."

            voice "audio/voice/kaoru_067.mp3"
            kaoru "You'll be back. The permit still expires."

            jump prologue_walkout_ending

label prologue_verbal_ending:

    scene bg magistrate_office with dissolve
    show kaoru thinking at left
    show toa determined at right

    show kaoru amused
    voice "audio/voice/kaoru_068.mp3"
    kaoru "You negotiate with your mouth. Adequate."

    show toa happy
    voice "audio/voice/toa_052.mp3"
    toa "And with my feet, when the dance required it. Sign the page, Magistrate-sama."

    show kaoru cold
    voice "audio/voice/kaoru_069.mp3"
    kaoru "Almost."

    voice "audio/voice/narrator_035.mp3"
    "He lifts the hanko, teasing height above the permit book, then sets it down untouched."

    show toa angry
    voice "audio/voice/toa_053.mp3"
    toa "That isn't justice. It's just cruelty, and you know it."

    show kaoru smirk
    voice "audio/voice/kaoru_070.mp3"
    kaoru "Justice arrives when you stop treating my office like a stage you can exit on your terms."

    show toa worried
    voice "audio/voice/toa_054.mp3"
    toa "I gave you the performance. I named my price. What more..."

    show kaoru commanding
    voice "audio/voice/kaoru_071.mp3"
    kaoru "More requires more. Leave before I charge you for the water you made me drink."

    show toa determined
    voice "audio/voice/toa_055.mp3"
    toa "I'll be back. With a better argument and dry obijime."

    show kaoru charm
    voice "audio/voice/kaoru_072.mp3"
    kaoru "I'll be here. Dates don't renew themselves."

    voice "audio/voice/narrator_442.mp3"
    "He does not sign the permit. But a provisional gate-chit slides across the lacquer, forward-dated, the ink barely dry: enough to keep the gate guards from hauling her in before she finds a better argument."

    $ show_cg_scene("corridor_lost", fade)
    play music audio.bgm_corridor fadein 2.0 loop volume 0.58

    voice "audio/voice/narrator_036.mp3"
    "The corridor is colder than the office. Somewhere a bell marks the hour, not dawn, not yet."

    voice "audio/voice/toa_056.mp3"
    toa "Three weeks. I can survive three weeks on curry and pride."

    voice "audio/voice/toa_057.mp3"
    toa "Snacks first. Justice second. I can hold that order for three weeks."

    jump prologue_case1_hook

label prologue_walkout_ending:

    scene bg magistrate_office with dissolve
    show toa angry at right
    show kaoru cold at left

    show toa determined
    voice "audio/voice/toa_058.mp3"
    toa "I came for a seal, not a lesson in your appetite."

    show kaoru cold
    voice "audio/voice/kaoru_073.mp3"
    kaoru "Then go. The city has other dancers and fewer scruples."

    voice "audio/voice/narrator_037.mp3"
    "She snatches the permit book. The hanko case stays, his, or forgotten, or a trap she refuses to spring."

    show kaoru smirk
    voice "audio/voice/kaoru_074.mp3"
    kaoru "You'll knock again when the gate guards ask for paper you don't have."

    $ show_cg_scene("corridor_lost")

    voice "audio/voice/toa_059.mp3"
    toa "Wrong door once was a mistake. I won't make it a habit."

    play sound audio.footsteps_corridor volume 0.85
    voice "audio/voice/narrator_038.mp3"
    "Lantern light stripes the floor. Her boots echo too loud for the noble quarter."

    voice "audio/voice/toa_060.mp3"
    toa "Guest room previews and forward-dated seals can wait. I still have pride."

    voice "audio/voice/toa_061.mp3"
    toa "...And a curry shop that doesn't ask questions."

    # Walking out is a boundary she is allowed to hold, not a death sentence. The
    # permit still expires, so pride cools and she returns three weeks later, non-canon
    # (unless_branch == "walk_out" pays off the "you came back" lines in case1_companion /
    # case1_investigation, and revives the rebuke axis). The brutal Kaoru-pursuit end
    # (prologue_bad_end_kaoru) remains reachable from the dev chapter-pick menu only.
    jump prologue_case1_hook

# --- DEV: content warning; implied coercion / violence; fade-to-black only. ---

label prologue_bad_end_kaoru:

    play music audio.bgm_bad_ending fadein 2.0 loop volume 0.52

    voice "audio/voice/narrator_213.mp3"
    "She turns the corner too fast. Behind her, boots do not hurry, they count."

    play sound audio.footsteps_corridor volume 0.9
    show kaoru cold at center

    voice "audio/voice/kaoru_243.mp3"
    kaoru "To-chan. My corridor. My hanko. You have neither."

    show toa angry at right
    voice "audio/voice/toa_201.mp3"
    toa "You said go."

    show kaoru cold
    voice "audio/voice/kaoru_242.mp3"
    kaoru "I said the city has other dancers. I did not release you from my hall."

    play sound audio.footsteps_corridor volume 0.95
    voice "audio/voice/narrator_212.mp3"
    "She runs for the outer gate. Lacquer and iron have not opened for petitioners this late, only for magistrates who forgot to lock shame inside."

    $ show_cg_scene("badend_kaoru_gate")

    voice "audio/voice/narrator_211.mp3"
    "The gate bars are down. Night watchmen pretend not to hear. They know whose seal buys silence in this quarter."

    show toa worried
    voice "audio/voice/toa_200.mp3"
    toa "Let me through... I'm not your..."

    show kaoru commanding at left
    voice "audio/voice/kaoru_241.mp3"
    kaoru "My escort list ends at my threshold. You're still on the docket."

    play sound audio.chair_creak volume 0.7
    voice "audio/voice/kaoru_240.mp3"
    kaoru "Desk. Now. The latch stays down until I say otherwise."

    voice "audio/voice/narrator_210.mp3"
    "His hand closes on her wrist, not a lover's grip, a clerk's. Fingers find the pulse the way he finds a misplaced line."

    $ show_cg_scene("badend_kaoru_wrist", fade)

    $ set_expression("toa", "angry")
    voice "audio/voice/toa_194.mp3"
    toa "Let go...!"

    voice "audio/voice/kaoru_239.mp3"
    kaoru "You carried my permit book out. That makes you my errand until I cancel it."

    $ show_cg_scene("badend_kaoru_corridor")

    voice "audio/voice/narrator_209.mp3"
    "He hauls her back through the corridor the way a seal returns to its case, boots skidding on polished wood, lantern stripes racing across her face."

    play sound audio.sliding_door_close volume 0.85

    voice "audio/voice/kaoru_238.mp3"
    kaoru "Wrong door was amusing once. I'm not amused anymore."

    $ set_expression("toa", "worried")
    voice "audio/voice/toa_199.mp3"
    toa "The watch can see..."

    voice "audio/voice/kaoru_237.mp3"
    kaoru "The watch files what I sign. You ran from my desk with wet ink on your sleeve."

    voice "audio/voice/kaoru_236.mp3"
    kaoru "Permit book without ink is just paper. You are still line item on my evening."

    $ set_expression("toa", "angry")
    voice "audio/voice/toa_198.mp3"
    toa "You can't..."

    $ set_expression("kaoru", "smirk")
    voice "audio/voice/kaoru_235.mp3"
    kaoru "Watch me stamp something that isn't your renewal."

    $ show_cg_scene("badend_kaoru_stamp")

    voice "audio/voice/narrator_208.mp3"
    "Red wax blooms under his hanko, not on her permit, but on a narrow custody chit he had waiting."

    voice "audio/voice/kaoru_234.mp3"
    kaoru "Companion escort, temporary. I know what I'm paying for tonight."

    $ show_cg_scene("badend_kaoru_office")

    voice "audio/voice/narrator_207.mp3"
    "The guest-room mat. The cushion she refused to preview. The docket stack still warm where she flung her pride."

    $ set_expression("toa", "determined")
    voice "audio/voice/toa_197.mp3"
    toa "I won't bow to your appetite..."

    voice "audio/voice/kaoru_233.mp3"
    kaoru "You bow when the floor meets your knees. Less talk."

    voice "audio/voice/narrator_206.mp3"
    "He turns, not in haste, but enough. Her shoulder meets air where his sleeve was."

    $ show_cg_scene("badend_kaoru_office_throw")

    voice "audio/voice/narrator_187.mp3"
    "The mat rushes up. Paper scatters like startled herons. The permit book skids under the desk where he wanted it in the first place."

    pause 0.5

    $ show_cg_scene("badend_kaoru_office_floor")

    $ set_expression("toa", "worried")
    voice "audio/voice/toa_193.mp3"
    toa "...Get up. Crane girls get up."

    voice "audio/voice/narrator_186.mp3"
    "Her arms do not answer. Pride was a costume. Under it she is only breath and bruised obi and the taste of his corridor."

    voice "audio/voice/kaoru_226.mp3"
    kaoru "There. Now you're low enough to hear terms."

    pause 0.4

    centered "{size=-2}This ending is brutal. Implied violence ahead.{/size}"

    menu:
        "Continue.":
            pass

        "Return to title.":
            stop music fadeout 1.5
            return

    window hide
    $ show_cg_scene("badend_kaoru_shoji", fade)

    voice "audio/voice/narrator_185.mp3"
    "The office door seals. Lamplight shrinks to a strip under the shoji."

    voice "audio/voice/narrator_184.mp3"
    "From the hall, clerks hear nothing, or learn to hear nothing. Emerald Magistrate business."

    voice "audio/voice/kaoru_232.mp3"
    kaoru "You'll knock again when hunger wins. Tonight I collect what you owed at the chair."

    $ set_expression("toa", "soft")
    voice "audio/voice/toa_192.mp3"
    toa "..."

    voice "audio/voice/narrator_183.mp3"
    "What happens next is not entered in any clerk's ledger, only in the ache she will carry if she survives the night."

    pause 0.6

    stop music fadeout 3.0
    scene black with fade
    pause 0.6

    centered "{size=+14}Game Over{/size}"
    pause 0.4

    centered "{size=+4}The End{/size}\n{size=-4}Kakita Toa reached for the door.\nKitsu Kaoru owned the hall.{/size}"

    return

# Canon encounter, see prologue_canon_encounter.rpy

label prologue_case1_hook:

    # Bridge to Case 1, canon: companion offer (3 days); else: non-canon reopening (3 weeks).
    scene black with fade
    stop music fadeout 2.5
    pause 0.5

    if canon_first_scene:
        centered "Three days later..."
        jump case1_companion_offer
    else:
        centered "Three weeks later..."
        jump case1_noncanon_start
