# Case Zero · Kaoru pro-prologue design

**Script:** `game/kaoru_pro_prologue.rpy`  
**Novel:** `docs/novel/ryoko-owari-case-zero.md`  
**CG defs:** `game/images/cgs-case-zero.rpy`  
**Play:** Dev menu → **Pro-prologue, Case Zero (Kaoru)**  
**Gallery:** Extra section only (2 CGs unlock via `show_cg_scene`; not on main new-game route until shipped).  
**Exit:** `jump prologue_start`

---

## Beat map (single combined narrative)

| # | Beat | Motif | POV | Key props |
|---|------|-------|-----|-----------|
| 0 | Title + redacted SUMMARY ONLY | Case Zero docket | Bureaucratic narrator | Black bars, seal, recommendation line |
| 1 | Three mornings montage | Empty tea cups ×3, renewal spike | Third / Kaoru | Cups, drowning report, ledger blank |
| 2 | Almost-smile inventory | Denied mouth entries | Kaoru speaks to empty office | Scrap list, mikan/kotatsu foreshadow |
| 2b | Menu (optional) | Player tone | Kaoru | Work vs rain |
| 3 | Runner POV (04:17–04:31) | Shoji crack, no reader address | Third only (boy) | Summons, stamp, three deliveries |
| 4 | Window puppet show | Wrong villain motive | Kaoru at sill | Puppet crate, canal stage |
| 4b | Menu (optional) | Cite vs watch | Kaoru | Obstruction chit |
| 5 | Rain alley mirror | Bad-end geography, door closed | Third + Kaoru | Tea-house alley, okami fee chit |
| 6 | Return + bridge | Predator aftercare, dread | Kaoru | Wash basin, four cups, footsteps |
| 7 | Transition | Echo prologue lines | Kaoru (off-screen) | Wrong door → `prologue_start` |

**Runtime target:** ~15–25 min VN read (93 voiced lines + pauses/CGs).

---

## Foreshadow table

| Case Zero seed | Pays off in |
|----------------|-------------|
| Three empty tea cups | Case 1.5 shoji tea, curry kitchen |
| Mikan / kotatsu denied | Epilogue bonus almost-smile, mikan peel |
| Almost-smile inventory | Epilogue: *You may almost smile if you try* |
| Puppeteer wrong motive | Prologue audition: dancer vs reason |
| "Dancer arrives with tea" (no name) | Case 1.5, companion corridor |
| Alley = brothel GO geometry | `prologue_bad_end_brothel`, rain game over |
| Door closed / fee line | Kaoru harsh mercy, quarter arithmetic |
| Renewal spike notice | Prologue permit crisis |
| Footsteps + wrong door echo | `prologue_start` first beats |
| `persistent.play_case_zero` gate (comment) | Optional pre-prologue on new game |

---

## Voice ID plan

**Allocated range (next free after kaoru_386 / narrator_311):**

| ID range | Count | Character | Notes |
|----------|-------|-----------|-------|
| `narrator_312`–`narrator_365` | 54 | narrator | Docket voice + third-person beats |
| `kaoru_387`–`kaoru_425` | 39 | kaoru | Conversational magistrate; no koans |

**Total new IDs:** 93  
**ElevenLabs:** not run (stub manifests only).

### Sample IDs by beat

- **Docket:** `narrator_312`–`320`
- **Three mornings:** `narrator_321`–`325`, `347`–`349`, `kaoru_387`–`389`, `412`–`414`
- **Almost-smile:** `narrator_326`–`327`, `350`, `kaoru_390`–`395`, `415`–`417`
- **Runner:** `narrator_328`–`334`, `351`–`353`, `kaoru_396`, `418`–`419`
- **Puppet:** `narrator_335`–`338`, `354`, `kaoru_397`–`401`, `420`–`421`
- **Alley mirror:** `narrator_339`–`346`, `355`–`358`, `kaoru_402`–`405`, `422`–`423`
- **Bridge:** `narrator_359`–`365`, `kaoru_406`–`411`, `424`–`425`

---

## Menus (2)

1. `case_zero_smile_menu` — work vs watch rain (flavor only)
2. `case_zero_puppet_menu` — watch vs cite puppeteer (flavor only)

---

## CG placeholders

| Tag | File (to generate) | Beat |
|-----|-------------------|------|
| `case_zero_redacted_docket` | `images/cg/cg-case-zero-redacted-docket.png` | Opening docket |
| `case_zero_rain_alley_door` | `images/cg/cg-case-zero-rain-alley-door.png` | Bad-end mirror alley |

Prompts in `game/images/cgs-case-zero.rpy` header comments.

---

## Constraints checklist

- [x] No Toa on-page (no name, no silhouette)
- [x] No em dashes
- [x] Shameless predator tone (patronage, spendable witnesses) per `docs/kaoru-dialogue-style.md`
- [x] Default new game unchanged; dev menu + optional `persistent.play_case_zero` documented
- [x] Ends `jump prologue_start`
