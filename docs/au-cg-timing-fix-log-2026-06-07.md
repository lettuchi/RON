# Modern AU CG Timing + Text Overflow Fix Log

**Date:** 2026-06-07  
**Scope:** All five Modern AU `.rpy` scripts only (canon untouched)

## Summary

| Episode | CG timing moves | `scene black` removed/tightened | Lines split/shortened |
|---------|----------------:|--------------------------------:|----------------------:|
| Wrong Floor | 12 | 4 | 52 |
| Case 1: Wellness Compliance | 10 | 3 | 53 |
| Case 2: Island Weekend | 11 | 2 | 25 |
| Case 3: Permits & HR | 9 | 4 | 52 |
| Epilogue: Effective Immediately | 7 | 1 | 48 |
| **Total** | **49** | **14** | **230** |

## CG timing — representative before/after

### Wrong Floor — rain parking
**Before:** Four long narrator paragraphs (incl. two unvoiced blocks) → then `show_cg_scene("au_modern_rain_parking")`.  
**After:** CG appears immediately after `narrator_472`; unvoiced sponsorship prose plays on the parking art.

### Case 1 — wellness arrival
**Before:** Full corridor narration → CG at end of beat.  
**After:** `show_cg_scene("au_modern_case1_club_exterior")` at label entry; narration and dialogue on the exterior shot.

### Case 2 — balcony night
**Before:** `scene black` + pause → balcony CG → dialogue → handclasp CG after HR line.  
**After:** Balcony CG at label entry (no black gap); handclasp CG before Kaoru's signatory-pressure speech.

## Text overflow — representative before/after

### Wrong Floor — contract rider explanation (`narrator_474`)
**Before:** One 728-character unvoiced paragraph.  
**After:** Six consecutive narrator lines (~80–95 chars each), same meaning, readable in the textbox.

### Case 1 — ballet barre (`toa` unvoiced)
**Before:** One 432-character French glossary block.  
**After:** Three `toa` lines at natural phrase breaks (plie/tendu; degage/rond de jambe; fondu through grand battement).

### Case 3 — People & Conduct (`narrator_478`, voiced)
**Before:** One 408-character voiced line.  
**After:** First sentence keeps `narrator_478.mp3`; two unvoiced continuation lines.

## Voice continuation fix (2026-06-07 follow-up)

**Root cause:** Ren'Py plays `voice` only on the immediately following say line. The overflow split left extra bare-string (or same-character) lines after a voiced first chunk; advancing to those lines was silent.

**Fix:** `scripts/merge_au_voice_continuations.py` folds continuations into the voiced say line (257 + 37 lines across five AU scripts). Manifests resynced via `sync_au_modern_manifests.py`. Three new IDs wired for lines that could not fold (`toa_474`, `kaoru_595`, `narrator_479`).

**Regen:** 187 IDs in `scripts/au_modern_voice_regen_ids.txt` (merged text + new lines). MP3s not yet regenerated for changed/new IDs.

## Lint

```
Ren'Py 8.5.3 lint — exit 0
Pre-existing: game/trailer.rpy pause '_trailer_runtime'; game/00auto-highlight.rpy unreachable (unchanged)
No new AU script errors.
```

## Voice regen queue

184 voice IDs with materially changed first-chunk text → `scripts/au_text_overflow_regen_ids.txt`
