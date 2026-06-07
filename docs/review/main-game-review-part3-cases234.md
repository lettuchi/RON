# Main Game Editorial Review - Part 3: Cases 2, 3, 4 (investigations + interludes + boat)

Scope: editorial review only. No `.rpy` files were edited. All line numbers refer to the files as read on 2026-06-05.

Files reviewed (canon order):
`case2_investigation.rpy`, `case2_festival.rpy`, `case3_investigation.rpy`, `case3_5_date_interlude.rpy`, `case4_investigation.rpy`, `case4_date_interlude.rpy`, `case4_5_boat.rpy`.

---

## 1. Slice summary

This slice runs the three middle investigations (the burned Academy packet, the sabotaged bolt room, the dock-raid swordfight) plus the romance beats braided between them (the hill festival, the Tear Drop Island date, the boat). The investigations share one connective thread - "Case One's flower," the surviving Chrysanthemum/Scorpion factor whose cousin keeps reappearing - and each case closes "pinned, not closed," correctly leaving the cabal's roots for Case 5. The writing is strong line-by-line, but the three cases are built on an identical structural template and an identical "trust Kaoru or be gravely hurt" peril-binary, and a spring-to-winter seasonal contradiction runs straight through the tightly-spaced timeline.

Finding counts: **[PLOT] 27 · [CHARACTER] 18 · [DIALOG] 15 · before->after rewrites: 8.** (A handful of [PLOT] bullets are positive continuity confirmations, e.g. "branch bookkeeping is clean," rather than defects; the rest are actionable.)

---

## 2. Per-file sections

### `case2_investigation.rpy`

#### [PLOT]
- **Villain faction is named two different ways inside one file.** Line 245 (close) calls the culprit "the **Plum** factor's cousin," but line 261 (trap branch) calls it "the **Chrysanthemum's** ledger," and Case 3/4 commit to "Chrysanthemum." Pick one house and propagate. (L245 "the cousin has slipped out with the tide"; L261 "straight back to the Chrysanthemum's ledger.")
- **Clue flags do not gate the resolution; the case self-heals to the same state.** If the player picks "body" or "runner" (not "ash"), `case2_packet_found` is force-set anyway at L162-167, and `case2_courier_name` is force-set to "Tsubaki" at L159-160. The three investigation choices (`ash`/`body`/`runner`) therefore have no downstream consequence beyond stats - the case reaches an identical outcome. Acceptable for a vertical slice, but flag that `case2_scene_choice` is never read again.
- **"Go in alone" is an instant game-over (L148-157).** This is the first instance of the slice-wide pattern "act independently -> punished." Noting it here because by Case 4.5 the pattern has fired four times.
- **The escaped cousin is a deliberately open thread (L245).** Good for serialization, but confirm Case 5 actually collects him; right now he is the only consequence of solving Case 2 and he simply leaves.
- **Trap-branch payoff is the only branch that advances the metaplot.** Only `case2_confront_choice == "trap"` surfaces the Chrysanthemum-ledger lead (L258-261); `accuse` (L253-256) and `defer` give no metaplot thread. A player who never picks "trap" never hears the throughline named in Case 2.

#### [CHARACTER]
- **Kaoru's "[virtue]. Rare in [you/a dancer]." construction starts here and becomes a tic.** L62 "Methodical. So the Academy taught you something useful," L86 "Discipline. Rare in you." The same backhanded-compliment frame recurs in Case 3 (L65 "Arithmetic. Rare in a dancer.") and Case 4 (L129 "Discipline. Rare, in a dancer."). Vary at least two of these.
- **Toa's strongest agency beat in the file is the defiant branch (L48 "Don't dangle my future like a coin to barter").** Good. But the menu rewards submission/compliance structurally (the "defer" path feeds `kaoru_submission`, which gates the entire romance chain - see Continuity handoff), so an assertively-played Toa is quietly written out of the romance. Worth a design note for the parent.
- **Tsubaki is humanized in one good line (L130, L251) then dropped.** "His name was Tsubaki ... I'll keep his name even if the watch won't." It is a nice interiority beat; it never returns. If it is meant to characterize Toa's compassion, consider a one-line callback later.

#### [DIALOG]
- On-the-nose recap, L185:

before:
> toa "Case One forged your seal from the outside. This one reaches all the way inside your office."

after:
> toa "Case One came at your seal from the street. This one was already holding your brush."

- Slightly stilted threat, L202:

before:
> kaoru "Factor. Scorpion. Ash. Give me the rest, or I let the kiln finish what's left of your tongue."

after:
> kaoru "Factor. Scorpion. Ash. Fill the gaps between those three, or the kiln does the talking for you."

- L74 "the Scorpion leftovers" and L146 "Scorpion grey" - see the recurring L5R color note under `case4_investigation.rpy` [DIALOG]. Scorpion's canon colours are red and black, not grey.

---

### `case2_festival.rpy`

#### [PLOT]
- **Season-coding starts the timeline problem.** The festival is fireworks-and-hill-festival coded (L68-82, "Fireworks climb over the canal. Chrysanthemum bursts"), which reads summer. This is days before Case 3, which is days before the explicitly-spring Case 3.5 and the explicitly-winter Case 4.5. See the cross-file seasonal contradiction in the Continuity handoff - this file is where the seasonal drift begins.
- **Catchphrase seeding.** "The watch files whatever I sign" (L25) and "Keep up, To-chan" (L33) both recur verbatim in Case 3.5 (L37, L62) and the boat (L32). Establishing catchphrases is fine; three near-identical uses inside one slice is heavy. Recommend retiring one instance.
- **Branch bookkeeping is clean.** `case2_festival_kiss_only` (L91) vs `case2_festival_intimate` (L135) both terminate at the shared `case2_festival_bridge` (L196) and then route correctly to `case2_romance_morning`/Case 3 (L216-220). No flag leak.

#### [CHARACTER]
- **This is the relationship's high point of warmth, and it lands.** L120's interiority ("the ache of wanting his nod to mean more than patronage") is the clearest articulation of Toa's wish in the slice. Keep it; later beats should escalate past it rather than restate it (they currently restate it - see boat).
- **The advance/retreat shape is established here and never varies.** Kaoru kisses her, then immediately devalues it (L104-108 "Don't go filing that under promises ... A festival kiss is paper confetti"). The identical move repeats in Case 3.5 ("Forget the second sentence," L507) and Case 4 ("Forget I said it," L228). It is his core characterization, but four retractions in a row across consecutive scenes flattens into a crutch.

#### [DIALOG]
- Generally the strongest dialogue in the slice; L58 "Kind is what merchants sell when the ledger stays honest for a single night. Enjoy the lie. It's cheaper than virtue." is excellent in register.
- Minor: L33 "Now keep up, To-chan." - see catchphrase note above; consider a unique sign-off here since this is the romantic apex.

---

### `case3_investigation.rpy`

#### [PLOT]
- **Investigation is one beat, then immediately the setpiece.** A single clue menu (L128-160) leads straight into the collapsing-shelf climax (L161-168). The case is solved offscreen "by afternoon" (L279-280). The header openly calls this a "vertical slice," so this is by design, but the mystery has no actual deduction step - the trap is sprung the instant one clue is examined.
- **Dead clue with no payoff: `case3_clue_clerk`.** The milestone only rewards `case3_clue_bolt` (L285-289) and `case3_clue_shelf` (L290-294). If the player picks "Lean on the clerk" (L139, sets `case3_clue_clerk`), neither milestone block fires and the clerk's second ledger is never paid off. Add a `case3_clue_clerk` branch at the milestone or fold its content in.
- **Peril-binary repeat #2.** L181-188: "Trust Kaoru. Scream for him." -> rescue; "Dodge it alone." -> injury bad end. Same structure as Case 2's "go in alone" game-over and Case 4's swordfight. See structural note in handoff.
- **The "fresh-cut brace" is spotted before the clue menu (L110), which deflates the shelf clue.** Toa already announces "why is the brace on that shelf fresh-cut?" at L110, so choosing "Look closer at the shelf brace" (L150) as a discovery is redundant - she has already discovered it. Either remove the L110 tell or make the shelf clue about *who* cut it rather than *that* it was cut.

#### [CHARACTER]
- **Kaoru's rescue confession is the emotional core (L223 "If you had died in my bolt room, I would have burned this entire quarter down to the canal").** Strong. The problem is purely that Case 4 reuses it almost verbatim (L220 "burned this whole pier down to the canal") two scenes later, halving the impact of both. Differentiate one.
- **Toa is purely acted-upon in the climax.** Her only "good" option is to scream for him (L182); her self-rescue is lethal (L186-188). For a Kakita-trained dancer with established footwork, the canon path gives her zero successful physical agency. Consider one case where her training saves her (or someone else) cleanly.
- **"your hands are shaking" / "A draft, from the alley. Nerves." (L213-217)** is a lovely tell of his suppressed fear. It is then reused word-for-word in Case 4 (L213-214) - see Dialog/production note below.

#### [DIALOG]
- Strained metaphor, L159:

before:
> toa "This whole room is a trap wearing inventory for a costume."

after:
> toa "This isn't a storeroom. It's a deadfall someone stacked with silk."

- Recycled rescue line (differentiate from Case 4), L223:

before:
> kaoru "If you had died in my bolt room, I would have burned this entire quarter down to the canal."

after:
> kaoru "If that shelf had taken you, there would be no bolt room left. No quarter. Nothing but the canal and my apology to it."

---

### `case3_5_date_interlude.rpy`

#### [PLOT]
- **Explicitly spring - this is the anchor of the seasonal contradiction.** L68 "Spring's turning," L74 "the first heralds of spring: grape hyacinth ... cherry," L162/L193 spring kaiseki, L166 "fiddleheads." Case 4 happens the very next morning (L558 "The dock tomorrow"), and Case 4.5 (immediately after Case 4) is deep winter. Spring -> winter in roughly two in-story days is the single clearest continuity break in the slice.
- **Place name: "Tear Drop Island" (3 occurrences, L43/L82 + header) vs "Teardrop Island" in `case4_5_boat.rpy` (L17/L41/L112).** Standardize the spelling.
- **Branch convergence is robust.** The "ask outright" path (L454-512) and the late-ask path (L522-546) both set `is_this_a_date_asked` and converge at `case3_5_date_after_walk`/Act VII; the dance-lecture (L261) and skip (L301) both reach `case3_5_date_trust_overshare`. No dangling jumps. `is_this_a_date_asked` is declared `default` (stats.rpy L130), so the late-ask guard at L522 is safe.
- **Save-flag smell.** The interlude sets the legacy `case4_date_interlude_seen = True` (L17) as its "seen" marker rather than a `case3_5_seen` of its own. It works (eligibility reads the same legacy var), but it is a maintenance trap; document it (the header does, L4).

#### [CHARACTER]
- **Best characterization in the slice for both leads.** Toa's dancer's-eye read of the troupe (L285) is excellent, specific, and shows her expertise as agency rather than yearning. Keep this as the model for giving her competence elsewhere.
- **The "is this a date" exchange escalates then retreats - but here the retreat is earned and well-built (L495-507).** The two-beat "...No." / "It is the closest I come to calling this courtship, before I learn better." / "Forget the second sentence" is the most precise version of his advance/retreat. Because it is the best version, let the earlier (festival) and later (Case 4) versions be smaller so this one peaks.
- **Anachronistic sprite tag: `toa date twitterpated` (L179, L437).** Not player-facing text (it is an expression name), so low priority, but "twitterpated" is a 20th-century English coinage and jars with the register if it ever surfaces in tooling or gallery labels.

#### [DIALOG]
- Honorific formatting is inconsistent within this one file: "Toa san" (L116, space), "Doji Sango san" (L354/L358, space), "Hiromi-san" (L354, hyphen), "To-chan" (hyphen). Standardize to one convention (recommend hyphenated "Toa-san," "Sango-san").
- Mild kaiseki anachronism: "Asparagus" (L162). Cultivated asparagus is a late import to Japanese cuisine; in a period kaiseki it stands out among otherwise well-chosen spring ingredients (fiddleheads, fukinoto-style greens, preserved cherry). Consider swapping for udo or warabi.
- Tighten the deflection, L220:

before:
> kaoru "I call it compensation for bolt-room competence. Do not have the quarter filing poetry about us before dessert arrives."

after:
> kaoru "I call it payment for bolt-room competence. Do not let the quarter file poetry about us before the dessert is even cleared."

---

### `case4_investigation.rpy`

#### [PLOT]
- **L5R register: the "sixteenth-petal" Chrysanthemum forgery may be the Imperial mon (L99).** The sixteen-petal chrysanthemum is the Emperor's crest; a merchant cabal forging it is lese-majeste/treason, not a charter-and-tax scam. Either rename the mon to a non-Imperial flower or have the characters register that the stakes just jumped to Imperial-crime level. Also grammatically "sixteenth-petal" should be "sixteen-petal."
- **Recycled voice files against changed text (production bug).** Case 4 reuses Case 3's audio with altered lines:
  - L213 `kaoru "Draft in the alley. Nerves. Stand."` uses `kaoru_295.mp3`, but that file voices Case 3's "**A draft, from the alley.** Nerves. Stand." (case3 L216-217). Text and audio will not match.
  - L235-236 `kaoru "Good. Devotion belongs on paper until I say otherwise."` uses `kaoru_298.mp3`, which voices Case 3's "Devotion **stays** on paper until I say otherwise." (case3 L238-239).
  - L216 reuses `narrator_257.mp3` and L223 reuses `toa_257.mp3` from Case 3. Either restore identical text or assign new voice IDs.
- **Peril-binary repeat #3.** L181-187: "Stay behind me" -> Kaoru defends; "I will cut him down myself" -> death bad end. Third consecutive case resolved by the same submit-or-die menu.
- **`case4_investigation_choice` (crate/watchman/stairs) barely pays off.** Its one consequence is whether Kaoru's challenge uses the named suspect or a generic line (L141-149 via `case4_suspect_named`), which is a nice touch - but the crate/stairs branches otherwise only move stats. Note for payoff balancing.
- **Bridge chain is correct.** `case4_post_case3_bridge` -> `case4_investigation_start` -> raid -> confrontation -> swordfight -> `case4_milestone_end` -> `case4_post_case4_bridge` -> boat/Case 5 (L300-309). `case4_kaoru_defended` is set (L191) and is required by boat eligibility; good.

#### [CHARACTER]
- **The defend beat is a near-clone of the Case 3 rescue beat.** Same choreography (he crosses her line, grip that will not loosen, "Forget I said it," "the only romance this file requires," "Devotion ... on paper"). L207-236 maps almost one-to-one onto case3 L209-239. Two consecutive case climaxes with the same emotional script reads as a template, not an escalation. This is the highest-impact characterization fix in the file: the Case 4 climax should move the relationship somewhere Case 3 did not.
- **Toa's protest is identical too:** L289 "I stayed because the file said witness. Not because..." echoes case3 L235 "I am not, that is not what." Give her a different reaction to being defended a second time (impatience? guilt that he keeps bleeding for her?).
- **Good small touch:** L67 "Magistrate-sama, I am not your decoration." is a real flash of Toa pushing back; it is immediately defused by his quip (L71), but the spark is welcome.

#### [DIALOG]
- Expository recap plus the Imperial-mon issue, L99:

before:
> toa "Grey wax. The sixteenth-petal forgery again. Case One's flower never drowned. It just moved into a warehouse."

after:
> toa "Grey wax, sixteen-petal seal. The same forger from Case One. Whoever he is, he didn't drown with that barge. He just changed warehouses."

- Recurring L5R color misuse (whole slice): "Scorpion grey" (here L48; also case2 L142/L198) and "grey wax" as the Scorpion tell. Scorpion colours are canonically red and black. Recommend "Scorpion red-and-black," "lacquer-black wax," or simply "unmarked grey wax (Scorpion work)" if the greyness is meant to signal *concealment* rather than clan livery.

---

### `case4_date_interlude.rpy`

#### [PLOT]
- **Confirmed: this is a stub/redirect, and it is dead code in the live flow.** The entire file is a compatibility alias (L3-4): `label case4_is_this_a_date_interlude: jump case3_5_is_this_a_date_interlude`. A repo-wide search finds the label name `case4_is_this_a_date_interlude` only in this file (no live `jump`/`call` targets it); the canon path reaches the date via `case3_post_case3_bridge -> case3_5_is_this_a_date_interlude` directly. It is harmless save-compat scaffolding. Recommendation: keep for save compatibility, or delete with a save-migration note - but no narrative content lives here.

#### [CHARACTER] / [DIALOG]
- None (no prose in file).

---

### `case4_5_boat.rpy`

#### [PLOT]
- **Explicitly winter, immediately after the spring date.** L17 "Winter Scorpion raids," L41 "winter ribs ... bay wind," L98 "it is so cold," L149 "winter pier." This is "Case Four's ink is barely dry" (L17), and Case 4 was "the dock tomorrow" after the spring date. The season cannot be winter. This is the downstream half of the seasonal contradiction - fixing requires picking one season for the whole 2/3/4 stretch (see handoff).
- **Internal contradiction about whether intimacy happens on the boat.** Narration strongly implies consummation in the kobune (L220-237: "the rhythm finally ends, they are a single knot of warmth and borrowed robes"), but then Kaoru's L279 line - "I am going to bend you over the side of that bath when we are behind my screen, **not the marina**" - frames the real act as still-to-come and explicitly *not* at the marina. Clarify: is the boat scene the consummation (then the bath line is round two and "not the marina" is confusing) or heavy petting/warming (then L220-237 over-implies)? Right now they conflict.
- **Peril-binary repeat #4, now inside a romance interlude.** L186-193: "Go limp and let the hull take you" -> survive; "Fight the throw" -> grave-injury bad end. The submit-or-be-injured menu has now fired in Cases 2, 3, 4, and 4.5. Using it for a *playful* beat (being thrown into a boat) right after she has been sobbing is the most tonally strained instance.
- **New threads dropped in passing, likely Case 5 seeds (confirm payoff):** L98 "that spooky nonsense in the wards" (first hint of anything supernatural in the slice) and L17 "Winter Scorpion raids ... lying about grain." Neither is set up earlier in the slice; flag both for Case 5 to honor or cut.
- **Eligibility is tightly gated (good).** Boat requires `all_romance_routes_complete()` + `case4_closed` + `case4_kaoru_defended` and excludes every bad-end flag (case_endings.rpy L86-96), so it can only fire on a clean canon defend route.

#### [CHARACTER]
- **This is the one place Toa breaks the yearning pattern, and it is the slice's best escalation (L141-153).** "I am not cargo to haul around on your bad night." / "Then ask. Do not order. Not when you need me." After three interludes of absorbing his retreats, she finally names the dynamic and demands reciprocity. Protect this beat; it should be the payoff the earlier aches were building toward.
- **Kaoru's L263 line risks flattening him and lands badly.** "Mostly I wonder why more women can't be like you. So willing to let a man like me bully them along." Generalizing approvingly about women being biddable reads less as in-character possessiveness and more as authorial endorsement of the dynamic; it also undercuts the specificity that makes their relationship work. Rewrite to keep the possessive register but make it about *her*, not women-in-general (see Dialog).
- **The throw undercuts the comfort.** She is crying about nearly losing him (L84-100), he reassures ("I'm fine, To-chan," L104), and then he physically throws her into the boat (L182). The whiplash from comfort to roughhousing-as-foreplay is jarring; consider letting the warmth land before the dominance reasserts.
- **Continuity of the recurring intimacy frame:** "implied, never filed, hunger without a ledger line" (L232) echoes the festival's "Implied, never filed, satisfaction with no ledger line" (case2_festival L159) almost verbatim. It is a nice motif; vary the wording so it reads as a refrain rather than a copy-paste.

#### [DIALOG]
- Off-voice generalization, L263:

before:
> kaoru "Mostly I wonder why more women can't be like you. So willing to let a man like me bully them along."

after:
> kaoru "I keep wondering what I did to deserve the one witness who lets a man like me bully her toward the warm side of the boat."

- Forced quip, L118:

before:
> kaoru "Are you going to stand there gawking, or come warm me up? It has been a bad day. You, To-chan, get to deal with it. Inventory does not heat itself."

after:
> kaoru "Stand there gawking or come warm me. It has been a bad day, To-chan, and you are the only fire on this pier."

- Tone of the bath line is fine for the register, but resolve the "not the marina" contradiction (see [PLOT]); if the boat scene is consummation, change L279 to read as continuation ("again, behind my screen, where the bay can't watch") rather than as if it has not happened.

---

## 3. Continuity handoff (CRITICAL)

### 3a. Flags / persistent vars / stats - SET and READ (this slice)
All vars below are declared `default` in `stats.rpy` (L79-143), so there are no undefined-variable risks in this slice.

Case 2 (`case2_investigation.rpy`):
- SETS: `case2_briefing_choice` route/politics/witnesses (L54/65/77); `case2_scene_choice` ash/body/runner (L110/122/135) - never read again; `case2_packet_found` (L119, force-set L167); `case2_courier_name`="Tsubaki" (L132, force-set L160); `case2_confront_choice` accuse/trap/defer (L191/205/217); `case2_milestone`="case2_closed" + `case2_closed=True` (L276-277).
- READS: `live_in_companion` (L32, L263); `kaoru_submission` (L224, `>=3` flavor).
- STAT WRITES: `insight` (+2/+1 across menus), `honor` (+1/+2), `composure` (+1/+2), `performance_boldness` (+1, L136), `kaoru_resistance` (+1, L193, accuse), `compliance` (+1, L218, defer), `kaoru_submission` (+1, L219, defer).

Case 2 festival (`case2_festival.rpy`):
- SETS: `case2_festival_seen=True` (L7); `case2_festival_kiss_only` (L91) OR `case2_festival_intimate` (L135).
- READS: routes to `case2_romance_morning` (sets `case2_romance_seen`, case_endings.rpy L294) then Case 3.

Case 3 (`case3_investigation.rpy`):
- SETS: `case3_started` (L10); `case3_briefing_choice` ledger/witness/scorpion_thread (L57/68/80); one of `case3_clue_bolt`/`case3_clue_clerk`/`case3_clue_shelf` (L130/140/151); `case3_accident_choice` trust_kaoru/dodge_alone (L183/187); `case3_accident_avoided`+`case3_kaoru_rescue` (L193-194) OR `case3_bad_end_injury` (L267); `case3_closed=True` (L303).
- READS: `live_in_companion` (L35); `case3_clue_bolt` (L285), `case3_clue_shelf` (L290) at milestone. **`case3_clue_clerk` is never read - dead clue.**
- STAT WRITES: `insight`, `composure`, `honor` across menus.

Case 3.5 date (`case3_5_date_interlude.rpy`):
- SETS: `case4_date_interlude_seen=True` (L17, legacy name = "Case 3.5 viewed"); `is_this_a_date_asked` (L455 or L528); outfit via `set_toa_outfit("date")` (L71) then `set_toa_outfit("work")` (L550).
- READS: `is_this_a_date_asked` (L522) to gate the late-ask menu.
- ENTRY GATE: `case3_5_date_interlude_eligible()` = `romance_through_case3_complete()` AND `not case4_date_interlude_seen`.

Case 4 (`case4_investigation.rpy`):
- SETS: `case4_started` (L37); `case4_investigation_choice` crate/watchman/stairs (L95/106/120); `case4_suspect_named`/`case4_suspect_name`="Kurogane" (L109-110 or L145-146); `case4_kaoru_defended=True` (L191) OR `case4_toa_slain=True` (L264); `case4_closed=True` (L299).
- READS: `live_in_companion and case3_kaoru_rescue` (L60); `case4_suspect_named` (L141); `case4_kaoru_defended` (L282).
- STAT WRITES: `insight` (+1), `composure` (+1), `honor` (+1), `compliance` (+1, L121), `kaoru_submission` (+1, L122).

Case 4 date alias (`case4_date_interlude.rpy`): no vars; dead redirect.

Case 4.5 boat (`case4_5_boat.rpy`):
- SETS: `case4_5_boat_interlude_seen=True` (L9); `case4_5_boat_choice` trust_warm/defy_cold (L122/127); `case4_5_boat_fall_choice` trust_fall/fight_fall (L188/192); `case4_5_boat_survived=True` (L198) OR `case4_5_bad_end_boat_injury=True` (L301).
- READS: none in-file beyond the menus; ENTRY GATE `case4_5_boat_interlude_eligible()` requires `all_romance_routes_complete()` + `case4_closed` + `case4_kaoru_defended` + no bad-end flags (case_endings.rpy L86-96).

### 3b. Central mystery per case + logic gaps
- **Case 2 - the burned Academy packet / murdered courier (Tsubaki).** Resolution chain: clerk -> warehouse foreman -> Plum/Chrysanthemum factor's cousin (escapes). Gaps: faction named both "Plum" and "Chrysanthemum" (case2 L245 vs L261); investigation choices don't change the outcome (force-set flags); only the "trap" branch surfaces the metaplot lead.
- **Case 3 - sabotaged bolt room / mislabeled Scorpion dye lot.** Resolution: clerk -> Chrysanthemum cousin's runner (offscreen, L280). Gaps: no real deduction step (one clue then setpiece); `case3_clue_clerk` has no milestone payoff; the shelf clue is pre-spoiled by Toa at L110.
- **Case 4 - dock raid on foreman Kurogane (Scorpion-trained).** Resolution: swordfight, foreman detained, ledger seized. Gaps: the "sixteen-petal"/Imperial-mon stakes problem (L99); investigation choice has minimal payoff beyond the named-suspect line.

### 3c. Threads OPENED vs CLOSED
- OPENED, still open at end of slice: "Case One's flower" (the Chrysanthemum/Scorpion factor) - "roots" explicitly remain (case4 L280); the factor's cousin escaped (case2 L245); the pleasure-quarter seal Kaoru predicts will be stolen "by morning" (case4 L285); "spooky nonsense in the wards" (boat L98); "Winter Scorpion raids ... grain" (boat L17); Tsubaki's memory (emotional thread, case2 L251).
- CLOSED within slice: each case "pinned, not closed" but locally resolved (suspects detained, ledgers seized); the festival kiss/date "is this a date" question is answered as far in as it goes pre-Case 5 ("the closest I come to calling this courtship, before I learn better").

### 3d. Toa/Kaoru relationship beats per interlude/boat (escalation ladder)
1. **Festival (case2_festival):** first kiss; optional first implied intimacy. Emotional note: she wants his nod "to mean more than patronage" (L120). He devalues the kiss afterward.
2. **Romance morning (case2_romance_morning, external):** soft domestic afterglow; sets `case2_romance_seen`.
3. **Tear Drop date (case3_5):** bought-out island, furisode, kaiseki; she nearly names her feeling and stops "until Case Five" (L332); the "is this a date" answer = "the closest I come to calling this courtship, before I learn better" then retracted.
4. **Dock defend (case4):** he takes the cut meant for her; "burned this whole pier down to the canal"; retracts again.
5. **Boat (case4_5):** the break in the pattern - she demands "ask, do not order" (L153); explicit comfort/intimacy; she says his full name "Kitsu Kaoru, the man" (L257). Highest point of mutual acknowledgment in the slice.

Escalation problem to hand off: beats 1, 3, 4 are the same shape (he advances, then retracts with "forget I said that"); only beat 5 escalates her agency. Case 5 should pay off beat 5, not reset to beat 1.

### 3e. State Case 5 / endings must honor
- `case4_kaoru_defended` is REQUIRED for the boat and for `all_romance_routes_complete()` (case_endings.rpy L71-78) and thus for `case5_romance_eligible()` and `epilogue_romance_bonus_eligible()` (L99, L101-111). The canon romance ending is hard-gated on the Case 4 "Stay behind me" choice.
- The romance chain is gated on `kaoru_submission >= 2` (via `canon_romance_eligible`, case_endings.rpy L27-32). Within this slice that point comes mainly from Case 2 "defer" (+1) and Case 4 "stairs" (+1); the rest must come from Case 1. **An assertively-played Toa can silently fall below the threshold and lose festival morning -> date -> boat -> romance ending.** Case 5/balancing should be aware this is a submission-gated romance.
- Bad-end flags that must keep the player out of romance extras: `case3_bad_end_injury`, `case4_toa_slain`, `case4_bad_end_abandoned` (deprecated supper arc, still checked), `case4_5_bad_end_boat_injury` (all referenced in case_endings.rpy L86-111).
- Open villain (Chrysanthemum/Scorpion factor + escaped cousin + predicted stolen pleasure-quarter seal) is the obvious Case 5 antagonist; honor the single chosen faction name.
- Accumulated stats (`insight`, `honor`, `composure`, `compliance`, `performance_boldness`, `kaoru_resistance`, `kaoru_submission`) are written all through this slice but only `kaoru_submission` is read in-slice; confirm Case 5/endings actually consume the others or document them as flavor-only.

### 3f. Consistency with earlier cases (Case 1) this slice assumes
- Case 1 closed with a Jiro murder + barge manifest + forged Crane seal, and a surviving "Chrysanthemum factor" whose barge "sank" - this slice repeatedly calls back to "Case One's flower" (case2 L74/L146/L261, case3 L26/L85, case4 L99). Keep the Case 1 villain's clan/family name aligned with whatever Case 2-4 settle on (currently muddled Plum vs Chrysanthemum).
- `live_in_companion` and `canon_first_scene` are set upstream (Case 1/prologue) and gate the festival and romance here; this slice assumes both can be true.
- `case3_kaoru_rescue` (set in Case 3) is read in Case 4 (L60) to vary Kaoru's line - Case 3's rescue outcome must persist into Case 4.

### 3g. `case4_date_interlude.rpy` status (explicitly requested)
Confirmed **stub/redirect and currently dead code.** Full contents are a 2-line compatibility alias (`case4_is_this_a_date_interlude` -> `case3_5_is_this_a_date_interlude`). No live label jumps to it; the canon flow reaches the date directly via `case3_post_case3_bridge`. Safe to retain for save compatibility or remove with a migration note; it holds no narrative content.

---

## 4. Highest-impact changes (this slice)

1. **Fix the spring -> winter seasonal contradiction across Cases 2-4.5.** The festival reads summer, Case 3.5 is explicitly spring, Case 4.5 is explicitly winter, yet the four are only days apart. Pick one season for the whole stretch (or insert real time-skips) - this is the most visible continuity break.
2. **Break the repeated peril-binary and the cloned rescue/defend climax.** "Trust Kaoru / go limp or be gravely hurt" fires in Cases 2, 3, 4, and 4.5, and the Case 3 rescue and Case 4 defend share near-verbatim dialogue. Re-shape at least one case (ideally Case 4) so the climax and the relationship move somewhere new, and give Toa one clean physical success.
3. **Settle the villain's faction name and the Imperial-mon stakes.** Choose "Chrysanthemum" or "Plum" and propagate (case2 L245 vs L261); decide whether the "sixteen-petal" seal is the Imperial chrysanthemum (if so, the stakes are treason and the characters should say so) and fix "sixteenth-petal" -> "sixteen-petal."
4. **Resolve the boat's internal contradiction and rewrite Kaoru's L263 line.** Clarify whether the kobune scene is consummation (then fix the "not the marina" bath line) and replace "why more women can't be like you ... let a man like me bully them along" with a her-specific line; also fix the recycled Case 3 voice files reused in Case 4 (kaoru_295/298, narrator_257, toa_257).
