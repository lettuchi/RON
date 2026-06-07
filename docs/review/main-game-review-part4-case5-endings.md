# Main-Game Editorial Review, Part 4: Case 5 Finale + All Endings/Epilogues

Editorial review only. No `.rpy` files were edited. Suggestions are proposals for the parent agent to accept or reject. Register kept feudal-Japan L5R (Rokugan / Ryoko Owari). Em dashes are avoided in all suggested rewrites, per `docs/style-no-em-dash.md`.

Files reviewed (in order):
- `game/case5_investigation.rpy`
- `game/case_endings.rpy`
- `game/epilogue_romance_bonus.rpy`
- `game/epilogue_rain_gameover.rpy`
- `game/ed_sequence.rpy`

---

## 1. Slice summary

This slice is the game's resolution layer: the Case 5 "Left Hand" finale (a public hearing where Toa is sworn as Kaoru's yoriki), every good/bad ending and game-over for Cases 1 through 5, the romance bonus kotatsu epilogue, the prologue rain/brothel bad end, and the golden-hour ED credits montage. The dominant structural fact is that Case 5 is a relationship-and-appointment payoff rather than a detective case: the criminal throughline (the "Chrysanthemum root") is named as backdrop and deliberately left open, while the emotional arc (provisional companion to sworn left hand) is what actually resolves. The biggest coherence risk in the slice is that declining a *job offer* routes to brutal trafficking/coercion bad ends, which clashes hard with the otherwise tender canon characterization of Kaoru established in the same scene and in the ED.

---

## 2. Per-file sections

### 2.1 `game/case5_investigation.rpy`

#### [PLOT]

- **P1. The "investigation" finale contains no investigation, and the central criminal mystery is deferred, not resolved.** Case 5 is presented as a case (`case5_investigation_start`, line 9) and the hearing docket is "witness chains for the Chrysanthemum root, and appointment of sworn yoriki" (line 130), but no clue, suspect, or deduction occurs on-screen. The finale explicitly closes the *relationship* while leaving the *crime* open: "Case Five is pinned, not closed. The city still lies." (line 315) and "The Chrysanthemum root still has tendrils in the pleasure quarter." (line 307). If Cases 1 to 4 set up the Chrysanthemum/Scorpion root as the season's spine, a reader expecting the spine to pay off will feel the finale dodges it. Decide deliberately: either (a) frame Case 5 in-text as a *deliberate* "the city never lets you close the big file" thesis (currently only half-stated), or (b) add one concrete investigative beat so the title earns the word.
- **P2. The entire main-game finale is gated behind full romance completion.** `case5_investigation_start` jumps to `case5_noncanon_discharge` unless `all_romance_routes_complete()` (lines 14 to 15). A player who solved the cases but did not complete the romance gets only the ~10-line discharge stub (lines 328 to 348), with no finale and no criminal-plot resolution at all. This makes the detective layer narratively unfinishable without the romance. Flag for design intent: is a "career-only / no-romance" finish supposed to exist? Right now it does not.
- **P3. The fake dismissal is a coherent Kaoru manipulation but is thinly motivated against the established intimacy.** In `case5_false_exit` Toa packs a travel kosode believing patronage has "run out" (line 54) and is told to "Leave the adjoining chamber key at the gate" (line 58); `case5_audition_callback` then reveals it was a staged test (lines 83 to 109). The reveal lands, but by Case 5 they are a fully bonded live-in couple, so letting her believe she is being discharged reads as needless cruelty rather than necessary discretion. A single line acknowledging *why* the public theater required keeping her in the dark would close the logic gap.
- **P4. The cases are retroactively reframed as a hidden audition.** Lines 83 to 101 recast Cases 1 to 4 as tests Kaoru set ("I said provisional attachment until the files close ... The files did not close themselves"). This is charming but borders on retcon, since those cases played as live investigations with real stakes, not staged trials. The Case 4 line is correctly gated on `case4_kaoru_defended` (line 91), which is good continuity, but the framing should be softened to "what each case revealed about you" rather than "what I was testing," to avoid implying the murders were a recruitment exercise.
- **P5. Refusing the appointment is the only non-acceptance branch, and it routes straight to brutal endings.** The `case5_yoriki_menu` (lines 175 to 182) offers exactly Accept or Refuse, and Refuse jumps to `case5_bad_end_refusal_warning` (line 182), which leads only to `gameover_case5_chained` or `gameover_case5_quarter_cage`. There is no graceful decline. A protagonist saying "I will keep serving as a witness but not sign as your sworn officer" has no path that is not trafficking or a cage. See C2 for why this is also a characterization problem.

#### [CHARACTER]

- **C1. Toa's arc lands; her thesis is clear but stated too bluntly.** Her through-line (dancer wanting a permit, to officer wanting to *stand beside* rather than be *kept*) pays off well, especially line 238 "I needed the permit to stay close, but I chose to stay on purpose." The capstone line 254, "In the bedroom I can be your toy. Out there, I want to stand beside you," is the right idea delivered as an on-the-nose mission statement (see D-rewrites).
- **C2. Canon-Kaoru and refusal-Kaoru are not the same man.** In the accept branch Kaoru is possessive but protective: "His hand covers the yoriki seal on the inner desk ... as if the oath were a body he could keep off the public tray" (lines 222 to 223), and "I chose yours before you knew what the job was called" (line 109). In the refuse branch the identical man, in the identical scene, sells her to a pleasure-quarter back room or cages her for "corrective custody" because she declined a *post* (lines 402 to 435). Dark-romance register can justify a controlling Kaoru, but escalating from "I love you and chose you" to "I will have you trafficked for saying no to a job" in the span of one menu is the slice's sharpest characterization break. Recommend either (a) a softer refusal end (estrangement / discharge / exile, like `gameover_case4_abandon`) or (b) seeding earlier that the *city*, not Kaoru personally, collects the unsigned left hand, so the coercion reads as institutional rather than as the love interest's whim.
- **C3. "To-chan" usage is consistent** (line 101) with its use elsewhere (e.g., `case1_punishment_bridge`), so the intimacy register is continuous. Good.
- **C4. The bad-end Toa stays in character.** Her pride-then-panic ("I am Kakita Toa of the Crane. I will not be inventory on a public desk," line 366) is consistent with the prologue/rain Toa, so the *protagonist* side of the bad ends is coherent; the problem in C2 is the *antagonist-coded* Kaoru, not her.

#### [DIALOG]

- **D1. Line 134 (anachronism / L5R register).** "Yoriki is **police** rank. That is not the same as a dancer's permit." "Police" is out-of-register for Rokugan.
  - Before: `toa "Yoriki is police rank. That is not the same as a dancer's permit."`
  - After: `toa "Yoriki is a sworn magistrate's rank. That is not the same as a dancer's permit."`
- **D2. Line 250 (crude tonal break in a romance beat).** "Most people try to rename me. You **lay on your back** and still came back to my corridor." The blunt phrasing undercuts the tenderness of the private confession.
  - Before: `kaoru "Most people try to rename me. You lay on your back and still came back to my corridor."`
  - After: `kaoru "Most people try to rename me. You let me keep you, and still walked back to my corridor on your own feet."`
- **D3. Line 254 (on-the-nose thesis).**
  - Before: `toa "In the bedroom I can be your toy. Out there, I want to stand beside you."`
  - After: `toa "Behind your screen I can be yours to keep. In the hall I do not want to be carried in your file. I want to stand."`
- **D4. Line 204 (modern register "math").**
  - Before: `"The envoy exhales once, not a blessing, just math. The rival magistrate's colors leave before the wax cools."`
  - After: `"The envoy exhales once, not a blessing, only a tally of who gains. The rival magistrate's colors leave before the wax cools."`
- **D5. Line 303 (modern register "montage").**
  - Before: `"The first week as his sworn left hand is not a montage of victory. It is runners, copied seals, and a quarter walk where the okami nod at her sash instead of her obi."`
  - After: `"The first week as his sworn left hand is not a triumph procession. It is runners, copied seals, and a quarter walk where the okami nod at her sash instead of her obi."`
- **D6. Line 168 (clipped expository list).**
  - Before: `kaoru "You already served the desk. You slept behind my screen. You argued well when I wanted competence within reach."`
  - After: `kaoru "You have already served this desk. You slept behind my screen. You argued well every time I needed a sharp mind within reach."`
- **D7. Line 141 (telegraphed phrasing "The quarter whispers kept woman").**
  - Before: `kaoru "Witness is not enough in this city. You signed my corridor, my cushion, my release. The quarter whispers kept woman. The file will say office."`
  - After: `kaoru "Witness is not enough in this city. You signed my corridor, my cushion, my release. Let the quarter whisper kept woman. The file will say office."`

---

### 2.2 `game/case_endings.rpy`

(Contains the eligibility gate functions plus all Case 1, 2, 3, 4, 4.5, and 5 game-overs and the Case 1/2 romance interludes. Case 5 bad ends are the in-slice focus; earlier-case ends are noted for continuity only.)

#### [PLOT]

- **P6. The eligibility/gate functions are clean and consistent.** `all_romance_routes_complete()` (lines 71 to 78) correctly composes `romance_through_case3_complete()` plus the Case 4 conditions, and `epilogue_romance_bonus_eligible()` (lines 101 to 111) layers the Case 5 accept flags and excludes every injury/death flag. This is the strongest continuity machinery in the slice; no logic bug found. (See the handoff table in section 4 for the full read list.)
- **P7. Redundant flag set in the Case 5 chained end.** `seen_gameover_case5 = True` is set in `case5_bad_end_refusal_chained` (line 404) and again at the top of `gameover_case5_chained` (line 344). Harmless, but redundant; same pattern for the cage path (lines 422 and 407). Worth a one-line cleanup note for the owning agent.
- **P8. The Case 5 chained end relies on a "the city/quarter collects, not me" framing that is never set up earlier.** Lines 377 ("Tell me how the city collects"), 408, and 380 ("The quarter keeps what I sell") try to displace agency onto the city, but Kaoru is the one selling her, so the displacement does not hold. This is the textual seam behind C2; if you keep the brutal end, the "institution collects" idea must be planted before Case 5, not asserted at the moment of punishment.

#### [CHARACTER]

- **C5. Within the dark-romance opt-in frame, the *earlier-case* bad ends are internally consistent.** `gameover_case1_canal`, `gameover_case2_alley`, `gameover_case3_injury`, `gameover_case4_abandon`, `gameover_case4_slayn`, `gameover_case4_5_boat` all punish the same flaw (Toa's pride / going alone) and share the "Ryoko Owari keeps its books / boats, not its dancers" refrain (lines 783, 729). That refrain is a strong unifying motif. Good.
- **C6. The Case 1 punishment end (`case1_bad_end_kaoru_punishment`, lines 529 to 634) is a coherent dark-Kaoru, because it is reached by Toa explicitly demanding it** ("Then punish me, Magistrate-sama," `case1_punishment_bridge` line 477). That consent-to-provoke framing is exactly what the Case 5 refusal end lacks: in Case 5 she declines a job, she does not demand punishment, yet the outcome is comparably brutal. Use Case 1's opt-in structure as the model for fixing C2.
- **C7. Kaoru's romance-interlude voice (lines 141, 146, 216, 226) is consistent with his finale voice** (possessive, ledger-minded, "audience of one"). The characterization is continuous across the file; the only discontinuity is the refusal-end cruelty (C2).

#### [DIALOG]

- **D8. Line 546 (modern register "line item" + grammar).** "You are line item on my evening" is missing an article and uses a bookkeeping anachronism.
  - Before: `kaoru "You are line item on my evening until I say otherwise. Desk. Now."`
  - After: `kaoru "You are one line on my evening's ledger until I say otherwise. Desk. Now."`
- **D9. Line 700 (modern register "arithmetic").** Part of the deliberate math/ledger motif, so lower priority, but "dock arithmetic" reads modern.
  - Before: `"Kurogane's cut is dock arithmetic, not theater. Rain swallows the pier. The magistrate's file closes without her breath."`
  - After: `"Kurogane's cut is dock work, plain and final, not theater. Rain swallows the pier. The magistrate's file closes without her breath."`
- **D10. Code comment line 61 contains an en dash** ("Cases 1–3"), which violates the project's no-dash convention even in comments. Trivial, comment-only, but flag for consistency: write "Cases 1 to 3."

---

### 2.3 `game/epilogue_romance_bonus.rpy`

#### [PLOT]

- **P9. Clean, well-gated, coherent.** Entered only via `epilogue_romance_bonus_eligible()` after `case5_epilogue_week_one`, sets `case5_romance_bonus_seen = True` (line 7) to prevent replay, and exits cleanly to title or `renpy.full_restart()` (lines 80 to 87). No logic issues.
- **P10. Possible missing handoff to the ED.** This bonus epilogue is the *last* canon beat a fully-romanced player reaches, yet it ends at a "Return to title / Main menu" menu and never calls `ed_sequence`. If the golden-hour ED is meant to be the emotional capstone of the canon route, the canon route currently never plays it automatically (see 2.5 / P13). Confirm whether the ED is intentionally main-menu-only.

#### [CHARACTER]

- **C8. This is the best Kaoru characterization in the slice and the strongest argument against the refusal end.** The "almost-smile he will deny tomorrow" (line 72), "Eat your mikan" (line 46), and "Just this room is still mine to share when the city is not listening" (line 57) show a tender, domestic Kaoru. It is consistent with `charm`/`satisfied` Kaoru elsewhere, and it makes the trafficking refusal end feel like a different character entirely (reinforces C2).
- **C9. Toa is warm, teasing, settled.** "You may almost smile if you try" (line 29) and "I will file that under victories too small for the docket" (line 42) land her arc's resolution nicely.

#### [DIALOG]

- **D11. Line 49 (modern/bureaucratic anachronism "classified information").**
  - Before: `"She passes him a segment anyway. He takes it without looking, as if hunger were classified information and her fingers on the peel were a form he intended to sign later."`
  - After: `"She passes him a segment anyway. He takes it without looking, as if hunger were a secret he refused to file, and her fingers on the peel a form he meant to seal later."`
- **D12. Line 46 (unclear idiom "I still take delivery").**
  - Before: `kaoru "Drip on the yoriki sash and I will make you copy the stain description twice. I still take delivery."`
  - After: `kaoru "Drip on the yoriki sash and I will make you copy the stain into the record twice. I still take what I am owed."`

---

### 2.4 `game/epilogue_rain_gameover.rpy`

(This is the *prologue* refuse bad end, reached very early from `prologue_refuse_bad_end → "Leave the magistrate's office."` It is a bad end, not a finale, but it lives in this slice file.)

#### [PLOT]

- **P11. Coherent tragedy with a clear causal chain.** No seal/permit (line 90) leads to flight into the rain, ronin in the alley, implied brothel sale (`prologue_bad_end_brothel`). The logic is sound and the content warning + opt-out menu (lines 188 to 196) match the slice's other brutal ends.
- **P12. External CG dependency noted.** The comment at line 78 ("refuse-leave skips flee CG; corridor_lost already shown") assumes a `corridor_lost`/`gameover_rain_flee` beat was shown earlier in the prologue. Confirm that the prologue branch actually shows it, or the first rain CG the player sees is `gameover_rain_run` mid-flight without the doorway establishing shot. Cross-file dependency for the prologue owner to verify.

#### [CHARACTER]

- **C10. Strong, consistent Toa.** "She kept her pride ... Tonight it is the only thing she owns in Ryoko Owari" (line 99) and the gag callback "Snacks first. Pride second. I finally got the order right. / Pity there was never a third." (lines 103 to 107) make this the most emotionally earned bad end in the slice. Her arc-flaw (pride over survival) is the explicit cause of her fall, so the end is *earned* in a way the Case 5 refusal end is not.
- **C11. Kaoru's absence is correct.** The file comment notes "Kaoru is not present in the rain" (line 18); keeping him offstage preserves that this is Toa's choice and consequence, not his cruelty. This is exactly the structure the Case 5 refusal end should borrow.

#### [DIALOG]

- **D13. Line 186 (modern register "alley math").** Part of the math motif, but "alley math" is the most modern-sounding instance.
  - Before: `"She twists. Crane training was for stages and polite duels, not alley math. They have numbers. She has pride, and pride does not block three men."`
  - After: `"She twists. Crane training was for stages and polite duels, not alley brawls. They have the numbers. She has pride, and pride does not block three men."`
- **D14. Line 161 ("arithmetic") is acceptable as motif** but if D13 is taken, consider matching it: "pays coin for that bargain" reads cleaner than "pays coin for that arithmetic." Lower priority.

---

### 2.5 `game/ed_sequence.rpy`

(Otome ED credits montage, Kaoru-POV song "The Liar's String." Mostly image defs and lyric-synced timing; narrative content is the translated lyric subtitles.)

#### [PLOT]

- **P13. The ED is not wired into the canon ending path within this slice.** The header says it is "Callable from main menu" (line 24), and nothing in `case5_epilogue_week_one` or `epilogue_romance_bonus` calls `ed_sequence`. So as far as this slice shows, finishing the canon route does not roll the ED credits; the player only sees them from the menu. Either this is intentional (replayable gallery piece) or the canon good end is missing its capstone. High-value question for the parent agent to resolve.
- **P14. The ED's red-string-of-fate motif pays off the finale's themes well.** "the birdcage door, left open / and still you return, that foolishness of yours, / I will, surely, call it love" (lines 192 to 198) directly answers Toa's "I could have run. Then you could have caught me" (case5 line 238) and her returning "to my corridor" motif. Strong thematic closure for the canon route.

#### [CHARACTER]

- **C12. The ED humanizes Kaoru and is consistent with the bonus-epilogue Kaoru.** "each time I pressed the seal, my hand trembled" (line 224) and "I kiss your sleeping form / and tie the string once more" (lines 250 to 253) match the "almost-smile" softness, not the trafficking refusal-end Kaoru. The canon characterization is fully consistent across the bonus epilogue and the ED; only the bad-end Kaoru diverges (C2).

#### [DIALOG]

- **D15. Trailing " , " lyric artifacts read as typos.** Several subtitles end with a space-comma-space continuation marker: line 153 "those fingers that peel off my mask , ", line 177 and line 209 "I don't know how to give it back, but , ", and line 221 ends a line on a comma. These appear to be deliberate em-dash substitutes (good that they avoid em dashes), but on screen they look like stray punctuation.
  - Before: `$ ed_sub("those fingers that peel off my mask , ")`
  - After: `$ ed_sub("those fingers that peel off my mask...")`
  - Before: `$ ed_sub("I don't know how to give it back, but , ")`
  - After: `$ ed_sub("I don't know how to give it back, but...")`
  - (Apply the same ellipsis-for-trailing-comma fix to the other instances.)
- **D16. Otherwise the lyric subtitles are clean and in-voice.** "you barged in, shoes still on, foolish woman" (line 151) and "once the ink dries, even a lie becomes truth" (line 221) fit both Kaoru and the city's "City of Lies" identity. No further changes needed.

---

## 3. Branch & ending audit

Every reachable ending/epilogue/game-over found in the slice, its routing conditions, and whether the state that leads there is coherent and *earned*.

| # | Ending / beat | Label | Routed by | Coherent & earned? |
|---|---|---|---|---|
| 1 | **Canon "Left Hand" finale** (sworn yoriki, week one) | `case5_epilogue_week_one` | `case5_yoriki_accepted` via `case5_yoriki_menu` (line 176); converges from all accept sub-branches | **Yes.** Pays off the provisional-attachment setup. |
| 1a | Canon sub-branch: private inner-office confession | `case5_private_extra` | "Sign and follow him to the inner office tonight" (line 208) | Yes. |
| 1b | Canon sub-branch: bedroom intimacy | `case5_private_intimacy_fade` | "Come to the screen..." (line 262) | Yes. |
| 1c | Canon sub-branch: bow at threshold (no intimacy) | back to `case5_epilogue_week_one` | "Bow at the threshold..." (line 266) / "return to the witness chamber" (line 211) | Yes; clean boundary-respecting variant. |
| 2 | **Romance bonus epilogue** (kotatsu afternoon) | `epilogue_romance_bonus` | `epilogue_romance_bonus_eligible()` after #1 (case5 line 322) | **Yes.** Fully gated, no replay, warm payoff. |
| 3 | **ED credits montage** ("The Liar's String") | `ed_sequence` | Main-menu call only (line 24); **not** chained from #1/#2 in this slice | **Partly.** Content is earned/coherent, but **routing is questionable** (P13): canon route never auto-plays it. |
| 4 | **Non-canon discharge** (served, no left hand) | `case5_noncanon_discharge` | `not all_romance_routes_complete()` at finale entry (line 14) | **Coherent but thin** (P2): only finish for non-romance players; criminal plot unresolved. |
| 5 | **Bad end: refusal, sold to quarter** | `gameover_case5_chained` | Refuse (line 182) then "Let the pleasure quarter buy what I would not sign" (line 395) | **Coherent mechanically, NOT earned characterization-wise** (C2/P5/P8): declining a job should not yield trafficking. |
| 6 | **Bad end: refusal, corrective custody/cage** | `gameover_case5_quarter_cage` | Refuse (line 182) then "Keep me in magistrate custody..." (line 398) | **Same problem as #5.** Unearned escalation from love interest. |
| 6x | Refusal warning opt-out | returns to title | "Return to title" in `case5_refusal_warning_menu` (line 385) | N/A (safe exit, not an ending). |
| 7 | **Prologue rain bad end** -> brothel sale | `gameover_rain` -> `prologue_bad_end_brothel` | `prologue_refuse_bad_end → "Leave the magistrate's office"` (external) | **Yes, earned.** Toa's pride-over-survival flaw is the explicit cause. |
| 8 | Bad end: Case 1 canal (board barge alone) | `gameover_case1_canal` | External Case 1 choice; `seen_gameover_case1` | Yes (pride/going-alone flaw). |
| 9 | Bad end: Case 1 punishment (opt-in) | `case1_bad_end_kaoru_punishment` via `case1_punishment_bridge` | Toa demands punishment (line 477); `case1_punishment_entry` canal/registry/fail | Yes; **opt-in consent framing makes dark-Kaoru coherent** (C6). |
| 10 | Bad end: Case 2 kiln alley | `gameover_case2_alley` | External Case 2 choice; `seen_gameover_case2` | Yes (pride/going-alone). |
| 11 | Bad end: Case 3 bolt-room injury | `gameover_case3_injury` | External Case 3; sets `seen_gameover_case3` (blocks romance via `case3_bad_end_injury`) | Yes. |
| 12 | Bad end: Case 4 abandon table | `gameover_case4_abandon` | External Case 4; `seen_gameover_case4` | Yes (pride). Notably **non-brutal** discharge model. |
| 13 | Bad end: Case 4 slain on dock | `gameover_case4_slayn` | External Case 4; `case4_toa_slain` | Yes (pride/Crane-blade flaw). |
| 14 | Bad end: Case 4.5 kobune throw injury | `gameover_case4_5_boat` | External Case 4.5; `case4_5_bad_end_boat_injury` | Yes. |
| (15) | Canon Case 1 romance interludes (trust / sponsorship / default) | `case1_romance_route_trust` / `..._sponsorship` / `case1_romance_interlude` | `case1_romance_router` thresholds | Coherent (out-of-slice thematically; included for completeness). |
| (16) | Canon Case 2 morning interlude | `case2_romance_morning` | Post-Case-2 canon companion route | Coherent. |

**Endings flagged as unearned or contradictory:** #5 and #6 (Case 5 refusal -> trafficking/cage) are the only ones whose *characterization* state is not earned, because the same scene's accept branch and both canon epilogues plus the ED portray Kaoru as protective/tender. **Routing flag:** #3 (ED) may be orphaned from the canon path.

---

## 4. Continuity handoff (CRITICAL)

What this slice **reads** and therefore what earlier cases **must** have set. (Eligibility logic is defined in `case_endings.rpy` lines 26 to 111.)

### Flags / persistent vars this slice READS (and where they must be set)

Finale entry gate, via `all_romance_routes_complete()` (must all be satisfied to reach the canon Case 5 instead of the discharge stub):
- `canon_first_scene` (True) — set in **prologue**.
- `live_in_companion` (True) — set in **prologue / Case 1**.
- `kaoru_submission >= 2` — accumulated across **Cases 1 to 4**.
- `case1_romance_seen` (True) — **Case 1** romance interlude.
- `case2_festival_seen` (True) — **Case 2** festival.
- `case2_romance_seen` (True) — **Case 2** morning interlude.
- `case3_kaoru_rescue` (True) — **Case 3** (Kaoru pulls her from the bolt room).
- `case3_bad_end_injury` (must be False) — **Case 3**.
- `case4_kaoru_defended` (True) — **Case 4** dock defend. (Also read directly at case5 line 91 to gate the Case 4 recap line.)
- `case4_toa_slain` (must be False) — **Case 4**.
- `case4_bad_end_abandoned` (must be False) — **Case 4**.

Romance-bonus gate, additionally via `epilogue_romance_bonus_eligible()`:
- `case5_yoriki_accepted` (True), `case5_yoriki_refused` (must be False), `case5_closed` (True) — set within this slice.
- `case5_romance_bonus_seen` (must be False) — replay guard, set within this slice.
- `case4_5_bad_end_boat_injury` (must be False) — **Case 4.5** boat interlude.

Self-guards read at entry:
- `case5_closed` — re-entry guard (case5 line 11).

### Flags / vars this slice SETS (downstream owners should know these exist)
`case5_started`, `case5_false_exit_seen`, `case5_hearing_attended`, `case5_yoriki_offered`, `case5_yoriki_accepted`, `case5_yoriki_refused`, `case5_private_confession`, `case5_private_intimacy`, `case5_closed`, `case5_romance_bonus_seen`, `seen_gameover_case5`, `seen_gameover_rain`. (Plus the `case1/2/3/4/4_5` `seen_gameover_*` and `case1_romance_seen` / `case2_romance_seen` defaults declared at the top of `case_endings.rpy`.)

### Threads that MUST be closed before this slice
- **Case 1** closed (`case1_closed`) with its romance interlude seen.
- **Case 2** festival + romance interlude seen.
- **Case 3** survived with `case3_kaoru_rescue` (no injury bad end).
- **Case 4** dock defended (`case4_kaoru_defended`), Toa neither slain nor having abandoned the table.
- **Case 4.5** boat interlude survived (no boat injury) — required only for the bonus epilogue.

### Threads that are deliberately NOT closed (sequel hooks the finale assumes)
- **The "Chrysanthemum root" criminal case** is named (case5 lines 130, 307) and explicitly left open ("pinned, not closed," line 315). The finale assumes the player accepts this as an ongoing-docket hook rather than a dropped payoff. If earlier cases promised the root would be solved, that promise is outstanding.
- **The rival magistrate / Crane envoy** (case5 lines 126, 144, 204) are introduced at the hearing and never resolved. The finale assumes they read as political texture, not new plot threads requiring closure.

### Payoffs that depend on earlier setup
- **"Snacks after tides" running gag** (Case 1 romance interludes, e.g. lines 184/241/285) pays off in the rain bad end (line 103) and underpins Toa's voice throughout. Must exist earlier.
- **"Provisional attachment until the files close / we'll talk terms"** promise (referenced case5 lines 37, 101) must have been planted in earlier cases for the audition reveal to land.
- **Per-case recap** (case5 lines 83 to 93) depends on specific earlier beats: Case 1 Lacquered Plum comb / Scorpion; Case 2 the hill and kiln ash; Case 3 the bolt room rescue; Case 4 standing behind Kaoru on the dock. These references will read as non-sequiturs if any earlier beat was changed.
- **Red-thread / birdcage motif** in the ED assumes the office/canal/bridge imagery and the "she keeps returning" dynamic were seeded earlier.

### Characterization the finale assumes
- **Kaoru:** possessive, ledger-minded, controlling but *chose* Toa; speaks in seals/files/corridors; uses "To-chan"; capable of the "almost-smile" tenderness shown in the bonus epilogue and ED. The slice assumes this protective-possessive baseline, which is exactly why the refusal-end trafficking Kaoru (C2) reads as out of character.
- **Toa:** Crane dancer-investigator whose defining flaw is pride/going-alone (the cause of nearly every bad end) and whose arc goal is to *stand beside* Kaoru rather than be *kept*. The finale, both epilogues, and every bad end assume this exact flaw-and-goal pairing.

---

## Appendix: finding counts

- **[PLOT] findings:** 14 (P1 to P14)
- **[CHARACTER] findings:** 12 (C1 to C12)
- **[DIALOG] findings:** 16 (D1 to D16)
- **Before -> after rewrites provided:** 14 (D1, D2, D3, D4, D5, D6, D7, D8, D9, D11, D12, D13, D15 [two example lines], and the D10 comment fix)
- **Em dashes in player-facing text:** 0 (one en dash in a code comment, `case_endings.rpy` line 61).
