# Dev / test, chapter jump menu (Ryoko Owari Nights)
#
# Entry labels used by this menu:
#   kaoru_pro_prologue, prologue_start
#   case1_companion_offer, case1_investigation_start, case1_romance_router
#   case1_5_romance_interlude
#   case2_investigation_start, case2_festival_interlude, case2_romance_morning
#   case3_investigation_start, case3_kaoru_rescue
#   case3_5_is_this_a_date_interlude, case4_investigation_start, case4_5_boat_interlude
#   case5_investigation_start, epilogue_romance_bonus
#   au_modern_wrong_floor_start, au_modern_case1_start, au_modern_case2_start, au_modern_case3_start, au_modern_epilogue_start (Modern AU bonus)
#   prologue_bad_end_kaoru, prologue_bad_end_brothel, gameover_case1_canal, case1_bad_end_kaoru_punishment
#   gameover_case2_alley, gameover_case3_injury
#
# Disable for release: set dev_chapter_pick_enabled = False below, or gate on config.developer only.

define dev_chapter_pick_enabled = False

init python:
    def dev_set_romance_flags_for_test(mark_prior_romance_seen=False):
        """Canon romance eligibility + case stats; optional *_seen for mid-game jumps."""
        store.canon_first_scene = True
        store.permit_signed = True
        store.permit_effective_days = 3
        store.unless_branch = "physical"
        store.live_in_companion = True
        store.door_response = "knock_again"
        store.formality_tone = "hyper_formal"
        store.performance_style = "flirtatious"
        store.performance_boldness = 2
        store.physical_initiative = 1
        store.compliance = 1
        store.kaoru_submission = 3
        store.companion_accept_tone = "gush"

        store.case1_kaoru_trust = 5
        store.case1_sponsorship_flirt = True
        store.case1_romance_route = "trust"
        store.case1_victim_name = "Miya Jiro"
        store.case1_clue_found = True
        store.case1_manifest_seized = True

        store.case2_festival_kiss_only = False
        store.case2_festival_intimate = True

        store.case3_kaoru_rescue = True
        store.case3_accident_avoided = True

        if mark_prior_romance_seen:
            store.case1_romance_seen = True
            store.case2_festival_seen = True
            store.case2_romance_seen = True


    def dev_set_case_prerequisites(upto_case):
        """Minimal closed-case flags so later scripts do not break (1–4)."""
        if upto_case >= 1:
            store.case1_closed = True
            store.case1_milestone = "case1_closed"
        if upto_case >= 2:
            store.case2_closed = True
            store.case2_milestone = "case2_closed"
            store.case2_packet_found = True
        if upto_case >= 3:
            store.case3_closed = True
            store.case3_started = True


label dev_apply_romance_flags:
    $ dev_set_romance_flags_for_test(mark_prior_romance_seen=False)
    return


label dev_chapter_pick_menu:

    scene black with dissolve
    centered "{size=+4}Dev, Chapter pick{/size}\n{size=-4}Romance eligibility is set for all jumps except Play from beginning.{/size}"

    menu dev_chapter_pick_main:

        "Play from beginning (no cheat flags)":
            jump dev_play_from_beginning

        "Pro-prologue, Case Zero (Kaoru)":
            jump kaoru_pro_prologue

        "Prologue":
            call dev_apply_romance_flags
            jump prologue_start

        "Case 1, companion offer":
            call dev_apply_romance_flags
            $ dev_set_case_prerequisites(0)
            jump case1_companion_offer

        "Case 1, investigation start":
            call dev_apply_romance_flags
            $ dev_set_case_prerequisites(0)
            jump case1_investigation_start

        "Case 1, romance interlude (router)":
            call dev_apply_romance_flags
            $ case1_romance_seen = False
            $ dev_set_case_prerequisites(0)
            jump case1_romance_router

        "Case 1.5, Kitchen Seal (chamber + curry)":
            call dev_apply_romance_flags
            $ dev_set_case_prerequisites(1)
            $ case1_romance_seen = True
            $ case1_5_romance_seen = False
            $ seen_gameover_case1 = False
            jump case1_5_romance_interlude

        "Case 2, investigation start":
            call dev_apply_romance_flags
            $ dev_set_case_prerequisites(1)
            jump case2_investigation_start

        "Case 2, festival interlude only":
            call dev_apply_romance_flags
            $ dev_set_case_prerequisites(2)
            $ case2_festival_seen = False
            $ case2_romance_seen = False
            jump case2_festival_interlude

        "Case 2, morning tea romance only":
            call dev_apply_romance_flags
            $ dev_set_case_prerequisites(2)
            $ case2_festival_seen = True
            $ case2_romance_seen = False
            jump case2_romance_morning

        "Case 3, investigation start":
            call dev_apply_romance_flags
            $ dev_set_case_prerequisites(2)
            $ case2_festival_seen = True
            $ case2_romance_seen = True
            $ case3_closed = False
            $ case3_started = False
            jump case3_investigation_start

        "Case 3, Kaoru rescue beat only":
            call dev_apply_romance_flags
            $ dev_set_case_prerequisites(2)
            $ case3_closed = False
            jump case3_kaoru_rescue

        "Case 3.5: Is this a date?":
            call dev_apply_romance_flags
            $ dev_set_case_prerequisites(3)
            $ dev_set_romance_flags_for_test(mark_prior_romance_seen=True)
            $ case3_closed = True
            $ case4_date_interlude_seen = False
            jump case3_5_is_this_a_date_interlude

        "Case 4, dock swordfight start":
            call dev_apply_romance_flags
            $ dev_set_case_prerequisites(3)
            $ dev_set_romance_flags_for_test(mark_prior_romance_seen=True)
            $ case4_date_interlude_seen = True
            $ case4_closed = False
            $ case4_started = False
            $ case4_kaoru_defended = False
            $ case4_toa_slain = False
            jump case4_investigation_start

        "Case 4.5, Teardrop kobune":
            call dev_apply_romance_flags
            $ dev_set_case_prerequisites(4)
            $ dev_set_romance_flags_for_test(mark_prior_romance_seen=True)
            $ case4_date_interlude_seen = True
            $ case4_closed = True
            $ case4_kaoru_defended = True
            $ case4_5_boat_interlude_seen = False
            $ case4_5_bad_end_boat_injury = False
            jump case4_5_boat_interlude

        "Case 5, yoriki hearing (Path A)":
            call dev_apply_romance_flags
            $ dev_set_case_prerequisites(4)
            $ dev_set_romance_flags_for_test(mark_prior_romance_seen=True)
            $ case4_date_interlude_seen = True
            $ case4_closed = True
            $ case4_kaoru_defended = True
            $ case4_5_boat_interlude_seen = True
            $ case5_started = False
            $ case5_closed = False
            $ case5_yoriki_accepted = False
            $ case5_yoriki_refused = False
            $ case5_romance_bonus_seen = False
            jump case5_investigation_start

        "Bonus, kotatsu epilogue (post Case 5)":
            call dev_apply_romance_flags
            $ dev_set_case_prerequisites(4)
            $ dev_set_romance_flags_for_test(mark_prior_romance_seen=True)
            $ case5_closed = True
            $ case5_yoriki_accepted = True
            $ case5_yoriki_refused = False
            $ case5_romance_bonus_seen = False
            jump epilogue_romance_bonus

        "AU: Wrong Floor (Modern)":
            jump au_modern_wrong_floor_start

        "AU Case 1: Wellness Compliance":
            jump au_modern_case1_start

        "AU Case 2: Island Weekend":
            jump au_modern_case2_start

        "AU Case 3: Permits & HR":
            jump au_modern_case3_start

        "AU Epilogue: Effective Immediately":
            jump au_modern_epilogue_start

        "--- Bad ends ---":
            jump dev_chapter_pick_bad_ends


label dev_chapter_pick_bad_ends:

    menu dev_chapter_pick_bad_menu:

        "Back":
            jump dev_chapter_pick_menu

        "Prologue, Kaoru pursuit bad end":
            call dev_apply_romance_flags
            jump prologue_bad_end_kaoru

        "Prologue, rain brothel bad end":
            call dev_apply_romance_flags
            jump prologue_bad_end_brothel

        "Case 1, canal game over":
            call dev_apply_romance_flags
            jump gameover_case1_canal

        "Case 1, office punishment bad end":
            call dev_apply_romance_flags
            jump case1_bad_end_kaoru_punishment

        "Case 2, alley game over":
            call dev_apply_romance_flags
            $ dev_set_case_prerequisites(1)
            jump gameover_case2_alley

        "Case 3, injury game over":
            call dev_apply_romance_flags
            $ dev_set_case_prerequisites(2)
            jump gameover_case3_injury

        "Case 4, dock slayn game over":
            call dev_apply_romance_flags
            $ dev_set_case_prerequisites(3)
            jump gameover_case4_slayn

        "Case 4.5, kobune injury game over":
            call dev_apply_romance_flags
            $ dev_set_case_prerequisites(4)
            jump gameover_case4_5_boat

        "Case 5, refusal bad end (quarter chains)":
            call dev_apply_romance_flags
            $ case5_yoriki_refused = True
            $ case5_closed = True
            jump case5_bad_end_refusal_chained

        "Case 5, refusal bad end (hall cage)":
            call dev_apply_romance_flags
            $ case5_yoriki_refused = True
            $ case5_closed = True
            jump case5_bad_end_refusal_cage

        "Case 5, game over CG only (chained)":
            call dev_apply_romance_flags
            jump gameover_case5_chained

        "Case 5, game over CG only (hall cage)":
            call dev_apply_romance_flags
            jump gameover_case5_quarter_cage


label dev_play_from_beginning:

    jump dev_play_normal_start
