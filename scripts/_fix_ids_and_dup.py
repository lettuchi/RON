from pathlib import Path
ROOT = Path(r"C:/Users/Amanda/Developer/ryoko-owari")
ids = """kaoru_426
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
(ROOT / "scripts/case1_unwired_voice_ids.txt").write_text("\n".join(ids) + "\n", encoding="utf-8")
# remove duplicate voice line in companion
p = ROOT / "game/case1_companion.rpy"
lines = p.read_text(encoding="utf-8").splitlines()
out = []
for line in lines:
    if line.strip() == 'voice "audio/voice/kaoru_426.mp3"' and out and out[-1].strip() == 'voice "audio/voice/kaoru_430.mp3"':
        continue
    out.append(line)
p.write_text("\n".join(out) + "\n", encoding="utf-8")
print("ids", len(ids), "removed dup", len(lines)-len(out))
