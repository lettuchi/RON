"""Composite tasteful R-18 CGs for Ryoko Owari from solo green-screen character
gens + background plates. Single-character GenerateImage workflow.

All output is 1536x1024.
"""
import os
import numpy as np
from PIL import Image, ImageFilter, ImageChops, ImageDraw

# Where GenerateImage writes its output (project assets folder).
GEN = r"C:\Users\Amanda\.cursor\projects\c-Users-Amanda-Developer-ryoko-owari\assets"
# Workspace folders
ROOT = r"C:\Users\Amanda\Developer\ryoko-owari"
CG = os.path.join(ROOT, "game", "images", "cg")
BUILD = os.path.join(ROOT, "assets", "cg-build")
OUT = os.path.join(BUILD, "out")

W, H = 1536, 1024


def gen(name):
    return os.path.join(GEN, name)


def chroma_cutout(path, key=(0, 177, 64), thresh=0.18, despill=True, feather=1.5):
    """Remove a flat chroma-(green) background. Returns RGBA Image.

    Uses a greenness metric: green dominance over red/blue. Robust to the
    slightly painterly / gradient backgrounds GenerateImage produces.
    """
    im = Image.open(path).convert("RGB")
    arr = np.asarray(im).astype(np.float32) / 255.0
    r, g, b = arr[..., 0], arr[..., 1], arr[..., 2]
    # greenness: how much green exceeds the brighter of r/b, normalized
    greenness = g - np.maximum(r, b)
    # alpha: 1 where character (low greenness), 0 where background (high greenness)
    a = np.clip((thresh - greenness) / thresh, 0.0, 1.0)
    # Anything strongly green is fully transparent
    a[greenness > thresh] = 0.0
    alpha = (a * 255).astype(np.uint8)
    out = arr.copy()
    if despill:
        # reduce green spill on semi-transparent edges
        spill = np.maximum(g - np.maximum(r, b), 0.0)
        # only despill where there's notable spill
        mask = spill > 0.02
        avg = (r + b) / 2.0
        g2 = np.where(mask, np.minimum(g, avg + 0.05), g)
        out[..., 1] = g2
    rgba = (np.dstack([out, alpha.astype(np.float32) / 255.0]) * 255).astype(np.uint8)
    img = Image.fromarray(rgba, "RGBA")
    if feather:
        a_ch = img.split()[3].filter(ImageFilter.GaussianBlur(feather))
        img.putalpha(a_ch)
    return img


def autocrop_alpha(img, pad=0):
    """Crop to non-transparent bounding box."""
    a = np.asarray(img.split()[3])
    ys, xs = np.where(a > 12)
    if len(xs) == 0:
        return img
    x0, x1 = xs.min(), xs.max()
    y0, y1 = ys.min(), ys.max()
    x0 = max(0, x0 - pad); y0 = max(0, y0 - pad)
    x1 = min(img.width, x1 + pad); y1 = min(img.height, y1 + pad)
    return img.crop((x0, y0, x1 + 1, y1 + 1))


def fit_height(img, target_h):
    scale = target_h / img.height
    return img.resize((max(1, int(img.width * scale)), int(target_h)), Image.LANCZOS)


def fit_bg(path):
    """Open a plate and cover-crop to 1536x1024."""
    im = Image.open(path).convert("RGB")
    s = max(W / im.width, H / im.height)
    im = im.resize((int(im.width * s + 0.5), int(im.height * s + 0.5)), Image.LANCZOS)
    x = (im.width - W) // 2
    y = (im.height - H) // 2
    return im.crop((x, y, x + W, y + H))


def drop_shadow(layer, blur=22, opacity=110, offset=(14, 26)):
    """Build a soft drop shadow RGBA the size of the canvas from a placed layer.
    `layer` is an RGBA already positioned on a WxH transparent canvas."""
    a = layer.split()[3]
    shadow = Image.new("RGBA", layer.size, (0, 0, 0, 0))
    solid = Image.new("RGBA", layer.size, (0, 0, 0, opacity))
    shadow.paste(solid, offset, a)
    shadow = shadow.filter(ImageFilter.GaussianBlur(blur))
    return shadow


def place(canvas_size, img, cx, baseline_y, target_h):
    """Scale img to target_h, return (placed_on_transparent_canvas).
    cx = horizontal center (px), baseline_y = bottom y (px)."""
    im = fit_height(img, target_h)
    x = int(cx - im.width / 2)
    y = int(baseline_y - im.height)
    canvas = Image.new("RGBA", canvas_size, (0, 0, 0, 0))
    canvas.alpha_composite(im, (x, y))
    return canvas


def lighting_overlay(base, color, opacity, mode="soft"):
    """Apply a unifying color wash. color=(r,g,b), opacity 0-255."""
    overlay = Image.new("RGB", base.size, color)
    return Image.blend(base, overlay, opacity / 255.0)


def vignette(base, strength=0.35):
    w, h = base.size
    mask = Image.new("L", (w, h), 0)
    d = ImageDraw.Draw(mask)
    d.ellipse([-w * 0.25, -h * 0.25, w * 1.25, h * 1.25], fill=255)
    mask = mask.filter(ImageFilter.GaussianBlur(min(w, h) * 0.12))
    dark = Image.new("RGB", (w, h), (0, 0, 0))
    return Image.composite(base, dark, mask.point(lambda v: int(255 - (255 - v) * strength)))


def save_cg(img, name):
    img = img.convert("RGB")
    assert img.size == (W, H), f"bad size {img.size}"
    p = os.path.join(OUT, name)
    img.save(p)
    print("saved", p, img.size)
    return p


if __name__ == "__main__":
    # quick cutout test
    t = chroma_cutout(gen("char-toa-test-dance.png"))
    t = autocrop_alpha(t)
    t.save(os.path.join(BUILD, "test-toa-cut.png"))
    print("toa cut size", t.size)
