# Main-Game Editorial Review, Part 1a: Prologue (First Meeting, "Unless?" Branch, Bad Ends)

Editorial review only. No `.rpy` files were edited. Suggestions are proposals for the parent agent to accept or reject. Register kept feudal-Japan L5R (Rokugan / Ryoko Owari). Em dashes are avoided in all suggested rewrites, per `docs/style-no-em-dash.md`.

File reviewed:
- `game/prologue.rpy` (1105 lines)

Cross-file files consulted for continuity only (not edited): `game/stats.rpy`, `game/prologue_canon_encounter.rpy`, `game/epilogue_rain_gameover.rpy`, `game/case1_investigation.rpy`, `game/case1_companion.rpy`, `game/case_endings.rpy`.

---

## 1. Slice summary

The prologue is the whole game's first impression: Kakita Toa, a post-gempukku Crane dancer newly arrived from Unicorn lands, gets lost in the noble quarter, knocks on the wrong door, and lands in the office of Emerald Magistrate Kitsu Kaoru, who discovers her performer's permit has expired and turns the renewal into a late-night audition and a power game. The player steers tone (formality, comply vs peek, negotiate vs refuse, rebuke vs lean in) toward one of three answers to Kaoru's signature "Unless?" cliffhanger: a physical answer (canon route into Case 1 companion), a verbal answer (non-canon reopening three weeks later), or walking out. Two dark fail-states branch off (a refuse-the-dance path that ends in the rain and the pleasure quarter, and a walk-out path that ends in Kaoru's pursuit), and the scene sets nearly every prologue flag Case 1 later reads.

---

## 2. Findings for `prologue.rpy`

### [PLOT]

- **P1. The "walk out" answer is a hard game-over here, but Case 1 was written assuming the player can choose it and come back. This is the slice's highest-impact defect.** At the "Unless?" menu, "Walk out, this crossed a line." sets `unless_branch = "walk_out"` (line 811) and routes to `prologue_walkout_ending` (line 820) and then unconditionally to `prologue_bad_end_kaoru` (line 918), which ends in `return` / Game Over (lines 1056, 1088). `unless_branch = "walk_out"` is set nowhere else in real play, and the canon path that reaches Case 1's companion file always sets `unless_branch = "physical"`. Yet both Case 1 files contain authored, voiced content gated on the walk-out value: `case1_investigation.rpy:135` (`if unless_branch == "walk_out"`, with `toa "I came back. That has to count for something."`) and `case1_companion.rpy:448` (`kaoru "You came back. I noted that."`). That dialogue can never fire. Decide intent: either (a) route walk-out into Case 1 non-canon ("she came back") so the existing Case 1 lines pay off, or (b) delete the dead `walk_out` branches in Case 1. Recommended (a), because Case 1 clearly expects a returning, defiant Toa.
- **P2. `rebuke` is set three times in this file but has zero reachable payoff.** `rebuke` is incremented at line 537 (refuse the dance, +1), line 729 (rebuke the grab, +2), and line 812 (walk out, +2). Its only reader anywhere in the game is `case1_companion.rpy:457` (`if rebuke >= 2`), and that check is nested inside the `unless_branch == "walk_out"` block (`case1_companion.rpy:448`) that P1 shows is unreachable. Net effect: the entire "push back on physical escalation" axis the prologue tracks never changes anything a player can see. Fixing P1 (option a) would also revive `rebuke`; otherwise either wire `rebuke` into a reachable Case 1 beat or stop tracking it.
- **P3. Two more flags are set and never read; one choice-value is overwritten before its only read.** `prologue_refused_dance` is set `True` (line 536) and `False` (line 588) but is read nowhere (only `default` in `stats.rpy:29`). `kaoru_formality = 1` (line 172) is likewise never read. And `door_response = "leave"` (line 61) is always overwritten by "knock_again"/"wait_quietly" at the second-chance menu before its single reader at line 155, so the "leave" value can never be observed. These are dead/illusory and should either be consumed downstream or dropped.
- **P4. The two flags the brief calls "prologue flags" (`canon_first_scene`, `live_in_companion`) are NOT set in this file, and the canon gate rests entirely on an off-file jump.** `canon_first_scene` is only *read* here (line 1099) and is *set* in `prologue_canon_encounter.rpy:113`; `live_in_companion` is set later still, in `case1_companion.rpy:290`. The physical answer's `jump prologue_canon_ending` (line 808) is therefore load-bearing for the whole canon route: that off-file label must set `canon_first_scene = True` and eventually fall through to `prologue_case1_hook` (line 1092), or the canon gate silently fails to non-canon. Worth a one-line code comment at line 808 documenting that contract, and the handoff in section 3 should track these as "set elsewhere."
- **P5. "Leave and find another office" is an illusory choice that always loops back, and the loop quietly removes the exit.** At `prologue_door_menu`, "Leave and find another office." (line 60) grants `honor += 1` and detours through `prologue_door_leave`, but every branch there returns to `prologue_door_second_chance` (lines 112, 118), whose menu only offers "Knock again" / "Wait quietly" (lines 124 to 144). The player is told they can leave, wanders, and is railroaded back with no leave option the second time. The `honor += 1` persists, so it is not inert, but the agency is fake. Consider either making the leave genuinely branch (a short detour scene with a real alternative) or reframing the first option so it does not promise an exit the scene will not honor.
- **P6. The rain bad-end's severity is under-telegraphed, and the fail-state design punishes the most sympathetic choice the hardest.** Refusing the audition (line 535) goes to `prologue_refuse_bad_end`, which at least offers a retry menu ("Try again, swallow your pride." vs "Leave the magistrate's office.", line 586); choosing to leave jumps to `gameover_rain` (line 606), which routes on to `prologue_bad_end_brothel` (implied trafficking; see `epilogue_rain_gameover.rpy:66` and `:114`). The only in-prologue telegraph of that outcome is a soft line, `narrator "Rain finds the noble quarter anyway. Case One will have to wait for a braver night."` (line 605), plus the earlier stakes card at line 582. The jump from "leave with your pride" to trafficking is large for that warning. Worse, the *walk-out* path (line 810), which is the player asserting a boundary against coercion, gets NO retry menu and drops straight into the Kaoru-pursuit bad end (line 918). So the two most ethically sympathetic choices (refuse, walk out) receive the darkest endings, and the walk-out one has no off-ramp at all. Recommend: give walk-out a "swallow your pride / leave" retry beat at parity with the refuse path (and ideally fold it into P1 option a, so walk-out can instead survive into Case 1), and add one more telegraph beat before the rain leave so the brothel outcome reads as earned rather than ambush.
- **P7. The verbal/non-canon route drops a deadline it makes a point of stating.** In the shared social-vacuum beat Toa fixes the clock: "By tomorrow I need proof I belong here." (line 434), and she herself names the consequence of an expired permit, "by morning a gate guard asks for paper, and I have a wet book and a very good bow" (echoed at line 90 / `epilogue_rain_gameover.rpy:90`). But the verbal ending sends her off with the seal explicitly withheld ("then sets it down untouched", line 841) and a three-week timeskip ("Three weeks. I can survive three weeks on curry and pride.", line 874; "Three weeks later...", line 1104). Nothing addresses how she survives three weeks of gate guards on an expired permit after insisting tomorrow was the deadline. Either soften the "by tomorrow" line, or have the verbal exit win her a short grace (a forward-dated provisional chit) so the three-week gap is not a plot hole she narrated herself.
- **P8. The grab "lean in" `physical_initiative += 1` never changes an outcome.** Line 752 grants `physical_initiative += 1`, but its only reader, `case1_companion.rpy:209` (`if canon_first_scene and physical_initiative >= 1`), is only reachable on the canon path, which requires the physical "Unless?" answer that already grants `physical_initiative += 2` (line 798). So the stat is always at least 2 by the time it is read, and the grab increment is redundant. Harmless, but if `physical_initiative` is meant to have texture (lean-in vs not), give it a gate that distinguishes 1 from 2.

### [CHARACTER]

- **C1. The detective premise is never seeded.** This is an otome *detective* VN, but the prologue presents Toa purely as dancer-petitioner, and her single flicker of investigative instinct (the "Peek at the shelves anyway." beat, where she clocks "Lion mon here, Emerald seal there", lines 294 to 300) is framed as a discipline failure Kaoru scolds ("I said sit. Not catalog my trophies.", line 303), not as competence. Case 1 immediately asks her to read a body and a forged seal, so the opening should plant her eye: let the shelf-peek (or a new beat) show one correct, unprompted deduction about Kaoru or the room that he grudgingly registers, so her later detective turn is set up rather than sprung.
- **C2. Kaoru is established as one relentless predatory note, and the better version of him is already on the page being underused.** Within a single first meeting he issues a stack of sexual threats to a stranger: "You'll need it on this cushion before I touch the hanko." (line 257), "We'll discover which tonight." (line 219), "We'll test that claim before dawn." (line 261), "We'll see what it's worth." with the `hungry` expression (line 409). The control/tease dynamic lands, but at this density he flattens into menace with little wit or curiosity to make him a viable romance lead. The sharper Kaoru is right there and barely used: "You ask for terms. That almost earns respect." (line 378) and "Plain speech. You waste less of my evening than most." (line 196). Trade two or three of the early innuendo beats for that competence-respect register so his interest in *her*, not just appetite, drives the audition.
- **C3. Toa's interiority leans on one gag until it undercuts her.** The snacks-vs-pride bit is charming the first time ("Snacks first was the plan. Pride second. I got the order wrong.", line 603) but becomes her default inner voice ("Snacks first. Justice second.", line 877; "...Snacks first. Pride second. I finally got the order right.", `epilogue_rain_gameover.rpy:103`). When it recurs verbatim inside the rain game-over, a beat that is meant to be devastating, it reads flip and deflates the stakes. Keep one or two instances and give her a second register (fear, resolve, a Crane-specific pride) for the high-stakes beats.
- **C4. The physical "Unless?" answer is available no matter how resistant the player has built Toa, which risks tonal whiplash.** `prologue_unless_menu` (line 783) offers "Answer physically, close the distance." (she "straddles the chair's arm", line 802) with no gate on prior `compliance`, `performance_boldness`, or `rebuke`. A player who chose direct address, refused, and rebuked the grab can pivot in one beat to straddling the magistrate. Either gate the physical option (or its framing) behind some prior warmth/boldness, or give it an alternate narration line that acknowledges a defiant Toa choosing this on her own terms rather than as seduction.

### [DIALOG]

Worst offenders with before -> after rewrites (all em-dash-free, period register):

- **D1. Line 781 (clinical, anachronistic narration).** "Power imbalance made visible" is modern sociological register and tells the theme outright.
  - Before: `"The chair creaks. Hakama folds. Power imbalance made visible, two figures, one question hanging."`
  - After: `"The chair creaks. Hakama folds. Two figures, one of them seated like he owns the floor she is standing on, and a single question left hanging between them."`
- **D2. Line 723 (abstract tell).** "Entitlement dressed as appraisal" names the subtext instead of showing it.
  - Before: `"His hand finds her wrist, not painful, not gentle. Entitlement dressed as appraisal."`
  - After: `"His hand finds her wrist, not painful, not gentle, the grip of a man weighing goods he already assumes are his."`
- **D3. Line 463 (modern idiom).** "Do the math" is anachronistic.
  - Before: `kaoru "Dance listed. Venue missing. Patron column blank. Do the math."`
  - After: `kaoru "Dance listed. Venue missing. Patron column blank. Even a junior clerk can read what that adds to."`
- **D4. Line 207 (modern-clever construction).** The geography/legality pun reads contemporary.
  - Before: `toa "I promise I'm only lost geographically, not legally. May I present my renewal request?"`
  - After: `toa "It is only your corridors I lost my way in, Magistrate, not the law. May I present my renewal?"`
- **D5. Line 434 (calendar anachronism).** "March twenty-sixth" is a Gregorian month name; Rokugan does not use Western months.
  - Before: `toa "It's March twenty-sixth. By tomorrow I need proof I belong here."`
  - After: `toa "The month is almost out. By tomorrow I need proof I belong here."`
  - (If a sharper anchor is wanted, tie it to a Rokugani festival or "before the next gate-count" rather than a numbered date.)
- **D6. Line 311 (clunky interjection).** The stacked "when, if," stalls the line.
  - Before: `kaoru "Since you admire my shelves, admire my seal from a distance when, if, you earn it."`
  - After: `kaoru "Since you admire my shelves so freely, you may admire the seal from a distance. If you ever earn it."`
- **D7. Line 514 (mixed metaphor).** Dawn does not "break ankles"; the image tangles.
  - Before: `toa "Then I'll dance until you're satisfied or until dawn breaks my ankles."`
  - After: `toa "Then I'll dance until you're satisfied, or until dawn, whichever gives out first."`
- **D8. Line 102 (modern cliche).** "Eats petitioners for breakfast" is a contemporary stock phrase.
  - Before: `"Clerk" "That's the one who stamps interclan renewals. Good luck. He eats petitioners for breakfast."`
  - After: `"Clerk" "That's the one who stamps interclan renewals. Good luck. Petitioners walk in proud and leave as paperwork."`

Additional dialog flags (no rewrite, mostly register/term checks):

- **D9. "sochira-no-kata" is misused as a direct address (lines 42, 176).** It is a polite third-person referential ("that person over there"), not a vocative; calling someone it to their face is off. Use a proper honorific address (an apology with a bow, or "Magistrate-sama" once his title is known) instead of "sochira-no-kata!" Confirm this is not a deliberate stylization.
- **D10. "curry shop" / "curry" recurs as a motif (lines 401, 426, 915, and into the bad ends).** Curry reads as an anachronistic import in a feudal-Japan register; because it recurs (and continues into Case 1, see Part 2 D7), if it is wrong it is wrong repeatedly. Consider a period-appropriate humble eatery (a noodle stall, a rice-and-pickles counter) if strict register is wanted, or accept it as an established Ryoko Owari flavor and keep it consistent.
- **D11. "To-chan" appears only in the assault bad end (line 933).** The affectionate "-chan" diminutive used mid-coercion is jarring; it can read as deliberately possessive menace, but it is the only time he uses it and it sits oddly. Confirm intent, or swap for a colder possessive. (Part 2 C2 raises the same diminutive used publicly in Case 1, so settle a single rule for when Kaoru uses it.)
- **D12. Title consistency and em-dash compliance.** Kaoru demands his title ("Emerald Magistrate Kitsu Kaoru. You will use my title", line 223), but Toa later drifts to the softer "Magistrate-sama" (lines 733, 834, 845, 861); pick one register for "after he has set the rule." On the positive side, the file is already em-dash-clean (commas and ellipses do the work, e.g. lines 615, 723), so no em-dash removals are needed here.

---

## 3. Continuity handoff

### 3.1 Flags / persistent vars / stats this file SETS (with line refs and where they are READ)

Routing / branch flags:
- `door_response` set at 61 ("leave", dead value, see P3), 66/126 ("knock_again"), 74/134 ("wait_quietly"). READ only at line 155 (knock SFX/lines). Used cosmetically for a choice CG (`images/cgs-choices.rpy`).
- `door_left_once` set `True` at 89. READ at 88 (controls first-vs-repeat leave text).
- `formality_tone` set at 171 ("hyper_formal") / 187 ("direct") / 203 ("humorous"). READ at 250, 254 (this file) and `case1_companion.rpy:53, 62`.
- `discipline_check` set 0 at 284 / 1 at 295. READ only at line 469 (this file).
- `permit_strategy` set at 345 ("academy_trip") / 365 ("local_fix") / 385 ("plead"). READ at 436, 440 (this file) and `case1_companion.rpy:484, 493`.
- `negotiated_terms` set `True` at 498. READ at 669 (this file) and `case1_companion.rpy:475` (note: `case1_companion.rpy:238` also re-sets it).
- `prologue_refused_dance` set `True` 536 / `False` 588. READ nowhere (dead, see P3).
- `performance_style` set at 619 ("formal_dance") / 637 ("flirtatious"). READ at 693, 707 (this file), `case1_companion.rpy:34, 44`, `case_endings.rpy:55`.
- `unless_branch` set at 785 ("verbal") / 797 ("physical") / 811 ("walk_out"). READ at `case1_investigation.rpy:135`, `case1_companion.rpy:448, 466`. NOTE: "walk_out" is currently terminal here, so that value never reaches Case 1 (see P1).

Stat axes (incremented; consumed by `case_endings.rpy` and later cases):
- `honor` (62, 188, 366, 786), `composure` (67, 127, 285, 386), `insight` (204, 296, 499, 786), `compliance` (76, 136, 346, 524, 690, 751, 799).
- `kaoru_submission` (75, 135, 173, 347, 800). Romance gate: `case_endings.rpy:31` requires `kaoru_submission >= 2` (canon path also gets +2 in `prologue_canon_encounter.rpy:115`).
- `kaoru_resistance` (189, 367, 538, 639, 730, 813). READ in Case 1 (`>= 2`, `>= 3`).
- `performance_boldness` (523 +1, 638 +2). READ `case_endings.rpy:56` (flirtatious gate) and Case 1.
- `physical_initiative` (752 +1, 798 +2). READ `case1_companion.rpy:209` (`>= 1`); see P8.
- `rebuke` (537, 729, 812). Only reader is unreachable (see P2).
- `kaoru_formality` (172). READ nowhere (dead, see P3).

### 3.2 Flags this file READS but does NOT set (cross-file dependencies)

- `canon_first_scene` READ at line 1099 (the canon vs non-canon switch in `prologue_case1_hook`). SET in `prologue_canon_encounter.rpy:113`, reached via the physical-answer `jump prologue_canon_ending` (line 808). See P4. `live_in_companion` (named in the brief) is not touched here; it is set in `case1_companion.rpy:290`. Both are honored by Cases 1 to 5 and `case_endings.rpy`.

### 3.3 Threads opened here that later cases must honor

- **Kaoru dynamic (strongly opened):** transactional control, the seal as leverage, and the recurring threat "you'll knock again when hunger wins" (lines 578, 818, 900; reprised `prologue_bad_end_kaoru:1068`). The water-cup-as-witness motif is planted (lines 318, 479, 654, 857) and Case 1+ should keep it as his tell. The permit ends "pending" / forward-dated, which is the hook the companion offer pays off.
- **Romance/power axis (opened):** `kaoru_submission` vs `kaoru_resistance` start accumulating here and gate the romance ending downstream; `performance_style == "flirtatious"` + `performance_boldness` is the flirtation thread `case_endings.rpy` reads.
- **Mystery/detective thread (barely opened):** the only seed is Kaoru's shelves of case files and interclan seals (lines 288, 299) plus "Interclan residence requires Emerald approval" (line 266). The Case 1 canal body, the Miya/Crane-politics angle, and the Scorpion "Chrysanthemum" patron are NOT seeded here. See C1: this is the biggest setup gap for the genre.
- **Companion vs witness fork (opened, decided later):** prologue routes canon -> `case1_companion_offer` (three days) vs non-canon -> `case1_noncanon_start` (three weeks); `live_in_companion` is decided in Case 1, not here.
- **Snacks/pride motif (opened):** lines 603, 874, 877; recurs in Case 1 (crackers/curry). Keep but vary (see C3).

### 3.4 Bad-end and route routing map

- **Canon (physical):** `prologue_unless_menu` -> "Answer physically" (line 796) -> `show_cg canon_proposition` -> `jump prologue_canon_ending` (line 808, in `prologue_canon_encounter.rpy`; sets `canon_first_scene = True`, `kaoru_submission += 2`) -> ... -> `prologue_case1_hook` (line 1092) -> `canon_first_scene` True -> "Three days later" -> `case1_companion_offer`.
- **Non-canon (verbal):** "Answer verbally" (line 784) -> `prologue_verbal_ending` (822) -> `jump prologue_case1_hook` (879) -> `canon_first_scene` False -> "Three weeks later" (1104) -> `case1_noncanon_start`.
- **Bad end A, rain / pleasure quarter:** refuse the dance (line 535) -> `prologue_refuse_bad_end` (549) -> retry menu (586): "Try again" -> `prologue_office_dance`; "Leave the magistrate's office" -> `jump gameover_rain` (606) -> `epilogue_rain_gameover.rpy:66` -> `prologue_bad_end_brothel` (`:114`, sets `seen_gameover_rain`). Implied trafficking, fade-to-black.
- **Bad end B, Kaoru pursuit:** walk out (line 810) -> `prologue_walkout_ending` (881) -> `prologue_bad_end_kaoru` (922) -> `return` / Game Over (1056, 1088). Implied coercion, no retry off-ramp. (This is the route that strands the Case 1 "walk_out" content; see P1.)

---

## 4. Counts and highest-impact changes

Counts:
- [PLOT] findings: 8 (P1 to P8)
- [CHARACTER] findings: 4 (C1 to C4)
- [DIALOG] findings: 12 (D1 to D12), of which 8 are before -> after rewrites (D1 to D8)

The 3 to 4 highest-impact changes:
1. **Resolve the walk-out contradiction (P1).** Route `unless_branch == "walk_out"` into Case 1 non-canon ("she came back") so the already-written, already-voiced Case 1 lines fire, or delete those dead branches. This is the one defect that makes authored content unreachable across files (and reviving it also fixes the dead `rebuke` stat, P2).
2. **Seed the detective (C1).** Give Toa one unprompted correct read of Kaoru or the room in the office (repurpose the shelf-peek beat) so the genre promise and her Case 1 competence are set up, not sprung.
3. **Make the fail-states fair (P6).** Give the walk-out path a retry/soft-fail at parity with the refuse path, and add one telegraph beat before the rain "leave," so the harshest outcomes do not land on the most sympathetic choices without warning.
4. **Deepen Kaoru and de-clutter dead flags (C2 + P3/P8).** Trade two or three early innuendo beats for the competence-respect register the script already contains, and drop or wire up the flags that currently do nothing (`kaoru_formality`, `prologue_refused_dance`, the "leave" value of `door_response`, the redundant grab `physical_initiative`).
