# Case 1 & 2: canon romance interludes and bad endings.
# Romance requires: canon_first_scene, live_in_companion, kaoru_submission >= 2.
# Case 1 romance routes: trust (case1_kaoru_trust >= 4) or sponsorship (flirt / gush / flirtatious style).
# Bad ends are opt-in menu choices (case1_kaoru_probe_menu, case1_registry_defiance_menu, case1_barge_menu).

default seen_gameover_case1 = False
default seen_gameover_case2 = False
default seen_gameover_case3 = False
default seen_gameover_case4 = False
default seen_gameover_case4_5 = False
default seen_gameover_case5 = False
default seen_gameover_case1_punishment = False
default case1_romance_seen = False
default case1_5_romance_seen = False
default case2_romance_seen = False

# --- Bad-end CGs ---
image cg gameover_case1_canal = At("images/cg/cg-case1-bad-canal.png", fit_cg)
image cg gameover_case2_exile = At("images/cg/cg-case2-bad-exile.png", fit_cg)
image cg gameover_case3_injury = At("images/cg/cg-case3-bad-injury.png", fit_cg)

# --- Canon romance CGs (Case 2; Case 1 defs in cgs-case1.rpy) ---
image cg case2_romance_morning = At("images/cg/cg-case2-romance-morning.png", fit_cg)


init python:
    def canon_romance_eligible():
        # Canon live-in romance. An assertively-played Toa who pushed back instead of
        # yielding still qualifies: either she leaned in (kaoru_submission) or she held
        # her own and he respected it (kaoru_resistance). The romance must not silently
        # write out a defiant Toa who still chose the corridor.
        return (
            store.canon_first_scene
            and store.live_in_companion
            and (store.kaoru_submission >= 2 or store.kaoru_resistance >= 2)
        )

    def case1_5_romance_interlude_eligible():
        return (
            canon_romance_eligible()
            and store.live_in_companion
            and store.case1_closed
            and store.case1_romance_seen
            and not store.case1_5_romance_seen
            and not store.seen_gameover_case1
        )

    def case2_festival_eligible():
        return store.canon_first_scene and store.live_in_companion

    def case1_trust_route():
        return store.case1_kaoru_trust >= 4

    def case1_sponsorship_route():
        return (
            store.case1_sponsorship_flirt
            or store.companion_accept_tone == "gush"
            or (
                store.performance_style == "flirtatious"
                and store.performance_boldness >= 1
            )
        )

    def romance_through_case3_complete():
        # Cases 1 to 3 canon romance in one playthrough (gates Case 3.5 date interlude).
        return (
            canon_romance_eligible()
            and store.case1_romance_seen
            and store.case2_festival_seen
            and store.case2_romance_seen
            and store.case3_kaoru_rescue
            and not store.case3_bad_end_injury
        )

    def all_romance_routes_complete():
        # Full canon romance through Case 4 dock defend (post-game extras if needed).
        return (
            romance_through_case3_complete()
            and store.case4_kaoru_defended
            and not store.case4_toa_slain
            and not store.case4_bad_end_abandoned
        )

    def case3_5_date_interlude_eligible():
        return romance_through_case3_complete() and not store.case4_date_interlude_seen

    def case4_date_interlude_eligible():
        return case3_5_date_interlude_eligible()

    def case4_5_boat_interlude_eligible():
        return (
            all_romance_routes_complete()
            and store.case4_closed
            and store.case4_kaoru_defended
            and not store.case4_5_boat_interlude_seen
            and not store.case4_toa_slain
            and not store.case4_bad_end_abandoned
            and not store.case3_bad_end_injury
            and not store.case4_5_bad_end_boat_injury
        )

    def case5_investigation_eligible():
        return all_romance_routes_complete() and not store.case5_closed

    def epilogue_romance_bonus_eligible():
        return (
            all_romance_routes_complete()
            and store.case5_yoriki_accepted
            and store.case5_closed
            and not store.case5_yoriki_refused
            and not store.case5_romance_bonus_seen
            and not store.case3_bad_end_injury
            and not store.case4_toa_slain
            and not store.case4_5_bad_end_boat_injury
        )


label case1_romance_router:
    # After Lacquered Plum, before high-tide barge (canon companion route).
    if not canon_romance_eligible() or case1_romance_seen:
        jump case1_barge_start

    if case1_trust_route():
        $ case1_romance_route = "trust"
        jump case1_romance_route_trust

    if case1_sponsorship_route():
        $ case1_romance_route = "sponsorship"
        jump case1_romance_route_sponsorship

    jump case1_romance_interlude


label case1_romance_route_trust:
    # Route A: investigation bond: canal lantern walk, then office almost-touch.
    $ case1_romance_seen = True

    scene bg street_exterior with fade
    play music audio.bgm_canon_intimate fadein 2.5 loop volume 0.5
    show kaoru charm at left
    show toa soft at right

    "Rain has thinned. The canal path back to the compound runs under paper lanterns, amber on black water, the same wrong-green she smelled at Jiro's recovery site."

    kaoru "You read Suzu without breaking her. You read the forged petals before I finished my sentence. That is trust, and trust is rarer than obedience in this hall."

    toa "Magistrate-sama, Case One isn't finished."

    show kaoru satisfied
    kaoru "Case One will still be there when you stop pretending the tide is the only clock that matters."

    $ show_cg_scene("case1_romance_canal_lantern", fade)

    "He walks a half step beside her, not ahead, close enough that her sleeve brushes his cuff when the wind shifts. No seal, no witness, only lantern stripes on the canal."

    show toa flustered
    toa "If the watch sees..."

    kaoru "The watch files what I sign. Tonight I sign nothing. Walk."

    scene bg magistrate_office with dissolve
    play music audio.bgm_canon_intimate fadein 1.5 loop volume 0.48
    show kaoru charm at left
    show toa flustered at right

    "The inner screen is still locked. Comb and forged writ wait on the tray; he dims the lamps to the same amber as the canal."

    kaoru "You asked me to stay where you could see me. I am not in the habit of granting dangerous requests twice."

    $ show_cg_scene("case1_romance_office_touch", fade)
    play sound audio.cushion_slide volume 0.4

    "His fingers find her knuckle, not a clerk's grip, not a threat. Her breath answers before courtesy remembers to object."

    show toa soft
    toa "Sign nothing tonight. Just, don't send me to the barge alone."

    show kaoru hungry
    kaoru "Dangerous request from my companion. I'll allow it until the wax cools."

    scene black with fade
    pause 0.8

    "What followed stayed off every ledger; implied, never filed. When they dressed, rain had returned, and the barge waited downstream."

    show kaoru smirk at left
    show toa happy at right
    kaoru "Snacks after tides. I expect you fed before the canal tries to drown you."

    toa "I ate already. Don't fuss."

    jump case1_barge_start


label case1_romance_route_sponsorship:
    # Route B, patronage tension (art donor, not danna); Discord sponsorship tone.
    $ case1_romance_seen = True

    scene bg magistrate_office with fade
    play music audio.bgm_canon_intimate fadein 2.0 loop volume 0.52
    show kaoru charm at left
    show toa flustered at right

    "The inner hall is empty. Suzu's fear still clings to Toa's sleeves; Kaoru locks the screen himself."

    kaoru "The tide waits. I don't."

    toa "Magistrate-sama, Case One isn't finished."

    show kaoru hungry
    kaoru "Case One will still be there when the city stops pretending you're only my sponsored dancer."

    show kaoru commanding
    kaoru "I am drafting patronage, not a courtesan's contract. The ledger reads art donor to artist. I know what I am paying for."

    show toa flustered
    toa "Sponsorship. Not, not that."

    show kaoru smirk
    kaoru "Gifts of money to support your expression. You may interpret that liberally, within the residence I set. Twice weekly you attend me here. The rest is written below."

    $ show_cg_scene("case1_romance_sponsorship", fade)

    "He slides the stipend sheet: three koku, board, companion duties, but his thumb stays on her seal line as if the wax were already warm."

    show toa happy
    toa "You enjoy making me blush in the same room where I signed."

    show kaoru satisfied
    kaoru "I enjoy watching you remember who bought the lanterns you're standing under. Perform for me, not the quarter. One breath. No bells."

    show toa soft
    toa "Audience of one, then."

    show kaoru charm
    kaoru "Always one. The barge crew can wait."

    scene black with fade
    pause 0.8

    "What followed stayed off every ledger; implied, never filed. When they dressed, rain had returned, and the barge waited downstream."

    show kaoru smirk at left
    show toa happy at right
    kaoru "Snacks after tides. Don't grin at the clerk."

    toa "I ate already. Don't fuss."

    jump case1_barge_start


label case1_romance_interlude:
    # Default romance beat when eligible but neither route threshold met.
    $ case1_romance_seen = True
    $ case1_romance_route = "default"

    scene bg magistrate_office with fade
    play music audio.bgm_canon_intimate fadein 2.5 loop volume 0.52
    show kaoru charm at left
    show toa flustered at right

    "The inner hall is empty. Suzu's fear still clings to Toa's sleeves; Kaoru locks the screen himself."

    kaoru "The tide waits. I don't."

    toa "Magistrate-sama, Case One isn't finished."

    show kaoru hungry
    kaoru "Case One will still be there when the city stops pretending you're only my sponsored dancer."

    $ show_cg_scene("case1_romance_lantern", fade)
    play sound audio.cushion_slide volume 0.45

    "He dims the lanterns to amber. Her obi loosens; they lean into the same breath until courtesy is only memory, his cruelty softens into something that still takes, but lets her choose the giving."

    show toa soft
    toa "Sign nothing tonight. Just, stay where I can see you."

    show kaoru satisfied
    kaoru "Dangerous request from my companion. I'll allow it until the wax cools."

    scene black with fade
    pause 0.8

    "What followed stayed off every ledger; implied, never filed. When they dressed, rain had returned, and the barge waited downstream."

    show kaoru smirk at left
    show toa happy at right
    kaoru "Snacks after tides, you said. I expect you fed before the canal tries to drown you."

    toa "I ate already. Don't fuss."

    jump case1_barge_start


label case2_romance_morning:
    # After Case Two closes (canon companion route).
    $ case2_romance_seen = True

    scene bg magistrate_office with fade
    play music audio.bgm_canon_intimate fadein 2.0 loop volume 0.48
    show kaoru charm at left
    show toa happy at right

    voice "audio/voice/narrator_245.mp3"
    "Dawn through cedar shutters. Duplicate charter cooling on the desk; tea steaming; the outer clerk already transferred to a cell."

    voice "audio/voice/kaoru_280.mp3"
    kaoru "The Academy thinks you're still respectable. I think you're still mine to complicate."

    voice "audio/voice/toa_242.mp3"
    toa "Respectable until noon, then. The rest of me is already yours."

    $ show_cg_scene("case2_romance_morning", fade)

    voice "audio/voice/narrator_246.mp3"
    "Tea cools untouched on the desk. They stay wrapped in the same cushion warmth instead, his thumb on her knuckle, her forehead against his shoulder, neither willing to break the spell first."

    show toa soft
    voice "audio/voice/toa_243.mp3"
    toa "Tsubaki deserved a better city. I deserved not to lose my future in ash."

    show kaoru charm
    voice "audio/voice/kaoru_281.mp3"
    kaoru "You kept both. That is rarer than virtue here."

    show toa flustered
    voice "audio/voice/toa_244.mp3"
    toa "Don't make me used to mornings that don't hurt."

    show kaoru hungry
    voice "audio/voice/kaoru_282.mp3"
    kaoru "Too late. Case Three will hurt worse. I'll be beside you when it does, if you keep choosing me over the door."

    show toa determined
    voice "audio/voice/toa_245.mp3"
    toa "The door can wait. The tea can't."

    if case2_closed and not case3_closed:
        jump case3_investigation_start

    return


# --- Case 5 bad ends (refusal; implied coercion; CG-held climax) ---

label gameover_case5_chained:
    $ seen_gameover_case5 = True
    stop music fadeout 1.0
    play music audio.bgm_bad_ending fadein 2.0 loop volume 0.55

    $ show_cg_scene("gameover_case5_chained", fade)
    pause 2.0

    voice "audio/voice/narrator_290.mp3"
    "Cedar oil and lantern steam. Iron finds her wrist where Crane footwork never taught her to break a magistrate's grip."

    pause 2.0

    $ set_expression("kaoru", "cold")
    voice "audio/voice/kaoru_368.mp3"
    kaoru "Temporary escort. Left hand filled. Her name stays off my appointment scroll."

    pause 2.0

    $ set_expression("toa", "worried")
    voice "audio/voice/toa_296.mp3"
    toa "Magistrate-sama, please."

    pause 2.0

    voice "audio/voice/narrator_291.mp3"
    "An okami counts coin without looking at her face. Kaoru's footsteps leave before the first lock clicks."

    pause 2.0

    voice "audio/voice/narrator_286.mp3"
    "Chains in a pleasure-quarter back room are still filed under Emerald business when the name on the scroll is not hers."

    pause 2.0

    $ set_expression("kaoru", "cold")
    voice "audio/voice/kaoru_372.mp3"
    kaoru "The quarter keeps what I sell. You keep what you refused to price."

    pause 2.0

    $ set_expression("toa", "soft")
    voice "audio/voice/toa_305.mp3"
    toa "...Not like this..."

    pause 2.0

    voice "audio/voice/narrator_292.mp3"
    "What the quarter collects is not entered where clerks can cite it. Only the ache, if she survives the night."

    pause 2.0

    scene black with fade
    pause 0.6

    centered "{size=+14}Game Over{/size}"
    pause 0.4

    centered "{size=+4}The End{/size}\n{size=-4}Case Five: 「帳の拒絶」\nKakita Toa refused the left hand.{/size}"

    return


label gameover_case5_quarter_cage:
    $ seen_gameover_case5 = True
    stop music fadeout 1.0
    play music audio.bgm_bad_ending fadein 2.0 loop volume 0.55

    $ show_cg_scene("gameover_case5_quarter_cage", fade)
    pause 2.0

    voice "audio/voice/narrator_293.mp3"
    "Stone under the magistrate hall is colder than canal water. Her kosode tears on an iron hinge someone forgot to file as sharp."

    pause 2.0

    voice "audio/voice/narrator_294.mp3"
    "A clerk slides wax paper under the grate. Not the yoriki scroll. A companion chit, quarter escort, temporary, the kind that buys silence."

    pause 2.0

    $ set_expression("kaoru", "cold")
    voice "audio/voice/kaoru_371.mp3"
    kaoru "Thumb here. Or I file you as flight risk and let the runners collect."

    pause 2.0

    $ set_expression("toa", "worried")
    voice "audio/voice/toa_307.mp3"
    toa "I... Magistrate-sama, this is not..."

    pause 2.0

    voice "audio/voice/narrator_295.mp3"
    "His hanko lands while her pride is still screaming. The hall does not echo. It only records."

    pause 2.0

    voice "audio/voice/narrator_287.mp3"
    "Holding cells under the magistrate hall learn a dancer's name the way the canal learns ash, slowly, and without mercy."

    pause 2.0

    $ set_expression("kaoru", "cold")
    voice "audio/voice/kaoru_373.mp3"
    kaoru "Corrective custody closes at dawn. What happens before dawn is hall business."

    pause 2.0

    voice "audio/voice/narrator_296.mp3"
    "The holding cell learns her thumbprint before she learns to stop shaking. No yoriki characters. Only file ink."

    pause 2.0

    scene black with fade
    pause 0.6

    centered "{size=+14}Game Over{/size}"
    pause 0.4

    centered "{size=+4}The End{/size}\n{size=-4}Case Five: 「御前の檻」\nThe hall kept Kakita Toa without the oath.{/size}"

    return


# --- DEV: content warning; implied coercion / violence; fade-to-black only. ---

label case1_punishment_bridge:

    if case1_punishment_entry == "canal":
        show toa angry at right
        show kaoru commanding at left

        voice "audio/voice/toa_272.mp3"
        toa "Then punish me, Magistrate-sama. You have been holding that threat over me since the night I touched the wrong door. So use it."

        show kaoru cold
        voice "audio/voice/kaoru_322.mp3"
        kaoru "You demand my desk in front of a half-drowned clerk and a Miya witness. That was stupid, To-chan. It was also the moment you stopped being anyone else's."

        show toa surprised
        voice "audio/voice/toa_273.mp3"
        toa "I did not mean... I only thought you would never actually..."

        show toa angry
        voice "audio/voice/toa_274.mp3"
        toa "...would never dare. Go on, keep guessing."

        show kaoru cold
        voice "audio/voice/kaoru_323.mp3"
        kaoru "My office. My corridor. We are finished when I say the word, not when your nerve runs out."

        voice "audio/voice/narrator_269.mp3"
        "Rain beads along the canal rope. The clerk keeps his eyes on his wax tablet, learning early how not to see. Kaoru's hand closes on her elbow, an escort's grip and nothing kinder, and the compound takes them both."

    elif case1_punishment_entry == "registry":
        show kaoru cold at left
        show toa angry at right

        voice "audio/voice/kaoru_324.mp3"
        kaoru "You begged for closed screens twice in one night. Congratulations. You will have them."

        voice "audio/voice/toa_275.mp3"
        toa "Behind closed screens. You heard me perfectly well the first time."

        show kaoru cold
        voice "audio/voice/kaoru_325.mp3"
        kaoru "The desk. Now. Before you confuse your appetite for my permission a second time."

    elif case1_punishment_entry == "fail":
        show kaoru cold at left
        show toa worried at right

        voice "audio/voice/kaoru_326.mp3"
        kaoru "An empty witness note. A blank collar line. You have nothing to show me, and you do not get another hour to find it."

        voice "audio/voice/toa_276.mp3"
        toa "Magistrate-sama... let me make one more pass at the canal, please..."

        show kaoru cold
        voice "audio/voice/kaoru_327.mp3"
        kaoru "The desk. You are about to learn what my hall charges a witness who comes back with nothing to sign."

    jump case1_bad_end_kaoru_punishment


label case1_bad_end_kaoru_punishment:
    $ seen_gameover_case1_punishment = True
    stop music fadeout 1.0
    play music audio.bgm_bad_end_punishment fadein 2.0 loop volume 0.52

    scene bg magistrate_office with fade
    show kaoru cold at left
    show toa angry at right

    voice "audio/voice/kaoru_231.mp3"
    kaoru "You wanted theater at the canal. My office is not a stage: it is a desk, a seal, and consequences."

    voice "audio/voice/toa_196.mp3"
    toa "Magistrate-sama, I am your witness, not your..."

    show kaoru cold
    voice "audio/voice/kaoru_230.mp3"
    kaoru "You are one line on my evening's ledger until I say otherwise. Desk. Now."

    $ show_cg_scene("gameover_case1_punishment_desk", fade)

    voice "audio/voice/narrator_189.mp3"
    "Cedar and ink. The docket stack still warm from Case One. His hanko waits beside a narrow custody chit, companion escort, temporary, the kind that buys silence from clerks who learn not to hear."

    play sound audio.chair_creak volume 0.65
    voice "audio/voice/kaoru_229.mp3"
    kaoru "You pushed twice at the waterline and once in my hall. I do not repeat warnings."

    voice "audio/voice/toa_195.mp3"
    toa "Let me through... I'm not..."

    voice "audio/voice/kaoru_228.mp3"
    kaoru "You carried my seal's work into Scorpion water and came back proud. Pride bends here."

    $ show_cg_scene("gameover_case1_punishment_hands")

    voice "audio/voice/narrator_188.mp3"
    "His hand closes on her wrist, not a lover's grip, a magistrate's. Fingers find the pulse the way he finds a misplaced line."

    $ set_expression("toa", "angry")
    voice "audio/voice/toa_194.mp3"
    toa "Let go...!"

    voice "audio/voice/kaoru_227.mp3"
    kaoru "Witness without obedience is gossip. Learn faster."

    $ show_cg_scene("gameover_case1_punishment_floor", fade)

    voice "audio/voice/narrator_187.mp3"
    "The mat rushes up. Paper scatters like startled herons. The permit book skids under the desk where he wanted it in the first place."

    pause 0.5

    $ set_expression("toa", "worried")
    voice "audio/voice/toa_193.mp3"
    toa "...Get up. Crane girls get up."

    voice "audio/voice/narrator_186.mp3"
    "Her arms do not answer. Pride was a costume. Under it she is only breath and bruised obi and the taste of his corridor."

    voice "audio/voice/kaoru_226.mp3"
    kaoru "There. Now you're low enough to hear terms."

    pause 0.4

    centered "{size=-2}This ending is brutal. Implied violence ahead.{/size}"

    menu case1_punishment_warning_menu:
        "Continue.":
            pass

        "Return to title.":
            stop music fadeout 1.5
            return

    window hide
    $ show_cg_scene("gameover_case1_punishment_shoji", fade)

    voice "audio/voice/narrator_185.mp3"
    "The office door seals. Lamplight shrinks to a strip under the shoji."

    voice "audio/voice/narrator_184.mp3"
    "From the hall, clerks hear nothing, or learn to hear nothing. Emerald Magistrate business."

    voice "audio/voice/kaoru_225.mp3"
    kaoru "You'll knock again when hunger wins. Tonight I collect what you owed at the canal."

    $ set_expression("toa", "soft")
    voice "audio/voice/toa_192.mp3"
    toa "..."

    voice "audio/voice/narrator_183.mp3"
    "What happens next is not entered in any clerk's ledger, only in the ache she will carry if she survives the night."

    pause 0.6

    stop music fadeout 3.0
    scene black with fade
    pause 0.6

    centered "{size=+14}Game Over{/size}"
    pause 0.4

    centered "{size=+4}The End{/size}\n{size=-4}Case One: 「執務室の制裁」\nKakita Toa pushed too far.\nKitsu Kaoru closed the screen.{/size}"

    return


label gameover_case1_canal:
    $ seen_gameover_case1 = True
    stop music fadeout 1.0
    play music audio.bgm_bad_ending fadein 2.0 loop volume 0.55

    $ show_cg_scene("gameover_case1_canal", fade)

    voice "audio/voice/narrator_192.mp3"
    "She boards alone, proud, fast, certain the manifest is a prize and not bait."

    voice "audio/voice/narrator_191.mp3"
    "The factor does not run. He smiles, steps from the awning, and the deckhand's pole finds the small of her back."

    voice "audio/voice/narrator_190.mp3"
    "Cold canal. Opium-sweet water. The last thing she sees is Scorpion grey paint bubbling under rain."

    scene black with fade
    pause 0.6

    centered "{size=+14}Game Over{/size}"
    pause 0.4

    centered "{size=+4}The End{/size}\n{size=-4}Case One: 「運河の餌」\nThe canal took Kakita Toa.{/size}"

    return


label gameover_case4_abandon:
    $ seen_gameover_case4 = True
    stop music fadeout 1.0
    play music audio.bgm_bad_ending fadein 2.0 loop volume 0.55

    scene bg street_exterior with fade
    show toa angry at center

    voice "audio/voice/narrator_194.mp3"
    "She walks into the rain, proud, certain the magistrate will call her back before the third bridge."

    voice "audio/voice/narrator_193.mp3"
    "He does not. The factor's runners do. The companion file closes without her signature."

    scene black with fade
    pause 0.6

    centered "{size=+14}Game Over{/size}"
    pause 0.4

    centered "{size=+4}The End{/size}\n{size=-4}Case Four: 「宴の呼び声」\nKakita Toa left the table.{/size}"

    return


label gameover_case4_slayn:
    $ seen_gameover_case4 = True
    stop music fadeout 1.0
    play music audio.bgm_bad_ending fadein 2.0 loop volume 0.55

    $ show_cg_scene("gameover_case4_slayn", fade)

    voice "audio/voice/narrator_196.mp3"
    "She lunges alone, pride, Crane footwork, the wish to prove the Academy still owns her blade."

    voice "audio/voice/narrator_195.mp3"
    "Kurogane's cut is dock work, plain and final, not theater. Rain swallows the pier. The magistrate's file closes without her breath."

    scene black with fade
    pause 0.6

    centered "{size=+14}Game Over{/size}"
    pause 0.4

    centered "{size=+4}The End{/size}\n{size=-4}Case Four: 「剣の果て」\nKakita Toa fell on the lower dock.{/size}"

    return


# --- DEV: content warning: grave injury on kobune throw; hospital implied; no graphic gore. ---

label gameover_case4_5_boat:
    $ seen_gameover_case4_5 = True
    stop music fadeout 1.0
    play music audio.bgm_bad_ending fadein 2.0 loop volume 0.55

    $ show_cg_scene("gameover_case4_5_boat", fade)

    voice "audio/voice/narrator_199.mp3"
    "She fights the throw, Crane pride against a hull built for fishermen. Shoulder and ribs meet the thwart wrong. Breath leaves. The kobune keeps rocking as if it did not witness."

    voice "audio/voice/narrator_198.mp3"
    "Bandages. Rain on shoji. A magistrate's shadow at the marina pilings that does not cross the gunwale, as if grief might be contagious on a ledger."

    voice "audio/voice/narrator_197.mp3"
    "The hospital cart creaks toward the lower quarter. Ryoko Owari keeps its boats. It does not always keep its dancers."

    scene black with fade
    pause 0.6

    centered "{size=+14}Game Over{/size}"
    pause 0.4

    centered "{size=+4}The End{/size}\n{size=-4}Case Four Point Five: 「舟の果て」\nThe kobune deck took Kakita Toa.{/size}"

    return


label gameover_case2_alley:
    $ seen_gameover_case2 = True
    stop music fadeout 1.0
    play music audio.bgm_bad_ending fadein 2.0 loop volume 0.55

    $ show_cg_scene("gameover_case2_exile", fade)

    voice "audio/voice/narrator_205.mp3"
    "She enters the kiln alley ahead of him, ash in her palms, proof in her mouth, pride in her stride."

    voice "audio/voice/narrator_204.mp3"
    "The clerk's knife was not for Kaoru. It was for the dancer who would not let the Academy packet stay dead."

    voice "audio/voice/narrator_203.mp3"
    "Tsubaki's ghost gets company. Toa's charter burns with the rest."

    scene black with fade
    pause 0.6

    centered "{size=+14}Game Over{/size}"
    pause 0.4

    centered "{size=+4}The End{/size}\n{size=-4}Case Two: 「灰の帰路」\nRyoko Owari closed its doors.{/size}"

    return


label gameover_case3_injury:
    $ seen_gameover_case3 = True
    stop music fadeout 1.0
    play music audio.bgm_bad_ending fadein 2.0 loop volume 0.55

    $ show_cg_scene("gameover_case3_injury", fade)

    voice "audio/voice/narrator_202.mp3"
    "The roll catches her shoulder, then the mat, then the world tilts wrong. Crane footwork is not armor against a room built to kill witnesses."

    voice "audio/voice/narrator_201.mp3"
    "Bandages. Rain on shoji. A magistrate's shadow in the doorway that does not cross the threshold, as if grief might be contagious on a ledger."

    voice "audio/voice/narrator_200.mp3"
    "The hospital cart creaks toward the canal quarter. Ryoko Owari keeps its books. It does not always keep its dancers."

    scene black with fade
    pause 0.6

    centered "{size=+14}Game Over{/size}"
    pause 0.4

    centered "{size=+4}The End{/size}\n{size=-4}Case Three: 「絹屋の帳」\nThe bolt room took Kakita Toa.{/size}"

    return
