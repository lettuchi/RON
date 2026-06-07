# Canon CG continuity bible (L5R / Ryoko Owari)

**Last updated:** 2026-06-07 (canon CG QA pass 2)

Reference for regen prompts and background consistency across canon CG groups. **Not** Modern AU.

---

## Emerald Magistrate office / yoriki chamber

**Anchor CGs:** `cg-first-scene-permit-desk.png`, `cg-first-scene-chair-tension.png`, `cg-canon-signing.png`, `cg-case1-romance-sponsorship.png`, `cg-case5-false-exit-office.png`

| Element | Canon lock |
|---------|------------|
| Desk | Dark polished wood; scrolls, inkstone, brush holder, low andon or standing lantern |
| Left wall | **Dark blue vertical banner** with **gold-rimmed jade-green sphere + imperial sixteen-petal kiku** (Emerald Magistrate badge). **Not** Kakita crane mon on wall hangings |
| Bookshelves | Floor-to-ceiling scrolls behind seated Kaoru |
| Window | Open shoji or glass; **rainy Ryoko Owari night**, pagoda/clock tower silhouette, warm window lights |
| Lighting | Warm amber interior vs cool blue rain exterior |

**Inconsistencies (borderline — document, no auto-regen):**

- Several office CGs (`permit-desk`, `sponsorship`, `office-dance` regen) use a **gold floral/sunburst mon** on the blue banner instead of the jade-sphere kiku lock from `vn-art-pipeline` / `cg-style-prompt-block.md`. Pass 2 confirms same drift on `choice-grab-lean-in`, `choice-dance-immediate` (regen), `punishment-shoji`. Reads as magistrate office but emblem drifts.
- `canon-signing` uses a **green circular wall crest** (three-leaf) rather than the blue banner — acceptable variant wall decor but not identical to permit-desk layout.
- Desk ornamentation varies (folding screen vs bookshelf emphasis) — acceptable scene-to-scene; same room register.

---

## Kaoru wardrobe (gold / maroon magistrate)

| Context | Lock |
|---------|------|
| Office / investigation | Gold or mustard **outer kosode/haori** over **maroon** inner layer; gold geometric collar trim; short brown ponytail |
| Festival / date (evening) | Same gold/mustard primary; maroon sleeve or inner visible at cuffs (`case2-festival-kiss`, `case3_5-date-kaiseki-duo`) |
| Kotatsu / domestic | Gold-brown outer over dark green inner (`epilogue-romance-kotatsu-intimate` regen) — warmer domestic register OK |

**Pass 2 note:** `case2-festival-intimate` uses cherry kosode + peach obi; re-read confirms **gold crane on obi** — festival evening dress, not work-obi drift.

---

## Toa wardrobe

| Context | Lock |
|---------|------|
| Work / office / cases 1–2 | Black kosode, **gold crane bird obi**, white hakama, white hair |
| Case 3.5 date inn | Black **furisode** with cherry/lavender motifs, ornate hairpins (`plot-guide-is-this-a-date.md`) — **intentional** date outfit |
| Festival intimate | Cherry kosode + peach obi with **crane motif on obi** (`case2-festival-intimate`) — intentional evening dress |

---

## Rain / harbor / Ryoko Owari exteriors

| Group | Anchor | Lock |
|-------|--------|------|
| Canal / rain gameover | `cg-gameover-rain-run.png` | Wet stone, lantern bokeh, no characters |
| Harbor wrist / boat | `cg-case4_5-boat-hands-gunwale-closeup.png` (regen 2026-06-07) | Wet wood gunwale, rain streaks, warm lantern reflections |
| Alley / bad ends | `cg-badend-brothel-grasp.png` | Narrow wet street, red lanterns, rain |
| Office window | All magistrate office CGs | Vertical rain on glass, distant lit towers |

Mood is consistent across groups; no regen required for atmosphere.

---

## Intimate / embrace CGs (hand-risk)

Highest QA priority. Regen backup folders: `canon-redo-hands-2026-06-07/` (pass 1), `canon-redo-hands-2026-06-07-pass2/` (pass 2).

| CG | Hand status (2026-06-07) |
|----|--------------------------|
| `cg-canon-embrace.png` | **Borderline** — back-hand knuckles crowded; pass 2: no regen |
| `cg-canon-steamy-intimacy.png` | **Borderline** — shoulder-hand family (orphan) |
| `cg-canon-steamy-afterglow.png` | **Borderline** — shoulder/forearm knuckles (orphan) |
| `cg-canon-pull-close.png` | PASS |
| `cg-canon-undress-toa.png` | PASS |
| `cg-case2-festival-kiss.png` | **Regen'd** (v3, single visible hand) |
| `cg-case2-festival-intimate.png` | PASS hands; festival wardrobe OK |
| `cg-epilogue-romance-kotatsu-intimate.png` | **Regen'd** |
| `cg-case3_5-date-almost-hands.png` | **Regen'd** |
| `cg-case1_5-shoji-wrist-closeup.png` | **Regen'd** |
| `cg-case4_5-boat-hands-gunwale-closeup.png` | **Regen'd** (v2) |
| `cg-first-scene-office-dance.png` | **Regen'd** (v2, fan-grip composition) |
| `cg-choice-dance-immediate.png` | **Regen'd** pass 2 (orphan choice CG) |
| `cg-prologue-dance-disrobe.png` | **FAIL** — blob hands; regen blocked pass 2 |
| `cg-epilogue-kotatsu-warmth-closeup.png` | PASS — feet macro stub OK |

---

## Case 1.5 yoriki chamber (private)

Shoji screens, quilt, curry kitchen, dawn desk — warmer and more private than magistrate office; **no shared furniture lock** with office group. Rain at windows recurs. Hands on `shoji-wrist` regen'd pass 1. Pass 2: `chamber-quilt`, `chamber-shoji-tea`, `shoji-tear` PASS.

**Punishment bad-end (case 1):** `punishment-desk`, `punishment-shoji` PASS; `punishment-floor` borderline thumb; `punishment-hands` PASS (pass 1).

**Kaoru prologue bad ends:** `badend-kaoru-wrist` PASS; `badend-kaoru-shoji` silhouette PASS.

---

## Case 3.5 date inn

Tatami, low tables, chochin, cherry night exterior. Furisode + gold haori duo per `plot-guide-is-this-a-date.md`. Do not force office crane obi in this arc.
