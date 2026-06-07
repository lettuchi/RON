#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Assemble the Ryoko Owari cel-shaded trailer from trailer/shotlist.json.

Per-shot motion:
  procedural    - Ken Burns (zoom/pan) over an existing still, on a 16:9 blurred-fill canvas.
  handdrawn_cel - if trailer/clips/<id>.mp4 exists (AI-motion of the cel keyframes) it is used;
                  otherwise the cel keyframes are machine-inbetweened (xfade morph) to fake
                  animation on 2s/3s.
  ai_video      - trailer/clips/<id>.mp4 if present, else procedural fallback on the first frame.

Any shot whose id has a matching trailer/clips/<id>.mp4 uses that clip (this is how the hero
"hand-drawn cel keyframes + AI inbetween" cuts are realized). Shots are cross-dissolved
(xfade chain) with per-shot transitions (dissolve / fadewhite / fadered) anchored to the OP
vocal-onset timing already in the shotlist. A final pass bakes warm_noir grade + vignette +
light grain + letterbox, drawtext lower-third subtitles / upper-third name cards / the title
(Yuji Syuku font), and muxes trailer/audio/trailer_bed.m4a. Outputs H.264 mp4 + VP9 webm.

Stdlib only; shells out to ffmpeg/ffprobe (FFmpeg 8.x).

Usage (project root):
    python scripts/build_trailer.py --dry-run
    python scripts/build_trailer.py
    python scripts/build_trailer.py --cut          # hard-cut concat fallback (no xfade)
    python scripts/build_trailer.py --skip-segments # reuse rendered segments, re-assemble only
    python scripts/build_trailer.py --no-webm
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SHOTLIST = ROOT / "trailer" / "shotlist.json"
WORK = ROOT / "trailer" / "_build"
SEGDIR = WORK / "seg"
TXTDIR = WORK / "txt"
CLIPDIR = ROOT / "trailer" / "clips"

CW, CH = 2400, 1350  # oversize 16:9 canvas (gives Ken Burns room)
FLASH_DUR = 0.25
OPEN_FADE = 0.8
FONT = "game/fonts/YujiSyuku-Regular.ttf"


def run(cmd: list[str], *, dry: bool, log: bool = False) -> None:
    if dry:
        print(" ".join(f'"{c}"' if (" " in c) else c for c in cmd))
        return
    proc = subprocess.run(
        cmd, cwd=str(ROOT),
        stdout=(None if log else subprocess.DEVNULL),
        stderr=(None if log else subprocess.STDOUT),
    )
    if proc.returncode != 0:
        print(f"ERROR: ffmpeg failed ({proc.returncode}):\n  "
              + " ".join(cmd), file=sys.stderr)
        raise SystemExit(proc.returncode)


def ffprobe_duration(path: Path) -> float:
    out = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "default=noprint_wrappers=1:nokey=1", str(path)],
        cwd=str(ROOT), capture_output=True, text=True,
    )
    try:
        return float(out.stdout.strip())
    except (TypeError, ValueError):
        return 0.0


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


# --- Ken Burns via zoompan (z/x/y evaluated per output frame) ----------------
def kenburns(motion: str, L: float, fps: int, W: int, H: int) -> str:
    """Return a zoompan filter producing a WxH Ken Burns move for the given motion."""
    F = max(1, round(L * fps))
    if motion == "kb_out":
        z = f"1.12-0.12*on/{F}"
    elif motion == "punch":
        z = f"1+0.20*on/{F}"
    elif motion == "kb_settle":
        z = f"1.06-0.05*on/{F}"
    elif motion in ("kb_pan_l", "kb_pan_r", "kb_rise"):
        z = "1.10"
    else:  # kb_in (default)
        z = f"1+0.12*on/{F}"

    if motion == "kb_pan_l":
        x, y = f"(iw-iw/zoom)*on/{F}", "ih/2-(ih/zoom/2)"
    elif motion == "kb_pan_r":
        x, y = f"(iw-iw/zoom)*(1-on/{F})", "ih/2-(ih/zoom/2)"
    elif motion == "kb_rise":
        x, y = "iw/2-(iw/zoom/2)", f"(ih-ih/zoom)*(1-on/{F})"
    else:
        x, y = "iw/2-(iw/zoom/2)", "ih/2-(ih/zoom/2)"
    return f"zoompan=z='{z}':x='{x}':y='{y}':d=1:s={W}x{H}:fps={fps}"


def fill_canvas(in_label: str, out_label: str) -> str:
    """Blurred-fill 16:9 canvas: full illustration contained over a blurred cover background."""
    return (
        f"{in_label}split=2[bg_{out_label}][fg_{out_label}];"
        f"[bg_{out_label}]scale={CW}:{CH}:force_original_aspect_ratio=increase,"
        f"crop={CW}:{CH},gblur=sigma=26,eq=brightness=-0.10:saturation=0.82[bgb_{out_label}];"
        f"[fg_{out_label}]scale={CW}:{CH}:force_original_aspect_ratio=decrease[fgs_{out_label}];"
        f"[bgb_{out_label}][fgs_{out_label}]overlay=(W-w)/2:(H-h)/2,setsar=1[{out_label}]"
    )


def alpha_fade(L: float, fin: float = 0.3, fout: float = 0.4) -> str:
    Ls = f"{L:.3f}"
    return (f"'if(lt(t,{fin}),t/{fin},"
            f"if(gt(t,{Ls}-{fout}),max(0,({Ls}-t)/{fout}),1))'")


def overlays(idx: int, shot: dict, L: float, W: int, H: int) -> str:
    """drawtext chain for subtitle / namecard / title (relative font + textfile paths)."""
    parts: list[str] = []
    a = alpha_fade(L)

    sub = shot.get("subtitle")
    if sub:
        p = TXTDIR / f"seg{idx:02d}_sub.txt"
        write_text(p, sub)
        rel = p.relative_to(ROOT).as_posix()
        parts.append(
            f"drawtext=fontfile={FONT}:textfile={rel}:fontcolor=0xF3DADA:"
            f"fontsize=34:x=(w-text_w)/2:y={int(H*0.855)}:box=1:boxcolor=black@0.45:"
            f"boxborderw=18:borderw=2:bordercolor=black@0.85:line_spacing=6:alpha={a}"
        )

    nc = shot.get("namecard")
    if nc:
        margin = int(W * 0.06)
        xmain = f"{margin}" if nc.get("side") == "left" else f"w-text_w-{margin}"
        pm = TXTDIR / f"seg{idx:02d}_nc_main.txt"
        write_text(pm, nc.get("main", ""))
        ps = TXTDIR / f"seg{idx:02d}_nc_sub.txt"
        write_text(ps, nc.get("sub", ""))
        parts.append(
            f"drawtext=fontfile={FONT}:textfile={pm.relative_to(ROOT).as_posix()}:"
            f"fontcolor=white:fontsize=54:x={xmain}:y={int(H*0.14)}:borderw=3:"
            f"bordercolor=0x14007A:shadowx=2:shadowy=2:alpha={a}"
        )
        parts.append(
            f"drawtext=fontfile={FONT}:textfile={ps.relative_to(ROOT).as_posix()}:"
            f"fontcolor=0xD2D2F0:fontsize=24:x={xmain}:y={int(H*0.14)+64}:borderw=2:"
            f"bordercolor=black@0.85:alpha={a}"
        )

    title = shot.get("title")
    if title:
        at = alpha_fade(L, fin=0.6, fout=1.2)
        pm = TXTDIR / f"seg{idx:02d}_title_main.txt"
        write_text(pm, title.get("main", ""))
        ps = TXTDIR / f"seg{idx:02d}_title_sub.txt"
        write_text(ps, title.get("sub", ""))
        parts.append(
            f"drawtext=fontfile={FONT}:textfile={pm.relative_to(ROOT).as_posix()}:"
            f"fontcolor=white:fontsize=96:x=(w-text_w)/2:y={int(H*0.38)}:borderw=4:"
            f"bordercolor=0x10005E:shadowx=2:shadowy=3:alpha={at}"
        )
        parts.append(
            f"drawtext=fontfile={FONT}:textfile={ps.relative_to(ROOT).as_posix()}:"
            f"fontcolor=0xDADAF3:fontsize=46:x=(w-text_w)/2:y={int(H*0.38)+124}:borderw=3:"
            f"bordercolor=0x10005E:alpha={at}"
        )

    return ",".join(parts) if parts else "null"


def flash_filter(idx: int, shot: dict) -> str | None:
    if idx == 0:
        return f"fade=t=in:st=0:d={OPEN_FADE}:color=black"
    t = shot.get("transition", "")
    if t == "fadewhite":
        return f"fade=t=in:st=0:d={FLASH_DUR}:color=white"
    if t == "fadered":
        return f"fade=t=in:st=0:d={FLASH_DUR}:color=red"
    return None


def render_segment(idx: int, shot: dict, L: float, cfg: dict, *, dry: bool) -> Path:
    W, H, FPS = cfg["width"], cfg["height"], cfg["fps"]
    seg_out = SEGDIR / f"seg{idx:02d}.mp4"
    clip = CLIPDIR / f"{shot['id']}.mp4"
    technique = shot.get("technique", "procedural")

    inputs: list[str] = []
    motion = shot.get("motion", "kb_in")

    use_clip = clip.is_file()
    use_cel = (not use_clip) and technique == "handdrawn_cel" and \
        all((ROOT / f).is_file() for f in shot.get("frames", []))

    if use_clip:
        clipdur = ffprobe_duration(clip) or L
        factor = L / clipdur if clipdur else 1.0
        inputs += ["-i", str(clip)]
        pre = (f"[0:v]setpts=(PTS-STARTPTS)*{factor:.5f},fps={FPS},"
               f"trim=duration={L:.3f},setpts=PTS-STARTPTS[rt];")
        canvas = fill_canvas("[rt]", "comp")
        base = f"{pre}{canvas};[comp]scale={W}:{H},setsar=1[base]"
    elif use_cel:
        frames = [ROOT / f for f in shot["frames"]]
        K = len(frames)
        per = L / K
        xf = min(0.5, per * 0.6)
        for fr in frames:
            inputs += ["-loop", "1", "-framerate", str(FPS), "-t", f"{per + xf:.3f}", "-i", str(fr)]
        chain = []
        for i, _ in enumerate(frames):
            chain.append(f"[{i}:v]scale={W}:{H}:force_original_aspect_ratio=increase,"
                         f"crop={W}:{H},setsar=1[c{i}]")
        # xfade morph the keyframes
        prev = "[c0]"
        cum = per + xf
        for i in range(1, K):
            off = cum - xf
            lbl = f"[m{i}]"
            chain.append(f"{prev}[c{i}]xfade=transition=dissolve:duration={xf:.3f}:offset={off:.3f}{lbl}")
            prev = lbl
            cum = off + (per + xf)
        base = ";".join(chain) + f";{prev}trim=duration={L:.3f},setpts=PTS-STARTPTS[base]"
    else:
        plate = shot.get("plate") or shot.get("fallback_plate")
        inputs += ["-loop", "1", "-framerate", str(FPS), "-t", f"{L:.3f}", "-i", str(ROOT / plate)]
        canvas = fill_canvas("[0:v]", "comp")
        base = f"{canvas};[comp]{kenburns(motion, L, FPS, W, H)}[base]"

    tail_parts: list[str] = []
    fl = flash_filter(idx, shot)
    if fl:
        tail_parts.append(fl)
    tail_parts.append(overlays(idx, shot, L, W, H))
    tail_parts.append("format=yuv420p")
    tail = ",".join(p for p in tail_parts if p and p != "null") or "format=yuv420p"

    filtergraph = f"{base};[base]{tail}[v]"

    cmd = [
        "ffmpeg", "-y", *inputs,
        "-filter_complex", filtergraph,
        "-map", "[v]", "-an",
        "-c:v", "libx264", "-crf", "16", "-preset", "veryfast",
        "-pix_fmt", "yuv420p", "-r", str(FPS), "-t", f"{L:.3f}",
        str(seg_out),
    ]
    src = "clip" if use_clip else ("cel" if use_cel else "still")
    print(f"  seg{idx:02d} {shot['id']:22} {src:5} {motion:9} L={L:5.2f}s")
    run(cmd, dry=dry)
    return seg_out


def grade_chain(cfg: dict) -> str:
    W, H = cfg["width"], cfg["height"]
    bar = int(round(H * float(cfg.get("letterbox_frac", 0.055))))
    bar -= bar % 2
    grain = max(0, int(round(float(cfg.get("grain", 0.06)) * 50)))
    dur = float(cfg["duration"])
    chain = (
        "colorbalance=rs=-0.04:gs=-0.01:bs=0.05:rm=0.05:gm=0.02:bm=-0.03:"
        "rh=0.07:gh=0.03:bh=-0.06,"
        "eq=contrast=1.07:saturation=1.10:brightness=-0.01:gamma=0.98"
    )
    if cfg.get("vignette", True):
        chain += ",vignette=PI/5"
    if grain > 0:
        chain += f",noise=alls={grain}:allf=t"
    if bar > 0:
        chain += (f",drawbox=x=0:y=0:w={W}:h={bar}:color=black@1:t=fill"
                  f",drawbox=x=0:y={H-bar}:w={W}:h={bar}:color=black@1:t=fill")
    chain += f",fade=t=out:st={dur-1.6:.3f}:d=1.6,format=yuv420p"
    return chain


def assemble(segments: list[Path], starts: list[float], trans: list[float],
             cfg: dict, *, cut: bool, dry: bool) -> None:
    out_mp4 = ROOT / cfg["out_mp4"]
    out_mp4.parent.mkdir(parents=True, exist_ok=True)
    audio = ROOT / cfg["audio_bed"]
    FPS, DUR = cfg["fps"], float(cfg["duration"])
    N = len(segments)

    inputs: list[str] = []
    for s in segments:
        inputs += ["-i", str(s)]
    audio_idx = N
    inputs += ["-i", str(audio)]

    parts: list[str] = []
    if cut:
        parts.append("".join(f"[{i}:v]" for i in range(N))
                     + f"concat=n={N}:v=1:a=0[vc]")
        parts.append(f"[vc]{grade_chain(cfg)}[vout]")
    else:
        prev = "[0:v]"
        for i in range(1, N):
            out = f"[x{i}]"
            parts.append(
                f"{prev}[{i}:v]xfade=transition=dissolve:"
                f"duration={trans[i]:.3f}:offset={starts[i]:.3f}{out}"
            )
            prev = out
        parts.append(f"{prev}{grade_chain(cfg)}[vout]")
    filtergraph = ";".join(parts)

    cmd = [
        "ffmpeg", "-y", *inputs,
        "-filter_complex", filtergraph,
        "-map", "[vout]", "-map", f"{audio_idx}:a",
        "-c:v", "libx264", "-crf", "21", "-preset", "medium",
        "-x264-params", "aq-mode=3",
        "-pix_fmt", "yuv420p", "-r", str(FPS),
        "-c:a", "aac", "-b:a", "256k",
        "-t", f"{DUR:.3f}", "-movflags", "+faststart",
        str(out_mp4),
    ]
    print(f"\nAssembling {'(hard cut)' if cut else '(xfade)'} -> {out_mp4.relative_to(ROOT)}")
    run(cmd, dry=dry, log=True)


def encode_webm(cfg: dict, *, dry: bool) -> None:
    out_mp4 = ROOT / cfg["out_mp4"]
    out_webm = ROOT / cfg["out_webm"]
    cmd = [
        "ffmpeg", "-y", "-i", str(out_mp4),
        "-c:v", "libvpx-vp9", "-crf", "34", "-b:v", "0", "-row-mt", "1",
        "-deadline", "good", "-cpu-used", "4",
        "-pix_fmt", "yuv420p", "-c:a", "libopus", "-b:a", "160k",
        str(out_webm),
    ]
    print(f"Encoding webm -> {out_webm.relative_to(ROOT)}")
    run(cmd, dry=dry, log=True)


def main() -> None:
    ap = argparse.ArgumentParser(description="Assemble the Ryoko Owari cel trailer.")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--cut", action="store_true", help="Hard-cut concat instead of xfade chain")
    ap.add_argument("--skip-segments", action="store_true", help="Reuse rendered segments")
    ap.add_argument("--no-webm", action="store_true")
    args = ap.parse_args()

    data = json.loads(SHOTLIST.read_text(encoding="utf-8"))
    cfg = data["config"]
    shots = data["shots"]
    N = len(shots)
    DUR = float(cfg["duration"])
    default_xf = float(cfg.get("default_xf", 0.45))

    starts = [float(s["start"]) for s in shots]
    seg_len = [(starts[i + 1] - starts[i]) if i < N - 1 else (DUR - starts[i]) for i in range(N)]
    # transition INTO shot i (i>=1)
    trans = [0.0] * N
    for i in range(1, N):
        trans[i] = 0.15 if shots[i].get("transition") in ("fadewhite", "fadered") else default_xf
    # segment lengths include a tail (overlap) for the xfade into the NEXT shot
    if args.cut:
        seg_dur = list(seg_len)
    else:
        seg_dur = [seg_len[i] + (trans[i + 1] if i < N - 1 else 0.0) for i in range(N)]

    SEGDIR.mkdir(parents=True, exist_ok=True)
    TXTDIR.mkdir(parents=True, exist_ok=True)

    print(f"Trailer: {N} shots, {DUR:.2f}s, {cfg['width']}x{cfg['height']}@{cfg['fps']} "
          f"({'hard cut' if args.cut else 'xfade'})")
    segments: list[Path] = []
    for i, shot in enumerate(shots):
        seg = SEGDIR / f"seg{i:02d}.mp4"
        if args.skip_segments and seg.is_file():
            print(f"  seg{i:02d} {shot['id']:22} reuse")
            segments.append(seg)
            continue
        segments.append(render_segment(i, shot, seg_dur[i], cfg, dry=args.dry_run))

    assemble(segments, starts, trans, cfg, cut=args.cut, dry=args.dry_run)
    if not args.no_webm:
        encode_webm(cfg, dry=args.dry_run)

    if not args.dry_run:
        out_mp4 = ROOT / cfg["out_mp4"]
        d = ffprobe_duration(out_mp4)
        print(f"\nDONE: {out_mp4.relative_to(ROOT)} "
              f"({out_mp4.stat().st_size // 1024} KiB, {d:.2f}s)")
        if not args.no_webm:
            out_webm = ROOT / cfg["out_webm"]
            if out_webm.is_file():
                print(f"      {out_webm.relative_to(ROOT)} "
                      f"({out_webm.stat().st_size // 1024} KiB)")


if __name__ == "__main__":
    main()
