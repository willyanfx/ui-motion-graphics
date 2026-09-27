# Verify the film and its mechanics

Scale review to the assignment: a plan needs internal consistency; a delivered film needs evidence from its export. Contact sheets locate problems; only continuous playback judges rhythm. A numerical score never proves the animation feels right.

## Review loop

1. Confirm the composition loads, then render a draft of the full sequence. Review the whole film for story, continuity, reading holds, clipping, and missing assets. If you can't play video, say which checks were sampled only.
2. Inspect problem passages more densely — full-resolution crops and adjacent frames for interaction details.
3. When the user or your own review reacts, say what works, specifically — it becomes a lock. Name the one main problem and its [category](#problem-categories), and whether it's local to a scene or structural.
4. Change only that layer and state the locks alongside the fix ("keep camera, hold, and colors; shorten pointer travel from 14 to 10 f"). Don't rebuild a scene to fix one detail or re-render the whole film for one passage.
5. Re-render the changed passage, then check its boundaries in the full export. Test late-frame and backward seeking in the renderer.
6. Update the scene's status and the verification log. If the note should apply everywhere, add it to the plan's global rules.
7. Report blocking defects separately from polish. Treat automated or AI review findings as candidates until confirmed on real frames. Don't override the chosen creative direction to satisfy a generic score.

### Problem categories

The one diagnostic vocabulary for this skill; other modules point here.

| Category | Typical symptoms |
|---|---|
| Story | Action unclear without narration; a scene changes nothing |
| Causality | Result lands before or without its cause; state changes with no visible trigger |
| Pointer | Hotspot misses the target, travel too slow or fast, press out of sync with the reaction |
| Continuity | Persistent UI flashes or replays its entrance, duplicate object at a handoff, an old state returns |
| Camera | Unmotivated move, press during a move, frame edge revealed, blur left on |
| Timing | Hold too short to read, equal time on every beat, overlapping moves steal focus |
| Curve | Ease or spring feels wrong for the intent (bouncy on serious UI, stiff on playful) |
| Readability | Text too small for placement, distortion during a hold, content outside the safe area |
| Fidelity | UI differs from the source, wrong font or asset, placeholder shipped as real |
| Renderer | Seek mismatch, dropped frames, font flash, wrong export size, FPS, or duration |
| Sound | Hit early or off its frame, a sound on every motion, music masking VO, loudness off target or clipping, click at a loop seam |

For Timing and Curve, [motion choreography](motion-choreography.md#design-rhythm-before-curves) narrows it further: scene rhythm, velocity profile, or overlap.

## Action and continuity checks

- At each press: the target exists in the outgoing state, the pointer hotspot overlaps its hit area, and the reaction lands on the planned frame (allowing for deliberate loading states).
- During one uninterrupted interaction, persistent UI doesn't flash, remount, or replay its entrance. Every state change has a visible cause. Narration and UI agree on what's being acted on.
- For an object carried across scenes, check one frame before, at, and after each ownership transfer: exactly one visible copy, with continuous geometry, color, and layering.
- On fast camera moves: frame edges, text legibility after settling, blur fully removed. Intended hard cuts must not become interpolated moves.
- For a seamless loop, play the seam at least twice and step the last and first five frames; see [kinetic type verification](kinetic-type.md#verification-additions).
- With sound: watch once muted and once with audio; follow the [sound checks](sound-design.md#verification-additions).
- The final frame and end hold look intended; exported duration, dimensions, FPS, assets, and audio are verified separately.

## Optional reference comparison

[`compare_videos.py`](../scripts/compare_videos.py) samples a reference and a render side by side. It reads the inputs and writes into a new or empty output folder only.

```sh
python3 /path/to/ui-showcase-motion/scripts/compare_videos.py reference.mp4 rendered.mp4 /path/to/review \
  --fps 8 --duration 4 --reference-start 3 --render-start 5
```

Output: paginated reference/render pairs, `report.json` with mean grayscale difference per sample, the largest inter-frame changes in the render (cut/glitch candidates), and duration/dimension differences. Aspect ratios are padded, start offsets align the passage, and nothing is time-stretched. Timestamps are requested seek times; for fast mechanics sample a short passage at source FPS and inspect full-resolution frames separately.

Reading the score: it covers only the common sampled window and misses color shifts, fine text, motion between samples, and brief glitches. There's no pass threshold. Large changes may be intended cuts. For an adaptation with different copy, layout, or pacing, compare corresponding beats and don't revert a sound creative choice just because it differs more from the reference.
