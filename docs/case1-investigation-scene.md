# Case 1 — Investigation opening (canal body)

**Script:** `game/case1_investigation.rpy`  
**Entry:** `case1_investigation_hook` / `case1_noncanon_start` → `case1_investigation_start`  
**Prior:** Companion offer signed (canon) or three-week non-canon return

---

## Canon outcome (Milestone B)

- Kaoru briefs **Case One**: body recovered from noble-quarter canal; report wrongness (borrowed haori, Miya retainer knot, blank name line).
- Office report review → walk to canal (no beat CGs; `bg street_exterior` + sprites only).
- Canal: physical clues, low-key supernatural unease (wrong water color, peeled-charm air).
- **Victim identified:** `Miya Jiro` — guest-house ledger clerk via courier chit in haori lining.
- **Physical clue:** Scorpion mon comb (`case1_physical_clue = "scorpion_comb"`, `case1_clue_found = True`).
- Ends at **`case1_investigation_milestone_end`** with `case1_milestone = "miya_guest_registry_next"` → `return`.

---

## Beat list

| # | Beat | Visual / audio |
|---|------|----------------|
| 0 | **Five-case week sprung** (canon: `case1_investigation_hook`; non-canon: `case1_noncanon_start`) | `bg magistrate_office`; voice `kaoru_328`–`333`, `toa_277`/`279`, `narrator_270` |
| 1 | Archive return (canon vs non-canon bridge) | `bg corridor`, `bgm_corridor`, footsteps |
| 2 | Office briefing — patronage→case callback, then Case One docket | `kaoru_330`, `toa_278`; then `kaoru_120`+ |
| 3 | Miya retainer / live-in vs cold dynamic | Sprites; `live_in_companion` branches |
| 4 | **Menu 1** — report focus | `case1_briefing_menu` |
| 5 | Departure through inner hall | `bg magistrate_hall`, `bgm_street` |
| 6 | Street walk — charm unease, crow sign | `bg street_exterior` |
| 7 | Canal arrival — body on pallet, clerk | Sprites only (no `cg case1_canal_body` until art exists) |
| 8 | **Menu 2** — what to examine first | `case1_canal_menu` |
| 9 | Kaoru one-sentence probe | **Menu 3** — `case1_kaoru_probe_menu` |
| 10 | Scorpion comb + haori chit → **Miya Jiro** | paper SFX; flags set |
| 11 | Office return — name on docket, next lead | `bg magistrate_office`, `return` |

---

## Choice menus

### `case1_briefing_menu` (office — what to study first)

| Choice | `case1_briefing_choice` | Stats |
|--------|-------------------------|-------|
| Study victim summary | `detail` | +2 insight |
| Ask who benefits politically | `politics` | +1 honor, +1 insight |
| Witness notes only | `professional` | +2 composure, +1 compliance |

### `case1_canal_menu` (canal — what to examine first)

| Choice | `case1_scene_choice` | Stats | Observation tag |
|--------|----------------------|-------|-----------------|
| Hands and sleeves | `observe` | +2 insight | `ink_and_hem` |
| Throat vs drowning report | `ask_kaoru` | +1 insight, +1 kaoru_resistance | `throat_bruise` |
| Signed minimum only | `professional` | +2 composure, +1 honor | `signed_minimum` |

### `case1_kaoru_probe_menu` (canal — respond to Kaoru's test)

| Choice | `case1_probe_response` | Stats |
|--------|------------------------|-------|
| Answer eagerly with theory | `eager` | +1 insight, +1 performance_boldness |
| Defer professionally | `defer` | +2 composure, +1 compliance |
| Push back on humiliation | `pushback` | +1 honor, +1 kaoru_resistance |

Briefing choice colors Kaoru's comb reaction lines. Probe choice colors post-identification banter.

---

## Flags (`game/stats.rpy`)

| Flag | Purpose |
|------|---------|
| `case1_briefing_choice` | Office menu tag |
| `case1_scene_choice` | Canal examine menu tag |
| `case1_probe_response` | Kaoru probe menu tag |
| `case1_observation` | Physical observation tag |
| `case1_victim_hint` | `miya_retainer` from briefing |
| `case1_victim_name` | `"Miya Jiro"` after chit |
| `case1_physical_clue` | `"scorpion_comb"` |
| `case1_clue_found` | True after comb secured |
| `case1_milestone` | `"miya_guest_registry_next"` |

---

## Non-canon path

**Label:** `case1_investigation_noncanon_bridge` when `live_in_companion` is False  
- Colder Kaoru (`kaoru cold`, `cruel`).  
- No adjoining-chamber warmth; residency still conditional on surviving the week.  
- Shares `case1_investigation_assign` trunk and canal scene with conditional dialogue.

---

## Voice tags (not yet recorded)

- **Toa:** `toa_102`–`toa_128`
- **Kaoru:** `kaoru_118`–`kaoru_160`

---

## How to test

### Canon playthrough

1. Start → prologue → physical **Unless?** → canon ending → **Three days later…**
2. Companion offer → sign → any first-duty choice → investigation plays through office → canal → office return.
3. Confirm: `live_in_companion`, `case1_victim_name == "Miya Jiro"`, `case1_clue_found`, `case1_milestone == "miya_guest_registry_next"`.

### Quick jump (Ren'Py shell)

```renpy
$ canon_first_scene = True
$ live_in_companion = True
$ companion_accept_tone = "graceful"
jump case1_investigation_start
```

Non-canon:

```renpy
$ unless_branch = "walk_out"
$ live_in_companion = False
jump case1_investigation_start
```

---

## Labels

| Label | Role |
|-------|------|
| `case1_investigation_start` | Reset flags; canon vs non-canon fork |
| `case1_investigation_noncanon_bridge` | Cold archive return |
| `case1_investigation_assign` | Office briefing + menu 1 |
| `case1_investigation_departure` | Hall → street |
| `case1_investigation_canal` | Canal scene + menus 2–3 + identification |
| `case1_investigation_milestone_end` | Comb/name on docket; sets `miya_guest_registry_next` → jumps into continuation |

---

## Continuation (day two) — guest registry / licensed quarter (Milestone C)

`case1_investigation_milestone_end` now jumps to `case1_registry_start` instead of returning.

- **Lacquered Plum** guest house in the licensed quarter (rain, wine-red lanterns, cedar stilts over the canal).
- **Geisha witness:** `Suzu` (`case1_witness_name = "Suzu"`) — knew Jiro, identifies the comb.
- **Comb traced** to a Scorpion patron who books the river room under the **"Chrysanthemum"** cipher (`case1_comb_owner = "chrysanthemum_patron"`, `case1_appointment_cipher = "chrysanthemum"`).
- **Forged Emerald writ** in the high-tide registry (`case1_forged_seal = True`) — sixteen-petal mon vs the office's fourteen.
- **Confrontation:** a Scorpion trade **Factor** demands the registry; Kaoru stares him down; he retreats with a high-tide warning.
- Ends at `case1_registry_milestone_end` with **`case1_milestone = "chrysanthemum_barge_next"`** → `return`.

### Continuation labels

| Label | Role |
|-------|------|
| `case1_registry_start` | Day-two office briefing + companion beat; **Menu 4** `case1_registry_menu` (approach) |
| `case1_guest_house` | Licensed quarter → Plum; okami + Suzu; comb traced; **Menu 5** `case1_witness_menu` |
| `case1_interrogation` | High-tide registry, forged seal reveal, Scorpion Factor standoff; **Menu 6** `case1_ledger_menu` |
| `case1_registry_milestone_end` | Kaoru companion beat + high-tide barge cliffhanger; `return` |

### Continuation menus

- **`case1_registry_menu`** → `case1_registry_approach` ∈ {`credentials` (+honor,+composure), `quiet` (+2 insight,+perf_boldness), `kaoru_lead` (+2 composure,+compliance,+kaoru_submission)}.
- **`case1_witness_menu`** → `case1_witness_handle` ∈ {`gentle` (+2 insight,+honor; deeper lead if `case1_registry_approach == "quiet"`), `press` (**gated on `case1_observation == "throat_bruise"`**; +insight,+composure), `loom` (+composure,+compliance,+kaoru_submission)}.
- **`case1_ledger_menu`** → `case1_ledger_choice` ∈ {`record` (+2 honor,+kaoru_resistance; Kaoru reaction varies on `case1_briefing_choice`), `copy` (+2 insight,+composure), `trust` (+composure,+compliance,+kaoru_submission; warmer if `kaoru_submission >= 2`)}.
- Final companion beat branches on `live_in_companion`, then `kaoru_resistance >= 2` vs `kaoru_submission >= 2`.

### New flags (`game/stats.rpy`)

`case1_registry_approach`, `case1_witness_name`, `case1_witness_handle`, `case1_comb_owner`, `case1_appointment_cipher`, `case1_forged_seal`, `case1_ledger_choice`.

### New background aliases (`game/images/backgrounds.rpy`)

- `bg licensed_quarter` (placeholder = `street_exterior.png`) — rainy lantern-lit pleasure-district canal.
- `bg guest_house_room` (placeholder = `magistrate_office.png`) — Lacquered Plum tatami interior.

### New CGs needed (placeholders wired; parent to generate)

Pre-choice moment CGs (`case1_registry_menu`, `case1_witness_menu`, `case1_ledger_menu`) currently reuse existing art. Dedicated art to generate (prompts in `game/images/cgs-choice-moments.rpy`):

- `cg-case1-licensed-quarter.png` — rainy canal pleasure district, the Lacquered Plum on stilts, three-eyed crow sign.
- `cg-case1-guesthouse-suzu.png` — frightened geisha Suzu with the Scorpion comb; Toa kneeling at her level; Kaoru looming.
- `cg-case1-registry-ledger.png` — open registry, forged Emerald wax seal (too many petals), comb in evidence tray, foreign silver.

---

## Finale — high-tide barge (Milestone D)

`case1_registry_milestone_end` → `case1_barge_start` → `case1_barge_milestone_end` → `case2_investigation_start`.

| Label | Role |
|-------|------|
| `case1_barge_start` | Dock approach; **Menu 7** `case1_barge_menu` |
| `case1_barge_boarding` | Seize manifest (false rice / true resin) |
| `case1_barge_milestone_end` | Case One closed; hooks Case Two |

### `case1_barge_menu`

| Choice | `case1_barge_approach` | Stats |
|--------|------------------------|-------|
| Board under cover | `stealth` | +2 insight, +1 performance_boldness |
| Board as the law | `official` | +2 honor, +1 composure |
| Kaoru distracts, Toa copies | `split` | +1 insight, +1 kaoru_submission, +1 compliance |

### New flags

`case1_barge_approach`, `case1_manifest_seized`, `case1_closed`

### Barge CGs

- `cg-case1-high-tide-barge.png` — menu / dock
- `cg-case1-barge-confrontation.png` — boarding beat art reference

---

## Future milestones

- **Chrysanthemum unmasked** — patron still at large after barge.
- **Watch testimony rewrite** — drowning vs strangulation politics.
- **Internal seal thief** — ties Case One forgery to Case Two desk leak.
