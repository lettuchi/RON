#!/usr/bin/env python3
"""Apply case1-updates.json game_text to case1 .rpy voice lines."""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SIDECAR = ROOT / "docs" / "script-rewrite-2026-06-04" / "case1-updates.json"
FILES = [
    ROOT / "game" / "case1_investigation.rpy",
    ROOT / "game" / "case1_companion.rpy",
]
VOICE_RE = re.compile(r'voice "audio/voice/(\w+)\.mp3"')


def patch_file(path: Path, by_id: dict[str, str]) -> tuple[int, list[str]]:
    lines = path.read_text(encoding="utf-8").splitlines()
    changed = 0
    missing: list[str] = []
    pending: str | None = None
    for i, line in enumerate(lines):
        vm = VOICE_RE.search(line)
        if vm:
            pending = vm.group(1)
            continue
        if not pending:
            continue
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        if stripped.startswith(
            ("show ", "play ", "$", "if ", "elif ", "else:", "jump ", "menu ", "pause", "scene ", "with ")
        ):
            continue
        new = by_id.get(pending)
        if new is None:
            missing.append(pending)
            pending = None
            continue
        m = re.match(r"^(toa|kaoru)\s+\".+\"$", stripped)
        if m:
            indent = line[: len(line) - len(line.lstrip())]
            lines[i] = f'{indent}{m.group(1)} "{new}"'
            changed += 1
            pending = None
            continue
        m = re.match(r'^"(.+)"$', stripped)
        if m:
            indent = line[: len(line) - len(line.lstrip())]
            lines[i] = f'{indent}"{new}"'
            changed += 1
            pending = None
            continue
        m = re.match(r'^"([^"]+)"\s+"(.+)"$', stripped)
        if m:
            indent = line[: len(line) - len(line.lstrip())]
            lines[i] = f'{indent}"{m.group(1)}" "{new}"'
            changed += 1
            pending = None
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return changed, missing


def main() -> int:
    rows = json.loads(SIDECAR.read_text(encoding="utf-8"))
    by_id = {r["id"]: r["game_text"] for r in rows}
    total = 0
    for path in FILES:
        n, miss = patch_file(path, by_id)
        print(f"{path.name}: {n} lines patched, {len(miss)} unmatched voice ids")
        total += n
    print(f"total patched: {total} (sidecar rows: {len(rows)})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
