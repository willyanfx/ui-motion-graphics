# UI intake and implementation handoff

## Collect the component and assets

Check the conversation and project files first. Then explicitly invite the user to provide the missing materials using normal chat, attachments, or a local folder path. Do not demand a whole repository when one component is sufficient, and do not request uploads through a text-only question tool.

| Material | What to request when missing | What it enables |
|---|---|---|
| Component source | HTML or React/component files and the relevant entry point | Map the storyboard to real elements |
| Styling | Component CSS, shared styles/design tokens, and required font files or font references | Preserve the UI's actual appearance |
| Behavior | JavaScript, existing animation code, relevant dependencies, and how to preview it | Reuse behavior and identify animation conflicts |
| Visual assets | Logo, preferably SVG for shape work; icons, images, illustrations, textures, video, or device mockups used in the scenes | Plan feasible reveals, transitions, and compositions |
| Audio, when wanted | Music, voiceover, sound effects, or a stated preference to choose later | Define audio cues without inventing synchronization |
| Demonstration states | Initial state, action, resulting state, and suitable sample data | Show meaningful cause and effect |
| Creative boundaries | Which elements to feature, required copy/CTA, and what must remain unchanged | Keep the showcase aligned with the user's intent |

Start with one concise invitation, adapted to the known context: “Share the component's HTML, CSS, and JavaScript—or point me to its folder—plus the assets it uses. Which element or interaction should be the main focus?” React source is an equally valid input. Follow up only for missing essentials.

Record each material as supplied, found in project, missing, or proposed replacement. Check that referenced paths resolve and identify external dependencies before promising a self-contained render. Do not silently replace a missing brand asset or rebuild supplied UI from an approximation. Offer a labeled placeholder when it helps planning; request the real asset before work that depends on it.

## Inspect the supplied UI

Read entry HTML, relevant CSS and JS, component files, package manifest, asset paths, and font loading. Identify real selectors/components, bounding boxes, responsive layout, clipping, stacking contexts, existing transforms, and states worth demonstrating. Use an available browser tool to inspect rendering; distinguish source inspection from visual verification.

Create a compact element map: file/location → selector/component → narrative role → existing behavior → planned animation → reuse/adaptation needed. A screenshot provides geometry, not editable DOM. Missing HTML does not block ideation, but every unverified selector must stay labeled as proposed.

Capture a baseline before adapting. Preserve source UI and create a separate composition when the showcase requires fake cursors, camera wrappers, staged data, or frame-driven interactions. Avoid executing live purchases, messages, or destructive application actions to stage a demo. Use deterministic fixtures for a render; label fictional data and avoid inventing factual product claims.

## Pick a renderer with the user's context

Use their preference if given. If undecided, an existing React component set favors Remotion reuse; existing HTML/CSS/GSAP favors Hyperframes reuse. These are adaptation considerations, not claims that one tool is universally better. Do not migrate the project or install both by default.

Inspect installed versions and follow the chosen renderer's available skill and current official documentation before writing tool-specific implementation. This skill defines the creative contract; renderer-specific code still needs preview/render validation.

### Remotion adapter

Represent the film as a composition with width, height, FPS, and duration in frames. Map scene boundaries to sequences and compute visual state from the current frame. Be explicit about local versus global frame numbers. Use frame-driven interpolation or springs; ordinary elapsed browser timers and autonomous CSS animation are not the source of truth for rendering. Convert reusable HTML to React only as needed, preserving CSS and assets where compatible.

Source: [Remotion fundamentals](https://www.remotion.dev/docs/the-fundamentals), checked 2026-09-27. Consult the installed version's sequencing/animation documentation for API details.

### Hyperframes adapter

Keep HTML/CSS structure where possible. The documented GSAP contract uses a paused timeline registered in `window.__timelines` under the matching `data-composition-id`. Define a finite composition duration and explicit tween positions. Use explicit endpoint states for reliable seeking, and let Hyperframes own the playhead and media playback. Nested compositions register their own timelines. Recheck the current contract before implementation.

Source: [Hyperframes GSAP guide](https://hyperframes.heygen.com/guides/gsap-animation), checked 2026-09-27. Use its authoring skill if installed; otherwise consult official docs and the local CLI help.

## Deliverables

Scale to scope. A small motion concept needs a concise plan; a full film handoff normally includes:

1. `motion-plan.md`: brief, chosen treatment, references, scene table, motion recipes, assumptions, and current decision status.
2. `timeline.json`: canvas/FPS/runtime, stable scene IDs, absolute frame boundaries, element mapping, keyframes/eases, transition overlap ownership, optional audio cue points, and renderer choice. Use one declared time unit; keep seconds only as a derived convenience.
3. Asset map: existing files, adaptations, missing assets, fonts, footage, logo vectors, and any uncertain provenance relevant to actual reuse.
4. Build prompt: implement the chosen plan with the supplied UI, preserving the mapped elements; resolve specifically named open details; create deterministic seeking and preview; report render/QA evidence.

Do not produce a purportedly executable timeline with imaginary selectors. For planning-only work, use explicitly named placeholder roles and say mapping remains pending.

## Verify at the appropriate stage

- Plan: causal story, complete boundaries, no unintended gaps, transition ownership, final hold, and readable content load.
- Prototype: first frame, each action, each result, both sides of transitions, last frame, and backward/random seeks. Test a late frame directly without playing earlier frames.
- Render: verify actual dimensions, FPS, duration, fonts/assets, clipping, missing frames, intended audio, and scene continuity in exported media. Preview the rendered file, not just the web page.
- Iterate: identify whether the issue is story, staging, duration, curve, camera, sound, or implementation; change the responsible layer while preserving chosen direction.

Report what was actually checked. If only a plan was requested, finish with a usable handoff and the next creative decision, without presenting it as a rendered video.
