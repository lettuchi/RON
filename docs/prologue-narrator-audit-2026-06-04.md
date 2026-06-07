# Prologue narrator voice audit (2026-06-04)

## Summary

| Metric | Count |
|--------|------:|
| Voice-tagged narrator lines audited (`prologue.rpy` + `prologue_canon_encounter.rpy`) | 63 |
| **Mismatches found** | **12** |
| **Mismatches fixed** | **12** (manifest only) |
| `prologue.rpy` lines OK before/after (001–038, 183–187, 206–213) | 51 |
| Miswired voice→wrong speaker | 0 |
| Manifest missing IDs | 0 |

## Root cause

A bad-end sync overwrote **`narrator_040`–`narrator_051`** in `scripts/voice_performance_manifest.json` with Kaoru-pursuit / desk-violence copy (the same lines correctly assigned to **`narrator_206`–`narrator_213`** and **`narrator_183`–`narrator_187`** in `prologue.rpy`).

Canon intimate narration still uses **`narrator_040`–`narrator_051`** in `game/prologue_canon_encounter.rpy`. Duplicate canon rows **`narrator_052`–`narrator_063`** had the right `game_text` / `tts_text` but are **not** wired in the canon script (Case 1 uses those IDs in `.rpy` — separate ID collision; not changed in this pass).

**Player impact:** On the canon “Unless?” path, on-screen canon lines played **bad-end TTS** (and manifest-driven regen targeted the wrong words for `narrator_040`–`051`).

## Fixes applied

### `scripts/voice_performance_manifest.json`

- Restored **`narrator_040`–`narrator_051`** `game_text`, `tts_text`, `source`, and tag notes from the duplicate canon entries **`narrator_052`–`narrator_063`**.
- **Backup (pre-fix snapshot):** `scripts/versions/voice_performance_manifest-pre-narrator-audit-2026-06-04.json`
- **No `.rpy` edits** — script dialogue was already correct.

### Files not changed

- `game/prologue.rpy` — already matched manifest for all 51 narrator IDs.
- Toa/Kaoru lines — untouched.
- `game/case1_companion.rpy` / `game/case1_investigation.rpy` — noted below; out of scope.

## Per-ID fix log (canon encounter)

| ID | Script file (correct display text) | Was in manifest (wrong) |
|----|-----------------------------------|-------------------------|
| `narrator_040` | The latch catches. Lamplight thins… | Bad-end gate chase (`narrator_212` text) |
| `narrator_041` | His hand finds her wrist — invitation… | Gate bars / watchmen (`211`) |
| `narrator_042` | Negotiation dissolves into breath… | Wrist grip / clerk (`210`) |
| `narrator_043` | She loosens the gold outer robe… | Corridor haul (`209`) |
| `narrator_044` | Maroon silk slips from one shoulder… | Custody chit wax (`208`) |
| `narrator_045` | They fold onto the cushion… | Guest-room mat (`207`) |
| `narrator_046` | She means it. He answers without words… | Office throw (`206`) |
| `narrator_047` | What followed stayed between petitioner… | Mat rushes up (`187`) |
| `narrator_048` | When breath and silk found order again… | Arms do not answer (`186`) |
| `narrator_049` | He draws the renewal from her permit book… | Office door seals (`185`) |
| `narrator_050` | Stamp. One crisp press… | Clerks hear nothing (`184`) |
| `narrator_051` | She holds the paper to the lamp. Three days hence… | Ledger / survive the night (`183`) |

## Optional voice regen (`narrator_040`–`narrator_051`)

Regenerate **only if** playback still sounds like bad-end narration after manifest fix:

```
narrator_040 narrator_041 narrator_042 narrator_043 narrator_044 narrator_045
narrator_046 narrator_047 narrator_048 narrator_049 narrator_050 narrator_051
```

`scripts/voice_v2_metadata_manifest.json` still lists bad-end `tts_text` for `narrator_040` (2026-06-04 batch) — regen should follow updated performance manifest.

**Do not** copy `narrator_052`–`063` MP3s over `040`–`051` without checking Case 1: those IDs are wired to different dialogue in `case1_companion.rpy` / `case1_investigation.rpy`.

## Related findings (not fixed here)

| Issue | Notes |
|-------|--------|
| **`narrator_039`** | `epilogue_rain_gameover.rpy` displays canal-district rain text; manifest still has bad-end pursuit copy (duplicate of `narrator_213`). Correct rain line exists as **`narrator_121`**. |
| **`narrator_052`–`063` manifest vs Case 1 script** | Manifest rows still describe canon encounter; Case 1 `.rpy` uses these IDs for companion/investigation morning lines (`narrator_064+` in manifest). Worth a follow-up ID remap or script rewire. |

## Verification

Re-run:

```bash
python scripts/_audit_prologue_narrator.py
```

Expected: **0 mismatches**, **51/51** OK for `prologue.rpy`, **12/12** OK for canon encounter.

## Reference

- Prologue narrator ID list: `scripts/prologue_voice_ids.txt`
- Audit helper: `scripts/_audit_prologue_narrator.py`
