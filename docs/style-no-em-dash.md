# No em dashes in script or TTS

**Project rule:** Do not use the Unicode em dash (`—`, U+2014) in player-visible copy or voice manifests.

## Where this applies

- `game/**/*.rpy` — dialogue, narrator strings, menu labels, gallery titles, and any other player-visible text
- `scripts/voice_performance_manifest.json` — `game_text` and `tts_text`
- `scripts/narrator_manifest.json` and `scripts/voice_manifest.json` when they mirror game lines

## Use instead

| Intent | Punctuation |
|--------|-------------|
| Parenthetical break | Comma or parentheses |
| Dramatic pause | Period, ellipsis (`...`), or comma |
| Elaboration / appositive | Colon or semicolon |
| Contrast (`not`, `but`, `or`) | Comma |
| Interrupted speech | Ellipsis (`...`) |
| Section / case titles (comments, gallery) | Colon (`Case 1: The Canal Investigation`) |
| Letter stutter | ASCII hyphen (`I-I`, not em dash) |

## TTS notes

- When editing `tts_text`, do **not** break ElevenLabs `[audio tags]` — replace em dashes only in spoken prose outside brackets.
- After changing `game_text` in `.rpy`, run `scripts/sync_voice_performance_manifest.py` so manifests stay aligned.

## En dash (`–`, U+2013)

En dashes are allowed only for **non-prose** ranges (numeric spans, coordinate notes in comments, e.g. `Cases 1–3`, `x578–1020`). Do not use en dashes as sentence punctuation in dialogue.

## History

- 2026-06-04: Removed all em dashes from game script and voice manifests; backup at `scripts/versions/voice_performance_manifest-pre-no-emdash-2026-06-04.json` and `game/versions/no-emdash-2026-06-04/`.
