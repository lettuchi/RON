# Ryoko Owari Nights, Consolidated Main-Game Story Review

Date: 2026-06-05. Scope: the canon main game (prologue through Case 5 finale and all endings) of the L5R otome detective visual novel. This is a holistic synthesis of five parallel editorial slices, not a fresh review. No `.rpy` files were edited. Register kept feudal-Japan Rokugan; em dashes avoided throughout, per `docs/style-no-em-dash.md`. The Modern AU is out of scope.

Findings roll-up across all five slices: **[PLOT] 83, [CHARACTER] 48, [DIALOG] 68 (199 total), with 50 before-to-after line rewrites supplied.** A handful of the [PLOT] entries (mostly in Cases 2 to 4) are positive continuity confirmations rather than defects, so the count of actionable defects is somewhat lower. Section docs and line refs are cited so the owning agent can drill in; see the Index (section 7).

---

## 1. Executive summary: top 12 highest-impact changes (ranked)

Ranked by impact across the whole game. Duplicates that several slices raised independently are merged and noted as game-wide.

1. **[PLOT] Release blocker: the dev chapter-pick menu is the first screen after the splash.** `dev_chapter_pick_enabled = True`, so pressing Start shows a debug menu with the banner "Dev build, choose how to start" before the OP. The fix is one line (flip to `False` or gate on `config.developer`), but as shipped no player reaches the canon entry cleanly. Source: Part 1b (setup), `script.rpy` P1 (`dev_chapter_pick.rpy:17`, `script.rpy:19 to 22`).

2. **[PLOT] Walk-out branch contradiction makes authored cross-file content unreachable.** The prologue routes the "walk out" answer to a terminal game-over (`prologue.rpy:811, 820, 918`), yet Case 1 contains voiced content gated on `unless_branch == "walk_out"` ("I came back. That has to count for something." / "You came back. I noted that.") at `case1_investigation.rpy:135` and `case1_companion.rpy:448`. That dialogue can never fire, and the entire `rebuke` axis dies with it. Recommended fix: route walk-out into Case 1 non-canon ("she came back"). Source: Part 1a (prologue) P1/P2.

3. **[PLOT] The season's central mystery is deferred, not resolved (game-wide).** The Chrysanthemum patron / forged Emerald seal / smuggling spine is seeded in Case 1 and recalled in Cases 2 to 4 as "Case One's flower," but Case 5 contains no investigation and explicitly leaves it "pinned, not closed." No single slice owned this verdict; each saw only its own case. Decide deliberately: commit to a "the city never closes the big file" thesis in-text, or give Case 5 one real investigative beat. Source: Part 4 P1; Part 2 section 3.4; Part 3 section 3c.

4. **[CHARACTER] Refusal-end Kaoru is a different man from canon Kaoru (sharpest characterization break).** Declining the yoriki appointment routes to trafficking (`gameover_case5_chained`) or a cage (`gameover_case5_quarter_cage`), while the same scene plus the bonus epilogue and ED portray a tender, protective Kaoru. Escalating from "I chose you" to "I will have you trafficked for refusing a job" inside one menu is unearned. Fix: a softer estrangement end, or seed earlier that the city (not Kaoru) collects the unsigned left hand. Source: Part 4 C2/P5/P8.

5. **[PLOT] Spring-to-winter seasonal contradiction across Cases 2 to 4.5.** The festival reads summer, Case 3.5 is explicitly spring, Case 4.5 is explicitly winter, yet the four beats are only days apart. Pick one season for the whole stretch or insert real time-skips. Source: Part 3 #1 (`case3_5 L68/74`, `case4_5 L17/41/98`).

6. **[PLOT] Peril-binary monotony and cloned climaxes (game-wide).** "Trust Kaoru or be gravely hurt" fires in Cases 2, 3, 4, and 4.5, and the Case 3 rescue and Case 4 defend share near-verbatim dialogue ("burned this whole quarter/pier down to the canal"). Reshape at least one climax and give Toa one clean physical success. Source: Part 3 #2 (`case2 L148`, `case3 L181 to 188/L223`, `case4 L181 to 187/L220`, `case4_5 L186 to 193`).

7. **[PLOT] Villain faction-name muddle plus Imperial-mon stakes.** Case 2 calls the culprit both "the Plum factor's cousin" (`L245`) and "the Chrysanthemum's ledger" (`L261`); Cases 1, 3, 4 commit to Chrysanthemum. Separately, the "sixteen-petal" chrysanthemum forgery (`case4 L99`) is the Emperor's crest, which makes the scheme treason, not a tax scam. Settle one faction name and decide the mon's stakes. Source: Part 3 #3.

8. **[PLOT] Scorpion comb provenance hole in Case 1.** The comb is found planted at the canal recovery site (`case1_investigation.rpy:404 to 408`) and read as a careless vanity slip (`:491`), but Suzu fixes its origin as the Plum's river room a month earlier, owned by a man who would "flay the maid who dared touch it" (`:713`). Meticulous-then-careless is contradictory, and no one asks how it reached the canal. Decide who placed it and give Toa one line acknowledging it was placed. Source: Part 2 P1.

9. **[CHARACTER] The detective premise is never seeded; the heroine is framed as a dancer.** The OP name card reads "a Crane dancer" (`opening.rpy:198`), Toa's first spoken line is pure quip (`script.rpy:50`), and her one flicker of investigative instinct in the prologue (the shelf-peek) is scolded as a discipline failure rather than competence. Plant one correct, unprompted deduction in the opening. Source: Part 1a C1; Part 1b `script.rpy` C1 / `opening.rpy` C1.

10. **[CHARACTER] Kaoru never drops his banter armor through intimate beats (game-wide).** The canon love scene stays one-note witty with no unguarded line (`prologue_canon_encounter.rpy` C1/C2), the Case Zero "almost-smile" payoff is never collected (P4), and the festival, Case 3.5, and Case 4 all run the same advance-then-retract ("Forget I said it"). Let the performance drop once per intimate scene. Source: Part 1b section 2.3 C1/C2/P4; Part 3 section 3d.

11. **[PLOT] Pervasive dead and unread flags (game-wide).** Set-but-never-read state appears in every slice: `rebuke`, `kaoru_formality`, `prologue_refused_dance`, the "leave" value of `door_response`, the three Case Zero flags, `case1_victim_hint`, `case1_scene_choice`, `case1_witness_handle`, `case1_comb_owner`, `case1_appointment_cipher`, `case1_sponsorship_flirt`, `toa_overjoyed`, `companion_salary`, `case1_kaoru_trust`, `case2_scene_choice`, `case3_clue_clerk`. Either wire to a payoff or delete. Source: Part 1a P2/P3; Part 2 P5/P6 and section 3.3; Part 3 (Case 2/Case 3 dead clues); Part 4 (flag list).

12. **[CHARACTER] The romance is submission-gated, silently writing out an assertive Toa.** The chain `canon_first_scene` plus `live_in_companion` plus `kaoru_submission >= 2` plus `case4_kaoru_defended` rewards compliant play; an assertively-played Toa can fall below `kaoru_submission >= 2` and lose festival morning, the date, the boat, and the romance ending. The physical "Unless?" answer is also ungated, allowing tonal whiplash. Source: Part 1a C4; Part 3 section 3e.

---

## 2. Game-wide themes (cross-slice patterns)

### T1. The "trust Kaoru or be gravely hurt" peril-binary spans the whole game, not just the middle cases
Part 3 named this for Cases 2, 3, 4, and 4.5, but the same submit-or-suffer shape actually brackets the entire game. It opens in the prologue (refuse the dance, or walk out, both route to dark ends) and closes in Case 5 (refuse the appointment, route to the cage). No single slice connected the prologue, middle, and finale instances as one design pattern.
- Prologue: `prologue_refuse_bad_end`, `prologue_walkout_ending` (Part 1a P6, routing map 3.4).
- Case 2 "go in alone" game-over; Case 3 "dodge it alone"; Case 4 "I will cut him down myself"; Case 4.5 "fight the throw" (Part 3 #2, section 3c).
- Case 5 refuse-the-job (Part 4 P5).

### T2. Unearned brutal bad ends versus the tender canon Kaoru (game-wide)
The trafficking/cage outcomes share one shape: a heroine declining coercion is punished with the pleasure quarter. This contradicts the canon Kaoru of the bonus epilogue and ED. The fix template already exists in the game, scattered across slices: Case 1's punishment end is coherent because Toa opts in by demanding it, and the rain bad end is earned because Kaoru is absent and Toa's pride is the named cause.
- Prologue rain/brothel and Kaoru-pursuit ends (Part 1a P6; Part 4 P11/C10/C11).
- Case 5 refusal trafficking/cage (Part 4 C2/P5/P8).
- Working model to copy: Case 1 opt-in punishment (Part 4 C6) and Kaoru-absent rain end (Part 4 C11).

### T3. Dead and unread flags in every slice
State is tracked with more granularity than the game ever reads. See the matrix in section 3 and executive item 11. Appears in Part 1a, Part 1b, Part 2, Part 3, and Part 4.

### T4. Rokugan-register slips and anachronisms (game-wide), with one recurring authorial tic
The strongest single tic is the modern math/ledger idiom: "order of operations" (`script.rpy:50`), "do the math" (`prologue:463`), "math/arithmetic/montage" (Case 5 `D4/D5`, rain end `D13`). Beyond that: digital clocks in Case Zero (`kaoru_pro_prologue 41/163/184/190`), the Gregorian "March twenty-sixth" (`prologue:434`), "opium" (`case1_investigation:184`), "curry"/"curtsey" (`case1_companion:47`), "energy" slang (`case1_companion:38`), "twitterpated" sprite tag (`case3_5`), "asparagus" kaiseki (`case3_5:162`), "police" (`case5:134`), "classified information" (`epilogue_romance_bonus:49`), and the L5R color error "Scorpion grey" (Scorpion's colors are red and black; Cases 2 and 4). Slices: all five.

### T5. Kaoru stays in "banter armor" through intimate beats, and his advance/retract becomes a crutch
The canon love scene never drops the wit (Part 1b 2.3), and the relationship's escalation ladder runs the same "he advances, then retracts" move at the festival, Case 3.5, and Case 4 (Part 3 section 3d). Only the boat (Case 4.5) breaks the pattern, when Toa demands "ask, do not order." Slices: Part 1b, Part 3, Part 4 (the bonus epilogue and ED finally show the unguarded Kaoru the earlier scenes withhold).

### T6. The detective genre is under-served structurally
The OP and prologue frame Toa as a dancer-petitioner, not an investigator (Part 1a C1, Part 1b). The middle cases are a single repeated template with little real deduction (Part 3, Case 3 "one clue then setpiece"). The finale contains no investigation (Part 4 P1). The mystery layer is also narratively unfinishable without the romance (Part 4 P2). Slices: Part 1a, Part 1b, Part 3, Part 4.

### T7. Toa's interiority leans on one gag; Kaoru on one register
The "snacks first, justice/pride second" bit recurs verbatim into high-stakes beats where it deflates the stakes (Part 1a C3; rain end Part 4 C10), and the "intimacy reframed as filing/ledger" device, while excellent, is overused within single scenes (Part 2 C2; Part 3 boat). Slices: Part 1a, Part 2, Part 3, Part 4.

---

## 3. Cross-case continuity matrix

Built from the handoff sections of all five slices. "Honored" means set in one place and meaningfully read in another. "Dead-unread" means set but never read in a reachable branch. "Contradiction" means two slices or two beats disagree. Line refs are as cited by the originating slices.

### 3.1 Honored / live state (the load-bearing spine)

| Flag / var | Set where | Read where | Status |
|---|---|---|---|
| `canon_first_scene` | `prologue_canon_encounter.rpy:113` | `prologue.rpy:1099`, `case1_companion.rpy:209`, `case2_festival.rpy:3`, `case_endings.rpy` (canon_romance_eligible) | honored |
| `live_in_companion` | `case1_companion.rpy:290` | Cases 1 to 5, `case_endings.rpy` | honored |
| `permit_signed` | `prologue_canon_encounter.rpy:112`, re-set `case1_companion.rpy:291` | downstream permit checks | honored |
| `permit_effective_days` | encounter `:114`, clamped `case1_companion:293 to 294` | Case 1 bridge / 3-days vs 3-weeks | honored |
| `kaoru_submission` | prologue (75/135/173/347/800), encounter `:115`, case1, `case2:219`, `case4:122` | `case1 907/972` (>=2), `case2 224` (>=3), `case_endings` canon_romance_eligible (>=2) | honored (gate; see contradiction-of-design in section 1 item 12) |
| `physical_initiative` | prologue `752` (+1) / `798` (+2) | `case1_companion.rpy:209` (>=1) | honored, but grab +1 is redundant (Part 1a P8) |
| `formality_tone` | prologue 171/187/203 | prologue 250/254, `case1_companion 53/62` | honored |
| `permit_strategy` | prologue 345/365/385 | prologue 436/440, `case1_companion 484/493` | honored |
| `performance_style` | prologue 619/637 | prologue 693/707, `case1_companion 34/44`, `case_endings:55` | honored |
| `negotiated_terms` | `prologue:498` (re-set `case1_companion:238`) | `prologue:669`, `case1_companion:475` | honored |
| `performance_boldness` | prologue 523/638 | `case_endings:56`, Case 1 | honored |
| `kaoru_resistance` | prologue (multiple) | Case 1 (>=2, >=3), case_endings | honored |
| `companion_accept_tone` | `case1_companion 222/235/260` | case_endings | honored |
| `case1_romance_seen` | Case 1 romance router | `case_endings` all_romance_routes_complete | honored |
| `case2_festival_seen` | `case2_festival:7` | `case_endings` all_romance_routes_complete | honored |
| `case2_romance_seen` | `case2_romance_morning` | case_endings | honored |
| `case3_kaoru_rescue` | `case3:194` | `case4:60`, `case_endings` all_romance_routes_complete | honored |
| `case4_kaoru_defended` | `case4:191` | `case4_5` boat eligibility, `case_endings:71 to 78`, `case5:91` | honored |
| `case5_yoriki_accepted` | Case 5 | `epilogue_romance_bonus_eligible()` | honored |
| `is_this_a_date_asked` | `case3_5:455/528` | `case3_5:522` | honored (in-file) |
| `case1_forged_seal` | `case1_investigation:838` | season spine (likely later) | honored (probable; verify) |
| `case1_manifest_seized` | `case1_investigation:1197` | later cases (likely) | honored (probable; verify) |

### 3.2 Explicit contradictions and gaps called out in the brief

| Item | Set / state A | Set / state B | Status |
|---|---|---|---|
| **Walk-out branch** | `unless_branch = "walk_out"` set `prologue:811`, but the branch routes to a terminal game-over (`:918`) | Read at `case1_investigation:135` and `case1_companion:448/466` with authored "you came back" lines | **Contradiction.** The walk_out value can never reach Case 1; authored content is unreachable. (Part 1a P1) |
| **Season coding** | Festival summer-coded (`case2_festival L68 to 82`); Case 3.5 explicitly spring (`L68/74`) | Case 4.5 explicitly winter (`case4_5 L17/41/98`), days later | **Contradiction.** Spring to winter in roughly two in-story days. (Part 3 #1) |
| **Faction name** | Case 1 commits "Chrysanthemum" (`case1 comb_owner:715`, `appointment_cipher:784`); Cases 3, 4 commit "Chrysanthemum" | Case 2 says both "Plum factor's cousin" (`L245`) and "Chrysanthemum's ledger" (`L261`) | **Contradiction.** Plum vs Chrysanthemum muddle inside one file. (Part 3 #3) |
| **Scorpion comb provenance** | Found planted at the canal recovery site (`case1 404 to 408`), read as careless (`:491`) | Suzu fixes origin at the Plum river room a month earlier, fiercely guarded (`:713`) | **Contradiction / gap.** No one asks how it reached the canal; meticulous-then-careless killer. (Part 2 P1) |
| **Kill-site geography** | Canal-slime clue points upstream / Scorpion (`case1 299, 303 to 304, 103`) | Forged seal asserts he died at the Plum river room (`case1 824, 871`) | **Contradiction.** Physical and documentary chains disagree on the murder scene. (Part 2 P2) |
| **Boat consummation** | Narration implies consummation in the kobune (`case4_5 L220 to 237`) | Kaoru's "not the marina" line frames the act as still to come (`case4_5 L279`) | **Contradiction.** Clarify whether the boat scene is the act. (Part 3 boat [PLOT]) |
| **Romance gating chain** | `canon_first_scene` (encounter:113) + `live_in_companion` (case1_companion:290) + `kaoru_submission >= 2` (accumulated) + `case4_kaoru_defended` (case4:191) | Read in `case_endings.rpy:26 to 111` (canon_romance_eligible, all_romance_routes_complete, epilogue_romance_bonus_eligible) | **Honored** as machinery (Part 4 P6), but design-gated toward compliance (item 12). |

### 3.3 Dead or unread flags (verify downstream or delete)

| Flag / var | Set where | Read where | Status |
|---|---|---|---|
| `rebuke` | `prologue 537/729/812` | `case1_companion:457` (inside the unreachable walk_out block) | dead-unread (revived only if walk-out is fixed; Part 1a P2) |
| `kaoru_formality` | `prologue:172` | nowhere | dead-unread (Part 1a P3) |
| `prologue_refused_dance` | `prologue 536/588` | nowhere | dead-unread (Part 1a P3) |
| `door_response` "leave" value | `prologue:61` | overwritten before its only read at `:155` | dead value (Part 1a P3) |
| `seen_case_zero` | `kaoru_pro_prologue:18` | nowhere | dead-unread (flavor; Part 1b 2.4 P2) |
| `case_zero_smile_choice` | `kaoru_pro_prologue 141/146` | nowhere | dead-unread (flavor) |
| `case_zero_puppet_choice` | `kaoru_pro_prologue 242/247` | nowhere | dead-unread (flavor) |
| `case1_victim_hint` | `case1_investigation:111` | nowhere | dead-unread (Part 2 P5) |
| `case1_scene_choice` | `case1 294/308/326` | superseded by `case1_observation` | redundant/dead (Part 2 P5) |
| `case1_witness_handle` | `case1 729/749/766` | nowhere in slice | dead-unread (verify; Part 2 P5) |
| `case1_comb_owner` | `case1:715` | nowhere in slice | dead-unread (verify) |
| `case1_appointment_cipher` | `case1:784` | nowhere in slice | dead-unread (verify) |
| `case1_sponsorship_flirt` | `case1_companion 35/118/264/370` | nowhere | dead-unread (Part 2 P3) |
| `toa_overjoyed` | `case1_companion:261` | nowhere | dead-unread |
| `companion_salary` | `case1_companion:195` | nowhere | dead-unread |
| `case1_kaoru_trust` | `case1` (eight places) | never tested | dead-unread (verify romance router; Part 2 P6) |
| `case2_scene_choice` | `case2 110/122/135` | never read again (outcome force-set) | dead-unread (Part 3) |
| `case3_clue_clerk` | `case3:140` | milestone reads only bolt/shelf | dead-unread, no payoff (Part 3) |
| Accumulated stats (`insight`, `honor`, `composure`, `compliance`) | written throughout Cases 2 to 4 | only `kaoru_submission` read in-slice | verify Case 5/endings consume, else flavor (Part 3 section 3e) |

Also note the maintenance traps (not dead, but fragile): `case4_date_interlude_seen` is the legacy "seen" marker used by Case 3.5 (Part 3 section 3a/3g); `case4_date_interlude.rpy` is a dead 2-line redirect kept for save-compat; `case1_5_romance_seen` versus `case1_romance_seen` are confusably named (Part 2 P4).

---

## 4. Central mystery throughline

Tracing the season crime: the Chrysanthemum patron, the forged Emerald seal, the smuggling ring, and "Case One's flower."

- **Case 1 (seeds).** Miya Jiro, a Crane guest-house ledger clerk, is pulled from a noble-quarter canal, written off as a drowning, and identified by Toa and Kaoru as strangled and staged. He had found a barge manifest of false cargo (rice on paper, resin in the hold). A Scorpion comb is planted, a forged Emerald seal (sixteen petals against the office's fourteen) locked the death room, and geisha Suzu names a flower-aliased Scorpion patron, "the Chrysanthemum," who tips in foreign silver. The barge manifest is seized; the factor flees. The Chrysanthemum's identity is left open by design. (Part 2 section 3.4.)
- **Case 2.** The burned Academy packet and the murdered courier Tsubaki. The trail runs clerk to warehouse foreman to the factor's cousin, who escapes. Only the "trap" branch surfaces the Chrysanthemum-ledger lead. (Part 3 section 3b.)
- **Case 3.** The sabotaged bolt room and a mislabeled Scorpion dye lot. The trail reaches the Chrysanthemum cousin's runner offscreen; the "roots" explicitly remain. (Part 3 section 3b/3c.)
- **Case 4.** The dock raid on foreman Kurogane (Scorpion-trained). The sixteen-petal forgery returns ("Case One's flower never drowned. It just moved into a warehouse"); the foreman is detained and a ledger seized, but the cabal's roots remain. (Part 3 section 3b.)
- **Case 5 (resolution layer).** The "Left Hand" finale is a public hearing and appointment, not a case. There is no clue, suspect, or deduction. The text states "The Chrysanthemum root still has tendrils in the pleasure quarter" and "Case Five is pinned, not closed. The city still lies." (Part 4 P1.)

**Verdict: the throughline is deferred, not paid off.** Each case is locally "pinned, not closed," which is fine serialization, but the season ends with the spine unresolved and the finale openly admitting it. This works only if it is framed as a deliberate thesis ("the city never lets you close the big file"), which the text currently only half-states. As written, a player who tracked the Chrysanthemum across five cases reaches the end without a culprit, a motive payoff, or an arrest of the patron. Either commit to the deferral in-voice and early, or add at least one concrete investigative beat to Case 5 so the finale earns the word "investigation." A second structural consequence: the finale is gated behind full romance completion (`all_romance_routes_complete()`), so the criminal layer is narratively unfinishable for a non-romance player, who gets only the ten-line discharge stub. (Part 4 P2.)

---

## 5. Branch and ending audit

Consolidated from the Part 4 ending table, with the prologue and mid-game bad ends folded in for completeness.

| # | Ending / beat | Label | Routed by | Earned / coherent? |
|---|---|---|---|---|
| 1 | Canon "Left Hand" finale (sworn yoriki, week one) | `case5_epilogue_week_one` | `case5_yoriki_accepted` via `case5_yoriki_menu` (`:176`) | Yes. Pays off the provisional-attachment setup. |
| 1a | Sub-branch: private inner-office confession | `case5_private_extra` | "Sign and follow him to the inner office" (`:208`) | Yes. |
| 1b | Sub-branch: bedroom intimacy | `case5_private_intimacy_fade` | "Come to the screen" (`:262`) | Yes. |
| 1c | Sub-branch: bow at threshold (no intimacy) | back to `case5_epilogue_week_one` | "Bow at the threshold" (`:266`) | Yes; clean boundary-respecting variant. |
| 2 | Romance bonus epilogue (kotatsu afternoon) | `epilogue_romance_bonus` | `epilogue_romance_bonus_eligible()` after #1 (`case5:322`) | Yes. Fully gated, no replay, warm payoff. |
| 3 | ED credits montage ("The Liar's String") | `ed_sequence` | Main-menu call only (`:24`); not chained from #1/#2 | Content earned; **routing questionable** (P13). |
| 4 | Non-canon discharge (served, no left hand) | `case5_noncanon_discharge` | `not all_romance_routes_complete()` at finale (`:14`) | Coherent but thin (P2); criminal plot unresolved. |
| 5 | **Bad end: refusal, sold to the quarter** | `gameover_case5_chained` | Refuse (`:182`) then "Let the pleasure quarter buy what I would not sign" (`:395`) | **Coherent mechanically, NOT earned** (C2/P5/P8). |
| 6 | **Bad end: refusal, corrective custody / cage** | `gameover_case5_quarter_cage` | Refuse (`:182`) then "Keep me in magistrate custody" (`:398`) | **Same problem as #5.** Unearned escalation. |
| 6x | Refusal warning opt-out | returns to title | "Return to title" (`:385`) | Safe exit, not an ending. |
| 7 | Prologue rain bad end, then brothel sale | `gameover_rain` to `prologue_bad_end_brothel` | Refuse the dance, then "Leave the magistrate's office" | Yes, earned. Pride-over-survival flaw is the cause. |
| 8 | Case 1 canal (board barge alone) | `gameover_case1_canal` | Case 1 "Board alone" choice | Yes (pride / going alone), but unsignaled and mis-named label (Part 2 P8). |
| 9 | Case 1 punishment (opt-in) | `case1_bad_end_kaoru_punishment` | Toa demands punishment (`:477`) | Yes; opt-in consent makes dark-Kaoru coherent (model for fixing #5/#6). |
| 10 | Case 2 kiln alley | `gameover_case2_alley` | Case 2 "go in alone" | Yes (pride / going alone). |
| 11 | Case 3 bolt-room injury | `gameover_case3_injury` | Case 3 "dodge it alone" | Yes. Blocks romance via `case3_bad_end_injury`. |
| 12 | Case 4 abandon table | `gameover_case4_abandon` | Case 4 abandon | Yes (pride). Notably non-brutal discharge model. |
| 13 | Case 4 slain on dock | `gameover_case4_slayn` | Case 4 "I will cut him down myself" | Yes (pride / Crane-blade flaw). |
| 14 | Case 4.5 kobune throw injury | `gameover_case4_5_boat` | Case 4.5 "fight the throw" | Yes. |
| 15 | Canon Case 1 romance interludes | `case1_romance_route_*` | `case1_romance_router` thresholds | Coherent. |
| 16 | Canon Case 2 morning interlude | `case2_romance_morning` | Post-Case-2 companion route | Coherent. |

**The two Case 5 refusal bad ends (#5 and #6)** are the only endings whose characterization state is not earned: the accept branch, both canon epilogues, and the ED all portray a protective Kaoru, so trafficking/caging Toa for declining a post reads as a different character. The fix template is already in the game (the Case 1 opt-in punishment, #9, and the Kaoru-absent rain end, #7).

**The ED-routing question (#3).** The ED is "Callable from main menu," and nothing in `case5_epilogue_week_one` or `epilogue_romance_bonus` calls `ed_sequence`. So the canon route never auto-rolls its own credits. Either this is an intentional gallery piece, or the canon good end is missing its emotional capstone. The ED's red-thread / open-birdcage motif directly answers the finale's themes (Part 4 P14), which argues for wiring it in. High-value decision for the owner.

---

## 6. Quick wins versus larger rewrites

### 6.1 Quick wins (trivial line, flag, and cosmetic fixes)

Anachronism and register line swaps (most have before-to-after rewrites in the slices):
- Modern math/ledger idiom sweep: "order of operations" (`script.rpy:50`), "do the math" (`prologue:463`), "police" (`case5:134`), "montage" (`case5:303`), "classified information" (`epilogue_romance_bonus:49`), "line item on my evening" (`case_endings:546`), "alley math" (`epilogue_rain_gameover:186`).
- Digital clocks to temporal hours (`kaoru_pro_prologue 41/163/184/190`).
- Gregorian date "March twenty-sixth" to a Rokugani anchor (`prologue:434`).
- "opium" to "poppy resin" (`case1_investigation:184`); "curtsey" to "bow" (`case1_companion:47`); "energy" slang (`case1_companion:38`).
- "asparagus" kaiseki to udo or warabi (`case3_5:162`); "twitterpated" sprite tag (`case3_5 179/437`).
- L5R color fix: "Scorpion grey" / "grey wax" to red-and-black or "unmarked grey (concealment)" (Cases 2 and 4).
- Grammar: "sixteenth-petal" to "sixteen-petal" (`case4:99`).
- `sochira-no-kata` misused as a vocative (`prologue 42/176`); confirm or replace with a proper honorific address.

Cosmetic / production:
- Em and en-dash sweep artifacts: trailing " , " in ED subtitles (`ed_sequence 153/177/209/221`, use ellipses); en dashes in code comments (`opening 15/18`, `case_endings:61`); bare appositive at `prologue_canon_encounter:28`.
- Standardize "Tear Drop Island" versus "Teardrop Island" (Case 3.5 vs Case 4.5).
- Standardize honorific formatting ("Toa san" vs "Hiromi-san" vs "To-chan"); recommend hyphenated.
- Cut one of the redundant title drops (`script.rpy:44` versus the OP title drop).
- Settle naming drift "encounter / ending / first scene" for one beat (`prologue_canon_encounter` P1).
- Remove shipped authoring notes and the drifted onset comment (`opening 188/243/250`).
- Fix recycled voice files in Case 4 (reuses `kaoru_295`, `kaoru_298`, `narrator_257`, `toa_257` against changed text).
- Settle one "To-chan" rule (public versus private).

Flag hygiene (delete or wire, see matrix 3.3):
- Delete the dead/unread flags listed in section 3.3, or give them a reader. Most are one-line deletions.
- Add a `case3_clue_clerk` milestone branch or fold its content in.
- Add a one-line note on the `case4_date_interlude.rpy` redirect and the legacy `case4_date_interlude_seen` marker.

### 6.2 Larger rewrites (structural)

- **Release blocker: dev menu as first screen.** Flip `dev_chapter_pick_enabled` to `False` or gate it on `config.developer` for any canon build. The edit is one line, but it is a ship blocker, so it belongs on the structural checklist. (Item 1.)
- **Walk-out branch redesign.** Route `unless_branch == "walk_out"` into Case 1 non-canon ("she came back") so the authored Case 1 lines fire, which also revives the `rebuke` axis; or delete the dead branches. (Item 2.)
- **Central mystery logic.** Either commit Case 5 to a deliberate "the city never closes the big file" thesis seeded earlier, or add one real investigative beat. Also resolve the Case 1 comb provenance, the kill-site geography, and the "frame the Scorpion loudly" versus "hide the death quietly" intent split. (Items 3, 8; Part 2 P1/P2/P3.)
- **Bad-end redesign.** Replace the Case 5 refusal trafficking/cage with estrangement or discharge, or seed an institutional "the city collects the unsigned left hand" before Case 5. Give the prologue walk-out a retry off-ramp at parity with the refuse path, and add one telegraph before the rain "leave." Use the Case 1 opt-in and the Kaoru-absent rain end as models. (Items 4, T2.)
- **Peril-binary variety.** Reshape at least one mid-game climax (ideally Case 4) so it moves the relationship somewhere new, differentiate the cloned Case 3 rescue and Case 4 defend, and give Toa one clean physical success. (Items 6, T1.)
- **Seasonal continuity.** Pick one season for the whole Cases 2 to 4.5 stretch, or insert real time-skips. (Item 5.)
- **Faction name and Imperial-mon stakes.** Settle Chrysanthemum versus Plum and propagate; decide whether the sixteen-petal seal is the Imperial mon (if so, raise the stakes to treason in-text). (Item 7.)
- **Submission-gated romance.** Gate or reframe the ungated physical "Unless?" answer, and rebalance so an assertively-played Toa is not silently written out of the romance. (Item 12.)
- **Seed the detective.** Give Toa one unprompted correct deduction in the prologue, and reframe the OP name card and her first line so the investigator role is set, not sprung. (Item 9, T6.)
- **Deepen Kaoru.** Let the banter armor drop once per intimate scene, pay off the Case Zero "almost-smile," and vary the advance/retract so only the best instance (Case 3.5) peaks. (Item 10, T5.)
- **Boat consummation contradiction.** Decide whether the kobune scene is the act, and reconcile the "not the marina" line. (Section 3.2; Part 3 boat.)
- **ED routing.** Wire the ED into the canon ending or confirm it is gallery-only. (Section 5 #3; Part 4 P13.)
- **Sponsorship fig-leaf.** Add one line of mutual awareness that "sponsorship, not a courtesan's contract" is a knowing legal fiction, so the 1.5 interlude reads as intended subtext rather than self-contradiction. (Part 2 companion P1.)

---

## 7. Index of source section docs

Relative to this file (`docs/main-game-story-review-2026-06-05.md`):

- Setup (script flow, OP, canon encounter, Case Zero): [`review/main-game-review-part1b-setup.md`](review/main-game-review-part1b-setup.md)
- Prologue (`prologue.rpy`, the "Unless?" branch, bad ends): [`review/main-game-review-part1a-prologue.md`](review/main-game-review-part1a-prologue.md)
- Case 1 plus the 1.5 romance interlude: [`review/main-game-review-part2-case1.md`](review/main-game-review-part2-case1.md)
- Cases 2, 3, 4 plus interludes and the boat: [`review/main-game-review-part3-cases234.md`](review/main-game-review-part3-cases234.md)
- Case 5 finale plus all endings and epilogues: [`review/main-game-review-part4-case5-endings.md`](review/main-game-review-part4-case5-endings.md)
