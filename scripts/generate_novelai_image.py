#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Generate Ryoko Owari CG art via NovelAI Image API.

Requires NOVELAI_API_KEY in scripts/.env (Persistent API token from NovelAI settings).
See docs/novelai-image-pipeline.md and .cursor/skills/novelai-image-gen/SKILL.md.

Usage (project root):
    python scripts/generate_novelai_image.py --dry-run --preset prologue_embrace
    python scripts/generate_novelai_image.py --preset case1_lantern
    python scripts/generate_novelai_image.py --preset prologue_embrace --toa-ref --ref-strength 1.0
    python scripts/generate_novelai_image.py --preset test_festival
    python scripts/generate_novelai_image.py --preset prologue_embrace --style-ref
    python scripts/generate_novelai_image.py --no-char-ref --vibe
    python scripts/generate_novelai_image.py --prompt "..." --negative "..." --output assets/test.png
    python scripts/generate_novelai_image.py --list-presets
"""
from __future__ import annotations

import argparse
import base64
import io
import json
import os
import sys
import zipfile
from dataclasses import dataclass
from pathlib import Path
from typing import Literal
from urllib import error, request

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = ROOT / "scripts"
ENV_FILE = SCRIPTS_DIR / ".env"
PROMPTS_FILE = SCRIPTS_DIR / "novelai_prompts.json"

API_BASE = "https://image.novelai.net"
GENERATE_PATH = "/ai/generate-image"
# Match every existing game/images/cg/*.png (NovelAI "Large Landscape", multiple
# of 64). Max-quality defaults: 50 steps, k_euler_ancestral, scale 6.5.
DEFAULT_MODEL = "nai-diffusion-4-5-full"
DEFAULT_WIDTH = 1536
DEFAULT_HEIGHT = 1024
DEFAULT_STEPS = 50
DEFAULT_SCALE = 6.5
DEFAULT_SAMPLER = "k_euler_ancestral"
DEFAULT_ACTION = "generate"
REQUEST_TIMEOUT = 300

DEFAULT_TOA_REF = "game/images/reference/toa-precise-reference.png"
DEFAULT_KAORU_REF = "game/images/reference/kaoru-precise-reference.png"
DEFAULT_REF_STRENGTH = 1.0
DEFAULT_REF_FIDELITY = 1.0
DEFAULT_REF_TYPE: Literal["character", "style", "character&style"] = "character"
DEFAULT_STYLE_REF = "game/images/reference/style-painterly-reference.png"
DEFAULT_VIBE_SOURCE = "assets/reference/yone-style-vibe-source.png"
DEFAULT_STYLE_REF_STRENGTH = 0.45
DEFAULT_STYLE_REF_FIDELITY = 0.25
DEFAULT_VIBE_STRENGTH = 0.35

ROMANCE_PRESETS_WITH_CHAR_REFS = frozenset(
    {
        "prologue_proposition",
        "prologue_pull_close",
        "prologue_undressing",
        "prologue_embrace",
        "prologue_afterglow",
        "case1_lantern",
        "case2_morning",
        "prologue_embrace_mild",
        "case1_lantern_mild",
    }
)

RefType = Literal["character", "style", "character&style"]


@dataclass(frozen=True)
class DirectorRef:
    path: Path
    ref_type: RefType
    strength: float
    fidelity: float


def load_env_file(path: Path) -> None:
    if not path.exists():
        return
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, val = line.partition("=")
        os.environ.setdefault(key.strip(), val.strip().strip('"').strip("'"))


def get_api_key(*, required: bool = True) -> str:
    load_env_file(ENV_FILE)
    key = os.environ.get("NOVELAI_API_KEY", "").strip()
    if not key and required:
        print(
            "ERROR: NOVELAI_API_KEY is not set.\n"
            "  1. Copy scripts/.env.example to scripts/.env\n"
            "  2. Add your NovelAI Persistent API token (Account → User Settings)\n"
            "  3. Do not commit scripts/.env",
            file=sys.stderr,
        )
        raise SystemExit(2)
    return key


def load_prompt_config() -> dict:
    if not PROMPTS_FILE.exists():
        print(f"ERROR: Missing {PROMPTS_FILE}", file=sys.stderr)
        raise SystemExit(2)
    return json.loads(PROMPTS_FILE.read_text(encoding="utf-8"))


def expand_prompt(template: str, config: dict) -> str:
    meta = config.get("_meta", {})
    tags = dict(config.get("character_tags", {}))
    tags["style_tags"] = meta.get("style_tags", "")
    out = template
    for key, value in tags.items():
        out = out.replace("{" + key + "}", value)
    return out


def resolve_prompt_text(preset: dict | None, config: dict, cli_prompt: str | None) -> str:
    if cli_prompt:
        return cli_prompt
    if not preset:
        return ""
    template = preset["prompt"]
    if "{style_tags}" not in template:
        template = "{style_tags}, " + template
    return expand_prompt(template, config)


def build_negative(config: dict, preset: dict | None, cli_negative: str | None) -> str:
    meta = config.get("_meta", {})
    parts = [meta.get("shared_negative", ""), meta.get("style_negative", "")]
    if preset:
        extra = preset.get("negative_extra", "")
        if extra:
            parts.append(extra)
    if cli_negative:
        parts.append(cli_negative)
    return ", ".join(p for p in parts if p)


def default_sprite_refs(config: dict) -> dict[str, str]:
    meta = config.get("_meta", {})
    sprites = meta.get("char_ref_sprites", {})
    return {
        "toa": sprites.get("toa", DEFAULT_TOA_REF),
        "kaoru": sprites.get("kaoru", DEFAULT_KAORU_REF),
    }


def default_style_ref_path(config: dict) -> str:
    return config.get("_meta", {}).get("style_ref_sprite", DEFAULT_STYLE_REF)


def resolve_char_ref_paths(
    preset: dict | None,
    config: dict,
    *,
    cli_refs: list[str] | None,
    use_toa_ref: bool,
    use_kaoru_ref: bool,
    no_char_refs: bool,
    preset_name: str | None,
    require_files: bool = True,
) -> tuple[list[Path], list[Path]]:
    if no_char_refs:
        return [], []

    paths: list[str] = []
    sprites = default_sprite_refs(config)

    if cli_refs:
        paths.extend(cli_refs)
    if preset:
        if preset.get("char_refs"):
            paths.extend(preset["char_refs"])
        if preset.get("toa_ref"):
            paths.append(sprites["toa"])
        if preset.get("kaoru_ref"):
            paths.append(sprites["kaoru"])
    if use_toa_ref:
        paths.append(sprites["toa"])
    if use_kaoru_ref:
        paths.append(sprites["kaoru"])
    if (
        not paths
        and preset_name in ROMANCE_PRESETS_WITH_CHAR_REFS
        and config.get("_meta", {}).get("romance_presets_char_refs", True)
    ):
        paths.extend(sprites.values())

    planned: list[Path] = []
    resolved: list[Path] = []
    seen: set[str] = set()
    for raw in paths:
        p = (ROOT / raw).resolve()
        key = str(p)
        if key in seen:
            continue
        seen.add(key)
        planned.append(p)
        if not p.is_file():
            if require_files:
                print(f"ERROR: Character reference image not found: {p}", file=sys.stderr)
                raise SystemExit(2)
            print(f"WARN: Character reference missing (dry-run): {p}", file=sys.stderr)
            continue
        resolved.append(p)
    return planned, resolved


def encode_image_base64(path: Path) -> str:
    return base64.standard_b64encode(path.read_bytes()).decode("ascii")


def build_director_references(refs: list[DirectorRef]) -> dict[str, list]:
    """Map Precise Reference UI inputs to NovelAI V4.5 parameters (director_reference_*)."""
    if not refs:
        return {}

    type_caption = {
        "character": "character",
        "style": "style",
        "character&style": "character&style",
    }

    images: list[str] = []
    descriptions: list[dict] = []
    information_extracted: list[float] = []
    secondary_strength: list[float] = []
    strength_values: list[float] = []

    for ref in refs:
        images.append(encode_image_base64(ref.path))
        descriptions.append(
            {
                "caption": {
                    "base_caption": type_caption[ref.ref_type],
                    "char_captions": [],
                },
                "legacy_uc": False,
            }
        )
        information_extracted.append(1.0)
        secondary_strength.append(1.0 - float(ref.fidelity))
        strength_values.append(float(ref.strength))

    return {
        "director_reference_images": images,
        "director_reference_descriptions": descriptions,
        "director_reference_information_extracted": information_extracted,
        "director_reference_secondary_strength_values": secondary_strength,
        "director_reference_strength_values": strength_values,
    }


def resolve_style_ref_path(
    preset: dict | None,
    config: dict,
    *,
    cli_style_ref: str | None,
    no_style_ref: bool,
    preset_name: str | None,
    require_files: bool = True,
) -> tuple[Path | None, Path | None]:
    if no_style_ref:
        return None, None

    raw: str | None = None
    if cli_style_ref is not None:
        raw = cli_style_ref if cli_style_ref else default_style_ref_path(config)
    elif preset and preset.get("style_ref"):
        raw = preset.get("style_ref_path") or default_style_ref_path(config)
    elif (
        preset_name in ROMANCE_PRESETS_WITH_CHAR_REFS
        and config.get("_meta", {}).get("romance_presets_style_ref", False)
    ):
        raw = default_style_ref_path(config)

    if not raw:
        return None, None

    planned = (ROOT / raw).resolve()
    if not planned.is_file():
        if require_files:
            print(f"ERROR: Style reference image not found: {planned}", file=sys.stderr)
            raise SystemExit(2)
        print(f"WARN: Style reference missing (dry-run): {planned}", file=sys.stderr)
        return planned, None
    return planned, planned


def apply_vibe_transfer(parameters: dict, vibe_path: Path, strength: float) -> None:
    """Vibe Transfer — only when Precise Reference is not used."""
    parameters["reference_image_multiple"] = [encode_image_base64(vibe_path)]
    parameters["reference_strength_multiple"] = [float(strength)]
    parameters["reference_information_extracted_multiple"] = [1.0]
    parameters["normalize_reference_strength_multiple"] = True


def strip_vibe_transfer_fields(parameters: dict) -> None:
    """Vibe Transfer and Precise Reference are mutually exclusive on V4.5."""
    for key in (
        "reference_image",
        "reference_image_multiple",
        "reference_strength",
        "reference_strength_multiple",
        "reference_information_extracted",
        "reference_information_extracted_multiple",
        "normalize_reference_strength_multiple",
    ):
        parameters.pop(key, None)


def resolve_preset(name: str, config: dict) -> dict:
    presets = config.get("presets", {})
    if name not in presets:
        known = ", ".join(sorted(presets))
        print(f"ERROR: Unknown preset '{name}'. Known: {known}", file=sys.stderr)
        raise SystemExit(2)
    meta = config.get("_meta", {})
    preset = presets[name]
    prompt = resolve_prompt_text(preset, config, None)
    negative = build_negative(config, preset, None)
    output = preset.get("output", f"assets/cg/{name}.png")
    return {
        "name": name,
        "prompt": prompt,
        "negative": negative,
        "output": ROOT / output,
        "model": preset.get("model", meta.get("default_model", DEFAULT_MODEL)),
        "width": int(preset.get("width", meta.get("default_width", DEFAULT_WIDTH))),
        "height": int(preset.get("height", meta.get("default_height", DEFAULT_HEIGHT))),
        "steps": int(preset.get("steps", meta.get("default_steps", DEFAULT_STEPS))),
        "scale": float(preset.get("scale", meta.get("default_scale", DEFAULT_SCALE))),
        "sampler": preset.get("sampler", meta.get("default_sampler", DEFAULT_SAMPLER)),
        "seed": preset.get("seed"),
        "scene": preset.get("scene", ""),
        "toa_ref": bool(preset.get("toa_ref")),
        "kaoru_ref": bool(preset.get("kaoru_ref")),
        "char_refs": list(preset.get("char_refs", [])),
        "ref_strength": preset.get("ref_strength"),
        "ref_fidelity": preset.get("ref_fidelity"),
        "ref_type": preset.get("ref_type"),
        "style_ref": bool(preset.get("style_ref")),
        "style_ref_strength": preset.get("style_ref_strength"),
        "style_ref_fidelity": preset.get("style_ref_fidelity"),
    }


def build_request_body(
    prompt: str,
    negative: str,
    *,
    model: str,
    width: int,
    height: int,
    steps: int,
    scale: float,
    sampler: str,
    seed: int | None,
    director_refs: list[DirectorRef] | None = None,
    vibe_path: Path | None = None,
    vibe_strength: float = DEFAULT_VIBE_STRENGTH,
) -> dict:
    parameters: dict = {
        "params_version": 3,
        "width": width,
        "height": height,
        "scale": scale,
        "sampler": sampler,
        "steps": steps,
        "n_samples": 1,
        "ucPreset": 0,
        "qualityToggle": True,
        "sm": False,
        "sm_dyn": False,
        "dynamic_thresholding": False,
        "controlnet_strength": 1,
        "legacy": False,
        "add_original_image": True,
        "cfg_rescale": 0,
        "noise_schedule": "karras",
        "negative_prompt": negative,
        "legacy_v3_extend": False,
        "prefer_brownian": True,
    }

    # V4 / V4.5 models require the structured v4_prompt / v4_negative_prompt
    # payload (and use_coords / legacy_uc); omitting them returns HTTP 500.
    if "diffusion-4" in model:
        parameters.update(
            {
                "use_coords": False,
                "legacy_uc": False,
                "v4_prompt": {
                    "caption": {"base_caption": prompt, "char_captions": []},
                    "use_coords": False,
                    "use_order": True,
                },
                "v4_negative_prompt": {
                    "caption": {"base_caption": negative, "char_captions": []},
                    "legacy_uc": False,
                },
            }
        )

    if seed is not None:
        parameters["seed"] = int(seed)

    if director_refs:
        if "diffusion-4-5" not in model and "diffusion-4.5" not in model:
            print(
                "ERROR: Precise Reference (director_reference_*) requires a V4.5 model "
                f"(got {model}).",
                file=sys.stderr,
            )
            raise SystemExit(2)
        strip_vibe_transfer_fields(parameters)
        parameters.update(build_director_references(director_refs))
    elif vibe_path:
        apply_vibe_transfer(parameters, vibe_path, vibe_strength)

    return {
        "input": prompt,
        "model": model,
        "action": DEFAULT_ACTION,
        "parameters": parameters,
    }


def post_generate(body: dict, api_key: str) -> bytes:
    url = f"{API_BASE}{GENERATE_PATH}"
    data = json.dumps(body).encode("utf-8")
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        # NovelAI sits behind Cloudflare, which rejects urllib's default
        # User-Agent (Cloudflare error 1010). Present as a normal browser client.
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
            "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
        ),
        "Accept": "*/*",
        "Origin": "https://novelai.net",
        "Referer": "https://novelai.net/",
    }
    req = request.Request(url, data=data, headers=headers, method="POST")
    try:
        with request.urlopen(req, timeout=REQUEST_TIMEOUT) as resp:
            return resp.read()
    except error.HTTPError as e:
        detail = ""
        try:
            detail = e.read().decode("utf-8", errors="replace")
        except Exception:
            pass
        handle_http_error(e.code, detail)
        raise  # unreachable
    except error.URLError as e:
        print(f"ERROR: Network failure contacting NovelAI: {e}", file=sys.stderr)
        raise SystemExit(1) from e


def handle_http_error(code: int, detail: str) -> None:
    detail_short = detail[:800] if detail else "(no body)"
    if code == 401:
        msg = (
            "401 Unauthorized — invalid or expired NOVELAI_API_KEY.\n"
            "  Generate a new Persistent API token in NovelAI → User Settings."
        )
    elif code == 402:
        msg = (
            "402 Payment Required — insufficient Anlas / subscription inactive.\n"
            "  Top up or renew at https://novelai.net/"
        )
    elif code == 429:
        msg = "429 Too Many Requests — rate limited. Wait and retry."
    elif code in (400, 422):
        msg = (
            f"{code} Bad Request — check prompt length, width×height limits, or model name.\n"
            f"  API detail: {detail_short}"
        )
    else:
        msg = f"HTTP {code} from NovelAI.\n  API detail: {detail_short}"

    lowered = detail.lower()
    if any(
        token in lowered
        for token in ("policy", "blocked", "content", "moderation", "not allowed", "refused")
    ):
        msg += (
            "\n  Content policy may have blocked this prompt. Try a milder preset "
            "(e.g. prologue_embrace_mild) or reduce explicit tags."
        )

    print(f"ERROR: {msg}", file=sys.stderr)
    raise SystemExit(1)


def extract_first_png(payload: bytes) -> bytes:
    if payload[:4] == b"\x89PNG":
        return payload
    if payload[:2] != b"PK":
        print(
            "ERROR: Unexpected response (not PNG or ZIP). "
            "Check API key and endpoint.",
            file=sys.stderr,
        )
        raise SystemExit(1)
    with zipfile.ZipFile(io.BytesIO(payload)) as zf:
        names = [n for n in zf.namelist() if n.lower().endswith(".png")]
        if not names:
            print("ERROR: ZIP response contained no PNG files.", file=sys.stderr)
            raise SystemExit(1)
        return zf.read(names[0])


def save_png(png_bytes: bytes, out_path: Path) -> None:
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_bytes(png_bytes)
    print(f"Wrote {out_path} ({len(png_bytes) // 1024} KiB)")


def print_dry_run(resolved: dict, body: dict) -> None:
    print("DRY RUN - no API call")
    print(f"  preset:   {resolved.get('name', '(inline)')}")
    if resolved.get("scene"):
        print(f"  scene:    {resolved['scene']}")
    print(f"  output:   {resolved['output']}")
    print(f"  model:    {body['model']}")
    p = body["parameters"]
    print(f"  size:     {p['width']}x{p['height']}")
    print(f"  steps:    {p['steps']}  scale: {p['scale']}  sampler: {p['sampler']}")
    director_refs: list[DirectorRef] = resolved.get("director_refs") or []
    if director_refs:
        print(f"  precise ref: {len(director_refs)} reference(s)")
        for ref in director_refs:
            rel = ref.path.relative_to(ROOT)
            print(
                f"    - {rel} type={ref.ref_type} "
                f"strength={ref.strength} fidelity={ref.fidelity}"
            )
        print("  API fields: director_reference_images (+ per-ref type/strength/fidelity)")
        print("  vibe transfer: omitted (incompatible with Precise Reference)")
    elif resolved.get("vibe_path"):
        rel = resolved["vibe_path"].relative_to(ROOT)
        print(
            f"  vibe transfer: {rel} strength={resolved.get('vibe_strength')}"
        )
    print(f"  prompt:   {body['input'][:200]}...")
    print(f"  negative: {p['negative_prompt'][:120]}...")


def list_presets(config: dict) -> None:
    print("Romance / canon CG presets:")
    romance = [
        "prologue_proposition",
        "prologue_pull_close",
        "prologue_undressing",
        "prologue_embrace",
        "prologue_afterglow",
        "case1_lantern",
        "case2_morning",
    ]
    for name in romance:
        if name in config.get("presets", {}):
            p = config["presets"][name]
            print(f"  {name:24} -> {p.get('output', '?')}")
    print("\nMild alternates:")
    for name in ("prologue_embrace_mild", "case1_lantern_mild"):
        if name in config.get("presets", {}):
            p = config["presets"][name]
            print(f"  {name:24} -> {p.get('output', '?')}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate images via NovelAI API.")
    parser.add_argument("--preset", help="Preset name from novelai_prompts.json")
    parser.add_argument("--prompt", help="Override / inline positive prompt")
    parser.add_argument("--negative", help="Extra negative prompt (appended)")
    parser.add_argument("--output", type=Path, help="Output PNG path (relative to repo root)")
    parser.add_argument("--model", default=None, help=f"Model id (default {DEFAULT_MODEL})")
    parser.add_argument("--width", type=int, default=None)
    parser.add_argument("--height", type=int, default=None)
    parser.add_argument("--steps", type=int, default=None)
    parser.add_argument("--scale", type=float, default=None)
    parser.add_argument("--sampler", default=None)
    parser.add_argument("--seed", type=int, default=None)
    parser.add_argument("--dry-run", action="store_true", help="Print request; do not call API")
    parser.add_argument("--list-presets", action="store_true", help="List romance presets and exit")
    parser.add_argument(
        "--char-ref",
        action="append",
        dest="char_refs",
        metavar="PATH",
        help="Precise Reference image (repeatable; repo-relative path)",
    )
    parser.add_argument(
        "--ref-strength",
        type=float,
        default=None,
        help=f"director_reference_strength_values (0-1, default {DEFAULT_REF_STRENGTH})",
    )
    parser.add_argument(
        "--ref-fidelity",
        type=float,
        default=None,
        help=f"Fidelity via director_reference_secondary_strength_values as 1-fidelity "
        f"(default {DEFAULT_REF_FIDELITY})",
    )
    parser.add_argument(
        "--ref-type",
        choices=("character", "style", "character&style"),
        default=None,
        help=f"Reference mode (default {DEFAULT_REF_TYPE})",
    )
    parser.add_argument(
        "--toa-ref",
        action="store_true",
        help="Include default Toa sprite as Precise Reference",
    )
    parser.add_argument(
        "--kaoru-ref",
        action="store_true",
        help="Include default Kaoru sprite as Precise Reference",
    )
    parser.add_argument(
        "--no-char-ref",
        action="store_true",
        help="Disable preset/default character references for this run",
    )
    parser.add_argument(
        "--style-ref",
        nargs="?",
        const="",
        default=None,
        metavar="PATH",
        help="Style Precise Reference (type=style); --style-ref alone uses _meta.style_ref_sprite",
    )
    parser.add_argument(
        "--no-style-ref",
        action="store_true",
        help="Disable preset/default style reference for this run",
    )
    parser.add_argument(
        "--style-ref-strength",
        type=float,
        default=None,
        help=f"Style reference strength (default {DEFAULT_STYLE_REF_STRENGTH})",
    )
    parser.add_argument(
        "--style-ref-fidelity",
        type=float,
        default=None,
        help=f"Style reference fidelity (default {DEFAULT_STYLE_REF_FIDELITY})",
    )
    parser.add_argument(
        "--vibe",
        "--style-vibe",
        dest="vibe",
        nargs="?",
        const="",
        default=None,
        metavar="PATH",
        help="Vibe Transfer mood board when no Precise Reference; --vibe alone uses assets/reference/yone-style-vibe-source.png",
    )
    parser.add_argument(
        "--vibe-strength",
        type=float,
        default=None,
        help=f"Vibe Transfer strength 0-1 (default {DEFAULT_VIBE_STRENGTH})",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    config = load_prompt_config()
    meta = config.get("_meta", {})

    if args.list_presets:
        list_presets(config)
        return

    if args.preset:
        resolved = resolve_preset(args.preset, config)
        if args.prompt:
            resolved["prompt"] = args.prompt
        if args.negative:
            resolved["negative"] = build_negative(
                config, config["presets"][args.preset], args.negative
            )
        if args.output:
            resolved["output"] = ROOT / args.output
    elif args.prompt and args.output:
        resolved = {
            "name": "(inline)",
            "prompt": args.prompt,
            "negative": build_negative(config, None, args.negative),
            "output": ROOT / args.output,
            "model": args.model or meta.get("default_model", DEFAULT_MODEL),
            "width": args.width or meta.get("default_width", DEFAULT_WIDTH),
            "height": args.height or meta.get("default_height", DEFAULT_HEIGHT),
            "steps": args.steps or meta.get("default_steps", DEFAULT_STEPS),
            "scale": args.scale if args.scale is not None else meta.get("default_scale", DEFAULT_SCALE),
            "sampler": args.sampler or meta.get("default_sampler", DEFAULT_SAMPLER),
            "seed": args.seed,
            "scene": "",
        }
    else:
        print(
            "ERROR: Provide --preset NAME or both --prompt and --output.\n"
            "  Try: python scripts/generate_novelai_image.py --list-presets",
            file=sys.stderr,
        )
        raise SystemExit(2)

    for field in ("model", "width", "height", "steps", "scale", "sampler", "seed"):
        cli_val = getattr(args, field, None)
        if cli_val is not None and field != "seed":
            resolved[field] = cli_val
        elif cli_val is not None:
            resolved["seed"] = cli_val

    preset_dict = config["presets"].get(args.preset) if args.preset else None
    char_ref_planned, char_ref_paths = resolve_char_ref_paths(
        preset_dict,
        config,
        cli_refs=args.char_refs,
        use_toa_ref=args.toa_ref,
        use_kaoru_ref=args.kaoru_ref,
        no_char_refs=args.no_char_ref,
        preset_name=args.preset,
        require_files=not args.dry_run,
    )
    style_ref_planned, style_ref_path = resolve_style_ref_path(
        preset_dict,
        config,
        cli_style_ref=args.style_ref,
        no_style_ref=args.no_style_ref,
        preset_name=args.preset,
        require_files=not args.dry_run,
    )

    ref_strength = (
        args.ref_strength
        if args.ref_strength is not None
        else (
            resolved.get("ref_strength")
            if resolved.get("ref_strength") is not None
            else meta.get("ref_strength", DEFAULT_REF_STRENGTH)
        )
    )
    ref_fidelity = (
        args.ref_fidelity
        if args.ref_fidelity is not None
        else (
            resolved.get("ref_fidelity")
            if resolved.get("ref_fidelity") is not None
            else meta.get("ref_fidelity", DEFAULT_REF_FIDELITY)
        )
    )
    ref_type: RefType = args.ref_type or resolved.get("ref_type") or DEFAULT_REF_TYPE

    style_ref_strength = (
        args.style_ref_strength
        if args.style_ref_strength is not None
        else (
            resolved.get("style_ref_strength")
            if resolved.get("style_ref_strength") is not None
            else meta.get("style_ref_strength", DEFAULT_STYLE_REF_STRENGTH)
        )
    )
    style_ref_fidelity = (
        args.style_ref_fidelity
        if args.style_ref_fidelity is not None
        else (
            resolved.get("style_ref_fidelity")
            if resolved.get("style_ref_fidelity") is not None
            else meta.get("style_ref_fidelity", DEFAULT_STYLE_REF_FIDELITY)
        )
    )

    director_refs: list[DirectorRef] = []
    for path in char_ref_paths:
        director_refs.append(
            DirectorRef(
                path=path,
                ref_type=ref_type,
                strength=float(ref_strength),
                fidelity=float(ref_fidelity),
            )
        )
    if style_ref_path:
        director_refs.append(
            DirectorRef(
                path=style_ref_path,
                ref_type="style",
                strength=float(style_ref_strength),
                fidelity=float(style_ref_fidelity),
            )
        )

    vibe_path: Path | None = None
    vibe_strength = (
        args.vibe_strength
        if args.vibe_strength is not None
        else meta.get("vibe_strength", DEFAULT_VIBE_STRENGTH)
    )
    if args.vibe is not None and not director_refs:
        raw_vibe = args.vibe if args.vibe else DEFAULT_VIBE_SOURCE
        vibe_candidate = (ROOT / raw_vibe).resolve()
        if not vibe_candidate.is_file():
            if args.dry_run:
                print(f"WARN: Vibe source missing (dry-run): {vibe_candidate}", file=sys.stderr)
            else:
                print(f"ERROR: Vibe source image not found: {vibe_candidate}", file=sys.stderr)
                raise SystemExit(2)
        else:
            vibe_path = vibe_candidate

    resolved["char_ref_planned"] = char_ref_planned
    resolved["char_ref_paths"] = char_ref_paths
    resolved["style_ref_planned"] = style_ref_planned
    resolved["style_ref_path"] = style_ref_path
    resolved["director_refs"] = director_refs
    resolved["vibe_path"] = vibe_path
    resolved["vibe_strength"] = float(vibe_strength)

    body = build_request_body(
        resolved["prompt"],
        resolved["negative"],
        model=resolved["model"],
        width=int(resolved["width"]),
        height=int(resolved["height"]),
        steps=int(resolved["steps"]),
        scale=float(resolved["scale"]),
        sampler=resolved["sampler"],
        seed=resolved.get("seed"),
        director_refs=director_refs or None,
        vibe_path=vibe_path,
        vibe_strength=float(vibe_strength),
    )

    if args.dry_run:
        print_dry_run(resolved, body)
        return

    api_key = get_api_key(required=True)
    print(
        f"Generating {resolved.get('name')} "
        f"({body['parameters']['width']}x{body['parameters']['height']})..."
    )
    raw = post_generate(body, api_key)
    png = extract_first_png(raw)
    save_png(png, Path(resolved["output"]))


if __name__ == "__main__":
    main()
