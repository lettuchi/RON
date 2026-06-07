# Modern AU CG regen log — western attire fix

**Date:** 2026-06-04  
**Reason:** Newest AU batch drifted to kimono/feudal dress; regen with Modern AU reference pack.  
**Backup:** `game/images/cg/versions/au-modern-regen-western-2026-06-04/` (22 files)  
**Refs used:** `docs/art-references/au-modern/*-reference.png` + `game/images/reference/style-painterly-reference.png` (+ waist-up refs for closeups; canon sprites face/hair only on phone closeups)  
**Prompt block:** `scripts/au_modern_cg_prompt_block.txt`  
**No git commit.**

## Summary

| Metric | Count |
|--------|------:|
| Total AU CGs audited | 22 |
| Regenerated (pass) | 22 |
| Failed | 0 |
| `.rpy` changes | 0 (filenames/tags unchanged) |

## Case 2 — Island Weekend (priority 1)

| File | Status | Notes |
|------|--------|-------|
| `cg-au-modern-case2-ferry-rain.png` | pass | Ferry deck rain; Toa tracksuit + gold crane logo, Kaoru charcoal suit |
| `cg-au-modern-case2-airbnb-exterior.png` | pass | Cottage exterior dusk; both in western AU default attire |
| `cg-au-modern-case2-one-bed.png` | pass | One-bed Airbnb; tracksuit + suit, no period dress |
| `cg-au-modern-case2-phone-text.png` | pass | Toa waist-up closeup; tracksuit + phone glow; waist-up AU ref |
| `cg-au-modern-case2-balcony-night.png` | pass | Balcony night; tracksuit + suit, blanket moment |
| `cg-au-modern-case2-intimate-audit.png` | pass | Tasteful fully clothed after-hours audit; no kimono/nudity |

## Case 1 — Wellness Compliance (priority 2)

| File | Status | Notes |
|------|--------|-------|
| `cg-au-modern-case1-club-exterior.png` | pass | Wellness club exterior; tracksuit + suit |
| `cg-au-modern-case1-clipboard.png` | pass | Inspection floor; clipboard compliance scene |
| `cg-au-modern-case1-phone-notes.png` | pass | Toa filming notes; waist-up tracksuit ref |
| `cg-au-modern-case1-kaoru-doorway.png` | pass | Doorway bureaucracy flirt; suit + tracksuit |
| `cg-au-modern-case1-hallway-tense.png` | pass | Hallway confrontation; western office wear only |
| `cg-au-modern-case1-elevator-echo.png` | pass | Service elevator rain glass; tracksuit + suit |

## Wrong Floor — original 9 (priority 3)

| File | Tag | Status | Notes |
|------|-----|--------|-------|
| `cg-au-modern-rain-parking.png` | `au_modern_rain_parking` | pass | Harbor parking raincoat over tracksuit |
| `cg-au-modern-wrong-floor.png` | `au_modern_wrong_floor` | pass | Glass doorway badge reader; tracksuit not kimono |
| `cg-au-modern-zoom-hearing.png` | `au_modern_zoom_hearing` | pass | Licensing office council monitor grid |
| `cg-au-modern-studio-audition.png` | `au_modern_studio_audition` | pass | Mirror studio barre; tracksuit port de bras |
| `cg-au-modern-contract-desk.png` | `au_modern_contract_desk` | pass | Tablet/PDF hands; tracksuit sleeves + suit cuffs |
| `cg-au-modern-phone-date.png` | `au_modern_phone_date` | pass | Phone glow + rain glass silhouette |
| `cg-au-modern-elevator.png` | `au_modern_elevator` | pass | Service elevator Unless? branch; clothed proximity |
| `cg-au-modern-curry-breakroom.png` | `au_modern_curry_breakroom` | pass | Break room curry + stamp on paper plate |
| `cg-au-modern-couch-stinger.png` | `au_modern_couch_stinger` | pass | Office couch blanket + clementines |

## AU gallery extra (priority 4)

| File | Tag | Status | Notes |
|------|-----|--------|-------|
| `cg-toa-ballet-practice-room.png` | `toa_ballet_practice_room` | pass | Mirror barre practice; tracksuit arabesque, Kaoru suit doorway witness |

## Registry verification

- `game/images/cgs-au-modern.rpy` — 9 tags, filenames match
- `game/images/cgs-au-modern-case1.rpy` — 6 tags, filenames match
- `game/images/cgs-au-modern-case2.rpy` — 6 tags, filenames match
- `game/images/cgs-practice-room.rpy` — `toa_ballet_practice_room` unchanged
- `game/gallery.rpy` — Extra: AU Wrong Floor (Modern) paths unchanged

## Attire anchors applied

- **Toa:** black zip tracksuit, gold side stripes, gold crane logo on chest (Crane Conservatory sponsorship)
- **Kaoru:** charcoal grey deputy director suit, white shirt, dark tie
- **Negatives:** kimono, kosode, furisode, hakama, obi, zori, magistrate robes, L5R period dress (full AU block)
