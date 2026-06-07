# Pre-choice CG map — one image on the beat immediately before each `menu:` statement

**Total menus:** 15 (10 prologue, 2 case1 companion, 3 case1 investigation)

**Art registration:** `game/images/cgs-choice-moments.rpy`  
**Show helper:** `$ show_cg_scene("moment <menu_id>")` or reuse beat tags via `$ show_cg_scene("permit_desk")`

**Sprite rule during CG:** full-body sprites hidden; bust portraits in textbox remain (`set_expression` / `cg_safe_show` wrapper).

---

## Prologue (`game/prologue.rpy`)

| # | Menu label / ID | Line before menu | Scene context | CG tag | File | Source |
|---|-----------------|------------------|---------------|--------|------|--------|
| 1 | `prologue_door_choices` | "The door shuts with finality…" | Wrong door, corridor | `cg moment prologue_door_choices` | `cg-first-scene-corridor-lost.png` | Reused beat |
| 2 | *(unnamed)* / `prologue_door_second_chance` | `prologue_door_second_chance` label | Loop-back at same door | `cg moment prologue_door_second_chance` | `cg-first-scene-corridor-lost.png` | Reused beat |
| 3 | `prologue_formality_menu` | Formal knock narration | Threshold kneel | `cg moment prologue_formality_menu` | `cg-choice-moment-prologue_formality_menu.png` | **Generated** |
| 4 | `prologue_enter_office_menu` | "He gestures. The door closes…" | Door shut, comply/peek | `cg moment prologue_enter_office_menu` | `cg-choice-office-comply.png` | Reused choice art |
| 5 | `prologue_expired_menu` | Permit dates crisis dialogue | Desk / expired permit | `cg permit_desk` | `cg-first-scene-permit-desk.png` | Reused beat (already on CG) |
| 6 | `prologue_before_dance_menu` | Kaoru: "Impress me." | Audition bargain | `cg moment prologue_before_dance_menu` | `cg-choice-moment-prologue_before_dance_menu.png` | **Generated** |
| 7 | *(unnamed)* / `prologue_refuse_retry_menu` | Bad-end centered text | Refuse-dance retry | `cg moment prologue_refuse_retry_menu` | `cg-choice-dance-refuse.png` | Reused choice art |
| 8 | `prologue_performance_menu` | Obi loosen / lamplight | Office dance entry | `cg office_dance` | `cg-first-scene-office-dance.png` | Reused beat (already on CG) |
| 9 | `prologue_grab_menu` | Wrist grab narration | Escalation | `cg moment prologue_grab_menu` | `cg-choice-grab-rebuke.png` | Reused choice art |
| 10 | `prologue_unless_menu` | Chair creak / "Unless?" setup | Cliffhanger | `cg chair_tension` | `cg-first-scene-chair-tension.png` | Reused beat (already on CG) |

---

## Case 1 companion (`game/case1_companion.rpy`)

| # | Menu label / ID | Line before menu | Scene context | CG tag | File | Source |
|---|-----------------|------------------|---------------|--------|------|--------|
| 11 | `case1_companion_accept_menu` | Contract / salary beat | Patronage companion offer | `cg moment case1_companion_accept_menu` | `cg-first-scene-permit-desk.png` | Reused beat |
| 12 | `case1_first_duty_menu` | Archive / bells line | Post-signing duties | `cg moment case1_first_duty_menu` | `cg-choice-moment-case1_first_duty_menu.png` | **Generated** |

---

## Case 1 investigation (`game/case1_investigation.rpy`)

| # | Menu label / ID | Line before menu | Scene context | CG tag | File | Source |
|---|-----------------|------------------|---------------|--------|------|--------|
| 13 | `case1_briefing_menu` | Kaoru: "Eat one now…" | Docket briefing | `cg moment case1_briefing_menu` | `cg-choice-moment-case1_briefing_menu.png` | **Generated** |
| 14 | `case1_canal_menu` | Kaoru: "…observe." | Canal body scene | `cg moment case1_canal_menu` | `cg-case1-canal-body.png` | **Generated** |
| 15 | `case1_kaoru_probe_menu` | Kaoru: "Summarize…" | Same canal beat | `cg moment case1_kaoru_probe_menu` | `cg-case1-canal-body.png` | Reused canal CG |

---

## Generated vs wired

| Category | Count |
|----------|-------|
| Menus total | **15** |
| Pre-choice CGs wired | **15** |
| New PNGs generated | **5** |
| Reused existing beat/choice PNGs | **10** |
| Menus missing art | **0** |

### New files (May 2026)

- `game/images/cg/cg-choice-moment-prologue_formality_menu.png`
- `game/images/cg/cg-choice-moment-prologue_before_dance_menu.png`
- `game/images/cg/cg-choice-moment-case1_first_duty_menu.png`
- `game/images/cg/cg-choice-moment-case1_briefing_menu.png`
- `game/images/cg/cg-case1-canal-body.png`

---

## Choice-outcome CGs (not pre-choice)

The 21 branch-outcome images in `cgs-choices.rpy` / `docs/cg-choice-map.md` remain available for post-choice beats but are **not** used as pre-choice moments (except where noted above as reuse).

`cg_beats` / even-turn overlay system remains removed — see `docs/cg-beat-map.md`.
