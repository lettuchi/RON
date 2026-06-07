#!/usr/bin/env python3
"""Emit markdown hand-audit rows for wired canon CGs."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
inv = (ROOT / "docs" / "_canon_cg_inventory.txt").read_text(encoding="utf-8")
audit = json.loads((ROOT / "docs" / "_canon_hand_audit.json").read_text(encoding="utf-8"))
audit_by_png = {r["png"]: r for r in audit}

# Visual ground truth from QA pass (2026-06-07)
VISUAL = {
    "cg-first-scene-office-dance.png": ("PASS (regen v2)", "Toa 2×5 fan grip; Kaoru 1 visible"),
    "cg-case2-festival-kiss.png": ("PASS (regen v3)", "1 visible hand, 5 fingers"),
    "cg-case3_5-date-almost-hands.png": ("PASS (regen)", "2 hands, 5 fingers each"),
    "cg-case4_5-boat-hands-gunwale-closeup.png": ("PASS (regen v2)", "2 hands, 5 fingers each"),
    "cg-epilogue-romance-kotatsu-intimate.png": ("PASS (regen)", "3 visible, 5 fingers each"),
    "cg-case1_5-shoji-wrist-closeup.png": ("PASS (regen)", "2 hands, 5 fingers each"),
    "cg-canon-embrace.png": ("BORDERLINE", "Kaoru shoulder hand knuckles messy"),
    "cg-canon-pull-close.png": ("PASS", "3 visible, correct"),
    "cg-canon-undress-toa.png": ("PASS", "Toa 2 visible"),
    "cg-canon-proposition.png": ("PASS", "3 visible"),
    "cg-canon-signing.png": ("PASS", "4 visible, correct"),
    "cg-canon-afterglow.png": ("PASS (spot)", "low visibility"),
    "cg-case1-romance-office-touch.png": ("PASS", "1 visible"),
    "cg-case1-romance-sponsorship.png": ("PASS", "4 visible"),
    "cg-case2-festival-intimate.png": ("PASS", "2 visible"),
    "cg-case4-romance-defend.png": ("PASS", "4 visible"),
    "cg-case1-bad-punishment-hands.png": ("PASS", "1 visible grip"),
    "cg-badend-brothel-grasp.png": ("BORDERLINE", "ronin fingers stylized long"),
    "cg-case5-oath-seal-hand-closeup.png": ("PASS", "2 hands macro"),
    "cg-choice-grab-rebuke.png": ("PASS", "3 visible"),
    "cg-case3_5-date-inn-collar-hands.png": ("PASS", "2 visible"),
    "cg-case3_5-date-lesson.png": ("BORDERLINE", "pointing arm slightly long"),
    "cg-first-scene-chair-tension.png": ("PASS", "3 visible"),
    "cg-first-scene-permit-desk.png": ("N/A", "no hands visible"),
    "cg-case5-false-exit-office.png": ("PASS", "2 visible on letter"),
}

NO_HUMAN = {
    "cg-case4-gritty-establishing.png", "cg-case4-fight-wide.png", "cg-case2-festival-fireworks.png",
    "cg-case2-festival-hill.png", "cg-case3-fabric-shop.png", "cg-case1-canal-body.png",
    "cg-case-zero-redacted-docket.png", "cg-case-zero-rain-alley-door.png",
    "cg-gameover-rain-run.png", "cg-gameover-rain-alone.png", "cg-case5-hearing-hall.png",
    "cg-case3_5-date-silk-fabric.png", "cg-case3_5-date-inn-exterior.png",
    "cg-case3_5-date-arrival.png", "cg-case3_5-date-tatami-lanterns.png",
    "cg-case4_5-boat-canal-night.png", "cg-case4_5-boat-throw-splash.png",
    "cg-case4_5-boat-lash-rain-closeup.png", "cg-case4_5-boat-lantern-implied.png",
    "cg-case1_5-hanko-pot.png", "cg-case5-false-exit-office.png",  # has humans - remove
}
NO_HUMAN.discard("cg-case5-false-exit-office.png")

rows = []
in_wired = False
seen = set()
for line in inv.splitlines():
    if line == "=== WIRED ===":
        in_wired = True
        continue
    if line.startswith("=== ") and in_wired:
        break
    if not in_wired or "\t" not in line:
        continue
    tag, png = line.split("\t", 1)
    if png == "MISSING" or png in seen:
        continue
    seen.add(png)

    if png in VISUAL:
        status, note = VISUAL[png]
    elif png in NO_HUMAN or any(
        k in png for k in ("establishing", "fireworks", "hill", "docket", "canal-night", "throw-splash", "lash-rain", "lantern-implied", "hearing-hall", "rain-run", "rain-alone", "fabric-shop", "silk-fabric", "inn-exterior", "arrival", "tatami-lanterns", "hanko-pot", "quarter-cage", "chained", "epilogue-week")
    ):
        status, note = "N/A", "no/minimal human hands"
    else:
        ar = audit_by_png.get(png, {})
        hr = ar.get("high_risk", False)
        status = "PASS (advisory)" if not hr else "NOT VISUALLY AUDITED"
        note = "MediaPipe only; high-risk needs second-pass visual" if hr else "MediaPipe advisory; spot-check recommended"

    rows.append((tag, png, status, note))

for tag, png, status, note in rows:
    print(f"| `{png}` | `{tag}` | {status} | {note} |")

print(f"\nTOTAL_ROWS={len(rows)}")
