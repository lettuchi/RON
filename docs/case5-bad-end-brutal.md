# Case 5 refusal bad ends (brutal)

**Status:** Shipped in `game/case5_investigation.rpy` + `game/case_endings.rpy`  
**Trigger:** Refuse yoriki at `case5_yoriki_menu` → `case5_bad_end_refusal_warning`  
**Tone:** Conversational Case 5 diction; Kaoru cold/proprietary; Toa pride fraying; implied coercion only (no explicit on-screen sex).

---

## Content warning

Centered small text before Continue / Return to title (mirrors Case 1 punishment):

> This ending is brutal. Chains, coerced use, loss of agency.

---

## Label map

| Label | Role |
|-------|------|
| `case5_bad_end_refusal_warning` | Hearing fallout, CW menu, `$ case5_closed = True` |
| `case5_bad_end_refusal_choice` | In-world fork menu |
| `case5_bad_end_refusal_chained` | Quarter path hearing beats → `gameover_case5_chained` |
| `case5_bad_end_refusal_cage` | Hall path hearing beats → `gameover_case5_quarter_cage` |
| `gameover_case5_chained` | CG-held climax, 「帳の拒絶」 card |
| `gameover_case5_quarter_cage` | CG-held climax, 「御前の檻」 card |

**Flags:** `case5_yoriki_refused`, `case5_closed`, `seen_gameover_case5`

---

## Path A: Quarter chains (`gameover_case5_chained`)

**Player choice:** *Let the pleasure quarter buy what I would not sign.*

1. **Hearing hall (sprites):** Kaoru sells the refusal; Toa tries to recant; scroll ink closed.
2. **CG climax (`cg-case5-bad-chained.png`):** Back-room chains, okami transaction, Kaoru's left hand filled without Toa's name on the appointment scroll. Dialogue stays on CG with `set_expression` + `pause 2.0` between beats.
3. **Game Over:** 「帳の拒絶」 / *Kakita Toa refused the left hand.*

**Voice IDs:** `kaoru_360`, `367`, `368`, `372`; `toa_304`, `296`, `305`; `narrator_290`, `291`, `286`, `292`

---

## Path B: Hall cage (`gameover_case5_quarter_cage`)

**Player choice:** *Keep me in magistrate custody where the hall can see.*

1. **Hearing hall (sprites):** Corrective custody filed; Toa protests Crane dignity.
2. **CG climax (`cg-case5-bad-quarter-cage.png`):** Holding cell under magistrate hall, torn kosode, coerced thumbprint on companion chit (not yoriki scroll). Bureaucratic cruelty on CG.
3. **Game Over:** 「御前の檻」 / *The hall kept Kakita Toa without the oath.*

**Voice IDs:** `kaoru_369`, `370`, `371`, `373`; `toa_306`, `307`; `narrator_293`, `294`, `295`, `287`, `296`

**Shared hearing IDs:** `narrator_288`, `289`; `toa_302`; `kaoru_365`, `366`

---

## Art briefs (PNGs shipped)

**CG assets:** `game/images/cg/cg-case5-bad-chained.png` and `cg-case5-bad-quarter-cage.png` — 1536×1024, GenerateImage 2026-06-04.

| File | Tag | Brief |
|------|-----|-------|
| `images/cg/cg-case5-bad-chained.png` | `gameover_case5_chained` | Pleasure-quarter back room, red lantern wash. Toa in travel kosode, wrists chained to iron ring or post (implied restraint, no gore). Okami silhouette or coin tray foreground. Kaoru exiting frame or shadow at door, gold haori edge. Tasteful otome tragedy, not explicit. |
| `images/cg/cg-case5-bad-quarter-cage.png` | `gameover_case5_quarter_cage` | Magistrate hall holding cell beneath dais: stone, iron grate, wax paper and hanko dish slid under bars. Toa torn kosode, kneeling or seated on cold floor, thumb inked. Clerk boots visible. Cold bureaucratic palette, no blood. |

---

## Dev QA

`game/dev_chapter_pick.rpy` → Bad endings menu:

- Full path: *Case 5, refusal bad end (quarter chains / hall cage)*
- CG-only: *Case 5, game over CG only (chained / hall cage)*

---

## Word counts (spoken + narrator lines)

| Path | Hearing | CG gameover | Total |
|------|---------|-------------|-------|
| Quarter chains | ~68 words | ~95 words | ~163 words |
| Hall cage | ~62 words | ~108 words | ~170 words |

*(Shared warning block ~75 words additional.)*
