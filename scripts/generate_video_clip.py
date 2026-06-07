#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Generate Ryoko Owari cel-trailer motion clips via the fal.ai image-to-video API.

Turns the generated cel keyframes (trailer/frames/*.png) into real AI-motion MP4s
in trailer/clips/<shot_id>.mp4. scripts/build_trailer.py auto-picks up any clip it
finds there and falls back to procedural Ken-Burns motion when a clip is absent, so
this script is an OPTIONAL upgrade step (see trailer/README.md).

Requires FAL_KEY in scripts/.env  (format "<key_id>:<key_secret>").
Get a key at https://fal.ai/dashboard/keys  and copy scripts/.env.example -> scripts/.env.

Uses the fal *queue* REST API (stdlib urllib only, no fal_client dependency):
    POST https://queue.fal.run/<model>      -> {request_id, status_url, response_url}
    GET  <status_url>  (poll until COMPLETED)
    GET  <response_url>                      -> {"video": {"url": "...mp4"}}

Usage (project root):
    python scripts/generate_video_clip.py --list-presets
    python scripts/generate_video_clip.py --dry-run --preset toa_fan
    python scripts/generate_video_clip.py --preset toa_fan
    python scripts/generate_video_clip.py --preset kaoru_turn --duration 5
    python scripts/generate_video_clip.py --preset embrace --no-end-image
    python scripts/generate_video_clip.py \
        --start-image trailer/frames/toa-fan-1.png \
        --end-image   trailer/frames/toa-fan-3.png \
        --prompt "..." --out trailer/clips/s04_toa_fan.mp4

Default model: fal-ai/kling-video/v2/standard/image-to-video  (start + end-frame
interpolation via image_url + tail_image_url). Open-weights alternative that also
runs on fal: fal-ai/wan-i2v (single start frame; pass --no-end-image and --model).
Browse model ids at https://fal.ai/models.
"""
from __future__ import annotations

import argparse
import base64
import json
import mimetypes
import os
import sys
import time
import uuid
from pathlib import Path
from urllib import error, request

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = ROOT / "scripts"
ENV_FILE = SCRIPTS_DIR / ".env"
PRESETS_FILE = ROOT / "trailer" / "video_presets.json"

QUEUE_BASE = "https://queue.fal.run"
STORAGE_UPLOAD_URL = "https://rest.alpha.fal.ai/storage/upload"

# Kling v2 image-to-video supports a start frame (image_url) plus an optional end
# frame (tail_image_url), giving true keyframe-1 -> keyframe-3 inbetweening.
DEFAULT_MODEL = "fal-ai/kling-video/v2/standard/image-to-video"
# Open-weights alternative on fal (single start frame, no tail frame):
ALT_MODEL = "fal-ai/wan-i2v"

DEFAULT_DURATION = 5
DEFAULT_ASPECT_RATIO = "16:9"
DEFAULT_IMAGE_KEY = "image_url"
DEFAULT_TAIL_IMAGE_KEY = "tail_image_url"
DEFAULT_POLL_INTERVAL = 4.0
DEFAULT_TIMEOUT = 900.0
REQUEST_TIMEOUT = 120

USER_AGENT = "ryoko-owari-trailer/1.0 (+https://fal.ai)"


# ---------------------------------------------------------------------------
# Config / credentials (mirrors scripts/generate_novelai_image.py conventions)
# ---------------------------------------------------------------------------
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
    key = os.environ.get("FAL_KEY", "").strip()
    if not key and required:
        print(
            "ERROR: FAL_KEY is not set.\n"
            "  1. Copy scripts/.env.example to scripts/.env\n"
            '  2. Add your fal.ai key as FAL_KEY=<key_id>:<key_secret>\n'
            "     (create one at https://fal.ai/dashboard/keys)\n"
            "  3. Do not commit scripts/.env",
            file=sys.stderr,
        )
        raise SystemExit(2)
    return key


def load_presets() -> dict:
    if not PRESETS_FILE.exists():
        print(f"ERROR: Missing {PRESETS_FILE}", file=sys.stderr)
        raise SystemExit(2)
    try:
        return json.loads(PRESETS_FILE.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        print(f"ERROR: {PRESETS_FILE} is not valid JSON: {e}", file=sys.stderr)
        raise SystemExit(2) from e


def resolve_preset(name: str, config: dict) -> dict:
    presets = config.get("presets", {})
    if name not in presets:
        known = ", ".join(sorted(presets))
        print(f"ERROR: Unknown preset '{name}'. Known: {known}", file=sys.stderr)
        raise SystemExit(2)
    meta = config.get("_meta", {})
    preset = presets[name]

    start_image = preset.get("start_image") or preset.get("image")
    end_image = preset.get("end_image") or preset.get("tail_image")
    out = preset.get("out") or preset.get("output") or f"trailer/clips/{name}.mp4"

    return {
        "name": name,
        "model": preset.get("model", meta.get("default_model", DEFAULT_MODEL)),
        "prompt": preset.get("prompt", ""),
        "negative_prompt": preset.get("negative_prompt", ""),
        "duration": preset.get("duration", DEFAULT_DURATION),
        "aspect_ratio": preset.get(
            "aspect_ratio", meta.get("aspect_ratio", DEFAULT_ASPECT_RATIO)
        ),
        "start_image": start_image,
        "end_image": end_image,
        "out": out,
    }


# ---------------------------------------------------------------------------
# Image inputs: upload to fal storage (best effort) or fall back to data: URI
# ---------------------------------------------------------------------------
def encode_data_uri(path: Path) -> str:
    mime = mimetypes.guess_type(path.name)[0] or "image/png"
    b64 = base64.standard_b64encode(path.read_bytes()).decode("ascii")
    return f"data:{mime};base64,{b64}"


def upload_to_fal_storage(path: Path, api_key: str) -> str | None:
    """Best-effort multipart upload to fal storage; returns a public URL or None.

    The exact storage response shape varies, so we probe a few common URL keys and
    fall back (via the caller) to a base64 data: URI on any failure.
    """
    mime = mimetypes.guess_type(path.name)[0] or "application/octet-stream"
    boundary = f"----ryoko{uuid.uuid4().hex}"
    pre = (
        f"--{boundary}\r\n"
        f'Content-Disposition: form-data; name="file"; filename="{path.name}"\r\n'
        f"Content-Type: {mime}\r\n\r\n"
    ).encode("utf-8")
    post = f"\r\n--{boundary}--\r\n".encode("utf-8")
    body = pre + path.read_bytes() + post

    headers = {
        "Authorization": f"Key {api_key}",
        "Content-Type": f"multipart/form-data; boundary={boundary}",
        "Accept": "application/json",
        "User-Agent": USER_AGENT,
    }
    req = request.Request(STORAGE_UPLOAD_URL, data=body, headers=headers, method="POST")
    try:
        with request.urlopen(req, timeout=REQUEST_TIMEOUT) as resp:
            raw = resp.read().decode("utf-8", errors="replace").strip()
    except (error.HTTPError, error.URLError, TimeoutError) as e:
        print(f"  WARN: fal storage upload failed ({e}); using inline data URI.",
              file=sys.stderr)
        return None

    if raw.startswith("http"):
        return raw.strip('"')
    try:
        data = json.loads(raw)
    except json.JSONDecodeError:
        print("  WARN: unexpected storage response; using inline data URI.",
              file=sys.stderr)
        return None
    for key in ("access_url", "file_url", "url", "download_url"):
        val = data.get(key) if isinstance(data, dict) else None
        if isinstance(val, str) and val.startswith("http"):
            return val
    print("  WARN: storage response had no URL field; using inline data URI.",
          file=sys.stderr)
    return None


def resolve_image_ref(
    raw: str, api_key: str, *, dry_run: bool, prefer_data_uri: bool, label: str
) -> str:
    """Return a value usable in the model `image_url`/`tail_image_url` field."""
    path = (ROOT / raw).resolve()
    if not path.is_file():
        msg = f"{label} image not found: {path}"
        if dry_run:
            print(f"WARN: {msg} (dry-run)", file=sys.stderr)
            return f"<missing:{raw}>"
        print(f"ERROR: {msg}", file=sys.stderr)
        raise SystemExit(2)

    if dry_run:
        return f"<image:{raw}>"

    if not prefer_data_uri:
        url = upload_to_fal_storage(path, api_key)
        if url:
            print(f"  {label}: uploaded to fal storage -> {url}")
            return url
    size_kib = path.stat().st_size // 1024
    print(f"  {label}: inline base64 data URI ({size_kib} KiB source)")
    return encode_data_uri(path)


# ---------------------------------------------------------------------------
# Request building + queue polling
# ---------------------------------------------------------------------------
def build_input(resolved: dict, config: dict, start_url: str, end_url: str | None) -> dict:
    meta = config.get("_meta", {})
    image_key = meta.get("image_key", DEFAULT_IMAGE_KEY)
    tail_key = meta.get("tail_image_key", DEFAULT_TAIL_IMAGE_KEY)

    payload: dict = {
        "prompt": resolved["prompt"],
        image_key: start_url,
        "duration": str(resolved["duration"]),
        "aspect_ratio": resolved["aspect_ratio"],
    }
    if resolved.get("negative_prompt"):
        payload["negative_prompt"] = resolved["negative_prompt"]
    if end_url:
        payload[tail_key] = end_url
    return payload


def _http_json(req: request.Request) -> dict:
    try:
        with request.urlopen(req, timeout=REQUEST_TIMEOUT) as resp:
            raw = resp.read().decode("utf-8", errors="replace")
    except error.HTTPError as e:
        detail = ""
        try:
            detail = e.read().decode("utf-8", errors="replace")
        except Exception:
            pass
        handle_http_error(e.code, detail)
        raise  # unreachable
    except error.URLError as e:
        print(f"ERROR: Network failure contacting fal.ai: {e}", file=sys.stderr)
        raise SystemExit(1) from e
    return json.loads(raw) if raw.strip() else {}


def submit_request(model: str, input_payload: dict, api_key: str) -> dict:
    url = f"{QUEUE_BASE}/{model}"
    data = json.dumps(input_payload).encode("utf-8")
    headers = {
        "Authorization": f"Key {api_key}",
        "Content-Type": "application/json",
        "Accept": "application/json",
        "User-Agent": USER_AGENT,
    }
    req = request.Request(url, data=data, headers=headers, method="POST")
    return _http_json(req)


def get_json(url: str, api_key: str) -> dict:
    headers = {
        "Authorization": f"Key {api_key}",
        "Accept": "application/json",
        "User-Agent": USER_AGENT,
    }
    req = request.Request(url, headers=headers, method="GET")
    return _http_json(req)


def poll_until_done(
    status_url: str, api_key: str, *, poll_interval: float, timeout: float
) -> dict:
    deadline = time.monotonic() + timeout
    last = ""
    while True:
        status = get_json(status_url, api_key)
        state = status.get("status", "")
        if state and state != last:
            extra = ""
            if state == "IN_QUEUE" and "queue_position" in status:
                extra = f" (position {status['queue_position']})"
            print(f"  status: {state}{extra}")
            last = state
        if state == "COMPLETED":
            if status.get("error"):
                print(f"ERROR: fal reported failure: {status['error']}", file=sys.stderr)
                raise SystemExit(1)
            return status
        if time.monotonic() > deadline:
            print(
                f"ERROR: Timed out after {timeout:.0f}s waiting for the clip "
                f"(last status: {state or 'unknown'}).",
                file=sys.stderr,
            )
            raise SystemExit(1)
        time.sleep(poll_interval)


def extract_video_url(result: dict) -> str:
    video = result.get("video")
    if isinstance(video, dict) and isinstance(video.get("url"), str):
        return video["url"]
    if isinstance(result.get("video_url"), str):
        return result["video_url"]
    videos = result.get("videos")
    if isinstance(videos, list) and videos:
        first = videos[0]
        if isinstance(first, dict) and isinstance(first.get("url"), str):
            return first["url"]
    print(
        "ERROR: Could not find a video URL in the fal response.\n"
        f"  Response keys: {sorted(result)}",
        file=sys.stderr,
    )
    raise SystemExit(1)


def download_video(url: str, out_path: Path) -> None:
    out_path.parent.mkdir(parents=True, exist_ok=True)
    req = request.Request(url, headers={"User-Agent": USER_AGENT}, method="GET")
    try:
        with request.urlopen(req, timeout=REQUEST_TIMEOUT) as resp:
            data = resp.read()
    except (error.HTTPError, error.URLError) as e:
        print(f"ERROR: Failed to download clip from {url}: {e}", file=sys.stderr)
        raise SystemExit(1) from e
    out_path.write_bytes(data)
    print(f"Wrote {out_path} ({len(data) // 1024} KiB)")


def handle_http_error(code: int, detail: str) -> None:
    detail_short = detail[:800] if detail else "(no body)"
    if code == 401:
        msg = (
            "401 Unauthorized — invalid or missing FAL_KEY.\n"
            '  Check scripts/.env: FAL_KEY=<key_id>:<key_secret> '
            "(create one at https://fal.ai/dashboard/keys)."
        )
    elif code == 402:
        msg = (
            "402 Payment Required — out of fal.ai credits.\n"
            "  Add a payment method / top up at https://fal.ai/dashboard/billing."
        )
    elif code in (400, 422):
        msg = (
            f"{code} Bad Request — invalid params for this model "
            "(check prompt, duration, aspect_ratio, image_url/tail_image_url, model id).\n"
            f"  Some models reject a tail frame — retry with --no-end-image.\n"
            f"  API detail: {detail_short}"
        )
    elif code == 429:
        msg = "429 Too Many Requests — rate limited. Wait and retry."
    else:
        msg = f"HTTP {code} from fal.ai.\n  API detail: {detail_short}"
    print(f"ERROR: {msg}", file=sys.stderr)
    raise SystemExit(1)


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------
def list_presets(config: dict) -> None:
    meta = config.get("_meta", {})
    default_model = meta.get("default_model", DEFAULT_MODEL)
    print("Video clip presets (trailer/video_presets.json):")
    presets = config.get("presets", {})
    if not presets:
        print("  (none)")
        return
    width = max(len(n) for n in presets)
    for name in sorted(presets):
        resolved = resolve_preset(name, config)
        end = resolved["end_image"] or "(none)"
        print(f"  {name:<{width}}  -> {resolved['out']}")
        print(f"  {'':<{width}}     start: {resolved['start_image']}")
        print(f"  {'':<{width}}     end:   {end}")
    print(f"\nDefault model: {default_model}")
    print(f"Open alternative (single start frame): {ALT_MODEL}")


def print_dry_run(resolved: dict, body: dict) -> None:
    print("DRY RUN — no network call")
    print(f"  preset:   {resolved.get('name', '(inline)')}")
    print(f"  model:    {body['model']}")
    print(f"  out:      {resolved['out']}")
    print(f"  endpoint: POST {QUEUE_BASE}/{body['model']}")
    print("  request JSON:")
    print(json.dumps(body, indent=2, ensure_ascii=False))
    print(
        "\n  (At runtime, local --start-image/--end-image are uploaded to fal storage "
        "[POST " + STORAGE_UPLOAD_URL + "] or inlined as base64 data: URIs.)"
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate cel-trailer motion clips via the fal.ai image-to-video API."
    )
    parser.add_argument("--preset", help="Preset name from trailer/video_presets.json")
    parser.add_argument("--list-presets", action="store_true",
                        help="List presets and exit")
    parser.add_argument("--dry-run", action="store_true",
                        help="Print the request JSON; do not call the API")
    parser.add_argument("--prompt", help="Override / inline positive prompt")
    parser.add_argument("--negative", help="Override negative prompt")
    parser.add_argument("--start-image", dest="start_image",
                        help="Start frame (repo-relative path); overrides preset")
    parser.add_argument("--end-image", dest="end_image",
                        help="End / tail frame (repo-relative path); overrides preset")
    parser.add_argument("--no-end-image", action="store_true",
                        help="Ignore any end/tail frame (single start frame only)")
    parser.add_argument("--duration", type=int, default=None,
                        help=f"Clip duration in seconds (default {DEFAULT_DURATION})")
    parser.add_argument("--model", default=None,
                        help=f"Model id (default {DEFAULT_MODEL}; alt {ALT_MODEL})")
    parser.add_argument("--out", type=Path, default=None,
                        help="Output mp4 path (default trailer/clips/<preset>.mp4)")
    parser.add_argument("--prefer-data-uri", action="store_true",
                        help="Skip fal storage upload; always inline images as data URIs")
    parser.add_argument("--poll-interval", type=float, default=None,
                        help=f"Seconds between status polls (default {DEFAULT_POLL_INTERVAL})")
    parser.add_argument("--timeout", type=float, default=None,
                        help=f"Max seconds to wait for the clip (default {DEFAULT_TIMEOUT:.0f})")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    config = load_presets()
    meta = config.get("_meta", {})

    if args.list_presets:
        list_presets(config)
        return

    if args.preset:
        resolved = resolve_preset(args.preset, config)
    elif args.start_image and args.prompt and args.out:
        resolved = {
            "name": "(inline)",
            "model": DEFAULT_MODEL,
            "prompt": args.prompt,
            "negative_prompt": "",
            "duration": DEFAULT_DURATION,
            "aspect_ratio": meta.get("aspect_ratio", DEFAULT_ASPECT_RATIO),
            "start_image": args.start_image,
            "end_image": args.end_image,
            "out": str(args.out),
        }
    else:
        print(
            "ERROR: Provide --preset NAME, or all of --start-image, --prompt and --out.\n"
            "  Try: python scripts/generate_video_clip.py --list-presets",
            file=sys.stderr,
        )
        raise SystemExit(2)

    # CLI overrides.
    if args.prompt:
        resolved["prompt"] = args.prompt
    if args.negative is not None:
        resolved["negative_prompt"] = args.negative
    if args.start_image:
        resolved["start_image"] = args.start_image
    if args.end_image:
        resolved["end_image"] = args.end_image
    if args.no_end_image:
        resolved["end_image"] = None
    if args.duration is not None:
        resolved["duration"] = args.duration
    if args.model:
        resolved["model"] = args.model
    if args.out:
        resolved["out"] = str(args.out)

    if not resolved.get("start_image"):
        print("ERROR: No start image for this clip (set 'start_image' / --start-image).",
              file=sys.stderr)
        raise SystemExit(2)

    poll_interval = (
        args.poll_interval
        if args.poll_interval is not None
        else float(meta.get("poll_interval", DEFAULT_POLL_INTERVAL))
    )
    timeout = (
        args.timeout
        if args.timeout is not None
        else float(meta.get("timeout", DEFAULT_TIMEOUT))
    )

    api_key = "" if args.dry_run else get_api_key(required=True)

    start_url = resolve_image_ref(
        resolved["start_image"], api_key,
        dry_run=args.dry_run, prefer_data_uri=args.prefer_data_uri, label="start",
    )
    end_url: str | None = None
    if resolved.get("end_image"):
        end_url = resolve_image_ref(
            resolved["end_image"], api_key,
            dry_run=args.dry_run, prefer_data_uri=args.prefer_data_uri, label="end",
        )

    input_payload = build_input(resolved, config, start_url, end_url)
    body = {"model": resolved["model"], "input": input_payload}

    if args.dry_run:
        print_dry_run(resolved, body)
        return

    print(f"Submitting {resolved['name']} to {resolved['model']} ...")
    submit = submit_request(resolved["model"], input_payload, api_key)
    status_url = submit.get("status_url")
    response_url = submit.get("response_url")
    if not status_url or not response_url:
        print(
            "ERROR: fal submit response missing status_url/response_url.\n"
            f"  Got: {json.dumps(submit)[:400]}",
            file=sys.stderr,
        )
        raise SystemExit(1)
    print(f"  request_id: {submit.get('request_id', '?')}")

    poll_until_done(status_url, api_key, poll_interval=poll_interval, timeout=timeout)
    result = get_json(response_url, api_key)
    video_url = extract_video_url(result)
    download_video(video_url, ROOT / resolved["out"])


if __name__ == "__main__":
    main()
