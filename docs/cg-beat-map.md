# Prologue beat CG map (even turns)

> **Removed (2026-05):** The even-turn beat CG system (`cg_beats_helper.rpy`, `cgs-beats.rpy`, automatic `cg beat_NNN` overlays) was disabled and deleted. Dedicated scene CGs (`corridor_lost`, `permit_desk`, etc.) are unchanged. This doc is kept as historical art/reference only.

Each **spoken or narration block** in `game/prologue.rpy` = one turn (menus skipped).
**Even turns** (2, 4, 6…) show `cg beat_NNN` unless a dedicated scene CG fired within 5 script lines.

## Counts

| Metric | Value |
|--------|------:|
| Total dialogue turns | 215 |
| Even turns | 107 |
| Even turns needing beat CG | 99 |
| Skipped (dedicated scene CG nearby) | 8 |
| First half (through turn 147) needing CG | 68 |
| Batch 1 unique PNGs generated | 21 |
| Placeholder fallback | `cg-beat-placeholder.png` |

### Batch 1 + wiring

- **Unique art:** turns `004, 006, 008, 010, 012, 016, 018, 020, 022, 024, 026, 030, 036, 040, 050, 060, 070, 092, 100, 116, 136`
- **Helper:** `game/cg_beats_helper.rpy` (say callback); enabled in `prologue_start`, off before Case 1 `return`
- **Skip turns:** `{2, 14, 58, 112, 114, 164, 180, 184}`
- **Remaining first-half even turns:** 47 use placeholder until more `cg-beat-NNN.png` are added

## Dedicated scene CGs (skip beat on same beat)

| Tag | File |
|-----|------|
| `canon_afterglow` | (see `cgs-first-scene.rpy` / `cgs-canon-ending.rpy`) |
| `canon_proposition` | (see `cgs-first-scene.rpy` / `cgs-canon-ending.rpy`) |
| `canon_signing` | (see `cgs-first-scene.rpy` / `cgs-canon-ending.rpy`) |
| `canon_three_days` | (see `cgs-first-scene.rpy` / `cgs-canon-ending.rpy`) |
| `chair_tension` | (see `cgs-first-scene.rpy` / `cgs-canon-ending.rpy`) |
| `corridor_lost` | (see `cgs-first-scene.rpy` / `cgs-canon-ending.rpy`) |
| `office_dance` | (see `cgs-first-scene.rpy` / `cgs-canon-ending.rpy`) |
| `permit_desk` | (see `cgs-first-scene.rpy` / `cgs-canon-ending.rpy`) |

## Turn → beat CG (first half, not skipped)

| Turn | Line | Speaker | Text (excerpt) | File |
|-----:|-----:|---------|------------------|------|
| 4 | 24 | narrator | The noble quarter smells of ink and cedar. Somewhere be | `images/cg/cg-beat-004.png` |
| 6 | 35 | kaoru | Done complaining? | `images/cg/cg-beat-006.png` |
| 8 | 44 | kaoru | Wrong door. Again. | `images/cg/cg-beat-008.png` |
| 10 | 63 | toa | Third time's the charm. Or the magistrate. Hopefully bo | `images/cg/cg-beat-010.png` |
| 12 | 75 | kaoru | Still there? Knock if you want something. | `images/cg/cg-beat-012.png` |
| 16 | 94 | Clerk | That's the one who stamps interclan renewals. Good luck | `images/cg/cg-beat-016.png` |
| 18 | 101 | narrator | The corridor loops — of course it loops — and deposits  | `images/cg/cg-beat-018.png` |
| 20 | 119 | toa | Round two. Posture up. Smile optional. | `images/cg/cg-beat-020.png` |
| 22 | 131 | kaoru | Smarter the second time. Knock. | `images/cg/cg-beat-022.png` |
| 24 | 145 | kaoru | Enter. Since you can follow instructions when motivated | `images/cg/cg-beat-024.png` |
| 26 | 156 | toa | Honored sochira-no-kata, this unworthy petitioner begs  | `images/cg/cg-beat-026.png` |
| 28 | 164 | kaoru | At least your bow didn't wobble. Continue — briefly. | `images/cg/cg-beat-028.png` |
| 30 | 176 | kaoru | Plain speech. You waste less of my evening than most. | `images/cg/cg-beat-030.png` |
| 32 | 187 | toa | I promise I'm only lost geographically, not legally. Ma | `images/cg/cg-beat-032.png` |
| 34 | 195 | toa | Crane training says brave. Unicorn roads say stupid is  | `images/cg/cg-beat-034.png` |
| 36 | 203 | kaoru | Emerald Magistrate Kitsu Kaoru. You will use my title i | `images/cg/cg-beat-036.png` |
| 38 | 212 | kaoru | State your business. Briefly. | `images/cg/cg-beat-038.png` |
| 40 | 220 | toa | Post-gempukku, traveling from Unicorn lands. I mean to  | `images/cg/cg-beat-040.png` |
| 42 | 228 | toa | The roads taught me flexibility. The Crane taught me po | `images/cg/cg-beat-042.png` |
| 44 | 237 | kaoru | Flexibility. Good. You'll need it — this city bends peo | `images/cg/cg-beat-044.png` |
| 46 | 246 | kaoru | Interclan residence requires Emerald approval. You knew | `images/cg/cg-beat-046.png` |
| 48 | 254 | kaoru | It does. Door. | `images/cg/cg-beat-048.png` |
| 50 | 263 | narrator | Toa keeps her gaze on the desk. Not on the shelves line | `images/cg/cg-beat-050.png` |
| 52 | 273 | narrator | Her eyes snag on a row of scrolls — Lion mon here, Emer | `images/cg/cg-beat-052.png` |
| 54 | 281 | toa | Yes, Magistrate. | `images/cg/cg-beat-054.png` |
| 56 | 289 | kaoru | Cushion. Desk. You stand too much for someone begging f | `images/cg/cg-beat-056.png` |
| 60 | 306 | toa | They should be current. I checked before leaving— | `images/cg/cg-beat-060.png` |
| 62 | 314 | toa | If I cannot renew locally, they'll send me back to the  | `images/cg/cg-beat-062.png` |
| 64 | 327 | kaoru | How obedient. The Unicorn taught you to yield before th | `images/cg/cg-beat-064.png` |
| 66 | 335 | kaoru | Unfortunately for your travel plans, I'm not finished w | `images/cg/cg-beat-066.png` |
| 68 | 347 | kaoru | Requirements. Finally, a useful word. | `images/cg/cg-beat-068.png` |
| 70 | 355 | toa | Almost is a start. I dance for a living — I know how to | `images/cg/cg-beat-070.png` |
| 72 | 366 | kaoru | Tragic. Continue. | `images/cg/cg-beat-072.png` |
| 74 | 374 | kaoru | A curry shop and borrowed bedding. Ryoko Owari's finest | `images/cg/cg-beat-074.png` |
| 76 | 382 | kaoru | We'll see what it's worth. | `images/cg/cg-beat-076.png` |
| 78 | 399 | toa | Only the inn, a pony that needs shoes, and a curry shop | `images/cg/cg-beat-078.png` |
| 80 | 407 | toa | It's March twenty-sixth. By tomorrow I need proof I bel | `images/cg/cg-beat-080.png` |
| 82 | 416 | kaoru | Tomorrow is generous. Tut. | `images/cg/cg-beat-082.png` |
| 84 | 422 | narrator | He tutted once. Toa has heard he can manage five. | `images/cg/cg-beat-084.png` |
| 86 | 431 | kaoru | May have. | `images/cg/cg-beat-086.png` |
| 88 | 439 | toa | I have training. I have— | `images/cg/cg-beat-088.png` |
| 90 | 448 | kaoru | Stand. | `images/cg/cg-beat-090.png` |
| 92 | 455 | kaoru | Proposed remedy? | `images/cg/cg-beat-092.png` |
| 94 | 463 | kaoru | Impress me. | `images/cg/cg-beat-094.png` |
| 96 | 475 | kaoru | Bold. We'll see if your art matches your contract law. | `images/cg/cg-beat-096.png` |
| 98 | 483 | toa | Then I'll dance until you're satisfied or until dawn br | `images/cg/cg-beat-098.png` |
| 100 | 496 | toa | Music optional. Audience of one. Watch closely, Magistr | `images/cg/cg-beat-100.png` |
| 102 | 510 | toa | I'm a petitioner, not your evening entertainment. | `images/cg/cg-beat-102.png` |
| 104 | 526 | toa | Justice isn't a private show for magistrates with bored | `images/cg/cg-beat-104.png` |
| 106 | 533 | narrator | She gathers her permit book. The hanko case clicks shut | `images/cg/cg-beat-106.png` |
| 108 | 541 | toa | I'll find another seal. Or another city. | `images/cg/cg-beat-108.png` |
| 110 | 559 | toa | Fine. One dance. One seal. Then I never perform for you | `images/cg/cg-beat-110.png` |
| 116 | 590 | toa | The maiden waits at the gate. The road is long. She wal | `images/cg/cg-beat-116.png` |
| 118 | 597 | kaoru | Crane precision. Unicorn stamina. Continue. | `images/cg/cg-beat-118.png` |
| 120 | 607 | narrator | She plays to one viewer. Hips sway where the kata allow | `images/cg/cg-beat-120.png` |
| 122 | 615 | kaoru | Cheeky. | `images/cg/cg-beat-122.png` |
| 124 | 621 | narrator | The cup sets down softly. His eyes don't blink. | `images/cg/cg-beat-124.png` |
| 126 | 639 | toa | We had terms. No delays. | `images/cg/cg-beat-126.png` |
| 128 | 647 | kaoru | Merit enough. Signature... pending. | `images/cg/cg-beat-128.png` |
| 130 | 655 | kaoru | Continue. | `images/cg/cg-beat-130.png` |
| 132 | 663 | narrator | She continues — coquette sway sharpened to obedience, e | `images/cg/cg-beat-132.png` |
| 134 | 669 | kaoru | A good performance. | `images/cg/cg-beat-134.png` |
| 136 | 682 | narrator | His hand finds her wrist — not painful, not gentle. Ent | `images/cg/cg-beat-136.png` |
| 138 | 694 | kaoru | No? And yet you're still here. | `images/cg/cg-beat-138.png` |
| 140 | 700 | narrator | She spins free and finishes the phrase — defiance as ch | `images/cg/cg-beat-140.png` |
| 142 | 710 | narrator | She doesn't pull away. The dance uses his grip as count | `images/cg/cg-beat-142.png` |
| 144 | 718 | kaoru | Better. | `images/cg/cg-beat-144.png` |
| 146 | 726 | kaoru | Unless? | `images/cg/cg-beat-146.png` |

## Skipped even turns (first half)

| Turn | Reason |
|-----:|--------|
| 2 | `corridor_lost` |
| 14 | `corridor_lost` |
| 58 | `permit_desk` |
| 112 | `corridor_lost` |
| 114 | `office_dance` |
