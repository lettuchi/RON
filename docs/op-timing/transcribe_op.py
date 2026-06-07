#!/usr/bin/env python3
"""Measure real vocal timings in game/audio/bgm/opening_op.mp3 for OP subtitle sync.

Read-only analysis (does NOT modify game/audio/). Outputs:
  docs/op-timing/op_timing.json

Approach (the dense techno mix defeats Silero VAD, so):
  1. Whisper (vad_filter OFF) transcribes the whole track -> segment + word start
     times. Japanese text on singing is imperfect, but the onset TIMES are useful
     and the OP line order is known (docs/menu-song-lyrics.md / OP_SONG).
  2. A numpy energy + vocal-band (300-3400 Hz) spectral-flux novelty detector
     finds phrase onsets independently, as a cross-check / fallback.
"""
import json
import sys
from pathlib import Path

import numpy as np
from faster_whisper import WhisperModel, decode_audio

# Windows console is cp1252; force UTF-8 so Japanese segment text can print.
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

ROOT = Path(__file__).resolve().parents[2]
AUDIO = ROOT / "game" / "audio" / "bgm" / "opening_op.mp3"
OUT = Path(__file__).resolve().parent / "op_timing.json"
MODEL = sys.argv[1] if len(sys.argv) > 1 else "small"

SR = 16000
print(f"decoding {AUDIO} ...")
audio = decode_audio(str(AUDIO), sampling_rate=SR).astype(np.float32)
dur = len(audio) / SR
print(f"duration = {dur:.3f}s  ({MODEL} model)")

# --- numpy onset detection (vocal-band spectral flux) ---------------------
hop = 512
win = 2048
window = np.hanning(win).astype(np.float32)
n_frames = 1 + max(0, (len(audio) - win) // hop)
freqs = np.fft.rfftfreq(win, 1.0 / SR)
band = (freqs >= 300) & (freqs <= 3400)   # vocal formant band
mag = np.zeros((n_frames, band.sum()), dtype=np.float32)
rms = np.zeros(n_frames, dtype=np.float32)
for i in range(n_frames):
    fr = audio[i * hop:i * hop + win] * window
    rms[i] = float(np.sqrt(np.mean(fr * fr)) + 1e-9)
    mag[i] = np.abs(np.fft.rfft(fr))[band]
# spectral flux: positive change of vocal-band magnitude
flux = np.zeros(n_frames, dtype=np.float32)
flux[1:] = np.maximum(0.0, (mag[1:] - mag[:-1]).sum(axis=1))
# normalize + smooth
flux = flux / (flux.max() + 1e-9)
k = 5
flux_s = np.convolve(flux, np.ones(k) / k, mode="same")
# peak pick: local max above adaptive threshold, min 0.6s apart
thr = flux_s.mean() + 0.6 * flux_s.std()
min_gap = int(0.6 * SR / hop)
onsets = []
last = -10 ** 9
for i in range(1, n_frames - 1):
    if flux_s[i] >= thr and flux_s[i] >= flux_s[i - 1] and flux_s[i] >= flux_s[i + 1]:
        if i - last >= min_gap:
            onsets.append(round(i * hop / SR, 3))
            last = i
print(f"energy/flux onsets ({len(onsets)}): {onsets}")

# --- Whisper transcription (no vad filter) --------------------------------
print(f"loading whisper model ({MODEL}, int8 cpu) ...")
model = WhisperModel(MODEL, device="cpu", compute_type="int8")
print("transcribing (ja, vad_filter=False) ...")
segments, info = model.transcribe(
    str(AUDIO), language="ja", word_timestamps=True, vad_filter=False,
    beam_size=5, condition_on_previous_text=False, no_speech_threshold=0.9,
)
segs = []
for s in segments:
    words = [{"w": w.word, "s": round(w.start, 3), "e": round(w.end, 3)}
             for w in (s.words or [])]
    segs.append({"start": round(s.start, 3), "end": round(s.end, 3),
                 "text": s.text, "words": words})
    print(f"  [{s.start:6.2f} -> {s.end:6.2f}] {s.text}")

OUT.write_text(json.dumps(
    {"duration": round(dur, 3), "model": MODEL,
     "flux_onsets": onsets, "segments": segs},
    ensure_ascii=False, indent=2), encoding="utf-8")
print(f"wrote {OUT}")
