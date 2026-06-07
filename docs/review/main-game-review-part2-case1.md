# Main-Game Editorial Review, Part 2: Case 1 (Canal Body) + Romance Interlude 1.5

Editorial review only. No `.rpy` files were edited. Suggestions are proposals for the parent agent to accept or reject. Register kept feudal-Japan L5R (Rokugan / Ryoko Owari). Em dashes are avoided in all suggested rewrites, per `docs/style-no-em-dash.md`.

Files reviewed (in the order requested):
- `game/case1_investigation.rpy`
- `game/case1_companion.rpy`
- `game/case1_5_romance_interlude.rpy`

Note on game-flow order: `case1_companion.rpy` (and its non-canon twin `case1_noncanon_start`) actually runs *before* `case1_investigation.rpy`; the interlude runs last. Sections below follow the requested file order, but continuity is traced in true play order in section 3.

---

## 1. Slice summary

Case 1 is the first real detective beat: a young man pulled from a noble-quarter canal at first light, written off as "drowning" by the watch, whom Toa and Kaoru identify as Crane guest-house clerk Miya Jiro, strangled and staged after he found a barge manifest of false cargo (rice on paper, resin in the hold). The trail runs from the canal to the Lacquered Plum (geisha Suzu's testimony) to a forged Emerald seal locking the room where Jiro died, to a high-tide barge seizure; the "Chrysanthemum" Scorpion patron behind it stays a deliberate open cipher for the season. Around the case sits the companion contract that defines the whole game's register (`live_in_companion` vs witness-only) and the 1.5 "kitchen seal" interlude, which delivers the first explicit Toa/Kaoru beat plus a domestic curry coda.

---

## 2. Per-file sections

### 2.1 `game/case1_investigation.rpy`

#### [PLOT]

- **P1. The Scorpion comb's provenance is self-contradictory, and it is the slice's clearest mystery-logic hole.** The comb is found planted at the *canal recovery site*, "wedged in the seam where oil and wrong-colored water meet" (lines 404 to 408), and Toa reads it as a vanity slip: "a sender vain enough to leave his comb behind" (line 491). But Suzu later fixes its origin as the *Plum's river room*: "He left it in the river room a month ago and threatened to flay the maid who'd dared touch it" (line 713). A comb left in a guest room a month ago does not appear on a corpse staged across the district unless someone deliberately carried it there, yet no one ever asks how it got to the canal. Worse, the two characterizations of the killer collide: a man who threatens to flay a maid for touching his comb (meticulous, possessive) is also "vain enough" to abandon that same comb on a body he is otherwise hiding behind a forged seal and a false drowning report. Decide who planted it and why (the Chrysanthemum framing himself makes no sense; a third party framing the Scorpion, or Jiro pocketing it as proof, both do), and give Toa one line acknowledging the comb had to be *placed*.
- **P2. The kill-site geography is muddy.** Three locations are implied for where Jiro died and never reconciled: (a) "he died somewhere else, then was dressed for display" with a sleeve hem "eaten by canal slime from upstream" (lines 299, 303 to 304), where upstream is the Scorpion quarter (line 103); (b) the river room at the Lacquered Plum in the licensed quarter, which the forged Emerald writ "locked... the night Miya Jiro was murdered inside it" (line 871, and line 824); (c) recovery at the noble-quarter canal (line 331). The forged-seal beat asserts he died at the Plum, but the canal-slime clue points upstream/Scorpion. If the Plum *is* upstream/Scorpion-adjacent, say so once; otherwise the physical-evidence chain and the documentary chain disagree about the murder scene.
- **P3. The crime's intent is pulled in two directions: "send a message" vs "hide a drowning."** Toa's theory is that the body was "dressed for display... A message meant for Crane eyes" (line 354), reinforced by the planted Scorpion comb. But the same conspiracy also forged an Emerald seal to *lock the room and bury the death as a drowning* (lines 824, 871, 95). Framing a rival clan loudly and hiding the death quietly are opposite operations. This can be reconciled (e.g., the visible frame and the documentary cover-up come from two different parties), but as written the case treats both as one scheme, which weakens the logic.
- **P4. "Five cases in one week" is an implausible clock that the case neither honors nor pays off.** Kaoru repeatedly sets the frame: "first of five you'll witness before this week ends" (line 81, also 85, 89), "Survive all five, or the quarter eats your stipend" (companion file line 395), and the non-canon stakes "one week to prove she belongs to any of them" (line 54). Yet Case 1 alone visibly spans the canal day, "Tomorrow we cross the Miya guest registry" (line 482) opening on "Morning again" (line 529), and then "the next high tide" barge (line 1012), i.e. three-plus days. Five murder investigations in seven days is not credible, and nothing in Case 1 ever feels the pressure of the other four. Either soften the number/timeframe or have the deadline actually bite somewhere.
- **P5. Several flags are set but never read in this slice (dead or redundant).** Concretely: `case1_victim_hint = "miya_retainer"` (line 111) is never consumed; `case1_scene_choice` (lines 294, 308, 326) is set but only its sibling `case1_observation` is ever read (line 748), so `case1_scene_choice` is redundant; `case1_witness_handle` (lines 729, 749, 766) and `case1_comb_owner = "chrysanthemum_patron"` (line 715) and `case1_appointment_cipher = "chrysanthemum"` (line 784) have no in-slice consumer. Either wire these into a later beat or drop them.
- **P6. `case1_kaoru_trust` accumulates but is never checked in this slice.** It is incremented in at least eight places (lines 160, 177, 296, 351, 370, 600, 732, 902) but no branch in any of the three files tests it. Verify a downstream consumer (romance router / later cases) actually reads it; otherwise the player is "earning trust" with no payoff.
- **P7. Most Case 1 menus are near-cosmetic.** Real consequence exists in a few places: `case1_observation == "throat_bruise"` gates the "press" witness option (line 748), and `case1_briefing_choice == "detail"` unlocks the sharper sixteen-vs-fourteen-petals forgery catch (lines 817 to 824). But `case1_briefing_choice == "politics"` vs `"professional"`, the whole `case1_probe_response` menu (only swaps a reaction line at 450/455), and `case1_registry_approach` mostly change flavor lines, not outcomes. For a detective VN, consider letting at least one early choice change *what evidence is available* later, not just Kaoru's quip.
- **P8. The "board alone" option is an unsignaled instant game-over, and the target label is mis-scoped.** In `case1_barge_menu`, "Board alone" gives one line ("Watch from the gangplank if you must. The manifest is mine to take.", line 1145), a single "Toa..." from Kaoru (line 1149), then `jump gameover_case1_canal` (line 1151). The death is at the *barge*, but the game-over label is `gameover_case1_canal`. Two issues: (a) for an otome audience this is a hard fail with no warning beat distinguishing it from the other three viable options; (b) the label name implies the wrong location and will confuse anyone maintaining the ending map.
- **P9. The failure safety-net retcons the clue and the victim's name for free.** `if not case1_clue_found or not case1_victim_name` offers "Beg him for one more hour at the canal," which simply sets `case1_clue_found = True` and `case1_victim_name = "Miya Jiro"` (lines 1042 to 1050) with no scene. Recovering a blown investigation by begging, with the comb and the name materializing off-screen, undercuts both the mystery and Toa's competence. If a recovery path is wanted, dramatize it (one extra observation beat) rather than assigning the answers.
- **P10. The "defiance" probe jumps out of the canal scene before the comb and the name are found.** Picking "Push him too far" sets `case1_punishment_entry = "canal"` and `jump case1_punishment_bridge` (lines 397 to 401) *before* the comb (line 418) and the courier's chit / `case1_victim_name` (line 444) are discovered. The punishment bridge is out of this slice, so verify it returns the player into the canal flow at/after the comb discovery; if it routes forward instead, the player can reach the registry with `case1_clue_found = False` and `case1_victim_name = ""`, which then trips the P9 safety-net. This is a real path-integrity risk to confirm.
- **P11. Two separate romance entry points, with eligibility logic out of slice.** `case1_registry_milestone_end` can `jump case1_romance_router` if `canon_romance_eligible() and not case1_romance_seen` (lines 1052 to 1053), and `case1_barge_milestone_end` can `jump case1_5_romance_interlude` if `case1_5_romance_interlude_eligible()` (line 1248). These are distinct beats with distinct flags (`case1_romance_seen` vs `case1_5_romance_seen`). Because the 1.5 interlude hard-codes the live-in premise (see 2.3 P2), confirm `case1_5_romance_interlude_eligible()` requires `live_in_companion`; otherwise the witness-only path can fall into a scene whose entire setup assumes she sleeps behind his screen.

#### [CHARACTER]

- **C1. On the witness-only (non-companion) path, Kaoru flattens into one-note cruelty.** His live-in lines have range (cold at the body, then `charm` at line 496 "Eat. Then copy the watch testimony twice"). The non-companion equivalents stay punitive without the warmth underneath: "copy testimony until your hand cramps. Then we'll discuss whether you've earned another week here" (line 501), "the city bites back. Try to keep up" (line 1100). The control/tease dynamic needs a flicker of the interest-beneath-the-cruelty even when she has not signed, or the non-canon Kaoru reads like a different, lesser character.
- **C2. "To-chan" used in public slightly undercuts the discretion thesis.** Kaoru insists "Discretion isn't decoration" (line 120) and forbids theories aloud at the canal, yet uses the intimate diminutive "To-chan" at the crime scene in front of the clerk and the Miya envoy (line 262). It is a nice intimacy tell, but a man this controlled would likely save it for behind the screen (as the interlude does). Consider reserving "To-chan" for private beats.
- **C3. The okami and the factor are pure function.** The okami is a smooth obstacle ("We keep no quarrels, and fewer corpses", line 657) and the factor a boilerplate menace ("buys tides, not trials. You have a page. You do not have a name.", line 1199). Suzu, by contrast, is specific and alive (the persimmons on cruel nights, line 696). One concrete human detail each (a tic, a fear, a tell) would lift the antagonists out of placeholder. Strengths to keep: Toa's conscience even in the submissive "loom" branch ("She gave that to fear, not to us. Remember that before you call it a victory.", line 778) is excellent interiority and should be protected.

#### [DIALOG]

- **D1. Line 115 (on-the-nose syllogism).** The "X means Y, Y means you" construction is mechanical.
  - Before: `toa "Miya means Crane politics. Crane politics means you, Magistrate-sama."`
  - After: `toa "A Miya retainer in the canal. That makes it Crane politics, and Crane politics always finds your desk, Magistrate-sama."`
- **D2. Line 442 (editorializing tag).** "That's a name now, not rumor" tells the audience the significance instead of trusting the read.
  - Before: `toa "Miya Jiro. Guest-house ledger clerk. Deliver before third bell. That's a name now, not rumor."`
  - After: `toa "Miya Jiro. Guest-house ledger clerk. 'Deliver before third bell.' He had an errand the night the canal took him."`
- **D3. Line 952 (flat summary tag).** "The names just keep climbing" is a weak button.
  - Before: `toa "We came for the guest registry and left with a forger somewhere inside your own office. The names just keep climbing."`
  - After: `toa "We came for a guest registry and found a forger sitting somewhere inside your own office, Magistrate-sama."`
- **D4. Line 184 (register: "opium").** "Opium" is a real-world drug name that sits slightly outside the Rokugan register, especially since the finale already uses the cleaner "resin" (lines 1163, 1182).
  - Before: `kaoru "Opium ledgers. Marriage contracts. Anyone in this city who sells silence by the barrel."`
  - After: `kaoru "Poppy resin. Marriage contracts. Anyone in this city who sells silence by the barrel."`
- **D5. Repetition (no rewrite, structural).** Toa hits the same "Case One has a [name/face/comb/tide] now / I won't forget Jiro" refrain at lines 505, 1016, 1029, and 1224 to 1243. It is a deliberate motif but lands three to four times in one case; vary at least two instances so the vow keeps its weight.
- **D6. Repetition (no rewrite, structural).** The "someone staged a poem/message and forgot it would have an audience" image appears at lines 354, 486, and 491. Keep one (it is a good line) and recast the others.
- **D7. Motif overuse (no rewrite).** The "curry shops / curry" running gag is frequent (lines 60, 89, 133, plus the snack/cracker beats at 145, 153, 416 to 420). It is good character flavor for Toa, but at this density it starts reading as a verbal tic for Kaoru rather than her appetite; thin by one or two.

---

### 2.2 `game/case1_companion.rpy`

#### [PLOT]

- **P1. The "sponsorship, not a courtesan's contract" framing is a fig leaf the text then quietly contradicts.** Kaoru is emphatic that this is art patronage: "I'm drafting sponsorship, not a courtesan's contract... It would insult your lord and mine both if I played danna" (line 140), and Toa's relieved "Sponsorship. Not... not that." (line 144). But the actual duties are live-in companion terms ("sleep in the chamber adjoining my office... answer when I call, day or night", lines 170 to 173), and the 1.5 interlude then depicts an explicitly sexual relationship "different line item" and all. The drama of a legal fiction everyone sees through is a good idea, but right now the denial is played straight, so when 1.5 happens it can read as the game contradicting its own setup rather than as a knowing fiction. One line of mutual awareness (he knows she knows the ledger word is a courtesy) would convert the contradiction into intended subtext.
- **P2. The canon path depends on un-shown prologue physical state.** The `if canon_first_scene and physical_initiative >= 1` branch (line 209) has Kaoru reference a prior physical beat: "You already proved you can close a proposition in this room" (line 211). Per the file header, canon live-in requires the "physical 'unless?'" prologue branch. This is a hard dependency on prologue flags outside the slice; later writers must keep the prologue's physical branch and `live_in_companion` aligned, or this callback dangles.
- **P3. Set-but-unread-in-slice flags.** `companion_salary = 3` (line 195), `case1_sponsorship_flirt = True` (set four times: lines 35, 118, 264, 370), and `toa_overjoyed = True` (line 261) are never read in any of the three files. Confirm a downstream consumer or trim them.

#### [CHARACTER]

- **C1. "I like you. Enough that I want to keep you around." is a tonal outlier.** This blunt, plain confession (line 73) is warmer and more direct than Kaoru anywhere else, and it sits oddly against the interlude's whole bit that he literally cannot say "thank you" because it "would admit I wanted the company" (1.5 line 49). If he can say "I like you" on day one, the later inability to thank her loses its edge. Either make line 73 more characteristically oblique, or treat it as a crack he immediately re-armors (a beat where he regrets saying it).
- **C2. The `hyper_formal` branch makes Toa read subservient, off her confident baseline.** "Honored Magistrate-sama, shall I pour the tea before the terms you mentioned on the thirtieth, or after?" (line 56) is a much meeker Toa than the performer who elsewhere teases and negotiates. It is gated on a prologue style flag so it is player-chosen, but the swing is large enough to feel like two different protagonists. Strength to keep: the `negotiate` accept branch (lines 234 to 257) is the best agency beat in the slice; she pins down "release" and Academy nights and wins escort-not-leash terms. Protect it.

#### [DIALOG]

- **D8. Line 140 (expository worldbuilding clump).** Necessary information, delivered a touch lecture-like.
  - Before: `kaoru "I'm drafting sponsorship, not a courtesan's contract. The ledger will read art donor to artist. It would insult your lord and mine both if I played danna to a Crane who crossed provinces for ink."`
  - After: `kaoru "This is sponsorship, not a courtesan's contract. The ledger reads art donor to artist. I will not insult your lord or mine by playing danna to a Crane who crossed provinces for ink."`
- **D9. Line 148 (dictionary-definition phrasing).** "Gifts of money to support your artistic expression" reads like a glossary entry, briefly breaking voice.
  - Before: `kaoru "Gifts of money to support your artistic expression. I know exactly what I'm paying for. Interpret that liberally, within the residence I set."`
  - After: `kaoru "Coin for your art, openly given. I know exactly what I am paying for. Interpret it as liberally as you like, so long as you do it under my roof."`
- **D10. Line 170 (garbled tail).** "Your art is why the treasury pays. Not the excuse." muddles its own meaning.
  - Before: `kaoru "...remain on the premises unless I release you. Your art is why the treasury pays. Not the excuse."`
  - After: `kaoru "...remain on the premises unless I release you. The treasury pays for the art. Everything else it merely permits."`
- **D11. Line 403 (abstract clump).** "Competence within reach, that's what I want" is vague (and, per the Part 4 review, this exact phrase recurs in Case 5, so it is becoming an authorial tic worth varying).
  - Before: `kaoru "Dance bought you the corridor. Cases buy your keep. Competence within reach, that's what I want. Archive stairs, Case One ledger, before the watch blanks the line."`
  - After: `kaoru "Dance bought you the corridor. Cases buy your keep. Show me competence I can reach for. Archive stairs, the Case One ledger, before the watch blanks that name line."`
- **D12. Line 38 (anachronism: "energy").** "Audience-of-one energy" uses contemporary slang ("X energy").
  - Before: `kaoru "Bring that audience-of-one energy to the docket. Cases bore me less when you perform."`
  - After: `kaoru "Bring that audience-of-one fervor to the docket. Cases bore me less when you perform."`
- **D13. Line 47 (register: "curtsey").** A curtsey is a Western court gesture; a bow fits Rokugan.
  - Before: `kaoru "You danced like a maiden at a shrine. Try not to curtsey at a corpse."`
  - After: `kaoru "You danced like a maiden at a shrine. Try not to bow to the corpse."`

---

### 2.3 `game/case1_5_romance_interlude.rpy`

#### [PLOT]

- **P1. The first-night flashback already has "Case Two's letters" on the desk, before Case Two exists.** The interlude frames itself after the barge (line 12), then jumps to `case1_5_chamber_flashback`, "the first night after she moved into the adjoining chamber" (line 20), explicitly the night before "Case One starts at dawn" (line 65). Yet inside that first night the prose name-checks the next case: "as if Case Two were already listening" (line 52) and "Case Two's letters glaring from the outer desk like a runner who already knows too much" (line 100). Per the investigation file, Case Two ("Academy letters") arrives only after the barge ("Case Two arrived with the dawn", line 1234). Either the letters were physically sitting unopened from the start (in which case the prose should not label them "Case Two" during a moment when Toa cannot know that), or this is a timeline slip. Recommend the flashback foreshadow with something unnamed ("a sealed bundle on the outer desk") rather than the numbered case.
- **P2. The interlude hard-codes the live-in premise; eligibility must enforce it.** Every beat assumes `live_in_companion`: "the first night she slept on the far side of his screen" (line 12), the adjoining chamber and "do not... rearrange his shelves" terms (line 20), the shoji between their rooms. If `case1_5_romance_interlude_eligible()` can return true on the witness-only path, the entire scene is incoherent. Confirm the gate requires `live_in_companion` (and, ideally, a romance flag, see P3).
- **P3. Explicit content has no in-scene gate or opt-out once entered.** `case1_5_shoji_night` (lines 70 to 100) is an explicit beat that plays linearly with no menu, fade option, or consent check after entry. For an otome title, verify the eligibility function gates on an actual romance-route flag (not merely `live_in_companion`), so a player who signed the contract but did not pursue Kaoru is not funneled into explicit content. Consider an opt-out branch at the chamber stage.
- **P4. Two confusable romance flags.** This file sets `case1_5_romance_seen = True` (line 173), while the investigation file reads `case1_romance_seen` (lines 1052, 1077) for the *other* romance entry point. The near-identical names are an easy source of downstream bugs; consider renaming one (e.g., `case1_interlude_seen`).

#### [CHARACTER]

- **C1. One crude line breaks Kaoru's otherwise elegant, oblique register.** Kaoru's signature is bureaucratic-erotic indirection ("a body in my corridor who could read a ledger without fainting", line 49; "evidence he catalogs", narration line 91). Line 82, "I can hear your thighs press together from here," is markedly blunter than the rest of his voice. If the explicit beat stays, keep it in his metaphor-of-the-ledger idiom (see D14).
- **C2. The "intimacy reframed as filing" device is excellent but overused.** It carries the interlude ("Different line item", line 49; "Scheduling, not romance", line 65; "I know what I am paying for", line 97; "filing enough for one afternoon", line 168). It is the scene's best joke and its through-line, but four-plus repetitions in one short interlude start to flatten it. Trim to the two strongest. Strengths to keep: the quilt "loan against your noise" (lines 52 to 58) is a perfect controlling-tenderness gesture, and Toa keeping a private self at the end ("she does not perform purity", line 100) preserves her interiority inside an explicit beat.

#### [DIALOG]

- **D14. Line 82 (crude register break; see C1).**
  - Before: `kaoru "Do not perform stillness at me, To-chan. I can hear your thighs press together from here."`
  - After: `kaoru "Do not perform stillness at me, To-chan. I have read quieter ledgers than the one your body is keeping tonight."`
- **D15. Line 168 (explicit closer in an otherwise light curry scene).** The "private seal between her thighs" callback is on-motif but tonally heavier than the rest of the gentle curry coda.
  - Before: `kaoru "And you are still in my corridor. That is filing enough for one afternoon. Try not to walk like a woman keeping a private seal between her thighs."`
  - After: `kaoru "And you are still in my corridor. That is filing enough for one afternoon. Try not to walk like a woman carrying a secret she forgot to seal."`
- **D16. Repetition (no rewrite; see C2).** The "filing / scheduling / line item / inventory" deflection lands at lines 49, 65, 97, 155, and 168. Keep the two best.

---

## 3. Continuity handoff (CRITICAL)

### 3.1 Flags / persistent vars / stats SET in this slice

Companion (`case1_companion.rpy`):
- `live_in_companion = True` (290); `permit_signed = True` (291); `permit_effective_days` clamped to >= 3 (293 to 294).
- `companion_accept_tone` = `graceful` | `negotiate` | `gush` (222, 235, 260); `negotiated_terms = True` (238); `toa_overjoyed = True` (261); `case1_sponsorship_flirt = True` (35, 118, 264, 370); `companion_salary = 3` (195).
- Stat deltas: composure/honor/compliance/insight/performance_boldness/kaoru_resistance/kaoru_submission across the prelude, accept, and first-duty menus (105 to 377).

Investigation (`case1_investigation.rpy`):
- Initialized at start (6 to 13): `case1_victim_hint`, `case1_victim_name`, `case1_observation`, `case1_physical_clue`, `case1_briefing_choice`, `case1_scene_choice`, `case1_probe_response`, `case1_clue_found = False`.
- `case1_victim_hint = "miya_retainer"` (111); `case1_briefing_choice` (159/174/191); `case1_scene_choice` (294/308/326); `case1_observation` = `ink_and_hem` | `throat_bruise` | `signed_minimum` (305/323/337); `case1_probe_response` = `eager` | `defer` | `pushback` | `defiance` (347/367/380/398).
- `case1_physical_clue = "scorpion_comb"` (418); `case1_clue_found = True` (419, and 1049); `case1_victim_name = "Miya Jiro"` (444, and 1050).
- `case1_registry_approach` = `credentials` | `quiet` | `kaoru_lead` (585/597/614); `case1_witness_name = "Suzu"` (698); `case1_comb_owner = "chrysanthemum_patron"` (715); `case1_witness_handle` = `gentle` | `press` | `loom` (729/749/766); `case1_appointment_cipher = "chrysanthemum"` (784); `case1_forged_seal = True` (838); `case1_ledger_choice` = `record` | `copy` | `trust` (866/886/898).
- `case1_barge_approach` = `stealth` | `official` | `split` (1106/1118/1130); `case1_manifest_seized = True` (1197); `case1_closed = True` (1246).
- `case1_milestone` progression: `"miya_guest_registry_next"` (507) -> `"chrysanthemum_barge_next"` (1031) -> `"case1_closed"` (1245).
- `case1_punishment_entry` = `canal` | `registry` | `fail` (400/1036/1045) before jumps to `case1_punishment_bridge` (out of slice).
- `case1_kaoru_trust` incremented (160, 177, 296, 351, 370, 600, 732, 902); never tested in slice.

Interlude (`case1_5_romance_interlude.rpy`):
- `case1_5_romance_seen = True` (173).

### 3.2 Flags / vars READ in this slice

- Prologue/earlier state read: `live_in_companion` (throughout both case files), `companion_accept_tone` (122, 547, 556), `performance_style` (companion 34, 44), `formality_tone` (companion 53, 62), `canon_first_scene` + `physical_initiative` (companion 209), `unless_branch` (companion 448/466, investigation 135), `rebuke` (companion 457), `negotiated_terms` (companion 475), `permit_strategy` (companion 484/493), `permit_effective_days` (companion 293).
- In-slice cross-reads: `case1_briefing_choice` (421/426/817/876), `case1_observation` (748), `case1_probe_response` (450/455), `case1_registry_approach` (665/675/682/737), `case1_ledger_choice` (1018/1089/1226), `case1_barge_approach` (1162/1173/1184), `kaoru_submission` (907/972), `kaoru_resistance` (959/1033), `case1_romance_seen` + `case1_romance_route` (1052/1077).
- Functions called (defined out of slice; verify): `canon_romance_eligible()` (1052), `case1_5_romance_interlude_eligible()` (1248), `canon_first_scene` usage, plus helpers `show_cg_scene`, `restore_location_sprites`, `set_expression`.

### 3.3 Candidate dead / unread-in-slice flags (verify downstream or trim)

`case1_victim_hint`, `case1_scene_choice` (superseded by `case1_observation`), `case1_witness_handle`, `case1_comb_owner`, `case1_appointment_cipher`, `case1_sponsorship_flirt`, `toa_overjoyed`, `companion_salary`, `case1_kaoru_trust` (no in-slice test). Likely consumed by later cases or the romance router (so not necessarily dead): `case1_forged_seal`, `case1_manifest_seized`, `case1_witness_name`, `case1_victim_name`.

### 3.4 The central Case 1 mystery

- **What it is:** A young man found in the noble-quarter canal at first light, dismissed as "drowning." Identified as Miya Jiro, a Crane guest-house ledger clerk at the Lacquered Plum (licensed quarter).
- **How it is solved:** Physical reads (throat bruising = strangled not drowned; borrowed haori found separate upstream; soft ledger-clerk hands with ink) plus a planted Scorpion comb and a courier's chit naming Jiro lead to the Plum. Geisha Suzu testifies Jiro feared a flower-aliased Scorpion patron ("the Chrysanthemum") who tips in foreign silver, and that Jiro found a barge manifest of false cargo and meant to take it to a trustworthy magistrate. A forged Emerald seal (sixteen petals vs the office's fourteen) locked the room he died in, implicating a forger inside or impersonating Kaoru's office. The finale seizes the barge manifest (rice on paper, resin in the hold); the factor flees.
- **Logic gaps (see 2.1):** comb provenance/self-incrimination (P1); kill-site geography (P2); "frame Scorpion" vs "hide as drowning" intent (P3). The Chrysanthemum's identity is left open *by design* (confirmed against the Part 4 review: the "Chrysanthemum root" is the season throughline), so his anonymity here is a feature, not a hole, provided Case 1 makes clear the comb was deliberately *placed* rather than carelessly dropped.

### 3.5 Threads OPENED vs CLOSED

- **Opened:** identity of "the Chrysanthemum" (Scorpion patron / killer); who forged the Emerald seal (mole or impersonator inside the magistracy, `case1_forged_seal`); the chartered shipping concern and smuggling ring (factor fled; Kaoru vows to "burn his charter", line 1221); Suzu's safety after informing; the supernatural undertone (the "peeled charm/ward" air at lines 236 and 643, and the three-eyed crow omen at lines 243 and 637), both seeded and unresolved; Case Two ("Academy letters" already on the outer desk).
- **Closed:** Jiro's identity and true cause of death (named and corrected from "drowning" to "strangled"); the immediate barge manifest secured (`case1_manifest_seized`); `case1_milestone = "case1_closed"`, `case1_closed = True`.

### 3.6 Toa / Kaoru relationship beats

- Contract signed: canon `live_in_companion` with `companion_accept_tone` flavor, or witness-only (non-canon) where she must still "earn" the hall.
- First night in the adjoining chamber: the quilt "loan" (interlude 52 to 58); first explicit beat through the shoji if the interlude is eligible (70 to 100); thank-you curry / domestic coda (108 to 171).
- `case1_kaoru_trust` accrues through cooperative choices; optional `case1_romance_router` is a separate, earlier romance touch.
- Kaoru's affection is mostly deflected into bureaucratic idiom; his one overt line is "I like you. Enough that I want to keep you around." (companion 73). "To-chan" is his intimate register (canal 262; interlude 65, 82).

### 3.7 State later cases must honor

- `case1_closed = True` / `case1_milestone = "case1_closed"`; do not reopen Case 1 as unsolved.
- `live_in_companion` (and `companion_accept_tone`) gate register everywhere; keep both branches alive in Case 2+.
- Case 2 = the "Academy letters" already foreshadowed on the outer desk (companion 249; investigation 1234; interlude 116, 147).
- The Chrysanthemum + forged-Emerald-seal/mole are the season spine; Case 2+ should reference them.
- World facts now true: three koku monthly stipend + board; chamber adjoining the office; Suzu (alive, Plum), the okami (Plum), and the factor (fled) exist; the "snacks/curry after paperwork" motif and the "To-chan" diminutive are established; supernatural seeds (peeled wards, three-eyed crow) are live.

### 3.8 Prologue consistency this case relies on

- Canon `live_in_companion` requires the prologue's physical "unless?" branch (`canon_first_scene`, `physical_initiative >= 1`), referenced at companion 209 to 216; keep prologue and companion in sync.
- `unless_branch` (verbal / walk_out), `rebuke`, `negotiated_terms`, `permit_strategy`, `performance_style`, `formality_tone` are all read here and must keep their prologue meanings.
- The permit is dated to "the thirtieth" (companion 14, 298) with a +3-day effective window (header); Toa danced an "audition" for Kaoru in his office (companion 95, 99, 103), which Case 1 treats as shared history.

### 3.9 Minor / housekeeping

- Em-dash rule: dialog and narration honor it; em dashes appear only in comment/banner headers (e.g., interlude line 1, the investigation section banners around lines 511 to 518 and 1057 to 1060). Cosmetic, but flagged since `docs/style-no-em-dash.md` is project-wide.
- The barge finale (lines 1062 onward) drops `voice` tags that earlier scenes carry (e.g., narration at 1069, 1160, 1218); confirm this is an intended unvoiced section rather than missing audio refs.
