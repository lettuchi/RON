from pathlib import Path
p = Path(__file__).resolve().parents[1] / "docs" / "missing-audio-audit-2026-06-04.md"
t = p.read_text(encoding="utf-8")
t = t.replace("Missing audio audit ? 2026-06-04", "Missing audio audit — 2026-06-04")
t = t.replace('voice "audio/voice/?"', 'voice "audio/voice/…"')
t = t.replace("rpy ? no legacy", "rpy → no legacy")
t = t.replace("**Never generated** ?", "**Never generated** —")
t = t.replace("**v2 not promoted** ?", "**v2 not promoted** —")
t = t.replace("**Unwired / false positives in rpy** ?", "**Unwired / false positives in rpy** —")
t = t.replace("Promote v2 ? legacy", "Promote v2 → legacy")
p.write_text(t, encoding="utf-8")
print("ok")
