# Canon CG QA report — 2026-06-07

**Scope:** L5R canon CGs only. Excluded: `cgs-au-modern*`, `cgs-practice-room.rpy`, all `au_modern_*` assets/scripts.

**Methods:** Registry + `show_cg_scene` cross-reference; MediaPipe advisory batch (`scripts/check_cg_hands.py`); **visual hand count** on all high-risk wired CGs and clear failures; GenerateImage regen with backups.

---

## Summary counts

| Metric | Count |
|--------|------:|
| Canon registry tags (`cgs-*.rpy`, excl. AU) | 112 |
| Unique registry PNG paths | 111 |
| **Wired gameplay tags** (`show_cg_scene`, excl. AU) | 124 |
| **Wired unique PNGs** (resolved paths) | **100** (94 from registries + 6 inline in `case_endings.rpy` / `epilogue_rain_gameover.rpy`) |
| Disk canon-pattern PNGs (`cg-case*`, `cg-prologue*`, etc., excl. AU) | 162 |
| Orphan registry-only tags (not wired) | 18 |
| Human-visible wired PNGs (heuristic) | ~90 |
| **Visually hand-audited (high-risk + failures)** | **35** |
| Hand **FAIL** (pre-regen) | **6** |
| Hand **regens promoted** | **6** |
| Hand **borderline** (user review) | **4** |
| Background consistency issues (clear defect) | **0** |
| Background regens | **0** |
| Remaining wired CGs (advisory / second pass) | **~59** |

---

## Top 5 worst offenders (pre-regen)

| File | Issue |
|------|--------|
| `cg-first-scene-office-dance.png` | Toa **6 fingers** on desk hand (prologue dance — high visibility) |
| `cg-case2-festival-kiss.png` | Wrong thumb / **extra hand** on embrace (style gold-standard CG) |
| `cg-case3_5-date-almost-hands.png` | Kaoru reaching hand **6 digits** |
| `cg-epilogue-romance-kotatsu-intimate.png` | Kaoru shoulder hand **6 digits** |
| `cg-case4_5-boat-hands-gunwale-closeup.png` | **Extra thumb / fused digits** on grip hand |

Also failed before regen: `cg-case1_5-shoji-wrist-closeup.png` (victim hand fused/extra digit) — fixed.

---

## Regens performed

Backup folder: `game/images/cg/versions/canon-redo-hands-2026-06-07/`

| Production file | Result | Notes |
|-----------------|--------|-------|
| `cg-first-scene-office-dance.png` | **Promoted (v2)** | Fan-grip composition; no desk splay hand |
| `cg-case2-festival-kiss.png` | **Promoted (v3)** | Single visible cupping hand, 5 fingers |
| `cg-case3_5-date-almost-hands.png` | **Promoted** | 2 hands × 5 fingers |
| `cg-case4_5-boat-hands-gunwale-closeup.png` | **Promoted (v2)** | Resting/grip macro, clean anatomy |
| `cg-epilogue-romance-kotatsu-intimate.png` | **Promoted** | Kotatsu duo, 3 visible hands OK |
| `cg-case1_5-shoji-wrist-closeup.png` | **Promoted** | Wrist grab through torn shoji |

Refs: `game/images/reference/style-painterly-reference.png`, canon sprites, scene anchors per `docs/cg-style-prompt-block.md`. Hand negatives in all prompts. **No `.rpy` changes.**

---

## Borderline (not auto-regen)

| File | Issue |
|------|--------|
| `cg-canon-embrace.png` | Kaoru right hand on shoulder — messy knuckles / possible extra digit at pinky |
| `cg-badend-brothel-grasp.png` | Off-screen ronin hands deliberately gnarled; long fingers — stylistic? |
| `cg-case3_5-date-lesson.png` | Pointing arm slightly long; furisode not crane work obi (may be intentional date outfit) |
| `cg-case2-festival-intimate.png` | Hands PASS; Toa **pink floral obi** vs work crane obi |

---

## Background / visual consistency

See **`docs/art-references/canon/canon-cg-continuity-notes.md`**.

| Location group | CGs compared | Finding |
|----------------|--------------|---------|
| Magistrate office | permit-desk, chair-tension, office-dance, sponsorship, signing, proposition, case5-false-exit | Layout register holds (desk, scrolls, rain window). **Borderline:** blue banner often uses floral/sun mon instead of locked **jade-sphere kiku** Emerald badge |
| Kaoru robes | office + festival + date + boat closeups | Gold/maroon register **consistent** |
| Toa appearance | work scenes vs festival intimate vs date furisode | Work = crane obi **consistent**; date furisode **intentional**; festival intimate **wardrobe drift** (borderline) |
| Rain / harbor | gameover rain, boat gunwale, badend grasp, office windows | **Consistent** mood |
| Intimate / embrace | canon encounter, festival, kotatsu, case1.5 shoji | Hand defects fixed where clear; embrace borderline noted |

**Background regens:** none — issues documented for user review, not immersion-breaking location drift.

---

## Wired vs orphan

**Inline wired defs** (not in `cgs-*.rpy` files): `case_endings.rpy` — `case2_romance_morning`, `gameover_case1_canal`, `gameover_case2_exile`, `gameover_case3_injury`; `epilogue_rain_gameover.rpy` — `gameover_rain_run`, `gameover_rain_alone`.

**Moment menu tags** (`moment case1_briefing_menu`, etc.) use spaced Ren'Py names in `cgs-choice-moments.rpy`; they reuse beat PNGs already counted above.

**Orphan registry tags** (gallery/unused beats): `canon_steamy_*`, `dance_disrobe`, `butt_wiggle_grab`, `bent_over_desk`, `case1_barge_confront`, duplicate table aliases, etc. — **not hand-audited** this pass.

---

## Hand audit table (wired unique PNGs)

Status legend: **PASS** = visual OK; **PASS (regen)** = fixed this pass; **BORDERLINE** = user review; **N/A** = no hands to count; **PASS (advisory)** = MediaPipe only; **NOT VISUALLY AUDITED** = high-risk, needs second-pass visual.

| PNG | Tag (primary wired) | Status | Hand notes |
|-----|---------------------|--------|------------|
| `cg-badend-brothel-cart.png` | `badend_brothel_cart` | PASS (advisory) | MediaPipe advisory |
| `cg-badend-brothel-crying.png` | `badend_brothel_crying` | PASS (advisory) | MediaPipe advisory |
| `cg-badend-brothel-grasp.png` | `badend_brothel_grasp` | BORDERLINE | ronin fingers stylized long |
| `cg-badend-brothel-permit.png` | `badend_brothel_permit` | PASS (advisory) | MediaPipe advisory |
| `cg-badend-brothel-ronin.png` | `badend_brothel_ronin` | PASS (advisory) | MediaPipe advisory |
| `cg-badend-brothel-tears.png` | `badend_brothel_tears` | NOT VISUALLY AUDITED | high-risk |
| `cg-badend-kaoru-corridor.png` | `badend_kaoru_corridor` | PASS (advisory) | MediaPipe advisory |
| `cg-badend-kaoru-gate.png` | `badend_kaoru_gate` | PASS (advisory) | MediaPipe advisory |
| `cg-badend-kaoru-office.png` | `badend_kaoru_office` | PASS (advisory) | MediaPipe advisory |
| `cg-badend-kaoru-office-floor.png` | `badend_kaoru_office_floor` | PASS (advisory) | MediaPipe advisory |
| `cg-badend-kaoru-office-throw.png` | `badend_kaoru_office_throw` | PASS (advisory) | MediaPipe advisory |
| `cg-badend-kaoru-shoji.png` | `badend_kaoru_shoji` | NOT VISUALLY AUDITED | high-risk |
| `cg-badend-kaoru-stamp.png` | `badend_kaoru_stamp` | PASS (advisory) | MediaPipe advisory |
| `cg-badend-kaoru-wrist.png` | `badend_kaoru_wrist` | NOT VISUALLY AUDITED | high-risk |
| `cg-canon-afterglow.png` | `canon_afterglow` | PASS (spot) | low visibility |
| `cg-canon-embrace.png` | `canon_embrace` | BORDERLINE | shoulder hand knuckles |
| `cg-canon-proposition.png` | `canon_proposition` | PASS | 3 visible |
| `cg-canon-pull-close.png` | `canon_pull_close` | PASS | 3 visible |
| `cg-canon-signing.png` | `canon_signing` | PASS | 4 visible |
| `cg-canon-three-days.png` | `canon_three_days` | PASS (advisory) | MediaPipe advisory |
| `cg-canon-undress-toa.png` | `canon_undressing` | PASS | Toa 2 visible |
| `cg-case1_5-chamber-corridor.png` | `case1_5_chamber_corridor` | PASS (advisory) | MediaPipe advisory |
| `cg-case1_5-chamber-quilt.png` | `case1_5_chamber_quilt` | NOT VISUALLY AUDITED | high-risk |
| `cg-case1_5-chamber-shoji-tea.png` | `case1_5_chamber_shoji_tea` | NOT VISUALLY AUDITED | high-risk |
| `cg-case1_5-curry-kitchen.png` | `case1_5_curry_kitchen` | PASS (advisory) | MediaPipe advisory |
| `cg-case1_5-dawn-desk-duo.png` | `case1_5_dawn_desk_duo` | PASS (advisory) | MediaPipe advisory |
| `cg-case1_5-hanko-pot.png` | `case1_5_hanko_pot` | N/A | prop focus |
| `cg-case1_5-kaoru-curry-bowl.png` | `case1_5_kaoru_curry_bowl` | PASS (advisory) | MediaPipe advisory |
| `cg-case1_5-shoji-tear-closeup.png` | `case1_5_shoji_tear` | NOT VISUALLY AUDITED | high-risk closeup |
| `cg-case1_5-shoji-wrist-closeup.png` | `case1_5_shoji_wrist` | PASS (regen) | 2×5 |
| `cg-case1-bad-canal.png` | `gameover_case1_canal` | PASS (advisory) | inline def; not visually audited |
| `cg-case1-bad-punishment-desk.png` | `gameover_case1_punishment_desk` | NOT VISUALLY AUDITED | high-risk |
| `cg-case1-bad-punishment-floor.png` | `gameover_case1_punishment_floor` | NOT VISUALLY AUDITED | high-risk |
| `cg-case1-bad-punishment-hands.png` | `gameover_case1_punishment_hands` | PASS | 1 grip hand |
| `cg-case1-bad-punishment-shoji.png` | `gameover_case1_punishment_shoji` | NOT VISUALLY AUDITED | high-risk |
| `cg-case1-romance-barge-moonlit.png` | `case1_romance_barge_moonlit` | NOT VISUALLY AUDITED | high-risk |
| `cg-case1-romance-canal-lantern.png` | `case1_romance_canal_lantern` | PASS (advisory) | MediaPipe advisory |
| `cg-case1-romance-lantern.png` | `case1_romance_lantern` | PASS (advisory) | MediaPipe advisory |
| `cg-case1-romance-office-touch.png` | `case1_romance_office_touch` | PASS | 1 visible |
| `cg-case1-romance-sponsorship.png` | `case1_romance_sponsorship` | PASS | 4 visible |
| `cg-case2-bad-exile.png` | `gameover_case2_exile` | PASS (advisory) | inline def |
| `cg-case2-festival-curry-stall.png` | `case2_festival_curry_stall` | PASS (advisory) | MediaPipe advisory |
| `cg-case2-festival-fireworks.png` | `case2_festival_fireworks` | N/A | sky / crowd |
| `cg-case2-festival-hill.png` | `case2_festival_hill` | N/A | establishing |
| `cg-case2-festival-intimate.png` | `case2_festival_intimate` | PASS | 2 visible; wardrobe borderline |
| `cg-case2-festival-kiss.png` | `case2_festival_kiss` | PASS (regen v3) | 1 visible hand |
| `cg-case2-romance-morning.png` | `case2_romance_morning` | PASS (advisory) | inline def |
| `cg-case3-bad-injury.png` | `gameover_case3_injury` | PASS (advisory) | inline def |
| `cg-case3_5-date-almost-hands.png` | `case3_5_date_almost_hands` | PASS (regen) | 2×5 |
| `cg-case3_5-date-arrival.png` | `case3_5_date_arrival` | N/A | exterior |
| `cg-case3_5-date-candle-flame.png` | `case3_5_date_candle_flame` | PASS (advisory) | MediaPipe advisory |
| `cg-case3_5-date-gossip.png` | `case3_5_date_gossip` | PASS (advisory) | MediaPipe advisory |
| `cg-case3_5-date-inn-collar-hands.png` | `case3_5_date_inn_collar_hands` | PASS | 2 visible |
| `cg-case3_5-date-inn-exterior.png` | `case3_5_date_inn_exterior` | N/A | exterior |
| `cg-case3_5-date-kaiseki-duo.png` | `case3_5_date_kaiseki_duo` | PASS (advisory) | MediaPipe advisory |
| `cg-case3_5-date-kaoru-hand-cup.png` | `case3_5_date_kaoru_hand_cup` | PASS (advisory) | MediaPipe advisory |
| `cg-case3_5-date-lesson.png` | `case3_5_date_lesson` | BORDERLINE | pointing arm |
| `cg-case3_5-date-reassurance.png` | `case3_5_date_reassurance` | NOT VISUALLY AUDITED | high-risk |
| `cg-case3_5-date-sake-cup.png` | `case3_5_date_sake_cup` | PASS (advisory) | MediaPipe advisory |
| `cg-case3_5-date-silk-fabric.png` | `case3_5_date_silk_fabric` | N/A | fabric |
| `cg-case3_5-date-tatami-lanterns.png` | `case3_5_date_tatami_lanterns` | N/A | room |
| `cg-case3_5-date-toa-lashes.png` | `case3_5_date_toa_lashes` | PASS (advisory) | face macro |
| `cg-case3_5-date-walk-duo.png` | `case3_5_date_walk_duo` | PASS (advisory) | MediaPipe advisory |
| `cg-case3_5-date-watch-dancers.png` | `case3_5_date_watch_dancers` | NOT VISUALLY AUDITED | high-risk |
| `cg-case3-accident-moment.png` | `case3_accident_moment` | PASS (advisory) | MediaPipe advisory |
| `cg-case3-fabric-shop.png` | `case3_fabric_shop` | N/A | shop |
| `cg-case3-kaoru-rescue.png` | `case3_kaoru_rescue` | PASS (advisory) | MediaPipe advisory |
| `cg-case4_5-bad-boat-injury.png` | `gameover_case4_5_boat` | PASS (advisory) | MediaPipe advisory |
| `cg-case4_5-boat-canal-night.png` | `case4_5_boat_canal_night` | N/A | boat wide |
| `cg-case4_5-boat-duo-tense.png` | `case4_5_boat_duo_tense` | PASS (advisory) | MediaPipe advisory |
| `cg-case4_5-boat-hands-gunwale-closeup.png` | `case4_5_boat_hands_gunwale` | PASS (regen v2) | 2×5 |
| `cg-case4_5-boat-lantern-implied.png` | `case4_5_boat_lantern_implied` | N/A | silhouette |
| `cg-case4_5-boat-lash-rain-closeup.png` | `case4_5_boat_lash_rain` | N/A | face macro |
| `cg-case4_5-boat-throw-splash.png` | `case4_5_boat_throw_splash` | N/A | action wide |
| `cg-case4-bad-slayn.png` | `gameover_case4_slayn` | PASS (advisory) | MediaPipe advisory |
| `cg-case4-fight-wide.png` | `case4_fight_wide` | N/A | fight wide |
| `cg-case4-gritty-establishing.png` | `case4_gritty_establishing` | N/A | establishing |
| `cg-case4-romance-defend.png` | `case4_romance_defend` | PASS | 4 visible |
| `cg-case5-bad-chained.png` | `gameover_case5_chained` | N/A | implied |
| `cg-case5-bad-quarter-cage.png` | `gameover_case5_quarter_cage` | N/A | cage |
| `cg-case5-bedroom-toy.png` | `case5_bedroom_toy` | NOT VISUALLY AUDITED | high-risk |
| `cg-case5-epilogue-week.png` | `case5_epilogue_week` | N/A | montage |
| `cg-case5-false-exit-office.png` | `case5_false_exit_office` | PASS | 2 on letter |
| `cg-case5-hearing-hall.png` | `case5_hearing_hall` | N/A | hall |
| `cg-case5-hearing-kaoru-dais.png` | `case5_hearing_kaoru_dais` | PASS (advisory) | MediaPipe advisory |
| `cg-case5-oath-seal-hand-closeup.png` | `case5_oath_seal_hand` | PASS | 2 macro |
| `cg-case5-private-talk.png` | `case5_private_talk` | PASS (advisory) | MediaPipe advisory |
| `cg-case5-scroll-desk.png` | `case5_scroll_desk` | PASS (advisory) | MediaPipe advisory |
| `cg-case5-yoriki-oath.png` | `case5_yoriki_oath` | PASS (advisory) | MediaPipe advisory |
| `cg-case-zero-rain-alley-door.png` | `case_zero_rain_alley_door` | N/A | door |
| `cg-case-zero-redacted-docket.png` | `case_zero_redacted_docket` | N/A | prop |
| `cg-epilogue-kotatsu-warmth-closeup.png` | `epilogue_kotatsu_warmth` | NOT VISUALLY AUDITED | high-risk; stub noted in docs |
| `cg-epilogue-romance-kotatsu-intimate.png` | `epilogue_romance_kotatsu_intimate` | PASS (regen) | 3 visible |
| `cg-first-scene-chair-tension.png` | `chair_tension` | PASS | 3 visible |
| `cg-first-scene-corridor-lost.png` | `corridor_lost` | PASS (advisory) | MediaPipe advisory |
| `cg-first-scene-office-dance.png` | `office_dance` | PASS (regen v2) | fan grip |
| `cg-first-scene-permit-desk.png` | `permit_desk` | N/A | no hands |
| `cg-gameover-rain-alone.png` | `gameover_rain_alone` | N/A | Toa small / rain |
| `cg-gameover-rain-run.png` | `gameover_rain_run` | N/A | rain run |
| `cg-prologue-wrong-door.png` | `prologue_wrong_door` | PASS (advisory) | MediaPipe advisory |

---

## Pass 2 (2026-06-07)

**Agent:** continuation of pass 1 (`0fd31880-29f2-4a5f-a15e-365fa7081f14`). Visual read-back ground truth; MediaPipe not re-run.

### Pass 2 summary counts

| Metric | Count |
|--------|------:|
| **Priority A wired high-risk visually audited** | **14** |
| Priority A hand **FAIL** (clear) | **0** |
| Priority A **borderline** | **1** (`punishment-floor` victim right-hand thumb) |
| Priority B re-audited | **3** |
| Priority C orphan high-risk sampled | **16** (+ `cg-case1-r18-intimacy.png`) |
| Orphan disk total (excl. AU, `_old`) | **67** |
| Pass 2 hand **FAIL** (clear) | **2** (both orphans) |
| Pass 2 hand **regens promoted** | **1** |
| Pass 2 regen blocked / not promoted | **1** |

**Backup folder (pass 2):** `game/images/cg/versions/canon-redo-hands-2026-06-07-pass2/`

### Priority A — wired high-risk (was NOT VISUALLY AUDITED)

| PNG | Tag | Pass 2 status | Hand notes |
|-----|-----|---------------|------------|
| `cg-badend-brothel-tears.png` | `badend_brothel_tears` | PASS | Face macro; no hands |
| `cg-badend-kaoru-shoji.png` | `badend_kaoru_shoji` | PASS | Silhouettes only; sleeves obscure hands |
| `cg-badend-kaoru-wrist.png` | `badend_kaoru_wrist` | PASS | Grip + limp hand, 2×5 |
| `cg-case1_5-chamber-quilt.png` | `case1_5_chamber_quilt` | PASS | Quilt grip + lap hand, 2×5 |
| `cg-case1_5-chamber-shoji-tea.png` | `case1_5_chamber_shoji_tea` | PASS | Tray grip, 2×5 |
| `cg-case1_5-shoji-tear-closeup.png` | `case1_5_shoji_tear` | PASS | Prop/torn shoji; no hands |
| `cg-case1-bad-punishment-desk.png` | `gameover_case1_punishment_desk` | PASS | Chin + desk fist, 2×5 |
| `cg-case1-bad-punishment-floor.png` | `gameover_case1_punishment_floor` | BORDERLINE | Both palms 5 digits; viewer-left thumb joint stiff |
| `cg-case1-bad-punishment-shoji.png` | `gameover_case1_punishment_shoji` | PASS | Collar grip + floor + shoji, 3 hands OK |
| `cg-case1-romance-barge-moonlit.png` | `case1_romance_barge_moonlit` | PASS | No hands in frame |
| `cg-case3_5-date-reassurance.png` | `case3_5_date_reassurance` | PASS | Shoulder + clasped hands, 4 visible OK |
| `cg-case3_5-date-watch-dancers.png` | `case3_5_date_watch_dancers` | PASS | Dancer fan hands, 6 hands OK |
| `cg-case5-bedroom-toy.png` | `case5_bedroom_toy` | PASS | Prop/room still; no characters |
| `cg-epilogue-kotatsu-warmth-closeup.png` | `epilogue_kotatsu_warmth` | PASS | Feet macro only; 4×5 toes |

**Priority A result:** All 14 wired high-risk CGs now have a visual pass. No production regens required.

### Priority B — borderline re-audit

| PNG | Pass 2 decision | Notes |
|-----|-----------------|-------|
| `cg-canon-embrace.png` | **BORDERLINE (no regen)** | Kaoru back-hand knuckles still slightly crowded; finger count correct (5). Not clearly 6-digit — user playtest call. |
| `cg-case2-festival-intimate.png` | **PASS hands; wardrobe OK** | Re-read shows gold **crane** on peach obi; cherry kosode is intentional festival dress. Prior “pink floral obi drift” downgraded — obi crane present. |
| Office blue banner (multi-CG) | **Document only** | `choice-grab-lean-in`, `choice-dance-immediate` (regen), `punishment-shoji` still use floral/sun mon on blue banner, not jade-sphere kiku lock. Subjective; not immersion-breaking. |

### Priority C — orphan / gallery / choice-outcome

**Scope:** 67 disk orphans (excl. `cg-au-modern*`, `*_old*`). **16 high-risk** keyword orphans + `cg-case1-r18-intimacy.png` visually audited; **47 low-risk** orphans (establishing, props, duplicates) **not** individually opened this pass.

| PNG | Status | Hand notes |
|-----|--------|------------|
| `cg-canon-steamy-intimacy.png` | BORDERLINE | Shoulder hand knuckles (same family as `canon-embrace`) |
| `cg-canon-steamy-undress-toa.png` | PASS | 2×5 on Toa |
| `cg-canon-steamy-afterglow.png` | BORDERLINE | Shoulder + forearm hands slightly uneven knuckles |
| `cg-prologue-bent-over-desk.png` | PASS | Desk fist + hip hand, 2×5 |
| `cg-prologue-butt-wiggle-grab.png` | PASS | Wall + hip, 2×5 (pinky slightly long) |
| `cg-prologue-dance-disrobe.png` | **FAIL** | Woman left hand blob/extra protrusion; man chin hand mushy — **not promoted** (regen blocked on retry) |
| `cg-choice-grab-lean-in.png` | PASS | Hand clasp + shoulder; shoulder knuckles borderline |
| `cg-choice-grab-rebuke.png` | PASS | Wrist grab + fan, 4 visible OK |
| `cg-choice-dance-immediate.png` | **PASS (regen)** | Promoted pass 2 — fan + clasped hands, 4×5 |
| `cg-choice-dance-negotiate.png` | PASS | Fan + extended hand, 4×5 |
| `cg-choice-dance-refuse.png` | BORDERLINE | Crossed-arm fingers slightly irregular spacing |
| `cg-case4-date-almost-hands.png` | PASS | Railing hands, 4×5 (long pinky borderline) |
| `cg-case3_5-date-duo-table.png` | PASS | Chin + sake cup, 2×5 |
| `cg-case1-r18-intimacy.png` | PASS | 4 hands embrace, 4×5 |

### Pass 2 regens

| Production file | Result | Notes |
|-----------------|--------|-------|
| `cg-choice-dance-immediate.png` | **Promoted** | Office dance twirl; fan + hand-hold, clean anatomy |
| `cg-prologue-dance-disrobe.png` | **Not promoted** | Pre-regen FAIL remains; safety-blocked on composition-locked retry |

### Cumulative totals (pass 1 + pass 2)

| Metric | Pass 1 | Pass 2 | Cumulative |
|--------|-------:|-------:|-----------:|
| Visually hand-audited (high-risk + failures) | 35 | +31 | **~66** |
| Hand FAIL → regen promoted | 6 | 1 | **7** |
| Hand borderline (user review) | 4 | +5 | **~9** |
| Wired high-risk NOT visually audited | ~15 | 0 | **0** |

### Still not visually audited after pass 2

- **~47 low-risk orphan PNGs** (establishing shots, ledger/prop stills, choice menu duplicates, `cg-case2-romance-morning.png`, inline gameover aliases on disk, etc.).
- **~45 wired CGs** at **PASS (advisory)** from pass 1 only (MediaPipe, no visual open) — low hand visibility (crowd, macro face, wide fight).
- **`cg-prologue-dance-disrobe.png`** — clear orphan FAIL; needs manual regen or NovelAI with composition lock.
- **Office jade-sphere kiku banner** — cosmetic multi-CG alignment (optional art pass).

---

## Second pass recommended (pass 3)

1. **Manual regen** `cg-prologue-dance-disrobe.png` (orphan gallery; safety filter blocked GenerateImage retry).
2. **Optional borderline regen:** `cg-canon-embrace.png`, `cg-canon-steamy-afterglow.png`, `cg-canon-steamy-intimacy.png` if knuckle crowding bothers playtest.
3. **Office banner emblem** alignment (jade-sphere kiku) — cosmetic batch.
4. **Low-risk orphan spot sample** (~47 remaining) — gallery completeness only.
5. Update `cg-style-prompt-block.md` gold standard note: festival kiss regen v3 + `choice-dance-immediate` pass 2 as hand-safe office-dance refs.

---

## Artifacts

- `docs/_canon_cg_inventory.txt` — wired/orphan listing
- `docs/_canon_hand_audit.json` — MediaPipe batch output
- `docs/art-references/canon/canon-cg-continuity-notes.md` — continuity bible
- `scripts/canon_cg_inventory.py`, `scripts/canon_cg_hand_audit.py` — helper scripts (optional reuse)

**No git commit** per task constraints.
