from pathlib import Path
p = Path('docs/voice-coverage-audit-2026-06-04.md')
t = p.read_text(encoding='utf-8')
t = t.replace('- New IDs: \toa_319-\toa_337, kaoru_426-kaoru_448 (see scripts/case1_unwired_voice_ids.txt).', '- New IDs: `toa_319`-`toa_338`, `kaoru_426`-`kaoru_449` (see `scripts/case1_unwired_voice_ids.txt`).')
t = t.replace('- Wired **42** post-choice / merge-path lines in case1_companion.rpy and case1_investigation.rpy (15 menu branches: sponsorship prelude, registry, witness, ledger, barge).', '- Wired **44** post-choice / merge-path lines in `case1_companion.rpy` and `case1_investigation.rpy` (menu branches + merge path at investigation witness exit).')
t = t.replace('- game/kaoru_pro_prologue.rpy: not present (Case Zero prologue not in tree).', '- `game/kaoru_pro_prologue.rpy`: **93/93** Case Zero voice statements present; legacy MP3s on disk.')
p.write_text(t, encoding='utf-8')
print('fixed audit typos')
