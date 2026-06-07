# Case 2 — The Academy Packet (便りの灰 / *Ashes of the Good Tidings*)

**Script:** `game/case2_investigation.rpy`  
**Entry:** `case1_barge_milestone_end` → `case2_investigation_start`  
**Prior:** Case One closed (`case1_closed`); Jiro murder resolved; barge manifest seized

---

## Outcome

- Crane Academy credential packet for Toa burned; courier **Tsubaki** dead in warehouse alley.
- Links to Case One Scorpion factor thread (kiln boy, clerk confession).
- Emergency duplicate charter issued; `case2_closed = True`, `case2_milestone = "case2_closed"`.

---

## Beat list

| # | Beat | Visual |
|---|------|--------|
| 1 | Office briefing — Case Two | `bg magistrate_office`, sprites |
| 2 | **Menu 1** `case2_briefing_menu` | `cg-case2-academy-desk.png` |
| 3 | Warehouse alley / kiln | `bg street_exterior` (warehouse_district alias available) |
| 4 | **Menu 2** `case2_alley_menu` | `cg-case2-alley-courier.png` |
| 5 | Outer desk — routing slip | `bg magistrate_office` |
| 6 | **Menu 3** `case2_desk_menu` | `cg-case2-warehouse-ash.png` |
| 7 | Resolution — duplicate charter | office sprites; `return` |

---

## Menus

### `case2_briefing_menu`

| Choice | `case2_briefing_choice` | Stats |
|--------|-------------------------|-------|
| Study courier route | `route` | +2 insight |
| Who profits politically | `politics` | +1 honor, +1 insight |
| Witness statements only | `witnesses` | +2 composure, +1 honor |

### `case2_alley_menu`

| Choice | `case2_scene_choice` | Stats |
|--------|----------------------|-------|
| Sift ash for Crane mon | `ash` | +2 insight, `case2_packet_found` |
| Examine body site | `body` | +1 insight, +1 composure, names Tsubaki |
| Question kiln boy | `runner` | +1 perf_boldness, +1 insight |

### `case2_desk_menu`

| Choice | `case2_confront_choice` | Stats |
|--------|-------------------------|-------|
| Accuse clerk aloud | `accuse` | +2 honor, +1 kaoru_resistance |
| Decoy trap | `trap` | +2 insight, +1 composure |
| Defer to Kaoru | `defer` | +1 compliance, +1 kaoru_submission |

---

## Flags (`game/stats.rpy`)

`case2_briefing_choice`, `case2_scene_choice`, `case2_confront_choice`, `case2_courier_name`, `case2_packet_found`, `case2_milestone`, `case2_closed`

---

## CGs

| File | Use |
|------|-----|
| `cg-case2-academy-desk.png` | Briefing menu |
| `cg-case2-alley-courier.png` | Alley menu |
| `cg-case2-warehouse-ash.png` | Desk menu |

---

## Quick test

```renpy
$ case1_closed = True
$ live_in_companion = True
$ case1_victim_name = "Miya Jiro"
jump case2_investigation_start
```

Or full Case 1 finale:

```renpy
jump case1_barge_start
```
