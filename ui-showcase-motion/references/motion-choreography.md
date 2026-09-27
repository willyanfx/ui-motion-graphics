# Motion choreography

## Design rhythm before curves

Build contrast within and between actions: prepare → travel → settle → hold. A slow opening followed by fast movement is not the same as ease-in-out on everything. Decide when attention changes, then pick curves for that intent.

When something feels wrong, diagnose which layer before changing all durations:

- **Scene rhythm** — time spent on each idea.
- **Velocity profile** — how one object accelerates and settles.
- **Overlap** — when secondary elements follow the lead.

## Starting values

Creative defaults to build from, then tune by eye in preview. They are not measurements from the reference library. Durations assume 30 fps; frames in brackets, rounded half up. Distances are in output pixels as seen on screen, after camera zoom.

### Durations

| Move | Start at | Range | Notes |
|---|---|---|---|
| Pointer travel | 450 ms [14] for ~400 px | 300–900 ms | Scale as `450 ms × √(distance / 400)`, capped at 900 ms (≈640 ms for 800 px) |
| Pointer hover before click / tap | 200 ms [6] | 120–350 ms | For touch there's no real hover — keep it as a visible pause so the viewer finds the target |
| Click press / release | 90 ms [3] down, 120 ms [4] up | — | Scale 0.9–0.94 on the pointer or the button, not both |
| Tap ripple | 350 ms [11] | 250–450 ms | Grows from the touch point to ~1.5× indicator size while fading out |
| Button / toggle state change | 180 ms [5] | 120–250 ms | Starts on the press frame |
| Panel or card expand | 500 ms [15] | 350–700 ms | Container leads; content follows 60–120 ms later |
| Content stagger per item | 40 ms [1–2] | 25–70 ms | Cap the total stagger near 400 ms |
| Chart / data morph | 600 ms [18] | 400–900 ms | Hold the final numbers ≥1.2 s |
| Camera push-in / pull-out | 800 ms [24] | 500–1200 ms | Zoom 1.2–1.5×. Finish the move before a press and hold still through the result |
| Scene transition (wipe, mask, shared object) | 500 ms [15] | 300–800 ms | Hard cut = 0 frames |
| Logo reveal | 900 ms [27] | 600–1500 ms | End on ≥0.5 s of stillness |

### Reading holds

A hold is the time content is fully visible and still — its entrance doesn't count.

| Content | Minimum hold |
|---|---|
| Result of an action (state visibly changed) | 1.0 s |
| Headline, ≤6 words | 1.5 s |
| Sentence or label group | ~0.3 s per word + 0.5 s |
| Number or statistic the viewer should remember | 1.5–2.0 s |
| End card with logo + CTA | 2.0–3.0 s |

Use the headline row for a standalone headline of up to six words; use the sentence row for longer copy or groups of labels. When separate content types share a beat, use the longer hold. For phone-first placements (Reels, TikTok, Shorts, Stories) multiply holds by 1.2 — viewers read at small size, often with the sound off.

### Curves

| Intent | CSS / GSAP | Remotion |
|---|---|---|
| Arrive and settle (default for entrances, pointer arrival) | `cubic-bezier(0.22, 1, 0.36, 1)` / `expo.out` | `Easing.bezier(0.22, 1, 0.36, 1)` |
| Leave with intent (exits, into a cut) | `cubic-bezier(0.64, 0, 0.78, 0)` / `power3.in` | `Easing.bezier(0.64, 0, 0.78, 0)` |
| Move between two resting states (camera, layout shift) | `cubic-bezier(0.65, 0, 0.35, 1)` / `power3.inOut` | `Easing.bezier(0.65, 0, 0.35, 1)` |
| Linear (progress bars, continuous rotation, scrubbing) | `linear` / `none` | `Easing.linear` |

### Springs

| Feel | stiffness / damping / mass | Use for |
|---|---|---|
| Precise, no overshoot | 200 / 30 / 1 | Serious UI, charts, text |
| Soft settle, tiny overshoot | 170 / 26 / 1 | Cards, panels, most UI |
| Playful | 250 / 16 / 1 | Badges, dots, pointer pops |
| Heavy | 120 / 22 / 1.5 | Large devices or full-screen moves |

Remotion's `spring()` takes these as `config: {stiffness, damping, mass}`; GSAP has no native spring — approximate with `back.out(1.4)` or `elastic.out(1, 0.6)`.

### When to change them

| Intent | Default | Change when |
|---|---|---|
| Direct arrival | Quick travel, long deceleration, stillness | Add anticipation only if the action would be missed |
| Deliberate departure | Brief preparation, speed into the cut | Shorten preparation if it feels hesitant |
| Playful response | Small overshoot, short damped settle | Remove bounce if it weakens precision or readability |
| Hierarchy reveal | Container → content → detail | Don't stagger every letter or row mechanically |
| Major statement | Short motion, generous hold | Cut copy before cutting the hold |

## Vertical and social formats

For 9:16 placements (1080×1920), start with these and check the platform's current guidance before final delivery:

- **Safe area:** Meta's Reels guidance, given as percentages, is to keep key content out of the top 14% (~270 px), the bottom 35% (~670 px) and 6% (~65 px) on each side. That leaves an area of roughly 950×980 px above the canvas center, and it's the zone to use for ads. For organic posts, preview the actual placement before relaxing these margins; keep text and the pointer's path clear of the right-side button rail. Put the end-card CTA in the middle third. These margins are provisional planning defaults from the seed notes, not independently verified current platform requirements. Confirm against [Meta's Reels ad specs](https://www.facebook.com/business/ads-guide/update/video/instagram-reels/outcome-engagement) and the actual placement preview before delivery (the official page required login during the 2026-09-27 review).
- **Fitting a web component:** render the component at a mobile CSS viewport (390–430 px wide), scale it to ~900–1000 px wide on the canvas, and position it so the action and its result stay inside the safe area (the rest of the component may run past it). Record viewport, scale, and offset in the timeline's `stage` block so geometry is reproducible. Don't squeeze a desktop layout into portrait; use its real mobile breakpoint.
- **Touch indicator instead of a cursor:** a mobile layout reads wrong with a desktop arrow. Use a soft circle ~64–80 px on a 1080-wide canvas (white at ~85% with a subtle shadow, or brand color), a 200 ms pause over the target, a press to ~0.9 scale, and a ripple. Action `type` is `tap`.
- **Text sizes on 1080×1920:** headlines 64–96 px, supporting lines 40–52 px, never under ~32 px; line width ≤ ~900 px; ≤ 2 lines per beat.
- **Loop:** Reels autoplay and repeat — decide whether the last frame should cut cleanly back to the first, or hold a composed end card.

## Classical principles for UI

- **Staging:** one dominant focal change at a time; background motion stays quieter than the UI result.
- **Anticipation:** a pointer pause, slight retreat, compression, or hover signals an action that might otherwise be missed.
- **Slow in / slow out:** decide where the object covers most distance and where it visibly settles.
- **Arcs:** curved paths feel natural for pointers and floating objects; straight paths read better on grids.
- **Follow-through / overlap:** a panel leads and its contents settle slightly later — but nothing should still be moving during the key reading moment.
- **Squash and stretch:** fine for dots, badges, playful pointers. Never distort text, charts, or serious controls.
- **Exaggeration:** enlarge a target or camera move enough to read on video without breaking the UI's logic.
- **Secondary action:** a click pulse or highlight supports the main change; drop it if the state change already explains itself.
- **Pose to pose:** define entry, peak, and resolved states before interpolating. Seed procedural particles so they repeat.

## Motion recipe

For each active element specify: selector/component; purpose; coordinate space; transform origin; from/to states; keyframes; ease or spring; overlap; hold; clipping/layering; reset behavior. Pixel values belong to a named output size; ratios name their reference box. See the recipe block in the [plan template](../assets/motion-plan-template.md).

Avoid scaling a parent and child at the same time unless intended. Camera is its own track on a scene wrapper. Evaluate pointer position in the right space after camera transforms.

## Pointer and identity

A pointer (cursor or touch indicator) has a hotspot, path, hover pause, press moment, and a resulting state. Show causality: arrive → hover/press → state change → read result.

For logo → pointer, inspect the available vectors and pick one method, named honestly:

1. Compatible SVG path interpolation (only when point structures can be matched).
2. Contract to a shared dot or triangle, then expand into the pointer.
3. Masked substitution while shape and position align.
4. A clean cut on movement.

Keep morph geometry and outgoing/incoming ownership explicit.

### Anchor the pointer to the component

Give meaningful targets stable selectors, e.g. `data-motion-id`. The action schedule names target and result: `{frame: 90, target: "[data-motion-id='weekly-filter']", result: "range=weekly"}`. A navigation target must exist in the outgoing state, before the action changes the view.

Derive the hotspot from the target's real bounds after fonts, assets, and layout are ready. Use the center or a deliberate inset point, minus the pointer artwork's hotspot offset. With design-time geometry, keep target, pointer, tooltip, and panel anchors in one shared layout definition.

Keep the pointer in the same transformed layer as its target, or project the target through the full transform chain exactly once — `getBoundingClientRect()` already returns viewport geometry, so don't apply the camera again. Re-measure on layout changes, but freeze or deterministically derive measurements so random-access rendering matches playback. Check the press frame at full resolution: pointer contact, button reaction, and the origin of any panel that opens.

## Camera and object handoffs

Represent camera motion as ordered poses: frame, position, zoom, transform origin, and an explicit cut flag (conventions in the [timeline example](../assets/timeline.example.json)). Don't land a press during a camera move — settle the camera first so the viewer can see what's being touched. Give each move a reason — establish context, approach an action, follow a result, restore the full view. A cut switches poses; it must never interpolate through unrelated space. Hold still when reading or precision benefits.

Directional blur for fast travel: scale it with displacement per frame in rendered coordinates, normalize for FPS, cap it (start near 12 px at 1080p), and remove it during holds and across hard cuts. Use overscan so frame edges don't show transparent strips.

When an object bridges scenes, define the source anchor, carry interval, destination anchor, and the exact ownership transfer. A temporary overlay can hold the object in output coordinates while scenes change underneath: hide the source when the overlay takes over, reveal the destination when it finishes. Match position, scale, shape, color, and stacking at both ends, and check the frames immediately before and after each transfer for duplicates or a missing frame. Remotion sequences and Hyperframes compositions both follow this contract.

## Scene transitions

- **Shared object** — links two ideas.
- **Directional wipe** — the layout implies travel.
- **Mask expansion** — entering a detail.
- **Hard cut** — a clean change of topic.

Blur can soften travel but resolves before reading. A crossfade implies two simultaneous states — check it doesn't confuse the interface story.

Save large rotations, elastic deformation, and long camera flights for moments that earn them. If the motion will also ship on a live website, plan a restrained version with reduced-motion behavior, focus preservation, and state changes that don't wait on animations finishing.
