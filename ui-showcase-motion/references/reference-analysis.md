# Analyze references

## Inventory before interpreting

Record each file's duration, dimensions, frame rate, audio presence, and hash. Duplicates are analyzed once; keep every filename and never delete files. IDs are stable once assigned — later imports add new IDs rather than renumbering.

```sh
# First run: overview of a folder (12 samples per video by default)
python3 /path/to/ui-showcase-motion/scripts/index_videos.py /path/to/videos /path/to/analysis/contact-sheets

# Later import: keep existing IDs, number only new files
python3 /path/to/ui-showcase-motion/scripts/index_videos.py /path/to/videos /path/to/analysis/contact-sheets-2 \
  --keep-ids /path/to/analysis/contact-sheets/manifest.json

# Dense look at one passage: 8 samples/s from 3 s to 7 s
python3 /path/to/ui-showcase-motion/scripts/index_videos.py /path/to/reference.mp4 /path/to/analysis/detail-R09 \
  --start 3 --end 7 --fps 8 --keep-ids /path/to/analysis/contact-sheets/manifest.json
```

Options: `--samples N` or `--fps F`, `--start`, `--end`, `--per-sheet` (default 24; dense runs paginate), `--workers`, `--keep-ids MANIFEST` (reuse IDs by path, then by file hash). The manifest records each sheet's sample times, `duplicate_of` for repeated byte streams, and display dimensions after rotation. Use a fresh output folder per run. Durations come from the video stream, since audio can run past the last frame.

Each run also writes `id-registry.json`, retaining IDs for clips absent from the current scan. Keep it beside `manifest.json`: `--keep-ids manifest.json` automatically reads the companion history. You can pass `--keep-ids id-registry.json` directly when moving only the registry. Carry that history forward through subset scans and removals so an old ID is never reused for a new clip. Legacy manifests still work, but cannot recover IDs already lost before the registry existed. The manifest lists only the current scan; inactive registry entries are history, not current footage or regenerated sheets.

## Observe at two scales

1. **Overview** every unique clip across its full length; long clips need more samples. Label coverage accurately: sampled overview, dense passage, continuous playback, or unavailable.
2. **Detail** for a technique worth adapting: inspect the short passage densely — before state, initiation, peak travel, settle, hold. Frame sequences support spatial analysis; felt rhythm needs playback.
3. **Sound** with [`audio_events.py`](../scripts/audio_events.py) ([how to read it](sound-design.md#analyze-reference-sound)) or by listening. An audio stream existing is not evidence of beat sync; a sync claim needs picture changes landing on hits clearly more often than chance.

Filenames aren't visual evidence. Separate screen-recording camera motion from authored scene motion.

## Match depth to the task

- **Inspiration:** the overview shortlists references. Twelve frames don't establish a cut list.
- **Selected technique:** sample the relevant passage at ~6–8 per second, read every sheet, then step through fast actions at source FPS.
- **Close timing match:** identify every cut and continuous move in the section using decoded frame timestamps. Scene-detection or luminance jumps are candidates — fades, flashes, occlusion, and camera moves trigger them too.

For timing work keep an event table: source timestamp/frame and FPS → visible action → target → bounds or anchor → confidence → proposed destination timing. Keep measured source timing separate from new creative timing. Convert to the destination FPS once; don't stretch one film to fit the other. A new dense pass on a clip doesn't upgrade the atlas's coverage for other clips.

## Remake an existing film

When the user brings their own earlier film (an old launch video, a hand-animated promo) to rebuild, it's a source, not a reference: its copy, identity, and structure are theirs to reuse. Confirm they own it, and ask what the remake is for — the product changed, the pacing felt off, a new aspect ratio, or making it editable.

1. Inventory it like any clip, then do a close timing match of the whole film: an event table of every cut, move, and text hold at the original's FPS.
2. Collect the real design files (Figma exports, the live component, logo vectors) and rebuild from those. Tracing frames from the video reproduces its compression and loses editability.
3. Write a beat map before planning scenes:

| Original window | Beat | Keep / change / drop | New scene | Rebuilt from |
|---|---|---|---|---|
| *0.0–2.4 s* | *Logo on blue* | *keep* | *S1* | *logo.svg, brand tokens* |
| *2.4–6.0 s* | *Three app screens in one pass* | *change: one screen per beat, longer holds* | *S2–S3* | *live component* |

4. Lock what must survive (music, duration, key copy) in the plan's global rules; everything else follows the normal modules. Base holds on [reading holds](motion-choreography.md#reading-holds), not the original's timing. Remakes tend to come out too fast, and pacing notes are the main lever.
5. Compare corresponding beats with [`compare_videos.py`](../scripts/compare_videos.py). A difference is a question, not a defect.

If it will be posted beside the original, the credit line says what was rebuilt, from which files, and who revised the pacing.

## Reference card

For each clip: ID and filename; type (UI interaction, product showcase, brand motion, editorial/type, process recording); checked windows and coverage; visible action; transition mechanism; visual anchor; pacing evidence; reusable principle; possible application; caveat.

Shortlist from the [reference atlas](reference-atlas.md), then recheck the chosen moments before quoting timings. Say "about 0.5–0.8 s" when that's what samples bound.

## Synthesize a motion vocabulary

Group by what the motion does: focus attention, explain a state change, build hierarchy, carry continuity, punctuate a claim, resolve identity. Recommend a small compatible set — one dominant transition family plus one contrasting accent. Mixing every reference weakens the film.

Finish with coverage totals, duplicate mappings, unavailable files, a timestamped shortlist, and concrete adaptations.
