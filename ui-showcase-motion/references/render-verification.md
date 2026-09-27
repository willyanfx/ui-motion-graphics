# Verify the film and its mechanics

Scale review to the assignment: a plan needs internal consistency; a delivered film needs evidence from its export. Contact sheets locate problems; only continuous playback judges rhythm. A numerical score never proves the animation feels right.

## Review loop

1. Confirm the composition loads, then render a draft of the full sequence. Review the whole film for story, continuity, reading holds, clipping, and missing assets. If you can't play video, say which checks were sampled only.
2. Inspect problem passages more densely — full-resolution crops and adjacent frames for interaction details. Group fixes by cause: geometry, state, camera, timing, or assets.
3. Re-render the changed passage, then check its boundaries in the full export. Test late-frame and backward seeking in the renderer.
4. Report blocking defects separately from polish. Treat automated or AI review findings as candidates until confirmed on real frames. Don't override the chosen creative direction to satisfy a generic score.

## Action and continuity checks

- At each press: the target exists in the outgoing state, the pointer hotspot overlaps its hit area, and the reaction lands on the planned frame (allowing for deliberate loading states).
- During one uninterrupted interaction, persistent UI doesn't flash, remount, or replay its entrance. Every state change has a visible cause. Narration and UI agree on what's being acted on.
- For an object carried across scenes, check one frame before, at, and after each ownership transfer: exactly one visible copy, with continuous geometry, color, and layering.
- On fast camera moves: frame edges, text legibility after settling, blur fully removed. Intended hard cuts must not become interpolated moves.
- The final frame and end hold look intended; exported duration, dimensions, FPS, assets, and audio are verified separately.

## Optional reference comparison

[`compare_videos.py`](../scripts/compare_videos.py) samples a reference and a render side by side. It reads the inputs and writes into a new or empty output folder only.

```sh
python3 /path/to/ui-showcase-motion/scripts/compare_videos.py reference.mp4 rendered.mp4 /path/to/review \
  --fps 8 --duration 4 --reference-start 3 --render-start 5
```

Output: paginated reference/render pairs, `report.json` with mean grayscale difference per sample, the largest inter-frame changes in the render (cut/glitch candidates), and duration/dimension differences. Aspect ratios are padded, start offsets align the passage, and nothing is time-stretched. Timestamps are requested seek times; for fast mechanics sample a short passage at source FPS and inspect full-resolution frames separately.

Reading the score: it covers only the common sampled window and misses color shifts, fine text, motion between samples, and brief glitches. There's no pass threshold. Large changes may be intended cuts. For an adaptation with different copy, layout, or pacing, compare corresponding beats and don't revert a sound creative choice just because it differs more from the reference.
