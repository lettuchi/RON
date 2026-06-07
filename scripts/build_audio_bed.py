#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Build the Ryoko Owari trailer audio bed.

Takes the OP techno song (game/audio/bgm/opening_op.mp3) as the spine, mixes in a
handful of voice lines and SFX accents from trailer/audio_overlays.json, ducks the
music under the voice lines, limits the sum, and writes a single timed track at the
exact trailer duration.

Stdlib only; shells out to ffmpeg/ffprobe (FFmpeg 8.x).

Usage (project root):
    python scripts/build_audio_bed.py
    python scripts/build_audio_bed.py --dry-run
    python scripts/build_audio_bed.py --overlays trailer/audio_overlays.json --out trailer/audio/trailer_bed.m4a
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SHOTLIST = ROOT / "trailer" / "shotlist.json"
OVERLAYS = ROOT / "trailer" / "audio_overlays.json"


def run(cmd: list[str], *, dry: bool) -> None:
    printable = " ".join(f'"{c}"' if " " in c else c for c in cmd)
    print(printable if dry else f"$ {printable}")
    if dry:
        return
    proc = subprocess.run(cmd, cwd=str(ROOT))
    if proc.returncode != 0:
        print(f"ERROR: command failed ({proc.returncode})", file=sys.stderr)
        raise SystemExit(proc.returncode)


def ffprobe_duration(path: Path) -> float:
    out = subprocess.run(
        [
            "ffprobe", "-v", "error", "-show_entries", "format=duration",
            "-of", "default=noprint_wrappers=1:nokey=1", str(path),
        ],
        cwd=str(ROOT), capture_output=True, text=True,
    )
    try:
        return float(out.stdout.strip())
    except (TypeError, ValueError):
        return 0.0


def load_json(path: Path) -> dict:
    if not path.exists():
        print(f"ERROR: missing {path}", file=sys.stderr)
        raise SystemExit(2)
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> None:
    ap = argparse.ArgumentParser(description="Build the trailer audio bed.")
    ap.add_argument("--overlays", type=Path, default=OVERLAYS)
    ap.add_argument("--out", type=Path, default=None)
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    shot_cfg = load_json(SHOTLIST)["config"]
    duration = float(shot_cfg["duration"])
    music = ROOT / shot_cfg["music"]
    out = args.out or (ROOT / shot_cfg["audio_bed"])
    out.parent.mkdir(parents=True, exist_ok=True)

    if not music.is_file():
        print(f"ERROR: music spine not found: {music}", file=sys.stderr)
        raise SystemExit(2)

    cfg = load_json(args.overlays)
    music_gain = float(cfg.get("music_gain_db", 0.0))
    duck_db = float(cfg.get("duck_db", -6.0))
    events = cfg.get("events", [])

    # Resolve overlay files; keep only those present on disk.
    resolved: list[dict] = []
    for ev in events:
        p = ROOT / ev["path"]
        if not p.is_file():
            print(f"WARN: overlay missing, skipping: {p}", file=sys.stderr)
            continue
        dur = ffprobe_duration(p)
        resolved.append({**ev, "abspath": p, "dur": dur})

    # Music ducking envelope: drop the bed under each voice window.
    duck_factor = 10 ** (duck_db / 20.0)
    voice_windows = [
        (float(ev["at"]), float(ev["at"]) + max(ev["dur"], 0.3))
        for ev in resolved if ev.get("kind") == "voice"
    ]
    if voice_windows:
        betweens = "+".join(
            f"between(t,{a:.3f},{b:.3f})" for a, b in voice_windows
        )
        # 1.0 normally, duck_factor inside any voice window.
        duck_expr = f"1-(1-{duck_factor:.4f})*min(1\\,{betweens})"
        music_filter = (
            f"volume={10 ** (music_gain / 20.0):.4f},"
            f"volume=eval=frame:volume='{duck_expr}'"
        )
    else:
        music_filter = f"volume={10 ** (music_gain / 20.0):.4f}"

    inputs: list[str] = ["-i", str(music)]
    for ev in resolved:
        inputs += ["-i", str(ev["abspath"])]

    parts: list[str] = [f"[0:a]aresample=48000,{music_filter}[m]"]
    mix_labels = ["[m]"]
    for idx, ev in enumerate(resolved, start=1):
        at_ms = int(round(float(ev["at"]) * 1000))
        gain = 10 ** (float(ev.get("gain_db", 0.0)) / 20.0)
        label = f"o{idx}"
        parts.append(
            f"[{idx}:a]aresample=48000,adelay={at_ms}|{at_ms},"
            f"volume={gain:.4f}[{label}]"
        )
        mix_labels.append(f"[{label}]")

    n = len(mix_labels)
    parts.append(
        "".join(mix_labels)
        + f"amix=inputs={n}:normalize=0:dropout_transition=0[mixraw]"
    )
    parts.append(
        f"[mixraw]alimiter=limit=0.95,"
        f"apad,atrim=end={duration:.3f},"
        f"afade=t=out:st={duration - 2.0:.3f}:d=2.0,"
        f"aresample=48000[out]"
    )
    filtergraph = ";".join(parts)

    cmd = [
        "ffmpeg", "-y", *inputs,
        "-filter_complex", filtergraph,
        "-map", "[out]",
        "-c:a", "aac", "-b:a", "256k",
        "-t", f"{duration:.3f}",
        str(out),
    ]

    print(f"Music spine : {music.relative_to(ROOT)}  ({ffprobe_duration(music):.2f}s)")
    print(f"Overlays    : {len(resolved)} "
          f"({sum(1 for e in resolved if e.get('kind') == 'voice')} voice, "
          f"{sum(1 for e in resolved if e.get('kind') == 'sfx')} sfx)")
    for ev in resolved:
        print(f"  + [{ev.get('kind'):5}] {ev['path']} @ {ev['at']}s "
              f"({ev['dur']:.2f}s, {ev.get('gain_db', 0.0):+}dB)")
    print(f"Output      : {out.relative_to(ROOT)}  (target {duration:.3f}s)")

    run(cmd, dry=args.dry_run)
    if not args.dry_run:
        print(f"\nWrote {out.relative_to(ROOT)} "
              f"({out.stat().st_size // 1024} KiB, {ffprobe_duration(out):.2f}s)")


if __name__ == "__main__":
    main()
