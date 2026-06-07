#!/usr/bin/env python3
"""Replace Unicode em dashes (U+2014) in game scripts and voice manifests."""
from __future__ import annotations

import json
import re
import shutil
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EM = "\u2014"
DATE = date.today().isoformat()

GAME_GLOB = ROOT / "game"
SKIP_PARTS = {"versions", "backups"}

MANIFESTS = [
    ROOT / "scripts" / "voice_performance_manifest.json",
    ROOT / "scripts" / "narrator_manifest.json",
    ROOT / "scripts" / "voice_manifest.json",
]

# Ordered (pattern, replacement) for spaced em dash — most specific first.
SPACED_RULES: list[tuple[str, str]] = [
    (r" — not ", ", not "),
    (r" — nor ", ", nor "),
    (r" — or ", ", or "),
    (r" — and ", ", and "),
    (r" — but ", ", but "),
    (r" — if ", ", if "),
    (r" — do not ", ". Do not "),
    (r" — observe\.", ", observe."),
    (r" — briefly\.", ", briefly."),
    (r" — starting with", ", starting with"),
    (r" — once for", ", once for"),
    (r" — day or night", ", day or night"),
    (r" — wrong week", "; wrong week"),
    (r" — noble quarter", ": noble quarter"),
    (r" — official gifts", ": official gifts"),
    (r" — implied,", "; implied,"),
    (r" — close enough", ", close enough"),
    (r" — escort,", ", escort,"),
    (r" — never filed", "; never filed"),
    (r" — not ahead", ", not ahead"),
    (r" — not comfort", ", not comfort"),
    (r" — not a ", ", not a "),
    (r" — not the ", ", not the "),
    (r" — not your", ", not your"),
    (r" — not because", ", not because"),
    (r" — not a stage", ", not a stage"),
    (r" — it is ", ": it is "),
    (r" — it is a ", ": it is a "),
    (r" — I'll ", "; I'll "),
    (r" — I am ", ", I am "),
    (r" — I only ", ", I only "),
    (r" — I meant", ", I meant"),
    (r" — I apologize", ", I apologize"),
    (r" — I can't", ", I can't"),
    (r" — I won't", ", I won't"),
    (r" — I have ", ", I have "),
    (r" — I gave ", ", I gave "),
    (r" — I stayed ", ", I stayed "),
    (r" — I tell ", ", I tell "),
    (r" — I wasn't ", ", I wasn't "),
    (r" — Case ", ", Case "),
    (r" — Case One", ", Case One"),
    (r" — Case Two", ", Case Two"),
    (r" — Case Three", ", Case Three"),
    (r" — Case Four", ", Case Four"),
    (r" — Case Five", ", Case Five"),
    (r" — The ", ": The "),
    (r" — the ", ", the "),
    (r" — his ", ", his "),
    (r" — her ", ", her "),
    (r" — you ", ", you "),
    (r" — she ", ", she "),
    (r" — he ", ", he "),
    (r" — they ", ", they "),
    (r" — we ", ", we "),
    (r" — within ", ", within "),
    (r" — only ", ", only "),
    (r" — just ", ", just "),
    (r" — proud,", ", proud,"),
    (r" — proud ", ", proud "),
    (r" — fast,", ", fast,"),
    (r" — certain ", ", certain "),
    (r" — ash ", ", ash "),
    (r" — proof ", ", proof "),
    (r" — pride ", ", pride "),
    (r" — temporary,", ", temporary,"),
    (r" — companion ", ", companion "),
    (r" — three koku", ": three koku"),
    (r" — amber ", ", amber "),
    (r" — as if ", ", as if "),
    (r" — as written", ", as written"),
    (r" — where ", ", where "),
    (r" — when ", ", when "),
    (r" — while ", ", while "),
    (r" — until ", ", until "),
    (r" — before ", ", before "),
    (r" — after ", ", after "),
    (r" — instead ", ", instead "),
    (r" — alone ", ", alone "),
    (r" — alone —", ", alone,"),
    (r" — ahead ", ", ahead "),
    (r" — behind ", ", behind "),
    (r" — beside ", ", beside "),
    (r" — beyond ", ", beyond "),
    (r" — without ", ", without "),
    (r" — with ", ", with "),
    (r" — for ", ", for "),
    (r" — from ", ", from "),
    (r" — into ", ", into "),
    (r" — onto ", ", onto "),
    (r" — over ", ", over "),
    (r" — under ", ", under "),
    (r" — through ", ", through "),
    (r" — across ", ", across "),
    (r" — between ", ", between "),
    (r" — among ", ", among "),
    (r" — about ", ", about "),
    (r" — around ", ", around "),
    (r" — upon ", ", upon "),
    (r" — toward ", ", toward "),
    (r" — towards ", ", towards "),
    (r" — almost ", ", almost "),
    (r" — nearly ", ", nearly "),
    (r" — still ", ", still "),
    (r" — already ", ", already "),
    (r" — even ", ", even "),
    (r" — especially ", ", especially "),
    (r" — particularly ", ", particularly "),
    (r" — simply ", ", simply "),
    (r" — especially", ", especially"),
    (r" — implied ", "; implied "),
    (r" — never ", "; never "),
    (r" — always ", ", always "),
    (r" — sometimes ", ", sometimes "),
    (r" — often ", ", often "),
    (r" — rarely ", ", rarely "),
    (r" — usually ", ", usually "),
    (r" — perhaps ", ", perhaps "),
    (r" — maybe ", ", maybe "),
    (r" — certainly ", ", certainly "),
    (r" — obviously ", ", obviously "),
    (r" — apparently ", ", apparently "),
    (r" — literally ", ", literally "),
    (r" — basically ", ", basically "),
    (r" — essentially ", ", essentially "),
    (r" — ultimately ", ", ultimately "),
    (r" — finally ", ", finally "),
    (r" — eventually ", ", eventually "),
    (r" — immediately ", ", immediately "),
    (r" — suddenly ", ", suddenly "),
    (r" — quietly ", ", quietly "),
    (r" — softly ", ", softly "),
    (r" — loudly ", ", loudly "),
    (r" — slowly ", ", slowly "),
    (r" — quickly ", ", quickly "),
    (r" — gently ", ", gently "),
    (r" — firmly ", ", firmly "),
    (r" — cold ", ", cold "),
    (r" — warm ", ", warm "),
    (r" — hot ", ", hot "),
    (r" — rain ", ", rain "),
    (r" — ink ", ", ink "),
    (r" — wax ", ", wax "),
    (r" — seal ", ", seal "),
    (r" — desk ", ", desk "),
    (r" — office ", ", office "),
    (r" — canal ", ", canal "),
    (r" — barge ", ", barge "),
    (r" — boat ", ", boat "),
    (r" — dock ", ", dock "),
    (r" — hall ", ", hall "),
    (r" — door ", ", door "),
    (r" — screen ", ", screen "),
    (r" — ledger ", ", ledger "),
    (r" — clerk ", ", clerk "),
    (r" — magistrate ", ", magistrate "),
    (r" — witness ", ", witness "),
    (r" — companion ", ", companion "),
    (r" — patronage ", ", patronage "),
    (r" — sponsorship ", ", sponsorship "),
    (r" — performance ", ", performance "),
    (r" — expression ", ", expression "),
    (r" — discretion ", ", discretion "),
    (r" — custody ", ", custody "),
    (r" — escort ", ", escort "),
    (r" — grief ", ", grief "),
    (r" — silence ", ", silence "),
    (r" — proof ", ", proof "),
    (r" — bait ", ", bait "),
    (r" — prize ", ", prize "),
    (r" — manifest ", ", manifest "),
    (r" — docket ", ", docket "),
    (r" — file ", ", file "),
    (r" — packet ", ", packet "),
    (r" — scroll ", ", scroll "),
    (r" — permit ", ", permit "),
    (r" — Academy ", ", Academy "),
    (r" — Empire ", ", Empire "),
    (r" — Ryoko ", ", Ryoko "),
    (r" — Emerald ", ", Emerald "),
    (r" — Crane ", ", Crane "),
    (r" — Scorpion ", ", Scorpion "),
    (r" — Lion ", ", Lion "),
    (r" — Unicorn ", ", Unicorn "),
    (r" — Kakita ", ", Kakita "),
    (r" — Kitsu ", ", Kitsu "),
    (r" — Toa ", ", Toa "),
    (r" — Kaoru ", ", Kaoru "),
    (r" — Magistrate", ", Magistrate"),
    (r" — magistrate", ", magistrate"),
    (r" — DEV:", ": DEV:"),
    (r" — bg ", ": bg "),
    (r" — CG ", ": CG "),
    (r" — sprite ", ": sprite "),
    (r" — fit_", ": fit_"),
    (r" — full ", ": full "),
    (r" — show ", ": show "),
    (r" — locked ", ": locked "),
    (r" — gold/", ": gold/"),
    (r" — self-contained", ": self-contained"),
    (r" — single file", ": single file"),
    (r" — never shown", ": never shown"),
    (r" — restore:", ": restore:"),
    (r" — 「", ": 「"),
    (r" — implied coercion", ": implied coercion"),
    (r" — grave injury", ": grave injury"),
    (r" — hospital implied", ": hospital implied"),
    (r" — fade-to-black", ": fade-to-black"),
    (r" — no graphic", ": no graphic"),
    (r" — investigation bond:", ": investigation bond:"),
    (r" — patronage tension", ": patronage tension"),
    (r" — Canon ", ": Canon "),
    (r" — Bad End", ": Bad End"),
    (r" — Prologue", ": Prologue"),
    (r" — Is this", ": Is this"),
    (r" — Fabric Shop", ": Fabric Shop"),
    (r" — The Left Hand", ": The Left Hand"),
    (r" — The Dock Ledger", ": The Dock Ledger"),
    (r" — Teardrop Kobune", ": Teardrop Kobune"),
    (r" — The Academy Packet", ": The Academy Packet"),
    (r" — The Canal Investigation", ": The Canal Investigation"),
    (r" — The Encounter", ": The Encounter"),
    (r" — The Magistrate", ": The Magistrate"),
    (r" — Into the Rain", ": Into the Rain"),
    (r" — Otome ", ": Otome "),
    (r" — Ryoko Owari Nights", ": Ryoko Owari Nights"),
    (r" — Debug aid", ": Debug aid"),
    (r" — Transforms", ": Transforms"),
    (r" — bottom-left", ": bottom-left"),
    (r" — xalign/", ": xalign/"),
    (r" — say_thought", ": say_thought"),
    (r" — use work", ": use work"),
    (r" — only clear", ": only clear"),
    (r" — flanking", ": flanking"),
    (r" — letterboxed", ", letterboxed"),
    (r" — black bars", ", black bars"),
    (r" — full scene", ", full scene"),
    (r" — full 1536", ", full 1536"),
    (r" — content warning", ": content warning"),
    (r" — canon romance", ": canon romance"),
    (r" — bad endings", ": bad endings"),
    (r" — Discord sponsorship", ": Discord sponsorship"),
    (r" — art donor", ": art donor"),
    (r" — not danna", ", not danna"),
    (r" — not a lover", ", not a lover"),
    (r" — not a clerk", ", not a clerk"),
    (r" — not a threat", ", not a threat"),
    (r" — not a stage", ", not a stage"),
    (r" — not a field", ", not a field"),
    (r" — not a kept", ", not a kept"),
    (r" — not a prize", ", not a prize"),
    (r" — not bait", ", not bait"),
    (r" — not graphic", ", not graphic"),
    (r" — not entered", "; not entered"),
    (r" — not crossed", ", not crossed"),
    (r" — not your—", ", not your..."),
    (r" — not yet", ", not yet"),
    (r" — not lying", ", not lying"),
    (r" — not lying—", ", not lying..."),
    (r" — not finished", ", not finished"),
    (r" — not compose", ". Do not compose"),
    (r" — not hear", ", not hear"),
    (r" — learn to hear", ", learn to hear"),
    (r" — perform for me", ", perform for me"),
    (r" — perform ", ", perform "),
    (r" — interpret ", ", interpret "),
    (r" — attend ", ", attend "),
    (r" — remain ", ", remain "),
    (r" — maintain ", ", maintain "),
    (r" — carry ", ", carry "),
    (r" — witness ", ", witness "),
    (r" — schedule ", ", schedule "),
    (r" — effective ", ", effective "),
    (r" — official ", ", official "),
    (r" — wrong ", "; wrong "),
    (r" — wrong clan", "; wrong clan"),
    (r" — wrong door", "; wrong door"),
    (r" — wrong-green", ", wrong-green"),
    (r" — bodies do not", ", bodies do not"),
    (r" — spooky nonsense", ", spooky nonsense"),
    (r" — almost sunk", ", almost sunk"),
    (r" — could have died", ", could have died"),
    (r" — that's all I", ", that's all I"),
    (r" — the book", ", the book"),
    (r" — please", ", please"),
    (r" — thank you", ", thank you"),
    (r" — wait", ", wait"),
    (r" — stay ", ", stay "),
    (r" — let ", ", let "),
    (r" — sign ", ", sign "),
    (r" — eat ", ", eat "),
    (r" — copy ", ", copy "),
    (r" — bag ", ", bag "),
    (r" — ask ", ", ask "),
    (r" — refill ", ", refill "),
    (r" — archive ", ", archive "),
    (r" — unpack ", ", unpack "),
    (r" — continue ", ", continue "),
    (r" — Continue ", ", Continue "),
    (r" — briefly", ", briefly"),
    (r" — observe", ", observe"),
    (r" — admire ", ", admire "),
    (r" — earn ", ", earn "),
    (r" — satisfied ", ", satisfied "),
    (r" — tired", ", tired"),
    (r" — thirtieth", ", thirtieth"),
    (r" — unlatched", ", unlatched"),
    (r" — pays ", ", pays "),
    (r" — excuse", ", excuse"),
    (r" — board ", ", board "),
    (r" — patronage", ", patronage"),
    (r" — ledger", ", ledger"),
    (r" — treasury", ", treasury"),
    (r" — written", ", written"),
    (r" — order ", ", order "),
    (r" — forward", ", forward"),
    (r" — first light", ": first light"),
    (r" — first ", ", first "),
    (r" — second ", ", second "),
    (r" — third ", ", third "),
    (r" — fourth ", ", fourth "),
    (r" — fifth ", ", fifth "),
    (r" — light ", ", light "),
    (r" — dark ", ", dark "),
    (r" — black ", ", black "),
    (r" — white ", ", white "),
    (r" — red ", ", red "),
    (r" — green ", ", green "),
    (r" — blue ", ", blue "),
    (r" — gold ", ", gold "),
    (r" — silver ", ", silver "),
    (r" — teal ", ", teal "),
    (r" — palette", ", palette"),
    (r" — matching", ", matching"),
    (r" — GUI", ", GUI"),
    (r" — instrument", ", instrument"),
    (r" — mixer", ", mixer"),
    (r" — BGM", ", BGM"),
    (r" — forced", ", forced"),
    (r" — minimal", ", minimal"),
    (r" — closed-case", ", closed-case"),
    (r" — later scripts", ", later scripts"),
    (r" — refine with", ", refine with"),
    (r" — faster-whisper", ", faster-whisper"),
    (r" — planned", ", planned"),
    (r" — beats", ", beats"),
    (r" — approximate", ", approximate"),
    (r" — lyric sync", ", lyric sync"),
    (r" — instrumental", ", instrumental"),
    (r" — title drop", ", title drop"),
    (r" — outro", ", outro"),
    (r" — Pre-Ch", ", Pre-Ch"),
    (r" — Cases ", ": Cases "),
    (r" — gates ", ", gates "),
    (r" — date interlude", ": date interlude"),
    (r" — canon ending", ": canon ending"),
    (r" — canon romance", ": canon romance"),
    (r" — bad ending", ": bad ending"),
    (r" — game over", ": game over"),
    (r" — screenshot", ": screenshot"),
    (r" — review", ": review"),
    (r" — generated", ": generated"),
    (r" — all turns", ": all turns"),
    (r" — chapter pick", ": chapter pick"),
    (r" — dev ", ": dev "),
    (r" — DEV ", ": DEV "),
    (r" — test ", ": test "),
    (r" — mute ", ": mute "),
    (r" — audio ", ": audio "),
    (r" — music ", ": music "),
    (r" — song ", ": song "),
    (r" — duet ", ": duet "),
    (r" — image song", ": image song"),
    (r" — ED ", ": ED "),
    (r" — OP ", ": OP "),
    (r" — transforms", ": transforms"),
    (r" — guisupport", ": guisupport"),
    (r" — options", ": options"),
    (r" — gui ", ": gui "),
    (r" — stats ", ": stats "),
    (r" — screens", ": screens"),
    (r" — gallery", ": gallery"),
    (r" — layering", ": layering"),
    (r" — layout", ": layout"),
    (r" — backgrounds", ": backgrounds"),
    (r" — characters", ": characters"),
    (r" — cgs-", ": cgs-"),
    (r" — Path ", ": Path "),
    (r" — Seal at", ": Seal at"),
    (r" — Hearing", ": Hearing"),
    (r" — Lantern", ": Lantern"),
    (r" — Morning", ": Morning"),
    (r" — Festival", ": Festival"),
    (r" — Boat", ": Boat"),
    (r" — Date", ": Date"),
    (r" — Encounter", ": Encounter"),
    (r" — Ending", ": Ending"),
    (r" — Choices", ": Choices"),
    (r" — First Scene", ": First Scene"),
    (r" — Choice Moments", ": Choice Moments"),
    (r" — Just ", ", Just "),
    (r" — Just —", ", Just..."),
    (r" — Not ", ", Not "),
    (r" — Not —", ", Not..."),
    (r" — Um—", ", Um..."),
    (r" — Wear my—", ", Wear my..."),
    (r" — That is not", ", That is not"),
    (r" — That is—", ", That is..."),
    (r" — Basically ", ", Basically "),
    (r" — Um ", ", Um "),
    (r" — Uh ", ", Uh "),
    (r" — So, uh.", ", So, uh."),
    (r" — So ", ", So "),
    (r" — Well ", ", Well "),
    (r" — Now ", ", Now "),
    (r" — Then ", ", Then "),
    (r" — Yes ", ", Yes "),
    (r" — No ", ", No "),
    (r" — Please", ", Please"),
    (r" — Thank", ", Thank"),
    (r" — Sorry", ", Sorry"),
    (r" — Excuse", ", Excuse"),
    (r" — Pardon", ", Pardon"),
    (r" — Magistrate-sama", ", Magistrate-sama"),
    (r" — magistrate-sama", ", magistrate-sama"),
    (r" — Toa,", ", Toa,"),
    (r" — Toa—", ", Toa..."),
    (r" — Toa ", ", Toa "),
    (r" — Kaoru ", ", Kaoru "),
    (r" — Clerk ", ", Clerk "),
    (r" — Watch ", ", Watch "),
    (r" — River ", ", River "),
    (r" — Canal ", ", Canal "),
    (r" — Compound ", ", Compound "),
    (r" — Residence ", ", Residence "),
    (r" — Inner hall", ", Inner hall"),
    (r" — Chamber ", ", Chamber "),
    (r" — Office ", ", Office "),
    (r" — Desk ", ", Desk "),
    (r" — Seal ", ", Seal "),
    (r" — Hanko ", ", Hanko "),
    (r" — Wax ", ", Wax "),
    (r" — Ink ", ", Ink "),
    (r" — Paper ", ", Paper "),
    (r" — Scroll ", ", Scroll "),
    (r" — Lantern ", ", Lantern "),
    (r" — Rain ", ", Rain "),
    (r" — Wind ", ", Wind "),
    (r" — Night ", ", Night "),
    (r" — Dawn ", ", Dawn "),
    (r" — Dusk ", ", Dusk "),
    (r" — Morning ", ", Morning "),
    (r" — Evening ", ", Evening "),
    (r" — Afternoon ", ", Afternoon "),
    (r" — Midnight ", ", Midnight "),
    (r" — Noon ", ", Noon "),
    (r" — Today ", ", Today "),
    (r" — Tonight ", ", Tonight "),
    (r" — Tomorrow ", ", Tomorrow "),
    (r" — Yesterday ", ", Yesterday "),
    (r" — Always ", ", Always "),
    (r" — Never ", ", Never "),
    (r" — Sometimes ", ", Sometimes "),
    (r" — Often ", ", Often "),
    (r" — Rarely ", ", Rarely "),
    (r" — Usually ", ", Usually "),
    (r" — Perhaps ", ", Perhaps "),
    (r" — Maybe ", ", Maybe "),
    (r" — Certainly ", ", Certainly "),
    (r" — Obviously ", ", Obviously "),
    (r" — Apparently ", ", Apparently "),
    (r" — Literally ", ", Literally "),
    (r" — Basically ", ", Basically "),
    (r" — Essentially ", ", Essentially "),
    (r" — Ultimately ", ", Ultimately "),
    (r" — Finally ", ", Finally "),
    (r" — Eventually ", ", Eventually "),
    (r" — Immediately ", ", Immediately "),
    (r" — Suddenly ", ", Suddenly "),
    (r" — Quietly ", ", Quietly "),
    (r" — Softly ", ", Softly "),
    (r" — Loudly ", ", Loudly "),
    (r" — Slowly ", ", Slowly "),
    (r" — Quickly ", ", Quickly "),
    (r" — Gently ", ", Gently "),
    (r" — Firmly ", ", Firmly "),
]


def replace_in_segment(text: str) -> str:
    if EM not in text:
        return text

    # Letter stutter: I—I -> I-I (ASCII hyphen, not ellipsis)
    text = re.sub(r"([A-Za-z])" + re.escape(EM) + r"([A-Za-z])", r"\1-\2", text)

    # Paired parenthetical: " — word — "
    text = re.sub(
        r" — (\w+(?:\s+\w+)?) — ",
        r", \1, ",
        text,
    )

    # Interruption: word— before space, punctuation, quote, or end
    text = re.sub(r"(\w)" + re.escape(EM) + r"(?=\s|$|[\"'!?.,;:\)])", r"\1...", text)
    text = re.sub(r"(\w)" + re.escape(EM) + r"(?=[A-Za-z])", r"\1... ", text)

    # Spaced em dash rules
    for pattern, repl in SPACED_RULES:
        text = re.sub(pattern.replace(" — ", f" {EM} ").replace("—", EM), repl, text)

    # Remaining spaced em dashes -> comma (most common prose break)
    text = text.replace(f" {EM} ", ", ")

    # Any remaining em dashes
    text = text.replace(EM, ", ")

    # Cleanup double punctuation artifacts
    text = re.sub(r",\s*,", ",", text)
    text = re.sub(r",\s*\.\s", ". ", text)

    return text


TAG_SPLIT = re.compile(r"(\[[^\]]*\])")


def replace_preserving_tags(text: str) -> str:
    parts = TAG_SPLIT.split(text)
    out: list[str] = []
    for part in parts:
        if part.startswith("[") and part.endswith("]"):
            out.append(part)
        else:
            out.append(replace_in_segment(part))
    return "".join(out)


def iter_rpy_files() -> list[Path]:
    files: list[Path] = []
    for path in GAME_GLOB.rglob("*.rpy"):
        if SKIP_PARTS.intersection(path.parts):
            continue
        files.append(path)
    return sorted(files)


def count_lines_changed(old: str, new: str) -> int:
    old_lines = old.splitlines()
    new_lines = new.splitlines()
    n = max(len(old_lines), len(new_lines))
    changed = 0
    for i in range(n):
        o = old_lines[i] if i < len(old_lines) else ""
        ne = new_lines[i] if i < len(new_lines) else ""
        if o != ne:
            changed += 1
    return changed


def process_text_file(path: Path) -> tuple[int, list[tuple[str, str]]]:
    old = path.read_text(encoding="utf-8")
    if EM not in old:
        return 0, []
    new = replace_preserving_tags(old)
    if new == old:
        return 0, []
    samples: list[tuple[str, str]] = []
    for o_line, n_line in zip(old.splitlines(), new.splitlines()):
        if o_line != n_line and EM in o_line:
            samples.append((o_line.strip(), n_line.strip()))
            if len(samples) >= 3:
                break
    path.write_text(new, encoding="utf-8")
    return count_lines_changed(old, new), samples


def backup_manifest() -> Path:
    dest_dir = ROOT / "scripts" / "versions"
    dest_dir.mkdir(parents=True, exist_ok=True)
    src = ROOT / "scripts" / "voice_performance_manifest.json"
    dest = dest_dir / f"voice_performance_manifest-pre-no-emdash-{DATE}.json"
    shutil.copy2(src, dest)
    return dest


def backup_rpy_files(paths: list[Path]) -> Path:
    dest_root = ROOT / "game" / "versions" / f"no-emdash-{DATE}"
    for path in paths:
        rel = path.relative_to(GAME_GLOB)
        dest = dest_root / rel
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(path, dest)
    return dest_root


def process_manifest(path: Path) -> tuple[int, set[str], list[tuple[str, str]]]:
    data = json.loads(path.read_text(encoding="utf-8"))
    changed_ids: set[str] = set()
    lines_changed = 0
    samples: list[tuple[str, str]] = []

    if "entries" in data:
        for entry in data["entries"]:
            entry_changed = False
            for field in ("game_text", "tts_text", "text", "line"):
                if field not in entry or EM not in str(entry[field]):
                    continue
                old_val = entry[field]
                new_val = replace_preserving_tags(old_val)
                if new_val != old_val:
                    if len(samples) < 3:
                        samples.append((old_val, new_val))
                    entry[field] = new_val
                    entry_changed = True
            if entry_changed and "id" in entry:
                changed_ids.add(entry["id"])
                lines_changed += 1
    else:
        # voice_manifest may be flat list
        items = data if isinstance(data, list) else data.get("lines", [])
        for entry in items:
            if not isinstance(entry, dict):
                continue
            for field in ("game_text", "tts_text", "text", "line"):
                if field not in entry or EM not in str(entry[field]):
                    continue
                old_val = entry[field]
                new_val = replace_preserving_tags(old_val)
                if new_val != old_val:
                    entry[field] = new_val
                    if "id" in entry:
                        changed_ids.add(entry["id"])
                    lines_changed += 1

    if changed_ids or lines_changed:
        path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    return lines_changed, changed_ids, samples


def main() -> None:
    print("=== Before ===")
    rpy_count = sum(p.read_text(encoding="utf-8").count(EM) for p in iter_rpy_files())
    print(f"game/**/*.rpy em dashes: {rpy_count}")
    for m in MANIFESTS:
        if m.exists():
            print(f"{m.name}: {m.read_text(encoding='utf-8').count(EM)}")

    manifest_backup = backup_manifest()
    print(f"\nBacked up manifest -> {manifest_backup.relative_to(ROOT)}")

    touched_rpy: list[Path] = []
    total_line_changes = 0
    all_samples: list[tuple[str, str, str]] = []

    for path in iter_rpy_files():
        if EM not in path.read_text(encoding="utf-8"):
            continue
        touched_rpy.append(path)

    if touched_rpy:
        backup_dir = backup_rpy_files(touched_rpy)
        print(f"Backed up {len(touched_rpy)} rpy files -> {backup_dir.relative_to(ROOT)}")

    for path in touched_rpy:
        lines, samples = process_text_file(path)
        total_line_changes += lines
        for before, after in samples:
            all_samples.append((str(path.relative_to(ROOT)), before, after))

    voice_ids: set[str] = set()
    manifest_lines = 0
    for m in MANIFESTS:
        if not m.exists() or EM not in m.read_text(encoding="utf-8"):
            continue
        # Re-read before process in case already written - process reads fresh
        lines, ids, samples = process_manifest(m)
        manifest_lines += lines
        voice_ids.update(ids)
        for before, after in samples:
            all_samples.append((m.name, before, after))

    print("\n=== After ===")
    rpy_after = sum(p.read_text(encoding="utf-8").count(EM) for p in iter_rpy_files())
    print(f"game/**/*.rpy em dashes: {rpy_after}")
    perf_after = (ROOT / "scripts" / "voice_performance_manifest.json").read_text(encoding="utf-8").count(EM)
    print(f"voice_performance_manifest.json: {perf_after}")

    print("\n=== Summary ===")
    print(f"Files touched: {len(touched_rpy) + sum(1 for m in MANIFESTS if m.exists())}")
    print(f"RPY files touched: {len(touched_rpy)}")
    print(f"RPY lines changed: {total_line_changes}")
    print(f"Manifest entry fields changed: {manifest_lines}")
    print(f"Voice IDs affected (performance manifest): {len(voice_ids)}")

    print("\n=== Samples ===")
    for src, before, after in all_samples[:8]:
        print(f"[{src}]")
        print(f"  BEFORE: {before[:120]}")
        print(f"  AFTER:  {after[:120]}")

    if rpy_after or perf_after:
        print("\nWARNING: em dashes remain!")
        for path in iter_rpy_files():
            text = path.read_text(encoding="utf-8")
            if EM in text:
                for i, line in enumerate(text.splitlines(), 1):
                    if EM in line:
                        print(f"  {path.relative_to(ROOT)}:{i}: {line.strip()[:100]}")
        raise SystemExit(1)


if __name__ == "__main__":
    main()
