import json
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parents[1]
PERF = ROOT / "scripts" / "voice_performance_manifest.json"
TAGGING = ROOT / "scripts" / "performance_tagging.py"
IDS = ROOT / "scripts" / "bow_disambig_ids.txt"
DOC = ROOT / "docs" / "voice-performance-manifest.md"
O = json.loads((ROOT / "scripts" / "bow_overrides.json").read_text(encoding="utf-8"))

data = json.loads(PERF.read_text(encoding="utf-8"))
by_id = {e["id"]: e for e in data["entries"]}
for vid, tts in O.items():
    e = by_id[vid]
    e["tts_text"] = tts
    note = "bow disambiguation tts"
    notes = e.get("tags_notes") or ""
    if note not in notes:
        e["tags_notes"] = (notes + "; " if notes else "") + note
    e["model_hint"] = "eleven_v3"

data["entries"] = sorted(by_id.values(), key=lambda x: x["id"])
PERF.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
IDS.write_text("\n".join(sorted(O)) + "\n", encoding="utf-8")

text = TAGGING.read_text(encoding="utf-8")
bow_block = "\n    # --- Bow disambiguation (courtesy bow / bending, not ribbon or archery) ---\n"
for vid in sorted(O):
    tts = O[vid].replace("\\", "\\\\").replace('"', '\\"')
    bow_block += f'    "{vid}": "{tts}",\n'

if "# --- Bow disambiguation" in text:
    text = re.sub(
        r"\n    # --- Bow disambiguation.*?(\n\})\n\n\ndef tag_toa",
        bow_block + r"\1\n\ndef tag_toa",
        text,
        count=1,
        flags=re.S,
    )
else:
    old = (
        '    "narrator_180": "[whispers] Rocking hull. Gunwales under his palms when the boat '
        "threatens to tip. *Good girl* breathed against her hair — implied, never filed, "
        'hunger without ledger line.",\n}'
    )
    if old not in text:
        raise SystemExit("anchor missing in performance_tagging.py")
    text = text.replace(old, old[:-2] + bow_block + "}")

TAGGING.write_text(text, encoding="utf-8")

line = (
    "- **2026-06-03** — Courtesy-bow TTS disambiguation batch "
    "(`scripts/bow_disambig_ids.txt`): "
    + ", ".join(sorted(O))
    + ".\n"
)
doc = DOC.read_text(encoding="utf-8")
if "Courtesy-bow TTS disambiguation" not in doc:
    if "## Changelog" in doc:
        doc = doc.replace("## Changelog\n", "## Changelog\n\n" + line)
    else:
        doc = doc.rstrip() + "\n\n## Changelog\n\n" + line
    DOC.write_text(doc, encoding="utf-8")

print("applied", len(O))