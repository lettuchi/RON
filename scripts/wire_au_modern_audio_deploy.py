#!/usr/bin/env python3
"""Modern AU audio deploy wiring (2026-06-05).

One-shot helper mirroring scripts/wire_au_modern_*_voice.py. It:

  STEP 2  Re-IDs the reused-ID overlaps in au_modern_case1_compliance.rpy
          (narrator_384 -> narrator_467, narrator_385 -> narrator_468,
           kaoru_510 -> kaoru_592) so each distinct AU line owns a unique file.
          The Wrong Floor occurrences keep the canonical original IDs (their
          manifest game_text already matches Wrong Floor, so their existing
          mp3s stay correct).

  STEP 3  Inserts `voice "audio/voice/<id>.mp3"` above the 11 formerly-silent
          new lines, allocating fresh IDs above the true per-speaker maxima
          (toa_464 / kaoru_591 / narrator_466).

  MANIFESTS  Upserts voice_manifest / narrator_manifest / voice_performance_manifest
             entries for all 14 newly-minted IDs (game_text + tagged tts_text).

  STEP 4  Re-syncs the 22 changed existing IDs (au_modern_rewrite_regen_ids.txt)
          game_text + tts_text from the current .rpy across voice_manifest,
          narrator_manifest, voice_performance_manifest, voice_v2_metadata_manifest.

  Writes scripts/au_modern_audio_deploy_ids.txt = [11 new] + [3 step2] + [22 changed].

Idempotent: re-running skips voice lines / manifest rows already present.
"""
from __future__ import annotations

import importlib.util
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GAME = ROOT / "game"
SCRIPTS = ROOT / "scripts"

VOICE_RE = re.compile(r'voice\s+"audio/voice/(\w+)\.mp3"')
DIALOGUE_RE = re.compile(r'^(\s*)(kaoru|toa|narrator)\s+"(.*)"\s*$')
NARRATION_RE = re.compile(r'^(\s+)"(.*)"\s*$')

WIRE_NOTE = "au modern audio deploy 2026-06-05"

# -- STEP 3: 11 new lines.  (file, anchor say-text, new_id, character) --
NEW_LINES = [
    ("au_modern_wrong_floor.rpy",
     "The fast track your letter promised is not a faster queue. It is a signature. A Council sponsorship is only valid once a deputy director signs for the applicant. I am the deputy director on this floor. That is the line your transfer letter left out.",
     "kaoru_593", "kaoru"),
    ("au_modern_wrong_floor.rpy",
     "So the fast track is a person. And I opened his door by accident, on camera.",
     "toa_465", "toa"),
    ("au_modern_wrong_floor.rpy",
     "If I sign your sponsorship, I swear to the Council that you are an artist and not a story about fraud waiting to happen. The board takes my word because I do not give it cheaply. So give me an artist to swear to.",
     "kaoru_594", "kaoru"),
    ("au_modern_wrong_floor.rpy",
     "And here I thought I was auditioning for a permit. I am auditioning for your signature.",
     "toa_466", "toa"),
    ("au_modern_wrong_floor.rpy",
     "I understand paperwork. I am very good at paperwork when someone explains the boxes. *Direct deputy review.* I read that line three times, and my pulse did something unprofessional each time.",
     "toa_467", "toa"),
    ("au_modern_case1_compliance.rpy",
     "Favoritism insurance. I document your inspections so the Council can see you are not handing permits to artists you happen to like. The irony writes itself. I am simply not allowed to laugh about it on the record.",
     "toa_468", "toa"),
    ("au_modern_case1_compliance.rpy",
     "Everything you offer is a calendar invite. The inspection, the weekend, possibly the rest of my life. I am starting to suspect the calendar is how you say the things you will not put in a sentence.",
     "toa_469", "toa"),
    ("au_modern_case2_island_weekend.rpy",
     "Witness posture, even here. I document the want and I do not perform it where a listing photo could see. My clause never asked me not to want him. It only forbade me to put it on letterhead.",
     "toa_470", "toa"),
    ("au_modern_case2_island_weekend.rpy",
     "Dependent. Signatory. Two boxes on one form, and a camera that turned them into a couple. I did not understand that my right to dance in this port was also your liability until you said it out loud on a balcony.",
     "toa_471", "toa"),
    ("au_modern_case3_permits_hr.rpy",
     "And if the Council decides the leverage looks like a favor, they can suspend the sponsorship, or revoke it, or hand my file to a deputy who never met me. My whole right to dance in this port is one sentence you signed. I keep forgetting that until a fishbowl reminds me.",
     "toa_472", "toa"),
    ("au_modern_epilogue.rpy",
     "A standing item. The Council files those the way it files rent and rain, the recurring things it expects to keep paying attention to. I have been a great many classifications in this building. That is the first one I would frame.",
     "toa_473", "toa"),
]

# -- STEP 2: reused-ID overlap rewires in case1 (old_id -> new_id) --
REWIRES = [
    ("au_modern_case1_compliance.rpy", "narrator_384", "narrator_467"),
    ("au_modern_case1_compliance.rpy", "narrator_385", "narrator_468"),
    ("au_modern_case1_compliance.rpy", "kaoru_510", "kaoru_592"),
]

NEW_IDS_ORDER = [nid for (_f, _t, nid, _c) in NEW_LINES] + [nid for (_f, _o, nid) in REWIRES]

AU_FILES = [
    "au_modern_wrong_floor.rpy",
    "au_modern_case1_compliance.rpy",
    "au_modern_case2_island_weekend.rpy",
    "au_modern_case3_permits_hr.rpy",
    "au_modern_epilogue.rpy",
]


def load_make_tts():
    spec = importlib.util.spec_from_file_location(
        "gen_case1", SCRIPTS / "generate_case1_sidecar.py"
    )
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.make_tts


def apply_rpy_edits() -> None:
    # STEP 3: insert voice lines above new say-lines.
    for fn, anchor, vid, char in NEW_LINES:
        p = GAME / fn
        lines = p.read_text(encoding="utf-8").splitlines()
        out: list[str] = []
        done = False
        for i, line in enumerate(lines):
            m = DIALOGUE_RE.match(line)
            if not done and m and m.group(2) == char and m.group(3) == anchor:
                indent = m.group(1)
                # Skip if a voice line already precedes it.
                if out and VOICE_RE.search(out[-1]):
                    out.append(line)
                    done = True
                    continue
                out.append(f'{indent}voice "audio/voice/{vid}.mp3"')
                out.append(line)
                done = True
            else:
                out.append(line)
        if not done:
            raise SystemExit(f"NEW LINE anchor not found: {fn} :: {vid} :: {anchor[:50]!r}")
        p.write_text("\n".join(out) + "\n", encoding="utf-8")

    # STEP 2: rewire duplicate IDs in case1.
    for fn, old_id, new_id in REWIRES:
        p = GAME / fn
        text = p.read_text(encoding="utf-8")
        needle = f'voice "audio/voice/{old_id}.mp3"'
        repl = f'voice "audio/voice/{new_id}.mp3"'
        if needle not in text:
            if repl in text:
                continue  # already rewired
            raise SystemExit(f"REWIRE needle not found: {fn} :: {needle}")
        if text.count(needle) != 1:
            raise SystemExit(f"REWIRE needle not unique ({text.count(needle)}x): {fn} :: {needle}")
        p.write_text(text.replace(needle, repl), encoding="utf-8")


def extract_au_rows() -> dict[str, dict]:
    """id -> {character, game_text, file, line} from current AU rpy state."""
    rows: dict[str, dict] = {}
    for fn in AU_FILES:
        p = GAME / fn
        lines = p.read_text(encoding="utf-8").splitlines()
        pending = None
        for i, line in enumerate(lines, start=1):
            vm = VOICE_RE.search(line)
            if vm:
                pending = vm.group(1)
                continue
            if not pending:
                continue
            dm = DIALOGUE_RE.match(line)
            if dm:
                char, text = dm.group(2), dm.group(3)
                prefix = pending.rsplit("_", 1)[0]
                if prefix != char:
                    raise SystemExit(f"ID/char mismatch {fn}:{i}: {pending} vs {char}")
                rows[pending] = {"character": char, "game_text": text,
                                 "file": f"game/{fn}", "line": i}
                pending = None
                continue
            nm = NARRATION_RE.match(line)
            if nm and pending.startswith("narrator_"):
                rows[pending] = {"character": "narrator", "game_text": nm.group(2),
                                 "file": f"game/{fn}", "line": i}
                pending = None
    return rows


def main() -> None:
    make_tts = load_make_tts()
    apply_rpy_edits()
    rows = extract_au_rows()

    changed_ids = [
        ln.strip()
        for ln in (SCRIPTS / "au_modern_rewrite_regen_ids.txt").read_text(encoding="utf-8").splitlines()
        if ln.strip() and not ln.startswith("#")
    ]

    vm_path = SCRIPTS / "voice_manifest.json"
    nm_path = SCRIPTS / "narrator_manifest.json"
    pm_path = SCRIPTS / "voice_performance_manifest.json"
    v2_path = SCRIPTS / "voice_v2_metadata_manifest.json"

    vm = json.loads(vm_path.read_text(encoding="utf-8"))
    nm = json.loads(nm_path.read_text(encoding="utf-8"))
    pm = json.loads(pm_path.read_text(encoding="utf-8"))
    v2 = json.loads(v2_path.read_text(encoding="utf-8"))

    vm_by = {r["id"]: r for r in vm["lines"]}
    nm_by = {r["id"]: r for r in nm["lines"]}
    pm_by = {e["id"]: e for e in pm["entries"]}
    v2_by = {e["id"]: e for e in v2.get("entries", [])}

    # --- Newly minted IDs (14): upsert manifest rows from AU rpy text. ---
    added = 0
    for vid in NEW_IDS_ORDER:
        r = rows.get(vid)
        if r is None:
            raise SystemExit(f"new id {vid} not found in AU rpy after wiring")
        char, game_text = r["character"], r["game_text"]
        tts = make_tts(char, vid, game_text)
        if vid not in vm_by:
            vm["lines"].append({"id": vid, "character": char, "text": game_text})
            vm_by[vid] = vm["lines"][-1]
            added += 1
        if char == "narrator" and vid not in nm_by:
            nm["lines"].append({"id": vid, "text": game_text, "source": f"{r['file']}:{r['line']}"})
            nm_by[vid] = nm["lines"][-1]
        if vid not in pm_by:
            pm["entries"].append({
                "id": vid, "character": char, "source": f"{r['file']}:{r['line']}",
                "game_text": game_text, "tts_text": tts,
                "tags_notes": WIRE_NOTE, "model_hint": "eleven_v3",
            })
            pm_by[vid] = pm["entries"][-1]

    # --- Sync the 22 changed IDs (game_text + tts_text) across all manifests. ---
    synced = []
    for vid in changed_ids:
        r = rows.get(vid)
        if r is None:
            raise SystemExit(f"changed id {vid} not found in AU rpy")
        char, new_text = r["character"], r["game_text"]
        new_tts = make_tts(char, vid, new_text)
        touched = []
        if vid in vm_by and vm_by[vid].get("text") != new_text:
            vm_by[vid]["text"] = new_text
            touched.append("vm")
        if vid in nm_by and nm_by[vid].get("text") != new_text:
            nm_by[vid]["text"] = new_text
            touched.append("nm")
        if vid in pm_by:
            e = pm_by[vid]
            if e.get("game_text") != new_text or e.get("tts_text") != new_tts:
                e["game_text"] = new_text
                e["tts_text"] = new_tts
                e["source"] = f"{r['file']}:{r['line']}"
                touched.append("pm")
        if vid in v2_by:
            e = v2_by[vid]
            if e.get("game_text") != new_text or e.get("text") != new_tts:
                e["game_text"] = new_text
                e["text"] = new_tts
                touched.append("v2")
        if touched:
            synced.append((vid, touched))

    vm_path.write_text(json.dumps(vm, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    nm_path.write_text(json.dumps(nm, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    pm_path.write_text(json.dumps(pm, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    v2_path.write_text(json.dumps(v2, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    # --- Combined deploy ID list: [11 new] + [3 step2] + [22 changed]. ---
    deploy = NEW_IDS_ORDER + changed_ids
    seen = set()
    deploy_unique = []
    for d in deploy:
        if d not in seen:
            seen.add(d)
            deploy_unique.append(d)
    ids_path = SCRIPTS / "au_modern_audio_deploy_ids.txt"
    ids_path.write_text("\n".join(deploy_unique) + "\n", encoding="utf-8")

    print(f"new IDs minted: {len(NEW_IDS_ORDER)} ({added} new voice_manifest rows)")
    print(f"  {NEW_IDS_ORDER}")
    print(f"changed IDs synced: {len(synced)} / {len(changed_ids)}")
    for vid, t in synced:
        print(f"    {vid}: {'+'.join(t)}")
    print(f"deploy list ({len(deploy_unique)}): {ids_path}")


if __name__ == "__main__":
    main()
