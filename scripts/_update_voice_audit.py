from pathlib import Path
import re
p = Path('docs/voice-coverage-audit-2026-06-04.md')
text = p.read_text(encoding='utf-8')

# count executable voice lines
voice_count = 0
for rpy in Path('game').rglob('*.rpy'):
    for line in rpy.read_text(encoding='utf-8').splitlines():
        s = line.strip()
        if s.startswith('#'): continue
        if 'voice "audio/voice/' in line:
            voice_count += 1

case1_wired = 0
for rel in ['game/case1_companion.rpy','game/case1_investigation.rpy']:
    t = Path(rel).read_text(encoding='utf-8')
    for m in re.finditer(r'voice "audio/voice/(\w+)\.mp3"', t):
        vid = m.group(1)
        pre = vid.split('_')[0]
        num = int(vid.split('_')[1])
        if pre in ('toa','kaoru') and num >= 319:
            case1_wired += 1
# unique high band
ids=set()
for rel in ['game/case1_companion.rpy','game/case1_investigation.rpy']:
    for m in re.finditer(r'voice "audio/voice/(\w+)\.mp3"', Path(rel).read_text(encoding='utf-8')):
        vid = m.group(1)
        pre = vid.split('_')[0]
        num = int(vid.split('_')[1])
        if pre in ('toa','kaoru') and num >= 319:
            ids.add(vid)

append = f"""

---

## Case Zero + Case 1 unwired pass (2026-06-04 evening)

| Item | Result |
|------|--------|
| Case Zero voice IDs (`narrator_312`-`365`, `kaoru_387`-`425`) | **93/93** legacy MP3s on disk |
| Case Zero regen (this session) | **6** newly synthesized in v2; **87** already in v2; **93** promoted to legacy |
| Case 1 menu-branch + merge-path wiring | **{len(ids)}** unique `toa_319+` / `kaoru_426+` IDs wired in `case1_companion.rpy` + `case1_investigation.rpy` |
| Case 1 regen (this session) | **2** newly synthesized (`toa_338`, `kaoru_449`); **42** reused existing v2; **44** promoted to legacy |
| Executable `voice` lines (`.rpy`, recount) | **{voice_count}** |
| Case 1 menu branches with unvoiced dialogue (companion + investigation) | **0** |

Logs: `scripts/case_zero_voice_regen_2026-06-04.log`, `scripts/case1_unwired_voice_regen_2026-06-04.log`.

Case Zero CGs: `cg-case-zero-redacted-docket.png`, `cg-case-zero-rain-alley-door.png` (NovelAI 1536x1024; GenerateImage unavailable in automation — NovelAI fallback).
"""
if 'Case Zero + Case 1 unwired pass' not in text:
    text = text.rstrip() + append + '\n'
    # update executive summary gap line
    text = text.replace(
        '**17 investigation/companion menu branches** contain character/narration lines with **no** preceding `voice` statement',
        '**Case 1 companion/investigation menu branches** are wired (0 unvoiced branch lines remaining in those files)'
    )
    text = text.replace(
        '| Regeneration run (`--ids @voice_coverage_missing_ids.txt`) | **Skipped** (empty list) |',
        '| Case Zero + Case 1 unwired regen | **Done** (see evening pass below) |'
    )
    p.write_text(text, encoding='utf-8')
    print('updated audit', len(ids))
else:
    print('audit already updated')
