# Prologue Choice CG Map

Generated placeholder event CGs for every distinct prologue choice outcome in `game/prologue.rpy`.  
Assets live in `game/images/cg/cg-choice-*.png`; Ren'Py tags in `game/images/cgs-choices.rpy`.

**Art anchors:** Toa — black kimono (not furisode), gold Kakita crane obi, white hakama, white hair/eyelashes. Kaoru — gold/maroon magistrate robes, faces right. Office — Emerald Magistrate jade chrysanthemum wall hanging (not Crane mon on wall). PG-13/M.

---

## Summary

| Count | Notes |
|-------|-------|
| **21 CGs** | Matches all implemented prologue menus |
| **0 shared** | Each variant has its own image (no merges) |

**Not in script (analysis only):** Documents (display/surrender), status bluff, refuse shut door — omitted; prologue implements fewer menus than full RP analysis.

---

## Choice moment → CG → script mapping

### 1. After door slam (`prologue_door_menu` → `door_response`)

| Menu label | Script var | Ren'Py image tag | File |
|------------|------------|------------------|------|
| Leave and find another office. | `leave` | `cg choice door leave` | `cg-choice-door-leave.png` |
| Knock again, properly this time. | `knock_again` | `cg choice door knock again` | `cg-choice-door-knock-again.png` |
| Wait quietly until invited. | `wait_quietly` | `cg choice door wait quietly` | `cg-choice-door-wait-quietly.png` |

*Note:* `leave` loops via `prologue_door_return`; CG depicts the leave beat before return.

---

### 2. Formality (`prologue_formality_menu` → `formality_tone`)

| Menu label | Script var | Ren'Py image tag | File |
|------------|------------|------------------|------|
| Hyper-formal address. | `hyper_formal` | `cg choice formality hyper formal` | `cg-choice-formality-hyper-formal.png` |
| Direct and plain. | `direct` | `cg choice formality direct` | `cg-choice-formality-direct.png` |
| Light humor, carefully. | `humorous` | `cg choice formality humorous` | `cg-choice-formality-humorous.png` |

---

### 3. Entering office (`prologue_enter_office_menu` → `discipline_check`)

| Menu label | Script var | Ren'Py image tag | File |
|------------|------------|------------------|------|
| Comply — eyes forward, no wandering. | `discipline_check = 0` | `cg choice office comply` | `cg-choice-office-comply.png` |
| Peek at the shelves anyway. | `discipline_check = 1` | `cg choice office peek shelves` | `cg-choice-office-peek-shelves.png` |

---

### 4. Expired permit (`prologue_expired_menu` → `permit_strategy`)

| Menu label | Script var | Ren'Py image tag | File |
|------------|------------|------------------|------|
| Accept the Academy trip. | `academy_trip` | `cg choice permit academy trip` | `cg-choice-permit-academy-trip.png` |
| Push for a local fix. | `local_fix` | `cg choice permit local fix` | `cg-choice-permit-local-fix.png` |
| Plead — she has nowhere else. | `plead` | `cg choice permit plead` | `cg-choice-permit-plead.png` |

---

### 5. Before dance (`prologue_before_dance_menu`)

| Menu label | Script flag / stat | Ren'Py image tag | File |
|------------|-------------------|------------------|------|
| Negotiate terms first. | `insight += 1` | `cg choice dance negotiate` | `cg-choice-dance-negotiate.png` |
| Perform immediately. | `performance_boldness += 1`, `compliance += 1` | `cg choice dance immediate` | `cg-choice-dance-immediate.png` |
| Refuse — this isn't justice. | `prologue_refused_dance = True` | `cg choice dance refuse` | `cg-choice-dance-refuse.png` |

---

### 6. Performance tone (`prologue_performance_menu` → `performance_boldness`)

| Menu label | Script effect | Ren'Py image tag | File |
|------------|---------------|------------------|------|
| Formal fan dance — maiden narrative, bells on obijime. | baseline / formal | `cg choice performance formal` | `cg-choice-performance-formal.png` |
| Flirtatious read — small audience, coquette sway. | `performance_boldness += 2` | `cg choice performance flirtatious` | `cg-choice-performance-flirtatious.png` |

---

### 7. Escalation at grab (`prologue_grab_menu`)

| Menu label | Script effect | Ren'Py image tag | File |
|------------|---------------|------------------|------|
| Rebuke him — pull back. | `rebuke += 2` | `cg choice grab rebuke` | `cg-choice-grab-rebuke.png` |
| Lean into the moment — don't break the spell. | `physical_initiative += 1`, `compliance += 2` | `cg choice grab lean in` | `cg-choice-grab-lean-in.png` |

---

### 8. Final "unless?" (`prologue_unless_menu` → `unless_branch`)

| Menu label | Script var | Ren'Py image tag | File |
|------------|------------|------------------|------|
| Answer verbally — name what you want in return. | `verbal` | `cg choice unless verbal` | `cg-choice-unless-verbal.png` |
| Answer physically — close the distance. | `physical` | `cg choice unless physical` | `cg-choice-unless-physical.png` |
| Walk out — this crossed a line. | `walk_out` | `cg choice unless walk out` | `cg-choice-unless-walk-out.png` |

---

## Shared CGs

None — each choice outcome has a dedicated image.

---

## Existing beat CGs (not choice-specific)

From `cgs-first-scene.rpy` — used in script for shared beats regardless of branch:

| Tag | File | Used at |
|-----|------|---------|
| `cg corridor_lost` | `cg-first-scene-corridor-lost.png` | Prologue open |
| `cg permit_desk` | `cg-first-scene-permit-desk.png` | Permit book on desk |
| `cg office_dance` | `cg-first-scene-office-dance.png` | Dance scene entry |
| `cg chair_tension` | `cg-first-scene-chair-tension.png` | Unless cliffhanger setup |

Choice CGs above are ready to `show` after each `$` assignment when script is wired to branch visuals.

---

## Even-turn beat CGs (removed)

The automatic even-turn beat CG overlay system was removed in May 2026. See `docs/cg-beat-map.md` for historical map/art reference. Dedicated scene and choice-branch CGs are unchanged.

---

## Source paths

| Location | Purpose |
|----------|---------|
| `assets/cg-choice-*.png` (Cursor project assets) | Generation source |
| `ryoko-owari/game/images/cg/cg-choice-*.png` | Ren'Py runtime copies |
