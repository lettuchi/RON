# Case 2: The Academy Packet (便りの灰 / Ashes of the Good Tidings).
# Entry: case1_barge_milestone_end → case2_investigation_start.
# Prior: Case One closed (Jiro murder, barge manifest); live-in companion optional.

label case2_investigation_start:

    $ case2_briefing_choice = ""
    $ case2_confront_choice = ""
    $ case2_courier_name = ""
    $ case2_packet_found = False
    $ case2_milestone = ""

    scene bg magistrate_office with dissolve
    play music audio.bgm_office fadein 2.0 loop volume 0.58
    show kaoru commanding at left
    show toa worried at right

    voice "audio/voice/narrator_229.mp3"
    "Case One's tray hasn't even cooled before the outer bell rings again. Not the watch. Not the Miya envoy. A Crane runner this time, clutching an empty satchel and a story that won't add up no matter how you stack it."

    voice "audio/voice/kaoru_244.mp3"
    kaoru "Case Two. The Academy was expecting a credential packet for one Kakita Toa. Charter renewal, examination waiver, all the paperwork you people dress up as mercy."

    voice "audio/voice/toa_211.mp3"
    toa "That satchel is my whole future. If it's ash, then I crawl back to the Academy in disgrace."

    show kaoru cold
    voice "audio/voice/kaoru_245.mp3"
    kaoru "They found the courier in a warehouse alley. Throat opened, satchel burned to nothing. The watch is calling it robbery. The ash is telling me it was a message."

    if live_in_companion:
        show kaoru charm
        voice "audio/voice/kaoru_246.mp3"
        kaoru "You're not running off to beg Crane clerks by letter. You'll find what burned, or you'll pack for that road I warned you about."

        show toa determined
        voice "audio/voice/toa_212.mp3"
        toa "Then we start where the fire did. This time the paper that burned is mine to mourn."

    else:
        show kaoru smirk
        voice "audio/voice/kaoru_247.mp3"
        kaoru "Your permit survived Case One. Case Two decides whether the Academy ever bothers to say your name again."

        show toa angry
        voice "audio/voice/toa_213.mp3"
        toa "Don't dangle my future like a coin to barter. Just point me at the alley and step back."

    $ show_cg_scene("moment case2_briefing_menu")

    menu case2_briefing_menu:
        "Trace the courier's route. Map it, time it, find who saw him last.":
            $ case2_briefing_choice = "route"
            $ insight += 2
            show toa thinking
            voice "audio/voice/toa_214.mp3"
            toa "Runners don't just vanish. Somebody watched him leave the compound, or watched him never arrive. Give me names and bell times."

            show kaoru satisfied
            voice "audio/voice/kaoru_248.mp3"
            kaoru "Methodical. So the Academy taught you something useful after all."

        "Ask who profits if the packet's gone. Politics first, ash later.":
            $ case2_briefing_choice = "politics"
            $ honor += 1
            $ insight += 1
            show toa determined
            voice "audio/voice/toa_215.mp3"
            toa "A burned charter hurts me first. So who else comes out ahead if I'm gone from Ryoko Owari by autumn?"

            show kaoru thinking
            voice "audio/voice/kaoru_249.mp3"
            kaoru "Make a list. The jealous, the indebted, the Scorpion leftovers. Case One left us enemies with ash still on their cuffs."

        "Witness statements only. No theories until the alley does the talking.":
            $ case2_briefing_choice = "witnesses"
            $ composure += 2
            $ honor += 1
            show toa neutral
            voice "audio/voice/toa_216.mp3"
            toa "Tell me what the watch wrote down. I'll fill in what the warehouse boys whisper once you've gone."

            show kaoru commanding
            voice "audio/voice/kaoru_250.mp3"
            kaoru "Discipline. Rare in you. Fetch the outer-desk file and meet me at the kiln."

    jump case2_warehouse_alley

label case2_warehouse_alley:

    scene bg street_exterior with fade
    play music audio.bgm_street fadein 2.0 loop volume 0.5
    show toa determined at right
    show kaoru cold at left

    voice "audio/voice/narrator_230.mp3"
    "The warehouse district trades honesty for inventory and never feels the loss. Rain has rinsed the cobbles clean, but not the soot. A narrow alley behind a rice broker's kiln still reeks of burned linen and Crane wax."

    voice "audio/voice/toa_217.mp3"
    toa "The air's wrong here. Thin, like the charms have been peeled away, like someone scraped the protection off these bricks and walked off laughing."

    voice "audio/voice/kaoru_251.mp3"
    kaoru "Or walked off paid. Charms don't come cheap this far from a shrine."

    $ show_cg_scene("moment case2_alley_menu")

    menu case2_alley_menu:
        "Dig through the ash. Sift for wax, seal fragments, anything Crane.":
            $ insight += 2
            voice "audio/voice/narrator_231.mp3"
            "Kneeling in the soot, Toa turns up a corner of lacquered board the fire never reached. The Academy's crane-in-flight crest, half melted, still unmistakable."

            show toa surprised
            voice "audio/voice/toa_218.mp3"
            toa "Crane wax. They burned the packet and missed the corner of the case. Either someone panicked, or someone wanted me to find proof it was ever real."

            $ case2_packet_found = True

        "Read the body, how he died, not just what they torched.":
            $ insight += 1
            $ composure += 1
            voice "audio/voice/narrator_232.mp3"
            "Rope burns ring the wrists. A thin cut tucked under the jaw. Not the showy strangling Jiro wore, but the same hand could have practiced on both."

            show toa worried
            voice "audio/voice/toa_219.mp3"
            toa "His name was Tsubaki. The watch knew it and left it off the report. That's silence you pay for."

            $ case2_courier_name = "Tsubaki"

        "Coax out the kiln boy crouched behind the rice sacks.":
            $ performance_boldness += 1
            $ insight += 1
            show toa soft
            voice "audio/voice/toa_220.mp3"
            toa "You, behind the sacks. I'm not the watch. I'm the woman whose future you can smell burning. So talk to me."

            "Kiln boy" "Saw a man in unmarked grey slip the foreman coin to keep the kiln hot past curfew. Scorpion lacquer at his collar, three black scales. Courier came tearing in, screaming about a seal. Then nothing."

            show kaoru cold
            voice "audio/voice/kaoru_252.mp3"
            kaoru "Grey to bury the clan colors, again. It seems Case One's little flower isn't finished with us yet."

        "Go in alone and read the ash before Kaoru catches up.":
            show toa determined
            voice "audio/voice/toa_221.mp3"
            toa "It's my charter in those ashes. Let me reach it first."

            show kaoru commanding
            voice "audio/voice/kaoru_253.mp3"
            kaoru "Toa. Wait..."

            jump gameover_case2_alley

    if not case2_courier_name:
        $ case2_courier_name = "Tsubaki"

    if not case2_packet_found:
        show toa thinking
        voice "audio/voice/toa_222.mp3"
        toa "No crest in the ash, but the boy's story leaves a footprint. Someone wanted the Academy to believe I never even arrived."

        $ case2_packet_found = True

    jump case2_outer_desk

label case2_outer_desk:

    scene bg magistrate_office with dissolve
    play music audio.bgm_office fadein 1.8 loop volume 0.56
    show kaoru commanding at left
    show toa determined at right

    voice "audio/voice/narrator_233.mp3"
    "The outer desk keeps what the alley couldn't burn. A duplicate routing slip, stamped but never filed, listing the courier's satchel and a second name scribbled in the margin."

    voice "audio/voice/kaoru_254.mp3"
    kaoru "That margin's a clerk's hand. Office ink, not warehouse soot. Someone inside my own compound touched the routing before Tsubaki ever set out."

    voice "audio/voice/toa_223.mp3"
    toa "Case One came at your seal from the street. This one was already holding your brush."

    $ show_cg_scene("moment case2_desk_menu")

    menu case2_desk_menu:
        "Accuse the outer clerk out loud, wring a confession from him before witnesses.":
            $ case2_confront_choice = "accuse"
            $ honor += 2
            $ kaoru_resistance += 1
            show toa angry
            voice "audio/voice/toa_224.mp3"
            toa "You filed the slip and you fed the kiln. Say so now, before Kaoru-sama writes your name next to a burned courier's."

            "Clerk" "I-I only copied what the factor paid me to copy! The Scorpion man swore the dancer's packet would wreck a charter!"

            show kaoru threatening
            voice "audio/voice/kaoru_255.mp3"
            kaoru "Factor. Scorpion. Ash. Fill the gaps between those three, or the kiln does the talking for you."

        "Copy the slip quietly and bait the forger with a second, false packet.":
            $ case2_confront_choice = "trap"
            $ insight += 2
            $ composure += 1
            show toa thinking
            voice "audio/voice/toa_225.mp3"
            toa "I'll draft a decoy charter and leave it where only the thief would dare bite. The real packet's already ash. The trap is whatever they reach for next."

            show kaoru satisfied
            voice "audio/voice/kaoru_256.mp3"
            kaoru "Patient. Vicious, in the right direction. I'll watch the desk myself tonight."

        "Hand it to Kaoru and let him choose who bleeds.":
            $ case2_confront_choice = "defer"
            $ compliance += 1
            $ kaoru_submission += 1
            show toa neutral
            voice "audio/voice/toa_226.mp3"
            toa "Your house, your clerk, your seal forged twice over. I put the slip in your hand and I wait."

            if kaoru_submission >= 3:
                show kaoru charm
                voice "audio/voice/kaoru_257.mp3"
                kaoru "You're learning. The clerk's sweating precisely because you didn't shout. Quiet frightens him more."

            else:
                show kaoru commanding
                voice "audio/voice/kaoru_258.mp3"
                kaoru "Wise. The clerk talks to me alone. You'll stand there and learn exactly what betrayal in an office sounds like."

    jump case2_milestone_end

label case2_milestone_end:

    scene bg magistrate_office with dissolve
    play music audio.bgm_office fadein 2.0 loop volume 0.52
    show kaoru smirk at left
    show toa determined at right

    play sound audio.paper_shuffle volume 0.4
    voice "audio/voice/narrator_234.mp3"
    "By afternoon the clerk has given up a warehouse foreman, the foreman has given up the Chrysanthemum factor's cousin, and the cousin has slipped out with the tide. Not before Kaoru inks a duplicate Crane charter on emergency authority, though."

    voice "audio/voice/kaoru_259.mp3"
    kaoru "The Academy gets proof you're still alive, still employed, and still a nuisance. That buys you the season."

    voice "audio/voice/toa_227.mp3"
    toa "Tsubaki deserved better than ash. I'll keep his name even if the watch won't."

    if case2_confront_choice == "accuse":
        show kaoru cold
        voice "audio/voice/kaoru_260.mp3"
        kaoru "You burned a clerk's cover in the open. Effective. Expensive, too. The office will chew on it for weeks."

    elif case2_confront_choice == "trap":
        show kaoru amused
        voice "audio/voice/kaoru_261.mp3"
        kaoru "Your decoy snared a rat. And the rat leads us straight back to the Chrysanthemum's ledger. Case One's flower isn't done blooming."

    if live_in_companion:
        show kaoru charm
        voice "audio/voice/kaoru_262.mp3"
        kaoru "Tonight, you sleep. Tomorrow Case Three arrives whether we invite it or not."

        show toa happy
        voice "audio/voice/toa_228.mp3"
        toa "A charter that survived the fire, and a night to actually sleep. I'll take it."

    show toa determined
    voice "audio/voice/toa_229.mp3"
    toa "Case Two, closed. The city still lies, but my name gets to stay in Ryoko Owari a little longer."

    $ case2_milestone = "case2_closed"
    $ case2_closed = True

    jump case2_post_case2_bridge

label case2_post_case2_bridge:
    # Evening festival first, then dawn tea (case2_festival.rpy → case2_romance_morning).

    if case2_festival_eligible() and not case2_festival_seen:
        jump case2_festival_interlude

    if canon_romance_eligible() and not case2_romance_seen:
        jump case2_romance_morning

    if case2_closed and not case3_closed:
        jump case3_investigation_start

    return
