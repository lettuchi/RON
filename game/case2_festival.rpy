# Case 2, post-close festival interlude (hill, fireworks, kiss).
# Entry: case2_post_case2_bridge after case2_milestone_end; morning tea follows this beat.
# Eligibility: canon_first_scene + live_in_companion (see case2_festival_eligible).

label case2_festival_interlude:

    $ case2_festival_seen = True

    scene bg street_exterior with fade
    play music audio.bgm_case2_festival fadein 2.0 loop volume 0.48
    show kaoru charm at left
    show toa happy at right

    voice "audio/voice/narrator_235.mp3"
    "The duplicate charter is barely cool when Kaoru locks the inner screen and slides a festival sash across the desk toward her. Not court dress. Not witness black. Borrowed color, just for the night."

    voice "audio/voice/kaoru_263.mp3"
    kaoru "The outer clerk can guard ash until dawn. You're coming to the hill festival with me. Call it a field inspection of morale."

    voice "audio/voice/toa_230.mp3"
    toa "Magistrate-sama, Case Two only just closed. The watch will talk if I go parading about in a gold obi."

    show kaoru smirk
    voice "audio/voice/kaoru_264.mp3"
    kaoru "The watch files whatever I sign. Tonight I'm signing nothing but your attendance. Bring an appetite. The curry stall by the lower bridge owes me a debt."

    show toa flustered
    voice "audio/voice/toa_231.mp3"
    toa "You say inspection. You mean you want me somewhere with lanterns instead of ledgers, where you can keep an eye on me."

    show kaoru satisfied
    voice "audio/voice/kaoru_265.mp3"
    kaoru "Correct. Now walk with me, To-chan. The lanterns will not wait."

    scene black with fade
    pause 0.5

    voice "audio/voice/narrator_236.mp3"
    "They slip out by the service stair. No hanko, no escort line. They climb the lantern road until the canal city spills out below them like a tray of scattered coins."

    $ show_cg_scene("case2_festival_hill", fade)
    play music audio.bgm_canon_intimate fadein 2.5 loop volume 0.5

    voice "audio/voice/narrator_237.mp3"
    "A wooden bench on the overlook faces the whole of Ryoko Owari: paper rivers winding between warehouses, drumbeats thin as a pulse, smoke from the food stalls threading up through the eaves."

    show kaoru charm at left
    show toa soft at right

    voice "audio/voice/kaoru_266.mp3"
    kaoru "Sit. The hill is mine, by tax map and by habit both. No clerk will come petitioning you up here."

    voice "audio/voice/toa_232.mp3"
    toa "The whole city's lit up. I never knew it could look... kind."

    show kaoru thinking
    voice "audio/voice/kaoru_267.mp3"
    kaoru "Kind is what merchants sell when the ledger stays honest for a single night. Enjoy the lie. It's cheaper than virtue."

    show toa happy
    voice "audio/voice/toa_233.mp3"
    toa "Then lie with me until the third bell. I've earned one night that doesn't stink of ash."

    show kaoru charm
    voice "audio/voice/kaoru_268.mp3"
    kaoru "One night. I know how carefully you count."

    $ show_cg_scene("case2_festival_fireworks", fade)

    voice "audio/voice/narrator_238.mp3"
    "Fireworks climb over the canal for the chrysanthemum festival. Chrysanthemum bursts, then falling embers that drown in the water, wrong-green and lovely. The first real chill of autumn has come off the water tonight. Toa flinches at the first crack. Kaoru's hand finds her wrist, steady, proprietary."

    show toa flustered
    voice "audio/voice/toa_234.mp3"
    toa "Magistrate-sama, everyone down there is watching the sky."

    show kaoru hungry
    voice "audio/voice/kaoru_269.mp3"
    kaoru "Let them have the sky. I'm watching you remember you're still alive after all that ash."

    voice "audio/voice/narrator_239.mp3"
    "The next volley paints her white lashes gold. He doesn't let go."

    $ show_cg_scene("case2_festival_kiss", fade)

    voice "audio/voice/narrator_240.mp3"
    "He kisses her there on the bench. No performance, no ink, just his mouth warm against hers while the fireworks stutter overhead and the city pretends it's innocent."

    menu case2_festival_kiss_menu:
        "Let the kiss be enough for one night.":
            $ case2_festival_kiss_only = True
            jump case2_festival_kiss_only_beat

        "Ask him for more than just a festival kiss.":
            jump case2_festival_go_further


label case2_festival_kiss_only_beat:

    show kaoru smirk at left
    show toa soft at right

    voice "audio/voice/kaoru_270.mp3"
    kaoru "Enough. Don't go filing that under promises."

    show kaoru cold
    voice "audio/voice/kaoru_271.mp3"
    kaoru "A festival kiss is paper confetti. Pretty, public, worthless by the morning docket. Don't read my mouth like it's a charter."

    show toa flustered
    voice "audio/voice/toa_235.mp3"
    toa "I wasn't. I only meant..."

    show kaoru commanding
    voice "audio/voice/kaoru_272.mp3"
    kaoru "Good. Then we go down before the watch invents a rumor worth selling."

    show toa neutral
    voice "audio/voice/narrator_241.mp3"
    "Her smile stays right where he can see it. Underneath, something dull settles in. Not heartbreak, not yet anything with a name, just the ache of wanting his nod to mean more than patronage."

    voice "audio/voice/toa_236.mp3"
    toa "Of course, Magistrate-sama. The hill gave me more than enough."

    show kaoru charm
    voice "audio/voice/kaoru_273.mp3"
    kaoru "Walk. Curry before curfew. Case Three won't wait just because you blushed on a bench."

    call case2_festival_curry_cg
    jump case2_festival_bridge


label case2_festival_go_further:

    $ case2_festival_intimate = True

    show toa flustered
    voice "audio/voice/toa_237.mp3"
    toa "Magistrate-sama, not here. Not with the whole city staring up at us."

    show kaoru hungry
    voice "audio/voice/kaoru_274.mp3"
    kaoru "Then choose a door I already hold. Guest room on the way down. One screen, one lock, my corridor."

    show toa soft
    voice "audio/voice/toa_238.mp3"
    toa "One lock. And your hanko stays tucked in your sleeve."

    show kaoru satisfied
    voice "audio/voice/kaoru_275.mp3"
    kaoru "A dangerous request, from my companion. I'll allow it until the wax cools."

    scene black with fade
    pause 0.9

    $ show_cg_scene("case2_festival_intimate", fade)

    voice "audio/voice/narrator_242.mp3"
    "The breath of the shoji, the grain of lantern light. Clothed silhouettes first, then the whisper of fabric. Implied, never filed, satisfaction with no ledger line to its name."

    pause 0.8

    voice "audio/voice/narrator_243.mp3"
    "By the time they dress, the fireworks have thinned to ash on the water. Her obi sits straight again. His cuff is still warm."

    show kaoru charm at left
    show toa happy at right

    voice "audio/voice/kaoru_276.mp3"
    kaoru "Don't thank me with poetry. Feed yourself before Case Three drags you back to witness notes."

    voice "audio/voice/toa_239.mp3"
    toa "I already ate. Don't fuss over me."

    show toa soft
    voice "audio/voice/toa_240.mp3"
    toa "...Thank you for the hill, though. Even if the city pretends none of it happened."

    show kaoru smirk
    voice "audio/voice/kaoru_277.mp3"
    kaoru "The city pretends every single night. I remember what I pay for."

    call case2_festival_curry_cg
    jump case2_festival_bridge


label case2_festival_curry_cg:

    $ show_cg_scene("case2_festival_curry_stall", fade)
    pause 2.0
    $ set_expression("kaoru", "amused")
    $ set_expression("toa", "happy")
    return


label case2_festival_bridge:

    scene bg street_exterior with dissolve
    play music audio.bgm_street fadein 2.0 loop volume 0.42
    show kaoru commanding at left
    show toa determined at right

    voice "audio/voice/narrator_244.mp3"
    "Lanterns gutter along the descent. Somewhere below, a clerk is already stacking the first paper of Case Three. A name, a seal, a lie dressed up as courtesy."

    voice "audio/voice/kaoru_278.mp3"
    kaoru "Sleep while you can. The next file won't smell of fireworks."

    voice "audio/voice/toa_241.mp3"
    toa "Then I'll dream of ash that didn't win for once. Case Three can wait until morning tea."

    show kaoru cold
    voice "audio/voice/kaoru_279.mp3"
    kaoru "It won't wait. Neither will I. When it knocks, you answer it beside me."

    if canon_romance_eligible() and not case2_romance_seen:
        jump case2_romance_morning

    if case2_closed and not case3_closed:
        jump case3_investigation_start

    return
