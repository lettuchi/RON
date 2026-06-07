# Case 4: The dock ledger (剣の帳 / Ledger at the Blade's Edge).
# Entry: case3_post_case3_bridge (after optional Case 3.5) → case4_post_case3_bridge → case4_investigation_start.
# Romance beat: sword crisis, trust Kaoru (case4_kaoru_defended).
# Archived supper vertical slice (宴の呼び声) removed 2026-06-03, see comment block at file end.

label case4_post_case3_bridge:

    if case4_closed:
        return

    scene bg magistrate_office with dissolve
    play music audio.bgm_office fadein 1.5 loop volume 0.48
    show kaoru commanding at left
    show toa work determined at right

    voice "audio/voice/narrator_260.mp3"
    "The fabric-shop clerk's runner never made it to the canal office. A dock watchman swears the man bolted for the lower piers with Case Three's night ledger under his arm, the grey wax on its cord still wet."

    voice "audio/voice/kaoru_302.mp3"
    kaoru "Case Four is where the paper trail runs out and the steel begins. We raid the lower dock tonight. Bring me Kurogane, or bring me his blood."

    voice "audio/voice/toa_261.mp3"
    toa "Magistrate-sama, I'm a witness. Not a yoriki."

    show kaoru cold
    voice "audio/voice/kaoru_303.mp3"
    kaoru "Tonight you are both. Stay in my line, or the file learns that you didn't."

    jump case4_investigation_start


label case4_investigation_start:

    if case4_closed:
        return

    $ case4_started = True
    $ case4_investigation_choice = ""
    $ case4_suspect_named = False
    $ case4_suspect_name = ""

    scene bg magistrate_office with fade
    play music audio.bgm_office fadein 2.0 loop volume 0.52
    show kaoru commanding at left
    show toa determined at right

    voice "audio/voice/narrator_261.mp3"
    "Rain hammers the compound before dawn. Case Three's custody chit is barely dry when Kaoru pins a dock watchman's note beside the bolt-room saw kerf. Lower pier. Warehouse three. A foreman who signs his name in unmarked grey, Scorpion-trained under the lacquer."

    voice "audio/voice/kaoru_304.mp3"
    kaoru "Case Four. Kurogane runs the split crates our clerk ran toward. He learned his trade under a Scorpion quartermaster, so he will not surrender to a brush and ink."

    voice "audio/voice/toa_262.mp3"
    toa "And me? Another bolt room to comb through, or steel this time?"

    show kaoru cold
    voice "audio/voice/kaoru_305.mp3"
    kaoru "Steel. You dance with a blade when I tell you to dance. You do not duel a foreman on your own."

    if live_in_companion and case3_kaoru_rescue:
        show kaoru charm
        voice "audio/voice/kaoru_306.mp3"
        kaoru "You learned how to breathe in my bolt room. Tonight you breathe in my line, or the ledger learns that you couldn't."

        show toa flustered
        voice "audio/voice/toa_263.mp3"
        toa "Magistrate-sama, I am not your decoration."

        show kaoru smirk
        voice "audio/voice/kaoru_307.mp3"
        kaoru "Correct. You are a witness with a wakizashi. Walk like you know the difference."

    jump case4_dock_raid


label case4_dock_raid:

    scene bg dock_raid with fade
    play music audio.bgm_case4_dock fadein 2.0 loop volume 0.55
    show kaoru cold at left
    show toa worried at right

    $ show_cg_scene("case4_gritty_establishing", fade)

    voice "audio/voice/narrator_262.mp3"
    "The lower piers. Tar ropes, split crates, that wrong shade of green breathing off the canal. Lanterns gutter in the rain, and the mouth of the warehouse swallows every sound."

    voice "audio/voice/kaoru_308.mp3"
    kaoru "Three breaths. Read the room. Then we take him."

    $ show_cg_scene("moment case4_investigation_menu")

    menu case4_investigation_menu:
        "Read the split crate. The wax seal, the Scorpion thread.":
            $ case4_investigation_choice = "crate"
            $ insight += 1
            show toa thinking
            voice "audio/voice/toa_264.mp3"
            toa "Grey wax, the sixteen-petal Imperial seal again, the same forger's hand from Case One. He didn't drown with that barge. He just changed warehouses."

            show kaoru satisfied
            voice "audio/voice/kaoru_309.mp3"
            kaoru "Note that down before the steel starts talking."

        "Question the watchman who signed the night manifest.":
            $ case4_investigation_choice = "watchman"
            $ composure += 1
            $ honor += 1
            $ case4_suspect_named = True
            $ case4_suspect_name = "Kurogane"
            show toa neutral
            voice "audio/voice/toa_265.mp3"
            toa "Foreman Kurogane. Scorpion pay, Crane crates for cover. He bolted the moment the clerk did."

            show kaoru commanding
            voice "audio/voice/kaoru_310.mp3"
            kaoru "Good. Say his name again when his blade clears the sheath."

        "Cover the stairs and defer to Kaoru's line.":
            $ case4_investigation_choice = "stairs"
            $ compliance += 1
            $ kaoru_submission += 1
            show toa determined
            voice "audio/voice/toa_266.mp3"
            toa "The stairs are mine. You take the floor. I won't break formation."

            show kaoru smirk
            voice "audio/voice/kaoru_311.mp3"
            kaoru "Discipline, with the steel this close. I will take it."

    jump case4_confrontation_kurogane


label case4_confrontation_kurogane:

    scene bg dock_raid with dissolve
    play music audio.bgm_case4_dock fadein 0.5 loop volume 0.6
    show kaoru commanding at left
    show toa determined at right

    if not case4_suspect_named:
        voice "audio/voice/kaoru_312.mp3"
        kaoru "Kurogane! Emerald custody. Lower your blade, or lower your head."

        $ case4_suspect_named = True
        $ case4_suspect_name = "Kurogane"
    else:
        voice "audio/voice/kaoru_313.mp3"
        kaoru "[case4_suspect_name]! Emerald custody. Lower your blade, or lower your head."

    voice "audio/voice/narrator_263.mp3"
    "A foreman steps out of the crate shadow, katana already drawn, rain streaming off shoulders the Scorpion trained. He does not bow."

    "Kurogane" "The magistrate's pet and his little dancer. So the clerk talked. I am not walking to the pleasure quarter in chains."

    show toa angry
    voice "audio/voice/toa_267.mp3"
    toa "Then talk to my witness note. After you sheathe that blade."

    "Kurogane" "Witnesses die quiet in Ryoko Owari."

    jump case4_swordfight


label case4_swordfight:

    $ show_cg_scene("case4_fight_wide", fade)
    play music audio.bgm_case4_dock fadein 0.3 loop volume 0.7

    voice "audio/voice/narrator_264.mp3"
    "Three blades in the rain. Kaoru's katana carves a clean arc, Toa's wakizashi rides her dance-line, and Kurogane's Scorpion cut keeps trying to split them apart. Crate wood splinters. The footing underneath is blood-slick tar."

    voice "audio/voice/kaoru_314.mp3"
    kaoru "Toa! Hold the line!"

    voice "audio/voice/narrator_265.mp3"
    "Kurogane feints high, then drops low, his steel angled for her ribs instead of his. One breath to choose. Crane footwork, or the magistrate's shadow."

    $ show_cg_scene("moment case4_swordfight_crisis_menu")

    menu case4_swordfight_crisis_menu:
        "\"Stay behind me, Magistrate-sama.\"":
            jump case4_romance_kaoru_defends

        "\"I will cut him down myself.\"":
            jump case4_bad_end_toa_slain_warning


label case4_romance_kaoru_defends:

    $ case4_kaoru_defended = True

    play sound audio.footsteps_corridor volume 0.8
    voice "audio/voice/narrator_266.mp3"
    "She drops back a single step, but not into his shadow. Her wakizashi rides the dance-line up and turns the foreman's low cut a hand's width wide, just long enough. Kaoru crosses into the opening she bought him, and his coat takes the edge that would have opened her ribs."

    $ show_cg_scene("case4_romance_defend", fade)
    play music audio.bgm_canon_intimate fadein 2.0 loop volume 0.45

    voice "audio/voice/narrator_267.mp3"
    "Steel screams once. Kurogane stumbles into the custody rope, not into mercy. Kaoru's sleeve is dark with rain, or with something worse, and still his free hand finds her wrist and pins her behind his shoulder."

    show kaoru cold at left
    show toa flustered at right

    voice "audio/voice/kaoru_315.mp3"
    kaoru "Breathe. Count to three. That deflection was clean. The Academy would not believe me if I filed it honestly."

    voice "audio/voice/toa_268.mp3"
    toa "I bought you one breath and you spent it shielding me. We could have both stood, Magistrate-sama."

    show kaoru cold
    voice "audio/voice/kaoru_567.mp3"
    kaoru "We held the line together. That is new, and I find I do not hate it. Do not let it go to your head before the stitches are even in."

    voice "audio/voice/narrator_440.mp3"
    "His grip does not loosen. Grey eyes on hers, too honest, and this time he does not reach for a witness-note to hide behind."

    voice "audio/voice/kaoru_316.mp3"
    kaoru "If you had died on my dock, I would have burned this whole pier down to the canal. I am not going to pretend I did not say it this time."

    show toa soft
    voice "audio/voice/toa_257.mp3"
    toa "Magistrate-sama..."

    show kaoru cold
    voice "audio/voice/kaoru_568.mp3"
    kaoru "Witness note: foreman detained, ledger seized, and my witness turned the cut that should have killed her. Write that line first. We will argue about the rest behind my screen, not on a wet dock."

    jump case4_milestone_end


label case4_bad_end_toa_slain_warning:

    scene bg dock_raid with dissolve
    show toa determined at center

    voice "audio/voice/narrator_228.mp3"
    "She lunges. Pride, Crane training, the need to prove the Academy still owns her footwork. But Kurogane's cut is not a performance. It is a dockman's arithmetic."

    centered "{size=-2}This ending is tragic. Implied death, artistic fallen CG, no graphic gore.{/size}"

    menu case4_slayn_warning_menu:
        "Continue.":
            pass

        "Return to title.":
            stop music fadeout 1.5
            return

    jump case4_bad_end_toa_slain


label case4_bad_end_toa_slain:

    $ case4_toa_slain = True
    jump gameover_case4_slayn


label case4_milestone_end:

    scene bg magistrate_office with dissolve
    play music audio.bgm_office fadein 2.0 loop volume 0.5
    show kaoru commanding at left
    show toa determined at right

    play sound audio.paper_shuffle volume 0.4
    voice "audio/voice/narrator_268.mp3"
    "By dawn the foreman's manifest sits in custody beside Case Three's saw kerf. The clerk's runner has not vanished, only gone quiet, and in Ryoko Owari that quiet is its own kind of confession."

    "Case Four put steel on the dock where Case Three put silk. The seized manifest and sixteen-petal wax now sit beside Jiro's file, waiting for a hearing bold enough to read them aloud."

    voice "audio/voice/kaoru_318.mp3"
    kaoru "Case Four is pinned, not closed. The flower still has its roots."

    if case4_kaoru_defended:
        show kaoru charm
        voice "audio/voice/kaoru_319.mp3"
        kaoru "You stayed in my line when the steel wanted you alone. Do not expect applause. Expect a pleasure-quarter seal stolen by morning."

        show toa flustered
        voice "audio/voice/toa_270.mp3"
        toa "I stayed because the file said witness. Not because..."

        show kaoru smirk
        voice "audio/voice/kaoru_320.mp3"
        kaoru "Because is a word for Case Five. Tonight you sleep."

    show toa determined
    voice "audio/voice/toa_271.mp3"
    toa "Case Four's line is on the tray with the rest. Four files witnessed, one hearing left. The city still lies, but I am still at your door."

    $ case4_closed = True

    jump case4_post_case4_bridge


label case4_post_case4_bridge:

    if case4_5_boat_interlude_eligible():
        jump case4_5_boat_interlude

    jump case5_investigation_start


# --- ARCHIVED: canal supper vertical slice (宴の呼び声), moved out of canon order 2026-06-03.
# Was: case4_canal_supper, case4_table_menu, case4_bad_end_abandon → gameover_case4_abandon.
# Romance table beat replaced by case4_romance_kaoru_defends (dock swordfight).
