#!/usr/bin/env python3
"""Generate labeled low-poly mannequin GLBs for Toa and Kaoru.

These are BLOCKING PLACEHOLDERS — not production anime character meshes.
Requires: pip install trimesh numpy scipy

Usage:
    python scripts/generate_3d_placeholders.py
    python scripts/generate_3d_placeholders.py --out assets/3d
"""

from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
import trimesh

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUT = ROOT / "assets" / "3d"

# Character colors (hex from docs/3d-character-spec-toa-kaoru.md)
COLORS = {
    "toa_hair": [0.96, 0.96, 0.96, 1.0],
    "toa_kimono": [0.10, 0.10, 0.10, 1.0],
    "toa_hakama": [0.98, 0.98, 0.98, 1.0],
    "toa_skin": [0.94, 0.87, 0.82, 1.0],
    "kaoru_hair": [0.36, 0.25, 0.20, 1.0],
    "kaoru_robe": [0.79, 0.64, 0.15, 1.0],
    "kaoru_under": [0.16, 0.09, 0.06, 1.0],
    "kaoru_skin": [0.90, 0.82, 0.76, 1.0],
}


def _cylinder(radius: float, height: float, sections: int = 12) -> trimesh.Trimesh:
    return trimesh.creation.cylinder(radius=radius, height=height, sections=sections)


def _box(extents: tuple[float, float, float]) -> trimesh.Trimesh:
    return trimesh.creation.box(extents=extents)


def _colored(mesh: trimesh.Trimesh, rgba: list[float]) -> trimesh.Trimesh:
    mesh = mesh.copy()
    mesh.visual.face_colors = np.tile(np.array(rgba), (len(mesh.faces), 1)).astype(np.uint8)
    return mesh


def _translate(mesh: trimesh.Trimesh, xyz: tuple[float, float, float]) -> trimesh.Trimesh:
    m = mesh.copy()
    m.apply_translation(xyz)
    return m


def build_mannequin(
    height_m: float,
    shoulder_w: float,
    parts: list[tuple[trimesh.Trimesh, list[float], tuple[float, float, float]]],
) -> trimesh.Trimesh:
    """Stack colored primitives into a rough humanoid silhouette."""
    meshes = []
    for primitive, color, offset in parts:
        meshes.append(_colored(_translate(primitive, offset), color))
    combined = trimesh.util.concatenate(meshes)
    combined.metadata = {"height_m": height_m, "shoulder_w": shoulder_w}
    return combined


def toa_mannequin() -> trimesh.Trimesh:
    """180 cm blocking figure — witness kosode + hakama hint."""
    h = 1.80
    parts: list[tuple[trimesh.Trimesh, list[float], tuple[float, float, float]]] = [
        (_cylinder(0.11, 0.22), COLORS["toa_skin"], (0, 0, 1.69)),  # head
        (_cylinder(0.13, 0.08), COLORS["toa_hair"], (0, 0, 1.82)),  # hair cap
        (_box((0.36, 0.18, 0.42)), COLORS["toa_kimono"], (0, 0, 1.38)),  # torso/kosode
        (_cylinder(0.07, 0.38), COLORS["toa_skin"], (-0.24, 0, 1.38)),  # L arm
        (_cylinder(0.07, 0.38), COLORS["toa_skin"], (0.24, 0, 1.38)),  # R arm
        (_box((0.34, 0.22, 0.52)), COLORS["toa_hakama"], (0, 0, 0.92)),  # hakama block
        (_cylinder(0.09, 0.48), COLORS["toa_kimono"], (-0.10, 0, 0.52)),  # L leg
        (_cylinder(0.09, 0.48), COLORS["toa_kimono"], (0.10, 0, 0.52)),  # R leg
        (_box((0.38, 0.06, 0.04)), COLORS["toa_kimono"], (0, 0.10, 1.12)),  # obi band
    ]
    return build_mannequin(h, 0.38, parts)


def kaoru_mannequin() -> trimesh.Trimesh:
    """173 cm blocking figure — gold haori silhouette."""
    h = 1.73
    parts: list[tuple[trimesh.Trimesh, list[float], tuple[float, float, float]]] = [
        (_cylinder(0.10, 0.21), COLORS["kaoru_skin"], (0, 0, 1.62)),
        (_cylinder(0.11, 0.06), COLORS["kaoru_hair"], (0, 0, 1.74)),
        (_box((0.12, 0.08, 0.06)), COLORS["kaoru_hair"], (0, -0.12, 1.66)),  # ponytail
        (_box((0.40, 0.20, 0.44)), COLORS["kaoru_robe"], (0, 0, 1.32)),  # haori
        (_box((0.32, 0.16, 0.38)), COLORS["kaoru_under"], (0, 0, 1.30)),  # under kimono
        (_cylinder(0.075, 0.36), COLORS["kaoru_skin"], (-0.26, 0, 1.32)),
        (_cylinder(0.075, 0.36), COLORS["kaoru_skin"], (0.26, 0, 1.32)),
        (_cylinder(0.085, 0.46), COLORS["kaoru_under"], (-0.11, 0, 0.49)),
        (_cylinder(0.085, 0.46), COLORS["kaoru_under"], (0.11, 0, 0.49)),
    ]
    return build_mannequin(h, 0.44, parts)


def export_glb(mesh: trimesh.Trimesh, path: Path, label: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    mesh.export(path, file_type="glb")
    size_kb = path.stat().st_size / 1024
    print(f"  wrote {path.relative_to(ROOT)} ({size_kb:.1f} KB) — {label}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate Toa/Kaoru placeholder GLBs")
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT, help="Output directory")
    args = parser.parse_args()

    print("Generating PLACEHOLDER mannequins (not anime meshes)...")
    export_glb(toa_mannequin(), args.out / "toa-placeholder.glb", "Toa 180cm witness block")
    export_glb(kaoru_mannequin(), args.out / "kaoru-placeholder.glb", "Kaoru 173cm magistrate block")
    print("Done. See docs/3d-character-spec-toa-kaoru.md for production specs.")


if __name__ == "__main__":
    main()
