# Main-Game Editorial Review, Part 1b: Setup (Entry / OP / Canon Encounter / Case Zero)

Editorial review only. No `.rpy` files were edited. Suggestions are proposals for the parent agent to accept or reject. Register kept feudal-Japan L5R (Rokugan / Ryoko Owari). Em dashes are avoided in all suggested rewrites, per `docs/style-no-em-dash.md`. The Modern AU is out of scope and ignored.

Files reviewed (in the order requested):
- `game/script.rpy` (entry / flow)
- `game/opening.rpy` (otome OP / title sequence)
- `game/prologue_canon_encounter.rpy` (canon first-night payoff: intimacy + signing)
- `game/kaoru_pro_prologue.rpy` (Case Zero, pre-Toa Kaoru pro-prologue)

Note on slice boundary: the wrong-door encounter itself (`prologue_start`) and the Case 1 bridge (`prologue_case1_hook`) live in `game/prologue.rpy`, which is out of this slice. Lines from `prologue.rpy`, `dev_chapter_pick.rpy`, `stats.rpy`, and `case_endings.rpy` are cited only where they define the routing boundary, the flag defaults, or the downstream consumers of state these four files set.

---

## 1. Slice summary

This slice is everything around the prologue's canon romance spine: the new-game flow (`script.rpy`), the 90-second otome OP montage (`opening.rpy`), the intimate "Unless?" payoff that signs Toa's permit and locks the canon route (`prologue_canon_encounter.rpy`), and the optional, default-off Case Zero that characterizes Kaoru before Toa ever knocks (`kaoru_pro_prologue.rpy`). The through-line is the canon-romance gate: the physical branch in `prologue.rpy` plus the encounter scene here set `canon_first_scene`, a forward-dated permit, and `kaoru_submission` to the threshold the whole romance route later checks. The biggest setup-level risks are a dev menu currently sitting in front of the canon entry path, a love-scene climax that never drops its banter armor, and a few Rokugan-register slips (a modern math idiom, digital clock timestamps).

---

## 2. Per-file sections

### 2.1 `game/script.rpy`

#### [PLOT]

- **P1. The dev chapter-pick gate is live, so the canonical first screen after the splash is a debug menu.** `dev_chapter_pick_enabled` is `True` (`dev_chapter_pick.rpy:17`), and `start` branches on it: `if dev_chapter_pick_enabled:` (line 20) shows `menu dev_start_gate_menu` with the on-screen banner `"Dev build, choose how to start."` (line 22). The in-file comment already flags this: `"Disable for release: dev_chapter_pick_enabled = False"` (line 19). As shipped, a player who presses Start sees a developer prompt before the OP. Highest-impact flow item in the slice: flip this to `False` (or gate on `config.developer`) for any canon/release build.
- **P2. Benign double-route worth a maintainer note.** The menu option `"Play from beginning..."` does `jump dev_play_normal_start` (lines 25 to 26), and there is also an unconditional `jump dev_play_normal_start` (line 31) after the menu block. Line 31 is only reachable when the gate is disabled; when it is enabled both menu options jump away (the other to `dev_chapter_pick_menu`, line 29). Not a bug, but line 31 looks like dead/duplicate code to anyone skimming, so a one-line comment ("fallthrough when gate disabled") would help.
- **P3. The game title is presented up to three times in the first two minutes.** Splash centered title `"Ryoko Owari Nights ... the city of lies"` (line 6), then the OP's own Yuji-Syuku title drop (`opening.rpy:259 to 261`), then a third centered title at line 44 immediately after the OP returns. The line-44 re-drop right behind the OP's title drop is redundant and softens both. Recommend cutting line 44 (or the splash card) so the title lands once and hard.
- **P4. Two commented gates sit inside the canon flow and one is mis-sequenced as written.** Lines 56 to 62 hold an optional Case Zero gate and an optional Modern AU gate, both off. Harmless while commented, but the Case Zero gate (`call kaoru_pro_prologue`, line 58) is positioned after Toa's street intro (lines 49 to 54). Case Zero is explicitly a pre-Toa pro-prologue, so enabling it here would play "before Toa exists" content after the player has already met Toa, and the `call` would never return (the label ends in `jump prologue_start`, see 2.4 P1). If Case Zero is ever promoted to canon, move the gate above the OP/street intro and use `jump`.

#### [CHARACTER]

- **C1. Toa's first spoken line in the entire game is pure attitude, no investigator.** `toa "Snacks first. Justice second. That's the order of operations."` (line 50) establishes her as flip and irreverent, but nothing here signals competence, curiosity, or the case ahead, which is the genre promise of a detective VN. The narration that immediately follows does the real work (the permit, the magistrate's hall, lines 52 to 54). Consider one line that fuses the quip with the mission so the heroine's first impression reads as sharp, not only glib.

#### [DIALOG]

- **D1. Line 50 (anachronism: "order of operations").** A modern arithmetic term. The prologue's twin line wisely avoids it (`prologue.rpy:877`: "Snacks first. Justice second. I can hold that order for three weeks.").
  - Before: `toa "Snacks first. Justice second. That's the order of operations."`
  - After: `toa "Snacks first. Justice second. That is the only order I keep."`
- **D2. Line 52 (tense slip).** Present-perfect "has slept" then past-perfect "had not expected" inside one sentence.
  - Before: `"The canals stink of copper and cheap incense. Toa has slept in worse places, but she had not expected Ryoko Owari to feel worse than the Unicorn roads."`
  - After: `"The canals stink of copper and cheap incense. Toa has slept in worse places, but she did not expect Ryoko Owari to smell worse than the Unicorn roads."`

---

### 2.2 `game/opening.rpy`

#### [PLOT]

- **P1. The OP sells romance only; the detective premise is absent.** The montage is almost entirely red-string/embrace/lantern romance (for example `op_embrace` at line 229, `op_pull` at line 232, the subtitle "A red string binds us together" at line 225). The investigation hook (a magistrate's hall, a permit, a body in the canal) appears only obliquely through `op_canal` (line 235) with no framing as a case. For an otome detective VN, one montage beat that reads clearly as "mystery" would set first-time players' genre expectation correctly.
- **P2. Title-drop redundancy with `script.rpy:44` (cross-ref 2.1 P3).** The OP ends on a strong title (lines 259 to 261) and then the caller immediately draws the title again. Pick one.
- **P3. Housekeeping: onset-comment drift and shipped authoring notes.** Line 188 `pause 6.72  # @ ~7.9` repeats the line-186 onset; per the header's measured onsets (Intro 7.9, 14.6) this beat should land near 14.6, so the trailing comment looks copy-pasted. The pauses themselves are fine, only the annotations future timing passes rely on are off. Also two leftover authoring notes ship in-file: `# alt: op_dance (office dance CG)` (line 243) and `# alt expansion: scene op_magistrate_qtr...` (line 250).

#### [CHARACTER]

- **C1. Toa's name card frames her as a dancer, not an investigator (first impression).** Her card reads `"a Crane dancer"` (line 198) while Kaoru's reads `"Emerald Magistrate"` (line 214). In a detective VN, defining the heroine's one-phrase intro as "dancer" undersells the investigator role the whole game runs on. The dance matters (she danced for ink in the prologue), but the card is her first framed impression. See D1 for a concrete swap.

#### [DIALOG]

- **D1. Line 198 (name-card framing).** Player-facing screen text.
  - Before: `op_namecard("Kakita Toa", "a Crane dancer", xa=0.06, ta=0.0)`
  - After: `op_namecard("Kakita Toa", "Crane dancer, sharper eyes", xa=0.06, ta=0.0)` (alt, if a cleaner genre signal is wanted: `"a Crane investigator"`).
- **Register note (no rewrite).** No stilted player-facing dialog exists here; the lyric subtitles are clean translation lines and contain no em dashes. The only en dashes in the file are in code comments (line 15 "44.9–49.7", line 18 "80–90 s") and the " , " comma-with-double-space artifacts of the em-dash sweep also appear only in comments (for example lines 24, 166). All cosmetic, flagged for the project-wide sweep but not player-visible.

---

### 2.3 `game/prologue_canon_encounter.rpy`

#### [PLOT]

- **P1. One beat is named three different ways.** File `prologue_canon_encounter.rpy`, label `prologue_canon_ending` (line 3), flag `canon_first_scene` (line 113). "Encounter" vs "ending" vs "first scene" all name the same moment, and it is neither the first encounter (that is the wrong door in `prologue_start`) nor an ending (it bridges into Case 1). Low logic risk, real maintenance risk. Settle on one term.
- **P2. Entry depends on un-shown prologue state, but the handoff is tight and correct (protect it).** This file is reached only from `prologue.rpy:808 jump prologue_canon_ending`, inside the physical "Unless?" branch (`prologue.rpy:796 to 808`), which sets `physical_initiative += 2`, `compliance += 1`, `kaoru_submission += 1` and shows CG `canon_proposition`. The opening line `kaoru "Chair wasn't enough. Good. Come here."` (line 12) pays off "She straddles the chair's arm" (`prologue.rpy:802`), and `toa "You asked unless. I answered with my body."` (line 16) pays off Kaoru's "Unless you mean to finish what you started." (`prologue.rpy:805`). Good cross-boundary continuity; later edits to the prologue branch must keep these callbacks valid.
- **P3. Date logic is consistent but the absolute anchor is implicit.** `permit_effective_days = 3` (line 114), narration "His hand wrote three days hence" (line 126), and `kaoru "...Return on the thirtieth."` (line 132). Downstream `prologue_case1_hook` prints "Three days later..." (`prologue.rpy:1100`) and Case 1 treats the permit as dated to the thirtieth. Everything reconciles only if tonight is the 27th, which is never stated. Optional: have Kaoru or the narration name the current date once so "three days" and "the thirtieth" visibly agree.
- **P4. Missed setup/payoff with Case Zero's "almost-smile."** Case Zero builds Kaoru's defining motif, the smile he always denies (`kaoru_pro_prologue.rpy:101, 112 to 131, 359`). This intimate canon scene is the natural place for that smile to finally go undenied, but it is never referenced; Kaoru stays in `hungry`/`charm`/`satisfied` sprites throughout. Because Case Zero is off by default the payoff cannot be relied on for most players, but even standalone the scene would deepen if the mask cracked once here. (Cross-ref 2.4 C1 and C1 below.)
- **P5. The flags set here are the canon-romance gate for the whole game.** Lines 112 to 115 set `permit_signed = True`, `canon_first_scene = True`, `permit_effective_days = 3`, `kaoru_submission += 2`. `case_endings.rpy:29 to 31` requires `canon_first_scene` and `live_in_companion` and `kaoru_submission >= 2`; this scene alone clears the submission threshold (entering at 1 from the prologue physical branch, leaving at 3 or more). Critical state; see section 3.

#### [CHARACTER]

- **C1. Both leads keep their witty armor through the entire intimate scene; the romantic climax has no unguarded beat.** Samples: `toa "Sign later. Touch now."` (line 40), `toa "I undress men who watch too long. You watched longest."` (line 58), `kaoru "Bold for someone who knocked on the wrong door."` (line 43). It is on-voice banter, but a canon love scene where neither character is ever sincere reads emotionally one-note. The single soft note, `toa "Magistrate-sama..."` (line 32), is immediately capped by Kaoru's quip (line 34). Let the performance drop for one exchange.
- **C2. Kaoru stays transactional even in afterglow.** `kaoru "Bring obedience. The rest is negotiable."` (line 138), `kaoru "Effective when I say."` (line 132). Consistent with Case Zero, but with zero counter-beat his "love interest" register is indistinguishable from his "magistrate" register. One line of plain wanting, not ledger-coded, would sell the pairing.

#### [DIALOG]

- **D1. Line 28 (em-dash-removal artifact).** The bare appositive "not restraint, invitation" reads as a comma splice; an em dash was likely stripped here.
  - Before: `"His hand finds her wrist, not restraint, invitation. He draws her off the chair and into the space between desk and lantern."`
  - After: `"His hand finds her wrist. Not to restrain her, to invite. He draws her off the chair, into the space between desk and lantern."`
- **D2. Line 61 (precious parallelism mid-action).** The abstract "hers the offering, his the permission" stalls a physical beat.
  - Before: `"Maroon silk slips from one shoulder. Her obi loosens; his hakama stays untouched, hers the offering, his the permission."`
  - After: `"Maroon silk slips from one shoulder. Her obi loosens; his hakama stays untouched. She offers; he allows."`
- **D3. Line 138 (on-the-nose dominance button).** Optional softening that keeps the power note but reads more period-courtly than kink-cliche.
  - Before: `kaoru "Bring obedience. The rest is negotiable."`
  - After: `kaoru "Bring yourself, on time. We will negotiate the rest across my desk."`

---

### 2.4 `game/kaoru_pro_prologue.rpy`

#### [PLOT]

- **P1. Call-vs-jump and sequencing of the optional gate.** The label exits with `jump prologue_start` (line 378), so the `script.rpy` gate's `call kaoru_pro_prologue from _call_kaoru_case_zero` (`script.rpy:58`, commented) would never return; and as positioned it would run after Toa's street intro even though Case Zero is explicitly pre-Toa (header line 1) and itself ends on Toa's arrival (lines 346 to 365). It is currently reachable only via `dev_chapter_pick_menu` (`dev_chapter_pick.rpy:87`), so this is latent, not live. If Case Zero is ever promoted to canon: use `jump`, and place the gate before the OP/street intro.
- **P2. Case Zero's two menus have no downstream payoff.** `case_zero_smile_choice` (work/rain, lines 141/146), `case_zero_puppet_choice` (watch/cite, lines 242/247), and `seen_case_zero` (line 18) are set but read nowhere outside this file (confirmed by search). For a characterization pro-prologue that is acceptable as pure flavor, but if any later beat is meant to acknowledge "you saw Case Zero" or which choices you made, the wiring is missing. Decide flavor-only (and document it) or pay them off later.
- **P3. The "sealed docket" frame opens but is never closed.** The scene opens as a redacted file the player is reading: "SUMMARY ONLY. Witness names redacted per magistrate seal." (line 29), "No numbered case file after closure." (line 32), witnesses A to D with blacked-out names (lines 38 to 47). Strong device, but once live scenes begin (line 55) the docket frame is dropped and never reprised; the close is just "Case Zero filed." (line 376). A one-line return to the docket frame at the end would bookend it.
- **P4. Convergence is clean (note for handoff).** Both Case Zero and the normal flow end at `prologue_start` (line 378), so seen and unseen players rejoin the same wrong-door scene with no divergent state beyond the cosmetic flags in P2.

#### [CHARACTER]

- **C1. This file is the strongest characterization in the slice; protect it.** The "almost-smile... Denied" litany (lines 106 to 134) and the runner-POV section (lines 153 to 201) build Kaoru as controlled, ledger-minded, and quietly starved without ever stating it flatly. This is exactly the interiority the canon encounter (2.3 C1/P4) fails to pay off.
- **C2. Risk of monotony.** Across roughly 360 lines Kaoru holds essentially one register (cold/transactional) with a single sanctioned flicker, "He almost smiled at that." (line 101). It works here because the runner-POV externalizes him, but any reuse of this voice elsewhere needs a counter-beat.
- **C3. The ending over-foreshadows Toa.** The last page telegraphs her hard: "When the dancer arrives with tea she will learn the same arithmetic." (line 95), "some Crane gets lost in my hall." (line 330), "She will knock wrong first. They always do." (line 356), "Too Crane." (line 359). Three or four of these in two minutes is over-egged; keep the best one or two.

#### [DIALOG]

- **D1. Lines 41, 163, 184, 190 (anachronism: digital clock).** Western 24-hour timestamps in feudal Rokugan, which tells time by temporal hours and temple bells (Hour of the Tiger, Hour of the Hare).
  - Before: `"Witness B ████████ (runner, age twelve): delivered summons 04:17, 04:22, 04:31. Subject signed without looking up."`
  - After: `"Witness B ████████ (runner, age twelve): delivered three summonses across the Hour of the Tiger, each a few breaths apart. Subject signed without looking up."`
  - Before: `"04:17. Summons packet, third copy, wax still warm from the night clerk. Magistrate wing, inner screen, do not knock like a petitioner who wants theater."`
  - After: `"First bell of the Tiger. Summons packet, third copy, wax still warm from the night clerk. Magistrate wing, inner screen, do not knock like a petitioner who wants theater."`
- **D2. Modern bureaucratic/accounting diction (period-swap a couple).** The ledger-voice is a deliberate, good motif, but at this density several terms read corporate rather than Rokugan: "Incident class: administrative." (line 32), "interclan renewal spike" (lines 35, 88), "fee schedule" (line 128), "a line item I do not owe" (line 148).
  - Before: `kaoru "Watching is free. Smiling costs a line item I do not owe."`
  - After: `kaoru "Watching is free. Smiling is a debt I have not agreed to owe."`
  - Before: `"Incident class: administrative. No body. No numbered case file after closure."`
  - After: `"Matter: administrative. No body. No numbered case file after closure."`
- **D3. Verbal tic (no rewrite).** "wrong-green" for the canal recurs (lines 88, 264). Evocative once, a tic twice; vary one.

---

## 3. Continuity handoff (CRITICAL)

### 3.1 Canonical play order (as defined in `script.rpy`)

1. `splashscreen` (`script.rpy:3 to 8`), auto splash, centered title "Ryoko Owari Nights / the city of lies."
2. `start` (line 10): `stop music`, then `if dev_chapter_pick_enabled` (True by default) shows `dev_start_gate_menu` (line 24); option "Play from beginning" jumps to step 3, option "Dev chapter pick" jumps to `dev_chapter_pick_menu` (out of canon). When the gate is disabled, falls through to step 3 (line 31).
3. `dev_play_normal_start` (line 35), the real new-game entry (target of both the menu option and the disabled-gate fallthrough).
4. `call opening_sequence` (line 39 to `opening.rpy:170`): the 90s OP montage; cleans up and returns.
5. Back in `dev_play_normal_start` (lines 41 to 54): black, centered title (line 44), `scene bg street_exterior` + Toa's "Snacks first. Justice second." intro (line 50), canal narration.
6. Optional gates (commented, off): Case Zero (lines 56 to 58), Modern AU (lines 60 to 62).
7. `jump prologue_start` (line 64 to `prologue.rpy:6`) [out of slice]: wrong-door encounter, audition/dance-for-ink, the chair, the "Unless?" menu (`prologue.rpy:783`), which branches:
   - physical -> `jump prologue_canon_ending` (`prologue.rpy:808`, into the file reviewed in 2.3);
   - verbal -> `prologue_verbal_ending` -> `jump prologue_case1_hook` (non-canon);
   - walk_out -> `prologue_walkout_ending`.
8. Canon: `prologue_canon_ending` (encounter file line 3) -> `prologue_canon_tame` (line 22) -> `prologue_canon_signing` (line 91) -> `jump prologue_case1_hook` (line 146 to `prologue.rpy:1092`).
9. `prologue_case1_hook` (`prologue.rpy:1092`): if `canon_first_scene` -> "Three days later..." -> `case1_companion_offer`; else -> "Three weeks later..." -> `case1_noncanon_start` [out of slice].

Entry points and orphan check:
- Real entry is Ren'Py `start`; `splashscreen` is automatic.
- `opening_sequence` has a second entry (a "Replay Opening" button, `screens.rpy:350 to 355`, via `renpy.call_in_new_context`), so it is not orphaned.
- `kaoru_pro_prologue` (Case Zero) is NOT in the canon order; it is reachable only from `dev_chapter_pick_menu` (`dev_chapter_pick.rpy:87`) or the commented gate, and exits to `prologue_start`. Canon-orphaned by default, intentionally.
- `prologue_canon_tame` and `prologue_canon_signing` are reached only by fallthrough/jump from `prologue_canon_ending`; fine.
- Only "double target" is `dev_play_normal_start` (menu option + fallthrough), benign (see 2.1 P2). Nothing harmful is double-routed.

### 3.2 Flags / persistent vars / stats SET in this slice

- `script.rpy`: no story flags set (only `stop music`). Reads `dev_chapter_pick_enabled`.
- `opening.rpy`: only the subtitle/name-card counters `_op_sub_n` / `_op_card_n` (defaults line 130 to 131; bumped in `op_sub`/`op_namecard`). No story flags.
- `prologue_canon_encounter.rpy`: `permit_signed = True` (line 112); `canon_first_scene = True` (line 113); `permit_effective_days = 3` (line 114); `kaoru_submission += 2` (line 115).
- `kaoru_pro_prologue.rpy`: `seen_case_zero = True` (line 18; default False line 12); `case_zero_smile_choice` = `work` | `rain` (lines 141/146; default "" line 13); `case_zero_puppet_choice` = `watch` | `cite` (lines 242/247; default "" line 14).

### 3.3 Flags / vars READ in this slice (and defaults defined out of slice)

- Read in slice: `dev_chapter_pick_enabled` (`script.rpy:20`). The encounter file only sets, never reads. Case Zero's menus set their choice vars but never branch on them.
- Defaults / dependencies defined out of slice: `kaoru_submission = 0` (`stats.rpy:7`), `permit_signed = False` (`stats.rpy:32`), `permit_effective_days = 0` (`stats.rpy:33`), `canon_first_scene = False` (`stats.rpy:34`), `dev_chapter_pick_enabled = True` (`dev_chapter_pick.rpy:17`). `show_cg_scene` is a helper defined out of slice.

### 3.4 Candidate dead / unread-in-slice flags (verify downstream or document)

- `seen_case_zero`, `case_zero_smile_choice`, `case_zero_puppet_choice`: set in Case Zero, read nowhere in the project per search. Either flavor-only (document) or pay off later (2.4 P2).

### 3.5 Downstream consumers later content must honor (confirmed by search)

- `case_endings.rpy:29 to 31, 45`: canon romance requires `canon_first_scene` and `live_in_companion` and `kaoru_submission >= 2`. This slice's encounter supplies `canon_first_scene` and pushes `kaoru_submission` to 3 or more.
- `case1_companion.rpy:209`: `if canon_first_scene and physical_initiative >= 1` (the physical branch supplies `physical_initiative += 2`); lines 291 to 294 re-assert `permit_signed` and clamp `permit_effective_days >= 3`.
- `prologue.rpy:1099`: `if canon_first_scene` (the 3-days vs 3-weeks split).
- `case2_festival.rpy:3`: eligibility `canon_first_scene + live_in_companion`.
- `kaoru_submission` is incremented across prologue and cases (`prologue.rpy` 75/135/173/347/800; `case1_investigation.rpy` 617/769/901/1132; `case2_investigation.rpy` 219; `case4_investigation.rpy` 122) and tested (`case1` 907/972 at `>= 2`; `case2` 224 at `>= 3`).
- `dev_chapter_pick.rpy:22 to 33` emulates this canon state for jump-in testing (`canon_first_scene = True`, `permit_signed = True`, `permit_effective_days = 3`, `kaoru_submission = 3`); keep it in sync if the encounter's deltas change.

### 3.6 Threads OPENED

- Canon route locked: live-in/residency promised, with a "Return on the thirtieth ... discuss your residency" appointment (encounter lines 132, 144) and a "Guest room preview" line (line 141) seeding the `live_in_companion` arc.
- Case Zero (only if seen): the "patronage appetite / spendable witness / proprietary corridor" worldview (lines 53, 137), "renewal season / wrong door season" (lines 333, 365), the spendable-witness bad-end logic (lines 268 to 313), and the puppeteer's "wrong motive: debt, not passion" (line 220) seed the season's mercenary-motive theme.

### 3.7 Toa / Kaoru relationship beats

- Encounter: first physical intimacy (fade-to-black), forward-dated permit signed, `kaoru_submission` pushed past the romance threshold, and Kaoru's "Bring obedience" / "I'll leave it unlatched" promise (lines 138, 144). The power-exchange register is established as the couple's baseline.
- Case Zero: pre-relationship; Kaoru's denied-smile/appetite established; ends on Toa's footsteps approaching (lines 346 to 365). No Toa dialogue (correct for pre-Toa).

### 3.8 State later content must honor

- `canon_first_scene = True` defines the canon route; do not contradict it.
- Permit is dated to "the thirtieth" with a +3-day effective window; the canon Case 1 bridge opens "Three days later" (`prologue.rpy:1100`). Keep all three references aligned.
- `kaoru_submission >= 2` is guaranteed after the encounter (3 or more via the physical branch).
- "Snacks first. Justice second." is Toa's catchphrase (also `prologue.rpy:877`); keep it consistent (and drop the "order of operations" tag if 2.1 D1 is accepted).
- If Case Zero is ever promoted to canon, honor `seen_case_zero` and the two choice flags or explicitly leave them as flavor (2.4 P2).

### 3.9 Minor / housekeeping

- Em dashes: zero in player-facing text across all four files (verified by search). Two en dashes exist only in `opening.rpy` comments (lines 15, 18); em-dash-sweep " , " comma artifacts also appear only in comments (for example `opening.rpy:24, 166`) and as the bare appositive at encounter line 28 (see 2.3 D1).
- Naming drift "encounter / ending / first scene" for one beat (2.3 P1).
- Shipped authoring notes and a drifted onset comment in `opening.rpy` (lines 188, 243, 250).
