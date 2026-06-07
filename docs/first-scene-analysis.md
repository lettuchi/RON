# First Scene Analysis — Toa & Kaoru

**Source:** Google Drive folder `Toa/Kaoru first scene screenshots` (16 Discord captures)  
**RP thread:** *Lost in the Magistrate's Office* · channel `noble-quarter`  
**IC dates:** 03/26/2025 evening → 03/27/2025 afternoon (scene ends mid-escalation)

---

## Per-screenshot timeline (chronological)

| # | Timestamp | Poster | Beat summary |
|---|-----------|--------|--------------|
| 1 | 170510 | Toa | Lost in magistrate complex; permit book + hanko case; urgent wandering |
| 2 | 170539 | Kaoru → Toa | Kaoru opens door: *"Done complaining?"* Toa startled in corridor |
| 3 | 170547 | Toa ↔ Kaoru | Formal knock; *sochira-no-kata*; renewal inquiry begins |
| 4 | 170557 | Toa ↔ Kaoru | New to Ryoko Owari; post-gempukku; Crane hair / Unicorn lands correction |
| 5 | 170628 | Kaoru ↔ Toa | Interclan matter → Emerald approval; door shut; sit; no shelf-gawking |
| 6 | 170637 | Kaoru ↔ Toa | Permit **expired**; Unicorn never told her; Academy trip feared |
| 7 | 170646 | Toa ↔ Kaoru | No local patrons; inn, pony, curry shop; date → March 27 |
| 8 | 170655 | Kaoru ↔ Toa | Dance disclosed; Kaoru lectures; cushion moved; stand |
| 9 | 170704 | Toa ↔ Kaoru | *"Proposed remedy?"* → Kaoru: *"Impress me. Perform."* |
| 10 | 170714 | Kaoru ↔ Toa | Small-space creative dance; obi loosens; coquette sway |
| 11 | 170729 | Toa ↔ Kaoru | Obijime bells; maiden narrative dance; Kaoru watches, drinks water |
| 12 | 170745 | Toa / Kaoru POV | Signature earned but withheld; performance continues |
| 13 | 170752 | (overlap) | Kaoru prolongs; Toa compliant display |
| 14 | 170802 | Kaoru ↔ Toa | Kaoru grabs; Toa reads entitlement; spins onward |
| 15 | 170813 | Toa ↔ Kaoru | Slow clap: *"A good performance…"* |
| 16 | 170823 | Toa ↔ Kaoru | *"Unless?"* — Toa straddles chair; hakama knots; **cliffhanger** |

---

## Major beats

1. **Arrival & disorientation** — Lost in magistrate complex  
2. **Wrong door** — Kaoru's noise complaint  
3. **Formal re-approach** — Hyper-polite knock  
4. **Permit pitch** — Renewal for Ryoko Owari residence  
5. **Interclan gate** — Emerald Magistrate required; private meeting  
6. **Expired permit** — Cannot simple-renew  
7. **Social vacuum** — No patrons; only inn / pony / curry  
8. **Audition bargain** — Performance as remedy  
9. **Office dance** — Small-space creative performance  
10. **Withheld signature** — Merit enough; Kaoru delays  
11. **Physical escalation (cliffhanger)** — Chair straddle; thread unfinished  

---

## Minor beats (flavor / props)

- Emerald Office affiliation on Kaoru  
- Toa suppresses habit of studying shelves  
- *sochira-no-kata* honorific  
- Shows paper but does not hand it over  
- Pony needs shoes; ride back to Academy  
- Curry restaurant as prior stop  
- Kaoru **tuts five times**  
- Cushion on tatami in front of desk
- Tall cup of water on desk  
- Obijime bells in dance  

---

## Choice points (VN branches)

| Moment | Options |
|--------|---------|
| After door slam | Leave / knock again / wait quietly |
| Addressing Kaoru | Hyper-formal / direct / humorous |
| Documents | Display only / surrender papers |
| Entering office | Refuse shut door / comply / peek at shelves |
| Expired permit | Accept Academy trip / push local fix / plead |
| Status question | Honest isolation / bluff connections |
| Before dance | Negotiate terms / perform immediately / refuse |
| Performance tone | Formal fan dance / flirtatious small-audience read |
| Escalation | Stop at dance / continue intimacy / rebuke grab |
| Final cliff | Verbal answer to *"unless?"* / **physical answer (canon)** / leave |

---

## CG / background notes

- **Corridor:** Lantern-lit magistrate hall, sliding doors, noble-quarter formality  
- **Office:** Desk, scrolls, permit book, hanko, shelves, cushion, water cup  
- **Performance:** Lamplight, obi on floor, tight framing  
- **Cliffhanger:** Chair two-shot, power imbalance composition  

---

## Canon ending (game true route)

**Trigger:** Physical answer to *"Unless?"* after compliant performance (`prologue_unless_menu` → `prologue_canon_ending`).

**Beats (PG-13/M → R sensual):**

1. **Proposition** — `cg canon_proposition` after physical unless answer (chair tension resolves).  
2. **Pull close** — `cg canon_pull_close`; latch, negotiation dissolves, Kaoru draws her off the chair.  
3. **Undressing** — `cg canon_undressing`; Toa loosens magistrate robes — tasteful, partial.  
4. **Embrace** — `cg canon_embrace`; cushion, lamplight, implied intimacy.  
5. **Fade to black** — amorous act implied, not narrated or CG-explicit.  
6. **Afterglow** — `cg canon_afterglow`; breath and silk regained, office intact.  
7. **Signing** — `cg canon_signing`; Kaoru pleased, **hanko stamp** on permit renewal.  
8. **Power play** — `cg canon_three_days`; signature **dated three days forward** (IC: effective March 30 if scene is March 27).  
9. **Case 1 hook:** `canon_first_scene` → *"Three days later…"* — early return, Case One, live-in preview dialogue.

Full beat doc: [canon-encounter-beats.md](./canon-encounter-beats.md). Script: `game/prologue_canon_encounter.rpy`.

Asset paths: `game/images/cg/cg-canon-*.png`, `game/images/cgs-canon-ending.rpy`.

**Flags set:** `permit_signed`, `permit_effective_days = 3`, `canon_first_scene`, `unless_branch = "physical"`, plus `kaoru_submission` / `compliance` / `physical_initiative` from prior choices.

**Non-canon branches:** Verbal unless → unresolved seal, three-week gap. Walk out → same. Refuse dance → bad-end menu.

---

## Ren'Py adaptation notes

- Prologue implements full first-scene arc through canon or branch endings  
- Case 0 candidate: *The Expired Permit* for non-canon replays  
- Kaoru route flags: `compliance`, `performance_boldness`, `rebuke`, `physical_initiative`, `kaoru_submission`  
- Canon flags: `permit_signed`, `permit_effective_days`, `canon_first_scene`  
- Keep game script **PG-13/M**; dark route can imply without explicit CG  

---

## Choice-outcome CGs

**Full mapping:** [cg-choice-map.md](./cg-choice-map.md)

21 placeholder event CGs (`cg-choice-{moment}-{variant}.png`) cover every menu in `game/prologue.rpy`:

| Moment | Variants |
|--------|----------|
| After door slam | leave · knock again · wait quietly |
| Formality | hyper-formal · direct · humorous |
| Entering office | comply · peek at shelves |
| Expired permit | academy trip · local fix · plead |
| Before dance | negotiate · perform immediately · refuse |
| Performance tone | formal fan dance · flirtatious |
| Escalation at grab | rebuke · lean in |
| Final "unless?" | verbal · physical · walk out |

Ren'Py definitions: `game/images/cgs-choices.rpy`. Shared beat CGs remain in `cgs-first-scene.rpy`.
