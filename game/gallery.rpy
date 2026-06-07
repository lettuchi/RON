# CG Gallery, Ryoko Owari Nights
#
# A persistent CG gallery reachable from BOTH the main menu and the game menu.
# All gallery logic, the registry, transforms, screens and styles live in this
# single file, no story/script edits are required.
#
# UNLOCK MECHANISM (built-in seen-image tracking)
# -----------------------------------------------
# Every story CG is shown through `show_cg_scene("<tag>")` (scene_layering.rpy),
# which calls the stock `renpy.show("cg <tag>")`. Ren'Py records every shown
# image-name in `persistent._seen_images` (renpy/exports/displayexports.py),
# so `renpy.seen_image("cg <tag>")` is True forever once the player has viewed
# that CG, persistent across save files and playthroughs. We use that as the
# unlock condition, which means:
#   * NO edits to the story/script files are needed.
#   * Unlocks apply retroactively to any existing persistent data.
#
# A few Case 1 illustrations are only ever shown under a pre-choice "moment"
# image name (the dedicated `cg case1_*` aliases are never shown by that name),
# so those entries match against the moment name(s) Ren'Py actually records,
# while the registry still points at the real `cg-case1-*` art for display.
#
# CURATION (see report for the full included/excluded list)
#   Included : 4 prologue first-scene CGs, 7 canon-ending CGs,
#              4 Case 1 illustrations, 2 Case Zero extra CGs (optional
#              pro-prologue; dev menu / future gate only),
#              5 rain/brothel bad-end CGs, 2 magistrate-hall bad-end CGs.
#   Excluded : the `cg choice *` branch art (defined in cgs-choices.rpy but
#              never shown by any script, so it can never be "seen", a
#              permanently-locked slot would just be filler) and the reused
#              pre-choice "moment" placeholders that only re-display first-scene
#              art.

## ---------------------------------------------------------------------------
## Tunables
## ---------------------------------------------------------------------------

# Debug aid only, leave False so unlocks come from seen-image tracking.
define GALLERY_UNLOCK_ALL = False

# Thumbnail geometry (16:9). gui.scale() == int() here (px @ 1280x720).
define GALLERY_COLS = 3
define GALLERY_THUMB_W = gui.scale(280)
define GALLERY_THUMB_H = gui.scale(158)
define GALLERY_ROW_W = gui.scale(912)

# Locked preview look.
define GALLERY_BLUR = 10.0               # blur radius (applied at thumb size)
define GALLERY_PLATE = "#05090a"         # letterbox plate behind every thumb
define GALLERY_LOCK_WASH = "#0a14179e"   # dark wash over locked thumbs


## ---------------------------------------------------------------------------
## Transforms: locked preview = grayscale + blur + slight darken
## ---------------------------------------------------------------------------

transform gallery_locked:
    matrixcolor SaturationMatrix(0.0) * BrightnessMatrix(-0.25)
    blur GALLERY_BLUR


## ---------------------------------------------------------------------------
## Registry + unlock logic
## ---------------------------------------------------------------------------

init python:

    class GalleryCG(object):
        """One gallery slot: art to draw + the seen-image name(s) that unlock it."""

        def __init__(self, title, image, seen=None):
            self.title = title
            self.image = image  # raw file path (same art the story displays)
            if seen is None:
                seen = [image]
            elif isinstance(seen, str):
                seen = [seen]
            self.seen = list(seen)

        def unlocked(self):
            if GALLERY_UNLOCK_ALL:
                return True
            for name in self.seen:
                if renpy.seen_image(name):
                    return True
            return False

    GALLERY_GROUPS = [
        (_("Prologue: The Magistrate's Office"), [
            GalleryCG(_("Wrong Door"),
                      "images/cg/cg-prologue-wrong-door.png", "cg prologue_wrong_door"),
            GalleryCG(_("Lost in the Corridor"),
                      "images/cg/cg-first-scene-corridor-lost.png", "cg corridor_lost"),
            GalleryCG(_("The Permit on the Desk"),
                      "images/cg/cg-first-scene-permit-desk.png", "cg permit_desk"),
            GalleryCG(_("A Dance for One"),
                      "images/cg/cg-first-scene-office-dance.png", "cg office_dance"),
            GalleryCG(_("A Hand on the Chair"),
                      "images/cg/cg-first-scene-chair-tension.png", "cg chair_tension"),
        ]),
        (_("The Encounter: Canon Ending"), [
            GalleryCG(_("The Proposition"),
                      "images/cg/cg-canon-proposition.png", "cg canon_proposition"),
            GalleryCG(_("Pulled Close"),
                      "images/cg/cg-canon-pull-close.png", "cg canon_pull_close"),
            GalleryCG(_("Undressing"),
                      "images/cg/cg-canon-undress-toa.png", "cg canon_undressing"),
            GalleryCG(_("Embrace"),
                      "images/cg/cg-canon-embrace.png", "cg canon_embrace"),
            GalleryCG(_("Afterglow"),
                      "images/cg/cg-canon-afterglow.png", "cg canon_afterglow"),
            GalleryCG(_("The Permit, Signed"),
                      "images/cg/cg-canon-signing.png", "cg canon_signing"),
            GalleryCG(_("Three Days"),
                      "images/cg/cg-canon-three-days.png", "cg canon_three_days"),
        ]),
        (_("Case 1: The Canal Investigation"), [
            GalleryCG(_("The Body in the Canal"),
                      "images/cg/cg-case1-canal-body.png",
                      ["cg moment case1_canal_menu", "cg moment case1_kaoru_probe_menu"]),
            GalleryCG(_("The Licensed Quarter"),
                      "images/cg/cg-case1-licensed-quarter.png",
                      "cg moment case1_registry_menu"),
            GalleryCG(_("Suzu's Testimony"),
                      "images/cg/cg-case1-guesthouse-suzu.png",
                      "cg moment case1_witness_menu"),
            GalleryCG(_("The Forged Ledger"),
                      "images/cg/cg-case1-registry-ledger.png",
                      "cg moment case1_ledger_menu"),
            GalleryCG(_("High Tide at the Barge"),
                      "images/cg/cg-case1-high-tide-barge.png",
                      "cg moment case1_barge_menu"),
            GalleryCG(_("Manifest on the Deck"),
                      "images/cg/cg-case1-barge-confrontation.png",
                      "cg case1_barge_confront"),
        ]),
        (_("Case 1.5: Kitchen Seal"), [
            GalleryCG(_("Left Corridor at Night"),
                      "images/cg/cg-case1_5-chamber-corridor.png",
                      "cg case1_5_chamber_corridor"),
            GalleryCG(_("Tea Past the Shoji"),
                      "images/cg/cg-case1_5-chamber-shoji-tea.png",
                      "cg case1_5_chamber_shoji_tea"),
            GalleryCG(_("Blanket on Her Side"),
                      "images/cg/cg-case1_5-chamber-quilt.png",
                      "cg case1_5_chamber_quilt"),
            GalleryCG(_("Wrist Through the Shoji"),
                      "images/cg/cg-case1_5-shoji-wrist-closeup.png",
                      "cg case1_5_shoji_wrist"),
            GalleryCG(_("Torn Paper, Warm Breath"),
                      "images/cg/cg-case1_5-shoji-tear-closeup.png",
                      "cg case1_5_shoji_tear"),
            GalleryCG(_("Hanko at the Pot Lid"),
                      "images/cg/cg-case1_5-hanko-pot.png",
                      "cg case1_5_hanko_pot"),
            GalleryCG(_("Thank-You Curry at Midday"),
                      "images/cg/cg-case1_5-curry-kitchen.png",
                      "cg case1_5_curry_kitchen"),
            GalleryCG(_("Kaoru Eats the Curry"),
                      "images/cg/cg-case1_5-kaoru-curry-bowl.png",
                      "cg case1_5_kaoru_curry_bowl"),
            GalleryCG(_("Case Two Letters by Midday"),
                      "images/cg/cg-case1_5-dawn-desk-duo.png",
                      "cg case1_5_dawn_desk_duo"),
        ]),
        (_("Case 2: The Academy Packet"), [
            GalleryCG(_("Burned Charter"),
                      "images/cg/cg-case2-academy-desk.png",
                      "cg moment case2_briefing_menu"),
            GalleryCG(_("Ash at the Kiln"),
                      "images/cg/cg-case2-warehouse-ash.png",
                      "cg moment case2_desk_menu"),
            GalleryCG(_("Courier's Alley"),
                      "images/cg/cg-case2-alley-courier.png",
                      "cg moment case2_alley_menu"),
        ]),
        (_("Case 4: The Dock Ledger"), [
            GalleryCG(_("Rain on the Lower Dock"),
                      "images/cg/cg-case4-gritty-establishing.png",
                      "cg case4_gritty_establishing"),
            GalleryCG(_("Three Blades in the Rain"),
                      "images/cg/cg-case4-fight-wide.png",
                      "cg case4_fight_wide"),
            GalleryCG(_("Behind His Line"),
                      "images/cg/cg-case4-romance-defend.png",
                      "cg case4_romance_defend"),
        ]),
        (_("Case 4.5: Teardrop Kobune"), [
            GalleryCG(_("Lantern Canal at Night"),
                      "images/cg/cg-case4_5-boat-canal-night.png",
                      "cg case4_5_boat_canal_night"),
            GalleryCG(_("Tense Aboard the Skiff"),
                      "images/cg/cg-case4_5-boat-duo-tense.png",
                      "cg case4_5_boat_duo_tense"),
            GalleryCG(_("Wet Lashes in the Rain"),
                      "images/cg/cg-case4_5-boat-lash-rain-closeup.png",
                      "cg case4_5_boat_lash_rain"),
            GalleryCG(_("Grip on the Gunwale"),
                      "images/cg/cg-case4_5-boat-hands-gunwale-closeup.png",
                      "cg case4_5_boat_hands_gunwale"),
            GalleryCG(_("Lantern Under Oilcloth"),
                      "images/cg/cg-case4_5-boat-lantern-implied.png",
                      "cg case4_5_boat_lantern_implied"),
            GalleryCG(_("Thrown to the Planking"),
                      "images/cg/cg-case4_5-boat-throw-splash.png",
                      "cg case4_5_boat_throw_splash"),
        ]),
        (_("Case 5: The Left Hand"), [
            GalleryCG(_("Dawn at the Vacant Desk"),
                      "images/cg/cg-case5-false-exit-office.png",
                      "cg case5_false_exit_office"),
            GalleryCG(_("The Public Hearing"),
                      "images/cg/cg-case5-hearing-hall.png",
                      "cg case5_hearing_hall"),
            GalleryCG(_("Seal at the Dais"),
                      "images/cg/cg-case5-hearing-kaoru-dais.png",
                      "cg case5_hearing_kaoru_dais"),
            GalleryCG(_("The Yoriki Scroll"),
                      "images/cg/cg-case5-scroll-desk.png",
                      "cg case5_scroll_desk"),
            GalleryCG(_("Oath on the Scroll"),
                      "images/cg/cg-case5-yoriki-oath.png",
                      "cg case5_yoriki_oath"),
            GalleryCG(_("Hand on the Seal"),
                      "images/cg/cg-case5-oath-seal-hand-closeup.png",
                      "cg case5_oath_seal_hand"),
            GalleryCG(_("Private Chamber"),
                      "images/cg/cg-case5-private-talk.png",
                      "cg case5_private_talk"),
            GalleryCG(_("Screen and Silk"),
                      "images/cg/cg-case5-bedroom-toy.png",
                      "cg case5_bedroom_toy"),
            GalleryCG(_("First Week on Duty"),
                      "images/cg/cg-case5-epilogue-week.png",
                      "cg case5_epilogue_week"),
        ]),
        (_("Bonus Epilogue"), [
            GalleryCG(_("Under the Kotatsu Quilt"),
                      "images/cg/cg-epilogue-kotatsu-warmth-closeup.png",
                      "cg epilogue_kotatsu_warmth"),
            GalleryCG(_("Kotatsu Evening"),
                      "images/cg/cg-epilogue-romance-kotatsu-intimate.png",
                      "cg epilogue_romance_kotatsu_intimate"),
        ]),
        (_("Extra: Case Zero (Pro-prologue)"), [
            GalleryCG(_("Redacted Docket"),
                      "images/cg/cg-case-zero-redacted-docket.png",
                      "cg case_zero_redacted_docket"),
            GalleryCG(_("Rain Alley Door"),
                      "images/cg/cg-case-zero-rain-alley-door.png",
                      "cg case_zero_rain_alley_door"),
        ]),
        (_("Extra: AU Wrong Floor (Modern)"), [
            GalleryCG(_("Practice at the Barre"),
                      "images/cg/cg-toa-ballet-practice-room.png",
                      "cg toa_ballet_practice_room"),
            GalleryCG(_("Rain Parking / Port Street"),
                      "images/cg/cg-au-modern-rain-parking.png",
                      "cg au_modern_rain_parking"),
            GalleryCG(_("Wrong Conference Room"),
                      "images/cg/cg-au-modern-wrong-floor.png",
                      "cg au_modern_wrong_floor"),
            GalleryCG(_("Zoom Council Hearing"),
                      "images/cg/cg-au-modern-zoom-hearing.png",
                      "cg au_modern_zoom_hearing"),
            GalleryCG(_("Witness Rules Post-Its"),
                      "images/cg/cg-au-modern-postit-witness.png",
                      "cg au_modern_postit_witness"),
            GalleryCG(_("Studio Audition"),
                      "images/cg/cg-au-modern-studio-audition.png",
                      "cg au_modern_studio_audition"),
            GalleryCG(_("Sponsorship Contract Desk"),
                      "images/cg/cg-au-modern-contract-desk.png",
                      "cg au_modern_contract_desk"),
            GalleryCG(_("Phone — Is This a Date?"),
                      "images/cg/cg-au-modern-phone-date.png",
                      "cg au_modern_phone_date"),
            GalleryCG(_("Service Elevator Unless"),
                      "images/cg/cg-au-modern-elevator.png",
                      "cg au_modern_elevator"),
            GalleryCG(_("Break Room Curry"),
                      "images/cg/cg-au-modern-curry-breakroom.png",
                      "cg au_modern_curry_breakroom"),
            GalleryCG(_("Couch Stinger"),
                      "images/cg/cg-au-modern-couch-stinger.png",
                      "cg au_modern_couch_stinger"),
            GalleryCG(_("After-Hours Office Intimate"),
                      "images/cg/cg-au-modern-office-intimate.png",
                      "cg au_modern_office_intimate"),
            GalleryCG(_("Service Lift Clinch (AU Wrong Floor)"),
                      "images/cg/cg-au-modern-wrong-floor-unless-lift-kiss.png",
                      "cg au_modern_unless_lift_kiss"),
            GalleryCG(_("Wellness Club Exterior (AU Case 1)"),
                      "images/cg/cg-au-modern-case1-club-exterior.png",
                      "cg au_modern_case1_club_exterior"),
            GalleryCG(_("Inspection Clipboard (AU Case 1)"),
                      "images/cg/cg-au-modern-case1-clipboard.png",
                      "cg au_modern_case1_clipboard"),
            GalleryCG(_("Phone Witness Notes (AU Case 1)"),
                      "images/cg/cg-au-modern-case1-phone-notes.png",
                      "cg au_modern_case1_phone_notes"),
            GalleryCG(_("Kaoru Doorway Grey Suit (AU Case 1)"),
                      "images/cg/cg-au-modern-case1-kaoru-doorway.png",
                      "cg au_modern_case1_kaoru_doorway"),
            GalleryCG(_("Tense Wellness Hallway (AU Case 1)"),
                      "images/cg/cg-au-modern-case1-hallway-tense.png",
                      "cg au_modern_case1_hallway_tense"),
            GalleryCG(_("Elevator Echo (AU Case 1)"),
                      "images/cg/cg-au-modern-case1-elevator-echo.png",
                      "cg au_modern_case1_elevator_echo"),
            GalleryCG(_("Tower Debrief / Harbor Invite (AU Case 1)"),
                      "images/cg/cg-au-modern-case1-tower-debrief.png",
                      "cg au_modern_case1_tower_debrief"),
            GalleryCG(_("Manager Standoff (AU Case 1)"),
                      "images/cg/cg-au-modern-case1-manager-standoff.png",
                      "cg au_modern_case1_manager_standoff"),
            GalleryCG(_("Sponsor-Charm Defuse (AU Case 1)"),
                      "images/cg/cg-au-modern-case1-charm-defuse.png",
                      "cg au_modern_case1_charm_defuse"),
            GalleryCG(_("Ferry Rain Delay (AU Case 2)"),
                      "images/cg/cg-au-modern-case2-ferry-rain.png",
                      "cg au_modern_case2_ferry_rain"),
            GalleryCG(_("Harbor Airbnb Exterior (AU Case 2)"),
                      "images/cg/cg-au-modern-case2-airbnb-exterior.png",
                      "cg au_modern_case2_airbnb_exterior"),
            GalleryCG(_("One Bed Filing (AU Case 2)"),
                      "images/cg/cg-au-modern-case2-one-bed.png",
                      "cg au_modern_case2_one_bed"),
            GalleryCG(_("Is This a Date? Texts (AU Case 2)"),
                      "images/cg/cg-au-modern-case2-phone-text.png",
                      "cg au_modern_case2_phone_text"),
            GalleryCG(_("Balcony Calendar Audit (AU Case 2)"),
                      "images/cg/cg-au-modern-case2-balcony-night.png",
                      "cg au_modern_case2_balcony_night"),
            GalleryCG(_("Exclusive Rider Audit (AU Case 2)"),
                      "images/cg/cg-au-modern-case2-intimate-audit.png",
                      "cg au_modern_case2_intimate_audit"),
            GalleryCG(_("Roommate Night Longing (AU Case 2)"),
                      "images/cg/cg-au-modern-case2-roommate-night.png",
                      "cg au_modern_case2_roommate_night"),
            GalleryCG(_("Exclusive Rider Afterglow (AU Case 2)"),
                      "images/cg/cg-au-modern-case2-audit-afterglow.png",
                      "cg au_modern_case2_audit_afterglow"),
            GalleryCG(_("Rider Doorway (AU Case 2)"),
                      "images/cg/cg-au-modern-case2-rider-doorway.png",
                      "cg au_modern_case2_rider_doorway"),
            GalleryCG(_("Viral Clip Phone (AU Case 3)"),
                      "images/cg/cg-au-modern-case3-viral-clip.png",
                      "cg au_modern_case3_viral_clip"),
            GalleryCG(_("HR Glass Office (AU Case 3)"),
                      "images/cg/cg-au-modern-case3-hr-office.png",
                      "cg au_modern_case3_hr_office"),
            GalleryCG(_("Signatory Desk (AU Case 3)"),
                      "images/cg/cg-au-modern-case3-signatory-desk.png",
                      "cg au_modern_case3_signatory_desk"),
            GalleryCG(_("After-Hours Reconciliation (AU Case 3)"),
                      "images/cg/cg-au-modern-case3-reconcile.png",
                      "cg au_modern_case3_reconcile"),
            GalleryCG(_("Two Ledgers Monitor (AU Case 3)"),
                      "images/cg/cg-au-modern-case3-calendar-monitor.png",
                      "cg au_modern_case3_calendar_monitor"),
            GalleryCG(_("After-Hours Office, Disclosed (AU Case 3)"),
                      "images/cg/cg-au-modern-case3-after-hours.png",
                      "cg au_modern_case3_after_hours"),
            GalleryCG(_("Public Statement (AU Case 3)"),
                      "images/cg/cg-au-modern-case3-public-statement.png",
                      "cg au_modern_case3_public_statement"),
            GalleryCG(_("Quiet Witness Posture (AU Case 3)"),
                      "images/cg/cg-au-modern-case3-quiet-witness.png",
                      "cg au_modern_case3_quiet_witness"),
            GalleryCG(_("Disclosure in His Own Hand (AU Case 3)"),
                      "images/cg/cg-au-modern-case3-disclosure-signed.png",
                      "cg au_modern_case3_disclosure_signed"),
            GalleryCG(_("Motion Granted, On the Record (AU Epilogue)"),
                      "images/cg/cg-au-modern-epilogue-smile.png",
                      "cg au_modern_epilogue_smile"),
            GalleryCG(_("Harbor, Effective Immediately (AU Epilogue)"),
                      "images/cg/cg-au-modern-epilogue-harbor.png",
                      "cg au_modern_epilogue_harbor"),
            GalleryCG(_("Date on Letterhead (AU Epilogue)"),
                      "images/cg/cg-au-modern-epilogue-office-date.png",
                      "cg au_modern_epilogue_office_date"),
            GalleryCG(_("After-Dark Audit (AU Epilogue)"),
                      "images/cg/cg-au-modern-epilogue-audit-intimate.png",
                      "cg au_modern_epilogue_audit_intimate"),
            GalleryCG(_("Harbor Afterglow (AU Epilogue)"),
                      "images/cg/cg-au-modern-epilogue-afterglow.png",
                      "cg au_modern_epilogue_afterglow"),
            GalleryCG(_("Filed Warm and Dressed (AU Epilogue)"),
                      "images/cg/cg-au-modern-epilogue-domestic.png",
                      "cg au_modern_epilogue_domestic"),
            GalleryCG(_("A Year of Queue Later (AU Epilogue)"),
                      "images/cg/cg-au-modern-epilogue-year-later.png",
                      "cg au_modern_epilogue_year_later"),
            GalleryCG(_("Uncurled, No Apology (AU Epilogue)"),
                      "images/cg/cg-au-modern-epilogue-uncurl.png",
                      "cg au_modern_epilogue_uncurl"),
            GalleryCG(_("Harbor Sofa Kiss (AU Epilogue)"),
                      "images/cg/cg-au-modern-epilogue-harbor-kiss.png",
                      "cg au_modern_epilogue_harbor_kiss"),
            GalleryCG(_("Opening: Harbor Licensing Tower (AU)"),
                      "images/cg/cg-au-modern-tower-establishing.png",
                      "cg au_modern_tower_establishing"),
            GalleryCG(_("Intake Counter Rejection (AU Wrong Floor)"),
                      "images/cg/cg-au-modern-intake-counter.png",
                      "cg au_modern_intake_counter"),
            GalleryCG(_("Waiting at the Glass Door (AU Wrong Floor)"),
                      "images/cg/cg-au-modern-wrong-floor-wait.png",
                      "cg au_modern_wrong_floor_wait"),
            GalleryCG(_("Standard Rider Sign-Off (AU Wrong Floor)"),
                      "images/cg/cg-au-modern-standard-rider.png",
                      "cg au_modern_standard_rider"),
            GalleryCG(_("Break Room Sink (AU Wrong Floor)"),
                      "images/cg/cg-au-modern-breakroom-sink.png",
                      "cg au_modern_breakroom_sink"),
            GalleryCG(_("Pre-Dawn Tower Meeting (AU Case 1)"),
                      "images/cg/cg-au-modern-case1-predawn-tower.png",
                      "cg au_modern_case1_predawn_tower"),
            GalleryCG(_("Float-Tank Inspection (AU Case 1)"),
                      "images/cg/cg-au-modern-case1-float-tank.png",
                      "cg au_modern_case1_float_tank"),
            GalleryCG(_("Counting Candles (AU Case 1)"),
                      "images/cg/cg-au-modern-case1-capacity-count.png",
                      "cg au_modern_case1_capacity_count"),
            GalleryCG(_("Wrist & Pulse (AU Case 1)"),
                      "images/cg/cg-au-modern-case1-wrist-pulse.png",
                      "cg au_modern_case1_wrist_pulse"),
            GalleryCG(_("Salt-Air Pier Arrival (AU Case 2)"),
                      "images/cg/cg-au-modern-case2-pier-arrival.png",
                      "cg au_modern_case2_pier_arrival"),
            GalleryCG(_("Deep Rider Audit (AU Case 2)"),
                      "images/cg/cg-au-modern-case2-audit-deep.png",
                      "cg au_modern_case2_audit_deep"),
            GalleryCG(_("Balcony Hand-Clasp (AU Case 2)"),
                      "images/cg/cg-au-modern-case2-balcony-handclasp.png",
                      "cg au_modern_case2_balcony_handclasp"),
            GalleryCG(_("Trending Cold Open (AU Case 3)"),
                      "images/cg/cg-au-modern-case3-trending-office.png",
                      "cg au_modern_case3_trending_office"),
            GalleryCG(_("HR Fishbowl Atrium (AU Case 3)"),
                      "images/cg/cg-au-modern-case3-fishbowl-exterior.png",
                      "cg au_modern_case3_fishbowl_exterior"),
            GalleryCG(_("Recusal Handover (AU Case 3)"),
                      "images/cg/cg-au-modern-case3-recuse-handover.png",
                      "cg au_modern_case3_recuse_handover"),
            GalleryCG(_("Crying About Paperwork (AU Case 3)"),
                      "images/cg/cg-au-modern-case3-paperwork-tears.png",
                      "cg au_modern_case3_paperwork_tears"),
            GalleryCG(_("You've Been Replaced (AU Epilogue)"),
                      "images/cg/cg-au-modern-epilogue-replaced-phone.png",
                      "cg au_modern_epilogue_replaced_phone"),
            GalleryCG(_("Witness Posture, Kept (AU Epilogue)"),
                      "images/cg/cg-au-modern-epilogue-witness-posture.png",
                      "cg au_modern_epilogue_witness_posture"),
            GalleryCG(_("After-Dark Audit Embrace (AU Epilogue)"),
                      "images/cg/cg-au-modern-epilogue-audit-count.png",
                      "cg au_modern_epilogue_audit_count"),
            GalleryCG(_("One Row Left Blank (AU Epilogue)"),
                      "images/cg/cg-au-modern-epilogue-blank-row.png",
                      "cg au_modern_epilogue_blank_row"),
        ]),
        (_("Canon Romance: Cases 1 & 2"), [
            GalleryCG(_("Lantern Night (Case 1)"),
                      "images/cg/cg-case1-romance-lantern.png",
                      "cg case1_romance_lantern"),
            GalleryCG(_("Canal Lantern Walk (Case 1)"),
                      "images/cg/cg-case1-romance-canal-lantern.png",
                      "cg case1_romance_canal_lantern"),
            GalleryCG(_("Almost Touch (Case 1)"),
                      "images/cg/cg-case1-romance-office-touch.png",
                      "cg case1_romance_office_touch"),
            GalleryCG(_("Patronage, Not Danna (Case 1)"),
                      "images/cg/cg-case1-romance-sponsorship.png",
                      "cg case1_romance_sponsorship"),
            GalleryCG(_("Moonlit Gangplank (Case 1)"),
                      "images/cg/cg-case1-romance-barge-moonlit.png",
                      "cg case1_romance_barge_moonlit"),
            GalleryCG(_("Morning Tea (Case 2)"),
                      "images/cg/cg-case2-romance-morning.png",
                      "cg case2_romance_morning"),
            GalleryCG(_("Hill Overlook (Case 2)"),
                      "images/cg/cg-case2-festival-hill.png",
                      "cg case2_festival_hill"),
            GalleryCG(_("Festival Fireworks (Case 2)"),
                      "images/cg/cg-case2-festival-fireworks.png",
                      "cg case2_festival_fireworks"),
            GalleryCG(_("Bench Kiss (Case 2)"),
                      "images/cg/cg-case2-festival-kiss.png",
                      "cg case2_festival_kiss"),
            GalleryCG(_("Shoji Silhouette (Case 2)"),
                      "images/cg/cg-case2-festival-intimate.png",
                      "cg case2_festival_intimate"),
        ]),
        (_("Case 3.5: Is this a date?"), [
            GalleryCG(_("Tear Drop Island Night"),
                      "images/cg/cg-case3_5-date-island-night.png",
                      "cg case3_5_date_island_night"),
            GalleryCG(_("Inn Between Geisha Houses"),
                      "images/cg/cg-case3_5-date-inn-exterior.png",
                      "cg case3_5_date_inn_exterior"),
            GalleryCG(_("Private Room Lanterns"),
                      "images/cg/cg-case3_5-date-tatami-lanterns.png",
                      "cg case3_5_date_tatami_lanterns"),
            GalleryCG(_("Kaiseki Course"),
                      "images/cg/cg-case3_5-date-kaiseki.png",
                      "cg case3_5_date_kaiseki"),
            GalleryCG(_("Sake Porcelain"),
                      "images/cg/cg-case3_5-date-sake-cup.png",
                      "cg case3_5_date_sake_cup"),
            GalleryCG(_("Spring Furisode Silk"),
                      "images/cg/cg-case3_5-date-silk-fabric.png",
                      "cg case3_5_date_silk_fabric"),
            GalleryCG(_("Tealight Flame"),
                      "images/cg/cg-case3_5-date-candle-flame.png",
                      "cg case3_5_date_candle_flame"),
            GalleryCG(_("Toa's Lashes"),
                      "images/cg/cg-case3_5-date-toa-lashes.png",
                      "cg case3_5_date_toa_lashes"),
            GalleryCG(_("Kaoru's Hand on Cup"),
                      "images/cg/cg-case3_5-date-kaoru-hand-cup.png",
                      "cg case3_5_date_kaoru_hand_cup"),
            GalleryCG(_("Collar Cord and Gold Brocade"),
                      "images/cg/cg-case3_5-date-inn-collar-hands.png",
                      "cg case3_5_date_inn_collar_hands"),
            GalleryCG(_("Almost Touch"),
                      "images/cg/cg-case3_5-date-almost-hands.png",
                      "cg case3_5_date_almost_hands"),
            GalleryCG(_("Dancer's Eye"),
                      "images/cg/cg-case3_5-date-toa-watching.png",
                      "cg case3_5_date_toa_watching"),
            GalleryCG(_("Duo at Low Table"),
                      "images/cg/cg-case3_5-date-duo-table.png",
                      "cg case3_5_date_duo_table"),
            GalleryCG(_("Gossip in Shadow"),
                      "images/cg/cg-case3_5-date-gossip-shadow.png",
                      "cg case3_5_date_gossip_shadow"),
            GalleryCG(_("Very Well Loved"),
                      "images/cg/cg-case3_5-date-reassurance.png",
                      "cg case3_5_date_reassurance"),
            GalleryCG(_("Bridge Arrival (Furisode)"),
                      "images/cg/cg-case3_5-date-arrival.png",
                      "cg case3_5_date_arrival"),
            GalleryCG(_("Kaiseki Duo"),
                      "images/cg/cg-case3_5-date-kaiseki-duo.png",
                      "cg case3_5_date_kaiseki_duo"),
            GalleryCG(_("Watching the Dancers"),
                      "images/cg/cg-case3_5-date-watch-dancers.png",
                      "cg case3_5_date_watch_dancers"),
            GalleryCG(_("Bodies as Truthtellers"),
                      "images/cg/cg-case3_5-date-lesson.png",
                      "cg case3_5_date_lesson"),
            GalleryCG(_("Gossip Trouble"),
                      "images/cg/cg-case3_5-date-gossip.png",
                      "cg case3_5_date_gossip"),
            GalleryCG(_("Lantern Path Walk"),
                      "images/cg/cg-case3_5-date-walk-duo.png",
                      "cg case3_5_date_walk_duo"),
        ]),
        (_("Case 3: Fabric Shop"), [
            GalleryCG(_("Bolt Room (Case 3)"),
                      "images/cg/cg-case3-fabric-shop.png",
                      "cg case3_fabric_shop"),
            GalleryCG(_("Falling Silk (Case 3)"),
                      "images/cg/cg-case3-accident-moment.png",
                      "cg case3_accident_moment"),
            GalleryCG(_("Pull Clear (Case 3)"),
                      "images/cg/cg-case3-kaoru-rescue.png",
                      "cg case3_kaoru_rescue"),
        ]),
        (_("Bad End: Cases 1 & 2"), [
            GalleryCG(_("Bait for the Canal"),
                      "images/cg/cg-case1-bad-canal.png",
                      "cg gameover_case1_canal"),
            GalleryCG(_("Judgment at the Desk"),
                      "images/cg/cg-case1-bad-punishment-desk.png",
                      "cg gameover_case1_punishment_desk"),
            GalleryCG(_("The Magistrate's Grip"),
                      "images/cg/cg-case1-bad-punishment-hands.png",
                      "cg gameover_case1_punishment_hands"),
            GalleryCG(_("On the Tatami"),
                      "images/cg/cg-case1-bad-punishment-floor.png",
                      "cg gameover_case1_punishment_floor"),
            GalleryCG(_("Screen Sealed"),
                      "images/cg/cg-case1-bad-punishment-shoji.png",
                      "cg gameover_case1_punishment_shoji"),
            GalleryCG(_("Road of Ash"),
                      "images/cg/cg-case2-bad-exile.png",
                      "cg gameover_case2_exile"),
            GalleryCG(_("Bolt Room Fall (Case 3)"),
                      "images/cg/cg-case3-bad-injury.png",
                      "cg gameover_case3_injury"),
            GalleryCG(_("Edge of the Blade (Case 4)"),
                      "images/cg/cg-case4-bad-slayn.png",
                      "cg gameover_case4_slayn"),
            GalleryCG(_("Night at the Hull (Case 4.5)"),
                      "images/cg/cg-case4_5-bad-boat-injury.png",
                      "cg gameover_case4_5_boat"),
            GalleryCG(_("Refused the Left Hand (Case 5)"),
                      "images/cg/cg-case5-bad-chained.png",
                      "cg gameover_case5_chained"),
            GalleryCG(_("Hall Cage (Case 5)"),
                      "images/cg/cg-case5-bad-quarter-cage.png",
                      "cg gameover_case5_quarter_cage"),
        ]),
        (_("Bad End: Into the Rain"), [
            GalleryCG(_("Flight into the Rain"),
                      "images/cg/cg-gameover-rain-flee.png", "cg gameover_rain_flee"),
            GalleryCG(_("Down the Canal Road"),
                      "images/cg/cg-gameover-rain-run.png", "cg gameover_rain_run"),
            GalleryCG(_("Alone in the Downpour"),
                      "images/cg/cg-gameover-rain-alone.png", "cg gameover_rain_alone"),
            GalleryCG(_("Broken in the Alley"),
                      "images/cg/cg-badend-brothel-crying.png", "cg badend_brothel_crying"),
            GalleryCG(_("Rain in White Lashes"),
                      "images/cg/cg-badend-brothel-tears.png", "cg badend_brothel_tears"),
            GalleryCG(_("Pulp and Pride"),
                      "images/cg/cg-badend-brothel-permit.png", "cg badend_brothel_permit"),
            GalleryCG(_("The Ronin's Arithmetic"),
                      "images/cg/cg-badend-brothel-ronin.png", "cg badend_brothel_ronin"),
            GalleryCG(_("Hold Her Arms"),
                      "images/cg/cg-badend-brothel-grasp.png", "cg badend_brothel_grasp"),
            GalleryCG(_("Cart and Lantern Door"),
                      "images/cg/cg-badend-brothel-cart.png", "cg badend_brothel_cart"),
        ]),
        (_("Bad End: The Magistrate's Hall"), [
            GalleryCG(_("Gate at Night"),
                      "images/cg/cg-badend-kaoru-gate.png", "cg badend_kaoru_gate"),
            GalleryCG(_("Clerk's Grip"),
                      "images/cg/cg-badend-kaoru-wrist.png", "cg badend_kaoru_wrist"),
            GalleryCG(_("Sealed to the Case"),
                      "images/cg/cg-badend-kaoru-corridor.png", "cg badend_kaoru_corridor"),
            GalleryCG(_("Something That Isn't Renewal"),
                      "images/cg/cg-badend-kaoru-stamp.png", "cg badend_kaoru_stamp"),
            GalleryCG(_("Line Item on His Evening"),
                      "images/cg/cg-badend-kaoru-office.png", "cg badend_kaoru_office"),
            GalleryCG(_("Off Balance at the Desk"),
                      "images/cg/cg-badend-kaoru-office-throw.png", "cg badend_kaoru_office_throw"),
            GalleryCG(_("From the Cushion"),
                      "images/cg/cg-badend-kaoru-office-floor.png", "cg badend_kaoru_office_floor"),
            GalleryCG(_("Strip Under the Shoji"),
                      "images/cg/cg-badend-kaoru-shoji.png", "cg badend_kaoru_shoji"),
        ]),
    ]

    def gallery_rows(entries, cols):
        return [entries[i:i + cols] for i in range(0, len(entries), cols)]

    def gallery_all_entries():
        result = []
        for _title, entries in GALLERY_GROUPS:
            result.extend(entries)
        return result

    def gallery_unlocked_entries():
        return [e for e in gallery_all_entries() if e.unlocked()]

    def gallery_unlocked_index(entry):
        ul = gallery_unlocked_entries()
        try:
            return ul.index(entry)
        except ValueError:
            return 0

    def gallery_total_count():
        return len(gallery_all_entries())

    def gallery_unlocked_count():
        return len(gallery_unlocked_entries())

    def gallery_play_music_cinematic(label_id):
        """Launch image-song / cinematic replay; restore menu music when opened from title."""
        if renpy.context()._main_menu:
            store._cinematic_from_menu = True
        renpy.call_in_new_context(label_id)


## ---------------------------------------------------------------------------
## Gallery grid screen (works from the main menu AND the game menu)
## ---------------------------------------------------------------------------

screen cg_gallery():

    tag menu

    use game_menu(_("CG Gallery"), scroll="viewport", spacing=gui.scale(20)):

        python:
            _g_unlocked = gallery_unlocked_count()
            _g_total = gallery_total_count()

        vbox:
            spacing gui.scale(20)

            text _("[_g_unlocked] / [_g_total] unlocked"):
                style "gallery_progress"

            for group_title, entries in GALLERY_GROUPS:

                vbox:
                    spacing gui.scale(10)

                    text group_title style "gallery_group_header"

                    for row in gallery_rows(entries, GALLERY_COLS):

                        hbox:
                            spacing gui.scale(14)

                            for entry in row:
                                use cg_gallery_slot(entry)

            vbox:
                spacing gui.scale(10)

                text _("Music") style "gallery_group_header"

                hbox:
                    spacing gui.scale(14)
                    use cg_gallery_kaoru_song_slot
                    use cg_gallery_toa_song_slot
                    # Duet hidden from gallery for now: restore: use cg_gallery_duet_song_slot


screen cg_gallery_kaoru_song_slot():

    vbox:
        xsize GALLERY_THUMB_W
        spacing gui.scale(4)

        button:
            style "gallery_thumb_button"
            xysize (GALLERY_THUMB_W, GALLERY_THUMB_H)
            action Function(gallery_play_music_cinematic, "kaoru_image_song_sequence")

            add Solid(GALLERY_PLATE)
            add "images/ks/ks-canal-night-ledger.png":
                fit "cover"
                xysize (GALLERY_THUMB_W, GALLERY_THUMB_H)
                align (0.5, 0.5)

        text _("Kaoru's Song: 「権利の帳」") style "gallery_caption"


screen cg_gallery_toa_song_slot():

    vbox:
        xsize GALLERY_THUMB_W
        spacing gui.scale(4)

        button:
            style "gallery_thumb_button"
            xysize (GALLERY_THUMB_W, GALLERY_THUMB_H)
            action Function(gallery_play_music_cinematic, "toa_image_song_sequence")

            add Solid(GALLERY_PLATE)
            add "images/ts/ts-canal-lanterns.png":
                fit "cover"
                xysize (GALLERY_THUMB_W, GALLERY_THUMB_H)
                align (0.5, 0.5)

        text _("Toa's Song: 「赤い糸の灯」") style "gallery_caption"


screen cg_gallery_duet_song_slot():

    vbox:
        xsize GALLERY_THUMB_W
        spacing gui.scale(4)

        button:
            style "gallery_thumb_button"
            xysize (GALLERY_THUMB_W, GALLERY_THUMB_H)
            action Function(gallery_play_music_cinematic, "duet_song_sequence")

            add Solid(GALLERY_PLATE)
            add "images/ds/ds-duet-portrait-canal.png":
                fit "cover"
                xysize (GALLERY_THUMB_W, GALLERY_THUMB_H)
                align (0.5, 0.5)

        text _("Duet: 「嘘の夜を走れ」") style "gallery_caption"


screen cg_gallery_slot(entry):

    $ unlocked = entry.unlocked()

    vbox:
        xsize GALLERY_THUMB_W
        spacing gui.scale(4)

        if unlocked:

            button:
                style "gallery_thumb_button"
                xysize (GALLERY_THUMB_W, GALLERY_THUMB_H)
                action Show("cg_gallery_view", index=gallery_unlocked_index(entry))

                add Solid(GALLERY_PLATE)
                add entry.image:
                    fit "contain"
                    xysize (GALLERY_THUMB_W, GALLERY_THUMB_H)
                    align (0.5, 0.5)

            text entry.title style "gallery_caption"

        else:

            fixed:
                xysize (GALLERY_THUMB_W, GALLERY_THUMB_H)

                add Solid(GALLERY_PLATE)

                # Same art, grayscale + blurred + darkened.
                fixed:
                    xysize (GALLERY_THUMB_W, GALLERY_THUMB_H)
                    at gallery_locked

                    add entry.image:
                        fit "contain"
                        xysize (GALLERY_THUMB_W, GALLERY_THUMB_H)
                        align (0.5, 0.5)

                add Solid(GALLERY_LOCK_WASH)

                # Crisp lock glyph on top (not blurred).
                text "?":
                    style "gallery_lock_glyph"
                    align (0.5, 0.5)

            text _("Locked") style "gallery_caption_locked"


## ---------------------------------------------------------------------------
## Full-screen CG viewer (unlocked slots only) with prev / next
## ---------------------------------------------------------------------------

screen cg_gallery_view(index=0):

    modal True
    zorder 150

    default pos = index

    python:
        _v_entries = gallery_unlocked_entries()
        _v_count = len(_v_entries)
        _v_cur = (pos % _v_count) if _v_count else 0
        _v_human = _v_cur + 1
        _v_entry = _v_entries[_v_cur] if _v_count else None

    add Solid("#000000")

    if _v_entry is not None:
        add _v_entry.image:
            fit "contain"
            xysize (config.screen_width, config.screen_height)
            align (0.5, 0.5)

    ## Click anywhere outside the controls to close.
    button:
        style "gallery_view_dismiss"
        action Hide("cg_gallery_view")

    ## Top bar: title (left) + counter & close (right).
    frame:
        style "gallery_view_bar"
        xfill True
        yalign 0.0

        if _v_entry is not None:
            text _v_entry.title:
                style "gallery_view_title"
                xalign 0.0
                yalign 0.5

        hbox:
            xalign 1.0
            yalign 0.5
            spacing gui.scale(20)

            text _("[_v_human] / [_v_count]"):
                style "gallery_view_counter"
                yalign 0.5

            textbutton _("Close"):
                style "gallery_view_button"
                yalign 0.5
                action Hide("cg_gallery_view")

    if _v_count > 1:

        textbutton _("< Prev"):
            style "gallery_view_button"
            align (0.0, 0.5)
            xoffset gui.scale(20)
            action SetScreenVariable("pos", (_v_cur - 1) % _v_count)

        textbutton _("Next >"):
            style "gallery_view_button"
            align (1.0, 0.5)
            xoffset gui.scale(-20)
            action SetScreenVariable("pos", (_v_cur + 1) % _v_count)

        key "K_LEFT" action SetScreenVariable("pos", (_v_cur - 1) % _v_count)
        key "K_RIGHT" action SetScreenVariable("pos", (_v_cur + 1) % _v_count)

    ## Right-click / Escape closes the viewer (back to the grid).
    key "game_menu" action Hide("cg_gallery_view")


## ---------------------------------------------------------------------------
## Styles (self-contained: gold/teal palette matching the rest of the GUI)
## ---------------------------------------------------------------------------

style gallery_progress is gui_text:
    size gui.scale(24)
    color gui.accent_color
    outlines [(1, "#0a1618aa", 0, 0)]

style gallery_group_header is gui_text:
    size gui.scale(28)
    color "#e8d5a3"
    font "fonts/YujiSyuku-Regular.ttf"
    outlines [(2, "#0a1618", 0, 0)]

style gallery_caption is gui_text:
    size gui.scale(15)
    color "#f5f0e6"
    xalign 0.5
    text_align 0.5
    layout "subtitle"

style gallery_caption_locked is gallery_caption:
    color "#5a5550"

style gallery_lock_glyph is gui_text:
    size gui.scale(56)
    color "#c9a227cc"
    font "fonts/YujiSyuku-Regular.ttf"
    outlines [(2, "#0a1618", 0, 0)]

style gallery_thumb_button is empty:
    background None
    hover_foreground Solid("#c9a22733")

style gallery_view_dismiss is empty:
    xfill True
    yfill True
    background None

style gallery_view_bar is empty:
    background Solid("#0a1618cc")
    padding (gui.scale(24), gui.scale(12))
    ysize gui.scale(58)

style gallery_view_title is gui_text:
    size gui.scale(26)
    color "#e8d5a3"
    outlines [(2, "#000000", 0, 0)]

style gallery_view_counter is gui_text:
    size gui.scale(20)
    color gui.idle_small_color

style gallery_view_button is button:
    background Solid("#0a1618aa")
    hover_background Solid("#c9a22755")
    padding (gui.scale(18), gui.scale(8))

style gallery_view_button_text is button_text:
    size gui.scale(22)
    color "#c9b896"
    hover_color "#e8d5a3"
    yalign 0.5
