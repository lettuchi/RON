# Ryoko Owari Nights — story so far

## Premise

> An itinerant Crane dancer earns Emerald Magistrate Kitsu Kaoru's companion permit, and follows him through five corrupt cases believing she is only his witness, and discovers in the end he was auditioning his yoriki the whole time.

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
- **Lacquered Plum:** geisha **Suzu** names the **Chrysanthemum** patron; forged **Emerald writ** (sixteenth-petal seal) locks the river room.
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

**Exit:** `case3_milestone_end` → `case3_post_case3_bridge`.

---

## Case 3.5 — "Is this a date?" (interlude)

**Hook:** After Case Three pins, Kaoru maps a canal walk — skewers, deflection, almost-admission walked back. Not a case file; attachment beat before steel.

**Eligibility:** `romance_through_case3_complete()` and not `case4_date_interlude_seen` (Cases 1–3 romance in one run; **no** Case 4 defend required).

**Script:** `game/case3_5_date_interlude.rpy` — `case3_5_is_this_a_date_interlude` (alias `case4_is_this_a_date_interlude`).

**Exit:** `case4_post_case3_bridge` → Case Four dock raid.

**Design:** `docs/case3.5-date-interlude-design.md`.

---

## Case 4 — The dock ledger (剣の帳) — vertical slice

**Hook:** Clerk fled to lower piers with Case Three's night ledger; **Kurogane**, warehouse foreman (Scorpion-trained); magistrate raid in rain.

**Investigation (one beat):** Dock menu — split crate, watchman names suspect, or cover stairs for Kaoru.

**Setpiece:** **Dual swordfight** — wide fight CG; crisis menu.

**Romance:** *Stay behind me, Magistrate-sama—* → Kaoru shields her (`case4_kaoru_defended`) → `case4_closed`.

**Bad end:** *I'll cut him down myself* → content warning → **Game Over** 「剣の果て」 (`case4_toa_slain`, `gameover_case4_slayn`).

**Close:** Case Five hearing (yoriki appointment on full romance path).

**Entry:** After Case 3.5 bridge (or skip straight from `case3_post_case3_bridge` if date ineligible).

**Design:** `docs/case4-investigation-scene.md`.

*Archived:* Canal supper vertical slice (宴の呼び声) removed from canon order 2026-06-03; `gameover_case4_abandon` retained for dev/saves.

---

## Case 4.5 — Teardrop kobune (舟の帳)

**Hook:** After Case Four, Toa witnesses at **Teardrop Island marina** (winter Scorpion crisis) and finds Kaoru soaked beside a **kobune** — Discord *Stress Reduction and Small Boats* spine, fade-to-black on the hull.

**Eligibility:** `case4_5_boat_interlude_eligible()` — `all_romance_routes_complete()`, `case4_closed`, `case4_kaoru_defended`, not `case4_5_boat_interlude_seen`, no prior case bad ends.

**Script:** `game/case4_5_boat.rpy` — `case4_5_boat_interlude`.

**Beats:** Island dispatch → marina find → sob/breakdown → warmth menu → throw **into boat** → fall menu → fade intimacy → *I found you* / **Kitsu Kaoru** → bath/kotatsu tease.

**Survival:** *Go limp — let the hull take you.* → bruised knees, attachment beat → `case5_investigation_start`.

**Bad end:** *Fight the throw — land rigid on the thwart.* → content warning → **Game Over** 「舟の果て」 (`case4_5_bad_end_boat_injury`, `gameover_case4_5_boat`, `seen_gameover_case4_5`).

**Exit:** `case4_post_case4_bridge` → Case 4.5 (if eligible) → `case5_investigation_start`.

**Design:** `docs/plot-guide-case4-5-boat.md` · Discord [Stress Reduction and Small Boats](https://discord.com/channels/1057790980327231609/1451232878829768807) — verbatim IC in `discord-threads-raw.md`; VN-only throw-fight bad end.

---

## Case 5 — The Left Hand (御前の帳)

**Shipped (Path A):** `game/case5_investigation.rpy` — dawn summons and false-exit bait, Cases 1–4 audition callback, public hearing, yoriki scroll, accept/refuse menu, optional private confession and bedroom fade, week-one epilogue. **Eligibility:** `all_romance_routes_complete()`; witness-only runs get `case5_noncanon_discharge`. **Refuse** → brutal bad-end stubs (`gameover_case5_chained`, `gameover_case5_quarter_cage`). **Bonus:** `epilogue_romance_bonus.rpy` after canon accept when `epilogue_romance_bonus_eligible()` — kotatsu, mikan, paperwork tease, almost-smile, off the ledger. Voice IDs `kaoru_335+`, `toa_281+`, `narrator_272+` (manifest stubs; regen batch TBD). Design draft: `docs/case5-path-a-draft.md`.

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
| `case4_date_interlude_seen` | Case 3.5 "Is this a date?" viewed |
| `is_this_a_date_asked` | Player pressed the date question |
| `case4_started` / `case4_closed` | Case Four dock raid vertical slice |
| `case4_suspect_named` | Kurogane identified before steel |
| `case4_kaoru_defended` | Dock swordfight — trust Kaoru at crisis |
| `case4_toa_slain` | Bad end — duel alone on the pier |
| `case4_5_boat_interlude_seen` | Teardrop kobune interlude viewed |
| `case4_5_boat_choice` | `trust_warm` / `defy_cold` (warmth menu) |
| `case4_5_boat_fall_choice` | `trust_fall` / `fight_fall` (into-hull throw menu) |
| `case4_5_bad_end_boat_injury` | Skiff throw injury bad end |
| `seen_gameover_case4_5` | Case 4.5 boat Game Over viewed |
| `case5_yoriki_accepted` / `case5_closed` | Case Five Path A canon complete |
| `case5_romance_bonus_seen` | Kotatsu bonus epilogue viewed |
| `seen_gameover_case5` | Case 5 refusal Game Over viewed |

---

## Music / gallery

- Image songs: Kaoru「権利の帳」, Toa「赤い糸の灯」; duet hidden from gallery (WIP).
- CG gallery: prologue, canon ending, Cases 1–5 investigation and endings, **Case 3.5** date group, **Case 4.5** skiff group.
