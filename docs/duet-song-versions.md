# Duet — 「嘘の夜を走れ」 version files



Primary: `game/audio/bgm/duet_song.mp3` (`audio.bgm_duet`). High-energy anime duet, all sung, no spoken word.



| File | Role |

|------|------|

| `duet_song.mp3` | **Primary** — ~215 s, song-id `A1fVC7lXmfeELrrcHi4K` (music_v1) |

| `versions/duet_song_backup_*.mp3` | Timestamped backups before regen |



## Regenerate



```powershell

python scripts/generate_duet_song.py --regen --model v2

```



- `music_v2` falls back to `music_v1` on plan blocks.

- Skip backup: `--no-backup`



Lyrics: `docs/duet-song-lyrics.md`. Montage: `game/duet_song.rpy`, stills `game/images/ds/ds-*.png`.

