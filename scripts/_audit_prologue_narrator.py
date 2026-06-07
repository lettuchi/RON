#!/usr/bin/env python3
"""One-off audit: prologue narrator script vs manifest game_text."""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PROLOGUE_FILES = [
    ROOT / "game/prologue.rpy",
    ROOT / "game/prologue_canon_encounter.rpy",
]


def normalize(s: str) -> str:
    s = (
        s.replace("\u2019", "'")
        .replace("\u2018", "'")
        .replace("\u201c", '"')
        .replace("\u201d", '"')
    )
    s = s.replace("\u2014", "—").replace("\u2013", "-")
    return re.sub(r"\s+", " ", s.strip())


def parse_narrator_voices(path: Path) -> list[tuple[str, str | None, int, str]]:
    lines = path.read_text(encoding="utf-8").splitlines()
    results: list[tuple[str, str | None, int, str]] = []
    i = 0
    while i < len(lines):
        m = re.search(r'voice "audio/voice/(narrator_\d+)\.mp3"', lines[i])
        if m:
            vid = m.group(1)
            j = i + 1
            while j < len(lines) and (
                not lines[j].strip() or lines[j].strip().startswith("#")
            ):
                j += 1
            if j < len(lines):
                line = lines[j].strip()
                sm = re.match(r'^"((?:[^"\\]|\\.)*)"', line)
                if sm:
                    dlg = sm.group(1).replace('\\"', '"').replace("\\n", " ")
                    results.append((vid, dlg, i + 1, path.name))
                elif re.match(r"^(toa|kaoru)\s", line, re.I):
                    results.append((vid, None, i + 1, path.name))
                else:
                    results.append((vid, f"<<{line[:80]}>>", i + 1, path.name))
        i += 1
    return results


def main() -> None:
    manifest = json.loads(
        (ROOT / "scripts/voice_performance_manifest.json").read_text(encoding="utf-8")
    )
    entries = manifest["entries"] if isinstance(manifest, dict) else manifest
    by_id = {e["id"]: e for e in entries}

    all_entries: list[tuple[str, str | None, int, str]] = []
    for p in PROLOGUE_FILES:
        all_entries.extend(parse_narrator_voices(p))

    mismatches = []
    missing_manifest = []
    miswired = []

    for vid, dlg, lineno, fname in all_entries:
        if dlg is None:
            miswired.append((vid, lineno, fname))
            continue
        if dlg.startswith("<<"):
            mismatches.append((vid, lineno, fname, "unparsed", dlg, ""))
            continue
        entry = by_id.get(vid)
        if not entry:
            missing_manifest.append((vid, lineno, fname, dlg))
            continue
        g = normalize(entry.get("game_text", ""))
        d = normalize(dlg)
        if g != d:
            mismatches.append((vid, lineno, fname, d, g))

    print("=== PROLOGUE NARRATOR AUDIT ===")
    print(f"Total voice-tagged narrator lines: {len(all_entries)}")
    print(f"Mismatches: {len(mismatches)}")
    print(f"Missing manifest: {len(missing_manifest)}")
    print(f"Miswired: {len(miswired)}")
    print()
    for m in mismatches:
        vid, ln, fn = m[0], m[1], m[2]
        if m[3] == "unparsed":
            print(f"{vid} {fn}:{ln} UNPARSED {m[4]}")
        else:
            print(f"--- {vid} {fn}:{ln} ---")
            print(f"  SCRIPT: {m[3]}")
            print(f"  MANIF:  {m[4]}")
    ref_path = ROOT / "scripts/prologue_voice_ids.txt"
    if ref_path.exists():
        ref_ids = {
            ln.strip()
            for ln in ref_path.read_text().splitlines()
            if ln.strip().startswith("narrator_")
        }
        script_ids = {v for v, _, _, _ in all_entries}
        print()
        print("In prologue_voice_ids but not script:", sorted(ref_ids - script_ids))
        print("In script but not prologue_voice_ids:", sorted(script_ids - ref_ids))


def audit_bad_end_and_main() -> None:
    """Verify prologue.rpy narrator IDs 001-038, 183-187, 206-213."""
    entries = parse_narrator_voices(ROOT / "game/prologue.rpy")
    manifest = json.loads(
        (ROOT / "scripts/voice_performance_manifest.json").read_text(encoding="utf-8")
    )
    by_id = {e["id"]: e for e in manifest["entries"]}
    bad = []
    ok = 0
    for vid, dlg, ln, fn in entries:
        if dlg is None or dlg.startswith("<<"):
            bad.append((vid, ln, "parse/miswire"))
            continue
        e = by_id.get(vid)
        if not e or normalize(e.get("game_text", "")) != normalize(dlg):
            bad.append((vid, ln, "mismatch" if e else "no entry"))
        else:
            ok += 1
    print(f"prologue.rpy only: OK={ok} BAD={len(bad)}")
    for b in bad:
        print(" ", b)


if __name__ == "__main__":
    main()
    print()
    audit_bad_end_and_main()
