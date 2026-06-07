#!/usr/bin/env python3
"""One-off audit for AU narration voicing + Toa respelling tasks."""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GAME = ROOT / "game"
VOICE_DIR = GAME / "audio" / "voice"

AU_FILES = [
    "au_modern_wrong_floor.rpy",
    "au_modern_case1_compliance.rpy",
    "au_modern_case2_island_weekend.rpy",
    "au_modern_case3_permits_hr.rpy",
    "au_modern_epilogue.rpy",
]

VOICE_RE = re.compile(r'voice\s+"audio/voice/(\w+)\.mp3"')
DIALOGUE_RE = re.compile(r'^\s*(kaoru|toa|narrator)\s+"(.*)"\s*$')
NARRATION_RE = re.compile(r'^(\s+)"(.*)"\s*$')


def manifest_max():
    out = {}
    for name in ("voice_manifest.json", "narrator_manifest.json",
                 "voice_performance_manifest.json", "voice_v2_metadata_manifest.json"):
        p = ROOT / "scripts" / name
        data = json.loads(p.read_text(encoding="utf-8"))
        rows = data.get("lines") or data.get("entries") or []
        ids = [r["id"] for r in rows]
        maxes = {}
        for vid in ids:
            try:
                c, n = vid.rsplit("_", 1)
                n = int(n)
            except ValueError:
                continue
            maxes[c] = max(maxes.get(c, 0), n)
        out[name] = {k: maxes.get(k, 0) for k in ("toa", "kaoru", "narrator")}
    return out


def script_max():
    maxes = {}
    for name in AU_FILES:
        for m in VOICE_RE.finditer((GAME / name).read_text(encoding="utf-8")):
            vid = m.group(1)
            try:
                c, n = vid.rsplit("_", 1)
                n = int(n)
            except ValueError:
                continue
            maxes[c] = max(maxes.get(c, 0), n)
    return maxes


def find_silent_and_voiced():
    """Return (silent, voiced_ids) per file.

    silent = narration lines with NO voice statement on the preceding
             non-blank/non-comment line.
    """
    silent = {}
    voiced_ids = {}
    for name in AU_FILES:
        lines = (GAME / name).read_text(encoding="utf-8").splitlines()
        file_silent = []
        file_voiced = []
        prev_code = None  # previous non-blank, non-comment line
        for i, line in enumerate(lines, start=1):
            stripped = line.strip()
            if not stripped or stripped.startswith("#"):
                continue
            vm = VOICE_RE.search(line)
            if vm and stripped.startswith("voice "):
                file_voiced.append((vm.group(1), i))
                prev_code = line
                continue
            # narration line?
            nm = NARRATION_RE.match(line)
            is_dialogue = DIALOGUE_RE.match(line)
            is_centered = stripped.startswith(("centered ", "menu", "$", "show ",
                                               "scene ", "play ", "stop ", "pause",
                                               "jump", "label", "if ", "elif ",
                                               "else", "default", "hide ", "with ",
                                               "return"))
            if nm and not is_dialogue and not stripped.startswith("centered "):
                # bare narration string. Voiced if prev_code is a voice stmt.
                prev_is_voice = bool(prev_code and prev_code.strip().startswith("voice "))
                if not prev_is_voice:
                    file_silent.append((i, nm.group(2)))
            prev_code = line
        silent[name] = file_silent
        voiced_ids[name] = file_voiced
    return silent, voiced_ids


def check_files(voiced_ids):
    missing = []
    empty = []
    for name, ids in voiced_ids.items():
        for vid, ln in ids:
            p = VOICE_DIR / f"{vid}.mp3"
            if not p.exists():
                missing.append((name, ln, vid))
            elif p.stat().st_size == 0:
                empty.append((name, ln, vid))
    return missing, empty


def toa_scan():
    """Scan performance + v2 manifests for narrator tts_text containing Toh-ah
    or plain Toa with no respelling."""
    pm = json.loads((ROOT / "scripts" / "voice_performance_manifest.json").read_text(encoding="utf-8"))
    tohah = []
    plain_toa = []
    for e in pm.get("entries", []):
        if not e["id"].startswith("narrator_"):
            continue
        tts = e.get("tts_text", "") or ""
        gt = e.get("game_text", "") or ""
        if "Toh-ah" in tts:
            tohah.append(e["id"])
        elif "Toa" in gt and "Toa" in tts:
            plain_toa.append(e["id"])
    return tohah, plain_toa


def main():
    print("=== manifest max ids ===")
    for k, v in manifest_max().items():
        print(f"  {k}: {v}")
    print(f"  script (au .rpy) voice-stmt max: {script_max()}")

    silent, voiced = find_silent_and_voiced()
    print("\n=== SILENT narration (no voice stmt above) ===")
    total = 0
    for name, rows in silent.items():
        print(f"  {name}: {len(rows)}")
        for ln, txt in rows:
            total += 1
            print(f"    L{ln}: {txt[:90]}")
    print(f"  TOTAL silent: {total}")

    missing, empty = check_files(voiced)
    print("\n=== voiced ids referenced in AU scripts but file MISSING ===")
    for name, ln, vid in missing:
        print(f"    {name}:L{ln} {vid}")
    print(f"  missing files: {len(missing)}")
    print(f"  empty files: {len(empty)} -> {empty}")

    tohah, plain = toa_scan()
    print("\n=== Toa respelling scan (narrator entries in performance manifest) ===")
    print(f"  tts_text containing 'Toh-ah': {len(tohah)}")
    print(f"    {tohah}")
    print(f"  game_text has Toa but tts_text still plain 'Toa' (no respell): {len(plain)}")
    print(f"    {plain}")


if __name__ == "__main__":
    main()
