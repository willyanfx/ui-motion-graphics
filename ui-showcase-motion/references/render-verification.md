# Verify the film and its mechanics

Scale this review to the assignment. A creative plan needs internal consistency; a delivered film needs visual evidence from its export. Avoid treating a small contact sheet or a numerical score as proof that animation feels right.

## Review loop

1. Confirm the composition loads with one useful preview, then render a draft covering the intended sequence. Review the whole film for story, continuity, readable holds, clipping, and missing assets. Contact sheets help locate problems; continuous playback is needed to judge rhythm. Label either unavailable check honestly.
2. Inspect affected passages at higher sample density. For interaction details use full-resolution crops and adjacent frames, not only thumbnails. Batch related fixes by cause: geometry, state, camera, timing, or assets.
3. Render the changed passage to verify the fix, then check its boundaries in the complete export. Recheck unrelated areas only when the change affects them. Test direct late-frame and backward seeking in the renderer as well.
4. Report blocking defects separately from optional polish. Automated or AI review findings are candidates; confirm them against actual frames. Do not override a chosen creative direction solely to satisfy a generic score.

## Action and continuity checks

- At each press, the target exists in the outgoing state, the pointer hotspot overlaps its intended hit area, and the reaction occurs at the planned time. Account for deliberately delayed results or loading states.
- Persistent UI does not flash, remount, or replay its entrance during one uninterrupted interaction. State changes have a visible user/system cause. Narration and UI agree about the object being acted on.
- For an object carried across scenes, inspect one frame before, at, and after each ownership transfer. There is one visible copy, and its geometry, color, and layer order remain continuous.
- At fast camera moves inspect frame edges, text legibility after settling, and blur removal. Intended hard cuts must not become accidental interpolated moves.
- Inspect the final displayed frame and planned end hold; verify the exported duration, dimensions, FPS, assets, and intended audio separately.

## Optional reference comparison

Use [compare_videos.py](../scripts/compare_videos.py) when comparing a measured passage or locating changes between two exports. It needs Python, Pillow, FFmpeg, and FFprobe. It reads the inputs and writes to a new, empty output directory; it does not alter the videos or run a renderer.

```sh
python3 /path/to/ui-showcase-motion/scripts/compare_videos.py reference.mp4 rendered.mp4 /path/to/review --fps 8 --duration 4 --reference-start 3 --render-start 5
```

The result includes paginated reference/render pairs, `report.json`, a mean grayscale pixel difference at the sampled times, the largest sampled inter-frame changes in the render, and metadata/available-duration differences. Aspect ratios are preserved by padding. Declared start offsets align the selected passage; there is no duration rescaling. Sampling labels are requested seek times, not decoded frame timestamps. For fast mechanics, select a short passage at source FPS and inspect full-resolution frames separately.

The score covers only the common sampled interval and can miss unmatched tails, color differences, fine text, easing between samples, and brief glitches. Duration mismatch is reported separately. Large inter-frame changes can be intentional cuts, flashes, or motion; they are inspection candidates, not automatic failures. There is no universal pass threshold.

For an adaptation with different copy, assets, layout, or pacing, prioritize the chosen story and corresponding visual beats. Do not revert a sound creative choice simply because it differs more from the reference. Low pixel difference cannot certify good animation, correct interaction, or an accessible live UI.
