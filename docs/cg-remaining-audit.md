# CG remaining audit â€” Ryoko Owari Nights

**Date:** 2026-06-03  
**Scope:** `game/images/cgs*.rpy`, `cgs-choice-moments.rpy`, `gallery.rpy`, `show_cg_scene` / `images/cg|op|ed/` in `game/*.rpy` (excluding `game/versions/`). Docs cross-check. **Audit only â€” no images generated.**

**Method:** Automated path scan of 168 referenced PNGs under `game/images/{cg,op,ed}/` plus manual script/gallery/docs review and spot-check of Case 4.5 / Case 3.5 art.

---

## Summary counts

| Category | Count | Notes |
|----------|------:|-------|
| **PNG paths referenced** (CG defs + gallery + OP + ED) | 168 | From `cgs*.rpy`, `gallery.rpy`, `opening.rpy`, `ed_sequence.rpy`, `epilogue_rain_gameover.rpy`, `case_endings.rpy` |
| **Missing on disk** | **0** | — |
| **Present on disk** | 168 | |
| **`game/images/cg/` PNG files** | 129 | Includes alternates (`*_old.png`) not all referenced |
| **OP stills** | 17 / 17 | All `opening.rpy` paths exist |
| **ED stills** | 36 / 36 | All `ed_sequence.rpy` paths exist |
| **`show_cg_scene` calls** (unique tags) | 96 | Story + moments |
| **Complete (wired + file OK)** | ~94 | See gaps below |
| **Placeholder / reuse / polish** | ~25 | Moment reuses, legacy Case 3.5 slots, bg-as-CG, comment-flagged 1536 duo pass |
| **Tooling-only defs** (not story/gallery) | 21+ | `cg choice *`, steamy prologue alts, `gameover_rain_flee` skipped in script |

**Headline:** Story CG pipeline is **largely complete**. Largest **content** gaps are **unwired beats** (barge boarding, five Case 3.5 gallery slots) and **quality/setting** polish (Tear Drop establishing vs canal reuse), not missing files.

---

## Case 4.5 â€” marina / kobune vs old canal

**Discord align:** Teardrop Island **winter marina**, beached **kobune**, gunwale throw â€” not magistrate canal / skiff.  
**Docs:** `docs/plot-guide-case4-5-boat.md` (regen table), `docs/voice-performance-manifest.md` (2026-06-03 regen note).  
**Code:** `game/images/cgs-case4-5-boat.rpy` â€” comments say regen when art shows canal; legacy ID `case4_5_boat_canal_night` kept.

| File | Ren'Py tag | On disk | Visual QA (2026-06-03) | Status |
|------|------------|---------|-------------------------|--------|
| `cg-case4_5-boat-canal-night.png` | `case4_5_boat_canal_night` | Yes | Winter shore, broken pilings, beached kobune, stars â€” **not** noble canal | **Complete** (rename optional) |
| `cg-case4_5-boat-duo-tense.png` | `case4_5_boat_duo_tense` | Yes | Soaked Kaoru on rubble shore, Toa approaching | **Complete** |
| `cg-case4_5-boat-throw-splash.png` | `case4_5_boat_throw_splash` | Yes | Throw into **kobune hull**, wet deck | **Complete** |
| `cg-case4_5-boat-lantern-implied.png` | `case4_5_boat_lantern_implied` | Yes | Interior silhouettes / gunwales | **Complete** |
| `cg-case4_5-bad-boat-injury.png` | `gameover_case4_5_boat` | Yes | Bad-end thwart (not re-viewed frame-by-frame) | **Complete** (playtest) |
| *(moment)* `case4_5_boat_crisis_menu` | reuses `duo-tense` PNG | â€” | **Not called** in `case4_5_boat.rpy` today | Def only |

**Verdict:** Case 4.5 set **matches Discord marina/kobune intent** after 2026-06-03 regen. Only cleanup left is **misleading filename** `boat-canal-night` and optional wiring of `case4_5_boat_crisis_menu` before the fall menu.

---

## Canon undress CG (resolved 2026-06-03)

cgs-canon-ending.rpy and gallery.rpy use images/cg/cg-canon-undress-toa.png for tag canon_undressing.

---

## Unwired story CGs (file exists, no `show_cg_scene` on that tag)

| Tag | PNG | Chapter | Notes |
|-----|-----|---------|-------|
| `case1_barge_confront` | `cg-case1-barge-confrontation.png` | Case 1 | Gallery unlock only; `case1_barge_boarding` is sprite-only |
| `case1_canal_body` | `cg-case1-canal-body.png` | Case 1 | Shown only via `moment case1_canal_menu` / probe |
| `case1_high_tide_barge` | `cg-case1-high-tide-barge.png` | Case 1 | Shown only via `moment case1_barge_menu` |
| `case3_5_date_island_night` | `cg-case3_5-date-island-night.png` | Case 3.5 | Gallery; canal-night establishing (not wired post-rewrite) |
| `case3_5_date_kaiseki` | `cg-case3_5-date-kaiseki.png` | Case 3.5 | Prop still; story uses `kaiseki_duo` |
| `case3_5_date_duo_table` | `cg-case3_5-date-duo-table.png` | Case 3.5 | Gallery; superseded by `kaiseki_duo` in script |
| `case3_5_date_toa_watching` | `cg-case3_5-date-toa-watching.png` | Case 3.5 | Gallery; fits dance-lesson beat, unwired |
| `case3_5_date_gossip_shadow` | `cg-case3_5-date-gossip-shadow.png` | Case 3.5 | Gallery; story uses `gossip` duo CG |
| `gameover_rain_flee` | `cg-gameover-rain-flee.png` | Prologue bad end | Def + gallery; **skipped** â€” script goes straight to `gameover_rain_run` |

Investigation menus reuse investigation art (`case2_*`, `case3_fabric_shop`, etc.) â€” wired as `moment *`, not direct tags.

---

## Placeholder / duplicate / comment flags

| Location | Flag |
|----------|------|
| `cgs-case3_5-date.rpy` L19 | `# Character-focused CGs â€¦ 1536Ã—1024 placeholders` on arrival/kaiseki_duo/dance/lesson/gossip/walk/reassurance |
| `cgs-case4-5-boat.rpy` L3 | Regen if art shows canal skiff |
| `backgrounds.rpy` | `guest_house_room` â†’ `magistrate_office.png`; `warehouse_district` / `fabric_shop` / `dock_raid` borrow CGs |
| `cgs-choice-moments.rpy` | Many menus **reuse** same PNG (corridor, permit desk, canal body, case2 desk for case4 briefing, etc.) â€” see `docs/cg-pre-choice-map.md` |
| `cgs-canon-ending.rpy` | `canon_permit_signed` aliases `canon_signing` PNG |
| `gallery.rpy` L27â€“30 | Excludes `cg choice *` (never shown â†’ never unlocked) |

**Pre-choice reuse map (not separate art):** `prologue_door_*` â†’ corridor; `case1_companion_accept` â†’ permit desk; `case1_kaoru_probe` â†’ canal body; `case3_briefing` / `investigation` â†’ fabric shop; `case4_briefing` â†’ case2 academy desk; `case4_table` â†’ licensed quarter (deprecated menus removed from Case 4).

---

## Docs vs repo (planned CGs)

| Doc | Says | Repo reality (2026-06-03) |
|-----|------|---------------------------|
| `case1-investigation-scene.md` | Licensed quarter / Suzu / ledger / barge PNGs â€œto generateâ€ | **Files exist** and power menus + gallery â€” doc **outdated**; eyeball vs Lacquered Plum brief |
| `case3.5-date-interlude-design.md` | 14 gallery entries | **20** gallery slots; 15 tags in `show_cg_scene` |
| `plot-guide-is-this-a-date.md` | VN was canal compression | **Superseded** â€” `case3_5_date_interlude.rpy` is Tear Drop kaiseki (rewrite note in doc footer) |
| `plot-guide-case4-5-boat.md` | Regen prompts if canal | **Regen done** per voice manifest + visual QA |
| `canon-encounter-beats.md` | Tame canon CG list | **OK** |
| `cg-pre-choice-map.md` | 0 menus missing art | Still accurate for **wiring**; not all unique art |

---

## Tables by chapter

Status key: **OK** = file exists + shown in play path; **Reuse** = moment/alias; **Unwired** = file OK, tag not in `show_cg_scene`; **Missing** = broken path; **Polish** = exists, quality/setting upgrade; **Tool** = defs only.

### Prologue & canon

| PNG path | Ren'Py name | Status |
|----------|-------------|--------|
| `cg-first-scene-corridor-lost.png` | `corridor_lost`, moments door | OK |
| `cg-first-scene-permit-desk.png` | `permit_desk`, moments | OK |
| `cg-first-scene-office-dance.png` | `office_dance`, moment performance | OK |
| `cg-first-scene-chair-tension.png` | `chair_tension`, moment unless | OK |
| `cg-choice-moment-prologue_formality_menu.png` | moment formality | OK |
| `cg-choice-moment-prologue_before_dance_menu.png` | moment before dance | OK |
| `cg-choice-office-comply.png` | moment enter office | Reuse |
| `cg-choice-dance-refuse.png` | moment refuse retry | Reuse |
| `cg-choice-grab-rebuke.png` | moment grab | Reuse |
| `cg-canon-proposition.png` | `canon_proposition` | OK |
| `cg-canon-pull-close.png` | `canon_pull_close` | OK |
| `cg-canon-undress-toa.png` | `canon_undressing` | **OK** |
| `cg-canon-embrace.png` | `canon_embrace` | OK |
| `cg-canon-afterglow.png` | `canon_afterglow` | OK |
| `cg-canon-signing.png` | `canon_signing` | OK |
| `cg-canon-three-days.png` | `canon_three_days` | OK |
| `cg-gameover-rain-run.png` | `gameover_rain_run` | OK |
| `cg-gameover-rain-alone.png` | `gameover_rain_alone` | OK |
| `cg-gameover-rain-flee.png` | `gameover_rain_flee` | Unwired |
| `cg-badend-kaoru-*.png` (8) | `badend_kaoru_*` | OK |
| `cg-badend-brothel-*.png` (6) | `badend_brothel_*` | OK |
| `cg-prologue-dance-disrobe.png` etc. | steamy / dance alts | Tool |

### Case 1

| PNG path | Ren'Py name | Status |
|----------|-------------|--------|
| `cg-choice-moment-case1_first_duty_menu.png` | moment | OK |
| `cg-choice-moment-case1_briefing_menu.png` | moment | OK |
| `cg-case1-canal-body.png` | moment canal / probe | Reuse |
| `cg-case1-licensed-quarter.png` | moment registry, bg | OK / Polish |
| `cg-case1-guesthouse-suzu.png` | moment witness | OK / Polish |
| `cg-case1-registry-ledger.png` | moment ledger | OK / Polish |
| `cg-case1-high-tide-barge.png` | moment barge | Reuse |
| `cg-case1-barge-confrontation.png` | `case1_barge_confront` | **Unwired** |
| `cg-case1-romance-*.png` (5) | romance router | OK |
| `cg-case1-bad-*.png` (5) | gameover punishment + canal | OK |

### Case 2

| PNG path | Ren'Py name | Status |
|----------|-------------|--------|
| `cg-case2-academy-desk.png` | moment briefing | Reuse |
| `cg-case2-alley-courier.png` | moment alley | Reuse |
| `cg-case2-warehouse-ash.png` | moment desk, bg | Reuse |
| `cg-case2-festival-*.png` (4) | festival interlude | OK |
| `cg-case2-romance-morning.png` | morning tea | OK |
| `cg-case2-bad-exile.png` | gameover | OK |

### Case 3

| PNG path | Ren'Py name | Status |
|----------|-------------|--------|
| `cg-case3-fabric-shop.png` | fabric + moments | OK |
| `cg-case3-accident-moment.png` | accident + moment | OK |
| `cg-case3-kaoru-rescue.png` | rescue | OK |
| `cg-case3-bad-injury.png` | gameover | OK |

### Case 3.5 â€” Is this a date?

| PNG path | Ren'Py name | Status |
|----------|-------------|--------|
| `cg-case3_5-date-silk-fabric.png` | `case3_5_date_silk_fabric` | OK |
| `cg-case3_5-date-arrival.png` | `case3_5_date_arrival` | OK / Polish (canal bridge) |
| `cg-case3_5-date-inn-exterior.png` | `case3_5_date_inn_exterior` | OK |
| `cg-case3_5-date-tatami-lanterns.png` | `case3_5_date_tatami_lanterns` | OK |
| `cg-case3_5-date-kaiseki-duo.png` | `case3_5_date_kaiseki_duo` | OK / comment placeholder |
| `cg-case3_5-date-sake-cup.png` | `case3_5_date_sake_cup` | OK |
| `cg-case3_5-date-candle-flame.png` | `case3_5_date_candle_flame` | OK |
| `cg-case3_5-date-toa-lashes.png` | `case3_5_date_toa_lashes` | OK |
| `cg-case3_5-date-dance.png` | `case3_5_date_dance` | OK / placeholder |
| `cg-case3_5-date-lesson.png` | `case3_5_date_lesson` | OK / placeholder |
| `cg-case3_5-date-kaoru-hand-cup.png` | `case3_5_date_kaoru_hand_cup` | OK |
| `cg-case3_5-date-gossip.png` | `case3_5_date_gossip` | OK / placeholder |
| `cg-case3_5-date-reassurance.png` | `case3_5_date_reassurance` | OK / placeholder |
| `cg-case3_5-date-walk-duo.png` | `case3_5_date_walk_duo` | OK / placeholder |
| `cg-case3_5-date-almost-hands.png` | `case3_5_date_almost_hands` | OK |
| `cg-case3_5-date-island-night.png` | `case3_5_date_island_night` | Unwired / Polish |
| `cg-case3_5-date-kaiseki.png` | `case3_5_date_kaiseki` | Unwired |
| `cg-case3_5-date-duo-table.png` | `case3_5_date_duo_table` | Unwired |
| `cg-case3_5-date-toa-watching.png` | `case3_5_date_toa_watching` | Unwired |
| `cg-case3_5-date-gossip-shadow.png` | `case3_5_date_gossip_shadow` | Unwired |

### Case 4 & 4.5

| PNG path | Ren'Py name | Status |
|----------|-------------|--------|
| `cg-case4-gritty-establishing.png` | establishing, bg | OK |
| `cg-case4-fight-wide.png` | fight + moment | OK |
| `cg-case4-romance-defend.png` | defend | OK |
| `cg-case4-bad-slayn.png` | gameover | OK |
| `cg-case4_5-boat-*.png` (5) | boat interlude + bad end | OK (see Case 4.5) |

### Opening (`images/op/`) & ending (`images/ed/`)

All referenced OP (17) and ED (35) PNGs **present**. OP also aliases four prologue/case1 CGs from `images/cg/` for montage â€” no extra missing files.

### Choice-outcome set (`cgs-choices.rpy`, 21 PNGs)

**Not shown in story** (gallery excluded by design). Not counted as â€œremainingâ€ unless you want branch-specific post-choice art later.

---

## Priority list (for Amanda)

2. **Wire `case1_barge_confront`** at boarding (`case1_barge_boarding`) â€” art is finished; scene is text-only today.
3. **Case 3.5 gallery cleanup** â€” wire `island_night` after black fade, `toa_watching` at dance lesson, or remove dead gallery slots (`kaiseki`, `duo_table`, `gossip_shadow`).
4. **Case 3.5 polish pass** â€” regen duo placeholders per `cgs-case3_5-date.rpy` comment; replace `island-night` canal reuse with Tear Drop winter bay.
5. **Eyeball Case 1 investigation CGs** vs `cgs-choice-moments.rpy` prompts (Plum on stilts, Suzu comb) â€” files exist but docs still asked for dedicated art.
6. **Playtest Case 4.5 bad end** + `lantern_implied` in context (regen set looks on-brief).
7. **Update `docs/case1-investigation-scene.md`** placeholder section so audit docs match repo.
8. **Dedicated backgrounds** â€” `guest_house_room`, true `licensed_quarter` (stop aliasing office / street).
9. **Optional:** restore `gameover_rain_flee` as beat 1 or drop def/gallery slot.
10. **Housekeeping:** rename `cg-case4_5-boat-canal-night` â†’ `marina-night`; prune unreferenced `*_old.png` in `cg/`.

---

## Scan command (re-run)

```bat
python scripts\_cg_audit_scan.py
```

*(Script was used for this audit then removed; re-create from repo history or duplicate the path scan logic above.)*

---

*Generated for Ryoko Owari Nights vertical slice (Cases 1â€“4.5 + prologue/canon). Case 5+ not in tree.*
