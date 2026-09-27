# Scene planning

Build a story around one primary takeaway. Use as many scenes as the story needs; a hook → demonstration → payoff → identity sequence is a starting option, not a required formula.

Write each scene as a visible action with a reason. “The pointer selects the weekly filter; the chart reorganizes; the total remains still long enough to read” is buildable. “Make it premium and smooth” is not.

## Scene contract

For every scene record:

| Field | Meaning |
|---|---|
| ID / purpose | Stable label and what this beat communicates |
| Start / end | Absolute seconds; end is exclusive |
| Entry composition | Visible objects, positions, camera, reading hierarchy |
| Focus | The single primary attention target |
| Action / result | Cursor or system action and resulting UI state |
| Beats | Anticipation, movement, settle, readable hold; omit unnecessary phases |
| Exit / continuity | Shared shape, color, direction, object, or deliberate hard cut |
| UI mapping | Actual selectors/components or explicitly proposed placeholders |
| Reference | ID, source time window, borrowed principle |
| Sound | Optional cue; mark unverified/unselected audio |
| Open decisions | Missing asset, geometry, claim, or preference |

Separate camera travel from object animation. Establish which coordinate space each uses. For transitions between scenes, name both outgoing and incoming states, their overlap interval, and which owns the shared object. A logo cannot disappear and reappear as a cursor without a defined bridge.

## Timeline math

Keep absolute boundaries in one canonical timeline. At the selected FPS convert boundaries once: `startFrame = round(startSeconds * fps)`, `endFrame = round(endSeconds * fps)`, `durationInFrames = endFrame - startFrame`. Use half-open intervals `[start, end)`; the last displayed frame is `endFrame - 1`. Quantize seconds back from frames if needed. Record transitions as overlaps instead of adding their duration twice. Check for unexplained gaps and conflicting owners of an animated property.

Do not allocate equal time to every scene by default. A rapid connective move can be short; a new UI state, text block, or result needs enough time to understand. Validate reading time at the actual output size. Tighten scope when the requested content exceeds the available runtime.

## Example: provisional 15-second story

This is an invented starting proposal, not measured reference choreography.

| Window | Beat | Continuity |
|---|---|---|
| 0–2s | Small identity mark settles, then bridges into a pointer | Match centroid and visual weight; mask swap if silhouettes cannot morph cleanly |
| 2–5s | Establish UI; pointer travels, pauses, selects one control | Keep target anchored while pointer decelerates |
| 5–9s | UI visibly changes; camera approaches the useful result; hold | Keep selected state legible |
| 9–12s | Pull back to reveal the complete screen and concise benefit | Result remains identifiable in context |
| 12–15s | Resolve into identity and CTA, with final reading hold | End on a composed frame or design a deliberate loop |

Inspect the actual UI before choosing that control or promising the state change. Replace generic feature beats with the real product's differentiating action.
