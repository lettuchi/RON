# Case 3 — Kimono fabric shop (絹屋の帳)

**Script:** `game/case3_investigation.rpy`  
**CG defs:** `game/images/cgs-case3.rpy`  
**Bad end:** `game/case_endings.rpy` → `gameover_case3_injury`  
**Entry:** `case3_investigation_start` from `case2_post_case2_bridge`, `case2_festival_bridge`, or `case2_romance_morning` when `case2_closed` and not `case3_closed`

---

## Design (vertical slice)

- **Setting:** Kimono fabric shop bolt room — inventory, mis-tagged Scorpion dye lot, sabotaged shelf brace.
- **Thread:** Chrysanthemum factor cousin from Case One; tax ledger vs bolt count (stub for full case).
- **Tone:** Case 3 attachment arc — Toa seeks Kaoru's nod on notes; fluster after danger; no love confession ([toa-dialogue-style.md](toa-dialogue-style.md)).
- **Kaoru:** Brief honest beat (*if you had died…*), then cold magistrate cover ([kaoru-dialogue-style.md](kaoru-dialogue-style.md)).

---

## Beat list

| # | Beat | Visual / audio |
|---|------|----------------|
| 1 | Office briefing — Case Three docket | `bg magistrate_office`, `bgm_office` |
| 2 | **Menu 1** — briefing focus | `case3_briefing_menu` |
| 3 | Fabric shop arrival | `bg fabric_shop`, `cg case3_fabric_shop` |
| 4 | **Menu 2** — one investigation clue | `case3_investigation_menu` |
| 5 | Shelf collapse — accident climax | `cg case3_accident_moment` |
| 6 | **Menu 3** — trust vs dodge alone | `case3_accident_menu` |
| 7a | Rescue route | `cg case3_kaoru_rescue`, `bgm_canon_intimate` → `case3_milestone_end` |
| 7b | Bad end | warning menu → `gameover_case3_injury` → title |

---

## Choice menus

### `case3_briefing_menu`

| Choice | `case3_briefing_choice` | Stats |
|--------|-------------------------|-------|
| Tax ledger first | `ledger` | +2 insight |
| Clerk interview first | `witness` | +2 composure, +1 honor |
| Scorpion dye thread | `scorpion_thread` | +1 insight, +1 honor |

### `case3_investigation_menu` (pick one clue)

| Choice | Flag | Stats |
|--------|------|-------|
| Mis-tagged bolt ends | `case3_clue_bolt` | +2 insight |
| Clerk's second ledger | `case3_clue_clerk` | +1 composure, +1 insight |
| Scored shelf brace | `case3_clue_shelf` | +1 honor, +1 insight |

### `case3_accident_menu`

| Choice | Route |
|--------|-------|
| Trust Kaoru — shout for him | `case3_kaoru_rescue`, `case3_accident_avoided`, `case3_kaoru_rescue` |
| Dodge alone — refuse help | `case3_bad_end_injury` → Game Over |

---

## Flags (`game/stats.rpy`)

| Flag | Purpose |
|------|---------|
| `case3_started` | Case Three opened |
| `case3_briefing_choice` | Office menu tag |
| `case3_clue_bolt` / `case3_clue_clerk` / `case3_clue_shelf` | Investigation clues |
| `case3_accident_choice` | `trust_kaoru` / `dodge_alone` |
| `case3_accident_avoided` | Rescue path |
| `case3_kaoru_rescue` | Romance beat taken |
| `case3_bad_end_injury` | Bad end taken |
| `case3_closed` | Vertical slice complete (`case3_milestone_end`) |
| `seen_gameover_case3` | Gallery / bookkeeping (`case_endings.rpy`) |

---

## CG assets

| File | Ren'Py tag |
|------|------------|
| `images/cg/cg-case3-fabric-shop.png` | `cg case3_fabric_shop` |
| `images/cg/cg-case3-accident-moment.png` | `cg case3_accident_moment` |
| `images/cg/cg-case3-kaoru-rescue.png` | `cg case3_kaoru_rescue` |
| `images/cg/cg-case3-bad-injury.png` | `cg gameover_case3_injury` |

---

## Playtest

**Rescue (canon continue):** Finish Case 2 → festival/morning bridge → Case 3 → briefing → any clue → *Trust Kaoru* → `case3_milestone_end` → `return`.

**Bad end:** Same through accident menu → *Dodge alone* → content warning → Continue → Game Over → title.

**DEV jump:** `renpy.jump("case3_investigation_start")` from console with `case2_closed = True`.
