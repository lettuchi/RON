#!/usr/bin/env python3
"""AU narration voicing (Task A) + Toa pronunciation re-fix (Task B), one pass.

Task A: wire the 7 newly-voiced AU narrator lines (narrator_472..478) into the
        narrator + performance manifests. Voice statements were already added to
        the .rpy files; game_text is extracted straight from them so it matches
        the on-screen line exactly. tts_text uses the AU house style
        ([dry] <first sentence>. [short pause] <rest>).

Task B: replace the prior wrong respelling "Toh-ah" with "Toe-uh" (target
        TOH-uh) in tts_text for every NARRATOR line whose game_text contains the
        name "Toa" (canon + AU). On-screen game_text stays "Toa". Character
        (Toa/Kaoru) lines are never touched. Existing emotion tags are kept.

Also syncs voice_v2_metadata_manifest.json (text/tts) and builds the combined
regen id list scripts/au_narration_and_toa_fix_ids.txt.
Idempotent; atomic writes.
"""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GAME = ROOT / "game"
SCRIPTS = ROOT / "scripts"
NARR_PATH = SCRIPTS / "narrator_manifest.json"
PERF_PATH = SCRIPTS / "voice_performance_manifest.json"
VM_PATH = SCRIPTS / "voice_manifest.json"
V2_PATH = SCRIPTS / "voice_v2_metadata_manifest.json"
IDS_OUT = SCRIPTS / "au_narration_and_toa_fix_ids.txt"

# Target pronunciation TOH-uh ("toe" + soft "uh"); clearest "toe + uh" respelling.
RESPELL = "Toe-uh"
WORD_TOA = re.compile(r"\bToa\b")
WIRE_NOTE = "au narration voicing 2026-06-05 (silent AU narrator line)"

NEW_IDS = [f"narrator_{n}" for n in range(472, 479)]  # 472..478

AU_FILES = [
    "au_modern_wrong_floor.rpy",
    "au_modern_case1_compliance.rpy",
    "au_modern_case2_island_weekend.rpy",
    "au_modern_case3_permits_hr.rpy",
    "au_modern_epilogue.rpy",
]

VOICE_RE = re.compile(r'voice\s+"audio/voice/(narrator_\d+)\.mp3"')
NARRATION_RE = re.compile(r'^\s+"(.*)"\s*$')


def normalize_toa(tts: str) -> str:
    """Undo any prior respelling (regular + non-breaking hyphen) back to 'Toa'."""
    return tts.replace("Toh-ah", "Toa").replace("Toh\u2011ah", "Toa")


def apply_respell(tts: str) -> str:
    return WORD_TOA.sub(RESPELL, tts)


def make_au_tts(game_text: str) -> str:
    """AU house style: leading [dry], [short pause] after the first sentence."""
    body = game_text.replace(". ", ". [short pause] ", 1)
    return apply_respell(f"[dry] {body}")


def extract_new_lines() -> dict[str, dict]:
    """Pull game_text/source for narrator_472..478 directly from the .rpy files."""
    found: dict[str, dict] = {}
    wanted = set(NEW_IDS)
    for name in AU_FILES:
        lines = (GAME / name).read_text(encoding="utf-8").splitlines()
        pending = None
        for i, line in enumerate(lines, start=1):
            m = VOICE_RE.search(line)
            if m:
                pending = (m.group(1), i)
                continue
            if pending:
                nm = NARRATION_RE.match(line)
                if nm:
                    vid, vln = pending
                    if vid in wanted and vid not in found:
                        found[vid] = {
                            "game_text": nm.group(1),
                            "source": f"game/{name}:{i}",
                        }
                pending = None
    missing = wanted - set(found)
    if missing:
        raise SystemExit(f"Could not extract new lines from .rpy: {sorted(missing)}")
    return found


def write_atomic(path: Path, text: str) -> None:
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(text, encoding="utf-8")
    tmp.replace(path)


def main() -> int:
    narr = json.loads(NARR_PATH.read_text(encoding="utf-8"))
    perf = json.loads(PERF_PATH.read_text(encoding="utf-8"))
    v2 = json.loads(V2_PATH.read_text(encoding="utf-8"))

    narr_by_id = {e["id"]: e for e in narr["lines"]}
    perf_by_id = {e["id"]: e for e in perf["entries"]}
    v2_by_id = {e["id"]: e for e in v2["entries"]}

    # ---- Task A: wire the 7 newly-voiced AU narrator lines ----
    new_lines = extract_new_lines()
    added = []
    for vid in NEW_IDS:
        info = new_lines[vid]
        game_text = info["game_text"]
        source = info["source"]
        tts_text = make_au_tts(game_text)

        if vid in narr_by_id:
            narr_by_id[vid]["text"] = game_text
            narr_by_id[vid]["source"] = source
            narr_by_id[vid]["character"] = "narrator"
        else:
            entry = {"id": vid, "character": "narrator", "text": game_text, "source": source}
            narr["lines"].append(entry)
            narr_by_id[vid] = entry

        if vid in perf_by_id:
            perf_by_id[vid]["game_text"] = game_text
            perf_by_id[vid]["tts_text"] = tts_text
            perf_by_id[vid]["source"] = source
        else:
            pentry = {
                "id": vid, "character": "narrator", "source": source,
                "game_text": game_text, "tts_text": tts_text,
                "tags_notes": WIRE_NOTE, "model_hint": "eleven_v3",
            }
            perf["entries"].append(pentry)
            perf_by_id[vid] = pentry
        added.append(vid)

    # ---- Task B: Toh-ah -> Toe-uh for narrator lines whose game_text has "Toa" ----
    perf_changed = []
    for vid, p in perf_by_id.items():
        if not vid.startswith("narrator_"):
            continue
        gt = p.get("game_text", "")
        tts = p.get("tts_text", "")
        if not (WORD_TOA.search(gt) or "Toh-ah" in tts or "Toh\u2011ah" in tts):
            continue
        after = apply_respell(normalize_toa(tts))
        if after != tts:
            p["tts_text"] = after
            perf_changed.append(vid)

    # mirror into v2 metadata manifest (text == tts); game_text stays "Toa"
    v2_changed = []
    for vid, e in v2_by_id.items():
        if not vid.startswith("narrator_"):
            continue
        gt = e.get("game_text", "")
        txt = e.get("text", "")
        if not (WORD_TOA.search(gt) or "Toh-ah" in txt or "Toh\u2011ah" in txt):
            continue
        after = apply_respell(normalize_toa(txt))
        if after != txt:
            e["text"] = after
            v2_changed.append(vid)

    # ---- counts / stats hygiene ----
    if "stats" in narr:
        narr["stats"]["line_count"] = len(narr["lines"])
    perf.setdefault("counts", {})
    perf["counts"]["total"] = len(perf["entries"])
    perf["counts"]["narrator"] = sum(
        1 for e in perf["entries"] if e["character"] == "narrator"
    )

    # ---- write back ----
    write_atomic(NARR_PATH, json.dumps(narr, ensure_ascii=False, indent=2) + "\n")
    write_atomic(PERF_PATH, json.dumps(perf, ensure_ascii=False, indent=2) + "\n")
    write_atomic(V2_PATH, json.dumps(v2, ensure_ascii=False, indent=2) + "\n")

    # ---- combined regen id list: new ids + every Task-B-changed narrator id ----
    def idnum(i: str) -> int:
        return int(re.search(r"(\d+)$", i).group(1))

    regen = list(NEW_IDS) + sorted(set(perf_changed), key=idnum)
    seen, ordered = set(), []
    for i in regen:
        if i not in seen:
            seen.add(i)
            ordered.append(i)
    IDS_OUT.write_text("\n".join(ordered) + "\n", encoding="utf-8")

    # ---- report ----
    canon = sorted([i for i in perf_changed if idnum(i) < 366], key=idnum)
    au = sorted([i for i in perf_changed if idnum(i) >= 366], key=idnum)
    print(f"Respelling chosen: 'Toa' -> '{RESPELL}'  (target TOH-uh)")
    print(f"Task A new narrator lines wired: {added}")
    print(f"Task B narrator tts respelled (perf): {len(perf_changed)}")
    print(f"  canon (<366): {len(canon)} -> {canon}")
    print(f"  au   (>=366): {len(au)} -> {au}")
    print(f"Task B narrator tts respelled (v2):   {len(v2_changed)}")
    print(f"Combined regen ids: {len(ordered)} -> {IDS_OUT.name}")
    print(f"  = {len(NEW_IDS)} new + {len(perf_changed)} respelled")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
