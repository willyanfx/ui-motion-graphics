# Sound for UI films

Sound makes cause and effect felt: the press lands, the panel arrives, the number settles. It reinforces the picture and never replaces it. Many placements autoplay muted (Reels, TikTok, web heroes), so the film must read with the sound off; captions carry any spoken meaning.

## Choose a sound mode

Decide in discovery and record it in the brief. Each mode changes how the timeline is built.

| Mode | What leads | Build consequence | Fits |
|---|---|---|---|
| Music-led | A track sets tempo; key actions and scene boundaries land on beats | Choose BPM before timing scenes; boundaries snap to the beat grid | Launch reels, social, energetic tours |
| Sound-design-led | UI sounds form the rhythm; little or no music | Every cue is authored; silence is part of the score | Craft showcases, portfolio pieces, calm product films |
| Hybrid (default) | A quiet bed for continuity, sparse UI accents on key moments | Bed is loose; only primary actions get sync points | Most product demos and walkthroughs |
| Voice-led | Narration explains; music ducks; few sound effects | Write VO after the action path, then fit holds to it | Explainers, onboarding, feature walkthroughs |
| Silent-first | Picture and captions carry everything; sound is optional | Plan as if muted; add sound as a bonus layer | Web background loops, autoplay feeds |

## UI sound palette

Starting properties (prop); pick from licensed libraries or generate. The sync point is the frame the sound's attack lands on.

| Sound | Attach to | Character | Sync point |
|---|---|---|---|
| Click / tick | Pointer press, toggle, checkbox, key | < 100 ms, mid-high, dry | Press frame (not release) |
| Tap / pop | Touch press, badge or dot appearing | Soft, short, slightly pitched | Press or appear frame |
| Swipe / whoosh | Camera move, panel slide, wipe transition | Length matches the move | Peak at the fastest point of the move |
| Riser | Build into a reveal or end card | 0.5–2 s, rising pitch or noise | Peak on the reveal frame, then cut dead |
| Impact / thump | Logo landing, chapter cut, big reveal | Low, with a short tail | Landing frame |
| Typing | Text entering a field | Per keystroke up to ~10 characters/s, a textured loop above that (on-camera typing at 2 f per character is 15/s — use the loop) | First and last character |
| Confirm / success | Result state, completed action | Short, resolved, pleasant | The action's `completeAt` frame |
| Data ticks | Counters, chart morphs, progress | Tick per step or a granular loop | Stops exactly when the number stops |
| Bed / room tone | Under everything | Low, steady | Loose; avoids dead air between hits |
| Silence | Right before the key moment | A 200–400 ms dropout | Ends on the hit, so it lands harder |

## Sync rules

- **Sound follows cause.** Put the hit on the frame the visible change starts — the press, the arrival, the state change — not where a keyframe begins traveling.
- **On the frame or slightly after, never early.** People notice sound that arrives before its picture sooner than sound that arrives late. ITU-R BT.1359 puts detectability at about 45 ms early versus 125 ms late, so place hits on the frame or up to one frame after, never more than a frame before.
- **One sound per cause.** Sonify the primary action; keep secondary motion quieter; leave ambient drift silent. Sound hierarchy mirrors visual hierarchy.
- **Leave gaps.** A walkthrough needs one sound per action, not per animation; dense montage tops out around 3–4 cues per second before it turns to noise.
- **Sync deliberately, not everywhere.** In the reference library, music mostly sets the pace; tight hits are saved for moments that matter (see [evidence](#library-evidence)). Pick the three to five frames where a hit proves causality and sync those precisely.

## Music and the beat grid

For music-led films, choose the tempo first, then time scenes on its grid.

- Frames per beat = `fps × 60 / BPM`: 120 BPM at 30 fps is 15 frames; 105 BPM is 17.14. Compute beat *n* as `round(offset + n × fps × 60 / BPM)` instead of adding a rounded beat repeatedly, so drift doesn't build up.
- Size scenes in bars (4 beats in 4/4). At 120 BPM, 30 fps, one bar is 60 frames = 2 s; an 8-bar film is 480 frames = 16 s.
- Snap scene boundaries and primary actions to beats (±1 frame); let connective motion run free between them.
- Tempo sets feel: roughly 60–90 BPM calm and precise, 100–125 default product energy, 130–160 fast social. The library's confident candidates span 60–158 BPM.
- **Loops:** the music loop must equal the film loop — `bars × beats per bar × frames per beat = durationInFrames`. Put a 5–10 ms crossfade at the wrap so the seam doesn't click.
- **VO over music:** duck music about 8–12 dB under speech. At ~150 words per minute, 15 s holds about 35 words.

## Mix and delivery (prop)

- **Loudness:** master social and web films to about −14 LUFS integrated with true peak at or below −1 dBTP. Platforms normalize, so louder doesn't win; hot masters clip after transcoding. Check the export: `ffmpeg -i film.mp4 -af ebur128=peak=true -f null -`.
- **Balance:** a sound effect sits about 3–6 dB above the bed at its moment; VO is the loudest element whenever it speaks.
- **Space:** optional subtle panning that follows screen position (a panel sliding right pans right). Keep low end and VO centered.
- **Stems:** export music, sound effects, and VO separately so a revision doesn't mean a full remix.
- **Rights:** record every sound's source and license in the asset map. Reference audio is analyzed for timing only — never lifted.

## Timeline fields

Extend the `audio` array in [`timeline.json`](../assets/timeline.example.json) and add a `sound` block; keep existing field names.

```json
{
  "sound": { "mode": "music-led", "beatGrid": { "bpm": 120, "offsetFrames": 0, "status": "decided" }, "loudnessTarget": { "lufs": -14, "truePeakDb": -1 } },
  "audio": [
    { "frame": 130, "cue": "tap", "role": "sfx", "sync": "press", "target": "[data-motion-id='filter-new']", "gainDb": -6, "file": null, "status": "open" },
    { "frame": 151, "cue": "confirm", "role": "sfx", "sync": "completeAt", "gainDb": -9, "file": null, "status": "open" },
    { "frame": 0, "until": 450, "cue": "bed", "role": "music", "duck": [{ "from": 90, "until": 180, "gainDb": -10, "reason": "vo" }], "file": "audio/track.wav", "status": "decided" }
  ]
}
```

`sound.beatGrid` defines the tempo that scene boundaries snap to; the music file itself is placed by its cue in `audio`. `role` is `sfx | music | vo | bed`; `sync` names what the frame is locked to (`press | arrival | peak | completeAt | beat | loose`).

## Analyze reference sound

[`audio_events.py`](../scripts/audio_events.py) reads a clip's audio and pairs it with the picture (needs Python 3, Pillow, FFmpeg; writes to a new or empty folder):

```sh
python3 /path/to/ui-showcase-motion/scripts/audio_events.py /path/to/clip-or-folder /path/to/analysis/audio \
  --ids /path/to/analysis/contact-sheets/manifest.json
```

Per clip it reports: hit candidates (time, band, rise, tail, a hint such as tick or thump), swells (whoosh or riser candidates), low/mid/high band energy, silences, loudness (LUFS, true peak), a tempo candidate, and picture changes paired with the nearest hit. The sheet shows the frame at each of the strongest hits above a band-energy timeline, with picture changes marked.

Reading it:

- Everything is a **candidate**. The tool can't separate music from sound effects or say what made a sound; name sources only after listening.
- **Sync is evidence only when `p_by_chance` is small (≤ 0.05).** With dense music a random moment is often near a hit, so 5 of 5 changes "on a hit" can still be chance. Few picture changes can't prove much either way.
- Tempo candidates can be half or double the felt tempo; values near 60 BPM often mean 120.
- Timing precision is about one 30 fps frame. For a close sync study, check the paired frames at full resolution and listen to the passage.

## Library evidence

Audio pass over the seed library, 2026-09-27 (`analysis/audio/`). **obs, candidates, not auditioned.**

- 33 unique clips have audio streams; three are silent tracks (R12, R24, R29). 30 were analyzed.
- Loudness: median −14.9 LUFS; 20 of 30 sit between −16 and −13. Nineteen have true peaks above −1 dBFS and nine above 0 dBFS — likely clipping after platform transcoding.
- Tempo: 28 clips give confident candidates between 60 and 158 BPM (the ~60 values may be half-time).
- Sync: of 23 clips with at least four picture changes, only R15 shows picture changes landing on hits beyond chance (4 of 4 within two frames, chance 0.36, p = 0.016), each hit landing on or about one frame after its cut (median +17 ms) — the placement the sync rule recommends. R30 looks perfect (5 of 5) but its dense music makes that likely anyway (p = 0.15). No clip shows a consistent lead or lag.
- **int:** in this library, music sets an overall pace and energy; frame-tight sync is a deliberate accent, not a default. That supports syncing a few causal moments precisely rather than every cut.

## Verification additions

On top of [render verification](render-verification.md): watch once muted (does the story still read?) and once with sound; step each planned hit and confirm its attack lands on or up to one frame after its picture event; listen across every loop seam for clicks; measure the export's loudness and true peak; confirm VO stays intelligible over music; confirm no unlicensed or placeholder audio ships.
