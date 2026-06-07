"""Composite ED replacement stills (1536x1024) for game/images/ed/.

Workflow: GenerateImage solo characters on chroma green + background plates,
then PIL composite (see compositor.py). Run after assets are in GEN folder:

    python assets/cg-build/build_ed_cgs.py all
    python scripts/install_ed_cgs.py

Plates may be copied from existing game/images/ed/ vistas (no character).
"""
from __future__ import annotations

import os
import sys

from PIL import Image, ImageEnhance

from build_cgs import prep, compose, warm_grade, shade_char
from compositor import W, H, fit_bg, gen, save_cg

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
ED_SRC = os.path.join(ROOT, "game", "images", "ed")

# Sunset canal / bridge grade (match existing ED golden hour)
SUNSET = dict(factor=0.88, warm=(255, 168, 72), warm_amt=0.12)
SUNSET_DK = dict(factor=0.82, warm=(255, 140, 60), warm_amt=0.14)
NIGHT = dict(factor=0.78, warm=(255, 120, 50), warm_amt=0.10)
SHA = dict(blur=22, opacity=95, offset=(14, 24))
SHA_SOFT = dict(blur=28, opacity=70, offset=(12, 20))


def _plate_existing(filename: str) -> Image.Image:
    path = os.path.join(ED_SRC, filename)
    if not os.path.isfile(path):
        raise FileNotFoundError(path)
    return fit_bg(path)


def _twilight_grade(img: Image.Image) -> Image.Image:
    img = img.convert("RGB")
    overlay = Image.new("RGB", img.size, (30, 35, 75))
    img = Image.blend(img, overlay, 0.42)
    img = ImageEnhance.Brightness(img).enhance(0.72)
    return warm_grade(img, color=(180, 90, 120), amt=0.08, vig=0.38, contrast=1.04)


def ed_canal_pursuit():
    bg = _plate_existing("ed-canal-dusk-vista.png")
    kaoru = prep(gen("char-ed-kaoru-pursuit.png"))
    layers = [(kaoru, 720, 1010, 920, SUNSET, SHA)]
    save_cg(warm_grade(compose(bg, layers), amt=0.11, vig=0.28), "ed-kaoru-canal-pursuit.png")


def ed_watches_return():
    bg = _plate_existing("ed-canal-dusk-vista.png")
    kaoru = prep(gen("char-ed-kaoru-watches.png"), thresh=0.16)
    layers = [(kaoru, 1180, 1012, 880, SUNSET_DK, SHA)]
    save_cg(warm_grade(compose(bg, layers), amt=0.12, vig=0.32), "ed-kaoru-watches-return.png")


def ed_bridge_chorus():
    bg = _plate_existing("ed-bridge-red-thread.png")
    kaoru = prep(gen("char-ed-kaoru-bridge-thread.png"))
    layers = [(kaoru, 640, 1015, 900, SUNSET, SHA)]
    save_cg(warm_grade(compose(bg, layers), amt=0.10, vig=0.26), "ed-kaoru-bridge-red-bind.png")


def ed_toa_bridge_mid_chorus():
    bg = _plate_existing("ed-bridge-red-thread.png")
    toa = prep(gen("char-ed-toa-run-chorus.png"))
    layers = [(toa, 560, 1012, 900, SUNSET, SHA)]
    save_cg(warm_grade(compose(bg, layers), amt=0.10, vig=0.26), "ed-toa-bridge-run-mid-chorus.png")


def ed_canal_twilight():
    bg = _plate_existing("ed-canal-dusk-vista.png")
    save_cg(_twilight_grade(bg), "ed-canal-twilight-ink.png")


def ed_canal_night():
    bg = _twilight_grade(_plate_existing("ed-canal-dusk-vista.png"))
    kaoru = prep(gen("char-ed-kaoru-night-lantern.png"))
    layers = [(kaoru, 700, 1010, 900, NIGHT, SHA)]
    save_cg(warm_grade(compose(bg, layers), color=(255, 130, 55), amt=0.14, vig=0.36),
            "ed-kaoru-canal-night-lantern.png")


def ed_name_retrace():
    bg = fit_bg(gen("plate-ed-office-night.png"))
    hands = prep(gen("char-ed-kaoru-hands-scroll.png"), thresh=0.15)
    layers = [(hands, 768, 820, 520, dict(factor=0.85, warm=(255, 165, 75), warm_amt=0.11), None)]
    save_cg(warm_grade(compose(bg, layers), amt=0.13, vig=0.30), "ed-office-name-retrace.png")


def ed_toa_bridge_instrumental():
    bg = _plate_existing("ed-bridge-red-thread.png")
    toa = prep(gen("char-ed-toa-distant.png"), thresh=0.16)
    layers = [(toa, 768, 720, 220, SUNSET, SHA_SOFT)]
    save_cg(warm_grade(compose(bg, layers), amt=0.09, vig=0.22), "ed-toa-bridge-instrumental.png")


def ed_toa_bridge_final_cho():
    bg = _plate_existing("ed-bridge-red-thread.png")
    toa = prep(gen("char-ed-toa-final-chorus.png"))
    layers = [(toa, 620, 1012, 880, SUNSET, SHA)]
    save_cg(warm_grade(compose(bg, layers), amt=0.10, vig=0.26), "ed-toa-bridge-final-chorus.png")


def ed_toa_bridge_hesitant():
    bg = _plate_existing("ed-bridge-red-thread.png")
    toa = prep(gen("char-ed-toa-hesitant.png"))
    layers = [(toa, 700, 1012, 860, SUNSET, SHA)]
    save_cg(warm_grade(compose(bg, layers), amt=0.10, vig=0.26), "ed-toa-bridge-hesitant.png")


def ed_sleep_red_thread():
    bg = fit_bg(gen("plate-ed-office-night.png"))
    toa = prep(gen("char-ed-toa-sleeping.png"))
    kaoru = prep(gen("char-ed-kaoru-tie-thread.png"), thresh=0.16)
    office_shade = dict(factor=0.84, warm=(255, 155, 70), warm_amt=0.12)
    layers = [
        (toa, 720, 1020, 520, office_shade, SHA_SOFT),
        (kaoru, 1050, 1018, 780, office_shade, SHA),
    ]
    save_cg(warm_grade(compose(bg, layers), amt=0.14, vig=0.32), "ed-office-sleep-red-thread.png")


def ed_hands_second_knot_native():
    """Full-frame native still (no composite) — must exist as char-ed-hands-knot.png."""
    src = gen("char-ed-hands-knot.png")
    if not os.path.isfile(src):
        raise FileNotFoundError(src)
    im = fit_bg(src)
    save_cg(warm_grade(im, amt=0.08, vig=0.20), "ed-hands-second-knot.png")


BUILDS = {
    "pursuit": ed_canal_pursuit,
    "watches": ed_watches_return,
    "bridge_chorus": ed_bridge_chorus,
    "toa_run": ed_toa_bridge_mid_chorus,
    "twilight": ed_canal_twilight,
    "canal_night": ed_canal_night,
    "name_retrace": ed_name_retrace,
    "toa_far": ed_toa_bridge_instrumental,
    "toa_final": ed_toa_bridge_final_cho,
    "toa_hesitant": ed_toa_bridge_hesitant,
    "sleep_thread": ed_sleep_red_thread,
    "hands": ed_hands_second_knot_native,
}

if __name__ == "__main__":
    keys = sys.argv[1:]
    if keys in (["all"], []):
        keys = list(BUILDS)
    for k in keys:
        print(f"--- {k} ---")
        BUILDS[k]()
