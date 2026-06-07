# Toa image song — 「赤い糸の灯」 version files



Primary playback uses `game/audio/bgm/toa_image_song.mp3` (`audio.bgm_toa_image` in `game/audio/music.rpy`). Used by `game/toa_image_song.rpy` → label `toa_image_song_sequence`.



| File | Role |

|------|------|

| `toa_image_song.mp3` | **Primary** — latest generation (overwrite target for regen) |

| `versions/toa_image_song_backup_*.mp3` | Automatic timestamped backups before each regen |



## Regenerate (with backup)



From project root:



```powershell

python scripts/generate_toa_image_song.py --regen --model v2

```



- Default: copies existing primary into `game/audio/bgm/versions/` before writing.

- Skip backup: `--no-backup`

- `music_v2` is tried first; script falls back to `music_v1` if v2 is unavailable.



Dry-run (plan only, no API):



```powershell

python scripts/generate_toa_image_song.py --dry-run

```



## Style reference



Target: **Hakuoki**-style otome **heroine** image songs — sweet clear female vocal, hopeful stubborn warmth, ~118–126 BPM, piano/strings + gentle drums. Contrast with Kaoru「権利の帳」 (male baritone, predatory pop-rock).



Composition hints live in `scripts/generate_toa_image_song.py`. Lyrics stay locked in `docs/toa-image-song-lyrics.md` and `docs/toa-image-song-trilingual.md`.



## Montage art



Stills: `game/images/ts/ts-*.png` (nine montage beats + gallery thumbnail). Regenerate via GenerateImage with reference `game/images/sprites/toa/toa-neutral.png` per `.cursor/skills/vn-art-pipeline/SKILL.md`.



## Subtitles



Montage timing in `game/toa_image_song.rpy` is approximate (~20 s beats). Re-sync with faster-whisper only when asked; update the header comment if duration shifts by more than ~10 s.

