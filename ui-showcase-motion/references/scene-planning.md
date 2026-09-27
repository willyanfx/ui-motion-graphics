# Scene planning

Build the story around one primary takeaway. Use as many scenes as the story needs; hook → demonstration → payoff → identity is a starting shape, not a formula.

Write each scene as a visible action with a reason. "The pointer selects the weekly filter; the chart reorganizes; the total stays still long enough to read" is buildable. "Make it premium and smooth" is not.

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

## Example: 15-second starting story

| Window | Beat | Continuity |
|---|---|---|
| 0–2 s | Hook: a short question or identity mark over the product | Crossfade or cut into the UI; a logo-to-pointer bridge is one option if the brand suits it |
| 2–5 s | Establish the UI; pointer travels, pauses, selects one control | Target stays anchored while the pointer decelerates |
| 5–9 s | UI visibly changes; camera approaches the result; hold | Selected state stays legible |
| 9–12 s | Pull back to the full screen and a short benefit line | Result stays identifiable in context |
| 12–15 s | Resolve to identity and CTA with a final hold | Composed end frame, or a deliberate loop |

Inspect the real UI before choosing that control or promising that state change, and replace generic beats with the product's differentiating action. The matching implementation shape is [`timeline.example.json`](../assets/timeline.example.json).
