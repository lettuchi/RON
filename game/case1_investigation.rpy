# Case 1, Investigation opening (canal body, noble quarter).
# Entry: case1_investigation_hook / case1_noncanon_start → case1_investigation_start.

label case1_investigation_start:

    $ case1_victim_name = ""
    $ case1_observation = ""
    $ case1_physical_clue = ""
    $ case1_briefing_choice = ""
    $ case1_probe_response = ""
    $ case1_clue_found = False

    if not live_in_companion:
        jump case1_investigation_noncanon_bridge

    # --- Canon: returns from archive with Case One docket ---
    scene bg corridor with fade
    play music audio.bgm_corridor fadein 2.0 loop volume 0.58
    play sound audio.footsteps_corridor volume 0.5

    voice "audio/voice/narrator_060.mp3"
    "The stair behind the inner screen swallows every footfall. Dust has crept into Toa's hakama, and the ledger under her arm smells of river damp and ink old enough to flake."

    voice "audio/voice/toa_102.mp3"
    toa "Case One. No bells on me, obijime still dry, and I never let go of the ledger. Small victories, for once."

    voice "audio/voice/narrator_061.mp3"
    "Lantern light finds her at the top step. The noble quarter corridor seems to narrow the moment she sees a magistrate standing in it, already waiting."

    show toa determined at right with dissolve
    show kaoru smirk at left with dissolve

    voice "audio/voice/kaoru_118.mp3"
    kaoru "You took long enough. Set the docket on my desk and try not to breathe on the wax seals."

    play sound audio.paper_shuffle volume 0.55
    voice "audio/voice/toa_103.mp3"
    toa "You said archive dust was acceptable. I assume my breathing counts too."

    jump case1_investigation_assign

label case1_investigation_noncanon_bridge:

    scene bg corridor with fade
    play music audio.bgm_corridor fadein 2.0 loop volume 0.58
    play sound audio.footsteps_corridor volume 0.5

    show toa neutral at right with dissolve
    show kaoru cold at left with dissolve

    voice "audio/voice/narrator_271.mp3"
    "She climbs back from the archive with the canal docket hugged to her chest. No adjoining chamber waits beside his office, only four more files stacked behind Case One, and a season to prove she belongs to any of them."

    voice "audio/voice/toa_104.mp3"
    toa "Docket retrieved. Still breathing."

    voice "audio/voice/kaoru_333.mp3"
    kaoru "Still insolent. Desk. Case One first. The other four will find you if you don't flee to the curry shops first."

    jump case1_investigation_assign

label case1_investigation_assign:

    scene bg magistrate_office with dissolve
    play music audio.bgm_office fadein 1.8 loop volume 0.6
    show kaoru commanding at left
    show toa determined at right

    voice "audio/voice/narrator_063.mp3"
    "Kaoru breaks the outer seal. Inside: watch reports, a charcoal sketch of the recovery site, and a name line left blank until someone puts a face to the dead."

    if live_in_companion:
        show toa worried
        voice "audio/voice/toa_278.mp3"
        toa "I unpacked for patronage. You're handing me a corpse."

        show kaoru commanding
        voice "audio/voice/kaoru_330.mp3"
        kaoru "Patronage keeps you in my corridor. Case One opens on my desk, first of five you'll witness before the season turns."
    else:
        show toa determined
        voice "audio/voice/toa_280.mp3"
        toa "Witness attachment. Five files. You never led with that number."

        show kaoru smirk
        voice "audio/voice/kaoru_334.mp3"
        kaoru "You wanted the hall. Case One opens first. Four more follow if you don't bore me or bolt for the curry shops."

    voice "audio/voice/kaoru_120.mp3"
    kaoru "Case One. A body in the canal at first light. Noble quarter, where the water runs clean enough to mirror gold leaf."

    voice "audio/voice/kaoru_121.mp3"
    kaoru "The watch writes drowning whenever the name line stays empty. You'll learn which boxes they'll sign, and which they won't."

    show toa thinking
    voice "audio/voice/toa_105.mp3"
    toa "Clean water, dirty ledger. Who pulled him out?"

    show kaoru smirk
    voice "audio/voice/kaoru_122.mp3"
    kaoru "Night watch. Fishermen who swore they saw nothing. And the Scorpion quarter upstream pretends the current runs backward."

    voice "audio/voice/narrator_064.mp3"
    "He taps the sketch: a narrow cut between warehouses, rope marks scored into the stone, no blood in the water worth mentioning."

    voice "audio/voice/kaoru_123.mp3"
    kaoru "The victim wears Miya colors under a borrowed haori. Retainer's knot. Someone wanted him found. Someone else wanted him lost."

    show toa worried
    voice "audio/voice/toa_106.mp3"
    toa "A Miya retainer in the canal. That makes it Crane politics, and Crane politics always finds your desk, Magistrate-sama."

    if live_in_companion:
        show kaoru cruel
        voice "audio/voice/kaoru_124.mp3"
        kaoru "Which is exactly why you sleep in the room beside my office. Discretion isn't decoration."

        if companion_accept_tone == "negotiate":
            show toa determined
            voice "audio/voice/toa_107.mp3"
            toa "Escort to the canal. Written terms. I'm here to collect."

            show kaoru amused
            voice "audio/voice/kaoru_125.mp3"
            kaoru "You'll collect at the waterline. First."
    else:
        show kaoru cold
        voice "audio/voice/kaoru_126.mp3"
        kaoru "Which is why you're not sleeping in my hall yet. Prove you can witness a thing without selling it to the curry shops."

        if unless_branch == "walk_out":
            show toa angry
            voice "audio/voice/toa_108.mp3"
            toa "I came back. That has to count for something."

            show kaoru cold
            voice "audio/voice/kaoru_127.mp3"
            kaoru "It counts toward the canal. It does not count toward trust."

    voice "audio/voice/narrator_065.mp3"
    "A bag of rice crackers sits on the desk corner. Her indulgence, his allowance."

    show toa happy
    voice "audio/voice/toa_109.mp3"
    toa "Snacks after paperwork. Even for corpses nobody's going to bury."

    show kaoru smirk
    voice "audio/voice/kaoru_128.mp3"
    kaoru "Eat one now. You'll lose your appetite before we reach the water."

    $ show_cg_scene("moment case1_briefing_menu")

    menu case1_briefing_menu:
        "Study the victim summary: the knots, the haori, whatever's missing from the report.":
            $ case1_briefing_choice = "detail"
            $ insight += 2
            $ case1_kaoru_trust += 1
            show toa thinking
            voice "audio/voice/toa_110.mp3"
            toa "Retainer's knot, tied left-handed. Haori two sizes too wide, borrowed. No wallet, no letter case."

            show kaoru satisfied
            voice "audio/voice/kaoru_129.mp3"
            kaoru "Good. The watch wrote drowning and missed half of what you just said."

            voice "audio/voice/narrator_066.mp3"
            "In the margin, a clerk noted the fingernails: scrubbed clean the night before. Labor without the honest dirt that should come with it."

        "Ask Kaoru who profits when a Miya retainer turns up dead in Scorpion water.":
            $ case1_briefing_choice = "politics"
            $ honor += 1
            $ insight += 1
            $ case1_kaoru_trust += 1
            show toa determined
            voice "audio/voice/toa_111.mp3"
            toa "So who profits when a Crane thread snaps in Scorpion current?"

            show kaoru thinking
            voice "audio/voice/kaoru_130.mp3"
            kaoru "Poppy resin. Marriage contracts. Anyone in this city who sells silence by the barrel."

            show kaoru commanding
            voice "audio/voice/kaoru_131.mp3"
            kaoru "You will not say any of that aloud at the canal. Watch faces instead."

        "Stay professional: witness notes only, no theories yet.":
            $ case1_briefing_choice = "professional"
            $ composure += 2
            $ compliance += 1
            show toa neutral
            voice "audio/voice/toa_112.mp3"
            toa "Witness notes only: recovery time, position, clothing, visible wounds. Theories can wait."

            if live_in_companion:
                show kaoru satisfied
                voice "audio/voice/kaoru_132.mp3"
                kaoru "Good. Notes I can file without crossing out half your adjectives."
            else:
                show kaoru smirk
                voice "audio/voice/kaoru_133.mp3"
                kaoru "Try keeping that posture once the smell reaches you."

    jump case1_investigation_departure

label case1_investigation_departure:

    scene bg magistrate_hall with dissolve
    play music audio.bgm_street fadein 2.5 loop volume 0.55
    show toa determined at right
    show kaoru commanding at left

    voice "audio/voice/narrator_067.mp3"
    "They leave through the inner hall, not the public corridor where Toa once wandered lost. Guards nod to Kaoru. They look straight through Toa, like furniture that learned to walk."

    voice "audio/voice/toa_113.mp3"
    toa "Furniture with legs still memorizes the route."

    voice "audio/voice/kaoru_134.mp3"
    kaoru "See that you do. Night calls won't wait for someone to light the lanterns."

    scene bg street_exterior with dissolve
    play sound audio.footsteps_corridor volume 0.4

    voice "audio/voice/narrator_068.mp3"
    "Ryoko Owari wakes around them: cart wheels, a shamisen somewhere distant, sweet smoke from a vial house two alleys over. The canal cut is still half a district off."

    voice "audio/voice/kaoru_135.mp3"
    kaoru "Watch the eaves. Thieves in the noble quarter work for employers, not hunger."

    show toa worried
    voice "audio/voice/toa_114.mp3"
    toa "And the wrongness in the air? Thin, like someone peeled a ward off the wall and left bare paper behind."

    show kaoru cold
    voice "audio/voice/kaoru_136.mp3"
    kaoru "Wrong-colored water usually means a clerk poured something upstream. Check the eaves before you blame charms."

    voice "audio/voice/narrator_069.mp3"
    "A crow watches from a warehouse sign, three painted eyes that aren't quite Imperial and aren't quite Scorpion. It takes wing the instant Kaoru glances up."

    jump case1_investigation_canal

label case1_investigation_canal:

    scene bg street_exterior with dissolve
    play music audio.bgm_case1_barge fadein 1.0 loop volume 0.5

    voice "audio/voice/narrator_070.mp3"
    "The canal runs black-green under morning cloud, greener than honest water, as if someone dissolved a charm and tipped the dregs downstream. Rope burns scar the stone where watchmen hauled the body up."

    show kaoru commanding at left
    show toa worried at right

    voice "audio/voice/narrator_071.mp3"
    "No crowd. Only a clerk with a wax tablet, and a Miya envoy pretending to read the warehouse sign so he won't have to look at the pallet."

    voice "audio/voice/kaoru_137.mp3"
    kaoru "Kakita. Stand where I point you, and don't touch the water."

    voice "audio/voice/toa_115.mp3"
    toa "Point, then. I'll witness."

    play music audio.bgm_kaoru_theme fadein 1.5 loop volume 0.52

    voice "audio/voice/narrator_072.mp3"
    "The covered pallet lies at the canal's lip, cloth still damp. When the clerk folds back the sheet, a young man's face shows, peaceful in entirely the wrong way, as if his sleep had been negotiated rather than earned."

    show toa sad
    voice "audio/voice/toa_116.mp3"
    toa "He looks borrowed, even now."

    show kaoru cold
    voice "audio/voice/kaoru_138.mp3"
    kaoru "Identification first. Gossip a distant second. Mourning never."

    "Clerk" "Magistrate. The watch reports drowning. No weapon. The haori's listed as found separate, snagged upstream."

    show toa thinking
    voice "audio/voice/toa_117.mp3"
    toa "Haori upstream, body down here. Current, or carriage?"

    show kaoru smirk
    voice "audio/voice/kaoru_139.mp3"
    kaoru "Ask the river once you're qualified to. Until then, observe."

    $ show_cg_scene("moment case1_canal_menu")

    menu case1_canal_menu:
        "Read the hands and sleeves: labor, ink, or court.":
            $ insight += 2
            $ case1_kaoru_trust += 1
            show toa thinking
            voice "audio/voice/toa_118.mp3"
            toa "Palms soft until yesterday, ink on the index finger. Ledger work. Sleeve hem eaten by canal slime from upstream, not from here."

            show kaoru satisfied
            voice "audio/voice/kaoru_140.mp3"
            kaoru "Which means he died somewhere else, then was dressed for display."

            $ case1_observation = "ink_and_hem"

        "Ask Kaoru why the watch said drowning when the throat tells another story.":
            $ kaoru_resistance += 1
            $ insight += 1
            show toa angry
            voice "audio/voice/toa_119.mp3"
            toa "Magistrate-sama, the bruising on his throat is shaped like fingers, not water."

            show kaoru cruel
            voice "audio/voice/kaoru_141.mp3"
            kaoru "Because drowning keeps the taxes calm. You'll learn when to write only what the city can swallow."

            show kaoru commanding
            voice "audio/voice/kaoru_142.mp3"
            kaoru "And when to make me swallow the harder truth instead. Not today."

            $ case1_observation = "throat_bruise"

        "Stay professional: record only what the watch will sign.":
            $ composure += 2
            $ honor += 1
            show toa neutral
            voice "audio/voice/toa_120.mp3"
            toa "Witness note: recovery at canal mark three, noble quarter. Clothing as listed. Cause of death pending magistrate review."

            show kaoru smirk
            voice "audio/voice/kaoru_143.mp3"
            kaoru "Boring. Useful. The clerk can sign that without fainting."

            $ case1_observation = "signed_minimum"

    show kaoru commanding
    voice "audio/voice/kaoru_151.mp3"
    kaoru "Summarize it. One sentence. If I say your words back to the Crane envoy, does he flinch or laugh?"

    $ show_cg_scene("moment case1_kaoru_probe_menu")

    menu case1_kaoru_probe_menu:
        "Answer eagerly: give him the theory he's fishing for.":
            $ case1_probe_response = "eager"
            $ insight += 1
            $ performance_boldness += 1
            if live_in_companion:
                $ case1_kaoru_trust += 1
            show toa determined
            voice "audio/voice/toa_124.mp3"
            toa "Dressed for display after he died. Borrowed haori, wrong water. A message meant for Crane eyes."

            if live_in_companion:
                show kaoru satisfied
                voice "audio/voice/kaoru_152.mp3"
                kaoru "Good. You sound like you belong in my hall, the moment you stop performing for corpses."

            else:
                show kaoru amused
                voice "audio/voice/kaoru_153.mp3"
                kaoru "Bold. Don't mistake my attention for approval."

        "Defer: witness first, theories only when he asks twice.":
            $ case1_probe_response = "defer"
            $ composure += 2
            $ compliance += 1
            $ case1_kaoru_trust += 2
            show toa neutral
            voice "audio/voice/toa_125.mp3"
            toa "Recovery at mark three. Clothing as listed. Cause of death pending your review, Magistrate-sama."

            show kaoru smirk
            voice "audio/voice/kaoru_154.mp3"
            kaoru "Safe. The envoy won't laugh. He won't fear you either."

        "Push back: he brought you here to learn, not to be humiliated.":
            $ case1_probe_response = "pushback"
            $ honor += 1
            $ kaoru_resistance += 1
            show toa angry
            voice "audio/voice/toa_126.mp3"
            toa "You asked me to observe. I did. If you wanted theater, you should have left the bells on me in the archive."

            if live_in_companion:
                show kaoru hungry
                voice "audio/voice/kaoru_155.mp3"
                kaoru "There she is. Keep that spine when the Miya registry clerks start smiling at you."

            else:
                show kaoru cold
                voice "audio/voice/kaoru_156.mp3"
                kaoru "A witness without a seal is gossip. Learn faster."

        "Push him too far: dare him to punish you in his office.":
            $ case1_probe_response = "defiance"
            $ kaoru_resistance += 2
            $ case1_punishment_entry = "canal"
            jump case1_punishment_bridge

    voice "audio/voice/narrator_073.mp3"
    "Near the rope post, something lacquered catches lantern glare, wedged in the seam where oil and wrong-colored water meet."

    show toa surprised
    voice "audio/voice/toa_121.mp3"
    toa "A comb. Scorpion mon inlaid. Not Miya."

    show kaoru thinking
    voice "audio/voice/kaoru_144.mp3"
    kaoru "Don't touch it with bare hands."

    play sound audio.paper_shuffle volume 0.45
    voice "audio/voice/narrator_074.mp3"
    "He wraps it in wax cloth himself, eyes never leaving the eaves, and hands it to Toa only long enough for her seal on the chain-of-custody line."

    $ case1_physical_clue = "scorpion_comb"
    $ case1_clue_found = True

    if case1_briefing_choice == "politics":
        show kaoru cold
        voice "audio/voice/kaoru_145.mp3"
        kaoru "Scorpion comb in Crane water. Bag it for custody. Don't compose metaphors over my desk."

    elif case1_briefing_choice == "detail":
        show kaoru satisfied
        voice "audio/voice/kaoru_146.mp3"
        kaoru "Borrowed haori, foreign comb. Someone staged a message for Crane eyes. Put a name on that blank line."

    else:
        show kaoru commanding
        voice "audio/voice/kaoru_147.mp3"
        kaoru "The comb goes to the office. The name goes on the line. You walk beside me, not a step ahead."

    play sound audio.paper_shuffle volume 0.5
    voice "audio/voice/narrator_075.mp3"
    "The clerk lifts the separate haori from a dry crate. Wax inside the lining has melted, but the inner fold still holds a courier's chit, half legible under river stain."

    show toa surprised
    voice "audio/voice/toa_127.mp3"
    toa "Miya Jiro. Guest-house ledger clerk. 'Deliver before third bell.' He had an errand the night the canal took him."

    $ case1_victim_name = "Miya Jiro"

    show kaoru thinking
    voice "audio/voice/kaoru_157.mp3"
    kaoru "Jiro handled Crane correspondence for the noble-quarter guest house. Someone killed the clerk and still kept the appointment."

    if case1_probe_response == "eager":
        show kaoru satisfied
        voice "audio/voice/kaoru_158.mp3"
        kaoru "You wanted a theory. Now you've got a face to hang it on. Don't gloat at the envoy."

    elif case1_probe_response == "pushback":
        show kaoru smirk
        voice "audio/voice/kaoru_159.mp3"
        kaoru "Still standing. Still useful. Copy the chit before the ink flakes."

    else:
        show kaoru commanding
        voice "audio/voice/kaoru_160.mp3"
        kaoru "Write it clean. The watch will keep signing drowning until I stop letting them."

    voice "audio/voice/narrator_076.mp3"
    "The Miya envoy finally looks up from the warehouse sign. He sees the chit in Kaoru's hand and suddenly remembers urgent business elsewhere."

    jump case1_investigation_milestone_end

label case1_investigation_milestone_end:

    scene bg magistrate_office with dissolve
    play music audio.bgm_office fadein 2.0 loop volume 0.58
    show kaoru smirk at left
    show toa determined at right

    play sound audio.paper_shuffle volume 0.45
    voice "audio/voice/narrator_077.mp3"
    "Back among cedar and ink, the Scorpion comb sits in a lacquer tray like a poisonous jewel. Beside it, Kaoru inks {i}Miya Jiro{/i} onto the line the watch left blank."

    voice "audio/voice/kaoru_148.mp3"
    kaoru "Tomorrow we cross the Miya guest registry against Scorpion shipping rolls. One of them flinches the moment Jiro's name is said aloud."

    show toa thinking
    voice "audio/voice/toa_122.mp3"
    toa "Guest-house clerk, Crane thread, Scorpion comb. None of this washed up by accident. Someone arranged the whole tableau."

    if case1_clue_found and case1_victim_name:
        show toa determined
        voice "audio/voice/toa_128.mp3"
        toa "And that comb did not slip off a careless man into a canal. A comb that fine is kept, not lost. Someone carried it to the water, the killer or the dead man, and I mean to learn which."

    if live_in_companion:
        show kaoru charm
        voice "audio/voice/kaoru_149.mp3"
        kaoru "Eat. Then copy the watch testimony twice: once for the Empire, once for what I actually believe happened."

    else:
        show kaoru cruel
        voice "audio/voice/kaoru_150.mp3"
        kaoru "Eat, if you must. Then copy the testimony twice. You read the water faster than my clerks did tonight. Do not let that go to your head before you have earned the rest of the season."

    show toa determined
    voice "audio/voice/toa_123.mp3"
    toa "Case One has a face now. Jiro. I won't forget him."

    $ case1_milestone = "miya_guest_registry_next"

    jump case1_registry_start

# ============================================================================
# Case 1, Continuation (day two): Miya guest registry / licensed quarter.
# Entry: case1_investigation_milestone_end → case1_registry_start.
# Follows the scorpion comb to the Lacquered Plum guest house, identifies the
# Scorpion "Chrysanthemum" patron, uncovers a forged Emerald writ, and lands on
# the high-tide barge cliffhanger (case1_milestone = "chrysanthemum_barge_next").
# VOICED: registry through barge (toa_339+, kaoru_450+); see case1_investigation_main_voice_ids.txt.
# ============================================================================

label case1_registry_start:

    scene bg magistrate_office with dissolve
    play music audio.bgm_office fadein 1.8 loop volume 0.58
    show kaoru commanding at left
    show toa determined at right

    play sound audio.paper_shuffle volume 0.45
    voice "audio/voice/narrator_078.mp3"
    "Morning again, and the docket has grown teeth overnight. Beside Jiro's name Kaoru pinned a second sheet: the Miya guest house, the Lacquered Plum, where a dead clerk once kept other men's appointments."

    show kaoru smirk
    kaoru "The Lacquered Plum sits deep in the licensed quarter. The okami answers to coin, not the watch. Bring my seal."

    show toa thinking
    voice "audio/voice/toa_338.mp3"
    toa "A clerk who couldn't even earn a funeral, clerking in a pleasure house."

    show kaoru cold
    voice "audio/voice/kaoru_449.mp3"
    kaoru "The okami won't open her registry for a watchman. She might open it for a magistrate. Give her no reason to lie faster than she already means to."

    if live_in_companion:
        show kaoru commanding
        voice "audio/voice/kaoru_450.mp3"
        kaoru "You walk a half step behind me, and you speak only when I open the door. The quarter swallows companions who forget who lights the lanterns."

        if companion_accept_tone == "negotiate":
            show toa determined
            voice "audio/voice/toa_339.mp3"
            toa "Half a step. The written terms said escort, not muzzle."

            show kaoru amused
            voice "audio/voice/kaoru_451.mp3"
            kaoru "In the Plum, the muzzle and the escort are the same thing. Stay where I can see you."

        elif companion_accept_tone == "gush":
            show toa happy
            voice "audio/voice/toa_340.mp3"
            toa "Half a step behind the most feared man in the noble quarter. I think I can live with that."

            show kaoru charm
            voice "audio/voice/kaoru_452.mp3"
            kaoru "Flatter the okami like that and she'll tip her whole ledger into your lap."
    else:
        show kaoru cold
        voice "audio/voice/kaoru_453.mp3"
        kaoru "You're not my hand yet. In the Plum you're a witness I tolerate. Try tolerating me back."

        show toa neutral
        voice "audio/voice/toa_341.mp3"
        toa "Tolerance, then. It's somewhere to start."

    show toa thinking
    voice "audio/voice/toa_342.mp3"
    toa "Snacks after paperwork. Does the Lacquered Plum count as paperwork, or as the field?"

    show kaoru smirk
    voice "audio/voice/kaoru_454.mp3"
    kaoru "It counts as a hunt. Now decide how we knock."

    $ show_cg_scene("moment case1_registry_menu")

    menu case1_registry_menu:
        "Arrive as the Emerald's hand: custody seal and comb in plain sight.":
            $ case1_registry_approach = "credentials"
            $ honor += 1
            $ composure += 1
            show toa determined
            voice "audio/voice/toa_325.mp3"
            toa "Then we arrive the way the law arrives. Seal out, comb wrapped, nothing hidden. Let the okami count what we already hold."

            show kaoru satisfied
            voice "audio/voice/kaoru_434.mp3"
            kaoru "Seal on the desk, comb in plain cloth. Crude, but the Plum opens for whatever it can see."

        "Suggest the side door: geisha talk to dancers, never to magistrates.":
            $ case1_registry_approach = "quiet"
            $ insight += 2
            $ performance_boldness += 1
            $ case1_kaoru_trust += 1
            show toa happy
            voice "audio/voice/toa_326.mp3"
            toa "Send me in through the kitchen first. I spent three years smiling at tired women in painted rooms. They'll tell a dancer what they'd never tell your seal."

            show kaoru thinking
            voice "audio/voice/kaoru_435.mp3"
            kaoru "Your past, turned into a bargaining chip. I dislike how useful it keeps being."

            show kaoru amused
            voice "audio/voice/kaoru_436.mp3"
            kaoru "Go in soft. I'll follow once the room is warm. Don't enjoy it more than the case."

        "Defer: let Kaoru lead, and watch the room.":
            $ case1_registry_approach = "kaoru_lead"
            $ composure += 2
            $ compliance += 1
            $ kaoru_submission += 1
            show toa neutral
            voice "audio/voice/toa_327.mp3"
            toa "You knock. I'll read the faces behind you. Safer for everyone that way."

            show kaoru commanding
            voice "audio/voice/kaoru_437.mp3"
            kaoru "Finally. Stand where I point. Breathe when I allow it. The Plum mistakes quiet witnesses for furniture, so use that."

    jump case1_guest_house

label case1_guest_house:

    scene bg licensed_quarter with fade
    play music audio.bgm_street fadein 2.0 loop volume 0.5

    voice "audio/voice/narrator_079.mp3"
    "Rain reaches the licensed quarter first. It beads on paper lanterns the color of old wine and runs the canal black between teahouses that sell forgetting by the hour."

    voice "audio/voice/narrator_080.mp3"
    "The Lacquered Plum leans over the water on cedar stilts. A three-eyed crow, the same painted sign or a cousin of it, watches from the gable. This time it does not fly."

    show kaoru cold at left
    show toa worried at right

    voice "audio/voice/toa_343.mp3"
    toa "The air's thin again. Peeled-charm thin. Someone scrubbed protection off this doorway and never bothered to replace it."

    show kaoru cold
    voice "audio/voice/kaoru_455.mp3"
    kaoru "Or never wanted one. The Plum prefers guests unwatched by anything that reports upward."

    play sound audio.sliding_door_open volume 0.7
    scene bg guest_house_room with dissolve
    show kaoru commanding at left
    show toa determined at right

    voice "audio/voice/narrator_081.mp3"
    "Inside: lamplight and face powder. The okami kneels behind a low desk stacked with appointment books, smile fixed hard as lacquer, eyes already tallying the cost of a magistrate's boots on her tatami."

    "Okami" "Magistrate-sama honors the Plum. We are a respectable house. We keep no quarrels, and fewer corpses."

    show kaoru smirk
    voice "audio/voice/kaoru_456.mp3"
    kaoru "And yet you kept Miya Jiro. He clerked your registry until the canal kept him instead. I want the book he wrote in."

    "Okami" "Jiro drowned. A sad, ordinary thing. Drunk boys and high water. The river writes that same story every season."

    if case1_registry_approach == "credentials":
        play sound audio.paper_shuffle volume 0.45
        voice "audio/voice/narrator_082.mp3"
        "Kaoru sets the wax-wrapped comb on the desk and folds the cloth back. The okami's painted calm cracks, just a hairline."

        show kaoru cold
        kaoru "Drowned men don't carry Scorpion combs into Crane water. Open the registry, or I open every book in this house in front of your patrons."

        "Okami" "...The registry is the magistrate's, of course. I only keep it for him."

    elif case1_registry_approach == "quiet":
        voice "audio/voice/narrator_083.mp3"
        "But Toa has already slipped past the desk the kitchen way: servant's bow, easy warmth of a woman who carried tea in worse rooms. A young geisha looks up from folding a dead man's spare haori."

        show toa soft
        toa "You knew him. Jiro. I'm not here to turn his name into a scandal. I'm here so the river doesn't get the last word."

    else:
        show kaoru threatening
        voice "audio/voice/kaoru_457.mp3"
        kaoru "Respectable houses survive by knowing which silences cost more than others. This silence will cost you the Plum itself. Choose."

        voice "audio/voice/narrator_084.mp3"
        "The okami's smile finally fails. In the corner a girl, a geisha, young, eyes red-rimmed, flinches under the weight of his voice."

    show toa worried
    toa "There. The one folding his haori like it still matters. She's the one who'll talk, if anyone's earned the right to hear it."

    voice "audio/voice/narrator_085.mp3"
    "The geisha rises. Perhaps nineteen, white makeup cried through at the edges. She bows too low, the way frightened people do once they've already decided to be brave."

    "Suzu" "I'm Suzu. Jiro brought me persimmons on the nights the patrons were cruel. He didn't drown, Magistrate-sama. He was afraid for a whole week before the canal took him."

    $ case1_witness_name = "Suzu"

    show kaoru thinking
    voice "audio/voice/kaoru_458.mp3"
    kaoru "Afraid of what?"

    "Suzu" "A guest. One who books the river room under a flower name and tips in foreign coin. Jiro carried letters into that room and came back grey."

    play sound audio.paper_shuffle volume 0.4
    voice "audio/voice/narrator_086.mp3"
    "Kaoru tilts the wrapped comb toward the lamp. Suzu goes the color of her own face powder."

    show toa surprised
    toa "Suzu. You know this comb."

    "Suzu" "It's his. The flower-name guest. He left it in the river room a month ago and threatened to flay the maid who'd dared touch it. Scorpion mon, three lacquer scales. I'd know it in the dark."

    show kaoru cold
    voice "audio/voice/kaoru_459.mp3"
    kaoru "A flower alias, foreign silver, frightened clerks. Suzu's mouth next, before the okami buys her silence back."

    show kaoru commanding
    voice "audio/voice/kaoru_460.mp3"
    kaoru "She's a frightened girl with one true thing left in her mouth. Get it out before her courage spends itself. How?"

    $ show_cg_scene("moment case1_witness_menu")

    menu case1_witness_menu:
        "Go gentle: kneel to her level, dancer to dancer, and let her set the pace.":
            $ insight += 2
            $ honor += 1
            $ case1_kaoru_trust += 2
            show toa soft
            voice "audio/voice/toa_328.mp3"
            toa "Suzu. Sit. Breathe. You're not betraying him by saying it. You're the only funeral he's ever going to get."

            if case1_registry_approach == "quiet":
                voice "audio/voice/narrator_087.mp3"
                "She's already decided Toa is safe. The kitchen bow bought what no seal could. Her words come in a rush, like water finding the crack it wanted."

                "Suzu" "They call him the Chrysanthemum. The river room is always his on high-tide nights. Jiro read his letters before he carried them, found a barge manifest that named the wrong cargo, and meant to take it to a magistrate he trusted. Then the tide came in."
            else:
                voice "audio/voice/narrator_088.mp3"
                "She watches Toa's hands, not her face. Slowly, fear loosens its knot."

                "Suzu" "They call him the Chrysanthemum. He keeps the river room on high-tide nights. Jiro read his letters before carrying them, and one of them held a barge manifest that named the wrong cargo. He meant to tell someone with a seal. He never got the chance."

        "Press her on the bruises: show her you already know he was strangled." if case1_observation == "throat_bruise":
            $ insight += 1
            $ composure += 1
            show toa determined
            voice "audio/voice/toa_329.mp3"
            toa "Suzu, the river didn't take Jiro. Fingers did. I saw the marks myself, dark as plum skin under his jaw. You saw them too. Didn't you."

            voice "audio/voice/narrator_089.mp3"
            "The girl's hand flies to her own throat. The gesture answers before her voice can."

            "Suzu" "He had the same marks two nights before he died. A warning, he called it, from the Chrysanthemum's man. He said next time the hand wouldn't stop. I begged him to run. He said clerks who run leave their families to pay off the manifest."

            show kaoru thinking
            voice "audio/voice/kaoru_438.mp3"
            kaoru "A manifest worth a man's throat. Twice over."

        "Let Kaoru loom: silence as a blade, and let it cut.":
            $ composure += 1
            $ compliance += 1
            $ kaoru_submission += 1
            show kaoru threatening
            voice "audio/voice/narrator_090.mp3"
            "Kaoru says nothing. He simply waits, and the room shrinks around his stillness until the okami's powder runs and Suzu's resolve breaks, all under a magistrate who hasn't yet bothered to threaten her."

            "Suzu" "The Chrysanthemum. The river room. High tide. Jiro found a barge manifest tucked in his letters, the wrong cargo named, and meant to carry it to someone with a seal. Please. That's everything I know."

            show toa worried
            voice "audio/voice/toa_330.mp3"
            toa "She gave that to fear, not to us. Remember that before you call it a victory."

            show kaoru cold
            voice "audio/voice/kaoru_439.mp3"
            kaoru "She'll talk while she's frightened. Ask now, before the okami buys her courage back."

    show toa determined
    voice "audio/voice/toa_338.mp3"
    toa "A flower-named Scorpion, a barge carrying a lying manifest, and a clerk who tried to do the honorable thing. That tells me whose comb rode the canal, too. A man who would flay a maid for touching it does not lose it. Jiro took it from the river room as proof of who he carried letters for, and died with it on him. He had a spine after all."

    show kaoru commanding
    voice "audio/voice/kaoru_449.mp3"
    kaoru "The registry book, okami. The high-tide pages, where the flower signs his name. Now."

    jump case1_interrogation

label case1_interrogation:

    scene bg guest_house_room with dissolve
    play music audio.bgm_kaoru_theme fadein 1.5 loop volume 0.5
    show kaoru commanding at left
    show toa determined at right

    play sound audio.paper_shuffle volume 0.55
    voice "audio/voice/narrator_091.mp3"
    "The okami surrenders the high-tide registry the way a gambler gives up a marked card: slowly, watching the door the whole time. Kaoru turns to the night Jiro died."

    "Okami" "The river room. Reserved, as always, under the Chrysanthemum. Paid a full season ahead. I ask no questions of a guest who pays a season ahead."

    show toa thinking
    voice "audio/voice/toa_344.mp3"
    toa "Booked, paid, private. And here, that's Jiro's hand. The third-bell delivery, signed off the very night he died."

    play sound audio.paper_shuffle volume 0.4
    voice "audio/voice/narrator_092.mp3"
    "The booking is authorized in red: a private-room writ, the kind the licensed quarter demands of the magistracy to seal a room against the watch. The wax bears the Emerald mon."

    if case1_briefing_choice == "detail":
        show toa surprised
        voice "audio/voice/toa_345.mp3"
        toa "Magistrate-sama, look at the seal. This chrysanthemum has sixteen petals. The Emerald office only ever cuts fourteen. The stamp's a forgery. A fine one, but the petal count gives it away."

        show kaoru cold
        voice "audio/voice/kaoru_461.mp3"
        kaoru "Sixteen petals. The forger did not merely counterfeit my office, he reached past it. Sixteen petals is the Emperor's own chrysanthemum. Whoever cut this seal dressed a smuggling cover in the Imperial mon, which makes it treason, and used it to lock a room where a Crane clerk was strangled inside my jurisdiction."
    else:
        show toa surprised
        voice "audio/voice/toa_346.mp3"
        toa "That's your office's mark, isn't it? An Emerald writ, sealing the river room off private the night Jiro died."

        show kaoru cold
        voice "audio/voice/kaoru_462.mp3"
        kaoru "It is my office's mark. It is not my seal. I authorized no writ for this house all season."

        show kaoru thinking
        voice "audio/voice/kaoru_463.mp3"
        kaoru "Which leaves me a forgery, or a thief inside the magistracy. Neither one is a comfort."

    $ case1_forged_seal = True

    show toa thinking
    voice "audio/voice/toa_436.mp3"
    toa "Then he died here, in this room, behind a seal that was never yours, and the tide carried him down to the noble canal where the watch would write drowning. The slime on his sleeve ran the wrong way for a man who fell in downstream. He came from up here, in the licensed quarter, where the water still tastes of the Scorpion piers."

    play sound audio.sliding_door_open volume 0.65
    voice "audio/voice/narrator_093.mp3"
    "The screen slides open without a knock. A man in unmarked grey steps in from the rain, a trade factor by his ink-stained cuffs, Scorpion by the lacquer-scale clasp at his collar, with the easy menace of someone used to buying magistrates by the dozen."

    "Factor" "The Plum's books are the commercial records of a chartered shipping concern. Privileged. You'll hand them to me, Magistrate, and forget the flower growing in them."

    show kaoru threatening
    voice "audio/voice/kaoru_464.mp3"
    kaoru "I am the privilege in this city. Take one step toward that registry, and the watch fishes a second body out of the noble quarter by dawn."

    "Factor" "The watch reports drowning. The watch reports whatever keeps the tax barges moving. You're one seal among many, Kitsu-san."

    show toa angry
    voice "audio/voice/toa_347.mp3"
    toa "One seal stands between you and that book, and yet here you are, come to fetch it yourself. A truly privileged record wouldn't need collecting by a man who tips in foreign silver."

    voice "audio/voice/narrator_094.mp3"
    "The factor's hand drifts toward his sleeve. Kaoru doesn't move at all, and somehow that's worse than if he had."

    show kaoru commanding
    kaoru "The book stays. What we do with the flower's forged writ, that's your choice. Decide it before our guest decides for us."

    $ show_cg_scene("moment case1_ledger_menu")

    menu case1_ledger_menu:
        "Enter the forged seal into evidence aloud: make it a matter of record, here, now, before witnesses.":
            $ case1_ledger_choice = "record"
            $ honor += 2
            $ kaoru_resistance += 1
            show toa determined
            voice "audio/voice/toa_331.mp3"
            toa "Let it be witnessed. A false Emerald seal locked this room the night Miya Jiro was murdered inside it. The okami heard me. The factor heard me. The river does not get this one."

            voice "audio/voice/narrator_095.mp3"
            "The factor's composure thins. A spoken record, in a house full of witnesses, is much harder to drown than a single clerk."

            if case1_briefing_choice == "politics":
                show kaoru cold
                voice "audio/voice/kaoru_440.mp3"
                kaoru "You said it aloud, against my instruction and your own safety both. The Crane envoy won't laugh now. Neither will the Scorpion."
            else:
                show kaoru thinking
                voice "audio/voice/kaoru_441.mp3"
                kaoru "Reckless. Effective. You've put the forgery on the okami's ledger, where no drowning can erase it."

        "Copy it quietly: leave the original, and don't let the forger know we've seen it.":
            $ case1_ledger_choice = "copy"
            $ insight += 2
            $ composure += 1
            show toa thinking
            voice "audio/voice/toa_332.mp3"
            toa "I'll trace the petals onto rice paper and set the book back exactly where it lay. Let whoever cut that false seal sleep easy one more night, just long enough to lead us home."

            show kaoru satisfied
            voice "audio/voice/kaoru_442.mp3"
            kaoru "Patience over theater. The Chrysanthemum keeps his appointment, and we keep the advantage. Good."

        "Hand the writ to Kaoru: ask nothing, and trust the seal standing between you and a knife.":
            $ case1_ledger_choice = "trust"
            $ composure += 1
            $ compliance += 1
            $ kaoru_submission += 1
            $ case1_kaoru_trust += 2
            show toa neutral
            voice "audio/voice/toa_333.mp3"
            toa "It's your mark and your jurisdiction, Magistrate-sama. I'll carry it wherever you point, and save my questions for where the walls don't lean in to listen."

            if kaoru_submission >= 2:
                show kaoru charm
                voice "audio/voice/kaoru_443.mp3"
                kaoru "You're learning the shape of safety at my side. The factor sees it too. Watch him reconsider the door."
            else:
                show kaoru commanding
                voice "audio/voice/kaoru_444.mp3"
                kaoru "Wise. In this quarter, the only seal worth standing behind is the one that frightens factors. Behind me. Now."

    show kaoru threatening
    voice "audio/voice/kaoru_465.mp3"
    kaoru "You came for a book and found a magistrate instead. Tell the Chrysanthemum the Emerald office is missing a seal, and that I've decided to take an interest in flowers."

    voice "audio/voice/narrator_096.mp3"
    "The factor weighs it all: the room, the spoken record, the unmoving magistrate. Then he bows to the exact depth that insults without inviting a blade, and withdraws into the rain."

    "Factor" "High tide waits for no one, Kitsu-san. Neither does the barge."

    play sound audio.sliding_door_close volume 0.6
    voice "audio/voice/narrator_097.mp3"
    "The screen slides shut. Suzu lets out a breath she's held since he entered. The okami has already started deciding which version of tonight she'll sell, and to whom."

    jump case1_registry_milestone_end

label case1_registry_milestone_end:

    scene bg magistrate_office with dissolve
    play music audio.bgm_office fadein 2.0 loop volume 0.56
    show kaoru commanding at left
    show toa determined at right

    play sound audio.paper_shuffle volume 0.45
    voice "audio/voice/narrator_098.mp3"
    "Back among cedar and ink, the case finally has a shape. On the lacquer tray: the Scorpion comb, Suzu's name, and, depending on the night, a forged Emerald writ or its careful copy."

    show kaoru thinking
    kaoru "A barge that names false cargo. A Scorpion who books his rooms under a flower and tips in foreign silver. A clerk who tried to be honest and was strangled for the courtesy."

    show kaoru cold
    voice "audio/voice/kaoru_466.mp3"
    kaoru "And a seal cut to wear my mark, sealing the very room he died in. Someone wants this murder to carry the Emerald crest."

    if case1_milestone == "miya_guest_registry_next":
        show toa thinking
        voice "audio/voice/toa_348.mp3"
        toa "We came for a guest registry and found a forger sitting somewhere inside your own office, Magistrate-sama."

    if live_in_companion:
        play sound audio.cushion_slide volume 0.4
        voice "audio/voice/narrator_099.mp3"
        "He crosses the office and stops too close: practiced proximity of a man who has decided the distance between you is his to set."

        if kaoru_resistance >= 2:
            show kaoru hungry
            voice "audio/voice/kaoru_467.mp3"
            kaoru "You spoke against me twice tonight, and twice you were right. I dislike how much that pleases me. Don't mistake the pleasure for permission."

            show toa determined
            voice "audio/voice/toa_349.mp3"
            toa "Then I'll call it progress, and try not to push my luck."

            show kaoru amused
            voice "audio/voice/kaoru_468.mp3"
            kaoru "Stubborn. Keep it. I'll need something that doesn't bend when this seal turns out to belong to a man I dine with."

        elif kaoru_submission >= 2:
            show kaoru charm
            voice "audio/voice/kaoru_469.mp3"
            kaoru "You stood behind me all night and let the quarter break itself against my stillness. That is exactly what a companion of mine is for."

            show toa soft
            voice "audio/voice/toa_350.mp3"
            toa "Behind you. Watching. And I still saw the petal count before you did, Magistrate-sama."

            show kaoru satisfied
            voice "audio/voice/kaoru_470.mp3"
            kaoru "You did. Obedient and observant both. I'm beginning to think I kept the right dancer."

        else:
            show kaoru commanding
            voice "audio/voice/kaoru_471.mp3"
            kaoru "Someone tried to hang a murder on my seal. Until I know who, you don't leave this compound without me. Not for the curry shops. Not for Academy letters. Nowhere."

            show toa worried
            voice "audio/voice/toa_351.mp3"
            toa "Escort, or cage?"

            show kaoru cold
            voice "audio/voice/kaoru_472.mp3"
            kaoru "Escort means my corridor, my hanko, my release. Tonight you don't leave without all three."
    else:
        show kaoru cold
        voice "audio/voice/kaoru_473.mp3"
        kaoru "You're still not sleeping in my hall. But you spoke for the Empire in a Scorpion house tonight, and the wax never once cracked. I'm noting it."

        show toa determined
        voice "audio/voice/toa_352.mp3"
        toa "And I'll keep noting it right back, until the ledger reads patronage beside my name."

        show kaoru cold
        voice "audio/voice/kaoru_474.mp3"
        kaoru "Survive the Chrysanthemum first. Forgers who cut my seal don't tend to leave their witnesses cheerful."

    show kaoru commanding
    voice "audio/voice/kaoru_475.mp3"
    kaoru "The Scorpion shipping rolls list one barge on the next high tide, booked to the same chartered concern as the river room. The flower will be aboard, or his manifest will. Either way, we meet the tide."

    show toa thinking
    voice "audio/voice/toa_353.mp3"
    toa "A forged seal, a barge, and a flower with a strangler's hand. Jiro pointed us up the current. So we follow it."

    if case1_ledger_choice == "record":
        show toa determined
        voice "audio/voice/toa_354.mp3"
        toa "And it's on the record now. Whoever cut your seal can't drown what a whole house full of witnesses already heard."
    elif case1_ledger_choice == "copy":
        show toa determined
        voice "audio/voice/toa_355.mp3"
        toa "And we copied it quiet. The flower books his room one more high tide, never dreaming we traced his petals."

    show toa determined
    voice "audio/voice/toa_356.mp3"
    toa "Case One has a name, a comb, and a tide now. Jiro pointed us up the current, and I mean to follow it all the way to the flower."

    $ case1_milestone = "chrysanthemum_barge_next"

    if kaoru_resistance >= 3 and case1_probe_response == "pushback":
        menu case1_registry_defiance_menu:
            "Push him too far: make him punish you behind closed screens.":
                $ case1_punishment_entry = "registry"
                jump case1_punishment_bridge

            "The tide won't wait. Keep Case One moving.":
                pass

    if not case1_clue_found or not case1_victim_name:
        menu case1_investigation_fail_menu:
            "Face him empty-handed: you lost the thread.":
                $ case1_punishment_entry = "fail"
                jump case1_punishment_bridge

            "Beg him for one more hour at the canal.":
                $ case1_clue_found = True
                $ case1_victim_name = "Miya Jiro"

    if canon_romance_eligible() and not case1_romance_seen:
        jump case1_romance_router

    jump case1_barge_start

# ============================================================================
# Case 1, Finale: high-tide barge (Chrysanthemum manifest).
# Entry: case1_registry_milestone_end → case1_barge_start.
# ============================================================================

label case1_barge_start:

    scene bg street_exterior with fade
    play music audio.bgm_case1_barge fadein 2.0 loop volume 0.55
    show kaoru commanding at left
    show toa determined at right

    "The noble quarter smells of wet rope and lamp oil. High tide lifts the canal until the warehouses seem to kneel into it, and one low barge, painted Scorpion grey, waits where the factor said it would."

    voice "audio/voice/kaoru_476.mp3"
    kaoru "Chartered concern, false cargo, a flower name on the ledger. Tonight we seize the manifest before the tide signs off on another drowning."

    voice "audio/voice/toa_357.mp3"
    toa "Jiro died for one page in that book. I am not letting the tide take it too."

    if case1_romance_seen and case1_romance_route == "trust":
        $ show_cg_scene("case1_romance_barge_moonlit")
        pause 0.4
        "High tide lifts the gangplank. For one breath he stands close enough that her sleeve catches on his cuff. Then the law remembers its face."

        $ restore_location_sprites("street_exterior", "commanding", "determined")

    if live_in_companion:
        show kaoru cold
        voice "audio/voice/kaoru_477.mp3"
        kaoru "Stay inside my shadow on the plank. One misstep, and the watch writes up two drownings and calls it efficiency."

        if case1_ledger_choice == "record":
            show toa determined
            voice "audio/voice/toa_358.mp3"
            toa "They already heard us at the Plum. The barge crew knows we're coming. Good."

            show kaoru amused
            voice "audio/voice/kaoru_478.mp3"
            kaoru "You turned a forgery into theater. Now go and finish the play."
    else:
        show kaoru threatening
        voice "audio/voice/kaoru_479.mp3"
        kaoru "You wanted a case. This is the part where the city bites back. Try to keep up."

    $ show_cg_scene("moment case1_barge_menu")

    menu case1_barge_menu:
        "Board under cover: slip aboard before the lines are cast off.":
            $ case1_barge_approach = "stealth"
            $ insight += 2
            $ performance_boldness += 1
            show toa thinking
            voice "audio/voice/toa_334.mp3"
            toa "Rain, rope shadows, and a dancer's feet. I'll be on that deck before they finish counting heads."

            show kaoru satisfied
            voice "audio/voice/kaoru_445.mp3"
            kaoru "Theft as a craft. I approve, provided you steal the right ledger page."

        "Board as the law: lantern, seal, and no apologies.":
            $ case1_barge_approach = "official"
            $ honor += 2
            $ composure += 1
            show toa determined
            voice "audio/voice/toa_335.mp3"
            toa "Emerald seal in hand. They can surrender the manifest, or explain it to the Champion's auditors."

            show kaoru commanding
            voice "audio/voice/kaoru_446.mp3"
            kaoru "Loud. Honest. Try not to get yourself shot before I've finished enjoying their faces."

        "Let Kaoru draw their eyes while you take the manifest from the cabin.":
            $ case1_barge_approach = "split"
            $ insight += 1
            $ kaoru_submission += 1
            $ compliance += 1
            show toa neutral
            voice "audio/voice/toa_336.mp3"
            toa "You make the noise. I'll make the copy. That's a division of labor I can trust."

            show kaoru charm
            voice "audio/voice/kaoru_447.mp3"
            kaoru "Finally. A companion who understands spectacle as cover."

        "Board alone: you don't need an escort to steal one page.":
            show toa determined
            voice "audio/voice/toa_337.mp3"
            toa "Watch from the gangplank if you must. The manifest is mine to take."

            show kaoru cold
            voice "audio/voice/kaoru_448.mp3"
            kaoru "Toa. That deck is full of the flower's men, and his hand has already strangled one clerk this season. Step onto it alone and you are the next name the canal swallows. Do not."

            jump gameover_case1_canal

    jump case1_barge_boarding

label case1_barge_boarding:

    scene bg licensed_quarter with dissolve
    play music audio.bgm_kaoru_theme fadein 1.5 loop volume 0.52

    "Lanterns swing on the barge rail. The deckhands freeze. A magistrate on the gangplank is a story that ends in arrests or in bribes, and they haven't yet decided which."

    if case1_barge_approach == "stealth":
        "Toa is already below the awning, fingers on a waxed folio bound with Scorpion cord. The night smells of poppy resin under the honest rice sacks."

        show toa surprised at right
        voice "audio/voice/toa_359.mp3"
        toa "Magistrate-sama, here's the cargo manifest. Rice in the ledger, resin in the barrels. Jiro was right all along."

        show kaoru cold at left
        voice "audio/voice/kaoru_480.mp3"
        kaoru "A falsified cargo tally. Hold onto that page."

    elif case1_barge_approach == "official":
        show kaoru commanding at left
        voice "audio/voice/kaoru_481.mp3"
        kaoru "Open the hold. The Emerald office is auditing chartered lies tonight."

        "A deck boss spits into the canal, then surrenders the folio with both hands raised."

        show toa determined at right
        voice "audio/voice/toa_360.mp3"
        toa "False rice tally, true resin weight. Someone taxed the city on its hunger and smuggled poison on the side."

    else:
        show kaoru threatening at left
        voice "audio/voice/kaoru_482.mp3"
        kaoru "You. The man who threatened my witness. Step into the light."

        "The factor from the Plum stumbles out of the cabin, foreign silver coins spilling from his sleeve."

        show toa determined at right
        "While Kaoru pins the factor with a smile like a drawn blade, Toa lifts the manifest from the table behind him: rice on the paper, resin in the hold."

        voice "audio/voice/toa_361.mp3"
        toa "Got it. Just don't let him swallow the seal this time."

    $ case1_manifest_seized = True

    "Factor" "The Chrysanthemum buys tides, not trials. You have a page. You do not have a name."

    show kaoru cold
    voice "audio/voice/kaoru_483.mp3"
    kaoru "I have enough to hang your chartered concern and every clerk who ever signed for it. Run to your flower. The tide won't hide you twice."

    play sound audio.sliding_door_close volume 0.5
    "He bolts into the warehouse alleys. The deckhands scatter. Only the manifest stays behind, its ink still wet with the lie that killed Jiro."

    jump case1_barge_milestone_end

label case1_barge_milestone_end:

    scene bg magistrate_office with dissolve
    play music audio.bgm_office fadein 2.0 loop volume 0.56
    show kaoru commanding at left
    show toa determined at right

    play sound audio.paper_shuffle volume 0.45
    "Morning after the tide. The Scorpion comb, Suzu's testimony, the forged writ, and the barge manifest share one tray. Case One finally has a spine the watch can't call drowning."

    voice "audio/voice/kaoru_484.mp3"
    kaoru "The Chrysanthemum is still a cipher. The factor's concern is not. I'll burn his charter before the week is out."

    voice "audio/voice/toa_362.mp3"
    toa "Jiro gets his name on the watch ledger now, and a line that says strangled. That's a funeral worth standing in the rain for."

    if case1_ledger_choice == "copy":
        show toa thinking
        voice "audio/voice/toa_363.mp3"
        toa "And we still have the traced petals from the Plum. The flower has more than one trap waiting for him now."

    if live_in_companion:
        show kaoru charm
        voice "audio/voice/kaoru_485.mp3"
        kaoru "Academy letters sat on the outer desk all night. Case Two arrived with the dawn, and it isn't a polite one."

    else:
        show kaoru smirk
        voice "audio/voice/kaoru_486.mp3"
        kaoru "Your permit survives because you survived the tide. Case Two is already on the desk. Try not to expect any gratitude."

    show toa determined
    voice "audio/voice/toa_364.mp3"
    toa "Case One, closed. Then whatever the city decides to throw at us next."

    $ case1_milestone = "case1_closed"
    $ case1_closed = True

    if case1_5_romance_interlude_eligible():
        jump case1_5_romance_interlude

    jump case2_investigation_start
