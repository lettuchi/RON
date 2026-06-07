"""PG-13 intimate-track CG composites (1536x1024). Replaces R-18 compositor builds.

Requires char-pg13-* assets in Cursor assets/ (see scripts/generate_pg13_char_list.md).
Run: python scripts/make_cg_plates.py
     python assets/cg-build/build_pg13_cgs.py all
     python scripts/install_intimate_cgs.py
"""
import sys

from PIL import Image, ImageEnhance

from build_cgs import prep, compose, warm_grade, dawn_grade, shade_char
from compositor import W, H, fit_bg, gen, save_cg

WARM_MD = dict(factor=0.86, warm=(255, 165, 75), warm_amt=0.10)
WARM_DK = dict(factor=0.80, warm=(255, 158, 70), warm_amt=0.13)
DAWN = dict(factor=0.98, warm=(255, 214, 150), warm_amt=0.13)
SHA = dict(blur=22, opacity=95, offset=(16, 24))
SHA_SOFT = dict(blur=28, opacity=70, offset=(12, 20))


def pg1_dance_disrobe():
    """Graceful dance — kosode on, obi intact; Kaoru watches from desk."""
    bg = fit_bg(gen("plate-prologue-office.png"))
    toa = prep(gen("char-pg13-toa-dance-grace.png"))
    kaoru = prep(gen("char-pg13-kaoru-desk-cup.png"))
    layers = [
        (kaoru, 1200, 1018, 700, WARM_MD, SHA),
        (toa, 545, 1012, 905, WARM_MD, SHA),
    ]
    save_cg(warm_grade(compose(bg, layers)), "cg-prologue-dance-disrobe.png")


def pg2_dance_closer():
    """Face-to-face dance tension — hands almost meeting, no rear presentation."""
    bg = fit_bg(gen("plate-prologue-office.png"))
    toa = prep(gen("char-pg13-toa-dance-facing.png"))
    kaoru = prep(gen("char-pg13-kaoru-standing-hand.png"))
    layers = [
        (kaoru, 1085, 1016, 940, WARM_MD, SHA),
        (toa, 620, 1012, 880, WARM_MD, SHA),
    ]
    save_cg(warm_grade(compose(bg, layers)), "cg-prologue-butt-wiggle-grab.png")


def pg3_desk_moment():
    """Toa at desk with scroll; Kaoru close behind, hand on shoulder — clothed."""
    bg = fit_bg(gen("plate-prologue-office.png"))
    toa = prep(gen("char-pg13-toa-desk-scroll.png"))
    kaoru = prep(gen("char-pg13-kaoru-shoulder.png"))
    layers = [
        (kaoru, 860, 1016, 980, WARM_MD, SHA),
        (toa, 545, 706, 632, WARM_MD, SHA),
    ]
    save_cg(warm_grade(compose(bg, layers)), "cg-prologue-bent-over-desk.png")


def pg4_steamy_obi():
    """Toa kneeling adjusting obi; Kaoru watching — fully clothed."""
    bg = fit_bg(gen("plate-prologue-office.png"))
    toa = prep(gen("char-pg13-toa-obi-kneel.png"))
    kaoru = prep(gen("char-pg13-kaoru-desk-cup.png"))
    layers = [
        (kaoru, 1185, 1018, 720, WARM_MD, SHA),
        (toa, 600, 1015, 780, WARM_MD, SHA),
    ]
    save_cg(warm_grade(compose(bg, layers)), "cg-canon-steamy-undress-toa.png")


def pg5_steamy_embrace():
    """Tatami embrace — both clothed."""
    bg = fit_bg(gen("plate-prologue-office.png"))
    toa = prep(gen("char-pg13-toa-embrace-seated.png"))
    kaoru = prep(gen("char-pg13-kaoru-embrace-seated.png"))
    layers = [
        (kaoru, 905, 1024, 800, WARM_MD, SHA_SOFT),
        (toa, 660, 1024, 690, WARM_MD, SHA_SOFT),
    ]
    save_cg(warm_grade(compose(bg, layers), vig=0.28), "cg-canon-steamy-intimacy.png")


def pg6_steamy_afterglow():
    """Seated close after intimacy — robes neat, lantern glow."""
    bg = fit_bg(gen("plate-prologue-office.png"))
    toa = prep(gen("char-pg13-toa-afterglow-seated.png"))
    kaoru = prep(gen("char-pg13-kaoru-afterglow-seated.png"))
    layers = [
        (kaoru, 920, 1024, 760, WARM_MD, SHA_SOFT),
        (toa, 700, 1024, 680, WARM_MD, SHA_SOFT),
    ]
    save_cg(warm_grade(compose(bg, layers), amt=0.11, vig=0.24),
            "cg-canon-steamy-afterglow.png")


def pg7_case1_obi():
    """Lantern hall — obi adjustment, clothed."""
    bg = fit_bg(gen("plate-case1-hall.png"))
    toa = prep(gen("char-pg13-toa-hall-obi.png"))
    kaoru = prep(gen("char-pg13-kaoru-standing-hand.png"))
    layers = [
        (kaoru, 1085, 1018, 940, WARM_DK, SHA),
        (toa, 585, 1015, 760, WARM_DK, SHA),
    ]
    save_cg(warm_grade(compose(bg, layers), amt=0.12, vig=0.26),
            "cg-case1-r18-undress.png")


def pg8_case1_embrace():
    bg = fit_bg(gen("plate-case1-hall.png"))
    toa = prep(gen("char-pg13-toa-embrace-seated.png"))
    kaoru = prep(gen("char-pg13-kaoru-embrace-seated.png"))
    layers = [
        (kaoru, 905, 1024, 800, WARM_DK, SHA_SOFT),
        (toa, 660, 1024, 690, WARM_DK, SHA_SOFT),
    ]
    save_cg(warm_grade(compose(bg, layers), amt=0.13, vig=0.30),
            "cg-case1-r18-intimacy.png")


def pg9_case2_morning():
    """Dawn tea — hand on knuckle, both clothed."""
    bg = fit_bg(gen("plate-case2-dawn.png"))
    img = dawn_grade(bg.convert("RGB"), amt=0.20, vig=0.12)
    bg = ImageEnhance.Brightness(img).enhance(1.08)
    toa = prep(gen("char-pg13-toa-tea-seated.png"))
    kaoru = prep(gen("char-pg13-kaoru-tea-pour.png"))
    layers = [
        (kaoru, 1015, 1024, 800, DAWN, SHA_SOFT),
        (toa, 615, 1024, 748, DAWN, SHA_SOFT),
    ]
    save_cg(dawn_grade(compose(bg, layers)), "cg-case2-r18-morning.png")


def pg10_case2_afterglow():
    bg = fit_bg(gen("plate-case2-dawn.png"))
    img = dawn_grade(bg.convert("RGB"), amt=0.18, vig=0.14)
    bg = ImageEnhance.Brightness(img).enhance(1.06)
    toa = prep(gen("char-pg13-toa-cushion-rest.png"))
    kaoru = prep(gen("char-pg13-kaoru-cushion-close.png"))
    kaoru_shade = dict(factor=1.08, warm=(255, 220, 158), warm_amt=0.10)
    layers = [
        (kaoru, 900, 1024, 760, kaoru_shade, SHA_SOFT),
        (toa, 690, 1024, 680, DAWN, SHA_SOFT),
    ]
    save_cg(dawn_grade(compose(bg, layers), amt=0.18, vig=0.14),
            "cg-case2-r18-afterglow.png")


BUILDS = {
    "pg1": pg1_dance_disrobe,
    "pg2": pg2_dance_closer,
    "pg3": pg3_desk_moment,
    "pg4": pg4_steamy_obi,
    "pg5": pg5_steamy_embrace,
    "pg6": pg6_steamy_afterglow,
    "pg7": pg7_case1_obi,
    "pg8": pg8_case1_embrace,
    "pg9": pg9_case2_morning,
    "pg10": pg10_case2_afterglow,
}

if __name__ == "__main__":
    keys = sys.argv[1:]
    if keys in (["all"], []):
        keys = list(BUILDS)
    for k in keys:
        print(f"--- {k} ---")
        BUILDS[k]()
