# Case 5 Path A: The Left Hand (御前の帳 / Seal at the Hearing).
# Entry: case4_post_case4_bridge / case4_5_boat_bridge → case5_investigation_start.
# Eligibility: all_romance_routes_complete(); else case5_noncanon_discharge.
# Path A only. Refuse → case5_bad_end_refusal_warning.
# VOICED: kaoru_335+, toa_281+, narrator_272+ (wired lines have legacy MP3s).
# CG beats: voice on master, bust via set_expression only; no scene bg + full show until leaving the beat.


label case5_investigation_start:

    if case5_closed:
        return

    if not all_romance_routes_complete():
        jump case5_noncanon_discharge

    $ case5_started = True

    scene bg magistrate_office with dissolve
    play music audio.bgm_case5_tease fadein 1.5 loop volume 0.45
    show kaoru commanding at left
    show toa determined at right

    voice "audio/voice/narrator_272.mp3"
    "Three mornings after the dock finally goes quiet, the runner skips breakfast. He brings a summons instead, ink still wet, pleasure-quarter seal copied twice like the clerk was afraid someone would call it a forgery."

    show toa worried
    voice "audio/voice/toa_281.mp3"
    toa "Magistrate-sama, the runner would not meet my eyes. Does that mean the witness line is finished?"

    show kaoru cold
    voice "audio/voice/kaoru_335.mp3"
    kaoru "Witness is a word for paper that has not earned ink yet. Case Five opens at the hour of the serpent. Dress for court, not for my corridor."

    show toa flustered
    voice "audio/voice/toa_282.mp3"
    toa "Court sounds like dismissal. Or punishment. You said when the files closed we would talk about terms."

    show kaoru smirk
    voice "audio/voice/kaoru_336.mp3"
    kaoru "We are talking about them. In a room that can hear you."

    jump case5_false_exit


label case5_false_exit:

    $ case5_false_exit_seen = True

    $ show_cg_scene("case5_false_exit_office", fade)
    pause 2.0

    voice "audio/voice/narrator_273.mp3"
    "She packs Crane neatness into a travel kosode, the kind you wear when patronage runs out and the gate guard asks for papers you no longer have."

    $ set_expression("kaoru", "cold")
    voice "audio/voice/kaoru_337.mp3"
    kaoru "Leave the adjoining chamber key at the gate. Today you are witness. The hall does not care what you called last night."

    $ set_expression("toa", "determined")
    voice "audio/voice/toa_283.mp3"
    toa "Then I will attend as your witness one last time. The hall taught me how to stand where I am told."

    $ set_expression("kaoru", "charm")
    voice "audio/voice/kaoru_338.mp3"
    kaoru "Good. That pleasure-quarter seal on the summons is bait for clerks who think Case Five is only Chrysanthemum politics. It is not. Stay in my line."

    pause 2.0
    scene black with fade
    pause 0.5

    jump case5_audition_callback


label case5_audition_callback:

    scene bg magistrate_office with dissolve
    play music audio.bgm_office fadein 2.0 loop volume 0.42
    show kaoru commanding at center
    show toa determined at left

    voice "audio/voice/kaoru_339.mp3"
    kaoru "Case One, you read a lie under pressure at the Lacquered Plum and you did not run when the comb turned out to be Scorpion."

    voice "audio/voice/kaoru_340.mp3"
    kaoru "Case Two, you stood on the hill where the city could see you beside my file, and you did not hide behind Crane honor when kiln ash choked the alley."

    voice "audio/voice/kaoru_341.mp3"
    kaoru "Case Three, you trusted the bolt room when the room tried to kill you. You let me pull you out instead of proving the Academy right on splinters."

    if case4_kaoru_defended:
        voice "audio/voice/kaoru_342.mp3"
        kaoru "Case Four, you stayed behind my shoulder when steel wanted you alone. You did not compose poetry on my dock."

    show toa soft
    voice "audio/voice/toa_284.mp3"
    toa "You never told me any of that was a test."

    show kaoru smirk
    voice "audio/voice/kaoru_343.mp3"
    kaoru "I said provisional attachment until the files close. They were real cases, and they did not close themselves, To-chan. I was not testing you. I was watching what each one revealed."

    show toa flustered
    voice "audio/voice/toa_285.mp3"
    toa "I thought you meant stipend. A permit. A room next to yours."

    show kaoru charm
    voice "audio/voice/kaoru_344.mp3"
    kaoru "I meant a left hand. The city needs a name on it. I could not offer it behind my screen, or the quarter would call it a kept woman's wages. You had to be seen choosing the desk over the road. Forgive the cold morning. I chose your name before you knew what the job was called."

    scene black with fade
    pause 0.4

    jump case5_public_hearing


label case5_public_hearing:

    $ case5_hearing_attended = True

    $ show_cg_scene("case5_hearing_hall", fade)
    pause 2.0
    play music audio.bgm_case5_hearing fadein 2.0 loop volume 0.48

    voice "audio/voice/narrator_274.mp3"
    "Ryoko Owari's open docket hall smells of wet stone and copied petitions. Quarter clerks line the left wall. A Crane envoy's crest sits cold on the right. Someone in the back row wears another magistrate's colors but never takes the seat."

    $ set_expression("kaoru", "cold")
    voice "audio/voice/kaoru_345.mp3"
    kaoru "Kitsu Kaoru, Emerald Magistrate. Case Five: witness chains for the Chrysanthemum root, and appointment of sworn yoriki for the ongoing docket."

    $ set_expression("toa", "worried")
    voice "audio/voice/toa_286.mp3"
    toa "Yoriki is a sworn magistrate's rank. That is not the same as a dancer's permit."

    $ show_cg_scene("case5_hearing_kaoru_dais", fade)
    pause 2.0

    $ set_expression("kaoru", "commanding")
    voice "audio/voice/kaoru_346.mp3"
    kaoru "Witness is not enough in this city. You signed my corridor, my cushion, my release. Let the quarter whisper kept woman. The file will say office."

    voice "audio/voice/narrator_275.mp3"
    "The Crane envoy does not stand. His silence reads like a letter home to the Crane courts."

    $ set_expression("toa", "thinking")
    voice "audio/voice/toa_438.mp3"
    toa "Magistrate-sama, the colors in the back row. He has not taken a seat, because to sit is to be entered in the record. Sixteen petals locked Jiro's room, cut by a hand that knew the Emerald office from the inside. A magistrate has been keeping the Chrysanthemum's wax warm this whole season."

    $ set_expression("kaoru", "cold")
    voice "audio/voice/kaoru_569.mp3"
    kaoru "Say his name aloud and you accuse a peer of the bench with a dead clerk and a petal-count. The Crane envoy writes that home, and this city eats the witness long before it eats the magistrate."

    $ set_expression("toa", "determined")
    voice "audio/voice/toa_439.mp3"
    toa "So the root keeps growing, because the one hand that could cut it sits where no one dares write his name. That is your whole season, Magistrate. Five files, none of them ever truly closed."

    $ set_expression("kaoru", "commanding")
    voice "audio/voice/kaoru_570.mp3"
    kaoru "Now you understand the work. We do not close the big file. We keep it open on purpose, one witness chain at a time, until the day the record can hold his name without burning the clerk who wrote it. That is what a left hand is for."

    pause 2.0
    jump case5_scroll_presentation


label case5_scroll_presentation:

    $ case5_yoriki_offered = True

    $ show_cg_scene("case5_scroll_desk", fade)
    pause 2.0

    play sound audio.paper_shuffle volume 0.5
    $ set_expression("kaoru", "commanding")
    voice "audio/voice/kaoru_347.mp3"
    kaoru "Kakita Toa. Appointment as yoriki to the Emerald office of Ryoko Owari. Witness chains, quarter escort, left-hand signature on my docket."

    $ set_expression("toa", "determined")
    voice "audio/voice/toa_287.mp3"
    toa "Magistrate-sama, Crane custom expects an honor guard and clan auditors at my side. Not a magistrate's toy left on a public desk."

    $ set_expression("kaoru", "smirk")
    voice "audio/voice/kaoru_348.mp3"
    kaoru "You have already served this desk. You slept behind my screen. You argued well every time I needed a sharp mind within reach."

    $ set_expression("kaoru", "charm")
    voice "audio/voice/kaoru_349.mp3"
    kaoru "This is office. I am not asking for poetry. I need a name the city can cite when the seal walks."

    pause 2.0
    menu case5_yoriki_menu:
        "Accept the oath, left hand on the scroll.":
            $ case5_yoriki_accepted = True
            jump case5_yoriki_accept

        "Refuse, I am a Crane dancer, not your property.":
            $ case5_yoriki_refused = True
            jump case5_refusal_estrangement


label case5_yoriki_accept:

    $ show_cg_scene("case5_yoriki_oath", fade)
    pause 2.0

    play sound audio.hanko_stamp volume 0.6
    $ set_expression("toa", "soft")
    voice "audio/voice/toa_288.mp3"
    toa "I accept the appointment and its duties. You will have my discretion and my attendance."

    $ set_expression("kaoru", "charm")
    voice "audio/voice/kaoru_350.mp3"
    kaoru "You passed every case I put in front of you. Do not make me say it twice in front of clerks who sell courage by the cup."

    $ set_expression("toa", "flustered")
    voice "audio/voice/toa_289.mp3"
    toa "I will not embarrass your file."

    voice "audio/voice/narrator_276.mp3"
    "The envoy exhales once, not a blessing, only a tally of who gains. The rival magistrate's colors leave before the wax cools."

    pause 2.0
    menu case5_post_oath_menu:
        "Sign and follow him to the inner office tonight.":
            jump case5_private_extra

        "Sign and return to the witness chamber, boundaries until he sends for you.":
            jump case5_epilogue_week_one


label case5_private_extra:

    $ case5_private_confession = True

    $ show_cg_scene("case5_oath_seal_hand", fade)
    pause 2.0

    voice "audio/voice/narrator_310.mp3"
    "His hand covers the yoriki seal on the inner desk, brown fingers, red wax still warm, as if the oath were a body he could keep off the public tray."

    $ show_cg_scene("case5_private_talk", fade)
    pause 2.0
    play music audio.bgm_office fadein 2.0 loop volume 0.38

    voice "audio/voice/narrator_277.mp3"
    "The inner office after public ink feels smaller than the hearing hall. He locks the corridor himself. No runner, no cushion joke, only cedar and the heat of wax that will not cool before he touches her again."

    $ set_expression("kaoru", "commanding")
    voice "audio/voice/kaoru_351.mp3"
    kaoru "Speak without the docket listening. One sentence you never filed, and one debt you still owe my desk."

    $ set_expression("toa", "worried")
    voice "audio/voice/toa_290.mp3"
    toa "I needed the permit to stay close, but I chose to stay on purpose. I could have run. Then you could have caught me."

    $ set_expression("kaoru", "smirk")
    voice "audio/voice/kaoru_352.mp3"
    kaoru "I know."

    $ set_expression("toa", "determined")
    voice "audio/voice/toa_291.mp3"
    toa "You are not easy."

    $ set_expression("kaoru", "charm")
    voice "audio/voice/kaoru_353.mp3"
    kaoru "Most people try to rename me. You let me keep you, and still walked back to my corridor on your own feet."

    $ set_expression("toa", "flustered")
    voice "audio/voice/toa_292.mp3"
    toa "Behind your screen I can be yours to keep. In the hall I do not want to be carried in your file. I want to stand."

    $ set_expression("kaoru", "satisfied")
    voice "audio/voice/kaoru_354.mp3"
    kaoru "Then stand. The oath is public. The rest is mine to file when you stop stammering like a petitioner."

    pause 2.0
    menu case5_private_intimacy_menu:
        "Come to the screen, tonight is his, not the city's.":
            $ case5_private_intimacy = True
            jump case5_private_intimacy_fade

        "Bow at the threshold, oath enough for one day.":
            jump case5_epilogue_week_one


label case5_private_intimacy_fade:

    scene black with fade
    pause 0.6

    $ show_cg_scene("case5_bedroom_toy", fade)
    pause 2.0

    voice "audio/voice/narrator_278.mp3"
    "She does not perform Crane purity behind his screen. She wants him honestly, without asking him to be kinder, only there, proprietary, filed under a heading she still refuses to name."

    voice "audio/voice/toa_293.mp3"
    toa "Magistrate-sama, still yours."

    voice "audio/voice/kaoru_355.mp3"
    kaoru "Still mine. That is the only title that matters behind my screen tonight."

    pause 2.0
    scene black with fade
    pause 1.0

    jump case5_epilogue_week_one


label case5_epilogue_week_one:

    $ case5_closed = True

    $ show_cg_scene("case5_epilogue_week", fade)
    pause 2.0
    play music audio.bgm_street fadein 2.0 loop volume 0.4

    voice "audio/voice/narrator_279.mp3"
    "The first week as his sworn left hand is not a triumph procession. It is runners, copied seals, and a quarter walk where the okami nod at her sash instead of her obi."

    $ set_expression("kaoru", "cold")
    voice "audio/voice/kaoru_356.mp3"
    kaoru "File the witness chain before noon. The Chrysanthemum root still has tendrils in the pleasure quarter."

    $ set_expression("toa", "soft")
    voice "audio/voice/toa_294.mp3"
    toa "Yes, Magistrate-sama. The line is written, and I am still at your door."

    $ set_expression("kaoru", "charm")
    voice "audio/voice/kaoru_357.mp3"
    kaoru "Good. Case Five is pinned, not closed. The city still lies."

    voice "audio/voice/narrator_280.mp3"
    "She does not say love. He does not offer it. Ryoko Owari has a name on his left hand, and a week that has only begun."

    pause 2.0

    if epilogue_romance_bonus_eligible():
        jump epilogue_romance_bonus

    # Canon capstone for completions that do not (re)play the bonus epilogue:
    # roll the ED credits as the emotional close.
    call ed_sequence from _ed_after_week_one
    return


label case5_noncanon_discharge:

    scene bg magistrate_office with dissolve
    play music audio.bgm_office fadein 1.5 loop volume 0.4
    show kaoru cold at left
    show toa determined at right

    voice "audio/voice/narrator_281.mp3"
    "The hearing hall does not open for witness-only paper. A clerk stamps discharge instead of appointment, and the pleasure-quarter seal on the summons goes in the file as bait, not verdict."

    voice "audio/voice/kaoru_358.mp3"
    kaoru "You served the docket. The city has your testimony. Do not expect my corridor to keep a room warm on gratitude alone."

    show toa soft
    voice "audio/voice/toa_295.mp3"
    toa "I will not ask for more than you owe the file."

    voice "audio/voice/kaoru_359.mp3"
    kaoru "Good. Case Five sleeps on my desk until someone earns the left hand. The Chrysanthemum root keeps its tendrils in the quarter, the way the big files always do."

    voice "audio/voice/narrator_445.mp3"
    "She served the season and kept her own road. Somewhere a peer magistrate's wax stays warm and uncut, and Ryoko Owari goes on lying as politely as ever. Some files the city never closes. That, too, is an ending."

    return


# --- ENDING: refusal (honorable estrangement; she keeps her name and freedom) ---
# Declining a sworn oath is a boundary the tender canon Kaoru respects, not a crime
# he punishes. He releases her with her permit and her freedom intact, and does not
# pursue. Bittersweet "the one that got away" close, modeled on the consent framing
# (an oath must be chosen) and the Kaoru-absent rain end.

label case5_refusal_estrangement:

    $ case5_closed = True
    $ seen_gameover_case5 = True

    scene bg hearing_hall with dissolve
    show kaoru cold at center
    show toa determined at left

    voice "audio/voice/narrator_288.mp3"
    "The scroll stays open a breath, then he rolls it closed himself. Quarter clerks on the left wall stop pretending they are not listening. No one reaches for chains. This is a parting, not a sentence."

    $ set_expression("toa", "angry")
    voice "audio/voice/toa_302.mp3"
    toa "I am Kakita Toa of the Crane. I came for a permit, not to become a name the city cites when the seal walks."

    $ set_expression("kaoru", "cold")
    voice "audio/voice/kaoru_365.mp3"
    kaoru "Then I will not forge your hand onto a docket you refuse to stand on. An oath taken under pressure is just another counterfeit seal, and I have hanged men for those."

    voice "audio/voice/narrator_289.mp3"
    "The Crane envoy's crest finally rises. Whatever he writes home tonight, it will not be a scandal. It will be a dancer who kept her own name in a city that collects them."

    $ set_expression("kaoru", "commanding")
    voice "audio/voice/kaoru_366.mp3"
    kaoru "Your permit stands, dated and honest. The stipend closes with the case. The adjoining chamber empties tonight. Dance in any quarter that will have you, and none of them will owe me a thing."

    $ show_cg_scene("case5_false_exit_office", fade)
    pause 2.0

    $ set_expression("toa", "soft")
    voice "audio/voice/toa_440.mp3"
    toa "You are letting me go. After all of it, you are simply... letting me go."

    $ set_expression("kaoru", "cold")
    voice "audio/voice/kaoru_571.mp3"
    kaoru "I keep what signs willingly. You did not. Holding what will not stay is the one crime this office cannot file. Take your road, Kakita Toa. Walk it on your own paper."

    voice "audio/voice/narrator_444.mp3"
    "She gathers the travel kosode she packed that morning, the one that turned out to be true after all. The corridor she had learned by heart goes quiet behind her. He does not follow. He never once raises his voice, and that is the gentlest cruelty the city ever taught him."

    pause 0.6
    scene black with fade
    pause 0.6

    centered "{size=+10}Ending{/size}\n{size=-4}The Road She Kept{/size}"
    pause 0.4

    centered "{size=+4}Kakita Toa kept her name, her permit, and her freedom.{/size}\n{size=-4}Some files the city never closes. Some hands it never gets to keep.{/size}"

    stop music fadeout 3.0
    return


# --- DEV-ONLY BAD ENDS: brutal refusal variants, reachable from the dev chapter-pick
# menu only (no canon path routes here). Kept for save/test compatibility. ---

label case5_bad_end_refusal_chained:

    $ seen_gameover_case5 = True

    $ set_expression("kaoru", "cold")
    voice "audio/voice/kaoru_360.mp3"
    kaoru "You refused the name. The city will still want one on my left hand. It will not be yours."

    $ set_expression("toa", "worried")
    voice "audio/voice/toa_304.mp3"
    toa "Magistrate-sama... I will sign. I will take the oath..."

    voice "audio/voice/kaoru_367.mp3"
    kaoru "Scroll ink dries at the dais. You are not at the dais anymore."

    jump gameover_case5_chained


label case5_bad_end_refusal_cage:

    $ seen_gameover_case5 = True

    $ set_expression("kaoru", "cold")
    voice "audio/voice/kaoru_369.mp3"
    kaoru "Fine. The hall keeps what the scroll would have claimed. Holding cell. Ink. Witnesses who learn not to hear."

    $ set_expression("toa", "angry")
    voice "audio/voice/toa_306.mp3"
    toa "I am not a Scorpion debtor you can cage for sport."

    voice "audio/voice/kaoru_370.mp3"
    kaoru "You are a Crane dancer who embarrassed my docket in open court. The file will say corrective custody."

    jump gameover_case5_quarter_cage
