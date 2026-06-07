# Modern AU Case 2: "Is this a date?" Island Weekend (dev bonus sequel).
#
# Play: Main menu → "AU Case 2: Island Weekend"; dev pick → "AU Case 2: Island Weekend";
#   or Case 1 end → "Continue to island weekend?"
# VOICED: narrator_400+, toa_397+, kaoru_531+ (wire: scripts/wire_au_modern_case2_voice.py).
# Does not set canon case/permit flags.

default seen_au_modern_case2 = False
default au_modern_case2_weekend_mode = ""
default au_modern_case2_night_audit = False

label au_modern_case2_start:

    ## Launched in the rollback-enabled game (root) context, from the Modern AU hub
    ## (au_modern_hub_menu) or the dev chapter pick. Because this is the normal game
    ## context (not a call_in_new_context child of the menu), Back/rollback, mid-episode
    ## saving, character + narrator voices, and the quick/game menu all work without any
    ## menu-state fix-ups. Mark the AU episode active so the story-music mute callback
    ## keeps story BGM audible (incl. after loading a mid-episode save).
    $ au_episode_active = True
    $ enable_cinematic_music()

    $ seen_au_modern_case2 = True
    $ au_modern_case2_weekend_mode = ""
    $ au_modern_case2_night_audit = False

    scene black with fade
    play music audio.bgm_street fadein 2.5 loop volume 0.34

    centered "{font=fonts/YujiSyuku-Regular.ttf}{size=+6}Is This a Date?{/size}{/font}\n{size=-4}Modern AU · Case 2 · Island Weekend{/size}"

    pause 1.0

    voice "audio/voice/narrator_400.mp3"
    "Saturday, and the harbor ferry schedule is a suggestion. Rain owns the channel. Kakita Toa owns a duffel bag and a Council sponsorship rider that still reads *not romance on letterhead*, the same exclusive rider that put her on the deputy's calendar in the first place."

    voice "audio/voice/narrator_401.mp3"
    "Deputy Director Kitsu Kaoru owns the calendar invite, the Airbnb confirmation, and the expression of a man who has already filed the weather as exhibit A."

    voice "audio/voice/narrator_477.mp3"
    "This is the harbor audit retreat he slid across her municipal portal at the end of the wellness inspection. Ferry slips, one bed filed as clerical error, the whole weekend logged on the Office of Arts and Licensing calendar as continued witness work under her clause. She accepted it on the Council form, in the dry font the portal assigns to everything. The form had no box for what she actually wanted, so she filed that part nowhere, which is its own kind of filing."

    voice "audio/voice/toa_397.mp3"
    toa "If the ferry is late, do we still owe the island a witness log?"

    voice "audio/voice/kaoru_531.mp3"
    kaoru "You owe the island punctuality. The ferry owes us a revised ETA. Those are different dockets."

    jump au_modern_case2_ferry_delay


label au_modern_case2_ferry_delay:

    $ show_cg_scene("au_modern_case2_ferry_rain", fade)
    pause 2.0

    voice "audio/voice/narrator_402.mp3"
    "The terminal roof drips into puddles that reflect diesel and regret. Commuters complain in the polite register of people who will not get refunds."

    voice "audio/voice/toa_398.mp3"
    toa "Two hours late. My tracksuit is waterproof. My patience is municipal."

    voice "audio/voice/kaoru_532.mp3"
    kaoru "Patience is a line item. Stand where I can see you and the manifest."

    $ show_cg_scene("au_modern_case2_pier_arrival", fade)
    pause 2.0

    voice "audio/voice/narrator_403.mp3"
    "When the ferry finally coughs to the pier, salt air replaces toner. Toa stops apologizing in her shoulders without being told."

    jump au_modern_case2_airbnb_arrival


label au_modern_case2_airbnb_arrival:

    scene black with dissolve
    pause 0.4

    $ show_cg_scene("au_modern_case2_airbnb_exterior", fade)
    pause 2.0

    voice "audio/voice/narrator_404.mp3"
    "The harbor Airbnb is cedar shingles, one parking space, and a lockbox that thinks it is a deputy director."

    voice "audio/voice/toa_399.mp3"
    toa "Cute. Very *audit retreat*. Does the listing mention ghosts or only damp towels?"

    voice "audio/voice/kaoru_533.mp3"
    kaoru "It mentions one queen bed, one sofa, and a clerical error I will not fix unless you ask in writing."

    voice "audio/voice/narrator_405.mp3"
    "Inside, the rental agreement on the tablet glows like a confession booth with Wi-Fi."

    $ show_cg_scene("au_modern_case2_one_bed", fade)
    pause 2.0

    voice "audio/voice/toa_400.mp3"
    toa "One bed. One deputy. That is either a rom-com or a labor violation."

    voice "audio/voice/kaoru_534.mp3"
    kaoru "It is a filing. You sleep. I review calendar conflicts. We do not perform couple on the listing photos."

    voice "audio/voice/narrator_406.mp3"
    "The sofa is narrow. The bed is worse, because it is comfortable and therefore suspicious."

    voice "audio/voice/toa_401.mp3"
    toa "I call the sofa. You call the bed. That is professional roommate energy, right?"

    jump au_modern_case2_friend_texts


label au_modern_case2_friend_texts:

    voice "audio/voice/narrator_407.mp3"
    "Her phone lights up before she can argue with the furniture."

    $ show_cg_scene("au_modern_case2_phone_text", fade)
    pause 2.0

    voice "audio/voice/toa_402.mp3"
    toa "Sango texts: *ferry delay omg*. Then: *one bed airbnb*. Then: *girl is this a date???*"

    voice "audio/voice/toa_403.mp3"
    toa "I should tell her it is a harbor audit with a man who counts witness work out loud."

    voice "audio/voice/narrator_408.mp3"
    "Kaoru does not look at her screen. He looks at her face, which is doing something between laughter and panic."

    voice "audio/voice/kaoru_535.mp3"
    kaoru "If you answer *yes*, I will add a footnote: *applicant confuses calendar with courtship*. If you answer *no*, tell the truth in dates and names only."

    voice "audio/voice/toa_404.mp3"
    toa "I text: *not a date. contract says not romance on letterhead. send snacks.*"

    toa "She sends back *sure, Jan.* And she is not wrong. The contract says not romance on letterhead, and the contract is the most romantic thing anyone has ever written about me. That is the whole joke. We file it as procedure so we never have to call it the thing it plainly is."

    voice "audio/voice/kaoru_536.mp3"
    kaoru "Good. Now choose how we file the weekend before the island files us."

    menu au_modern_case2_weekend_menu:

        "Professional roommate (sofa, boundaries, audit on paper).":
            $ au_modern_case2_weekend_mode = "roommate"
            voice "audio/voice/toa_405.mp3"
            toa "Roommate mode. Separate sleep surfaces. You keep your blazer on like a seatbelt."

            voice "audio/voice/kaoru_537.mp3"
            kaoru "Acceptable. I will deny almost-smile inventory until Monday."

            jump au_modern_case2_roommate_night

        "Test the exclusive rider (proximity, clause stress-test).":
            $ au_modern_case2_weekend_mode = "rider"
            voice "audio/voice/toa_406.mp3"
            toa "We stress-test the exclusive rider. Not dating. Just... deliverable review with salt air."

            voice "audio/voice/kaoru_538.mp3"
            kaoru "You understand that clause is calendar and audit, not romance on letterhead."

            jump au_modern_case2_rider_menu


label au_modern_case2_roommate_night:

    voice "audio/voice/narrator_409.mp3"
    "She claims the sofa with a blanket fort of municipal dignity. He takes the bed and the laptop, queue numbers reflected in the rain window."

    $ show_cg_scene("au_modern_case2_roommate_night", fade)
    pause 2.0

    voice "audio/voice/kaoru_539.mp3"
    kaoru "Lights out at eleven. Snore above acceptable noise and I reassign you to the ferry bench."

    voice "audio/voice/toa_407.mp3"
    toa "Then I'll file my breathing under *compliant*. Good night, Deputy Director-sama."

    voice "audio/voice/narrator_410.mp3"
    "At midnight she hears him typing. At one she hears the rain stop pretending to be subtle. At two she does not cross the room. That is also witness work."

    voice "audio/voice/toa_470.mp3"
    toa "Witness posture, even here. I document the want and I do not perform it where a listing photo could see. My clause never asked me not to want him. It only forbade me to put it on letterhead."

    jump au_modern_case2_balcony_audit


label au_modern_case2_rider_menu:

    voice "audio/voice/narrator_411.mp3"
    "The bed is one surface. The contract is another. Toa stands in the doorway like a woman who has read the rider twice and still wants a third opinion."

    $ show_cg_scene("au_modern_case2_rider_doorway", fade)
    pause 2.0

    menu au_modern_case2_rider_night_menu:

        "Keep tonight procedural (balcony debrief only).":
            voice "audio/voice/toa_408.mp3"
            toa "Procedural night. Balcony debrief. No deliverables behind closed doors."

            voice "audio/voice/kaoru_540.mp3"
            kaoru "Motion granted. Bring your tablet. Leave performance posture in the closet."

            jump au_modern_case2_balcony_audit

        "Audit the exclusive rider after hours (tasteful, western inn).":
            $ au_modern_case2_night_audit = True
            voice "audio/voice/toa_409.mp3"
            toa "After-hours audit. Quiet. Western inn. Not romance on letterhead."

            voice "audio/voice/kaoru_541.mp3"
            kaoru "Then audit quietly. The harbor still has ears."

            jump au_modern_case2_rider_intimate


label au_modern_case2_rider_intimate:

    voice "audio/voice/narrator_412.mp3"
    "Rain writes shorthand on the window. His blazer folds over the chair like a man who has filed himself for the night. Her tracksuit jacket follows."

    $ show_cg_scene("au_modern_case2_intimate_audit", fade)
    pause 2.0

    voice "audio/voice/kaoru_542.mp3"
    kaoru "Deliverable one. You hold still when I count."

    voice "audio/voice/toa_410.mp3"
    toa "I can hold still. Count."

    $ show_cg_scene("au_modern_case2_audit_deep", dissolve)
    pause 2.0

    voice "audio/voice/narrator_413.mp3"
    "He audits heat the way he audits queue numbers: thorough, unhurried, denying her the performance of shame."

    voice "audio/voice/kaoru_543.mp3"
    kaoru "Deliverable two. You do not perform gratitude on rental linens."

    voice "audio/voice/toa_411.mp3"
    toa "I file gratitude in the break room. You said so."

    voice "audio/voice/narrator_414.mp3"
    "When she trembles, he steadies her with his palm at her hip and says acceptable noise is still noise."

    $ show_cg_scene("au_modern_case2_audit_afterglow", fade)
    pause 2.0

    voice "audio/voice/kaoru_544.mp3"
    kaoru "File it under exclusive rider. Monday calendar owns the rest."

    voice "audio/voice/toa_412.mp3"
    toa "Already filed. Deputy Director-sama."

    jump au_modern_case2_balcony_audit


label au_modern_case2_balcony_audit:

    scene black with fade
    pause 0.5

    $ show_cg_scene("au_modern_case2_balcony_night", fade)
    pause 2.0

    voice "audio/voice/narrator_415.mp3"
    "Sunday night finds them on the balcony, the weekend almost filed, harbor lights smeared across the rail and a tablet open to the municipal portal where Tuesday is already waiting."

    voice "audio/voice/kaoru_545.mp3"
    kaoru "Calendar audit. Ferry back at six. HR block on Tuesday. Answer in dates, not poetry."

    voice "audio/voice/toa_413.mp3"
    toa "Tuesday HR. That sounds like the viral Zoom clip finally grew teeth."

    $ show_cg_scene("au_modern_case2_balcony_handclasp", dissolve)
    pause 2.0

    voice "audio/voice/kaoru_546.mp3"
    kaoru "It sounds like signatory pressure. You are listed dependent on the sponsorship I signed. I am the signatory of record. If that clip convinces the Council I favor you, People and Conduct opens a conflict-of-interest file, and the apparatus decides what to do with the pair of us. None of that is romance on letterhead."

    voice "audio/voice/toa_471.mp3"
    toa "Dependent. Signatory. Two boxes on one form, and a camera that turned them into a couple. I did not understand that my right to dance in this port was also your liability until you said it out loud on a balcony."

    toa "I keep thinking about the studio. The afternoon you put down the clipboard and played the piano so I could take class. You stopped counting and started listening, and you have been a different kind of careful with me ever since. That is also not on any letterhead. I checked the file twice."

    kaoru "The piano is not in the record. Neither is the reason I sat down at it. Some deliverables I keep in the drawer with no label, where the board cannot ask me to explain them. You are filed in that drawer. So is the afternoon."

    if au_modern_case2_weekend_mode == "roommate":
        voice "audio/voice/narrator_416.mp3"
        "She stayed on the sofa. He stayed on the bed. The weekend still felt like proximity wearing a tie."

        voice "audio/voice/toa_414.mp3"
        toa "Roommate mode survived. Barely. Sango will not believe me."

    elif au_modern_case2_night_audit:
        voice "audio/voice/narrator_417.mp3"
        "Her neck still remembers counting. His voice stays level, as if the island did not hear what the room heard."

        voice "audio/voice/toa_415.mp3"
        toa "Exclusive rider survived cross-examination. My face did not."

    else:
        voice "audio/voice/narrator_418.mp3"
        "They filed the weekend as debrief and salt air. Almost-touch inventory: noted, denied, noted again."

        voice "audio/voice/toa_416.mp3"
        toa "Procedural night. I can survive procedural."

    voice "audio/voice/kaoru_547.mp3"
    kaoru "Pack at five. If you post *is this a date* with my badge in frame, I will revoke your witness clause."

    voice "audio/voice/narrator_419.mp3"
    "The ferry horn answers like a stamp. Case two closes on salt air and a rider that held. Case three is already forming on the far shore, where a viral clip and an HR inbox will decide whether a deputy's signature counts as a favor."

    jump au_modern_case2_end_stinger


label au_modern_case2_end_stinger:

    scene black with fade
    stop music fadeout 2.0

    centered "{size=+2}Island Weekend (Modern AU Case 2){/size}\n{size=-4}Not a date on letterhead. HR Tuesday pending.{/size}"

    pause 1.0

    jump au_modern_case2_end


label au_modern_case2_end:

    menu au_modern_case2_continue_menu:

        "Continue to Case 3: Permits and HR?":
            jump au_modern_case3_start

        "Return to menu.":
            pass

    if dev_chapter_pick_enabled:
        jump dev_chapter_pick_menu

    ## Back to the Modern AU hub (rollback-enabled game context). The hub clears
    ## au_episode_active and restores the menu theme.
    jump au_modern_hub_menu
