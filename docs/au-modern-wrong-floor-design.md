# Modern AU: Wrong Floor — design doc

**Status:** Main menu **Bonus: Wrong Floor (Modern AU)** + **AU Case 1: Compliance** + **AU Case 2: Island Weekend** + **AU Case 3: Permits & HR**; dev chapter pick entries for all four (no new-game gate). Does not touch canon save flags. Trilogy of sequels complete; only the **AU Bad End: Parking Garage** remains a doc stub.

**Tone:** Rom-com bureau noir. Port-city rain, municipal paperwork as flirtation, sponsorship-not-dating contract frame. R18-otome tasteful on optional exclusive branch (Case 1.5 shoji level, not novel erotica).

**Play:** Main menu → **Bonus: Wrong Floor (Modern AU)**; or dev chapter pick → **AU: Wrong Floor (Modern)** → `au_modern_wrong_floor_start`. Sequel: **AU Case 1: Compliance** → `au_modern_case1_start` (or Wrong Floor end → *Continue to Case 1?*). **AU Case 2: Island Weekend** → `au_modern_case2_start` (or Case 1 end → *Continue to island weekend?*).

---

## Modern roles

| Canon | Modern AU |
|-------|-----------|
| Emerald Magistrate, Ryoko Owari quarter | **Kitsu Kaoru**, Deputy Director, Municipal Arts & Licensing (Ryoko Port tower) |
| Kakita Toa, Crane Academy dancer | **Kakita Toa**, Crane Conservatory graduate, sponsorship applicant |
| Permit book / hanko | Tablet + expired sponsorship packet + personal stamp |
| Wrong sliding door | Wrong conference room (14-B vs licensing wing) |
| Zoom interrupt | Live council hearing on deputy's monitor |
| Unless? elevator | After-hours service elevator, rain on glass |
| Kitchen seal / curry | Break-room roux, stamp on **paper plate** |
| Kotatsu stinger | Office couch, shared blanket, clementines on armrest |

**On-screen rule:** No L5R terms (no magistrate, shoji, Emerald, gempukku, etc.). Modern bureaucratic props only.

---

## Beat map

| Act | Label | Beats | CG |
|-----|-------|-------|-----|
| 0 | `au_modern_wrong_floor_start` | Title card, rain tower, lost applicant | `au_modern_rain_parking` |
| 1 | `au_modern_wrong_door` | Wrong room, Zoom bleed, **Menu 1** (leave / knock / wait) | `au_modern_wrong_floor` |
| 2 | `au_modern_permit_crisis` | Expired packet, live hearing witness | `au_modern_zoom_hearing` |
| 3 | `au_modern_studio_audition` | Rehearsal proof, counting-as-witness-work | `au_modern_studio_audition` |
| 4 | `au_modern_contract_menu` | **Menu 2** (standard rider / exclusive rehearsal sponsor) | `au_modern_contract_desk` |
| 4b | exclusive rider only | “Not romance on letterhead” | `au_modern_phone_date` |
| 5 | `au_modern_elevator_unless` | Optional if exclusive; Unless? + fade intimate | `au_modern_elevator` |
| 6 | `au_modern_curry_breakroom` | Thank-you curry, hanko-on-plate joke | `au_modern_curry_breakroom` |
| 7 | `au_modern_signing` | Contract effective +3 business days | `au_modern_contract_desk` (dissolve) |
| 8 | `au_modern_stinger_couch` | Blanket loan, clementines, almost-smile denied | `au_modern_couch_stinger` |
| 9 | `au_modern_wrong_floor_end` | Return to dev menu / main menu | — |

**Menus (max 2):**

1. **Door:** Leave and find Arts Council → loop back; Knock properly → trust; Wait quietly → compliance + knock prompt.
2. **Contract:** Standard performance rider (professional); Exclusive rehearsal sponsor → unlocks Unless? elevator branch + Case 1.5-level fade.

---

## Character sheet (dialogue)

**Kaoru — Deputy Director**

- Dry municipal imperative voice; props: stamp, queue number, monitor, paper plate, blanket, clementines.
- Nickname: **To-chan** (proprietary, not romantic confession).
- Warmth filed as scheduling: *Three business days effective*, *blanket is a loan against your noise*.
- Almost-smile inventory explicitly denied (Case Zero echo).

**Toa — Dance grad**

- Bright, concrete, permit-panic energy; *Deputy Director-sama* (modern honorific swap for Magistrate-sama).
- Geography jokes, gratitude via curry, stubborn clean audition lines.
- No love declarations; contract and attendance frame.

See [kaoru-dialogue-style.md](kaoru-dialogue-style.md) and [toa-dialogue-style.md](toa-dialogue-style.md) for cadence; translate props to modern equivalents.

---

## CG list

**Attire rule (all AU CGs):** Western / 21st-century only. Toa: black zip tracksuit with gold stripes + gold crane chest logo (default), or smart casual / rehearsal warm-up (crane on jacket, not obi). Kaoru: charcoal grey deputy-director suit, white shirt. **Reference pack (mandatory for regen):** [au-modern-character-references.md](au-modern-character-references.md) — attach `docs/art-references/au-modern/*-reference.png`; canon sprites are face/hair only. Prompt negatives: kimono, kosode, furisode, hakama, obi, zori (full block in that doc + `scripts/au_modern_cg_prompt_block.txt`).

| Tag | File | Prompt summary |
|-----|------|----------------|
| `au_modern_rain_parking` | `cg-au-modern-rain-parking.png` | Harbor parking / wet port street, raincoat, distant suit silhouette |
| `au_modern_wrong_floor` | `cg-au-modern-wrong-floor.png` | Glass doorway, badge reader, wrong-floor plate, Zoom glow |
| `au_modern_zoom_hearing` | `cg-au-modern-zoom-hearing.png` | Wide licensing office, live council grid on monitor |
| `au_modern_studio_audition` | `cg-au-modern-studio-audition.png` | Mirror studio, barre, port de bras, suit + clipboard witness |
| `au_modern_contract_desk` | `cg-au-modern-contract-desk.png` | Hands on tablet/PDF, seal, sponsorship clause closeup |
| `au_modern_phone_date` | `cg-au-modern-phone-date.png` | Toa at phone glow, deputy silhouette through rain glass |
| `au_modern_elevator` | `cg-au-modern-elevator.png` | Service elevator, rain on glass, two figures close |
| `au_modern_curry_breakroom` | `cg-au-modern-curry-breakroom.png` | Municipal break room, curry pot, stamp on paper plate |
| `au_modern_couch_stinger` | `cg-au-modern-couch-stinger.png` | Office couch, blanket, clementines, rain window |

**Total:** 9 AU CGs. Prior art backed up to `game/images/cg/versions/au-modern-backup-2026-06-04/`.

Registry: `game/images/cgs-au-modern.rpy`. Gallery group: **Extra: AU Wrong Floor (Modern)**.

---

## Voice ID plan

Next free ranges after Case Zero / Case 1 investigation wire (2026-06-04):

| Speaker | Range | Count |
|---------|-------|------:|
| `toa` | `toa_365` – `toa_382` | 18 |
| `narrator` | `narrator_366` – `narrator_383` | 18 |
| `kaoru` | `kaoru_487` – `kaoru_509` | 23 |

**Total wired lines:** 59 (~40–60 target).

**Manifests:** `scripts/voice_performance_manifest.json` (tts_text with Eleven v3 tags), `scripts/voice_manifest.json`, `scripts/narrator_manifest.json`.

**Regen batch:** `scripts/au_modern_voice_ids.txt` → `regenerate_voice_with_metadata.py --model eleven_v3 --ids @scripts/au_modern_voice_ids.txt` → `promote_v2_voice_ids.py`.

**Voice status (2026-06-04):** Manifest entries wired; **59/59 lines regenerated** (`eleven_v3`) and promoted to `game/audio/voice/` via `scripts/au_modern_voice_promote_2026-06-04.log`.

---

## AU Case 1: Wellness District Compliance

**Script:** `game/au_modern_case1_compliance.rpy` (`au_modern_case1_start` → `au_modern_case1_end`).

**Play:** Main menu → **AU Case 1: Compliance**; dev pick → **AU Case 1: Wellness Compliance**; Wrong Floor end → *Continue to Case 1?*

| Act | Label | CG |
|-----|-------|-----|
| 0 | `au_modern_case1_start` | Title, street BGM |
| 1 | `au_modern_case1_wellness_arrival` | `au_modern_case1_club_exterior` |
| 2 | `au_modern_case1_inspection_floor` | `au_modern_case1_clipboard` |
| 3 | `au_modern_case1_llc_joke` + **Menu 1** (film vs log) | `au_modern_case1_phone_notes` |
| 4 | `au_modern_case1_bureaucracy_flirt` | `au_modern_case1_kaoru_doorway` |
| 5 | `au_modern_case1_manager_pushback` + **Menu 2** (firm vs soft) | `au_modern_case1_hallway_tense` (firm branch) |
| 6 | `au_modern_case1_passed_witness` | Harbor weekend calendar hook |
| 7 | `au_modern_case1_elevator_echo` (film or firm branch) | `au_modern_case1_elevator_echo` |

**Menus:** (1) witness documentation style; (2) manager pushback response.

### Case 1 CG list

| Tag | File |
|-----|------|
| `au_modern_case1_club_exterior` | `cg-au-modern-case1-club-exterior.png` |
| `au_modern_case1_clipboard` | `cg-au-modern-case1-clipboard.png` |
| `au_modern_case1_phone_notes` | `cg-au-modern-case1-phone-notes.png` |
| `au_modern_case1_kaoru_doorway` | `cg-au-modern-case1-kaoru-doorway.png` |
| `au_modern_case1_hallway_tense` | `cg-au-modern-case1-hallway-tense.png` |
| `au_modern_case1_elevator_echo` | `cg-au-modern-case1-elevator-echo.png` |

Registry: `game/images/cgs-au-modern-case1.rpy`. Gallery: appended under **Extra: AU Wrong Floor (Modern)**.

### Case 1 voice IDs

| Speaker | Range | Count |
|---------|-------|------:|
| `toa` | `toa_383` – `toa_396` | 14 |
| `narrator` | `narrator_384` – `narrator_399` | 16 |
| `kaoru` | `kaoru_510` – `kaoru_530` | 21 |

**Total:** 51 voiced lines. Regen: `scripts/au_modern_case1_voice_ids.txt` → `regenerate_voice_with_metadata.py --model eleven_v3 --ids @scripts/au_modern_case1_voice_ids.txt` → `promote_v2_voice_ids.py`. **Status (2026-06-04):** 51/51 promoted (`scripts/au_modern_case1_voice_promote_2026-06-04.log`).

**Novel:** `docs/novel/ryoko-owari-au-modern-case1-compliance.md`.

---

## AU Case 2: "Is this a date?" Island Weekend

**Script:** `game/au_modern_case2_island_weekend.rpy` (`au_modern_case2_start` → `au_modern_case2_end`).

**Play:** Main menu → **AU Case 2: Island Weekend**; dev pick → **AU Case 2: Island Weekend**; Case 1 end → *Continue to island weekend?*

| Act | Label | CG |
|-----|-------|-----|
| 0 | `au_modern_case2_start` | Title, street BGM |
| 1 | `au_modern_case2_ferry_delay` | `au_modern_case2_ferry_rain` |
| 2 | `au_modern_case2_airbnb_arrival` | `au_modern_case2_airbnb_exterior`, `au_modern_case2_one_bed` |
| 3 | `au_modern_case2_friend_texts` + **Menu 1** (roommate vs test rider) | `au_modern_case2_phone_text` |
| 4a | `au_modern_case2_roommate_night` | — |
| 4b | `au_modern_case2_rider_menu` + **Menu 2** (procedural vs after-hours audit) | `au_modern_case2_intimate_audit` (audit branch) |
| 5 | `au_modern_case2_balcony_audit` | `au_modern_case2_balcony_night` |
| 6 | `au_modern_case2_end` | Case 3 stub menu or return |

**Menus:** (1) professional roommate vs. test exclusive rider; (2) on rider path only: procedural balcony vs. tasteful after-hours audit (Case 1.5 level).

### Case 2 CG list

| Tag | File |
|-----|------|
| `au_modern_case2_ferry_rain` | `cg-au-modern-case2-ferry-rain.png` |
| `au_modern_case2_airbnb_exterior` | `cg-au-modern-case2-airbnb-exterior.png` |
| `au_modern_case2_one_bed` | `cg-au-modern-case2-one-bed.png` |
| `au_modern_case2_phone_text` | `cg-au-modern-case2-phone-text.png` |
| `au_modern_case2_balcony_night` | `cg-au-modern-case2-balcony-night.png` |
| `au_modern_case2_intimate_audit` | `cg-au-modern-case2-intimate-audit.png` |

Registry: `game/images/cgs-au-modern-case2.rpy`. Gallery: appended under **Extra: AU Wrong Floor (Modern)**.

### Case 2 voice IDs

| Speaker | Range | Count |
|---------|-------|------:|
| `toa` | `toa_397` – `toa_416` | 20 |
| `narrator` | `narrator_400` – `narrator_419` | 20 |
| `kaoru` | `kaoru_531` – `kaoru_547` | 17 |

**Total:** 57 voiced lines. Regen: `scripts/au_modern_case2_voice_ids.txt` → `regenerate_voice_with_metadata.py --model eleven_v3 --ids @scripts/au_modern_case2_voice_ids.txt` → `promote_v2_voice_ids.py`. **Status (2026-06-04):** 57/57 regenerated (`eleven_v3`) and promoted to `game/audio/voice/` via `scripts/au_modern_case2_voice_promote_2026-06-04.log`.

**Novel:** `docs/novel/ryoko-owari-au-modern-case2-island-weekend.md`.

---

## AU Case 3: Permits & HR

**Script:** `game/au_modern_case3_permits_hr.rpy` (`au_modern_case3_start` → `au_modern_case3_end`).

**Play:** Main menu → **AU Case 3: Permits & HR**; dev pick → **AU Case 3: Permits & HR**; Case 2 end → *Continue to Case 3: Permits and HR?*

**Premise:** A viral clip of the Wrong Floor Zoom hearing (*"revise the agenda"*) surfaces and HR opens a file. Kaoru is the signatory of record; Toa is the sponsorship-dependent applicant. The public narrative (deputy + favorite) collides with the deputy's real calendar (audit retreat row left blank on purpose). Canon echo: yoriki / signatory pressure, public hearing exposure.

| Act | Label | CG |
|-----|-------|-----|
| 0 | `au_modern_case3_start` | Title, office BGM |
| 1 | `au_modern_case3_viral_clip` | `au_modern_case3_viral_clip` |
| 2 | `au_modern_case3_hr_summons` + **Menu 1** (public statement vs stay quiet) | `au_modern_case3_hr_office` |
| 3 | `au_modern_case3_signatory_desk` (reads `au_modern_case3_statement`) | `au_modern_case3_signatory_desk` |
| 4 | `au_modern_case3_calendar_vs_narrative` + **Menu 2** (procedural recuse vs personal disclosure) | — |
| 5 | `au_modern_case3_reconcile` (reads `au_modern_case3_disclosure` + Case 2 `au_modern_case2_night_audit`) | `au_modern_case3_reconcile` |
| 6 | `au_modern_case3_end_stinger` → `au_modern_case3_end` (AU Bad End stub card or return) | — |

**Menus:** (1) viral-clip public posture → `au_modern_case3_statement` (`public`/`quiet`), read at signatory desk; (2) signatory-conflict resolution → `au_modern_case3_disclosure` (`procedural`/`personal`), read at the reconciliation beat (also gates the end-stinger card). Both new flags `default` in `game/stats.rpy`; episode also reads existing Case 2 `au_modern_case2_night_audit` for continuity.

### Case 3 CG list

| Tag | File |
|-----|------|
| `au_modern_case3_viral_clip` | `cg-au-modern-case3-viral-clip.png` |
| `au_modern_case3_hr_office` | `cg-au-modern-case3-hr-office.png` |
| `au_modern_case3_signatory_desk` | `cg-au-modern-case3-signatory-desk.png` |
| `au_modern_case3_reconcile` | `cg-au-modern-case3-reconcile.png` |

Registry: `game/images/cgs-au-modern-case3.rpy`. Gallery: appended under **Extra: AU Wrong Floor (Modern)**.

### Case 3 voice IDs

| Speaker | Range | Count |
|---------|-------|------:|
| `toa` | `toa_417` – `toa_434` | 18 |
| `narrator` | `narrator_425` – `narrator_439` | 15 |
| `kaoru` | `kaoru_549` – `kaoru_565` | 17 |

**Total:** 50 voiced lines. Wire: `scripts/wire_au_modern_case3_voice.py` → ID list `scripts/au_modern_case3_voice_ids.txt`. Regen: `regenerate_voice_with_metadata.py --model eleven_v3 --ids @scripts/au_modern_case3_voice_ids.txt --output-subdir v2/eve-donovan-2026-06-04 --force` → `promote_v2_voice_ids.py`. **Status (2026-06-05):** 50/50 regenerated (`eleven_v3`) and promoted to `game/audio/voice/` (`scripts/au_modern_case3_voice_regen.log`, `scripts/au_modern_case3_voice_promote_2026-06-05.log`).

**Next free IDs:** `toa_435+`, `narrator_440+`, `kaoru_566+`.

**Novel:** `docs/novel/ryoko-owari-au-modern-case3-permits-hr.md`.

---

## Deferred AU episodes (doc stubs only)

**AU Bad end · Parking garage** — Wrong-floor recurrence, leaked elevator footage or garage confrontation; ends at dev menu with *sponsorship revoked*. Canon echo: exposure / failure routes. (Case 3's continue menu offers a tasteful not-yet-playable stub card for this.)

---

## Foreshadow / canon echo table

| Modern beat | Canon echo | Notes |
|-------------|------------|-------|
| Wrong conference room | Prologue wrong door | Menu 1 parity (leave/knock/wait) |
| Zoom council hearing | Permit crisis / renewal panic | Bureaucratic pressure, not combat |
| Studio audition | Office dance / performance proof | Counting = witness work |
| Sponsorship contract (not dating) | Companion permit / patronage frame | No romance label on form |
| Unless? elevator | Prologue Unless? branch | Exclusive rider gate only |
| Break-room curry + stamp on plate | Case 1.5 hanko on pot lid | Comic official overreach |
| Couch + blanket + clementines | Case Zero mikan / epilogue kotatsu | Almost-smile denied |
| To-chan / three business days | To-chan / permit +3 days | Nickname + effective date |
| Deputy Director-sama | Magistrate-sama | Same deferential register |

---

## Integration checklist

- [x] `game/au_modern_wrong_floor.rpy`
- [x] `game/images/cgs-au-modern.rpy`
- [x] `game/dev_chapter_pick.rpy` menu entry
- [x] `game/gallery.rpy` group
- [x] `game/script.rpy` optional gate comment (default off)
- [x] `default seen_au_modern_wrong_floor` (isolated; no canon flags)
- [x] Bonus novel stub linked from `docs/novel/README.md`
- [x] `game/au_modern_case1_compliance.rpy`
- [x] `game/images/cgs-au-modern-case1.rpy`
- [x] Main menu + dev pick Case 1 entry
- [x] Wrong Floor end → Continue to Case 1 menu
- [x] `docs/novel/ryoko-owari-au-modern-case1-compliance.md`
- [x] `game/au_modern_case2_island_weekend.rpy`
- [x] `game/images/cgs-au-modern-case2.rpy`
- [x] Main menu + dev pick Case 2 entry
- [x] Case 1 end → Continue to island weekend menu
- [x] `docs/novel/ryoko-owari-au-modern-case2-island-weekend.md`
- [x] `game/au_modern_case3_permits_hr.rpy`
- [x] `game/images/cgs-au-modern-case3.rpy`
- [x] Main menu + dev pick Case 3 entry
- [x] Case 2 end → Continue to Case 3 menu (stub replaced with `jump au_modern_case3_start`)
- [x] `default au_modern_case3_*` flags in `game/stats.rpy` (read at signatory desk + reconcile)
- [x] `docs/novel/ryoko-owari-au-modern-case3-permits-hr.md`

---

## Files

| Path | Role |
|------|------|
| `game/au_modern_wrong_floor.rpy` | Wrong Floor script |
| `game/au_modern_case1_compliance.rpy` | Case 1 script |
| `game/au_modern_case2_island_weekend.rpy` | Case 2 script |
| `game/images/cgs-au-modern.rpy` | Wrong Floor image defs |
| `game/images/cgs-au-modern-case1.rpy` | Case 1 image defs |
| `game/images/cgs-au-modern-case2.rpy` | Case 2 image defs |
| `game/images/cg/cg-au-modern-*.png` | Wrong Floor art |
| `game/images/cg/cg-au-modern-case1-*.png` | Case 1 art |
| `scripts/au_modern_voice_ids.txt` | Wrong Floor regen ID list |
| `scripts/au_modern_case1_voice_ids.txt` | Case 1 regen ID list |
| `scripts/au_modern_case2_voice_ids.txt` | Case 2 regen ID list |
| `scripts/wire_au_modern_case1_voice.py` | Case 1 manifest wire helper |
| `scripts/wire_au_modern_case2_voice.py` | Case 2 manifest wire helper |
| `docs/novel/ryoko-owari-au-modern-wrong-floor.md` | Wrong Floor prose + roadmap |
| `docs/novel/ryoko-owari-au-modern-case1-compliance.md` | Case 1 prose |
