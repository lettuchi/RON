# Case 4 — The Dock Ledger (剣の帳 / *Ledger at the Blade's Edge*)

**Script:** `game/case4_investigation.rpy`  
**Entry:** `case3_milestone_end` → `case4_post_case3_bridge` → `case4_investigation_start`  
**Prior:** Case Three pinned (fabric shop / bolt room); `case3_closed = True` recommended for bridge dialogue

**Tone:** Very dark, gritty. Investigation climax vs suspect **Kurogane** (warehouse foreman, Scorpion-trained).

---

## Outcome

- **Romance path:** Toa trusts Kaoru at sword crisis → `case4_kaoru_defended`, custody taken, protective beat (honest then cold correction).
- **Bad end:** Toa fights alone → implied death → Game Over **「剣の果て」**.
- **Milestone:** `case4_closed = True`; Case Five tease (pleasure-quarter seal).

---

## Beat list

| # | Beat | Visual |
|---|------|--------|
| 1 | Bridge from Case Three | `case4_post_case3_bridge` |
| 2 | Dock briefing | `bg dock_raid`, sprites |
| 3 | Establishing | `cg-case4-gritty-establishing.png` |
| 4 | **Menu** `case4_investigation_menu` | investigation stub |
| 5 | Confrontation — Kurogane | `bg dock_raid` |
| 6 | Dual swordfight | `cg-case4-fight-wide.png` |
| 7 | **Menu** `case4_swordfight_crisis_menu` | fight crisis |
| 8a | Romance defend | `cg-case4-romance-defend.png` → `case4_milestone_end` |
| 8b | Bad end | content warning → `cg-case4-bad-slayn.png` → Game Over |
| 9 | Close + Case Five tease | `bg magistrate_office`, `return` |

---

## Menus

### `case4_investigation_menu`

| Choice | Effect |
|--------|--------|
| Read split crate (wax / Scorpion thread) | +1 insight |
| Question watchman | +1 composure, +1 honor, `case4_suspect_named`, name Kurogane |
| Cover stairs; defer to Kaoru | +1 compliance, +1 kaoru_submission |

If suspect not named, Kaoru names **Kurogane** before confrontation.

### `case4_swordfight_crisis_menu`

| Choice | Label | Flags |
|--------|-------|-------|
| *"Stay behind me, Magistrate-sama—"* | `case4_romance_kaoru_defends` | `case4_kaoru_defended` |
| *"I'll cut him down myself."* | `case4_bad_end_toa_slain` | `case4_toa_slain`, `seen_gameover_case4` |

Bad end uses project content-warning menu pattern before CG.

---

## Flags (`game/stats.rpy`)

`case4_started`, `case4_suspect_named`, `case4_suspect_name`, `case4_toa_slain`, `case4_kaoru_defended`, `case4_closed`

---

## CGs

| File | Ren'Py tag |
|------|------------|
| `cg-case4-gritty-establishing.png` | `case4_gritty_establishing` / `bg dock_raid` |
| `cg-case4-fight-wide.png` | `case4_fight_wide` |
| `cg-case4-romance-defend.png` | `case4_romance_defend` |
| `cg-case4-bad-slayn.png` | `gameover_case4_slayn` |

Defs: `game/images/cgs-case4.rpy`. Gallery: Case 4 group + bad end + romance slots.

---

## Quick test — romance end

```renpy
$ case3_closed = True
$ live_in_companion = True
$ canon_first_scene = True
jump case4_post_case3_bridge
```

At `case4_swordfight_crisis_menu`, choose **Stay behind me, Magistrate-sama—**.

Or jump directly:

```renpy
jump case4_romance_kaoru_defends
```

---

## Quick test — bad end

```renpy
$ case3_closed = True
jump case4_swordfight
```

Choose **I'll cut him down myself.** → confirm content warning → Game Over **「剣の果て」**.

Or:

```renpy
jump case4_bad_end_toa_slain
```

---

## Full chain from Case 2 (when Case 3 not skipped)

```renpy
$ case1_closed = True
$ case2_closed = True
$ live_in_companion = True
$ canon_first_scene = True
jump case3_investigation_start
```

Play through to Case Four automatically after `case3_milestone_end`.
