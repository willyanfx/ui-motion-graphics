# Motion choreography

## Design rhythm before curves

Use contrast within and between actions: prepare → travel → settle → hold. A slow opening followed by fast movement is not the same as applying ease-in-out to every object. Define when attention changes, then choose curves for that intent.

Separate **scene rhythm** (time spent on ideas), **velocity profile** (how one object accelerates), and **overlap** (when secondary elements follow). Diagnose which of these feels wrong before changing all durations.

The following are creative defaults for experimentation, not measurements extracted from the library:

| Intent | Starting treatment | When to change it |
|---|---|---|
| Direct arrival | Quick travel, long deceleration, then stillness | Add anticipation only if it improves comprehension |
| Deliberate departure | Brief preparation, increasing speed into the cut | Reduce preparation if the video feels hesitant |
| Playful response | Small overshoot with a short damped settle | Remove bounce if it weakens precision or readability |
| Hierarchy reveal | Container leads, content follows, detail last | Avoid staggering every letter or row mechanically |
| Major statement | Short motion followed by a generous hold | Reduce copy before eliminating the hold |

## Classical principles translated to UI

- **Staging:** one dominant focal change at a time. Keep background motion quieter than the UI result.
- **Anticipation:** a pointer pause, slight retreat, compression, or hover can signal an action. Use it where the action would otherwise be missed.
- **Timing and spacing / slow in and out:** decide where the object covers most distance and where it visibly settles. Record a curve or keyframe sequence only when defining implementation, not as an unsupported claim about reference footage.
- **Arcs:** give a pointer or floating object a purposeful curved path when it feels natural. A straight path can be clearer for grid alignment.
- **Follow-through / overlapping action:** a panel leads and its contents settle a little later. Avoid secondary movement continuing through the key reading moment.
- **Squash and stretch:** useful for an abstract dot, badge, or playful pointer. Preserve the legibility and proportions of text, charts, and serious controls.
- **Exaggeration:** enlarge a target or camera move enough for video readability, while preserving the real UI's logic.
- **Secondary action:** a click pulse or highlight supports the main change. Remove it when the state change already explains itself.
- **Pose-to-pose planning:** define entry, peak, and resolved states before filling in interpolation. For procedural particles, use repeatable trajectories/seeds.

## Motion recipe

For each active element specify: selector/component; purpose; coordinate space; transform origin; from/to states; keyframe times; ease or spring parameters; overlap; hold; clipping/layering; reset behavior. Values in pixels belong to a named output size; ratios must name their reference box.

Avoid simultaneous parent and child scale changes unless intentional. Camera movement is a separate track on a scene wrapper. Pointer position must be evaluated in the correct space after camera transformations.

## Cursor and identity

“Mouse” can mean a pointer graphic or physical device; resolve that only when it affects the concept. A pointer has a hotspot, path, hover pause, click moment, and resulting state. Anchor the hotspot to the actual hit target. Show causality: arrive → hover/press → state change → read result.

For logo → cursor, inspect available vectors. Options: compatible SVG path interpolation; contraction to a shared dot/triangle then expansion; masked substitution while shape and position align; or a simple cut on movement. Identify the method honestly. Do not promise arbitrary SVG paths can directly morph. Keep morph geometry and outgoing/incoming ownership explicit.

### Anchor the pointer to the component

Give meaningful targets stable selectors or IDs. The action schedule should name the target and result, for example `{atFrame: 90, target: "[data-motion-id='weekly-filter']", result: "weekly-selected"}`. This is illustrative syntax, not a required framework API. A navigation target must exist in the outgoing state, before the action changes the view.

Derive the hotspot from the target's actual bounds after fonts/assets and the relevant layout are ready. Use the center or a deliberate inset point in its hit area; subtract the pointer artwork's hotspot offset. If using design-time geometry, keep target, pointer, tooltip, and panel anchors in one shared layout definition instead of independent coordinate guesses.

Keep the pointer in the same transformed layer as its target, or project its target through the complete transform chain exactly once. `getBoundingClientRect()` already returns viewport geometry; do not apply the camera a second time. Re-resolve geometry for state/layout changes, but freeze or deterministically derive measurements for random-access rendering. Verify the press frame at full resolution, including pointer contact, button reaction, and the resulting panel's origin.

## Camera and object handoffs

Represent camera motion as ordered poses with time/frame, position, zoom, transform origin, and explicit cut flags. Record the reason for each move: establish context, approach an action, follow a result, or restore the whole view. A cut switches poses; it must not accidentally interpolate through unrelated space. Hold still when reading or precision benefits from it.

For rapid travel, optional directional blur can follow displacement per unit time in the rendered coordinate space. Normalize for FPS, cap the blur, and remove it during reading holds and across hard cuts. Blur the scene content with adequate background/overscan, checking frame edges for transparent strips. This is a visual approximation to test, not a measured physical shutter model.

When an object bridges scenes, define the source anchor, carry interval, destination anchor, and exact ownership transfer. A temporary overlay can keep the object in output coordinates while scenes change underneath. Hide the source copy when the overlay takes over, and reveal the destination copy only when the overlay finishes. Match position, scale, shape, color, and stacking at both boundaries; check immediately before and after each transfer for duplicates or a missing frame. Remotion sequences and Hyperframes compositions must both honor this same ownership contract.

## Scene transitions

Use a shared object when it links ideas, a directional wipe when the layout implies travel, a mask expansion to enter a detail, and a hard cut for a clean change of topic. Blur can soften travel but must resolve before reading. Crossfade can imply two simultaneous states; check whether that confuses the interface story.

Reserve large rotations, elastic deformation, and long camera flights for moments that justify them. A showcase's theatrical motion may need a separate restrained treatment if reused in a live website. For interactive output, define reduced-motion behavior, focus preservation, and state changes independent of animation completion.
