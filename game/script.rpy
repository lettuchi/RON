# Ryoko Owari Nights, entry point; prologue → Case 1 companion (canon) / investigation stub

label splashscreen:
    scene black with dissolve
    pause 0.6
    centered "{font=fonts/YujiSyuku-Regular.ttf}{size=+4}Ryoko Owari Nights{/size}{/font}\n{size=-6}the city of lies{/size}" with dissolve
    pause 1.2
    return

label start:

    # End the main-menu theme the instant the player commits to Start. The
    # opening plays its own track right after this (and stops music at its own
    # end), so this is a safety net: the menu song never lingers even if the OP
    # is skipped or later removed.
    stop music fadeout 1.0

    # Dev builds: gate before chapter pick (game/dev_chapter_pick.rpy).
    # Disable for release: dev_chapter_pick_enabled = False in dev_chapter_pick.rpy.
    if dev_chapter_pick_enabled:
        scene black with dissolve
        centered "{size=+4}Ryoko Owari Nights{/size}\n{size=-4}Dev build, choose how to start.{/size}"

        menu dev_start_gate_menu:
            "Play from beginning (opening + prologue, no cheat flags)":
                jump dev_play_normal_start

            "Dev chapter pick (jump to a case or bad end)":
                jump dev_chapter_pick_menu

    jump dev_play_normal_start


# Normal new-game flow (also used by dev menu "Play from beginning").
label dev_play_normal_start:

    # Otome opening sequence (game/opening.rpy). Skippable via the usual Ren'Py
    # skip (Ctrl / Tab) or by clicking through; it cleans up and returns here.
    call opening_sequence from _call_opening_sequence

    scene black with fade
    pause 0.5

    scene bg street_exterior with dissolve
    show toa determined at right

    voice "audio/voice/toa_129.mp3"
    toa "Snacks first. Justice second. That is the only order I keep."

    "The canals stink of copper and cheap incense. Toa has slept in worse places, but she did not expect Ryoko Owari to smell worse than the Unicorn roads."

    "Tonight: a magistrate's hall, a permit book, and a city that files its cleanest crimes behind its politest paperwork. She means to read both."

    # Optional Case Zero gate (default off): set persistent.play_case_zero = True
    # if getattr(persistent, "play_case_zero", False):
    #     call kaoru_pro_prologue from _call_kaoru_case_zero

    # Optional Modern AU gate (default off): set persistent.play_au_modern_wrong_floor = True
    # if getattr(persistent, "play_au_modern_wrong_floor", False):
    #     call au_modern_wrong_floor_start from _call_au_modern_wrong_floor

    jump prologue_start
