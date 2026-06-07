#!/usr/bin/env python3
"""Meshy image-to-3D REST pipeline for Ryoko Owari character refs.

Loads MESHY_API_KEY from scripts/.env (never commit .env).
Downloads GLB outputs to assets/3d/raw/meshy-YYYY-MM-DD/ (Meshy URLs expire ~3 days).

Canonical refs: docs/3d-character-spec-toa-kaoru.md
Prompt packs: scripts/3d_model_request_template.md
Setup: docs/meshy-setup.md

Examples (project root):
    python scripts/meshy_image_to_3d.py --check
    python scripts/meshy_image_to_3d.py --character toa
    python scripts/meshy_image_to_3d.py --image game/images/sprites/kaoru/kaoru-smirk.png
    python scripts/meshy_image_to_3d.py --character toa --dry-run

Deps: Python 3.10+ stdlib only (urllib). Optional: pip install requests (not required).
"""
from __future__ import annotations

import argparse
import base64
import json
import mimetypes
import os
import sys
import time
from datetime import date
from pathlib import Path
from typing import Any
from urllib import error, request

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = ROOT / "scripts"
ENV_FILE = SCRIPTS_DIR / ".env"
RAW_BASE = ROOT / "assets" / "3d" / "raw"

API_BASE = "https://api.meshy.ai"
BALANCE_PATH = "/openapi/v1/balance"
IMAGE_TO_3D_PATH = "/openapi/v1/image-to-3d"

CHARACTER_REFS: dict[str, Path] = {
    "toa": ROOT / "game/images/sprites/toa/toa-neutral.png",
    "kaoru": ROOT / "game/images/sprites/kaoru/kaoru-smirk.png",
}

DEFAULT_POLL_SEC = 15.0
DEFAULT_TIMEOUT_SEC = 1800.0
REQUEST_TIMEOUT = 120


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
    key = os.environ.get("MESHY_API_KEY", "").strip()
    if not key and required:
        print(
            "ERROR: MESHY_API_KEY is not set.\n"
            "  1. Copy scripts/.env.example to scripts/.env\n"
            "  2. Add your key from https://www.meshy.ai/settings/api\n"
            "  3. Do not commit scripts/.env",
            file=sys.stderr,
        )
        raise SystemExit(2)
    return key


def api_request(
    method: str,
    path: str,
    api_key: str,
    *,
    body: dict[str, Any] | None = None,
) -> Any:
    url = f"{API_BASE}{path}"
    data = None
    headers = {"Authorization": f"Bearer {api_key}"}
    if body is not None:
        data = json.dumps(body).encode("utf-8")
        headers["Content-Type"] = "application/json"
    req = request.Request(url, data=data, headers=headers, method=method)
    try:
        with request.urlopen(req, timeout=REQUEST_TIMEOUT) as resp:
            raw = resp.read().decode("utf-8")
            if not raw.strip():
                return {}
            return json.loads(raw)
    except error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"HTTP {exc.code} {exc.reason}: {detail}") from exc


def image_to_data_uri(path: Path) -> str:
    if not path.is_file():
        raise FileNotFoundError(path)
    mime, _ = mimetypes.guess_type(path.name)
    if mime not in ("image/png", "image/jpeg"):
        suffix = path.suffix.lower()
        if suffix == ".png":
            mime = "image/png"
        elif suffix in (".jpg", ".jpeg"):
            mime = "image/jpeg"
        else:
            raise ValueError(f"Unsupported image type: {path} (use .png or .jpg)")
    encoded = base64.standard_b64encode(path.read_bytes()).decode("ascii")
    return f"data:{mime};base64,{encoded}"


def cmd_check(api_key: str) -> int:
    if not api_key:
        print("ERROR: MESHY_API_KEY is not set.", file=sys.stderr)
        return 2
    if not api_key.startswith("msy_"):
        print("WARNING: key does not start with msy_ (unexpected format).", file=sys.stderr)
    print("Checking Meshy API...")
    try:
        data = api_request("GET", BALANCE_PATH, api_key)
        balance = data.get("balance")
        print(f"  balance: {balance} credits")
        print("  OK — key accepted.")
        return 0
    except Exception as exc:  # noqa: BLE001
        print(f"  FAILED: {exc}", file=sys.stderr)
        return 1


def create_image_to_3d_task(api_key: str, image_path: Path) -> str:
    payload = {
        "image_url": image_to_data_uri(image_path),
        "should_texture": True,
        "enable_pbr": True,
        "target_formats": ["glb"],
        "ai_model": "latest",
    }
    data = api_request("POST", IMAGE_TO_3D_PATH, api_key, body=payload)
    task_id = data.get("result") or data.get("id")
    if not task_id:
        raise RuntimeError(f"Unexpected create response: {data}")
    return str(task_id)


def poll_task(
    api_key: str,
    task_id: str,
    *,
    poll_sec: float,
    timeout_sec: float,
) -> dict[str, Any]:
    deadline = time.monotonic() + timeout_sec
    while True:
        task = api_request("GET", f"{IMAGE_TO_3D_PATH}/{task_id}", api_key)
        status = task.get("status", "")
        progress = task.get("progress")
        prog_txt = f" {progress}%" if progress is not None else ""
        print(f"  status={status}{prog_txt}")
        if status == "SUCCEEDED":
            return task
        if status in ("FAILED", "CANCELED"):
            err = task.get("task_error") or {}
            raise RuntimeError(f"Task {status}: {err.get('message') or task}")
        if time.monotonic() > deadline:
            raise TimeoutError(f"Timed out after {timeout_sec}s (task {task_id})")
        time.sleep(poll_sec)


def download_url(url: str, dest: Path) -> None:
    dest.parent.mkdir(parents=True, exist_ok=True)
    req = request.Request(url, method="GET")
    with request.urlopen(req, timeout=REQUEST_TIMEOUT) as resp:
        dest.write_bytes(resp.read())


def output_dir_for_today() -> Path:
    return RAW_BASE / f"meshy-{date.today().isoformat()}"


def run_generation(
    api_key: str,
    image_path: Path,
    *,
    out_name: str,
    poll_sec: float,
    timeout_sec: float,
    dry_run: bool,
) -> int:
    out_dir = output_dir_for_today()
    out_path = out_dir / out_name
    print(f"Input:  {image_path.relative_to(ROOT)}")
    print(f"Output: {out_path.relative_to(ROOT)}")
    if dry_run:
        print("DRY RUN - no API calls.")
        return 0
    print("Creating image-to-3d task (consumes Meshy credits)...")
    task_id = create_image_to_3d_task(api_key, image_path)
    print(f"  task_id={task_id}")
    print("Polling...")
    task = poll_task(api_key, task_id, poll_sec=poll_sec, timeout_sec=timeout_sec)
    urls = task.get("model_urls") or {}
    glb_url = urls.get("glb")
    if not glb_url:
        raise RuntimeError(f"No model_urls.glb in response: {task}")
    credits = task.get("consumed_credits")
    print(f"Downloading GLB ({credits} credits consumed)...")
    download_url(glb_url, out_path)
    print(f"Saved {out_path} ({out_path.stat().st_size:,} bytes)")
    meta_path = out_path.with_suffix(".json")
    meta_path.write_text(
        json.dumps(
            {
                "task_id": task_id,
                "source_image": str(image_path.relative_to(ROOT)).replace("\\", "/"),
                "consumed_credits": credits,
                "thumbnail_url": task.get("thumbnail_url"),
            },
            indent=2,
        ),
        encoding="utf-8",
    )
    print(f"Wrote {meta_path.name}")
    return 0


def resolve_image_and_name(
    character: str | None,
    image: str | None,
) -> tuple[Path, str]:
    if character and image:
        raise SystemExit("ERROR: use only one of --character or --image.")
    if character:
        key = character.lower()
        if key not in CHARACTER_REFS:
            raise SystemExit(f"ERROR: --character must be one of: {', '.join(CHARACTER_REFS)}")
        path = CHARACTER_REFS[key]
        out_name = f"{key}-work-meshy.glb" if key == "toa" else f"{key}-meshy.glb"
        return path, out_name
    if image:
        path = Path(image)
        if not path.is_absolute():
            path = ROOT / path
        stem = path.stem.replace(" ", "-")
        return path, f"{stem}-meshy.glb"
    raise SystemExit("ERROR: provide --character toa|kaoru or --image PATH.")


def main() -> int:
    ap = argparse.ArgumentParser(description="Meshy image-to-3D for Toa/Kaoru refs.")
    ap.add_argument("--check", action="store_true", help="Validate API key and credit balance.")
    ap.add_argument("--character", choices=sorted(CHARACTER_REFS), help="Locked sprite ref.")
    ap.add_argument("--image", help="Single reference image path (repo-relative or absolute).")
    ap.add_argument("--dry-run", action="store_true", help="Print paths only; no paid API calls.")
    ap.add_argument("--poll-interval", type=float, default=DEFAULT_POLL_SEC)
    ap.add_argument("--timeout", type=float, default=DEFAULT_TIMEOUT_SEC)
    args = ap.parse_args()

    load_env_file(ENV_FILE)
    api_key = os.environ.get("MESHY_API_KEY", "").strip()

    if args.check:
        return cmd_check(api_key)

    if not args.character and not args.image:
        ap.print_help()
        return 2

    image_path, out_name = resolve_image_and_name(args.character, args.image)
    if not image_path.is_file():
        print(f"ERROR: missing reference image: {image_path}", file=sys.stderr)
        return 2

    if not api_key and not args.dry_run:
        get_api_key(required=True)

    if api_key and not args.dry_run:
        rc = cmd_check(api_key)
        if rc != 0:
            return rc

    try:
        return run_generation(
            api_key,
            image_path,
            out_name=out_name,
            poll_sec=args.poll_interval,
            timeout_sec=args.timeout,
            dry_run=args.dry_run,
        )
    except Exception as exc:  # noqa: BLE001
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
