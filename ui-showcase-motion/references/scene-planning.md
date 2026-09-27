# Scene planning

Build the story around one primary takeaway. Use as many scenes as the story needs; hook → demonstration → payoff → identity is a starting shape, not a formula.

Write each scene as a visible action with a reason. "The pointer selects the weekly filter; the chart reorganizes; the total stays still long enough to read" is buildable. "Make it premium and smooth" is not.

## Story shapes

Pick the shape before the scenes. Feature proof is the default; switch when the brief has a real problem to solve, a person to follow, or a list to deliver.

| Shape | Structure | Best for | Watch out |
|---|---|---|---|
| Feature proof (default) | Hook → one action proves the product → payoff → identity | Demos, launches | Choosing the wrong action — find the differentiator |
| Problem → relief | Show the friction (clutter, waiting, steps), then the product removes it | Products that fix a known pain | Don't fake a competitor's UI; stylize the "before" |
| Before / after | Same frame, same camera, state swaps | Redesigns, automation, cleanup | The swap needs a visible cause, not a crossfade |
| Journey | One implied user moves through tasks; time cues (notifications, clock, light) carry continuity | Workflows, day-in-the-life, onboarding | One goal only; more than three tasks in 30 s blurs |
| Assembly | The product builds itself piece by piece, then one action proves the whole | Platforms, modular tools | Reading time for the finished whole |
| Numbered list | "Three things…" chapters with a fixed title grid | Social, feature roundups | Each item still needs one action and a hold |
| Question → answer | The hook asks; the UI answers | Search, AI, analytics | The answer must be visible in the UI, not just in copy |
| Loop story | The ending hands back to the opening | Reels, web heroes | Plan the seam from the start ([loops](kinetic-type.md#loops)) |

**A protagonist without a face.** A UI film can still have a character: the pointer as the actor (hesitates, decides, acts), a named avatar or sender in notifications, or on-screen captions as the narrator. Keep one protagonist with one goal and at most one obstacle in anything under 30 s.

**Who tells it.** Choose one voice: on-screen copy, voiceover, or the UI itself (labels, notifications, typed text). On-screen copy follows the [reading holds](motion-choreography.md#reading-holds); voiceover is written after the action path at about 150 words per minute (~35 words in 15 s), with captions for muted viewing. Mixing all three competes for attention. Sound mode follows from this choice — see [sound for UI films](sound-design.md#choose-a-sound-mode).

## Scene contract

Record for every scene (this is section 6 of the [plan template](../assets/motion-plan-template.md)):

| Field | Meaning |
|---|---|
| ID / purpose | Stable label and what the beat communicates |
| Start / end | Absolute frames (seconds derived); end is exclusive |
| Entry composition | Visible objects, positions, camera, reading hierarchy |
| Focus | The single primary attention target |
| Action / result | Pointer or system action and the resulting UI state |
| Beats | Anticipation, travel, settle, readable hold — drop phases you don't need |
| Exit / continuity | Shared shape, color, direction, object, or a deliberate hard cut |
| UI mapping | Real selectors/components, or `proposed:` placeholders |
| Reference | ID, source window, borrowed principle |
| Sound | Optional cue; tag audio [open] until chosen |
| Open decisions | Missing asset, geometry, claim, or preference |

Keep camera travel separate from object animation and name each one's coordinate space. For each transition name the outgoing and incoming states, their overlap, and who owns the shared object. A logo can't vanish and reappear as a pointer without a defined bridge.

## Timeline math

Keep one canonical timeline in frames. Keyframes live inside their scene's `[start, end)`; UI that persists across scenes goes in a top-level layer rather than being re-declared per scene. Convert once, rounding half up: `startFrame = floor(startSeconds × fps + 0.5)`, `endFrame = floor(endSeconds × fps + 0.5)`, `durationInFrames = endFrame − startFrame`. Intervals are half-open `[start, end)`; the last visible frame is `endFrame − 1`. Record transitions as overlaps rather than adding their duration twice; the overlap frames sit at the tail of the outgoing scene (e.g. `[54, 60)` for a boundary at 60). Anything that must animate in during the overlap belongs to a persistent layer. Check for unexplained gaps and for two tracks animating the same property.

Don't give every scene equal time. Connective moves can be short; a new UI state, text, or result needs reading time (see [reading holds](motion-choreography.md#reading-holds)). If the content doesn't fit the runtime, cut scope rather than holds.

A scene in the middle of the film doesn't need its own entrance and exit. Enter on an action already under way and leave while the next one begins; only the opening and the end card need composed starts and stops.

Once the film works, make variants from the same opening rather than new films: alternate hooks, CTAs, end cards, or aspect ratios, driven by props. Keep the shared frames identical so variants can be compared and cut together.

## Example: 15-second starting story

| Window | Beat | Continuity |
|---|---|---|
| 0–2 s | Hook: a short question or identity mark over the product | Crossfade or cut into the UI; a logo-to-pointer bridge is one option if the brand suits it |
| 2–5 s | Establish the UI; pointer travels, pauses, selects one control | Target stays anchored while the pointer decelerates |
| 5–9 s | UI visibly changes; camera approaches the result; hold | Selected state stays legible |
| 9–12 s | Pull back to the full screen and a short benefit line | Result stays identifiable in context |
| 12–15 s | Resolve to identity and CTA with a final hold | Composed end frame, or a deliberate loop |

Inspect the real UI before choosing that control or promising that state change, and replace generic beats with the product's differentiating action. The matching implementation shape is [`timeline.example.json`](../assets/timeline.example.json).
