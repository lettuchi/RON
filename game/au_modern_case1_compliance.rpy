# Modern AU Case 1: Wellness District Compliance (dev bonus sequel).
#
# Play: Main menu → "AU Case 1: Compliance"; dev pick → "AU Case 1: Wellness Compliance";
#   or Wrong Floor end → "Continue to Case 1?"; end → "Continue to island weekend?"
# VOICED: narrator_384+, toa_383+, kaoru_510+ (wire: scripts/wire_au_modern_case1_voice.py).
# Does not set canon case/permit flags.

default seen_au_modern_case1 = False
default au_modern_case1_witness_style = ""
default au_modern_case1_pushback = ""
default au_modern_case1_piano_mode = ""   # "" / precise / fumble (studio piano accompaniment beat)

label au_modern_case1_start:

    ## Launched in the rollback-enabled game (root) context, from the Modern AU hub
    ## (au_modern_hub_menu) or the dev chapter pick. Because this is the normal game
    ## context (not a call_in_new_context child of the menu), Back/rollback, mid-episode
    ## saving, character + narrator voices, and the quick/game menu all work without any
    ## menu-state fix-ups. Mark the AU episode active so the story-music mute callback
    ## keeps story BGM audible (incl. after loading a mid-episode save).
    $ au_episode_active = True
    $ enable_cinematic_music()

    $ seen_au_modern_case1 = True
    $ au_modern_case1_witness_style = ""
    $ au_modern_case1_pushback = ""

    scene black with fade
    play music audio.bgm_street fadein 2.5 loop volume 0.34

    centered "{font=fonts/YujiSyuku-Regular.ttf}{size=+6}Wellness Compliance{/size}{/font}\n{size=-4}Modern AU · Case 1 · dev bonus{/size}"

    pause 1.0

    $ show_cg_scene("au_modern_case1_predawn_tower", fade)
    pause 2.0

    voice "audio/voice/narrator_467.mp3"
    "Three business days after the wrong conference room, the sponsorship is signed and Ryoko Port still files rain against every window it owns. The fast track turned out to be a person. The person, it turns out, comes with errands."

    voice "audio/voice/narrator_468.mp3"
    "Kakita Toa's sponsorship packet now carries a deputy director's chop and a witness clause she did not read until it became mandatory."

    voice "audio/voice/narrator_475.mp3"
    "The witness clause is the price of a fast Council sponsorship. She attends the deputy's inspections, documents what he points at, and proves on the record that the signatory who vouched for her is not inventing or favoring the artists he licenses. It is favoritism insurance, filed in advance, for a favoritism nobody has committed yet. Skip an inspection and the standing that gets revoked is hers, not his."

    voice "audio/voice/toa_383.mp3"
    toa "Mandatory on-site witness for a surprise inspection. That sounds like a field trip with liability."

    voice "audio/voice/kaoru_592.mp3"
    kaoru "It sounds like you attend, you document, and you do not perform gratitude on municipal letterhead. Again."

    voice "audio/voice/toa_468.mp3"
    toa "Favoritism insurance. I document your inspections so the Council can see you are not handing permits to artists you happen to like. The irony writes itself. I am simply not allowed to laugh about it on the record."

    jump au_modern_case1_wellness_arrival


label au_modern_case1_wellness_arrival:

    voice "audio/voice/narrator_386.mp3"
    "The wellness corridor is a row of Council-licensed calm: massage studios, float tanks, candle rhetoric under one neon awning, every storefront holding an operating license his office issued. This is the first inspection her witness clause requires her to stand through. Deputy Director Kitsu Kaoru walks it like the queue is already behind him."

    $ show_cg_scene("au_modern_case1_club_exterior", fade)
    pause 2.0

    voice "audio/voice/toa_384.mp3"
    toa "Velvet Lantern Wellness Collective. The sign promises serenity in four fonts."

    voice "audio/voice/kaoru_511.mp3"
    kaoru "Their operating license promises posted occupancy, working fire exits, and honest books. My inspection confirms it, or my office pulls the license. The witness log needs a sponsor artist on it. That is you."

    voice "audio/voice/narrator_387.mp3"
    "Harbor mist and pink neon turn the wet sidewalk into a brochure nobody asked for."

    voice "audio/voice/narrator_476.mp3"
    "The Office of Arts and Licensing signs the artists and licenses the storefronts, both under the same Council seal. The office that stamped her sponsorship is the office that can decide whether this spa keeps its doors. Today both halves of the deputy's jurisdiction share one wet sidewalk, and she is standing on the artist half of it."

    jump au_modern_case1_inspection_floor


label au_modern_case1_inspection_floor:

    scene black with dissolve
    pause 0.4

    $ show_cg_scene("au_modern_case1_clipboard", fade)
    pause 2.0

    voice "audio/voice/narrator_471.mp3"
    "Inside the Velvet Lantern, the lobby smells of eucalyptus and money pretending to be mindfulness. Soft music hides the diesel and the ferries under panpipes. Toa raises her phone and waits to be told what counts as evidence."

    voice "audio/voice/kaoru_512.mp3"
    kaoru "Surprise inspection. No appointment. If they scrub the lobby, we note the scrub."

    voice "audio/voice/narrator_388.mp3"
    "His clipboard is municipal grey. Her phone is personal black. Both will end up in the same PDF."

    voice "audio/voice/toa_385.mp3"
    toa "Do I film everything or only what you point at?"

    voice "audio/voice/kaoru_513.mp3"
    kaoru "You film what I tell you is exhibit-worthy. Flirt with the lens on your own time."

    voice "audio/voice/narrator_389.mp3"
    "The front desk host smiles like a man who has never seen a deputy director before noon."

    jump au_modern_case1_llc_joke


label au_modern_case1_llc_joke:

    $ show_cg_scene("au_modern_case1_float_tank", fade)
    pause 2.0

    voice "audio/voice/kaoru_514.mp3"
    kaoru "Operating entity on file: Scorpion-grey Holdings LLC. Cute. File that under *names that audition for subpoenas*."

    voice "audio/voice/toa_386.mp3"
    toa "Is that a problem or a punchline?"

    voice "audio/voice/kaoru_515.mp3"
    kaoru "It is a line item. Grey LLCs love grey corridors. We walk them anyway."

    voice "audio/voice/narrator_390.mp3"
    "Toa bites her cheek so she does not laugh in a room that already smells like eucalyptus and panic."

    $ show_cg_scene("au_modern_case1_phone_notes", fade)
    pause 2.0

    voice "audio/voice/kaoru_516.mp3"
    kaoru "Witness protocol. Choose how you document before I choose for you."

    menu au_modern_case1_witness_menu:

        "Film timestamped video notes (thorough).":
            $ au_modern_case1_witness_style = "film"
            voice "audio/voice/toa_387.mp3"
            toa "Timestamped video. If they move a chair, the chair has a timecode."

            voice "audio/voice/kaoru_517.mp3"
            kaoru "Good. Bureaucracy loves clocks. So do I, when they save me a hearing."

        "Typed witness log only (discreet).":
            $ au_modern_case1_witness_style = "log"
            voice "audio/voice/toa_388.mp3"
            toa "Typed log. Quiet thumbs. No flash."

            voice "audio/voice/kaoru_518.mp3"
            kaoru "Also acceptable. Do not typo my name. I will notice."

    jump au_modern_case1_bureaucracy_flirt


label au_modern_case1_bureaucracy_flirt:

    voice "audio/voice/narrator_391.mp3"
    "They move through treatment rooms that are legally not treatment rooms until the inspector says otherwise."

    $ show_cg_scene("au_modern_case1_kaoru_doorway", fade)
    pause 2.0

    voice "audio/voice/kaoru_519.mp3"
    kaoru "Form 14-C requires posted capacity. Count the candles as people and I will cite you for poetry."

    voice "audio/voice/toa_389.mp3"
    toa "Fourteen seats, twelve candles, one diffuser working overtime."

    $ show_cg_scene("au_modern_case1_capacity_count", fade)
    pause 2.0

    voice "audio/voice/kaoru_520.mp3"
    kaoru "Write *diffuser exceeds serenity*. That is flirtation via footnote, To-chan, and I allow it once."

    voice "audio/voice/toa_390.mp3"
    toa "You called me To-chan in a wellness closet. Is that witness work or harassment?"

    voice "audio/voice/kaoru_521.mp3"
    kaoru "It is scheduling. You respond faster when I use the nickname inventory."

    voice "audio/voice/narrator_392.mp3"
    "Her phone buzzes with a calendar ping she is not allowed to open during an active inspection. The portal only ever pings her with the next thing he has already filed."

    jump au_modern_case1_manager_pushback


label au_modern_case1_manager_pushback:

    voice "audio/voice/narrator_393.mp3"
    "The floor manager finds them at the aromatherapy storage door. His badge says *Director of Calm*."

    $ show_cg_scene("au_modern_case1_manager_standoff", fade)
    pause 2.0

    voice "audio/voice/kaoru_522.mp3"
    kaoru "You are interrupting a Council inspection of a license this office issued and this office can revoke. Step aside, or join the exhibit list."

    menu au_modern_case1_pushback_menu:

        "Stand with the deputy (firm witness).":
            $ au_modern_case1_pushback = "firm"
            voice "audio/voice/toa_391.mp3"
            toa "Deputy Director Kitsu is on record. I am on record. Your hallway is on record."

            voice "audio/voice/narrator_394.mp3"
            "The manager's smile dies in a very professional way."

            jump au_modern_case1_hallway_tense

        "Defuse with sponsor charm (soft witness).":
            $ au_modern_case1_pushback = "soft"
            voice "audio/voice/toa_392.mp3"
            toa "We only need five more minutes and your posted capacity chart. Sponsorship requires patience."

            $ show_cg_scene("au_modern_case1_charm_defuse", fade)
            pause 2.0

            voice "audio/voice/kaoru_523.mp3"
            kaoru "She said patience. I said compliance. Both are true. Move."

            voice "audio/voice/narrator_395.mp3"
            "He moves. The corridor exhales eucalyptus and defeat."

            jump au_modern_case1_studio_session


label au_modern_case1_hallway_tense:

    $ show_cg_scene("au_modern_case1_hallway_tense", fade)
    pause 2.0

    voice "audio/voice/narrator_396.mp3"
    "For ten seconds the hallway is only rain on glass, clipboard metal, and a man deciding whether calm is a job title or a threat."

    voice "audio/voice/kaoru_524.mp3"
    kaoru "You wanted firm. He learned firm. Log the timestamp."

    voice "audio/voice/toa_393.mp3"
    toa "Logged. My hands shook. That is also on the record."

    $ show_cg_scene("au_modern_case1_wrist_pulse", dissolve)
    pause 2.0

    voice "audio/voice/kaoru_525.mp3"
    kaoru "Shaking is human. Falsifying is not. Continue."

    jump au_modern_case1_studio_session


label au_modern_case1_studio_session:

    # New beat: the witness clause inverts. He has made her document four of his
    # inspections; today he witnesses one of hers, a ballet class, and ends up
    # accompanying it himself at a studio piano. Emotional hinge for Kaoru's arc
    # (duty -> respect -> care). Reuses existing studio CGs; no new art. All lines
    # below are NEW and SILENT (no voice id yet); see scripts/au_metaphor_ballet_new_lines.txt.
    scene black with dissolve
    play music audio.bgm_canon_intimate fadein 2.0 loop volume 0.26
    pause 0.5

    $ show_cg_scene("au_modern_studio_audition", fade)
    pause 2.0

    "The city rents the corner studio by the hour, the same kind of room he had once made her audition in: mirror wall, a barre bolted along it, rain ticking the glass like a clerk tapping a stamp. The only new fact in the room is the upright piano against the far wall, municipal brown, a half-step out of tune, the lid already up as if it had been waiting for someone with a reason."

    kaoru "Your witness clause runs both directions today. You have documented four of my inspections. An auditor who has never seen the deliverable cannot certify it. So I am here to witness one of yours. Run a class. I will sit where I can see you and the mirror."

    toa "You want to witness a whole ballet class. Barre to reverence. Most of it is in French and none of it will hold still for your clipboard."

    kaoru "Then translate as you go. I have audited stranger languages than yours, and most of them were also hiding something in the footnotes."

    "She gave him the structure the way she would have given it to any inspector who asked, because narrating the next step was the only way to keep her hands from apologizing for the room."

    toa "Barre first. It warms the instrument, slow before fast, small before large. Plie, to bend. Tendu, to stretch the foot along the floor without lifting it. Degage, the same stretch let off the ground. Rond de jambe, the toe drawing a half circle. Then fondu, frappe, and grand battement, which is the leg thrown up like an objection nobody bothered to sustain. The order is not negotiable. Even the Council would approve of the order."

    $ show_cg_scene("toa_ballet_practice_room", fade)
    pause 2.0

    "He watched her run the barre with the flat attention he gave a hearing, counting under his breath, low and even, the way he had counted her once in this same kind of room. Plie and recover. Tendu front, side, back. Somewhere in the rond de jambe she stopped performing for the witness and simply worked, and he registered the difference the way he registered everything, and filed it where he filed the things he intended to keep."

    "She set her phone on the barre to play the centre music, a tinny recording through a speaker that had survived three tours. Kaoru looked at it the way he looked at a capacity chart that had already lied to him once."

    kaoru "That is a recording. A recording cannot tell whether you are early or whether you are apologizing. It plays the same eight bars at the same tempo whether you are a witness or a liability. It is a metronome that forgot it was supposed to be a human."

    toa "And you could do better, Deputy Director-sama. You, who count witness work out loud and call it a duty."

    kaoru "I read music. It is mostly counting with better penmanship and a key signature where the case number goes."

    "He stood, crossed the room, and did the thing she had never once managed to make him do across a desk. He took off the charcoal jacket, folded it over the barre with more care than he gave most applicants, rolled his sleeves to the forearm, and sat down at the municipal piano as if it were one more office the Council had assigned him. He set the stamp down. He met her on her floor, in her medium, where no signature he owned was worth a single thing."

    menu au_modern_case1_piano_menu:

        "Ask him for a repetiteur's ticket (precise, clinical at first).":
            $ au_modern_case1_piano_mode = "precise"

            toa "Then take a ticket, the way a class accompanist does. A repetiteur plays the dancer's instruction the way you read a filing. I hand you meter, tempo, quality, count. Adagio: a slow waltz, three-four time, smooth, thirty-two counts. Then play it like you mean it, not like you are proving the meter is compliant."

            kaoru "Three-four. Slow. Thirty-two. Noted."

            "He played it correctly and without one ounce of feeling, every bar squared to the edge like a citation, a man performing the meter to prove the meter existed. She danced the adagio to it anyway, developpe and promenade and the long arabesque line, and it was fine, and fine was the most insulting word in either of their vocabularies."

        "Let him fumble it and teach him by dancing (badly at first).":
            $ au_modern_case1_piano_mode = "fumble"

            toa "Adagio first. Slow waltz, three-four, smooth. Thirty-two counts. Try not to file the rests."

            "He fumbled the first eight bars the way a deputy fumbles a language he has only ever read in translation, a half beat behind her line, the left hand too literal, the waltz vamp landing like a stamp instead of a breath. She did not stop. She lifted into the developpe a fraction early and let her arm finish the phrase his hand had clipped short, teaching him with her spine the thing the file could not put into French."

    "And then, somewhere in the second pass, it happened, the small unscheduled thing. He stopped playing the count and started playing her. His left hand found the breath underneath the three-four and held the dancer instead of the meter. When she suspended at the top of the developpe he waited for her, the chord hanging until her balance asked for the next one, and he gave it to her exactly when she needed it and not a beat before. He was not a metronome anymore. He was listening. He was, against every clause he had ever drafted, accompanying her."

    "She felt the shift the way you feel a room change temperature. The piano stopped telling her what the tempo was and started asking what she wanted it to be, and answering. For eight bars the deputy director of the Office of Arts and Licensing was nobody's signatory of record. He was the man at the piano who had decided, mid-phrase, to meet her where she actually lived."

    $ show_cg_scene("toa_ballet_practice_room", dissolve)
    pause 2.0

    toa "You changed it. You stopped counting and started listening. Those are not the same skill. The first one keeps time. The second one keeps me."

    kaoru "A recording cannot do the second one. I find I object to being outperformed by a speaker that survived three tours. File it under professional pride and let it stay there."

    toa "I will file it wherever lets you keep doing it."

    "She ran the rest of the centre to his hands: pirouettes that found their spot because he gave her the downbeat to spot to, petit allegro snapped tight to a brisk two-four march, grand allegro carried clear across the floor on a waltz that finally let her leave the ground like she meant to. He watched and played at once, the witness and the accompaniment collapsed into one man in rolled sleeves, which she would not have believed of him an hour ago."

    kaoru "Grand allegro. You travel, I give you the bars to land in. Do not apologize on the descent. The descent is the part the board never watches and the only part that can hurt you."

    toa "Noted, Deputy Director-sama. I will land like I am allowed to be in the room."

    "When the class wound down he slowed without being asked, into something adagio and low, and she understood he had read far enough into the file to know what came last."

    toa "Reverence. The end of every class. A bow to the teacher, and a bow to the accompanist, because a dancer never thanks the audience first. She thanks the two people who actually held the room. There is no audience here. There is only the accompanist."

    "She curtsied to the piano. To him. He let the last chord ring out under the rain and did not deny the bow, did not rule against it, did not reach yet for the jacket folded over the barre and the title that lived in its breast pocket. For the length of one held chord he was only the man she had thanked, and he let himself be thanked, on no letterhead at all."

    if au_modern_case1_piano_mode == "fumble":
        kaoru "I played the first eight bars badly. Strike them from the witness log."

        toa "Denied. The bad eight bars are how I know the good ones were real. I am keeping the whole take, Deputy Director-sama."
    else:
        kaoru "I played it correctly before I played it well. Note the difference in your log. It is the only review I will ever file on myself."

        toa "Noted and entered. The correct version was compliant. The well version was you. I can tell them apart now, and I will never be able to stop."

    "He rolled his sleeves back down, refastened the cuffs, and reassembled the deputy director one button at a time. But he was slower about it than the file required, and she saw that too, and said nothing, because some witness work is kinder kept off the record."

    kaoru "We are due back at the tower. The inspection still has to close on paper. None of what just happened goes in that report. A studio with a piano is not a deliverable the Council keeps a box for."

    toa "Then it stays off letterhead. Like everything else you mean. I am learning the filing system, Deputy Director-sama. The real things go in the drawer with no label, and you guard that drawer harder than you guard the seal."

    "He did not confirm it. He held the studio door for her the way a gate holds weather, and the almost-smile got as far as his eyes before he filed it, and for once the filing took a visible second longer than it should have."

    jump au_modern_case1_passed_witness


label au_modern_case1_passed_witness:

    scene black with fade
    pause 0.4

    $ show_cg_scene("au_modern_case1_tower_debrief", fade)
    pause 2.0

    "He did not mention the studio on the walk back, and neither did she, which was its own kind of minutes. But he booked the harbor weekend that same afternoon, and she would wonder, later, whether the piano had moved the date up by a week."

    voice "audio/voice/narrator_397.mp3"
    "Back at the tower, the inspection closes without blood, without bodies, and with three minor citations the Council will post as politely worded threats against a storefront's operating license."

    voice "audio/voice/kaoru_526.mp3"
    kaoru "You passed witness work. That is not a compliment. It is a classification."

    voice "audio/voice/toa_394.mp3"
    toa "I'll take classifications that keep my sponsorship active."

    voice "audio/voice/kaoru_527.mp3"
    kaoru "There is a harbor weekend on the calendar, logged as an audit retreat. Continued witness work: your clause, my signature, the Council's letterhead. Ferry slips Saturday. One bed in the Airbnb filing is a clerical error I will not fix unless you ask in writing."

    voice "audio/voice/toa_395.mp3"
    toa "That sounds like Case 2 with salt air."

    voice "audio/voice/kaoru_528.mp3"
    kaoru "It sounds like a calendar invite. Accept on the municipal portal or argue with the tide."

    voice "audio/voice/toa_469.mp3"
    toa "Everything you offer is a calendar invite. The inspection, the weekend, possibly the rest of my life. I am starting to suspect the calendar is how you say the things you will not put in a sentence."

    if au_modern_case1_witness_style == "film" or au_modern_case1_pushback == "firm":
        jump au_modern_case1_elevator_echo
    else:
        jump au_modern_case1_end_stinger


label au_modern_case1_elevator_echo:

    voice "audio/voice/narrator_398.mp3"
    "The service elevator remembers them from the wrong-floor building. Rain stripes the glass. Proximity becomes paperwork if you stare at it long enough."

    $ show_cg_scene("au_modern_case1_elevator_echo", fade)
    pause 2.0

    voice "audio/voice/kaoru_529.mp3"
    kaoru "Unless the harbor?"

    voice "audio/voice/toa_396.mp3"
    toa "Unless the harbor. Not romance on letterhead."

    voice "audio/voice/kaoru_530.mp3"
    kaoru "Correct. File that under rider compliance."

    toa "Rider compliance. We have a clause for standing this close, a footnote for the elevator, a code for the harbor. The file has a word for everything we do except the one word for what it is."

    kaoru "The file uses the words I can defend. The word you mean stays off letterhead, where the board cannot read it back to us in a hearing. That is not a denial. That is custody."

    voice "audio/voice/narrator_399.mp3"
    "Their reflections almost touch in the glass. Neither reaches. The lift dings like a stamp."

    jump au_modern_case1_end_stinger


label au_modern_case1_end_stinger:

    scene black with fade
    stop music fadeout 2.0

    centered "{size=+2}Wellness Compliance (Modern AU Case 1){/size}\n{size=-4}Witness work filed. Harbor weekend pending.{/size}"

    pause 1.0

    jump au_modern_case1_end


label au_modern_case1_end:

    menu au_modern_case1_continue_case2_menu:

        "Continue to island weekend?":
            jump au_modern_case2_start

        "Return to menu.":
            pass

    if dev_chapter_pick_enabled:
        jump dev_chapter_pick_menu

    ## Back to the Modern AU hub (rollback-enabled game context). The hub clears
    ## au_episode_active and restores the menu theme.
    jump au_modern_hub_menu
