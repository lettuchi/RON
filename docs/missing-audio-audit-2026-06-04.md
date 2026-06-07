# Missing audio audit — 2026-06-04

Automated scan of `game/**/*.rpy` for `voice "audio/voice/…"` (comment lines excluded), compared to legacy playback path `game/audio/voice/{id}.mp3`, manifests, and v2 folders.

## Totals

| Metric | Count |
|--------|------:|
| Voice IDs referenced in `.rpy` | 967 |
| Legacy MP3 files on disk | 1013 |
| v2 MP3 files (all dated folders) | 1012 |
| **Missing at audit start** (rpy → no legacy file) | **15** |
| Missing after this run | **0** |
| Manifest line IDs (`voice_manifest` + `narrator_manifest`) | 1010 |
| Manifest IDs with no legacy file (post-fix) | 0 |

## Missing by chapter / label (pre-fix)

| Chapter (heuristic) | Missing IDs | Count |
|---------------------|-------------|------:|
| case5 | `kaoru_368`, `kaoru_371`, `kaoru_372`, `kaoru_373`, `narrator_286`, `narrator_287`, `narrator_290`, `narrator_291`, `narrator_292`, `narrator_293`, `narrator_294`, `narrator_295`, `narrator_296`, `toa_305`, `toa_307` | 15 |

### Label hints (pre-fix)

| ID | First label context |
|----|---------------------|
| `kaoru_368` | `case_endings.rpy` / `gameover_case5_chained` |
| `kaoru_371` | `case_endings.rpy` / `gameover_case5_quarter_cage` |
| `kaoru_372` | `case_endings.rpy` / `gameover_case5_chained` |
| `kaoru_373` | `case_endings.rpy` / `gameover_case5_quarter_cage` |
| `narrator_286` | `case_endings.rpy` / `gameover_case5_chained` |
| `narrator_287` | `case_endings.rpy` / `gameover_case5_quarter_cage` |
| `narrator_290` | `case_endings.rpy` / `gameover_case5_chained` |
| `narrator_291` | `case_endings.rpy` / `gameover_case5_chained` |
| `narrator_292` | `case_endings.rpy` / `gameover_case5_chained` |
| `narrator_293` | `case_endings.rpy` / `gameover_case5_quarter_cage` |
| `narrator_294` | `case_endings.rpy` / `gameover_case5_quarter_cage` |
| `narrator_295` | `case_endings.rpy` / `gameover_case5_quarter_cage` |
| `narrator_296` | `case_endings.rpy` / `gameover_case5_quarter_cage` |
| `toa_305` | `case_endings.rpy` / `gameover_case5_chained` |
| `toa_307` | `case_endings.rpy` / `gameover_case5_quarter_cage` |

## Root causes (top 3)

1. **Never generated** — All 15 gaps were Case 5 / late investigation lines present in manifests and `voice_performance_manifest.json` but with no MP3 in legacy or any v2 folder before this run.
2. **v2 not promoted** — Not applicable this run (0 missing IDs had v2-only copies). A bulk promote earlier today (`scripts/promote_v2_legacy_2026-06-04.log`, 886 files) already synced most staged regen output.
3. **Unwired / false positives in rpy** — One comment-only placeholder `narrator_NNN` in `mute_narrator.rpy` matched a naive scan but is **not** active script. **1** wired ID (`narrator_287` etc.) was in manifest; **43** manifest IDs are still unused by current `.rpy` (branch leftovers / deduped lines).

## Fixes applied this run

| Action | Count |
|--------|------:|
| ElevenLabs regen (`eleven_v3`, missing-only) | 15 |
| Promote v2 → legacy (`eve-donovan-2026-06-04`) | 15 |
| Legacy backups (replaced files) | 0 |

Commands run:

```powershell
python scripts/regenerate_voice_with_metadata.py --check
python scripts/regenerate_voice_with_metadata.py --model eleven_v3 --ids @scripts/missing_audio_audit_ids.txt
# promote: scripts/missing_audio_promote_2026-06-04.log
```

Logs: `scripts/missing_audio_regen_2026-06-04.log`, `scripts/missing_audio_promote_2026-06-04.log`.

## Remaining work

- **Runtime voice lines:** none missing for wired `voice "audio/voice/…"` statements.
- **Optional cleanup:** 43 manifest entries are not referenced in current `.rpy` (no player impact unless re-wired).
- **Ren'Py lint:** SDK not found in repo; no automated lint run.

Recommended next command if new script lines land:

```powershell
python scripts/regenerate_voice_with_metadata.py --check
python scripts/regenerate_voice_with_metadata.py --model eleven_v3 --ids @scripts/missing_audio_audit_ids.txt
```

(Re-run the audit snippet in `scripts/_audit_voice_result.json` or regenerate `missing_audio_audit_ids.txt` after editing `.rpy`.)

## Reference files

| File | Notes |
|------|-------|
| `scripts/missing_voice_ids.txt` | Empty (0 bytes) |
| `scripts/missing_voice_v2_ids.txt` | Not present |
| `scripts/missing_audio_audit_ids.txt` | 15 IDs used for this regen batch |
| `scripts/_audit_voice_result.json` | Machine-readable pre-fix audit |
