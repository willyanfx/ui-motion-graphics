# Motion plan — New arrivals filter demo

Film status: planned. This is a complete fictional planning example paired with [timeline.example.json](timeline.example.json), not a source-verified or rendered film. Every creative choice below is **[assumed]**, pending a real brief; none records user approval.

## Current point

Last approved: none. In test: structural timeline only. Next action: inspect the supplied product grid and resolve the proposed source mappings before implementation.

## 1. Brief

- Takeaway: one tap reveals new arrivals in a product grid.
- Audience and placement: shoppers, vertical social feed.
- Canvas and runtime: 1080×1920, 30 fps, 450 frames / 15 seconds.
- Focus: one filter interaction; calm, precise motion.
- Palette: light neutral background #F6F6F4 to match a light product grid; primary and accent come from the component's own tokens once supplied.
- Renderer: Remotion, assuming a React source component is supplied.
- Story shape: feature proof, ending on a still CTA rather than a seamless loop.
- Sound: hybrid intent, with tap and confirmation cues planned. No music bed chosen; do not invent a beat grid.
- Preserve: real component typography, layout, labels, and filtering behavior. Camera, indicator, and card reflow are presentation treatments, not claims about live animation or speed.

## 2. Chosen treatment

**One tap, visible result.** A question introduces the grid. The camera approaches the filter, a touch indicator selects it, and the filtered cards settle. The viewer gets time to read the result before the camera restores context. A short benefit caption leads into a neutral mask reveal and a composed logo/CTA.

## 3. References

R04, prior atlas notes at 1.8–9.1 s: borrow a stable camera during an action and its result. **Evidence: prior sampled notes, not rechecked for this example.** None of this timeline's frame values is a measurement from that clip.

## 4. Materials and asset map

| Material | Proposed location | State | Pixel source |
|---|---|---|---|
| React grid and styles | ProductGrid.tsx and its imports | Missing; inspect actual supplied files | Live UI rendered in the composition |
| Fonts | Existing component font sources | Missing; preserve and verify loading | Live UI |
| Logo | assets/logo.svg | Missing; no stand-in approved | Supplied vector |
| Product images and sample data | Component fixtures | Missing; use deterministic, labeled demo data | Supplied images inside the live UI |
| Touch indicator, captions, end-card mask | Authored overlays | Planned | Coded animation |
| Tap and confirmation | Licensed audio sources to choose | Open | Library audio |

Figures and claims:

| ID | Exact value | Source | Checked | Used in | Status |
|---|---|---|---|---|---|
| new-this-week | 24 | Proposed: product feed, new-arrivals count for the capture week | — | S5 benefit caption | open |

## 5. Element map

All source mappings are **proposed**, including the component name and both selectors. Observed source behavior is unknown until intake.

| Source / role | Proposed target | Planned treatment |
|---|---|---|
| Persistent mobile UI | ProductGrid | Mount frames [0, 345); retain settled state across scene boundaries |
| New-arrivals filter | [data-motion-id='filter-new'] | Tap at 130; determine its actual behavior from source |
| Cards | [data-motion-id='product-card'] | Reflow 136–151, then preserve filter=new |
| Touch indicator | Authored overlay | Travel to the measured filter center, press, then fade out |
| End-card background | Authored output-space circle | Expand from the measured filter center; stay mounted until 450 |

## 6. Scenes

| ID | Frames [start, end) | Purpose and continuity |
|---|---|---|
| S1-hook | [0, 84) | Question over the persistent grid; hold 15–69, then fade caption |
| S2-select-filter | [84, 189) | Camera settles by 108; indicator arrives 124, taps 130; cards settle 151; hold result; indicator gone by 188 |
| S3-read-result | [189, 243) | Continue the same close view and settled filter state; no entrance or reset |
| S4-restore-context | [243, 273) | Pull back while retaining the filtered grid |
| S5-result | [273, 345) | Benefit caption ("{claim:new-this-week} new arrivals, one tap.") holds 279–333; neutral mask covers UI by 344. If the count can't be sourced, drop the figure and keep the timing |
| S6-end-card | [345, 450) | Logo and CTA settle by 372; hold through frame 449 |

All scenes remain `to direct`; structural validity is not creative approval. The JSON is the canonical source of exact frames.

## 7. Motion and sound recipes

Use the timeline's stage viewport, scale, and offset as proposed starting geometry. Measure the filter after fonts/assets load. Scene camera poses transform the stage and scene-space overlays together; output-space captions stay fixed. Match the camera pose at every scene boundary.

The action schedule changes the selected state at 130, with card reflow 136–151. Derive all later frames from that schedule so direct seeking to 300 restores filter=new. Pointer motion is 14 frames with a 6-frame pause, followed by 3 frames down and 4 up. Its hotspot is the target center minus (36, 36).

The tap cue locks to frame 130; confirmation locks to `completeAt: 151`. Both sources are open. Mastering targets of −14 LUFS / −1 dBTP are proposals, not measured output.

## 8. Transitions and ownership

S1→S2 removes only the headline. S2→S3→S4→S5 retain the same UI layer. At 333, the `end-card-background` layer begins a circular mask reveal in output space. Freeze its anchor at the filter's projected center on that frame; grow radius 0→2300 by 344. Clip to the canvas. The app-shell ends at 345, fully covered. Keep the background through 449 at z-index 20, with end-card content at 30. This is a mask reveal, not a chip morph.

## 9. Open decisions

Resolve the source UI, selectors, fonts, fixture data, logo, feature copy, the new-arrivals count, and licensed audio. Verify safe-area fit in the intended placement. If the actual grid cannot perform the stated filter action, revise the story before implementing it.

## 10. Build prompt

Implement the paired timeline with the inspected React component. Preserve real UI behavior and label any presentation-only reflow. Resolve the proposed targets and missing assets. Mount persistent layers once, derive state from the absolute frame, and apply camera transforms exactly once. Read the benefit figure from the `new-this-week` claim. Render the tap and reflow passage (frames 120–155) first and step it frame by frame before the full draft. Deliver a seekable preview and a draft export; inspect each press, scene boundary, and final frame. Keep status at planned until actual implementation evidence exists.

## 11. Verification plan

Run `validate_timeline.py timeline.json` during planning; run it with `--require-resolved` after resolving declared placeholders. These checks cannot verify DOM targets or media quality. In the renderer, check frames 0, 108, 124, 130, 151, 188–189, 242–243, 272–273, 332–345, 372, and 449; seek directly to 300 and backward to 130. Then review the complete export muted and with sound, confirm source fidelity, reading time, assets, dimensions, FPS, and duration, and record actual results in the project's verification log.
