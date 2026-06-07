# Case 1.5 — 「台所の印」 / Kitchen Seal

Romance interlude (not a numbered case file). Bridges Case One closure and Case Two briefing for canon companion players who cleared Case One romance without the canal bad end.

## Eligibility

`case1_5_romance_interlude_eligible()` in `game/case_endings.rpy`:

- `canon_romance_eligible()` (canon first scene, live-in companion, `kaoru_submission >= 2`)
- `case1_closed` and `case1_romance_seen`
- not `case1_5_romance_seen`
- not `seen_gameover_case1`

## Entry / exit

| | |
|---|---|
| **Entry** | `case1_barge_milestone_end` in `case1_investigation.rpy`, after `case1_closed = True` |
| **Exit** | `case2_investigation_start` |
| **Flag** | `case1_5_romance_seen = True` at interlude end |

## Beats

### A — Adjoining chamber (flashback)

- Narrator frame: first night after companion menu adjoining chamber.
- Tone: cute, domestic; Kaoru deadpan proprietary; Toa earnest.
- CG tags via `show_cg_scene` + `pause 2.0` + `set_expression` on dialogue only:
  - `case1_5_chamber_corridor` → corridor, tea tray, lantern
  - `case1_5_chamber_shoji_tea` → unasked tea through shoji
  - `case1_5_chamber_quilt` → blanket loan on her side of screen
- Story: cannot sleep; hears stamping; unasked tea; no thanks; blanket on her side of screen; no explicit sex.

### B — Curry kitchen (present)

- Midday/lunch after barge; Case Two letters waiting on outer desk since morning.
- Thank-you curry; almost stamps **hanko** on pot lid; jurisdictional lentils; one bowl, no praise.
- CG tags:
  - `case1_5_hanko_pot` → comedy close-up, seal at lid
  - `case1_5_curry_kitchen` → kitchen duo, curry steam (existing art)
  - `case1_5_kaoru_curry_bowl` → Kaoru seated eating thank-you curry, Toa watching
  - `case1_5_dawn_desk_duo` → midday desk, letters stacked, empty bowl (tag/filename kept from original dawn framing)

## Art

| Tag | Asset |
|-----|--------|
| `case1_5_chamber_corridor` | `cg-case1_5-chamber-corridor.png` |
| `case1_5_chamber_shoji_tea` | `cg-case1_5-chamber-shoji-tea.png` |
| `case1_5_chamber_quilt` | `cg-case1_5-chamber-quilt.png` |
| `case1_5_hanko_pot` | `cg-case1_5-hanko-pot.png` |
| `case1_5_curry_kitchen` | `cg-case1_5-curry-kitchen.png` (kept) |
| `case1_5_kaoru_curry_bowl` | `cg-case1_5-kaoru-curry-bowl.png` |
| `case1_5_dawn_desk_duo` | `cg-case1_5-dawn-desk-duo.png` |

All under `images/cg/`. No `images/op/` reuse.

Defs: `game/images/cgs-case1_5-romance.rpy`

## Voice (stubs only)

- `narrator_297`–`303`
- `kaoru_374`–`383`
- `toa_308`–`311`, `313`–`317` (no `toa_312`)

Manifests updated; audio not regenerated.

## Dev / gallery

- Dev jump: `dev_chapter_pick.rpy` → "Case 1.5, Kitchen Seal"
- Dev CG QA: `dev_case1_5_cg_qa` (seven slots)
- Gallery group: "Case 1.5: Kitchen Seal" in `gallery.rpy`

## Constraints

- No Case 1.5 file on desk (diegetic).
- No fail state or bad end.
- No opening/OP art in Case 1.5.
- ~15–25 lines per beat.
