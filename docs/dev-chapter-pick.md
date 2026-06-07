# Dev chapter pick menu

Quick-jump menu for playtesting cases and romance interludes without a full canon playthrough.

## Enable / disable

| Control | Location |
|---------|----------|
| `dev_chapter_pick_enabled` | `game/dev_chapter_pick.rpy` â€” set to `False` for release builds |
| `config.developer` | Ren'Py launcher â€œDeveloperâ€ mode â€” optional extra gate in `script.rpy` |

On **Play from beginning**, no cheat flags are applied; you get the normal opening, street intro, and prologue.

All other menu entries call `dev_apply_romance_flags` (which runs `dev_set_romance_flags_for_test()`), then jump to the target label.

## Start button (dev builds)

When `dev_chapter_pick_enabled` is `True`, **Start** shows a short gate menu first:

1. **Play from beginning** — `dev_play_normal_start` (opening + prologue, no cheat flags)
2. **Dev chapter pick** — full jump menu below

Release builds skip the gate and go straight to `dev_play_normal_start`.

## Menu structure

1. **Play from beginning** â€” normal `start` flow (opening + intro lines â†’ `prologue_start`)
2. **Prologue** â€” `prologue_start`
3. **Case 1** â€” companion offer, investigation start, romance router
4. **Case 2** â€” investigation, festival only, morning tea only
5. **Case 3** â€” investigation start, Kaoru rescue beat only
6. **Case 3.5** â€” `case3_5_is_this_a_date_interlude` (â€œIs this a date?â€)
7. **Case 4** â€” dock swordfight `case4_investigation_start`
8. **Case 4.5** â€” Teardrop kobune `case4_5_boat_interlude`
9. **Bad ends** â€” prologue Kaoru pursuit, Case 1 canal, Case 2 alley, Case 3 injury, Case 4 dock slayn, Case 4.5 kobune injury

## Flags set by `dev_set_romance_flags_for_test`

**Prologue / canon**

- `canon_first_scene`, `live_in_companion`, `permit_signed`, `permit_effective_days = 3`
- `unless_branch = "physical"`, `kaoru_submission = 3`, flirtatious performance choices
- `companion_accept_tone = "gush"`, `toa_overjoyed`, `companion_salary = 12`

**Case 1 romance eligibility**

- `case1_kaoru_trust = 5`, `case1_sponsorship_flirt = True`, `case1_romance_route = "trust"`
- Investigation bootstrap: `case1_victim_name`, `case1_clue_found`, `case1_manifest_seized`

**Case 2 festival path (max romance)**

- `case2_festival_intimate = True`, `case2_festival_kiss_only = False`

**Case 3 rescue**

- `case3_kaoru_rescue`, `case3_accident_avoided`

**Not set by default** (so interludes still play): `case1_romance_seen`, `case2_festival_seen`, `case2_romance_seen`. Case 3+ jumps also call `dev_set_case_prerequisites` and may mark prior romance as seen.

**Case prerequisites** (`dev_set_case_prerequisites(n)`): sets `case1_closed`, `case2_closed`, `case3_started` / `case3_closed` as needed for the target case.

## Case 3.5 / Case 4 jumps

**Case 3.5** sets Case 3 closed, prior romance seen, clears `case4_date_interlude_seen`, jumps `case3_5_is_this_a_date_interlude`.

**Case 4 dock start** sets Cases 1â€“3 closed, prior romance seen, marks date interlude seen (skip 3.5), resets `case4_closed` / `case4_started` / defend flags, jumps `case4_investigation_start`.

**Case 4.5 kobune** sets Cases 1â€“4 closed, full romance flags, `case4_kaoru_defended`, clears `case4_5_boat_interlude_seen`, jumps `case4_5_boat_interlude`.

## Backup

**Ren'Py loads all `.rpy` under `game/` recursively.** Snapshots in `game/versions/` must use `.rpy.bak` (not `.rpy`) or you get duplicate label errors. See `game/versions/README.txt`.

Pre-order snapshot: `game/versions/case-order-2026-06-03/`
