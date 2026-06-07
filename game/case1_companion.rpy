# Case 1, Companion arrangement (canon path, three days after prologue).
# Canon: physical "unless?" → permit dated +3 days → live-in companion / art sponsorship offer.
# Continues into Case 1 investigation via case1_investigation_hook.

label case1_companion_offer:

    scene bg magistrate_office with dissolve
    play music audio.bgm_office fadein 2.0 loop volume 0.62
    play sound audio.sliding_door_open volume 0.75
    show kaoru smirk at left
    show toa happy at right

    voice "audio/voice/narrator_052.mp3"
    "Morning in the noble quarter tastes of ink and cedar. The thirtieth is still the date on her permit, but Toa is already at the threshold with tea and a borrowed case file."

    voice "audio/voice/toa_067.mp3"
    toa "The permit says I'm legal on the thirtieth. I'm early with tea and a case file."

    show kaoru cruel
    voice "audio/voice/kaoru_081.mp3"
    kaoru "Early is still obedience. Sit before you spill something on my docket."

    voice "audio/voice/narrator_053.mp3"
    "He gestures to the cushion on the tatami in front of the desk, the same spot where he made her sit for her audition."

    show toa determined
    voice "audio/voice/toa_068.mp3"
    toa "Snacks after paperwork. That's still the order of operations, isn't it?"

    show kaoru satisfied
    voice "audio/voice/kaoru_082.mp3"
    kaoru "We'll see if your appetite survives what I'm about to read you aloud."

    if performance_style == "flirtatious":
        $ case1_sponsorship_flirt = True
        show kaoru hungry
        voice "audio/voice/kaoru_083.mp3"
        kaoru "Bring that audience-of-one fervor to the docket. Cases bore me less when you perform."

        show toa happy
        voice "audio/voice/toa_070.mp3"
        toa "Then I'll save the bells for evidence review."

    elif performance_style == "formal_dance":
        show kaoru amused
        voice "audio/voice/kaoru_091.mp3"
        kaoru "You danced like a maiden at a shrine. Try not to bow to the corpse."

        show toa flustered
        voice "audio/voice/toa_078.mp3"
        toa "I'll manage, Magistrate-sama. I know the difference."

    if formality_tone == "hyper_formal":
        show toa worried
        voice "audio/voice/toa_079.mp3"
        toa "Honored Magistrate-sama, shall I pour the tea before the terms you mentioned on the thirtieth, or after?"

        show kaoru bored
        voice "audio/voice/kaoru_092.mp3"
        kaoru "After. And stop bowing at every clause. My neck aches just from watching you."

    elif formality_tone == "direct":
        show toa determined
        voice "audio/voice/toa_080.mp3"
        toa "You said we'd discuss residency. So I'm listening."

        show kaoru smirk
        voice "audio/voice/kaoru_093.mp3"
        kaoru "Good. Plain speech spares us both another fan dance."

    show kaoru charm
    voice "audio/voice/kaoru_321.mp3"
    kaoru "I find you less tiresome than the rest of my docket. Enough that I have decided to keep you within reach. Do not make me phrase it more plainly than that."

    # Beat, Guest room preview becomes formal offer
    play sound audio.paper_shuffle volume 0.55
    show kaoru commanding

    voice "audio/voice/narrator_054.mp3"
    "He slides a stack across the desk. Not her permit book this time, but office stationery stamped with the Emerald crest."

    voice "audio/voice/kaoru_094.mp3"
    kaoru "You may keep the guest room until the date takes effect. That was courtesy, not a loophole."

    show toa flustered
    voice "audio/voice/toa_081.mp3"
    toa "A guest room. A preview. You really do enjoy making people come back, don't you."

    show kaoru charm
    voice "audio/voice/kaoru_161.mp3"
    kaoru "The signature was always going to bring you back. I merely wrote out the appointment you'd earned."

    show kaoru thinking
    voice "audio/voice/kaoru_426.mp3"
    kaoru "Before I read it aloud, one question. Plainly. When your permit was dying, you danced for me in this room. The quarter forgets dancers who vanish after sunset. I don't."

    show toa soft
    voice "audio/voice/toa_319.mp3"
    toa "You watched like the whole city had gone quiet. That was not a clerk's audition, Magistrate-sama."

    show kaoru satisfied
    voice "audio/voice/kaoru_427.mp3"
    kaoru "No. Witnesses lie. You had a body worth housing and a voice worth putting on a filing."

    menu case1_sponsorship_prelude_menu:
        "Ask him, honestly, what he wants from you.":
            $ insight += 1
            show toa worried
            voice "audio/voice/toa_320.mp3"
            toa "What do you actually want from me? Not the polite version. The one you write down on paper."

            show kaoru commanding
            voice "audio/voice/kaoru_428.mp3"
            kaoru "Attendance. Discretion. Art that doesn't embarrass the seal on my door."

        "Offer to dance again: show him the art is still yours.":
            $ performance_boldness += 1
            $ case1_sponsorship_flirt = True
            show toa determined
            voice "audio/voice/toa_321.mp3"
            toa "If you need proof, I'll dance. Not for ink this time. For your eyes only."

            show kaoru hungry
            voice "audio/voice/kaoru_429.mp3"
            kaoru "Later. First you hear what I'm willing to pay for."

        "Hold back: the permit should be enough without new chains.":
            $ honor += 1
            $ kaoru_resistance += 1
            show toa angry
            voice "audio/voice/toa_322.mp3"
            toa "I came for a renewal, not a collar. Tell me what this costs before I seal anything."

            show kaoru amused
            voice "audio/voice/kaoru_430.mp3"
            kaoru "Brave. The cost is written right here. Listen."

    show kaoru charm
    voice "audio/voice/kaoru_431.mp3"
    kaoru "This is sponsorship, not a courtesan's contract. The ledger reads art donor to artist. I will not insult your lord or mine by playing danna to a Crane who crossed provinces for ink."

    show toa flustered
    voice "audio/voice/toa_323.mp3"
    toa "Sponsorship. Not... not that."

    show kaoru commanding
    voice "audio/voice/kaoru_432.mp3"
    kaoru "Coin for your art, openly given. I know exactly what I am paying for, and so do you. 'Patronage' is the courtesy the ledger requires. Interpret it as liberally as you like, so long as you do it under my roof."

    show toa thinking
    voice "audio/voice/toa_324.mp3"
    toa "How often, Magistrate-sama? And where? The thirtieth was supposed to mean residency, not..."

    show kaoru satisfied
    voice "audio/voice/kaoru_433.mp3"
    kaoru "Twice a week you attend me here. For performance, and for case work when I need a witness who doesn't flinch. The rest is written below."

    $ show_cg_scene("permit_desk")
    play music audio.bgm_kaoru_theme fadein 1.8 loop volume 0.58

    voice "audio/voice/narrator_055.mp3"
    "The top sheet is titled {i}Appointment of Live-In Companion (Patronage of Artistic Residence){/i}. Her name is already inked there, in his hand."

    $ set_expression("toa", "surprised")
    voice "audio/voice/toa_082.mp3"
    toa "Live-in companion. That's not a guest room preview. That's a contract."

    $ set_expression("kaoru", "smirk")
    voice "audio/voice/kaoru_095.mp3"
    kaoru "Companion duties: attend the magistrate, carry messages, witness interviews, keep discretion, remain on the premises unless I release you. The treasury pays for the art. Everything else it merely permits."

    "Witness, on his paper, is not rank. It is permission to stand where he points and speak what she saw before the quarter can bury it. A Crane dancer hears what constables cannot ask and geisha will not repeat to men wearing seals."

    voice "audio/voice/kaoru_096.mp3"
    kaoru "You'll take meals in the inner hall. You'll sleep in the chamber adjoining my office. You'll answer when I call, day or night."

    $ set_expression("toa", "thinking")
    voice "audio/voice/toa_083.mp3"
    toa "Day or night. You ask a great deal, Magistrate-sama."

    $ set_expression("kaoru", "commanding")
    voice "audio/voice/kaoru_097.mp3"
    kaoru "It sounds like law because it is. Ryoko Owari doesn't grant interclan residence to dancers who vanish after sunset."

    play sound audio.hanko_case_click volume 0.4
    voice "audio/voice/narrator_056.mp3"
    "He taps a second page: stipend figures, duty rotations, and a line for her seal beside his."

    $ set_expression("toa", "worried")
    voice "audio/voice/toa_084.mp3"
    toa "And the stipend?"

    $ set_expression("kaoru", "amused")
    voice "audio/voice/kaoru_098.mp3"
    kaoru "Three koku monthly, plus board. Official gifts to support your expression. The treasury won't call you a kept performer so long as the ledger says patronage."

    scene bg magistrate_office with dissolve
    show kaoru smirk at left
    show toa surprised at right

    show toa thinking
    voice "audio/voice/toa_085.mp3"
    toa "Three koku is more than the curry shop ever paid me to smile at tourists."

    show kaoru cruel
    voice "audio/voice/kaoru_099.mp3"
    kaoru "Then you understand the bargain. Sign it, or go back to Unicorn roads and expired paper."

    if canon_first_scene and physical_initiative >= 1:
        show kaoru hungry
        voice "audio/voice/kaoru_100.mp3"
        kaoru "You already proved you can close a proposition in this room. Don't pretend shock suits you."

        show toa flustered
        voice "audio/voice/toa_086.mp3"
        toa "Shock and delight, both at once. You do that to me."

    $ show_cg_scene("moment case1_companion_accept_menu")

    menu case1_companion_accept_menu:
        "Accept with composure: the sponsored artist she means to become.":
            $ companion_accept_tone = "graceful"
            $ composure += 2
            $ honor += 1
            $ compliance += 1
            show toa determined
            voice "audio/voice/toa_087.mp3"
            toa "Magistrate-sama, I accept the appointment and its duties. You'll have my discretion and my attendance."

            show kaoru satisfied
            voice "audio/voice/kaoru_101.mp3"
            kaoru "Better. You almost sound like you belong behind my desk, instead of on it."

        "Negotiate: duties, hours, and what 'release' actually means.":
            $ companion_accept_tone = "negotiate"
            $ insight += 2
            $ kaoru_resistance += 1
            $ negotiated_terms = True
            show toa determined
            voice "audio/voice/toa_088.mp3"
            toa "I'll sign once we've defined release, and settled which nights are mine for Academy correspondence."

            show kaoru amused
            voice "audio/voice/kaoru_102.mp3"
            kaoru "Bold, for someone who still smells of my cedar shelves."

            show kaoru commanding
            voice "audio/voice/kaoru_103.mp3"
            kaoru "Academy letters wait on the outer desk. You don't leave this compound without escort until Case One closes. Those are the terms."

            show toa thinking
            voice "audio/voice/toa_089.mp3"
            toa "Escort, not a leash. I can live with that."

            show kaoru smirk
            voice "audio/voice/kaoru_104.mp3"
            kaoru "You'll work with what I give you. Now sign."

        "Gush honestly: the money means nothing next to staying.":
            $ companion_accept_tone = "gush"
            $ performance_boldness += 1
            $ kaoru_submission += 1
            $ case1_sponsorship_flirt = True
            show toa happy
            voice "audio/voice/toa_090.mp3"
            toa "Three koku. Fine. Wonderful, I'll frame the ledger. But Magistrate-sama, I want the room. I want the hall. I want to be here."

            show toa flustered
            voice "audio/voice/toa_091.mp3"
            toa "That came out louder than was professional."

            show kaoru charm
            voice "audio/voice/kaoru_105.mp3"
            kaoru "Honest, at last. The treasury pays you regardless. Try not to grin at the clerk."

    jump case1_companion_offer_close

label case1_companion_offer_close:

    scene bg magistrate_office with dissolve
    show kaoru smirk at left
    show toa happy at right

    play sound audio.paper_shuffle volume 0.5
    voice "audio/voice/narrator_057.mp3"
    "She takes up the brush. Her seal meets his: waxless, official, irrevocable until he says otherwise."

    play sound audio.hanko_stamp volume 0.65
    $ live_in_companion = True
    $ permit_signed = True

    if permit_effective_days < 3:
        $ permit_effective_days = 3

    show kaoru satisfied
    voice "audio/voice/kaoru_106.mp3"
    kaoru "Effective on the thirtieth, as written. Until then, you're mine to schedule, starting with Case One."

    show toa determined
    voice "audio/voice/toa_092.mp3"
    toa "Case One it is. Files, witnesses, and snacks for the road."

    show kaoru cold
    voice "audio/voice/kaoru_107.mp3"
    kaoru "You'll fetch the docket from the inner archive. Then you'll learn how this city buries its dead without funerals."

    if companion_accept_tone == "gush":
        show toa soft
        voice "audio/voice/toa_093.mp3"
        toa "I'll fetch it. I'll learn it. Just... thank you. For the room next to yours."

        show kaoru hungry
        voice "audio/voice/kaoru_108.mp3"
        kaoru "Thank me with a dry ledger, not with your mouth. Archive stairs. Now."

    elif companion_accept_tone == "negotiate":
        show toa determined
        voice "audio/voice/toa_094.mp3"
        toa "Archive. Escort. Written terms. I'm holding you to all three."

        show kaoru cold
        voice "audio/voice/kaoru_109.mp3"
        kaoru "Hold the lantern instead. You'll want both hands free on those steps."

    else:
        show toa neutral
        voice "audio/voice/toa_095.mp3"
        toa "Understood. I'll be back with the docket and a dry obijime."

        show kaoru charm
        voice "audio/voice/kaoru_110.mp3"
        kaoru "Leave the bells behind. This case is not a stage."

    $ show_cg_scene("moment case1_first_duty_menu")

    menu case1_first_duty_menu:
        "Ask where the adjoining chamber is: move in today.":
            $ insight += 1
            show toa happy
            voice "audio/voice/toa_096.mp3"
            toa "Point me to the chamber. I'd rather unpack before the archive swallows me whole."

            show kaoru amused
            voice "audio/voice/kaoru_111.mp3"
            kaoru "Past the inner screen, down the left corridor. Don't rearrange my shelves."

            show toa flustered
            voice "audio/voice/toa_097.mp3"
            toa "I only peeked the once. And you noticed."

            show kaoru smirk
            voice "audio/voice/kaoru_112.mp3"
            kaoru "I notice everything. Unpack after the docket, not before."

        "Go straight to the archive: prove the companion role first.":
            $ honor += 1
            $ composure += 1
            show toa determined
            voice "audio/voice/toa_098.mp3"
            toa "Archive first. You'll know I'm serious when I come back covered in dust."

            show kaoru satisfied
            voice "audio/voice/kaoru_113.mp3"
            kaoru "Left stair, behind the screen. Archive dust on your hakama is acceptable. Just don't drop the ledger."

        "Tease him: companion duty surely includes refilling his tea.":
            $ performance_boldness += 1
            $ kaoru_submission += 1
            $ case1_sponsorship_flirt = True
            show toa happy
            voice "audio/voice/toa_099.mp3"
            toa "Case One, the archive, and look, your cup's already empty. Companion duty starts now."

            show kaoru cruel
            voice "audio/voice/kaoru_114.mp3"
            kaoru "Refill it. Then the archive. Then unpack. In that order, or I'll date your next permit forward again."

            show toa surprised
            voice "audio/voice/toa_100.mp3"
            toa "Cruel. And fair. The cup first, then."

    jump case1_investigation_hook

label case1_investigation_hook:

    # Bridge to Case 1 investigation loop (Milestone B).
    scene bg magistrate_office with dissolve
    show kaoru commanding at left
    show toa determined at right

    play music audio.bgm_office fadein 1.5 loop volume 0.6

    voice "audio/voice/kaoru_328.mp3"
    kaoru "Five matters on my slate this season. Companion ink puts you on my witness docket for all of it, Case One through Five. Survive all five, or the quarter eats your stipend."

    show toa surprised
    voice "audio/voice/toa_277.mp3"
    toa "The permit was for dance. Patronage. A room behind your screen, not five corpses in rotation."

    show kaoru smirk
    voice "audio/voice/kaoru_329.mp3"
    kaoru "Dance bought you the corridor. Cases buy your keep. Show me competence I can reach for. Archive stairs, the Case One ledger, before the watch blanks that name line."

    voice "audio/voice/narrator_270.mp3"
    "He files witness attachment the way clerks file tax. Her whole season is already columned on his desk, five cases on one witness chain, and he never once said yoriki."

    "She came for patronage and a permit. The docket makes her his eyes in rooms his constables would turn into clan feuds, and whatever she signs under his seal becomes filing."

    voice "audio/voice/narrator_058.mp3"
    "The inner screen slides open. Beyond it, the stairs smell of old paper and river damp: the archive, where Case One waits."

    voice "audio/voice/kaoru_115.mp3"
    kaoru "When you come back, we open the file on the canal body. No audience. No bells. Only answers."

    show toa thinking
    voice "audio/voice/toa_101.mp3"
    toa "Snacks after paperwork. The rule still holds, even for corpses without funerals."

    show kaoru smirk
    voice "audio/voice/kaoru_116.mp3"
    kaoru "Bring rice crackers. I'll allow one indulgence before the city disappoints you."

    jump case1_investigation_start

# --- Non-canon path (verbal / walkout prologue), three weeks later ---

label case1_noncanon_start:

    scene bg magistrate_office with dissolve
    play music audio.bgm_office fadein 2.0 loop volume 0.62
    show toa neutral at right
    show kaoru smirk at left

    voice "audio/voice/toa_071.mp3"
    toa "Case file, tea, and, if I've been very good, a rice cracker. Ready when you are."

    show kaoru commanding
    voice "audio/voice/kaoru_331.mp3"
    kaoru "Correction: five matters on my slate this season. Witness attachment only. Case One through Five. No companion seal on this timeline."

    show toa angry
    voice "audio/voice/toa_279.mp3"
    toa "You sold me a permit renewal. Not a whole magistrate's season."

    show kaoru cruel
    voice "audio/voice/kaoru_332.mp3"
    kaoru "Seasons are what I assign. Fetch Case One from the archive. Survive the season, and then we'll discuss whether you sleep in my hall."

    if unless_branch == "walk_out":
        show kaoru cold
        voice "audio/voice/kaoru_085.mp3"
        kaoru "You came back. I noted that."

        show toa determined
        voice "audio/voice/toa_072.mp3"
        toa "The permit still expires. Some of us actually read the dates."

        if rebuke >= 2:
            show kaoru amused
            voice "audio/voice/kaoru_086.mp3"
            kaoru "You still flinch when I reach for the cup. Don't, next time."

            show toa angry
            voice "audio/voice/toa_073.mp3"
            toa "Progress would be signing without all the games."

    elif unless_branch == "verbal":
        show kaoru amused
        voice "audio/voice/kaoru_087.mp3"
        kaoru "You negotiated once. We'll see if you learned anything."

        show toa happy
        voice "audio/voice/toa_074.mp3"
        toa "I learned that you drink water when you're impressed."

        if negotiated_terms:
            show toa determined
            voice "audio/voice/toa_075.mp3"
            toa "I also learned your terms shift. So Case One gets its terms in writing."

            show kaoru smirk
            voice "audio/voice/kaoru_088.mp3"
            kaoru "Ambitious. Now fetch the file."

    if permit_strategy == "local_fix":
        show kaoru commanding
        voice "audio/voice/kaoru_089.mp3"
        kaoru "You asked me for remedies once. Case One is your audition for belonging here."

        show toa determined
        voice "audio/voice/toa_076.mp3"
        toa "Then watch closely. Audience of one."

    elif permit_strategy == "plead":
        show kaoru cruel
        voice "audio/voice/kaoru_090.mp3"
        kaoru "No curry shop tonight. Just work."

        show toa happy
        voice "audio/voice/toa_077.mp3"
        toa "Fine. But I'm billing you for the snacks."

    voice "audio/voice/narrator_059.mp3"
    "A live-in companion appointment waits in draft on his desk: unsigned, unoffered on this timeline. Case One opens without the patronage seal."

    show kaoru commanding
    voice "audio/voice/kaoru_117.mp3"
    kaoru "Fetch the canal docket from the archive. We'll discuss residency once you've survived the season."

    jump case1_investigation_start
