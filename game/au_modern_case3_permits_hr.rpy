# Modern AU Case 3: Permits & HR (dev bonus sequel; trilogy cap).
#
# Play: Main menu → "AU Case 3: Permits & HR"; dev pick → "AU Case 3: Permits & HR";
#   or Case 2 end → "Continue to Case 3: Permits and HR?"
# VOICED: narrator_425+, toa_417+, kaoru_549+ (wire: scripts/wire_au_modern_case3_voice.py).
# New choice flags live in game/stats.rpy (au_modern_case3_*); reads existing Case 2 flags too.
# Does not set canon case/permit flags.

label au_modern_case3_start:

    ## Launched in the rollback-enabled game (root) context, from the Modern AU hub
    ## (au_modern_hub_menu) or the dev chapter pick. Because this is the normal game
    ## context (not a call_in_new_context child of the menu), Back/rollback, mid-episode
    ## saving, character + narrator voices, and the quick/game menu all work without any
    ## menu-state fix-ups. Mark the AU episode active so the story-music mute callback
    ## keeps story BGM audible (incl. after loading a mid-episode save).
    $ au_episode_active = True
    $ enable_cinematic_music()

    $ seen_au_modern_case3 = True
    $ au_modern_case3_statement = ""
    $ au_modern_case3_disclosure = ""

    scene black with fade
    play music audio.bgm_office fadein 2.5 loop volume 0.32

    centered "{font=fonts/YujiSyuku-Regular.ttf}{size=+6}Permits & HR{/size}{/font}\n{size=-4}Modern AU · Case 3 · dev bonus{/size}"

    pause 1.0

    voice "audio/voice/narrator_425.mp3"
    "Tuesday in Ryoko Port opens the way audits open. Not with a knock, with a notification. Weeks after the harbor weekend, rain files itself against the licensing tower while a clip eleven seconds long teaches the whole channel a deputy director's voice."

    voice "audio/voice/narrator_426.mp3"
    "Someone screen-recorded the Wrong Floor hearing weeks ago, back when it was only a routine Arts Council licensing stream nobody watched. *If the agenda cannot tolerate a witness, revise the agenda.* The internet revised nothing. It played the line forty thousand times, set it to a beat, and tagged the Council's account until the Council itself had to notice."

    $ show_cg_scene("au_modern_case3_trending_office", fade)
    pause 2.0

    voice "audio/voice/toa_417.mp3"
    toa "Deputy Director-sama, you are trending. Your one good sentence has a hashtag and a remix."

    voice "audio/voice/kaoru_549.mp3"
    kaoru "Trending is not a docket. Sit where I can see you and the inbox. People and Conduct, the office the Council refers conflicts to, opened a file at eight this morning, before the coffee was enforceable."

    voice "audio/voice/narrator_478.mp3"
    "People and Conduct does not investigate feelings. It investigates conflicts of interest, and it has exactly one question about the two of them: whether a deputy who signed an artist's sponsorship had any business signing for an artist the whole channel now assumes he favors. Behind the question sits the Council's full kit of remedies, the ones every sponsorship hangs under: suspend it, revoke it, audit it, reassign the signatory, or compel disclosure. Whatever they choose goes in a permanent file that outlives the clip, the hashtag, and probably the deputy."

    jump au_modern_case3_viral_clip


label au_modern_case3_viral_clip:

    $ show_cg_scene("au_modern_case3_viral_clip", fade)
    pause 2.0

    voice "audio/voice/narrator_427.mp3"
    "On Toa's phone the clip loops in a feed that does not care about packets. A councilor freezes mid-objection. A white-haired applicant sits in the wrong chair. The comments sort themselves into the usual castes."

    voice "audio/voice/toa_418.mp3"
    toa "The top comment says *who is the dancer*. The second says *HR nightmare*. The third is a recipe ad. The internet has no witness posture."

    voice "audio/voice/toa_419.mp3"
    toa "And someone clipped the part where you muted the gallery. They captioned it *deputy protects mystery girl*. I am the mystery girl. I have a name and an expired packet."

    voice "audio/voice/kaoru_550.mp3"
    kaoru "You have a current packet now. That is the problem the clip just made expensive. I signed it. You depend on it. A camera turned both facts into a story we did not write."

    voice "audio/voice/narrator_428.mp3"
    "He does not watch the clip. He watches the inbox count climb, the way a man watches a tide decide whether to take the lower dock."

    jump au_modern_case3_hr_summons


label au_modern_case3_hr_summons:

    scene black with dissolve
    pause 0.4

    $ show_cg_scene("au_modern_case3_fishbowl_exterior", fade)
    pause 1.5

    $ show_cg_scene("au_modern_case3_hr_office", fade)
    pause 2.0

    voice "audio/voice/narrator_429.mp3"
    "The HR wing is all glass and acoustic panels, a fishbowl that lets the building watch you stay calm. A liaison named in the calendar only as *People & Conduct* slides two folders across the table with the patience of a fault line."

    voice "audio/voice/kaoru_551.mp3"
    kaoru "Folder one: signatory of record, Kitsu Kaoru. Folder two: sponsorship dependent applicant, Kakita Toa. The clip put both folders in the same frame. HR would like the frame explained."

    voice "audio/voice/toa_420.mp3"
    toa "I walked into the wrong conference room once. I have read the plate every day since. Does the file know I read the plate now?"

    voice "audio/voice/narrator_430.mp3"
    "The liaison says, in the level voice of someone reading policy aloud, that the concern is not the wrong door. The concern is a signatory whose name appears beside a dependent the public has decided to find interesting."

    voice "audio/voice/kaoru_552.mp3"
    kaoru "The concern is conflict of interest. Stated plainly: a deputy who signs for an applicant he is rumored to favor. Rumor is not a finding. But rumor schedules meetings, and we are in one."

    voice "audio/voice/toa_421.mp3"
    toa "So the building thinks the rider says romance, and the rider says *not romance on letterhead*. We agree with the letterhead. The internet did not read the letterhead."

    voice "audio/voice/kaoru_553.mp3"
    kaoru "Before the liaison files, we decide the public posture. Choose, applicant. The clip is loud. Our answer should be quieter, but it still has to be an answer."

    menu au_modern_case3_statement_menu:

        "Issue a public statement (own the narrative).":
            $ au_modern_case3_statement = "public"
            voice "audio/voice/toa_422.mp3"
            toa "We post one statement. Plain. *The deputy seated a confused applicant and corrected a packet error. There is no story. There is a queue.* I will sign my own name to it."

            voice "audio/voice/kaoru_554.mp3"
            kaoru "Owning the narrative is a real strategy. It is also a microphone. If you take the microphone, you do not improvise. Dates and names only, even in a caption."

            jump au_modern_case3_signatory_desk

        "Stay quiet, let HR process the file (witness posture).":
            $ au_modern_case3_statement = "quiet"
            voice "audio/voice/toa_423.mp3"
            toa "Then I do nothing loud. I keep witness posture. The clip wants a reaction. I give it a closed mouth and a current packet."

            voice "audio/voice/kaoru_555.mp3"
            kaoru "Silence is also a filing. Harder to misquote, slower to clear. You will sit in the comments for a week and not answer them. Some applicants cannot. Can you?"

            jump au_modern_case3_signatory_desk


label au_modern_case3_signatory_desk:

    scene black with dissolve
    pause 0.4

    $ show_cg_scene("au_modern_case3_signatory_desk", fade)
    pause 2.0

    voice "audio/voice/narrator_431.mp3"
    "Back in the licensing wing, the sponsorship packet lies open under the desk lamp. His chop in the signatory box. Her name in the dependent box. Two boxes a camera turned into a couple."

    voice "audio/voice/kaoru_556.mp3"
    kaoru "Signatory of record means I answer for your compliance. Sponsorship dependent means your right to work in this port routes through my signature. That is leverage. I do not enjoy being someone's leverage, including my own."

    voice "audio/voice/toa_472.mp3"
    toa "And if the Council decides the leverage looks like a favor, they can suspend the sponsorship, or revoke it, or hand my file to a deputy who never met me. My whole right to dance in this port is one sentence you signed. I keep forgetting that until a fishbowl reminds me."

    voice "audio/voice/toa_424.mp3"
    toa "You sound like a man reading his own name as a liability. I have practiced that face in studio mirrors. It is not a flattering port de bras."

    voice "audio/voice/narrator_432.mp3"
    "He almost answers that. He files the almost where he files everything he intends to keep."

    if au_modern_case3_statement == "public":
        voice "audio/voice/narrator_433.mp3"
        "By noon her statement is live under her own handle, three sentences, no emoji, a queue number where a heart might go. The remix accounts hate that it is boring. Boring is enforceable."

        $ show_cg_scene("au_modern_case3_public_statement", fade)
        pause 2.0

        voice "audio/voice/toa_425.mp3"
        toa "I owned it. *Confused applicant, corrected packet, no story.* My follower count went up. My panic went down. Roughly even trade."

    else:
        voice "audio/voice/narrator_434.mp3"
        "By noon she has posted nothing. The clip keeps looping without her. The silence reads, to everyone but her, like composure. To her it reads like sitting in the wrong chair and not getting up."

        $ show_cg_scene("au_modern_case3_quiet_witness", fade)
        pause 2.0

        voice "audio/voice/toa_426.mp3"
        toa "I stayed quiet. Witness posture. It turns out the hardest deliverable is the one where I do not defend myself out loud."

    voice "audio/voice/kaoru_557.mp3"
    kaoru "Either way the public narrative now exists in parallel with my actual calendar. Those two ledgers do not match, and HR audits the gap, not the gossip."

    jump au_modern_case3_calendar_vs_narrative


label au_modern_case3_calendar_vs_narrative:

    voice "audio/voice/narrator_435.mp3"
    "He turns his monitor toward her. The public narrative: a deputy and his favorite. The deputy's real calendar: thirty-one applicants, four inspections, a ferry receipt from a harbor weekend filed under *audit retreat*, and one row left blank on purpose."

    $ show_cg_scene("au_modern_case3_calendar_monitor", fade)
    pause 2.0

    voice "audio/voice/kaoru_558.mp3"
    kaoru "The harbor weekend is in the calendar as audit. The internet would call it something else. Both readings are on the same row. That row is what HR will ask me to explain."

    voice "audio/voice/toa_427.mp3"
    toa "So the question is not whether we did anything against the rules. The question is which version of us goes in the permanent file. The clip's version, or the calendar's."

    voice "audio/voice/kaoru_559.mp3"
    kaoru "Correct. And the applicant gets a vote, because the applicant is the one the file outlives. Choose how we resolve the signatory conflict before the liaison chooses a template for us."

    menu au_modern_case3_disclosure_menu:

        "Keep it procedural (amend the filing, hand the signature to another deputy).":
            $ au_modern_case3_disclosure = "procedural"
            voice "audio/voice/toa_428.mp3"
            toa "Recuse the signatory. Move my packet to a deputy with no hashtag. Clean conflict, clean file. You stop being my leverage. I stop being your liability."

            voice "audio/voice/kaoru_560.mp3"
            kaoru "Procedural and correct. It also means another desk reviews you, and I lose the only honest reason to keep you in my afternoons. I will file it anyway, if that is the version you can live in."

            jump au_modern_case3_reconcile

        "Disclose honestly (put the relationship on the record, personally).":
            $ au_modern_case3_disclosure = "personal"
            voice "audio/voice/toa_429.mp3"
            toa "Or we tell the truth on a form. *Signatory and applicant have a personal relationship. Signatory discloses. Applicant consents to oversight.* Not romance on letterhead. Romance disclosed in the margin, where HR can read it."

            voice "audio/voice/kaoru_561.mp3"
            kaoru "Disclosure is the riskier filing. It survives the clip by agreeing with it, on our terms. You understand that once I write it, the port owns the sentence too, not just the harbor."

            jump au_modern_case3_reconcile


label au_modern_case3_reconcile:

    scene black with fade
    pause 0.5

    $ show_cg_scene("au_modern_case3_reconcile", fade)
    pause 2.0

    voice "audio/voice/narrator_436.mp3"
    "After hours the HR fishbowl goes dark and his office keeps one lamp. The couch remembers them. A blanket, a bowl of clementines someone keeps restocking and denying. Rain reads the window like a slow auditor."

    if au_modern_case3_disclosure == "procedural":
        $ show_cg_scene("au_modern_case3_recuse_handover", fade)
        pause 2.0

        voice "audio/voice/kaoru_562.mp3"
        kaoru "I filed the recusal. Deputy Saito reviews your packet now. He is competent and he does not know your coffee order. That is the price of a clean conflict."

        voice "audio/voice/toa_430.mp3"
        toa "So you are not my signatory anymore. You are just the man who taught me witness posture and keeps clementines he claims he does not eat."

    else:
        voice "audio/voice/kaoru_563.mp3"
        kaoru "I wrote the disclosure in my own hand. *Personal relationship. Disclosed. Oversight accepted.* The port owns that sentence now. So, apparently, do I."

        $ show_cg_scene("au_modern_case3_disclosure_signed", fade)
        pause 2.0

        $ show_cg_scene("au_modern_case3_paperwork_tears", dissolve)
        pause 2.0

        voice "audio/voice/toa_431.mp3"
        toa "You put us on a form and signed it. That is the most romantic thing a deputy director can do. It is also, technically, paperwork. I am crying about paperwork."

    $ show_cg_scene("au_modern_case3_after_hours", fade)
    pause 2.0

    if au_modern_case2_night_audit:
        voice "audio/voice/narrator_437.mp3"
        "The harbor weekend sits between them unspoken, the after-hours audit neither of them will caption. Her neck remembers a count. His calendar remembers a blank row he left on purpose."

        voice "audio/voice/toa_432.mp3"
        toa "If the clip ever finds the ferry receipt, I will deny everything in dates and names only. Saturday. Harbor. Audit. No poetry."

    else:
        voice "audio/voice/narrator_438.mp3"
        "Whatever the harbor weekend was, they filed it as debrief and salt air. The clip never reached the ferry receipt. Some rows stay blank because someone chose to leave them blank."

        voice "audio/voice/toa_433.mp3"
        toa "The clip got the conference room and none of the quiet parts. I find I do not want the internet auditing the quiet parts."

    voice "audio/voice/kaoru_564.mp3"
    kaoru "The quiet parts are not on any portal. Blanket is still a loan against your noise. Clementine is domestic filing. Almost-smile inventory: pending, denied, pending again."

    voice "audio/voice/toa_434.mp3"
    toa "You almost smiled when I said I cried about paperwork. I have witnesses. The witness is me. I am very reliable."

    voice "audio/voice/kaoru_565.mp3"
    kaoru "Motion denied, To-chan. Effective in three business days, like everything I intend to keep. Go home before the building decides we are a story it can stamp."

    voice "audio/voice/narrator_439.mp3"
    "She peels a clementine she did not ask permission to take, and the rain keeps its own minutes against the glass. Whichever way they filed it, the conflict now lives on the record instead of in the gossip, which is the one place the Council cannot use it against them. The clip will loop until the channel finds a louder one. The file will close quieter than it opened."

    jump au_modern_case3_end_stinger


label au_modern_case3_end_stinger:

    scene black with fade
    stop music fadeout 2.0

    if au_modern_case3_disclosure == "personal":
        centered "{size=+2}Permits & HR (Modern AU Case 3){/size}\n{size=-4}Disclosed in the margin. Not a story the city wrote.{/size}"
    else:
        centered "{size=+2}Permits & HR (Modern AU Case 3){/size}\n{size=-4}Conflict recused. The quiet parts stay off the portal.{/size}"

    pause 1.0

    jump au_modern_case3_end


label au_modern_case3_end:

    menu au_modern_case3_continue_menu:

        "Continue to the Epilogue: Effective Immediately?":
            jump au_modern_epilogue_start

        "Peek at the AU Bad End: Parking Garage? (stub)":
            scene black with fade
            centered "{size=+2}AU Bad End: Parking Garage{/size}\n{size=-4}Stub · design doc only · not yet playable.{/size}"
            pause 2.0

        "Return to menu.":
            pass

    if dev_chapter_pick_enabled:
        jump dev_chapter_pick_menu

    ## Back to the Modern AU hub (rollback-enabled game context). The hub clears
    ## au_episode_active and restores the menu theme.
    jump au_modern_hub_menu
