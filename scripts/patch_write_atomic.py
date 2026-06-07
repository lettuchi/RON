from pathlib import Path
import re
p = Path(r"C:\Users\Amanda\Developer\ryoko-owari\scripts\generate_music.py")
t = p.read_text(encoding="utf-8")
old = """def write_atomic(path: Path, data: bytes) -> None:
    tmp = path.with_suffix(path.suffix + ".part")
    tmp.write_bytes(data)
    tmp.replace(path)"""
new = """def write_atomic(path: Path, data: bytes) -> Path:
    tmp = path.with_suffix(path.suffix + ".part")
    tmp.write_bytes(data)
    try:
        tmp.replace(path)
        return path
    except PermissionError:
        alt = path.with_name(path.stem + "_regen" + path.suffix)
        if alt.exists():
            alt.unlink()
        tmp.replace(alt)
        print(f"  WARN: {path.name} locked; wrote {alt.name} instead", file=sys.stderr)
        return alt"""
if old not in t:
    raise SystemExit("write_atomic not found")
t = t.replace(old, new, 1)
t = t.replace(
    '        write_atomic(out, audio)\n        print(f"[{tid}] OK: {len(audio)} bytes -> {out}")',
    '        out_written = write_atomic(out, audio)\n        print(f"[{tid}] OK: {len(audio)} bytes -> {out_written}")',
    1,
)
p.write_text(t, encoding="utf-8")
print("ok")
