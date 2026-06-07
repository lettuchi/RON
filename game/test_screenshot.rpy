# Automated prologue screenshot capture for UI verification.
# Run: renpy.sh ryoko-owari test screenshot_capture::prologue_turn_3 --overwrite-screenshots
# Formality CG (small stage sprites): renpy.sh ryoko-owari test screenshot_capture::prologue_formality_cg --overwrite-screenshots
#
# Full scene review batch: _run_screenshot_review.bat (see game/test_screenshot_review.rpy)

label _screenshot_formality_cg:
    $ show_cg_scene("moment prologue_formality_menu")
    show kaoru commanding
    kaoru "State your business. Briefly."
    return

init python:
    _test_prologue_turn3_caption = (
        'Turn 1: "Lantern light pools on polished floorboards. Every sliding door looks the same." | '
        'Turn 2: "Toa clutches her permit book and hanko case, turning in a corridor that refuses to end." | '
        'Turn 3: Toa, "I was sure the clerk said third hall, fourth door on the left. Or was it the right?"'
    )

testsuite screenshot_capture:
    setup:
        $ _test.screenshot_directory = ""
        $ _test.transition_timeout = 0.05
        $ _test.timeout = 30.0
        $ preferences.text_cps = 0
        $ preferences.afm_enable = True
        $ preferences.afm_time = 0

    testcase prologue_turn_3:
        run Jump("prologue_start")
        advance until "I was sure the clerk"
        pause 1.0
        screenshot "docs/test-screenshots/turn-3"
        python:
            caption_path = os.path.join(renpy.config.basedir, "docs/test-screenshots/turn-3-caption.txt")
            with open(caption_path, "w", encoding="utf-8") as f:
                f.write(_test_prologue_turn3_caption + "\n")
        exit

    testcase prologue_formality_cg:
        run Jump("_screenshot_formality_cg")
        pause 1.0
        screenshot "docs/test-screenshots/formality-cg"
        exit
