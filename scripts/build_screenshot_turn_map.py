#!/usr/bin/env python3
"""Build docs/screenshot-turn-map.json and docs/screenshot-turn-map.md.

Scans the four canon-screenshot source .rpy files for every player-visible
say line (centered, character, narrator, named speaker). Menu choice captions
are excluded; dialogue inside choice branches is included (all branches).

Canon screenshot branch metadata matches test_all_turns.rpy policy:
first menu option except prologue_unless_menu → index 1.

Run from repo root:  python scripts/build_screenshot_turn_map.py
"""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GAME = ROOT / "game"
DOCS = ROOT / "docs"
JSON_OUT = DOCS / "screenshot-turn-map.json"
MD_OUT = DOCS / "screenshot-turn-map.md"

SOURCE_FILES = [
    GAME / "script.rpy",
    GAME / "prologue.rpy",
    GAME / "case1_companion.rpy",
    GAME / "case1_investigation.rpy",
]

SNIPPET_LEN = 72

CENTERED_RE = re.compile(
    r'^\s*centered\s+"((?:\\.|[^"\\])*)".*$', re.IGNORECASE
)
CHAR_RE = re.compile(
    r'^\s*(?P<tag>toa|kaoru)\s+"(?P<text>(?:\\.|[^"\\])*)"'
)
NAMED_RE = re.compile(
    r'^\s*"(?P<name>[^"]+)"\s+"(?P<text>(?:\\.|[^"\\])*)"'
)
NARRATOR_RE = re.compile(r'^\s*"(?P<text>(?:\\.|[^"\\])*)"\s*$')
MENU_START_RE = re.compile(r"^\s*menu(?:\s+(?P<name>\w+))?:\s*$")
CHOICE_RE = re.compile(r'^\s+"((?:\\.|[^"\\])*)":\s*$')

# Canon screenshot run (test_all_turns.rpy). display = table label when menu has no name.
CANON_MENU_SPECS: list[dict] = [
    {"menu": "prologue_door_choices", "choice": 0},
    {"menu": "__anonymous__", "at_label": "prologue_door_second_chance", "choice": 0,
     "display": "(second chance)"},
    {"menu": "prologue_formality_menu", "choice": 0},
    {"menu": "prologue_enter_office_menu", "choice": 0},
    {"menu": "prologue_expired_menu", "choice": 0},
    {"menu": "prologue_before_dance_menu", "choice": 0},
    {"menu": "prologue_performance_menu", "choice": 0},
    {"menu": "prologue_grab_menu", "choice": 0},
    {"menu": "prologue_unless_menu", "choice": 1},
    {"menu": "case1_sponsorship_prelude_menu", "choice": 0},
    {"menu": "case1_companion_accept_menu", "choice": 0},
    {"menu": "case1_first_duty_menu", "choice": 0},
    {"menu": "case1_briefing_menu", "choice": 0},
    {"menu": "case1_canal_menu", "choice": 0},
    {"menu": "case1_kaoru_probe_menu", "choice": 0},
]


def unescape_renpy(s: str) -> str:
    s = s.replace('\\"', '"').replace("\\'", "'")
    s = s.replace("\\n", "\n").replace("\\\\", "\\")
    return s


def snippet(text: str) -> str:
    flat = text.replace("\n", " ")
    if len(flat) <= SNIPPET_LEN:
        return flat
    return flat[: SNIPPET_LEN - 1] + "…"


def parse_turn(line: str) -> tuple[str, str] | None:
    m = CENTERED_RE.match(line)
    if m:
        return "centered", unescape_renpy(m.group(1))
    m = CHAR_RE.match(line)
    if m:
        return m.group("tag"), unescape_renpy(m.group("text"))
    m = NAMED_RE.match(line)
    if m:
        return m.group("name"), unescape_renpy(m.group("text"))
    m = NARRATOR_RE.match(line)
    if m:
        return "narrator", unescape_renpy(m.group(1))
    return None


def collect_turns(path: Path) -> list[dict]:
    turns: list[dict] = []
    src = path.read_text(encoding="utf-8").splitlines()
    rel = f"game/{path.name}"
    for i, line in enumerate(src, start=1):
        if CHOICE_RE.match(line):
            continue
        parsed = parse_turn(line)
        if not parsed:
            continue
        speaker, text = parsed
        if not text.strip():
            continue
        turns.append({
            "speaker": speaker,
            "text": text,
            "snippet": snippet(text),
            "source_file": rel,
            "source_line": i,
        })
    return turns


def collect_menus(path: Path) -> tuple[dict[str, list[str]], dict[str, list[str]]]:
    """Return (menus by name, anonymous menus keyed by label above menu block)."""
    by_name: dict[str, list[str]] = {}
    anon_at_label: dict[str, list[str]] = {}
    src = path.read_text(encoding="utf-8").splitlines()
    current_label = ""
    pending_anon_label = ""
    i = 0
    while i < len(src):
        line = src[i]
        lm = re.match(r"^label\s+(\w+):", line)
        if lm:
            current_label = lm.group(1)
        mm = MENU_START_RE.match(line)
        if mm:
            name = mm.group("name")
            choices: list[str] = []
            j = i + 1
            while j < len(src):
                cm = CHOICE_RE.match(src[j])
                if not cm:
                    if src[j].strip() and not src[j].startswith(" "):
                        break
                    if src[j].strip().startswith("menu "):
                        break
                    j += 1
                    continue
                choices.append(unescape_renpy(cm.group(1)))
                j += 1
            if name:
                by_name[name] = choices
            else:
                anon_at_label[pending_anon_label or current_label] = choices
            i = j
            continue
        if line.strip() and not line.strip().startswith("#"):
            pending_anon_label = current_label
        i += 1
    return by_name, anon_at_label


def build_canon_menus() -> list[dict]:
    by_name: dict[str, list[str]] = {}
    anon: dict[str, list[str]] = {}
    for path in SOURCE_FILES:
        n, a = collect_menus(path)
        by_name.update(n)
        anon.update(a)

    out: list[dict] = []
    for spec in CANON_MENU_SPECS:
        menu = spec["menu"]
        choice = spec["choice"]
        labels: list[str] = []
        if menu == "__anonymous__":
            labels = anon.get(spec["at_label"], [])
        else:
            labels = by_name.get(menu, [])
        label = labels[choice] if choice < len(labels) else ""
        entry: dict = {
            "menu": spec.get("display") or menu,
            "choice": choice,
        }
        if label:
            entry["label"] = label
        out.append(entry)
    return out


def write_markdown(data: dict) -> None:
    lines = [
        "# Screenshot turn map",
        "",
        f"Total dialogue/narration turns in scanned sources: **{data['turn_count']}**.",
        "",
        "## Canon screenshot run",
        "",
        f"- **Policy:** {data['canon_screenshot_branch']['menu_policy']}",
        f"- **Entry:** `{data['canon_screenshot_branch']['entry']}`",
        "",
        "### Menu branch choices",
        "",
        "| Menu | Index | Label |",
        "|------|-------|-------|",
    ]
    for m in data["canon_screenshot_branch"]["menus"]:
        label = m.get("label", "(first option)")
        lines.append(f"| {m['menu']} | {m['choice']} | {label} |")
    lines.extend([
        "",
        "## Turn index",
        "",
        "| ID | Speaker | Snippet | Source |",
        "|----|---------|---------|--------|",
    ])
    for t in data["turns"]:
        snip = t["snippet"].replace("|", "\\|")
        lines.append(
            f"| {t['id']} | {t['speaker']} | {snip} | "
            f"`{t['source_file']}:{t['source_line']}` |"
        )
    lines.append("")
    MD_OUT.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    all_turns: list[dict] = []
    for path in SOURCE_FILES:
        if not path.is_file():
            print(f"ERROR: missing {path}", file=__import__("sys").stderr)
            return 1
        all_turns.extend(collect_turns(path))

    for n, t in enumerate(all_turns, start=1):
        t["id"] = f"turn_{n:03d}"
        t["index"] = n

    data = {
        "generated_by": "scripts/build_screenshot_turn_map.py",
        "sources": [f"game/{p.name}" for p in SOURCE_FILES],
        "turn_count": len(all_turns),
        "canon_screenshot_branch": {
            "name": "canon_first_choice_physical_unless",
            "entry": "start → prologue_start → … → case1_investigation_milestone_end",
            "menu_policy": (
                "First menu option at each prompt, except prologue_unless_menu "
                "→ physical (index 1)."
            ),
            "menus": build_canon_menus(),
            "notes": [
                "Static turn map includes all branches in source; runtime screenshots "
                "follow this path only.",
                "Menu prompts may get an extra *_menu.png screenshot before the "
                "choice is clicked.",
            ],
        },
        "turns": all_turns,
    }

    JSON_OUT.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    write_markdown(data)
    print(f"wrote {JSON_OUT} ({data['turn_count']} turns)")
    print(f"wrote {MD_OUT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
