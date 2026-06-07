# Scene review screenshots: CG catalog, branch beats, bad endings, cinematic first frames.
#
# Re-run (repo root, Windows):
#   _run_screenshot_review.bat
#
# Or individual suites:
#   renpy.exe ryoko-owari test screenshot_review::review_cg_catalog --overwrite-screenshots
#   renpy.exe ryoko-owari test screenshot_review::review_story_beats --overwrite-screenshots
#   renpy.exe ryoko-owari test screenshot_all_turns::canon_all_dialogue --overwrite-screenshots
#
# Output root: screenshots/review-2026-06-02/
# Manifest:    screenshots/review-2026-06-02/manifest.md (scripts/write_screenshot_manifest.py)

define REVIEW_SCREENSHOT_ROOT = "screenshots/review-2026-06-02"


init python:
    import os

    REVIEW_CG_CATALOG = [
        # Prologue: menus & key CGs
        ("cg/prologue/010-prologue_door_choices", "moment prologue_door_choices", "Door choice menu"),
        ("cg/prologue/020-prologue_door_second_chance", "moment prologue_door_second_chance", "Second-chance knock menu"),
        ("cg/prologue/030-prologue_formality_menu", "moment prologue_formality_menu", "Formality tone menu"),
        ("cg/prologue/040-prologue_enter_office_menu", "moment prologue_enter_office_menu", "Enter office menu"),
        ("cg/prologue/050-permit_desk", "permit_desk", "Permit on the desk"),
        ("cg/prologue/060-prologue_before_dance_menu", "moment prologue_before_dance_menu", "Before dance menu"),
        ("cg/prologue/070-prologue_refuse_retry_menu", "moment prologue_refuse_retry_menu", "Refuse dance retry menu"),
        ("cg/prologue/080-office_dance", "office_dance", "Office dance CG"),
        ("cg/prologue/090-prologue_grab_menu", "moment prologue_grab_menu", "Grab moment menu"),
        ("cg/prologue/100-chair_tension", "chair_tension", "Hand on the chair"),
        ("cg/prologue/110-canon_proposition", "canon_proposition", "Canon proposition (unless?)"),
        ("cg/prologue/120-corridor_lost", "corridor_lost", "Lost in the corridor"),
        # Canon encounter
        ("cg/canon/010-canon_pull_close", "canon_pull_close", "Pulled close (tame)"),
        ("cg/canon/020-canon_undressing", "canon_undressing", "Undressing (tame)"),
        ("cg/canon/030-canon_embrace", "canon_embrace", "Embrace (tame)"),
        ("cg/canon/040-canon_afterglow", "canon_afterglow", "Afterglow (tame)"),
        ("cg/canon/050-canon_signing", "canon_signing", "Permit signed"),
        ("cg/canon/060-canon_three_days", "canon_three_days", "Three days later card"),
        # Case 1 companion
        ("cg/case1/010-case1_companion_accept_menu", "moment case1_companion_accept_menu", "Companion accept menu"),
        ("cg/case1/020-case1_first_duty_menu", "moment case1_first_duty_menu", "First duty menu"),
        # Case 1 investigation menus
        ("cg/case1/030-case1_briefing_menu", "moment case1_briefing_menu", "Case 1 briefing menu"),
        ("cg/case1/040-case1_canal_menu", "moment case1_canal_menu", "Canal scene menu"),
        ("cg/case1/050-case1_kaoru_probe_menu", "moment case1_kaoru_probe_menu", "Kaoru probe menu"),
        ("cg/case1/060-case1_registry_menu", "moment case1_registry_menu", "Registry menu"),
        ("cg/case1/070-case1_witness_menu", "moment case1_witness_menu", "Witness menu"),
        ("cg/case1/080-case1_ledger_menu", "moment case1_ledger_menu", "Ledger menu"),
        ("cg/case1/090-case1_barge_menu", "moment case1_barge_menu", "Barge menu"),
        ("cg/case1/100-case1_romance_lantern", "case1_romance_lantern", "Case 1 romance lantern"),
        ("cg/case1/110-gameover_case1_canal", "gameover_case1_canal", "Case 1 bad end: canal"),
        # Case 2
        ("cg/case2/010-case2_briefing_menu", "moment case2_briefing_menu", "Case 2 briefing menu"),
        ("cg/case2/020-case2_alley_menu", "moment case2_alley_menu", "Warehouse alley menu"),
        ("cg/case2/030-case2_desk_menu", "moment case2_desk_menu", "Outer desk menu"),
        ("cg/case2/040-case2_romance_morning", "case2_romance_morning", "Case 2 romance morning"),
        ("cg/case2/050-gameover_case2_exile", "gameover_case2_exile", "Case 2 bad end: exile"),
        # Rain game over
        ("cg/gameover-rain/010-gameover_rain_flee", "gameover_rain_flee", "Rain flee"),
        ("cg/gameover-rain/020-gameover_rain_run", "gameover_rain_run", "Rain run"),
        ("cg/gameover-rain/030-gameover_rain_alone", "gameover_rain_alone", "Rain alone"),
    ]

    def _review_root():
        return os.path.join(renpy.config.basedir, REVIEW_SCREENSHOT_ROOT)

    def _review_save_png(rel_base):
        filename = os.path.join(_review_root(), rel_base + ".png")
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        img = renpy.display.draw.screenshot(renpy.game.interface.surftree)
        renpy.display.scale.image_save_unscaled(img, filename)
        del img

    def _review_bootstrap_canon_prologue():
        store.canon_first_scene = True
        store.permit_signed = True
        store.permit_effective_days = 3
        store.unless_branch = "physical"
        store.live_in_companion = True
        store.door_response = "knock_again"
        store.formality_tone = "hyper_formal"
        store.performance_style = "formal_dance"
        store.physical_initiative = 1
        store.kaoru_submission = 2

    def _review_bootstrap_canon_case1():
        _review_bootstrap_canon_prologue()
        store.case1_closed = False
        store.case1_clue_found = True
        store.case1_victim_name = "Miya Jiro"
        store.kaoru_submission = 3

    def _review_bootstrap_noncanon():
        store.canon_first_scene = False
        store.live_in_companion = False
        store.unless_branch = "verbal"
        store.permit_signed = False

    def _review_write_catalog_report(captured):
        import json
        report_path = os.path.join(_review_root(), "cg-catalog-report.json")
        payload = {
            "screenshots_captured": captured,
            "output_subdir": "cg/",
            "entries": len(REVIEW_CG_CATALOG),
        }
        with open(report_path, "w", encoding="utf-8") as f:
            json.dump(payload, f, indent=2)
            f.write("\n")


label _review_show_cg:
    $ show_cg_scene(_review_cg_tag, fade)
    show toa neutral at right
    show kaoru smirk at left
    " "
    return


label _review_opening_first_frame:
    $ enable_cinematic_music()
    scene black with None
    scene op_lanterns at op_kb_in with Dissolve(1.0)
    pause 0.6
    return


label _review_ed_first_frame:
    scene black with None
    scene ed_canal_dusk at ed_kb_in with Dissolve(0.5)
    pause 0.6
    return


label _review_toa_song_first_frame:
    $ enable_cinematic_music()
    scene black with None
    scene ts_canal_lanterns at ts_kb_in with Dissolve(0.5)
    pause 0.6
    return


label _review_kaoru_song_first_frame:
    $ enable_cinematic_music()
    scene black with None
    scene ks_canal_ledger at ks_kb_in with Dissolve(0.5)
    pause 0.6
    return


label _review_duet_song_first_frame:
    $ enable_cinematic_music()
    scene black with None
    scene ds_canal_two at ds_kb_in with Dissolve(0.5)
    pause 0.6
    return


testsuite screenshot_review:
    description "Review screenshots for major story beats and CG catalog"

    setup:
        $ _test.screenshot_directory = ""
        $ _test.transition_timeout = 0.05
        $ _test.timeout = 600.0
        $ preferences.text_cps = 0
        $ preferences.afm_enable = True
        $ preferences.afm_time = 0

    testcase review_story_beats:
        # Prologue opening (corridor beat)
        run Jump("prologue_start")
        advance repeat 18
        pause 0.5
        screenshot "screenshots/review-2026-06-02/story/prologue/001-prologue_start"

        # Non-canon Case 1 reopening
        python:
            _review_bootstrap_noncanon()
        run Jump("case1_noncanon_start")
        advance repeat 12
        pause 0.5
        screenshot "screenshots/review-2026-06-02/story/case1/001-case1_noncanon_start"

        # Canon companion offer (yoriki menu, long voice chain)
        python:
            _review_bootstrap_canon_prologue()
        run Jump("case1_companion_offer")
        advance repeat 55
        pause 0.5
        screenshot "screenshots/review-2026-06-02/story/case1/002-case1_companion_offer"

        # Case 1 investigation (canon)
        python:
            _review_bootstrap_canon_case1()
        run Jump("case1_investigation_start")
        advance repeat 20
        pause 0.5
        screenshot "screenshots/review-2026-06-02/story/case1/003-case1_investigation_start"

        # Case 2 opening
        python:
            _review_bootstrap_canon_case1()
            store.case1_closed = True
        run Jump("case2_investigation_start")
        advance repeat 18
        pause 0.5
        screenshot "screenshots/review-2026-06-02/story/case2/001-case2_investigation_start"

        # Prologue refuse bad end (title card)
        run Jump("prologue_refuse_bad_end")
        advance repeat 28
        pause 0.5
        screenshot "screenshots/review-2026-06-02/story/prologue/002-prologue_refuse_bad_end"

        exit

    testcase review_bad_endings:
        run Jump("gameover_rain")
        advance repeat 8
        pause 0.5
        screenshot "screenshots/review-2026-06-02/endings/001-gameover_rain_flee"

        advance repeat 6
        pause 0.5
        screenshot "screenshots/review-2026-06-02/endings/002-gameover_rain_run"

        advance repeat 8
        pause 0.5
        screenshot "screenshots/review-2026-06-02/endings/003-gameover_rain_alone"

        run Jump("gameover_case1_canal")
        advance repeat 8
        pause 0.5
        screenshot "screenshots/review-2026-06-02/endings/004-gameover_case1_canal"

        run Jump("gameover_case2_alley")
        advance repeat 8
        pause 0.5
        screenshot "screenshots/review-2026-06-02/endings/005-gameover_case2_alley"

        exit

    testcase review_cinematics_first_frame:
        run Jump("_review_opening_first_frame")
        advance repeat 12
        pause 0.4
        screenshot "screenshots/review-2026-06-02/cinematics/001-opening_sequence"

        run Jump("_review_ed_first_frame")
        advance repeat 12
        pause 0.4
        screenshot "screenshots/review-2026-06-02/cinematics/002-ed_sequence"

        run Jump("_review_toa_song_first_frame")
        advance repeat 12
        pause 0.4
        screenshot "screenshots/review-2026-06-02/cinematics/003-toa_image_song"

        run Jump("_review_kaoru_song_first_frame")
        advance repeat 12
        pause 0.4
        screenshot "screenshots/review-2026-06-02/cinematics/004-kaoru_image_song"

        run Jump("_review_duet_song_first_frame")
        advance repeat 12
        pause 0.4
        screenshot "screenshots/review-2026-06-02/cinematics/005-duet_song"

        exit
