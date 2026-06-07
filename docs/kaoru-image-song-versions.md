# Kaoru image song — 「権利の帳」 version files

Primary playback uses `game/audio/bgm/kaoru_image_song_kenri.mp3` (`audio.bgm_kaoru_kenri` in `game/audio/music.rpy`). Named copies keep older generations for comparison and gallery experiments.

| File | Role |
|------|------|
| `kaoru_image_song_kenri.mp3` | **Primary** — latest Hakuoki-style v3 (~222 s, song-id `QsHtwIZzkfw1YpMIEFmt`; overwrite target for regen) |
| `kaoru_image_song_kenri_v1_original.mp3` | First generation (~226 s, pre–high-energy tweak), if recovered from git |
| `kaoru_image_song_kenri_v2_energetic.mp3` | High-energy / raspy regen (~216 s, song-id `zpSs4reVzkQJabic1xoQ`) |
| `kaoru_image_song_kenri_v3_hakuoki.mp3` | Hakuoki-style polished regen (~222 s, song-id `QsHtwIZzkfw1YpMIEFmt`; duplicate of primary) |
| `versions/kaoru_image_song_kenri_backup_*.mp3` | Automatic timestamped backups before each regen |

## Regenerate (with backup)

From project root:

```powershell
python scripts/generate_kaoru_image_song.py --regen --model v2
```

- Default: copies existing primary into `game/audio/bgm/versions/` before writing.
- Skip backup: `--no-backup`
- `music_v2` is tried first; script falls back to `music_v1` if v2 is unavailable.

After a Hakuoki-style pass, also keep an explicit named copy:

```powershell
Copy-Item game\audio\bgm\kaoru_image_song_kenri.mp3 game\audio\bgm\kaoru_image_song_kenri_v3_hakuoki.mp3
```

## Style reference (v3+)

Target: **Hakuoki**-style otome character image songs — smooth baritone, dramatic but not raspy, 128–132 BPM, strings + restrained drums, pop-rock/orchestral polish. Avoid metal screaming, gravel vocals, or 140 BPM metal rush.

Composition hints live in `scripts/generate_kaoru_image_song.py` (`_GLOBAL_POSITIVE` / section plans). Lyrics stay locked in `docs/kaoru-image-song-kenri-lyrics.md`.

## v1 recovery note

If `kaoru_image_song_kenri_v1_original.mp3` is missing, the first Eleven generation was likely overwritten in place before versioned filenames were adopted. Try `git log -- game/audio/bgm/kaoru_image_song_kenri.mp3` and `git show <commit>:game/audio/bgm/kaoru_image_song_kenri.mp3` on a machine with git and a tracked copy of this asset. This workspace has no `.git` directory and git was not on PATH during the v3 pass — v1 was **not** recovered; use `v2_energetic` or `versions/kaoru_image_song_kenri_backup_20260602_163753.mp3` for the pre–Hakuoki regen.

## Subtitles

Montage timing in `game/kaoru_image_song.rpy` is approximate. Re-sync with faster-whisper only when asked; update the header comment if duration shifts by more than ~10 s.
