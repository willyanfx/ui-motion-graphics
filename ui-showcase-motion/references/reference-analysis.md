# Analyze references

## Inventory before interpretation

Record each file, duration, dimensions, frame rate, audio presence, and file hash. Hash duplicates once and retain all filenames. Do not delete duplicates. Assign stable IDs in a saved project manifest; on later imports preserve existing ID-to-file mappings rather than renumbering after a sort.

The helper creates an initial inventory (its IDs follow filename sorting within that run):

```sh
python3 /path/to/ui-showcase-motion/scripts/index_videos.py /path/to/videos /path/to/analysis/contact-sheets
```

It accepts a directory or a single file, `--samples` (default 12), `--start`, `--end`, and `--workers`. Keep a single-file detail run in a separate output folder: its local R01 ID does not replace the video's library ID. Use the inventory's video-stream duration, since audio can continue after the last video frame.

## Observe at two scales

1. Overview every unique clip across its duration. Longer videos need additional samples or playback if major sections fall between thumbnails. Label the coverage accurately: sampled overview, dense passage review, continuous playback, or unavailable.
2. For a technique worth adapting, inspect the relevant short passage at closer intervals or by frame stepping. Observe the before state, initiation, peak travel, settlement, and hold. When image tools cannot play video, timestamped sequences support spatial analysis; they do not establish the felt rhythm of uninterrupted playback.
3. Review sound only with an actual audio-capable tool. The presence of an audio stream is not evidence of beat synchronization. If sound has not been heard, leave musical timing unverified.

Do not use filenames as visual evidence. A still/contact sheet is not proof of working hover behavior, implementation library, exact easing, or spring physics. Separate camera motion in a screen recording from authored scene motion.

## Reference card

For each clip save: ID and filename; type (UI interaction, product showcase, brand motion, editorial/type, process recording); checked time windows and coverage; visible action; transition mechanism; visual anchor; pacing evidence and uncertainty; reusable principle; possible application to the user's UI; caveat.

Use the seed [reference atlas](reference-atlas.md) to shortlist patterns. Reinspect selected source moments before claiming exact timings. Report “approximately 0.5–0.8 seconds” when bounded by samples, not a fabricated frame count.

## Synthesize into a motion vocabulary

Group by what motion does, not just aesthetics: focus attention, explain a state change, build a hierarchy, carry continuity, punctuate a claim, or resolve identity. Recommend a small compatible set for a project. Keep a dominant transition family and a deliberate contrasting accent; combining every reference usually weakens consistency.

Finish with coverage totals, duplicate mappings, unavailable files, a shortlist with timestamps, and concrete adaptations. A pattern catalogue is analysis; the project storyboard remains a proposal.
