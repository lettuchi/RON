# AU Modern — Municipal Arts & Licensing Practice Studio

**Scene:** `au_modern_case1_studio_session` (Case 1 compliance ballet beat)  
**Locked:** 2026-06-07 consistency pass  
**Style anchor CG:** `game/images/cg/cg-au-modern-case1-piano-sit.png`

## Room identity

Municipal Arts & Licensing **corner practice studio** — same room as Wrong Floor audition (`au_modern_studio_audition`), rented by the hour. Afternoon light (warm neutral, not night-only). Rain may streak **high clerestory/back windows** but the **left long wall is mirrors**, not a full glass harbor view.

## Layout (camera = audience POV, wide 3:2 landscape)

```
                    [ back wall — cream/neutral, high windows optional ]
    ┌──────────────────────────────────────────────────────────────────┐
    │                                                                  │
    │  LEFT LONG WALL          OPEN FLOOR           RIGHT WALL         │
    │  ═══════════════                              ┌─────────┐      │
    │  │ MIRROR WALL │  ← barre bolted here         │ BROWN   │      │
    │  │ (frames)    │                               │ UPRIGHT │      │
    │  │ reflects:   │         Toa works here        │ PIANO   │      │
    │  │ Toa, barre, │         (barre / centre)      │ (fixed) │      │
    │  │ Kaoru, piano│                               └─────────┘      │
    │  ═══════════════                              wooden bench     │
    │                                                                  │
    └──────────────────────────────────────────────────────────────────┘
                         dark polished wooden floor
```

| Element | Lock |
|---------|------|
| **Mirrors** | Full-height ballet mirrors on **left/long wall**; visible frames; reflections must show **actual scene** (Toa at barre, Kaoru at piano, barre, room — never blank gray) |
| **Barre** | Wooden barre **mounted on mirror wall** (not floating in front of back windows only) |
| **Piano** | **Brown wooden upright** (municipal, slightly worn). **Same model, wood tone, and position every shot** — **right wall**, below/right of mirror corner. **NOT** black grand, NOT digital keyboard |
| **Piano orientation** | Upright **back panel flush against RIGHT wall** (rain windows on right behind piano). **Keyboard faces LEFT** into open floor toward mirror wall. **Bench between keyboard and right windows** — Kaoru sits **facing the keys (body facing LEFT) with BACK toward RIGHT rain windows**, same seat as `piano-lookup` / `piano-sit`; he turns head left over shoulder to watch Toa at centre-left. **NOT** bench on centre-floor side only (pianist back to mirrors), NOT keyboard facing right wall, NOT piano backwards (keyboard against wall) |
| **Floor** | Dark polished wood |
| **Walls** | Neutral/cream where visible; back may have **small high windows** with rain — do not replace entire left wall with harbor glass |
| **Light** | Afternoon studio light (fluorescent + warm window spill); readable, not night-only |

## Characters (this scene)

| Who | Lock |
|-----|------|
| **Toa** | **Ballet class bun** (white/silver hair, neat, tight — NOT loose, NOT ponytail) for every ballet-practice shot. Black/gold crane-logo tracksuit over leotard; white ballet slippers/pointe as beat requires |
| **Kaoru** | Tan skin, brown hair slicked back short ponytail, grey eyes. **Charcoal deputy-director suit**; **sleeves rolled to forearm** when at piano; jacket may be folded on barre in some beats |

## CG tags (Case 1 studio pass)

| File | Tag | Beat |
|------|-----|------|
| `cg-au-modern-case1-studio-piano.png` | `au_modern_case1_studio_piano` | Establishing — upright on right, Toa at barre, Kaoru entering |
| `cg-au-modern-case1-barre-twoshot.png` | `au_modern_case1_barre_twoshot` | Barre work — Kaoru witnesses; **brown upright visible on right** |
| `cg-au-modern-case1-piano-sit.png` | `au_modern_case1_piano_sit` | Kaoru sits at piano, rolled sleeves — **style anchor** |
| `cg-au-modern-case1-piano-lookup.png` | `au_modern_case1_piano_lookup` | Hinge — Kaoru looks up from keys at dancing Toa |
| `cg-au-modern-case1-reverence.png` | `au_modern_case1_reverence` | Toa curtsies to accompanist at piano |

## Legacy CGs (Wrong Floor audition — separate label)

`au_modern_studio_audition` / `toa_ballet_practice_room` are wired in `au_modern_wrong_floor.rpy`, **not** `au_modern_case1_studio_session`. Regen separately if audition room must match this bible.

## Prompt anchors (every studio regen)

```
municipal ballet practice studio, afternoon light, cream neutral walls, dark wooden floor,
full-wall ballet mirrors on LEFT with visible frames and accurate reflections of dancers and piano,
wooden barre mounted on mirror wall,
brown wooden upright piano on RIGHT wall back panel against right wall keyboard faces LEFT into room municipal brown wood NOT black grand,
piano bench between keyboard and right rain windows accompanist seated facing keyboard body facing LEFT back toward right wall and window glass NOT bench centre-floor side only,
rain streaks on high back windows only
```

**Toa:** `white silver hair neat ballet bun, black tracksuit gold crane logo, gold stripes, ballet slippers`

**Kaoru at piano:** `charcoal suit vest white shirt rolled sleeves, tan skin brown hair`

**Hands (mandatory):** `anatomically correct hands, five fingers per hand, two hands per person` + negative `extra hands, extra limbs, duplicated hands, three hands, floating hands`

**Refs:** AU outfit refs + `cg-au-modern-case1-piano-sit.png` + `style-painterly-reference.png`

## Registry

No tag/filename changes. Images live in `game/images/cgs-au-modern-case1.rpy`.
