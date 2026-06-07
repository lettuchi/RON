# Case 1 — Companion offer scene (canon path)

**Script:** `game/case1_companion.rpy`  
**Entry:** `prologue_case1_hook` → `case1_companion_offer` when `canon_first_scene`  
**Timing:** Three days after prologue (permit effective date still forward-dated to the 30th)

---

## Canon outcome (locked)

- Kaoru offers **live-in companion** under **art patronage** (sponsor-to-artist ledger, not yoriki or danna): adjoining chamber, meals in inner hall, twice-weekly attendance, day/night case witness duties.
- **Stipend:** 3 koku/month + board (`companion_salary = 3`).
- Toa signs; **`live_in_companion = True`**. Money is secondary; gush path sets **`toa_overjoyed = True`**.
- Ends at **`case1_investigation_hook`**: fetch archive docket → **canal body / Case One** (investigation loop stub).

---

## Beat list

| # | Beat | Visual / audio |
|---|------|----------------|
| 1 | Early return with tea + case file | `bg magistrate_office`, `bgm_office`, door open |
| 2 | Cushion / obedience banter | Sprites; prologue callback lines |
| 3 | Performance / formality callbacks | `performance_style`, `formality_tone` branches |
| 4 | Guest-room line → sponsorship prelude | Dance value, patronage framing, `case1_sponsorship_prelude_menu` |
| 5 | Contract title + duties + stipend read aloud | `cg permit_desk`; CG expressions via `set_expression` |
| 6 | **Menu 1** — accept / negotiate / gush | `companion_accept_tone`; stat deltas |
| 7 | Dual seal + effective date | hanko SFX; flags set |
| 8 | Kaoru reads her (tone branches) | Smirk / hungry / cold |
| 9 | **Menu 2** — unpack vs archive vs tea | `insight` / `honor` / `performance_boldness` |
| 10 | Investigation hook | Archive stairs; canal body tease; `return` |

---

## Choice menus

### `case1_sponsorship_prelude_menu`

| Choice | Stats |
|--------|-------|
| Ask what he wants honestly | +1 insight |
| Offer to dance again | +1 performance_boldness |
| Hold back — permit should be enough | +1 honor, +1 kaoru_resistance |

All paths → sponsorship speech (art donor / twice weekly) → contract stack.

### `case1_companion_accept_menu`

| Choice | `companion_accept_tone` | Stats |
|--------|-------------------------|-------|
| Accept gracefully | `graceful` | +2 composure, +1 honor, +1 compliance |
| Negotiate terms | `negotiate` | +2 insight, +1 kaoru_resistance, `negotiated_terms` |
| Gush honestly | `gush` | `toa_overjoyed`, +1 performance_boldness, +1 kaoru_submission |

All paths → `case1_companion_offer_close` → same canon flags.

### `case1_first_duty_menu`

| Choice | Effect |
|--------|--------|
| Ask for adjoining chamber | +1 insight |
| Archive first | +1 honor, +1 composure |
| Tea refill tease | +1 performance_boldness, +1 kaoru_submission |

All paths → `case1_investigation_hook`.

---

## Flags (`game/stats.rpy`)

| Flag | Purpose |
|------|---------|
| `live_in_companion` | True after signing patronage companion appointment |
| `companion_salary` | Stipend in koku (3) |
| `toa_overjoyed` | True if gush accept path |
| `companion_accept_tone` | `graceful` / `negotiate` / `gush` |

---

## Non-canon stub

**Label:** `case1_noncanon_start` (three weeks later)  
- Reuses prologue non-canon hook dialogue from prior `prologue_case1_hook` body.  
- **No** live-in offer; draft on desk only.  
- Archive fetch + residency “if you survive the week” → `return`.

---

## How to test

1. Launch game → **Start** → play prologue to **physical “Unless?”** → canon ending → **Three days later…**
2. In console or after scene: confirm `live_in_companion`, `companion_salary == 3`, `canon_first_scene`.
3. Replay non-canon: verbal or walkout unless → three weeks → `case1_noncanon_start` (no `live_in_companion`).

Quick jump (Ren'Py shell):

```renpy
$ canon_first_scene = True
$ permit_signed = True
$ permit_effective_days = 3
$ unless_branch = "physical"
$ performance_style = "flirtatious"
jump case1_companion_offer
```

---

## Labels

| Label | Role |
|-------|------|
| `case1_companion_offer` | Canon companion scene start |
| `case1_companion_offer_close` | Post-menu signing |
| `case1_investigation_hook` | Case One tease / end of milestone |
| `case1_noncanon_start` | Three-week alternate opening |
