# Case 1.5 — 「台所の印」 / Kitchen Seal (romance interlude; not a numbered case file).
# Entry: case1_barge_milestone_end when case1_5_romance_interlude_eligible().
# Exit: case2_investigation_start.
# VOICED: narrator_297-306, kaoru_374-386, toa_308-318 (no toa_312; see manifests).

label case1_5_romance_interlude:

    scene black with fade
    play music audio.bgm_office fadein 2.5 loop volume 0.32

    voice "audio/voice/narrator_297.mp3"
    "Case One has its spine on the tray now, though this part never gets a number. Call it the kitchen seal. It is the first night she slept on the far side of his screen, and the midday she tried to cook her gratitude straight into a pot."

    jump case1_5_chamber_flashback


label case1_5_chamber_flashback:

    voice "audio/voice/narrator_298.mp3"
    "It is the first night after she moved into the adjoining chamber. The terms are the same ones from the companion menu. Past the inner screen, down the left corridor, and do not, under any circumstances, rearrange his shelves."

    $ show_cg_scene("case1_5_chamber_corridor", fade)
    pause 2.0

    voice "audio/voice/narrator_299.mp3"
    "Paper keeps rustling on his side of the shoji. She lies there counting ceiling beams instead of sheep, and somewhere past the magistrate wing a night clerk stamps a form she will never get to read."

    voice "audio/voice/toa_308.mp3"
    toa "If you are awake over there, you are doing a terrible job of hiding it. The whole city can hear you pacing."

    voice "audio/voice/kaoru_374.mp3"
    kaoru "Counting is witness work. Stop filing ceiling beams and sleep."

    voice "audio/voice/toa_309.mp3"
    toa "I brought you tea. I know you did not ask for any."

    $ show_cg_scene("case1_5_chamber_shoji_tea", fade)
    pause 2.0

    $ set_expression("kaoru", "cold")
    voice "audio/voice/kaoru_375.mp3"
    kaoru "I did not ask for a chambermate either, and yet here you are. Drink before it goes cold. I am not thanking you for tea I did not request."

    voice "audio/voice/toa_310.mp3"
    toa "You still have not said thank you, you know."

    $ set_expression("kaoru", "smirk")
    voice "audio/voice/kaoru_376.mp3"
    kaoru "Thank you would admit I wanted the company. I wanted a body in my corridor who could read a ledger without fainting. Different line item."

    voice "audio/voice/narrator_300.mp3"
    "The footsteps stop. Fabric whispers in the dark. A quilt lands on her side of the screen, heavy wool, unmistakably his, smelling of cedar, ink, and the sleep he will never admit to losing. Paper keeps rustling on his side anyway, as if some sealed bundle on the outer desk were already listening."

    $ show_cg_scene("case1_5_chamber_quilt", fade)
    pause 2.0

    voice "audio/voice/kaoru_377.mp3"
    kaoru "The corridor is still mine. The blanket is only a loan against your noise. Snore, and I reassign you to the archive."

    voice "audio/voice/toa_311.mp3"
    toa "Then I will file my breathing under acceptable noise. Good night, Magistrate-sama."

    $ set_expression("kaoru", "charm")
    voice "audio/voice/kaoru_378.mp3"
    kaoru "Good night, To-chan. Case One starts at dawn. Be vertical. Scheduling, not romance."

    jump case1_5_shoji_night


label case1_5_shoji_night:

    scene black with fade
    pause 0.4

    voice "audio/voice/narrator_304.mp3"
    "The wing goes quiet. Then paper scratches on his side of the shoji, deliberate, filing the dark. Rice paper tears once, not theater. Warm breath ghosts through the gap before she has counted another beam."

    $ show_cg_scene("case1_5_shoji_wrist", fade)
    pause 2.0

    voice "audio/voice/kaoru_384.mp3"
    kaoru "Do not perform stillness at me, To-chan. I have read quieter ledgers than the one your body is keeping tonight."

    voice "audio/voice/toa_318.mp3"
    toa "Magistrate-sama, the archive will hear you."

    voice "audio/voice/kaoru_385.mp3"
    kaoru "The archive sleeps. You do not. Hands on the post. Do not leave a mark I cannot explain."

    voice "audio/voice/narrator_305.mp3"
    "Tan fingers close on her pale wrist through the torn panel. Shallow light, shallow depth. Her sob against the grain is evidence he catalogs without sharing her name with any clerk who sells courage by the cup."

    $ show_cg_scene("case1_5_shoji_tear", fade)
    pause 2.0

    voice "audio/voice/kaoru_386.mp3"
    kaoru "Quiet. Take what I give you from behind the screen and do not drip on my tatami. I know what I am paying for."

    voice "audio/voice/narrator_306.mp3"
    "When it ends she does not perform purity. She crawls back to her futon with his blanket over her shoulders and something private cooling between her thighs, a sealed bundle of letters glaring from the outer desk like a runner who already knows too much."

    scene black with fade
    pause 0.5

    jump case1_5_curry_kitchen


label case1_5_curry_kitchen:

    scene bg magistrate_office with dissolve
    play music audio.bgm_office fadein 2.0 loop volume 0.4
    show kaoru commanding at left
    show toa happy at right

    voice "audio/voice/narrator_301.mp3"
    "Midday after the barge, with Case Two's letters still waiting unopened on the outer desk. The magistrate wing kitchen smells of curry roux and a little guilt."

    voice "audio/voice/toa_313.mp3"
    toa "Case One is closed, and you survived a whole tray of my handwriting. So today I am cooking you thank-you curry, not filing a report about it."

    show kaoru amused
    voice "audio/voice/kaoru_379.mp3"
    kaoru "The kitchen is not a courtroom, To-chan. Neither is the lid of that pot."

    show toa surprised
    voice "audio/voice/toa_314.mp3"
    toa "I was only lining up the seal. A proper hanko makes everything official, does it not?"

    $ show_cg_scene("case1_5_hanko_pot", fade)
    pause 2.0

    show kaoru cold
    voice "audio/voice/kaoru_380.mp3"
    kaoru "Official lentils are still lentils. Put my chop on paper, not on my dinner. I am not signing your gratitude into the pot lid."

    $ show_cg_scene("case1_5_curry_kitchen", fade)
    pause 2.0

    $ show_cg_scene("case1_5_kaoru_curry_bowl", fade)
    pause 2.0

    voice "audio/voice/narrator_302.mp3"
    "He eats without praise and without flinching, as though his jurisdiction now extends to broth."

    $ set_expression("kaoru", "satisfied")
    voice "audio/voice/kaoru_381.mp3"
    kaoru "Edible. More than I can say for the Academy letters out on the desk. Case Two has been waiting there since this morning."

    $ set_expression("toa", "determined")
    voice "audio/voice/toa_315.mp3"
    toa "Then they can keep waiting until I have washed the pot. You did finish the whole bowl, I noticed."

    $ set_expression("kaoru", "smirk")
    voice "audio/voice/kaoru_382.mp3"
    kaoru "I ate the proof that you follow instructions when you are not stamping dinner. Do not expect a second serving or a softer inventory."

    $ show_cg_scene("case1_5_dawn_desk_duo", fade)
    pause 2.0

    voice "audio/voice/narrator_303.mp3"
    "No new case number lands on her desk. Only the steam, and the seal tucked back into his sleeve where it belongs."

    voice "audio/voice/toa_316.mp3"
    toa "Kitchen seal noted, then. Case Two is next, and I am still right here at your door."

    $ set_expression("kaoru", "charm")
    voice "audio/voice/kaoru_383.mp3"
    kaoru "And you are still in my corridor. That is filing enough for one afternoon. Try not to walk like a woman carrying a secret she forgot to seal."

    voice "audio/voice/toa_317.mp3"
    toa "Filed. And I promise I will not stamp the ladle again."

    $ case1_5_romance_seen = True

    jump case2_investigation_start
