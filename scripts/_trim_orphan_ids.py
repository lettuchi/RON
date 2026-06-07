import json
from pathlib import Path
ROOT = Path(r"C:/Users/Amanda/Developer/ryoko-owari")
VALID = """kaoru_426
toa_319
kaoru_427
toa_320
kaoru_428
toa_321
kaoru_429
toa_322
kaoru_430
kaoru_431
toa_323
kaoru_432
toa_324
kaoru_433
toa_325
kaoru_434
toa_326
kaoru_435
kaoru_436
toa_327
kaoru_437
toa_328
toa_329
kaoru_438
toa_330
kaoru_439
toa_331
kaoru_440
kaoru_441
toa_332
kaoru_442
toa_333
kaoru_443
kaoru_444
toa_334
kaoru_445
toa_335
kaoru_446
toa_336
kaoru_447
toa_337
kaoru_448""".strip().split()
(ROOT / "scripts/case1_unwired_voice_ids.txt").write_text("\n".join(VALID) + "\n", encoding="utf-8")
ORPHAN = {"toa_338", "kaoru_449"}
for fname in ["voice_manifest.json", "narrator_manifest.json"]:
    p = ROOT / "scripts" / fname
    d = json.loads(p.read_text(encoding="utf-8"))
    d["lines"] = [r for r in d["lines"] if r["id"] not in ORPHAN]
    p.write_text(json.dumps(d, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
pm = json.loads((ROOT / "scripts/voice_performance_manifest.json").read_text(encoding="utf-8"))
pm["entries"] = [e for e in pm["entries"] if e["id"] not in ORPHAN]
(ROOT / "scripts/voice_performance_manifest.json").write_text(json.dumps(pm, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
for vid in ORPHAN:
    for folder in [ROOT / "game/audio/voice", ROOT / "game/audio/voice/v2/eve-donovan-2026-06-04"]:
        f = folder / f"{vid}.mp3"
        if f.is_file():
            f.unlink()
            print("removed", f)
print("trimmed ids to", len(VALID))
