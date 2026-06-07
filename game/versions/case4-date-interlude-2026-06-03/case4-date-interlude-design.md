# Case 4 post-close interlude — "Is this a date?"

**Script:** `game/case4_date_interlude.rpy`  
**Label:** `case4_is_this_a_date_interlude`  
**Entry:** `case4_post_case4_bridge` after `case4_milestone_end` when `all_romance_routes_complete()` and not `case4_date_interlude_seen`.

---

## Discord source

| Field | Value |
|-------|--------|
| **Thread title** | Is this a date? |
| **URL** | *Not indexed in repo as of 2026-06-03.* Search guild `1057790980327231609` / `#noble-quarter` threads panel when logged in. |
| **Transcript** | Not in `docs/discord-threads-raw.md` |
| **Adaptation** | Beats inferred from title + `docs/toa-dialogue-style.md` (Case 3–4 attachment: devotion/hunger, not named love until Case 5) + `docs/kaoru-dialogue-style.md` (deflect, proprietary warmth, walked-back honesty) |

When the thread URL is confirmed, add a row to `docs/discord-thread-index.md`.

---

## Eligibility — `all_romance_routes_complete()`

Defined in `game/case_endings.rpy` (`init python`).

**Meaning:** All major canon romance beats **in one playthrough**, not every optional branch.

| Requirement | Flag / condition |
|-------------|------------------|
| Canon romance base | `canon_first_scene`, `live_in_companion`, `kaoru_submission >= 2` |
| Case 1 romance | `case1_romance_seen` (trust **or** sponsorship **or** default — router picks one) |
| Case 2 festival | `case2_festival_seen` (kiss-only **or** intimate both qualify) |
| Case 2 morning | `case2_romance_seen` |
| Case 3 rescue | `case3_kaoru_rescue` (menu: trust Kaoru at shelf fall) |
| Case 4 defend | `case4_kaoru_defended` (supper table: stand beside his chair) |
| No Case 3/4 bad ends | `not case3_bad_end_injury`, `not case4_bad_end_abandoned`, `not case4_toa_slain` |

**Not required:** Both Case 1 trust and sponsorship routes (mutually exclusive per run).  
**Not required:** `case2_festival_intimate` specifically.

Helper: `case4_date_interlude_eligible()` = `all_romance_routes_complete()` and not `case4_date_interlude_seen`.

---

## Flags

| Flag | Set when |
|------|----------|
| `case4_date_interlude_seen` | Interlude starts |
| `is_this_a_date_asked` | Player chooses "Press the question" or late menu "Ask anyway" |

---

## Beats (shipped)

1. Office — Kaoru maps canal walk (field inspection framing).
2. CG canal walk — skewers, proprietary *I remember what I pay for*.
3. CG hopeful two-shot — menu: play along **or** press *Is this a date?*
4. If pressed — Kaoru denies (custody / lanterns); Toa hides ache (unnamed disappointment).
5. CG almost hands — *If this were a date I would have sent a clerk* → walked back to fatigue / Case Five.
6. Optional late ask if player played along first.
7. Return to office — no bad end.

---

## CGs

| File | Tag |
|------|-----|
| `images/cg/cg-case4-date-canal-walk.png` | `case4_date_canal_walk` |
| `images/cg/cg-case4-date-toa-hopeful.png` | `case4_date_toa_hopeful` |
| `images/cg/cg-case4-date-almost-hands.png` | `case4_date_almost_hands` |

Defs: `game/images/cgs-case4-date.rpy`. Gallery: Canon Romance — Cases 1 & 2 group (Case 4 slots appended).

---

## Playtest (console)

```renpy
$ canon_first_scene = True
$ live_in_companion = True
$ kaoru_submission = 3
$ case1_romance_seen = True
$ case2_festival_seen = True
$ case2_romance_seen = True
$ case3_kaoru_rescue = True
$ case4_kaoru_defended = True
$ case4_closed = True
$ case4_date_interlude_seen = False
jump case4_is_this_a_date_interlude
```

Full vertical slice from Case 2 close: canon play through Cases 1–4 with romance menus as documented above; confirm interlude auto-plays after supper defend.
