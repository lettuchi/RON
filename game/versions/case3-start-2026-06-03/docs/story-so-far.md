# Ryoko Owari Nights — story so far

**Protagonist:** Kakita Toa — Crane dancer, white hair, grey eyes, black kosode, gold crane obi, white hakama.  
**Love interest:** Kitsu Kaoru — Emerald Magistrate of Ryoko Owari; cruel, charming, politically lethal.  
**Setting:** Ryoko Owari — corrupt canal city of lies, Scorpion influence, peeled charms and wrong water.

---

## Prologue — the wrong door

Toa arrives with an **expired permit** and a permit book the Unicorn caravan never warned her about. She finds the magistrate's hall by lantern light, knocks wrong doors, and faces **Kitsu Kaoru** — who makes her **dance for ink**, tests her pride, and corners her with *unless?*

**Branches:**
- **Canon route** (`canon_first_scene`): physical *unless?* → intimate office encounter → permit signed **three days forward** → return on the 30th for residency talk.
- **Refuse dance + leave (bad end):** no seal, rain canal CGs → ronin abduction → implied brothel sale → **Game Over**.
- **Unless walk-out (bad end):** Kaoru pursues, drags her back to the magistrate office → implied coercion → **Game Over** (no canon recovery).
- **Refuse dance / verbal branches:** non-canon reopening weeks later, colder dynamic, no live-in companion offer.

---

## Case 1 — The canal body (Miya Jiro)

**Hook:** Companion offer (canon) or cold return (non-canon). Toa becomes **live-in companion** under Kaoru's **art patronage** on canon path (not yoriki).

**Investigation:**
- Body in noble-quarter canal; watch calls drowning.
- **Clues:** borrowed haori, Scorpion comb, courier chit → victim **Miya Jiro**, guest-house clerk.
- **Lacquered Plum:** geisha **Suzu** names the **Chrysanthemum** patron; forged **Emerald writ** (sixteen-petal seal) locks the river room.
- **Scorpion factor** demands the registry; Kaoru stares him down.

**Finale:** High-tide **Scorpion barge** — false rice / true resin manifest seized; Case One closed.

**Romance (canon):** After the Plum, if prologue canon + live-in companion + trust (`kaoru_submission`), **office interlude** before the barge (`case1_romance_interlude`).

**Bad end:** Board the barge **alone** — factor throws Toa into the canal → **Game Over**.

---

## Case 2 — The Academy packet (便りの灰)

**Hook:** Crane Academy credential packet burned; courier **Tsubaki** dead in warehouse alley.

**Investigation:**
- Ash with half-melted Crane mon; kiln boy names Scorpion paymaster.
- Outer-desk routing slip — **clerk** tied to Case One's factor thread.
- Emergency duplicate charter saves Toa's season.

**Romance (canon):** Same evening as the close — **hill festival interlude** (`case2_festival_interlude`), then **morning tea** (`case2_romance_morning`). Festival requires `canon_first_scene` + `live_in_companion`; kiss menu has no bad end — kiss only (Kaoru: don't take it seriously; Toa hides a dull unnamed ache) or go further (fade-to-black, shoji silhouette CG). Morning requires `canon_romance_eligible()` (`kaoru_submission` ≥ 2). Flags: `case2_festival_seen`, `case2_festival_kiss_only`, `case2_festival_intimate`. Bridges into Case Three when `case2_closed`.

**Bad end:** Rush into the alley **alone** — throat cut in the ash → **Game Over** (Academy road closed).

---

## Case 3 — Kimono fabric shop (絹屋の帳) — vertical slice

**Hook:** Chrysanthemum factor thread continues — kimono merchant, mis-tagged bolts, sabotaged shelf in the bolt room.

**Investigation (one beat):** Office briefing menu → fabric shop → pick one clue (bolt tags, clerk ledger, shelf brace).

**Accident setpiece:** Collapsing shelf / falling silk roll → menu before harm resolves.

**Romance (canon continue):** *Trust Kaoru / call for him* — rescue CG, his hands shake, one honest line then cold cover; Toa flustered, devotion not love (`case3_kaoru_rescue`, `case3_closed`).

**Bad end:** *Dodge alone* — content warning → gravely injured Toa (bandages, rain, Kaoru shadow at door) → **Game Over** (`gameover_case3_injury`, `seen_gameover_case3`). Hospital implied; no graphic gore.

**Entry:** `case3_investigation_start` from Case 2 post-bridge / festival / morning tea when `case2_closed` and not `case3_closed`.

---

## Route flags (quick reference)

| Flag | Meaning |
|------|---------|
| `canon_first_scene` | Prologue intimacy + forward-dated permit |
| `live_in_companion` | Signed live-in companion / patronage appointment |
| `case1_closed` | Jiro murder arc resolved |
| `case2_closed` | Academy packet arc resolved |
| `case1_romance_seen` / `case2_romance_seen` | Canon romance beats viewed |
| `case2_festival_seen` | Hill festival interlude viewed |
| `case2_festival_kiss_only` / `case2_festival_intimate` | Festival kiss branch |
| `case3_started` / `case3_closed` | Case Three vertical slice |
| `case3_kaoru_rescue` | Fabric-shop rescue beat |
| `case3_bad_end_injury` | Bolt-room injury bad end |

---

## Music / gallery

- Image songs: Kaoru「権利の帳」, Toa「赤い糸の灯」; duet hidden from gallery (WIP).
- CG gallery: prologue, canon ending, Case 1 & 2 investigation and endings.
