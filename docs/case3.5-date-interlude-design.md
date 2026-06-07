# Case 3.5 interlude — "Is this a date?"

**Script:** `game/case3_5_date_interlude.rpy`  
**Label:** `case3_5_is_this_a_date_interlude` (alias: `case4_is_this_a_date_interlude` in `case4_date_interlude.rpy`)  
**Entry:** `case3_milestone_end` → `case3_post_case3_bridge` when `romance_through_case3_complete()` and not `case4_date_interlude_seen`.  
**Exit:** `case4_post_case3_bridge` → Case 4 dock raid.

---

## Discord source

| Field | Value |
|-------|--------|
| **Thread title** | Is this a date? |
| **URL** | https://discord.com/channels/1057790980327231609/1496697813835190272 |
| **Channel** | `#teardrop-island` (parent `1141618624814129173`) |
| **Transcript** | `docs/discord-threads-raw.md` § **Is this a date?** (browser 2026-06-03) |
| **Plot guide** | `docs/plot-guide-is-this-a-date.md` |
| **Adaptation** | VN port (2026-06-03 rewrite): Tear Drop kaiseki, dance expertise, gossip reassurance, optional IC date question; island path replaces canal compression |

---

## Eligibility — `romance_through_case3_complete()`

Defined in `game/case_endings.rpy` (`init python`).

**Meaning:** Canon romance beats through Case 3 in one playthrough (gates Case 3.5 only — **not** Case 4 defend).

| Requirement | Flag / condition |
|-------------|------------------|
| Canon romance base | `canon_first_scene`, `live_in_companion`, `kaoru_submission >= 2` |
| Case 1 romance | `case1_romance_seen` |
| Case 2 festival | `case2_festival_seen` |
| Case 2 morning | `case2_romance_seen` |
| Case 3 rescue | `case3_kaoru_rescue` |
| No Case 3 bad end | `not case3_bad_end_injury` |

**Not required:** `case4_kaoru_defended` (comes **after** this interlude in story order).

Helper: `case3_5_date_interlude_eligible()` = `romance_through_case3_complete()` and not `case4_date_interlude_seen`.  
Alias: `case4_date_interlude_eligible()` (legacy name).

`all_romance_routes_complete()` = through Case 3 **plus** `case4_kaoru_defended` (full run through dock defend).

---

## Flags

| Flag | Set when |
|------|----------|
| `case4_date_interlude_seen` | Interlude starts (legacy save name for Case 3.5) |
| `is_this_a_date_asked` | Player asks on island walk or late almost-hands menu |

---

## Beats (shipped — 2026-06-03 rewrite)

1. **Act I — Invitation & crossing:** Wax-sealed instructions (Tear Drop Island, inn between geisha houses, wear your best); furisode prep CG; ferry / island night.
2. **Act II — Arrival:** Private buyout shock; hojicha; tatami lanterns; stiff-obi bow; fragrance callback.
3. **Act III — Kaiseki:** Appreciation without *thank you*; seasonal courses; sake kampai; meal menu (eat vs early label press).
4. **Act IV — Dance:** Ensemble; *dance crimes* line; menu (quiet delight vs body-reading lecture); trust overshare → *I know.*
5. **Act V — Gossip:** Hiromi / Doji Sango; rumor delight; *Never once. You are very well loved in this city.*; dessert.
6. **Act VI — Island path:** Optional IC *Is this a date?* (player reward); deflection + walked-back almost-admission; almost-hands CG; late ask menu.
7. **Act VII — Return:** Magistrate compound; ache unnamed (devotion, not love confession); `case4_post_case3_bridge`. **No bad end.**

**Attachment arc:** Post–Case 3 devotion + physical awareness; reassurance lands; romance vocabulary still deflected IC.

---

## CGs

| File | Tag |
|------|-----|
| `images/cg/cg-case3_5-date-island-night.png` | `case3_5_date_island_night` |
| `images/cg/cg-case3_5-date-inn-exterior.png` | `case3_5_date_inn_exterior` |
| `images/cg/cg-case3_5-date-tatami-lanterns.png` | `case3_5_date_tatami_lanterns` |
| `images/cg/cg-case3_5-date-kaiseki.png` | `case3_5_date_kaiseki` |
| `images/cg/cg-case3_5-date-sake-cup.png` | `case3_5_date_sake_cup` |
| `images/cg/cg-case3_5-date-silk-fabric.png` | `case3_5_date_silk_fabric` |
| `images/cg/cg-case3_5-date-candle-flame.png` | `case3_5_date_candle_flame` |
| `images/cg/cg-case3_5-date-toa-lashes.png` | `case3_5_date_toa_lashes` |
| `images/cg/cg-case3_5-date-kaoru-hand-cup.png` | `case3_5_date_kaoru_hand_cup` |
| `images/cg/cg-case3_5-date-almost-hands.png` | `case3_5_date_almost_hands` |
| `images/cg/cg-case3_5-date-toa-watching.png` | `case3_5_date_toa_watching` |
| `images/cg/cg-case3_5-date-duo-table.png` | `case3_5_date_duo_table` |
| `images/cg/cg-case3_5-date-gossip-shadow.png` | `case3_5_date_gossip_shadow` |
| `images/cg/cg-case3_5-date-reassurance.png` | `case3_5_date_reassurance` |

Defs: `game/images/cgs-case3_5-date.rpy` (legacy `case4_date_*` tags alias to new art). Gallery: **Case 3.5 — Is this a date?** (14 entries).

Backup: `game/versions/case3_5-date-rewrite-2026-06-03/`

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
$ case3_closed = True
$ case4_date_interlude_seen = False
$ is_this_a_date_asked = False
jump case3_5_is_this_a_date_interlude
```

Full chain: play Cases 1–3 with romance menus → `case3_milestone_end` → interlude auto-plays → dock raid.

**Unvoiced:** ~87 character lines + ~38 narrator blocks (~442 script lines; manifest pass pending).
