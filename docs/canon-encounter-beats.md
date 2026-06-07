# Canon Encounter Beats â€” Physical "Unless?" Route

**Script:** `game/prologue_canon_encounter.rpy` (`label prologue_canon_ending`)  
**Entry:** `prologue_unless_menu` â†’ physical answer â†’ `cg canon_proposition` â†’ jump  
**Tone:** R-rated sensual (tame implied path only; Toa and Kaoru on tatami, fade before graphic detail).

---

## Beat sequence (`prologue_canon_tame`)

| # | Beat | CG tag | File | Notes |
|---|------|--------|------|-------|
| 0 | Chair tension / physical unless | â€” | (prior) | `chair_tension` â†’ menu â†’ `canon_proposition` |
| 1 | Proposition intensifies | `canon_pull_close` | `cg-canon-pull-close.png` | Kaoru draws Toa off the chair |
| 2 | Partial undress | `canon_undressing` | `cg-canon-undress-toa.png` | She loosens his magistrate robes at collar/shoulder |
| 3 | Intimate embrace | `canon_embrace` | `cg-canon-embrace.png` | Cushion on floor, lamplight, implied heat |
| 4 | Fade to black | â€” | â€” | Encounter implied, not narrated |
| 5 | Afterglow | `canon_afterglow` | `cg-canon-afterglow.png` | Breath and silk regained |
| 6 | Signing | `canon_signing` | `cg-canon-signing.png` | Hanko on permit renewal |
| 7 | Three-day hook | `canon_three_days` | `cg-canon-three-days.png` | Forward-dated effective date â†’ Case 1 |

`prologue_canon_ending` jumps straight into `prologue_canon_tame` (no intensity menu). Both merge at `prologue_canon_signing` â†’ `prologue_case1_hook`.

---

## CG registration

`game/images/cgs-canon-ending.rpy`:

- `canon_proposition` â€” existing (unless menu)
- `canon_pull_close`, `canon_undressing`, `canon_embrace`, `canon_afterglow` â€” tame path
- `canon_signing`, `canon_three_days` â€” signing beats

Archived intimate-track PNGs (`canon_steamy_*`, `dance_disrobe`, `butt_wiggle_grab`, `bent_over_desk`) remain defined for tooling only; they are not shown in story or gallery.

Show via `$ show_cg_scene("tag")`; small sprites use `cg_left` / `cg_right` per `scene_layering.rpy`.

---

## Flags & audio

**Set at signing:** `permit_signed`, `canon_first_scene`, `permit_effective_days = 3`, `kaoru_submission += 2`

**Music:** `audio.bgm_canon_intimate` from encounter start through signing.

**SFX:** `sliding_door_close`, `cushion_slide` (robe/cushion beats), `paper_shuffle`, `hanko_stamp`

**Voice:** New encounter dialogue is unvoiced; afterglow through three-days retains `kaoru_075`â€“`080` / `toa_062`â€“`066`.

---

## Content boundaries

- Sensual dialogue and partial disrobing; embrace CG; fade before explicit act
- No genitalia, no pornographic close-ups on any CG
- Otome/L5R power dynamic: Kaoru controlled but yielding; Toa bold and willing

## Art generation (tame canon CGs)

Use existing canon presets / compositor in `assets/cg-build/` and `scripts/novelai_prompts.json` for `canon_pull_close`, `canon_undressing`, `canon_embrace`, `canon_afterglow`, `canon_signing`, `canon_three_days`.

