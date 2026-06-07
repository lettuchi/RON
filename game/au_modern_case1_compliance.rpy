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
    "Kakita Toa's packet carries his chop now, and a witness clause she did not read until it became mandatory. The rider she chose on the contract floor only decided how close he stood. Standard or exclusive, the witness clause came with both."
    voice "audio/voice/narrator_475.mp3"
    "The witness clause is the price of a fast Council sponsorship. She attends the deputy's inspections, documents what he points at, and proves on the record that the signatory who vouched for her is not inventing or favoring her. It is favoritism insurance, filed in advance, for a favoritism nobody has committed yet. Skip an inspection and the standing that gets revoked is hers, not his."
    voice "audio/voice/toa_383.mp3"
    toa "Mandatory on-site witness for a surprise inspection. That sounds like a field trip with liability."
    voice "audio/voice/kaoru_592.mp3"
    kaoru "It sounds like you attend, you document, and you do not perform gratitude on municipal letterhead. Again."
    voice "audio/voice/toa_468.mp3"
    toa "Favoritism insurance. I document your inspections so the Council can see you are not handing permits to artists you happen to favor. The irony writes itself. I am simply not allowed to laugh about it on the record."
    jump au_modern_case1_wellness_arrival


label au_modern_case1_wellness_arrival:

    $ show_cg_scene("au_modern_case1_club_exterior", fade)
    pause 1.0

    voice "audio/voice/narrator_386.mp3"
    "The wellness corridor is a row of Council-licensed calm: massage studios, float tanks, candle rhetoric under one neon awning, every storefront holding an operating license his office issued. This is the first inspection her witness clause requires her to stand through. Deputy Director Kitsu Kaoru walks it like the queue is already behind him."
    voice "audio/voice/toa_384.mp3"
    toa "Velvet Lantern Wellness Collective. The sign promises serenity in four fonts."
    voice "audio/voice/kaoru_511.mp3"
    kaoru "Their operating license promises posted occupancy, working fire exits, and honest books. My inspection confirms it, or my office pulls the license. The witness log needs a sponsor artist on it. That is you."
    voice "audio/voice/narrator_387.mp3"
    "Harbor mist and pink neon turn the wet sidewalk into a brochure nobody asked for."
    voice "audio/voice/narrator_476.mp3"
    "The Office of Arts and Licensing signs the artists and licenses the storefronts, both under the same Council seal. The office that stamped her sponsorship is the office that can decide whether this spa keeps its license. Today both halves of the deputy's jurisdiction share one wet sidewalk, and she is standing on the artist half of it."
    jump au_modern_case1_inspection_floor


label au_modern_case1_inspection_floor:

    $ show_cg_scene("au_modern_case1_clipboard", fade)
    pause 1.0

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
    pause 1.0

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
            $ show_cg_scene("au_modern_case1_witness_film", fade)
            pause 2.0

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

    $ show_cg_scene("au_modern_case1_corridor_walk", fade)
    pause 1.0

    voice "audio/voice/narrator_391.mp3"
    "They move through treatment rooms that are legally not treatment rooms. Not until the inspector says otherwise."
    $ show_cg_scene("au_modern_case1_kaoru_doorway", fade)
    pause 1.0

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

    $ show_cg_scene("au_modern_case1_manager_standoff", fade)
    pause 1.0

    voice "audio/voice/narrator_393.mp3"
    "The floor manager finds them at the aromatherapy storage door. His badge says *Director of Calm*."
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

    play music audio.bgm_canon_intimate fadein 2.0 loop volume 0.26

    $ show_cg_scene("au_modern_case1_studio_piano", fade)
    pause 1.0

    voice "audio/voice/narrator_507.mp3"
    "The city rents the corner studio by the hour,"
    voice "audio/voice/narrator_508.mp3"
    "the same kind of room he had once made her audition in: mirror wall, a barre bolted along it,"
    voice "audio/voice/narrator_509.mp3"
    "rain ticking the glass like a clerk tapping a stamp."
    voice "audio/voice/narrator_510.mp3"
    "The only new fact in the room is the upright piano against the far wall, municipal brown,"
    voice "audio/voice/narrator_511.mp3"
    "a half-step out of tune,"
    voice "audio/voice/narrator_512.mp3"
    "the lid already up as if it had been waiting for someone with a reason."

    voice "audio/voice/kaoru_596.mp3"
    kaoru "Your witness clause runs both directions today. You have documented four of my inspections."
    voice "audio/voice/kaoru_597.mp3"
    kaoru "An auditor who has never seen the deliverable cannot certify it."
    voice "audio/voice/kaoru_598.mp3"
    kaoru "So I am here to witness one of yours. Run a class."
    voice "audio/voice/kaoru_599.mp3"
    kaoru "I will sit where I can see you and the mirror."

    voice "audio/voice/toa_475.mp3"
    toa "You want to witness a whole ballet class. Barre to reverence."
    voice "audio/voice/toa_476.mp3"
    toa "Most of it is in French and none of it will hold still for your clipboard."

    voice "audio/voice/kaoru_600.mp3"
    kaoru "Then translate as you go."
    voice "audio/voice/kaoru_601.mp3"
    kaoru "I have audited stranger languages than yours,"
    voice "audio/voice/kaoru_602.mp3"
    kaoru "and most of them were also hiding something in the footnotes."

    voice "audio/voice/narrator_513.mp3"
    "She gave him the structure the way she would have given it to any inspector who asked, because narrating the next step was the only way to keep her hands from apologizing for the room."

    voice "audio/voice/toa_477.mp3"
    toa "Barre first. It warms the instrument, slow before fast, small before large. Plie, to bend. Tendu, to stretch the foot along the floor without lifting it."
    voice "audio/voice/toa_478.mp3"
    toa "Degage, the same stretch let off the ground. Rond de jambe, the toe drawing a half circle. Then fondu, frappe, and grand battement, which is the leg thrown up like an objection nobody bothered to sustain."
    voice "audio/voice/toa_479.mp3"
    toa "The order is not negotiable. Even the Council would approve of the order."

    $ show_cg_scene("au_modern_case1_barre_twoshot", fade)
    pause 2.0

    voice "audio/voice/narrator_514.mp3"
    "He watched her run the barre with the flat attention he gave a hearing,"
    voice "audio/voice/narrator_515.mp3"
    "counting under his breath, low and even,"
    voice "audio/voice/narrator_516.mp3"
    "the way he had counted her once in this same kind of room. Plie and recover."
    voice "audio/voice/narrator_517.mp3"
    "Tendu front, side, back."
    voice "audio/voice/narrator_518.mp3"
    "Somewhere in the rond de jambe she stopped performing for the witness and simply worked,"
    voice "audio/voice/narrator_519.mp3"
    "and he registered the difference the way he registered everything,"
    voice "audio/voice/narrator_520.mp3"
    "and filed it where he filed the things he intended to keep."

    voice "audio/voice/narrator_521.mp3"
    "She set her phone on the barre to play the centre music,"
    voice "audio/voice/narrator_522.mp3"
    "a tinny recording through a speaker that had survived three tours."
    voice "audio/voice/narrator_523.mp3"
    "Kaoru looked at it the way he looked at a capacity chart that had already lied to him once."

    voice "audio/voice/kaoru_603.mp3"
    kaoru "That is a recording."
    voice "audio/voice/kaoru_604.mp3"
    kaoru "A recording cannot tell whether you are early or whether you are apologizing."
    voice "audio/voice/kaoru_605.mp3"
    kaoru "It plays the same eight bars at the same tempo whether you are a witness or a liability."
    voice "audio/voice/kaoru_606.mp3"
    kaoru "It is a metronome that forgot it was supposed to be a human."

    voice "audio/voice/toa_480.mp3"
    toa "And you could do better, Deputy Director-sama."
    voice "audio/voice/toa_481.mp3"
    toa "You, who count witness work out loud and call it a duty."

    voice "audio/voice/kaoru_607.mp3"
    kaoru "I read music."
    voice "audio/voice/kaoru_608.mp3"
    kaoru "It is mostly counting with better penmanship and a key signature where the case number goes."

    voice "audio/voice/narrator_524.mp3"
    "He stood, crossed the room,"
    voice "audio/voice/narrator_525.mp3"
    "and did the thing she had never once managed to make him do across a desk."
    voice "audio/voice/narrator_526.mp3"
    "He took off the charcoal jacket,"
    voice "audio/voice/narrator_527.mp3"
    "folded it over the barre with more care than he gave most applicants,"
    voice "audio/voice/narrator_528.mp3"
    "rolled his sleeves to the forearm,"
    voice "audio/voice/narrator_529.mp3"
    "and sat down at the municipal piano as if it were one more office the Council had assigned him."
    voice "audio/voice/narrator_530.mp3"
    "He set the stamp down."
    voice "audio/voice/narrator_531.mp3"
    "He met her on her floor, in her medium, where no signature he owned was worth a single thing."

    $ show_cg_scene("au_modern_case1_piano_sit", dissolve)
    pause 2.0

    menu au_modern_case1_piano_menu:

        "Ask him for a repetiteur's ticket (precise, clinical at first).":
            $ au_modern_case1_piano_mode = "precise"

            voice "audio/voice/toa_482.mp3"
            toa "Then take a ticket, the way a class accompanist does."
            voice "audio/voice/toa_483.mp3"
            toa "A repetiteur plays the dancer's instruction the way you read a filing."
            voice "audio/voice/toa_484.mp3"
            toa "I hand you meter, tempo, quality, count."
            voice "audio/voice/toa_485.mp3"
            toa "Adagio: a slow waltz, three-four time, smooth, thirty-two counts."
            voice "audio/voice/toa_486.mp3"
            toa "Then play it like you mean it, not like you are proving the meter is compliant."

            voice "audio/voice/kaoru_609.mp3"
            kaoru "Three-four. Slow. Thirty-two. Noted."

            voice "audio/voice/narrator_532.mp3"
            "He played it correctly and without one ounce of feeling,"
            voice "audio/voice/narrator_533.mp3"
            "every bar squared to the edge like a citation,"
            voice "audio/voice/narrator_534.mp3"
            "a man performing the meter to prove the meter existed."
            voice "audio/voice/narrator_535.mp3"
            "She danced the adagio to it anyway, developpe and promenade and the long arabesque line,"
            voice "audio/voice/narrator_536.mp3"
            "and it was fine, and fine was the most insulting word in either of their vocabularies."

        "Let him fumble it and teach him by dancing (badly at first).":
            $ au_modern_case1_piano_mode = "fumble"

            voice "audio/voice/toa_487.mp3"
            toa "Adagio first. Slow waltz, three-four, smooth. Thirty-two counts. Try not to file the rests."

            voice "audio/voice/narrator_537.mp3"
            "He fumbled the first eight bars the way a deputy fumbles a language he has only ever read in"
            voice "audio/voice/narrator_538.mp3"
            "translation, a half beat behind her line, the left hand too literal,"
            voice "audio/voice/narrator_539.mp3"
            "the waltz vamp landing like a stamp instead of a breath. She did not stop."
            voice "audio/voice/narrator_540.mp3"
            "She lifted into the developpe a fraction early and let her arm finish the phrase his hand had"
            voice "audio/voice/narrator_541.mp3"
            "clipped short, teaching him with her spine the thing the file could not put into French."

    voice "audio/voice/narrator_542.mp3"
    "And then, somewhere in the second pass, it happened, the small unscheduled thing."
    voice "audio/voice/narrator_543.mp3"
    "He stopped playing the count and started playing her."
    voice "audio/voice/narrator_544.mp3"
    "His left hand found the breath underneath the three-four and held the dancer instead of the"
    voice "audio/voice/narrator_545.mp3"
    "meter."
    voice "audio/voice/narrator_546.mp3"
    "When she suspended at the top of the developpe he waited for her,"
    voice "audio/voice/narrator_547.mp3"
    "the chord hanging until her balance asked for the next one,"
    voice "audio/voice/narrator_548.mp3"
    "and he gave it to her exactly when she needed it and not a beat before."
    voice "audio/voice/narrator_549.mp3"
    "He was not a metronome anymore. He was listening."
    voice "audio/voice/narrator_550.mp3"
    "He was, against every clause he had ever drafted, accompanying her."

    voice "audio/voice/narrator_551.mp3"
    "She felt the shift the way you feel a room change temperature."
    voice "audio/voice/narrator_552.mp3"
    "The piano stopped telling her what the tempo was and started asking what she wanted it to be,"
    voice "audio/voice/narrator_553.mp3"
    "and answering."
    voice "audio/voice/narrator_554.mp3"
    "For eight bars the deputy director of the Office of Arts and Licensing was nobody's signatory"
    voice "audio/voice/narrator_555.mp3"
    "of record."
    voice "audio/voice/narrator_556.mp3"
    "He was the man at the piano who had decided, mid-phrase, to meet her where she actually lived."

    $ show_cg_scene("au_modern_case1_piano_lookup", dissolve)
    pause 2.0

    voice "audio/voice/toa_488.mp3"
    toa "You changed it. You stopped counting and started listening. Those are not the same skill."
    voice "audio/voice/toa_489.mp3"
    toa "The first one keeps time. The second one keeps me."

    voice "audio/voice/kaoru_610.mp3"
    kaoru "A recording cannot do the second one."
    voice "audio/voice/kaoru_611.mp3"
    kaoru "I find I object to being outperformed by a speaker that survived three tours."
    voice "audio/voice/kaoru_612.mp3"
    kaoru "File it under professional pride and let it stay there."

    voice "audio/voice/toa_490.mp3"
    toa "I will file it wherever lets you keep doing it."

    voice "audio/voice/narrator_557.mp3"
    "She ran the rest of the centre to his hands: pirouettes that found their spot because he gave"
    voice "audio/voice/narrator_558.mp3"
    "her the downbeat to spot to, petit allegro snapped tight to a brisk two-four march,"
    voice "audio/voice/narrator_559.mp3"
    "grand allegro carried clear across the floor on a waltz that finally let her leave the ground"
    voice "audio/voice/narrator_560.mp3"
    "like she meant to."
    voice "audio/voice/narrator_561.mp3"
    "He watched and played at once,"
    voice "audio/voice/narrator_562.mp3"
    "the witness and the accompaniment collapsed into one man in rolled sleeves,"
    voice "audio/voice/narrator_563.mp3"
    "which she would not have believed of him an hour ago."

    voice "audio/voice/kaoru_613.mp3"
    kaoru "Grand allegro. You travel, I give you the bars to land in. Do not apologize on the descent."
    voice "audio/voice/kaoru_614.mp3"
    kaoru "The descent is the part the board never watches and the only part that can hurt you."

    voice "audio/voice/toa_491.mp3"
    toa "Noted, Deputy Director-sama. I will land like I am allowed to be in the room."

    voice "audio/voice/narrator_564.mp3"
    "When the class wound down he slowed without being asked, into something adagio and low,"
    voice "audio/voice/narrator_565.mp3"
    "and she understood he had read far enough into the file to know what came last."

    voice "audio/voice/toa_492.mp3"
    toa "Reverence. The end of every class."
    voice "audio/voice/toa_493.mp3"
    toa "A bow to the teacher, and a bow to the accompanist,"
    voice "audio/voice/toa_494.mp3"
    toa "because a dancer never thanks the audience first."
    voice "audio/voice/toa_495.mp3"
    toa "She thanks the two people who actually held the room. There is no audience here."
    voice "audio/voice/toa_496.mp3"
    toa "There is only the accompanist."

    $ show_cg_scene("au_modern_case1_reverence", dissolve)
    pause 2.0

    voice "audio/voice/narrator_566.mp3"
    "She curtsied to the piano. To him."
    voice "audio/voice/narrator_567.mp3"
    "He let the last chord ring out under the rain and did not deny the bow,"
    voice "audio/voice/narrator_568.mp3"
    "did not rule against it,"
    voice "audio/voice/narrator_569.mp3"
    "did not reach yet for the jacket folded over the barre and the title that lived in its breast"
    voice "audio/voice/narrator_570.mp3"
    "pocket."
    voice "audio/voice/narrator_571.mp3"
    "For the length of one held chord he was only the man she had thanked,"
    voice "audio/voice/narrator_572.mp3"
    "and he let himself be thanked, on no letterhead at all."

    if au_modern_case1_piano_mode == "fumble":
        voice "audio/voice/kaoru_615.mp3"
        kaoru "I played the first eight bars badly. Strike them from the witness log."

        voice "audio/voice/toa_497.mp3"
        toa "Denied. The bad eight bars are how I know the good ones were real."
        voice "audio/voice/toa_498.mp3"
        toa "I am keeping the whole take, Deputy Director-sama."
    else:
        voice "audio/voice/kaoru_616.mp3"
        kaoru "I played it correctly before I played it well. Note the difference in your log."
        voice "audio/voice/kaoru_617.mp3"
        kaoru "It is the only review I will ever file on myself."

        voice "audio/voice/toa_499.mp3"
        toa "Noted and entered. The correct version was compliant. The well version was you."
        voice "audio/voice/toa_500.mp3"
        toa "I can tell them apart now, and I will never be able to stop."

    voice "audio/voice/narrator_573.mp3"
    "He rolled his sleeves back down, refastened the cuffs,"
    voice "audio/voice/narrator_574.mp3"
    "and reassembled the deputy director one button at a time."
    voice "audio/voice/narrator_575.mp3"
    "But he was slower about it than the file required, and she saw that too, and said nothing,"
    voice "audio/voice/narrator_576.mp3"
    "because some witness work is kinder kept off the record."

    voice "audio/voice/kaoru_618.mp3"
    kaoru "We are due back at the tower. The inspection still has to close on paper."
    voice "audio/voice/kaoru_619.mp3"
    kaoru "None of what just happened goes in that report."
    voice "audio/voice/kaoru_620.mp3"
    kaoru "A studio with a piano is not a deliverable the Council keeps a box for."

    voice "audio/voice/toa_501.mp3"
    toa "Then it stays off letterhead. Like everything else you mean."
    voice "audio/voice/toa_502.mp3"
    toa "I am learning the filing system, Deputy Director-sama."
    voice "audio/voice/toa_503.mp3"
    toa "The real things go in the drawer with no label,"
    voice "audio/voice/toa_504.mp3"
    toa "and you guard that drawer harder than you guard the seal."

    voice "audio/voice/narrator_577.mp3"
    "He did not confirm it."
    voice "audio/voice/narrator_578.mp3"
    "He held the studio door for her the way a gate holds weather,"
    voice "audio/voice/narrator_579.mp3"
    "and the almost-smile got as far as his eyes before he filed it,"
    voice "audio/voice/narrator_580.mp3"
    "and for once the filing took a visible second longer than it should have."

    jump au_modern_case1_passed_witness


label au_modern_case1_passed_witness:

    $ show_cg_scene("au_modern_case1_tower_debrief", fade)
    pause 1.0

    voice "audio/voice/narrator_581.mp3"
    "He did not mention the studio on the walk back, and neither did she,"
    voice "audio/voice/narrator_582.mp3"
    "which was its own kind of minutes."
    voice "audio/voice/narrator_583.mp3"
    "But he booked the harbor weekend that same afternoon, and she would wonder, later,"
    voice "audio/voice/narrator_584.mp3"
    "whether the piano had moved the date up by a week."

    voice "audio/voice/narrator_397.mp3"
    "Back at the tower, the inspection closes without blood, without bodies, and with three minor citations the Council will post as politely worded threats against a"
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

    $ show_cg_scene("au_modern_case1_elevator_echo", fade)
    pause 1.0

    voice "audio/voice/narrator_398.mp3"
    "The service elevator remembers them from the wrong-floor building. Rain stripes the glass. Proximity becomes paperwork if you stare at it long enough."
    voice "audio/voice/kaoru_529.mp3"
    kaoru "Unless the harbor?"
    voice "audio/voice/toa_396.mp3"
    toa "Unless the harbor. Not romance on letterhead."
    voice "audio/voice/kaoru_530.mp3"
    kaoru "Correct. File that under rider compliance."

    voice "audio/voice/toa_474.mp3"
    toa "Rider compliance. We have a clause for standing this close, a footnote for the elevator, a code for the harbor. The file has a word for everything we do except the one word for what it is."

    voice "audio/voice/kaoru_595.mp3"
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
