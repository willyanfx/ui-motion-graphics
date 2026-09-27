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

## Scene transitions

Use a shared object when it links ideas, a directional wipe when the layout implies travel, a mask expansion to enter a detail, and a hard cut for a clean change of topic. Blur can soften travel but must resolve before reading. Crossfade can imply two simultaneous states; check whether that confuses the interface story.

Reserve large rotations, elastic deformation, and long camera flights for moments that justify them. A showcase's theatrical motion may need a separate restrained treatment if reused in a live website. For interactive output, define reduced-motion behavior, focus preservation, and state changes independent of animation completion.
