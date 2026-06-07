#!/usr/bin/env python3
"""Option D narrator finalization: sync 15 rewritten AU lines, add 3 new lines,
apply consistent Toa->Toh-ah respelling in tts_text (narrator lines only),
and build the regen id set. Idempotent; atomic writes."""
from __future__ import annotations
import json, re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
NARR_PATH = SCRIPTS / "narrator_manifest.json"
PERF_PATH = SCRIPTS / "voice_performance_manifest.json"
REGEN_IDS = SCRIPTS / "option_d_narrator_regen_ids.txt"
AU_PENDING = SCRIPTS / "au_emotion_tags_narrator_pending_ids.txt"

RESPELL = "Toh-ah"
WORD_TOA = re.compile(r"\bToa\b")

# ---- 15 rewritten AU narrator lines: id -> (new on-screen text, new tts_text) ----
# tts_text preserves the existing leading emotion tag and house-style [short pause].
# Toa stays bare here; respelling applied uniformly in a later pass.
REWRITES = {
    "narrator_366": (
        "Rain needles the harbor glass. Under the municipal licensing tower, the parking structure is a cathedral of dripping concrete, fluorescents buzzing while ferries cough diesel into the channel below. This is where Kakita Toa starts the morning she means to spend fixing her papers, and where Ryoko Port quietly decides it will not be that simple.",
        "[dry] Rain needles the harbor glass. [short pause] Under the municipal licensing tower, the parking structure is a cathedral of dripping concrete, fluorescents buzzing while ferries cough diesel into the channel below. This is where Kakita Toa starts the morning she means to spend fixing her papers, and where Ryoko Port quietly decides it will not be that simple.",
    ),
    "narrator_367": (
        "Ryoko Port keeps its appointments under fluorescent mercy and never apologizes for the weather. The municipal tower hums like a printer that learned to judge people. Floor fourteen B belongs to the Ryoko Port Arts Council, the board that decides which artists the port will license at all, and renewing the sponsorship she had let lapse was supposed to be the easy part of her morning.",
        "[dry] Ryoko Port keeps its appointments under fluorescent mercy and never apologizes for the weather. [short pause] The municipal tower hums like a printer that learned to judge people. Floor fourteen B belongs to the Ryoko Port Arts Council, the board that decides which artists the port will license at all, and renewing the sponsorship she had let lapse was supposed to be the easy part of her morning.",
    ),
    "narrator_376": (
        "When the hearing ends without praise, he hands her a studio key and a hallway that smells of floor wax and rain. The city rents the rehearsal room by the hour to applicants who need to prove, in a mirror, that they are more than a packet error. Prove it, and the deputy signs. That is the only fast track Ryoko Port actually keeps.",
        "[dry] When the hearing ends without praise, he hands her a studio key and a hallway that smells of floor wax and rain. [short pause] The city rents the rehearsal room by the hour to applicants who need to prove, in a mirror, that they are more than a packet error. Prove it, and the deputy signs. That is the only fast track Ryoko Port actually keeps.",
    ),
    "narrator_378": (
        "Building hour passes six. The official business is filed, the contract floor goes dark, and the public elevators sigh into standby one by one. Only the service lift still answers when he badges it, a dull metal box that does not appear on the map tourists photograph.",
        "[dry] Building hour passes six. [short pause] The official business is filed, the contract floor goes dark, and the public elevators sigh into standby one by one. Only the service lift still answers when he badges it, a dull metal box that does not appear on the map tourists photograph.",
    ),
    "narrator_380": (
        "She does not pretend, afterward, that nothing happened. Whatever the service lift was, every form that matters will still file it as sponsorship: after-hours rehearsal access, logged under the exclusive rider she signed with her eyes open. The seal stays professional on paper. The rest stays off the public record, which is exactly what that rider is for.",
        "[softly] She does not pretend, afterward, that nothing happened. [short pause] Whatever the service lift was, every form that matters will still file it as sponsorship: after-hours rehearsal access, logged under the exclusive rider she signed with her eyes open. The seal stays professional on paper. The rest stays off the public record, which is exactly what that rider is for.",
    ),
    "narrator_381": (
        "The next midday she comes back to the tower, not as a lost applicant this time but as a woman cooking thank-you curry in the municipal break room, which smells of roux and a little guilt. Fluorescents hum. Rain keeps filing itself against the window. Somewhere upstairs a printer jams and someone swears with the tenderness of a prayer.",
        "[tender] The next midday she comes back to the tower, not as a lost applicant this time but as a woman cooking thank-you curry in the municipal break room, which smells of roux and a little guilt. [short pause] Fluorescents hum. Rain keeps filing itself against the window. Somewhere upstairs a printer jams and someone swears with the tenderness of a prayer.",
    ),
    "narrator_386": (
        "The wellness corridor is a row of Council-licensed calm: massage studios, float tanks, candle rhetoric under one neon awning, every storefront holding an operating license his office issued. This is the first inspection her witness clause requires her to stand through. Deputy Director Kitsu Kaoru walks it like the queue is already behind him.",
        "[dry] The wellness corridor is a row of Council-licensed calm: massage studios, float tanks, candle rhetoric under one neon awning, every storefront holding an operating license his office issued. [short pause] This is the first inspection her witness clause requires her to stand through. Deputy Director Kitsu Kaoru walks it like the queue is already behind him.",
    ),
    "narrator_392": (
        "Her phone buzzes with a calendar ping she is not allowed to open during an active inspection. The portal only ever pings her with the next thing he has already filed.",
        "[dry] Her phone buzzes with a calendar ping she is not allowed to open during an active inspection. [short pause] The portal only ever pings her with the next thing he has already filed.",
    ),
    "narrator_467": (
        "Three business days after the wrong conference room, the sponsorship is signed and Ryoko Port still files rain against every window it owns. The fast track turned out to be a person. The person, it turns out, comes with errands.",
        "[dry] Three business days after the wrong conference room, the sponsorship is signed and Ryoko Port still files rain against every window it owns. [short pause] The fast track turned out to be a person. The person, it turns out, comes with errands.",
    ),
    "narrator_400": (
        "Saturday, and the harbor ferry schedule is a suggestion. Rain owns the channel. Kakita Toa owns a duffel bag and a Council sponsorship rider that still reads *not romance on letterhead*, the same exclusive rider that put her on the deputy's calendar in the first place.",
        "[dry] Saturday, and the harbor ferry schedule is a suggestion. [short pause] Rain owns the channel. Kakita Toa owns a duffel bag and a Council sponsorship rider that still reads *not romance on letterhead*, the same exclusive rider that put her on the deputy's calendar in the first place.",
    ),
    "narrator_415": (
        "Sunday night finds them on the balcony, the weekend almost filed, harbor lights smeared across the rail and a tablet open to the municipal portal where Tuesday is already waiting.",
        "[softly] Sunday night finds them on the balcony, the weekend almost filed, harbor lights smeared across the rail and a tablet open to the municipal portal where Tuesday is already waiting.",
    ),
    "narrator_419": (
        "The ferry horn answers like a stamp. Case two closes on salt air and a rider that held. Case three is already forming on the far shore, where a viral clip and an HR inbox will decide whether a deputy's signature counts as a favor.",
        "[dry] The ferry horn answers like a stamp. [short pause] Case two closes on salt air and a rider that held. Case three is already forming on the far shore, where a viral clip and an HR inbox will decide whether a deputy's signature counts as a favor.",
    ),
    "narrator_425": (
        "Tuesday in Ryoko Port opens the way audits open. Not with a knock, with a notification. Weeks after the harbor weekend, rain files itself against the licensing tower while a clip eleven seconds long teaches the whole channel a deputy director's voice.",
        "[dry] Tuesday in Ryoko Port opens the way audits open. [short pause] Not with a knock, with a notification. Weeks after the harbor weekend, rain files itself against the licensing tower while a clip eleven seconds long teaches the whole channel a deputy director's voice.",
    ),
    "narrator_439": (
        "She peels a clementine she did not ask permission to take, and the rain keeps its own minutes against the glass. Whichever way they filed it, the conflict now lives on the record instead of in the gossip, which is the one place the Council cannot use it against them. The clip will loop until the channel finds a louder one. The file will close quieter than it opened.",
        "[softly] She peels a clementine she did not ask permission to take, and the rain keeps its own minutes against the glass. [short pause] Whichever way they filed it, the conflict now lives on the record instead of in the gossip, which is the one place the Council cannot use it against them. The clip will loop until the channel finds a louder one. The file will close quieter than it opened.",
    ),
    "narrator_446": (
        "Months after People and Conduct closed the conflict-of-interest file on its own quiet terms, the harbor turned cold and the clip stopped being about her. Ryoko Port moves on the way a feed moves on. It finds a louder fool and forgets the quiet one.",
        "[dry] Months after People and Conduct closed the conflict-of-interest file on its own quiet terms, the harbor turned cold and the clip stopped being about her. [short pause] Ryoko Port moves on the way a feed moves on. It finds a louder fool and forgets the quiet one.",
    ),
}

# ---- 3 new narrator lines: id -> (source, game_text, tts_text) ----
NEW_LINES = {
    "narrator_469": (
        "game/au_modern_wrong_floor.rpy:45",
        "The public elevator lets her out on floor fourteen B, and on the wrong half of it. Intake, the counter where applicants take a number and wait their turn, is one wing over. Toa turns the other way, toward a glass door with a badge reader, and opens it without reading the plate.",
        "[dry] The public elevator lets her out on floor fourteen B, and on the wrong half of it. [short pause] Intake, the counter where applicants take a number and wait their turn, is one wing over. Toa turns the other way, toward a glass door with a badge reader, and opens it without reading the plate.",
    ),
    "narrator_470": (
        "game/au_modern_wrong_floor.rpy:218",
        "Back in the licensing office, the audition behind her, the sponsorship draft waits on his desk. His signature is ready. The only thing still hers to decide is which rider hangs off it.",
        "[dry] Back in the licensing office, the audition behind her, the sponsorship draft waits on his desk. [short pause] His signature is ready. The only thing still hers to decide is which rider hangs off it.",
    ),
    "narrator_471": (
        "game/au_modern_case1_compliance.rpy:75",
        "Inside the Velvet Lantern, the lobby smells of eucalyptus and money pretending to be mindfulness. Soft music hides the diesel and the ferries under panpipes. Toa raises her phone and waits to be told what counts as evidence.",
        "[dry] Inside the Velvet Lantern, the lobby smells of eucalyptus and money pretending to be mindfulness. [short pause] Soft music hides the diesel and the ferries under panpipes. Toa raises her phone and waits to be told what counts as evidence.",
    ),
}


def normalize_toa(tts: str) -> str:
    """Undo any prior respelling, then leave bare 'Toa' for uniform re-spelling."""
    tts = tts.replace("Toh-ah", "Toa").replace("Toh\u2011ah", "Toa")
    return tts


def apply_respell(tts: str) -> str:
    return WORD_TOA.sub(RESPELL, tts)


def write_atomic(path: Path, text: str) -> None:
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(text, encoding="utf-8")
    tmp.replace(path)


def main() -> int:
    narr = json.loads(NARR_PATH.read_text(encoding="utf-8"))
    perf = json.loads(PERF_PATH.read_text(encoding="utf-8"))
    narr_by_id = {e["id"]: e for e in narr["lines"]}
    perf_by_id = {e["id"]: e for e in perf["entries"]}

    # --- Task 1: sync 15 rewritten AU narrator lines ---
    synced = []
    for nid, (game_text, tts_text) in REWRITES.items():
        n = narr_by_id[nid]
        p = perf_by_id[nid]
        n["text"] = game_text
        p["game_text"] = game_text
        p["tts_text"] = tts_text  # respelling applied below
        synced.append(nid)

    # --- Task 2: add 3 new narrator lines to both manifests ---
    added = []
    for nid, (source, game_text, tts_text) in NEW_LINES.items():
        if nid not in narr_by_id:
            entry = {"id": nid, "character": "narrator", "text": game_text, "source": source}
            narr["lines"].append(entry)
            narr_by_id[nid] = entry
        else:
            narr_by_id[nid]["text"] = game_text
            narr_by_id[nid]["source"] = source
        if nid not in perf_by_id:
            pentry = {
                "id": nid, "character": "narrator", "source": source,
                "game_text": game_text, "tts_text": tts_text,
                "tags_notes": "option-d new narrator line", "model_hint": "eleven_v3",
            }
            perf["entries"].append(pentry)
            perf_by_id[nid] = pentry
        else:
            perf_by_id[nid]["game_text"] = game_text
            perf_by_id[nid]["tts_text"] = tts_text
        added.append(nid)

    # --- Task 3: uniform Toa->Toh-ah respelling in tts for narrator lines whose
    #             game_text contains the word "Toa". game_text/on-screen untouched. ---
    respelled = []
    for nid, p in perf_by_id.items():
        if not nid.startswith("narrator_"):
            continue
        gt = p.get("game_text", "")
        if not WORD_TOA.search(gt):
            continue
        before = p.get("tts_text", "")
        after = apply_respell(normalize_toa(before))
        p["tts_text"] = after
        respelled.append(nid)

    # --- counts hygiene ---
    n_narr = sum(1 for e in perf["entries"] if e["character"] == "narrator")
    perf.setdefault("counts", {})
    perf["counts"]["total"] = len(perf["entries"])
    perf["counts"]["narrator"] = n_narr
    narr_narr = sum(1 for e in narr["lines"] if e.get("character") == "narrator")
    if "stats" in narr:
        narr["stats"]["unique"] = narr_narr
        narr["stats"]["occurrences"] = narr_narr
        narr["stats"]["line_count"] = len(narr["lines"])

    # --- write back ---
    write_atomic(NARR_PATH, json.dumps(narr, ensure_ascii=False, indent=2) + "\n")
    write_atomic(PERF_PATH, json.dumps(perf, ensure_ascii=False, indent=2) + "\n")

    # --- Task 4: build regen id set ---
    au_ids = [ln.strip() for ln in AU_PENDING.read_text(encoding="utf-8").splitlines()
              if ln.strip() and not ln.startswith("#")]
    canon_respell = sorted(
        [nid for nid in respelled
         if int(re.search(r"(\d+)$", nid).group(1)) < 366],
        key=lambda i: int(re.search(r"(\d+)$", i).group(1)))
    regen = []
    for i in au_ids + canon_respell + list(NEW_LINES):
        if i not in regen:
            regen.append(i)
    regen_sorted = sorted(regen, key=lambda i: int(re.search(r"(\d+)$", i).group(1)))
    REGEN_IDS.write_text("\n".join(regen_sorted) + "\n", encoding="utf-8")

    # --- report ---
    def idnum(i):
        return int(re.search(r"(\d+)$", i).group(1))
    au_respell = sorted([i for i in respelled if idnum(i) >= 366], key=idnum)
    print(f"Respelling chosen: 'Toa' -> '{RESPELL}'")
    print(f"synced 15 rewrite lines: {len(synced)}")
    print(f"added new lines: {added}")
    print(f"narrator lines respelled (game_text has Toa): {len(respelled)}")
    print(f"  canon: {len(canon_respell)}  au+new: {len(au_respell)}")
    print(f"  canon ids: {canon_respell}")
    print(f"  au+new ids: {au_respell}")
    print(f"AU pending ids: {len(au_ids)}")
    print(f"regen set size: {len(regen_sorted)} -> {REGEN_IDS.name}")
    print(f"  = AU {len(au_ids)} + canon-respell {len(canon_respell)} + new {len(NEW_LINES)}")
    total_narr_canon = sum(1 for e in perf['entries']
                           if e['id'].startswith('narrator_')
                           and int(re.search(r'(\d+)$', e['id']).group(1)) < 366)
    print(f"canon narrator total: {total_narr_canon}  in regen: {len(canon_respell)}  "
          f"skipped (already-correct): {total_narr_canon - len(canon_respell)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
