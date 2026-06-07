"""Per-CG composite builds. `python build_cgs.py all` or specific keys e.g. `cg1 cg5`."""
import sys
from PIL import Image, ImageOps, ImageEnhance
from compositor import (gen, chroma_cutout, autocrop_alpha, fit_height, fit_bg,
                        drop_shadow, lighting_overlay, vignette, save_cg, W, H)


def warm_grade(img, color=(255, 150, 50), amt=0.13, vig=0.30, contrast=1.05):
    img = img.convert("RGB")
    img = lighting_overlay(img, color, int(amt * 255))
    img = ImageEnhance.Contrast(img).enhance(contrast)
    img = vignette(img, vig)
    return img


def dawn_grade(img, color=(255, 224, 158), amt=0.17, vig=0.16, contrast=1.02):
    img = img.convert("RGB")
    img = lighting_overlay(img, color, int(amt * 255))
    img = ImageEnhance.Contrast(img).enhance(contrast)
    img = vignette(img, vig)
    return img


def shade_char(layer, factor=0.82, warm=(255, 170, 80), warm_amt=0.10):
    a = layer.split()[3]
    rgb = layer.convert("RGB")
    rgb = ImageEnhance.Brightness(rgb).enhance(factor)
    ov = Image.new("RGB", rgb.size, warm)
    rgb = Image.blend(rgb, ov, warm_amt)
    rgb = rgb.convert("RGBA")
    rgb.putalpha(a)
    return rgb


def prep(path, thresh=0.18, flip=False):
    c = autocrop_alpha(chroma_cutout(path, thresh=thresh))
    if flip:
        c = ImageOps.mirror(c)
    return c


def compose(bg, layers):
    """layers (back->front): (rgba, cx, baseline_y, target_h, shade_kw, shadow_kw)."""
    canvas = bg.convert("RGBA")
    for (char, cx, baseline, th, shade_kw, shadow_kw) in layers:
        im = fit_height(char, th)
        x = int(cx - im.width / 2)
        y = int(baseline - im.height)
        placed = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        placed.alpha_composite(im, (x, y))
        if shadow_kw is not None:
            canvas.alpha_composite(drop_shadow(placed, **shadow_kw))
        shaded = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        shaded.alpha_composite(shade_char(im, **shade_kw) if shade_kw else im, (x, y))
        canvas.alpha_composite(shaded)
    return canvas


# warm lamplight shade presets
WARM_DK = dict(factor=0.80, warm=(255, 158, 70), warm_amt=0.13)   # dark hall
WARM_MD = dict(factor=0.86, warm=(255, 165, 75), warm_amt=0.10)   # office
DAWN = dict(factor=0.98, warm=(255, 214, 150), warm_amt=0.13)     # dawn backlight
SHA = dict(blur=22, opacity=95, offset=(16, 24))
SHA_SOFT = dict(blur=28, opacity=70, offset=(12, 20))


# ---------------- PROLOGUE (office plate) ----------------
def cg1():
    """dance-disrobe: Toa dancing kosode off one shoulder; Kaoru watching from desk."""
    bg = fit_bg(gen("plate-prologue-office.png"))
    toa = prep(gen("char-toa-dance-offshoulder.png"))
    kaoru = prep(gen("char-kaoru-seated-cup.png"))
    layers = [
        (kaoru, 1200, 1018, 700, WARM_MD, SHA),
        (toa, 545, 1012, 905, WARM_MD, SHA),
    ]
    save_cg(warm_grade(compose(bg, layers)), "cg-prologue-dance-disrobe.png")


def cg2():
    """butt-wiggle-grab: Toa swaying glancing back; Kaoru reaching."""
    bg = fit_bg(gen("plate-prologue-office.png"))
    toa = prep(gen("char-toa-test-dance.png"))
    kaoru = prep(gen("char-kaoru-seated-reach.png"), flip=True)
    layers = [
        (kaoru, 1170, 1015, 720, WARM_MD, SHA),
        (toa, 560, 1010, 880, WARM_MD, SHA),
    ]
    save_cg(warm_grade(compose(bg, layers)), "cg-prologue-butt-wiggle-grab.png")


def cg3():
    """bent-over-desk: Toa leaning hands-on-desk; Kaoru standing close behind."""
    bg = fit_bg(gen("plate-prologue-office.png"))
    toa = prep(gen("char-toa-bent-desk.png"))
    kaoru = prep(gen("char-kaoru-standing.png"))
    layers = [
        (kaoru, 860, 1016, 980, WARM_MD, SHA),
        (toa, 545, 706, 632, WARM_MD, SHA),
    ]
    save_cg(warm_grade(compose(bg, layers)), "cg-prologue-bent-over-desk.png")


# ---------------- CASE 1 (lantern hall plate) ----------------
def cg4():
    """undress: Toa baring shoulders loosening obi; Kaoru near."""
    bg = fit_bg(gen("plate-case1-hall.png"))
    toa = prep(gen("char-toa-undress-standing.png"))
    kaoru = prep(gen("char-kaoru-standing.png"))
    layers = [
        (kaoru, 1085, 1018, 940, WARM_DK, SHA),
        (toa, 585, 1015, 760, WARM_DK, SHA),
    ]
    save_cg(warm_grade(compose(bg, layers), amt=0.12, vig=0.26),
            "cg-case1-r18-undress.png")


def cg5():
    """intimacy: close embrace on tatami, clothed-disheveled."""
    bg = fit_bg(gen("plate-case1-hall.png"))
    toa = prep(gen("char-toa-lean-embrace.png"))
    kaoru = prep(gen("char-kaoru-embrace-seated.png"))
    layers = [
        (kaoru, 905, 1024, 800, WARM_DK, SHA_SOFT),
        (toa, 660, 1024, 690, WARM_DK, SHA_SOFT),
    ]
    save_cg(warm_grade(compose(bg, layers), amt=0.13, vig=0.30),
            "cg-case1-r18-intimacy.png")


# ---------------- CASE 2 (dawn office plate) ----------------
def cg6():
    """morning: Toa slipping night-robe off shoulders; Kaoru drawing her back."""
    bg = fit_bg(gen("plate-case2-dawn.png"))
    toa = prep(gen("char-toa-morning-robe.png"))
    kaoru = prep(gen("char-kaoru-seated-reach.png"), flip=True)
    layers = [
        (kaoru, 1015, 1024, 800, DAWN, SHA_SOFT),
        (toa, 615, 1024, 748, DAWN, SHA_SOFT),
    ]
    save_cg(dawn_grade(compose(bg, layers)), "cg-case2-r18-morning.png")


def cg7():
    """afterglow: tender post-intimacy, both disheveled but covered."""
    bg = fit_bg(gen("plate-case2-dawn.png"))
    toa = prep(gen("char-toa-morning-robe.png"))
    kaoru = prep(gen("char-kaoru-embrace-seated.png"))
    kaoru_shade = dict(factor=1.08, warm=(255, 220, 158), warm_amt=0.10)
    layers = [
        (kaoru, 900, 1024, 760, kaoru_shade, SHA_SOFT),
        (toa, 690, 1024, 680, DAWN, SHA_SOFT),
    ]
    save_cg(dawn_grade(compose(bg, layers), amt=0.18, vig=0.14),
            "cg-case2-r18-afterglow.png")


BUILDS = {"cg1": cg1, "cg2": cg2, "cg3": cg3, "cg4": cg4,
          "cg5": cg5, "cg6": cg6, "cg7": cg7}

if __name__ == "__main__":
    keys = sys.argv[1:]
    if keys == ["all"] or not keys:
        keys = list(BUILDS)
    for k in keys:
        BUILDS[k]()
