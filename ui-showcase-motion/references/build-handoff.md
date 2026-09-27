# UI intake and implementation handoff

## Collect the component and assets

Check the conversation and project files first, then invite only what's missing — via chat, attachments, or a folder path. One component is usually enough; don't ask for the whole repository. Don't ask for uploads through a text-only question tool.

| Material | Ask for when missing | What it enables |
|---|---|---|
| Component source | HTML or React files and the entry point | Map the storyboard to real elements |
| Styling | Component CSS, shared styles/tokens, font files or references | Keep the UI's real appearance |
| Behavior | JS, existing animation code, dependencies, how to preview | Reuse behavior, spot animation conflicts |
| Visual assets | Logo (SVG preferred for shape work), icons, images, video, device mockups | Plan feasible reveals and transitions |
| Audio, if wanted | Music, VO, SFX, or "choose later"; licenses | Define cues without inventing sync ([sound module](sound-design.md)) |
| Demo states | Initial state, action, resulting state, sample data | Show real cause and effect |
| Boundaries | What to feature, required copy/CTA, what must not change | Stay aligned with intent |

Start with one short invitation adapted to context: "Share the component's HTML, CSS, and JavaScript — or point me to its folder — plus the assets it uses. Which element or interaction should be the focus?" React is equally fine. Follow up only for missing essentials.

Mark each material as supplied, found in project, missing, or placeholder. Check that referenced paths resolve and flag external dependencies before promising a self-contained render. Never silently replace a missing brand asset or rebuild supplied UI from an approximation; offer a labeled placeholder for planning and request the real asset before work that depends on it. If the user is unavailable, build with the labeled placeholder and list the asset as [open].

## Inspect the supplied UI

Read the entry HTML, relevant CSS/JS, component files, package manifest, asset paths, and font loading. Identify real selectors/components, bounds, responsive layout, clipping, stacking contexts, existing transforms, and states worth showing. Use a browser tool to see it rendered when available — source reading and visual checking are different evidence.

Build the element map (section 5 of the [plan template](../assets/motion-plan-template.md)): file → selector/component → role in the film → existing behavior → planned animation. A screenshot gives geometry, not editable DOM; keep any unverified selector marked `proposed:`.

Capture a baseline before adapting. Leave the source UI intact and build a separate composition for fake pointers, camera wrappers, staged data, or frame-driven interactions. Never trigger live purchases, messages, or destructive actions to stage a demo. Use deterministic fixtures, label fictional data, and don't invent product claims.

## Choose the continuity model

A montage or set of independent feature shots can use separate scenes. For a walkthrough, keep a continuous product session:

- Keep the app shell and persistent components mounted across beats; change the relevant panel or state instead of remounting and replaying entrances. Returning to a view restores its settled state.
- Every meaningful change has a visible cause — a click, a submission, or a signaled system event. Narration describes that sequence.
- Define one action schedule (frame → existing target → resulting state → optional completion frame). Derive visible state from the absolute frame, including all prior actions, so seeking straight to a late frame gives the same result as playback. Don't rely on replaying clicks, timers, or network requests.
- Plan voiceover after the action path, then adjust holds to fit it.
- In `timeline.json`, declare the persistent UI once in `layers[]` rather than per scene.
- Keep real UI components reusable; put camera, pointer, and orchestration logic outside them. Apply the [anchor and handoff rules](motion-choreography.md#anchor-the-pointer-to-the-component), and make sure a layout change can't slide a control away from its pointer.

## Parallel builds

Split implementation across tasks or agents only where no two of them change the same state. Good splits: independent scenes, the end card, audio, reference research. Bad splits: two tasks tuning the same scene, one editing shared tokens or `timeline.json` while another builds from the old version.

Record ownership in the plan before starting:

| Task | Scenes | May edit | Must not edit | Last sync |
|---|---|---|---|---|
| *A* | *S1–S2* | *scenes/S1, scenes/S2* | *layers/, timeline.json* | *2026-09-27* |

One owner holds persistent layers, shared styles, and `timeline.json`. Each task reads the plan before starting, records its boundary frames when it finishes, and reports if it moves a boundary. Saved build prompts and old files are history; the plan decides.

## Renderer choice

Use the user's preference. If undecided: existing React components favor Remotion; existing HTML/CSS/GSAP favors Hyperframes. Don't migrate the project or install both.

Check installed versions and follow the chosen renderer's skill and current official docs before writing tool-specific code.

### Remotion adapter

The film is a composition with width, height, FPS, and `durationInFrames`. Map scenes to `<Sequence>`s and compute visual state from `useCurrentFrame()`; be explicit about local vs global frames. Use `interpolate()` / `spring()` — browser timers and autonomous CSS animations are not the source of truth for rendering. Convert HTML to React only as needed, keeping CSS and assets where compatible.

Source: [Remotion fundamentals](https://www.remotion.dev/docs/the-fundamentals), checked 2026-09-27.

### Hyperframes adapter

Keep the HTML/CSS structure. The documented GSAP contract is a paused timeline registered in `window.__timelines` under the matching `data-composition-id`, with a finite duration and explicit tween positions. Use explicit end states so seeking is reliable, and let Hyperframes own the playhead and media playback. Nested compositions register their own timelines.

Source: [Hyperframes GSAP guide](https://hyperframes.heygen.com/guides/gsap-animation), checked 2026-09-27. Recheck before implementing.

## Deliverables

Scale to scope. A full handoff includes:

1. **`motion-plan.md`** — from the [template](../assets/motion-plan-template.md): current point and global rules, brief, treatment, references, materials, element map, scenes, recipes, transitions, assumptions, verification log.
2. **`timeline.json`** — follow the shape of [`timeline.example.json`](../assets/timeline.example.json): canvas/FPS/duration in frames, stable scene IDs, absolute frame boundaries, element targets, keyframes/eases/springs, camera poses, action schedule, transition ownership, audio cues, renderer, open items.
3. **Asset map** — plan section 4: existing files, adaptations, missing assets, fonts, footage, logo vectors, provenance notes.
4. **Build prompt** — plan section 10: implement the plan with the supplied UI, preserve mapped elements, resolve named open items, build deterministic seeking and preview, report render/QA evidence.

For planning-only work, use named placeholder roles in `timeline.json` and say that mapping is pending — never present imaginary selectors as executable.

## Verify at each stage

Use [render verification](render-verification.md) for the full procedure.

- **Plan:** causal story, complete boundaries, no gaps, transition ownership, final hold, readable content load.
- **Prototype:** first frame, each action and result, both sides of each transition, last frame, backward and random seeks (jump to a late frame directly).
- **Render:** real dimensions, FPS, duration, fonts/assets, clipping, missing frames, audio, and continuity in the exported file — not just the web preview.
- **Iterate:** name the main problem with the [problem categories](render-verification.md#problem-categories) and change only that layer.

Report what was actually checked. For a plan-only request, finish with a usable handoff and the next creative decision.
