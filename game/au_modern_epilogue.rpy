# Modern AU Epilogue: "Effective Immediately" (dev bonus; trilogy cap).
#
# Play: Bonus: Modern AU submenu -> "AU Epilogue: Effective Immediately";
#   dev pick -> "AU Epilogue: Effective Immediately";
#   or Case 3 end -> "Continue to the Epilogue?"
# VOICED: narrator_446+, toa_441+, kaoru_572+ (wire: scripts/wire_au_modern_epilogue_voice.py).
#   New IDs sit strictly above the canon review block (toa_435-440, narrator_440-445,
#   kaoru_566-571) and above every existing AU id. Menu choice labels are NOT voiced.
# New choice flags live in game/stats.rpy (au_modern_epilogue_*); reads existing AU flags
#   (au_modern_case3_disclosure, au_modern_case2_night_audit) for continuity callbacks.
# Does not set canon case/permit flags. This is the final Modern AU episode (no next case).

label au_modern_epilogue_start:

    ## Launched in the rollback-enabled game (root) context, from the Modern AU hub
    ## (au_modern_hub_menu) or the dev chapter pick. Because this is the normal game
    ## context (not a call_in_new_context child of the menu), Back/rollback, mid-episode
    ## saving, character + narrator voices, and the quick/game menu all work without any
    ## menu-state fix-ups. Mark the AU episode active so the story-music mute callback
    ## keeps story BGM audible (incl. after loading a mid-episode save).
    $ au_episode_active = True
    $ enable_cinematic_music()

    $ seen_au_modern_epilogue = True
    $ au_modern_epilogue_waiting = ""
    $ au_modern_epilogue_posture = ""
    $ au_modern_epilogue_audit = False

    scene black with fade
    play music audio.bgm_office fadein 2.5 loop volume 0.30

    centered "{font=fonts/YujiSyuku-Regular.ttf}{size=+6}Effective Immediately{/size}{/font}\n{size=-4}Modern AU · Epilogue · dev bonus{/size}"

    pause 1.0

    $ show_cg_scene("au_modern_epilogue_replaced_phone", fade)
    pause 1.0

    voice "audio/voice/narrator_446.mp3"
    "Months after People and Conduct closed the conflict-of-interest file on its own quiet terms, the harbor turned cold and the clip stopped being about her. Ryoko Port moves on the way a feed moves on. It finds a louder fool and forgets the quiet one."
    voice "audio/voice/toa_441.mp3"
    toa "Deputy Director-sama. You have been replaced. The channel found a louder clip. A councilor narrated nine minutes of a budget meeting with his microphone muted. The internet calls it *muted councilor energy*."
    voice "audio/voice/toa_442.mp3"
    toa "I am no longer the mystery girl. I am, at most, a footnote with good hair."
    voice "audio/voice/kaoru_572.mp3"
    kaoru "Footnotes outlive headlines. That is the only fame worth filing."
    voice "audio/voice/narrator_447.mp3"
    "The crane on her tracksuit catches the lamp, gold over her heart, the same black jacket she wore into the wrong conference room a year of queue ago. She owns newer ones. She keeps wearing this one. It stopped apologizing in the shoulders somewhere around the harbor."
    $ show_cg_scene("au_modern_epilogue_year_later", fade)
    pause 2.0

    voice "audio/voice/toa_443.mp3"
    toa "The People and Conduct fishbowl went quiet months back. The folder with two names in it closed, one way or another, on terms the building agreed to carry. The building wanted a story it could stamp. It never got one."
    if au_modern_case3_disclosure == "personal":
        voice "audio/voice/kaoru_573.mp3"
        kaoru "The disclosure sits in the permanent file in my own hand. *Personal relationship, disclosed, oversight accepted.* The internet, bored of the truth, went hunting for a man with a muted mic instead."
    else:
        voice "audio/voice/kaoru_574.mp3"
        kaoru "We kept it procedural. Another desk reviews your packet now, and the file closed clean. The internet, bored of clean, went hunting for a man with a muted mic instead."
    jump au_modern_epilogue_letterhead


label au_modern_epilogue_letterhead:

    $ show_cg_scene("au_modern_epilogue_office_date", fade)
    pause 1.0

    voice "audio/voice/narrator_448.mp3"
    "He turns his monitor toward her, the way he once turned it to show her the gap between two ledgers. The calendar again. Thirty-one applicants, four inspections, a standing Friday row that used to read *audit retreat* in the dry font the portal assigns to everything it does not have feelings about."
    voice "audio/voice/narrator_449.mp3"
    "It does not read *audit retreat* anymore. Someone has written over the row by hand. His hand. The row says, in ink, on a calendar the whole licensing wing can open, a date. Not the noun of it. The plain fact of it."
    voice "audio/voice/toa_444.mp3"
    toa "You filed a date on letterhead. In your own handwriting. You. The man who spent three cases insisting it was not romance on letterhead."
    voice "audio/voice/kaoru_575.mp3"
    kaoru "It was not, then. It is, now. I amended the filing. The letterhead caught up to the calendar. The calendar caught up to the harbor."
    voice "audio/voice/toa_516.mp3"
    toa "You spent three cases teaching me what *on letterhead* meant."
    voice "audio/voice/toa_517.mp3"
    toa "That filing us as real was the one motion you would not grant."
    voice "audio/voice/toa_518.mp3"
    toa "And now you have granted it in your own hand, on the Council's own grid,"
    voice "audio/voice/toa_519.mp3"
    toa "where the building keeps the things it cannot take back."
    voice "audio/voice/toa_520.mp3"
    toa "You did not keep us off the record to hide. You put us on it so no one could."

    voice "audio/voice/toa_445.mp3"
    toa "Effective when?"
    voice "audio/voice/kaoru_576.mp3"
    kaoru "Effective immediately. No waiting period. I have run out of business days I am willing to make you wait."
    menu au_modern_epilogue_waiting_menu:

        "Accept the filing. *Effective immediately.*":
            $ au_modern_epilogue_waiting = "immediate"
            voice "audio/voice/toa_446.mp3"
            toa "Then I accept the filing as written. Effective immediately, no waiting period. For the record, I have wanted it effective immediately since the wrong conference room. I just never filed it."
            voice "audio/voice/kaoru_577.mp3"
            kaoru "Noted. Entered. The record agrees with you, which it rarely does and never out loud."
            jump au_modern_epilogue_smile

        "Demand the old three-business-day waiting period back (joke).":
            $ au_modern_epilogue_waiting = "three_days"
            voice "audio/voice/toa_447.mp3"
            toa "Objection, Deputy Director-sama. For three cases you told me everything you intended to keep was effective in three business days. I want my waiting period back. I have grown attached to the suspense."
            $ show_cg_scene("au_modern_epilogue_three_days_joke", fade)
            pause 2.0

            voice "audio/voice/kaoru_578.mp3"
            kaoru "Overruled. The waiting period was always for the building, not for you. I am done making you wait for the benefit of an audience that muted its own microphone."
            jump au_modern_epilogue_smile


label au_modern_epilogue_smile:

    voice "audio/voice/narrator_450.mp3"
    "That was when it happened, the thing he had denied for three cases, the motion he had ruled against every time she filed it. The corner of his mouth went, and kept going, and did not stop at almost. It landed."
    $ show_cg_scene("au_modern_epilogue_smile", fade)
    pause 2.0

    voice "audio/voice/narrator_451.mp3"
    "A whole one, small and grey-eyed and without precedent in any file she had ever read. She did not breathe."
    voice "audio/voice/toa_448.mp3"
    toa "You smiled. I have witnesses. The witness is me. I am extremely reliable. It has been classified."
    voice "audio/voice/kaoru_579.mp3"
    kaoru "Noted."
    voice "audio/voice/narrator_452.mp3"
    "He did not file it away. He did not say *motion denied*. He let it sit on his face where the building could have seen it if the building had cared to look."
    voice "audio/voice/kaoru_580.mp3"
    kaoru "Motion granted, To-chan. On the record."
    if au_modern_epilogue_waiting == "three_days":
        voice "audio/voice/toa_449.mp3"
        toa "Granted with no waiting period, after I argued for the suspense. I withdraw my objection. Slowly. Under protest. For the record."
        voice "audio/voice/kaoru_581.mp3"
        kaoru "Your protest is noted and overruled. I am keeping the smile and closing the clause."
    else:
        voice "audio/voice/toa_450.mp3"
        toa "Granted and effective immediately. I accepted the filing and the filing accepted me back. That is not how paperwork usually works."
        voice "audio/voice/kaoru_582.mp3"
        kaoru "It is how this one works. I wrote it that way."
    jump au_modern_epilogue_harbor


label au_modern_epilogue_harbor:

    play music audio.bgm_canon_intimate fadein 2.0 loop volume 0.28

    $ show_cg_scene("au_modern_epilogue_harbor", fade)
    pause 1.0

    voice "audio/voice/narrator_453.mp3"
    "They keep the harbor Airbnb now. Not as a clerical error. A line item with both their names on the booking and a lockbox that has finally learned the two of them. Rain comes back the way it always comes back to Ryoko Port, quietly and in quantity, and files itself against the cedar-framed glass."
    voice "audio/voice/toa_451.mp3"
    toa "You restock the clementines. You have always restocked the clementines. You denied it for a year."
    voice "audio/voice/kaoru_583.mp3"
    kaoru "Domestic filing."
    $ show_cg_scene("au_modern_epilogue_harbor_piano", dissolve)
    pause 1.0

    voice "audio/voice/toa_521.mp3"
    toa "You still play sometimes. When you think the building has stopped listening."
    voice "audio/voice/toa_522.mp3"
    toa "The same out-of-tune municipal piano,"
    voice "audio/voice/toa_523.mp3"
    toa "moved to the harbor place on a work order nobody questioned."
    voice "audio/voice/toa_524.mp3"
    toa "You filed the piano under *equipment,"
    voice "audio/voice/toa_525.mp3"
    toa "surplus.* I filed it under the afternoon you stopped counting and started listening,"
    voice "audio/voice/toa_526.mp3"
    toa "which is the afternoon you decided to keep me."
    voice "audio/voice/toa_527.mp3"
    toa "We have very different filing systems for the same instrument."

    voice "audio/voice/narrator_454.mp3"
    "Which was not a denial, which from him was a confession with the serial numbers left on. The blanket on the harbor sofa is no longer a loan against her noise. It is hers, or theirs, the distinction having quietly collapsed."
    voice "audio/voice/narrator_455.mp3"
    "She sits in witness posture out of habit, hands folded, spine honest. He notices, because he notices everything."
    voice "audio/voice/kaoru_584.mp3"
    kaoru "You can sit however you want. You are not a witness here. You are the filing."
    menu au_modern_epilogue_posture_menu:

        "Keep witness posture (old habit, still paying attention).":
            $ au_modern_epilogue_posture = "witness"
            voice "audio/voice/toa_452.mp3"
            toa "I like the posture. It is how I sit when I am paying attention. I am paying attention, Deputy Director-sama."
            $ show_cg_scene("au_modern_epilogue_witness_posture", dissolve)
            pause 2.0

            voice "audio/voice/kaoru_585.mp3"
            kaoru "Then pay attention to this part. It is the part I did not put on any portal."
        "Uncurl. Sit however she wants (no apology).":
            $ au_modern_epilogue_posture = "uncurled"
            voice "audio/voice/toa_453.mp3"
            toa "Then I will sit like a woman who stopped reading the plate to confirm she is allowed in the room."
            voice "audio/voice/narrator_456.mp3"
            "She uncurls, slow, into something with no apology in it at all. He watches her do it the way he watches a tide decide whether to take the lower dock."
            $ show_cg_scene("au_modern_epilogue_uncurl", fade)
            pause 2.0

    jump au_modern_epilogue_audit_choice


label au_modern_epilogue_audit_choice:

    voice "audio/voice/narrator_457.mp3"
    "He takes the clementine peel out of her fingers and sets it on the armrest, bright and forgotten, the way it had been forgotten on a narrower couch in a glass building once."
    $ show_cg_scene("au_modern_epilogue_clementine_peel", dissolve)
    pause 2.0

    $ show_cg_scene("au_modern_epilogue_harbor_kiss", fade)
    pause 2.0

    voice "audio/voice/kaoru_586.mp3"
    kaoru "Acceptable noise is still noise. The harbor has ears. The neighbors have a lease. We decide how loud the audit gets tonight, and you decide first."
    if au_modern_case2_night_audit:
        voice "audio/voice/toa_454.mp3"
        toa "We audited the rider once before, on the island, after hours. My neck still remembers the count. I came back for the rest of it."
    else:
        voice "audio/voice/toa_455.mp3"
        toa "We kept the island procedural. I have wondered, on every ferry since, what the unprocedural version files like."
    voice "audio/voice/kaoru_587.mp3"
    kaoru "Then choose, on the record. A quiet audit after dark, on your word, or we close the file here, warm and dressed, and let the rain keep its own minutes."
    menu au_modern_epilogue_audit_menu:

        "Audit the rider after hours (quiet, tasteful, consenting).":
            $ au_modern_epilogue_audit = True
            voice "audio/voice/toa_456.mp3"
            toa "Audit it. Quietly. On my word, in dates and names only. You taught me the difference."
            jump au_modern_epilogue_audit_beat

        "Close the file warm and dressed (fade to domestic).":
            $ au_modern_epilogue_audit = False
            voice "audio/voice/toa_457.mp3"
            toa "Close it here. Warm. Dressed. Your arm, the blanket, the rain. That is the whole filing tonight."
            jump au_modern_epilogue_domestic


label au_modern_epilogue_audit_beat:

    voice "audio/voice/narrator_458.mp3"
    "He draws the zip of her tracksuit down, slow, the way he does everything he intends to keep, knuckles tracing the bare line of her sternum where the gold crane sits warm over her heart."
    $ show_cg_scene("au_modern_epilogue_audit_intimate", fade)
    pause 2.0

    voice "audio/voice/kaoru_588.mp3"
    kaoru "Deliverable one. You beg the only way I allow after dark. Dates and names. Nothing performed for an audience."
    $ show_cg_scene("au_modern_epilogue_audit_count", dissolve)
    pause 2.0

    voice "audio/voice/toa_458.mp3"
    toa "Friday. Harbor. Kaoru. Please."
    voice "audio/voice/narrator_459.mp3"
    "He counts under his breath, one, two, three, matching stroke to count, unhurried, refusing her the performance of shame and refusing, also, to stop, until her heel presses a careful bruise into his shoulder and the rain loses track of itself against the glass. The screen fades on the rest of their coupling."
    $ show_cg_scene("au_modern_epilogue_afterglow", fade)
    pause 2.0

    voice "audio/voice/kaoru_589.mp3"
    kaoru "You do not perform gratitude on the furniture. You never did. You file it in the break room. I have the precedent in my own hand."
    voice "audio/voice/toa_459.mp3"
    toa "Already filed, Deputy Director-sama. The standing Friday, made flesh. Effective immediately."
    voice "audio/voice/narrator_460.mp3"
    "After, he steadies her with his palm at her hip, the same bracket from a service elevator and a western inn and a couch the city used to own. They lie spent under the blanket while harbor light slides across the ceiling. The standing Friday audit, he does not say aloud, has begun."
    $ show_cg_scene("au_modern_epilogue_curve_pull", dissolve)
    pause 2.0

    jump au_modern_epilogue_closure


label au_modern_epilogue_domestic:

    voice "audio/voice/narrator_461.mp3"
    "He pulls the blanket up over them both in the same patient order he does everything, and she fits herself into the curve of him while the rain keeps its own minutes on the glass. No audit tonight. Just the bracket of his arm, the one from a service elevator and a western inn and a couch the city used to own."
    $ show_cg_scene("au_modern_epilogue_domestic", fade)
    pause 2.0

    voice "audio/voice/kaoru_590.mp3"
    kaoru "Acceptable noise is still noise. Tonight the acceptable noise is the rain and you breathing under my arm. The file can stay open until morning."
    voice "audio/voice/toa_460.mp3"
    toa "I can survive an open file. I have survived worse paperwork. This is the first one I do not want closed."
    jump au_modern_epilogue_closure


label au_modern_epilogue_closure:

    $ show_cg_scene("au_modern_epilogue_standing_item", dissolve)
    pause 1.0

    voice "audio/voice/toa_461.mp3"
    toa "Three business days used to be how long I had to wait for everything you intended to keep."
    voice "audio/voice/kaoru_591.mp3"
    kaoru "You do not wait anymore. That clause is closed. You are not a deliverable with an effective date. You are a standing item."
    voice "audio/voice/toa_473.mp3"
    toa "A standing item. The Council files those the way it files rent and rain, the recurring things it expects to keep paying attention to. I have been a great many classifications in this building. That is the first one I would frame."
    if au_modern_epilogue_waiting == "three_days":
        voice "audio/voice/narrator_462.mp3"
        "She had argued for the waiting period out of habit and lost on purpose. The suspense had only ever been the building's. He had stopped scheduling her like a deliverable somewhere around the harbor, and she had let him."
    else:
        voice "audio/voice/narrator_463.mp3"
        "She had accepted effective immediately the way she accepted most true things, late out loud and early in private. He had stopped scheduling her like a deliverable somewhere around the harbor, and she had let him."
    $ show_cg_scene("au_modern_epilogue_blank_row", fade)
    pause 2.0

    voice "audio/voice/narrator_464.mp3"
    "On the calendar back at the tower he has left exactly one row blank, the way he used to leave one blank on purpose. A man should keep one row for the thing he has not scheduled yet. The next case. The next door. The next *unless*. He has stopped leaving the rest of them blank."
    if au_modern_epilogue_posture == "witness":
        voice "audio/voice/toa_462.mp3"
        toa "I still sit in witness posture sometimes. Old habit. It is how I sit when I am paying attention, and I am still paying attention. I read the plate before I open the door. I have for a long time now."
    else:
        voice "audio/voice/toa_463.mp3"
        toa "I stopped sitting in witness posture. I sit like the filing now. I still read the plate before I open the door, out of love instead of procedure. I have for a long time now."
    voice "audio/voice/narrator_465.mp3"
    "She had been reading the plate before she opened the door for a long time now, and she no longer pretended she had wandered in by mistake. She had not. Not once since the first."
    voice "audio/voice/toa_464.mp3"
    toa "I file that under *kept*. In a place no portal can index. And I let the harbor keep its own minutes against the glass."
    voice "audio/voice/narrator_466.mp3"
    "Disclosed. Oversight accepted. Effective immediately."
    jump au_modern_epilogue_end_stinger


label au_modern_epilogue_end_stinger:

    scene black with fade
    stop music fadeout 2.5

    if au_modern_epilogue_audit:
        centered "{size=+2}Effective Immediately (Modern AU Epilogue){/size}\n{size=-4}Motion granted. Audited quietly. On the record.{/size}"
    else:
        centered "{size=+2}Effective Immediately (Modern AU Epilogue){/size}\n{size=-4}Motion granted. Filed warm. On the record.{/size}"

    pause 2.0

    scene black with fade
    centered "{size=-3}One calendar row left blank, for the next {i}unless{/i}.\nThe rain keeps its own minutes against the glass.{/size}"

    pause 2.5

    jump au_modern_epilogue_end


label au_modern_epilogue_end:

    menu au_modern_epilogue_continue_menu:

        "Sit with the ending a moment.":
            scene black with fade
            centered "{size=+2}End of the Modern AU trilogy.{/size}\n{size=-4}Wrong Floor · Compliance · Island Weekend · Permits & HR · Effective Immediately.{/size}"
            pause 3.0

        "Return to menu.":
            pass

    if dev_chapter_pick_enabled:
        jump dev_chapter_pick_menu

    ## Back to the Modern AU hub (rollback-enabled game context). The hub clears
    ## au_episode_active and restores the menu theme.
    jump au_modern_hub_menu
