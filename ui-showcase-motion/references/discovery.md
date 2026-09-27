# Creative discovery

First pull out what's already known: product, audience, message, placement, duration, references, available UI, renderer, sound, constraints. Mark the unknowns, but don't turn them all into questions at once.

For a vague request, a good first round:

1. What should someone understand or do after watching? If unsure, offer: feature demo, product introduction, or design portfolio piece.
2. What's the focus: one interaction, a complete screen, or a journey across screens? Ask for the idea in plain language, not a spec.
3. Which feeling fits: calm and precise, playful and elastic, or bold and fast? Invite a reference ID and a specific moment they like or dislike.

Then resolve only the next gaps that change the plan: placement/aspect ratio, length, logo/CTA, available HTML or React, sound/voiceover, Remotion vs Hyperframes. Suggest defaults with their consequences — "I suggest a 15-second draft with three feature beats; that leaves time to read the result."

Shortcuts: if the user supplies HTML first, inventory it while asking about the story. If they bring a storyboard, skip ideation and refine choreography. If they want a close reference adaptation, ask which visual qualities matter most.

## Bring in the actual component

Once the story is clear, invite the component before finalizing element-specific scenes, following the [component and asset intake](build-handoff.md#collect-the-component-and-assets). Accept a folder path, pasted source, or attachments, and use what's already available.

Explain what helps: the HTML or React component, its CSS and JS, and the logo, images, icons, and fonts it uses. Ask which parts to feature, which interaction or before/after state matters, and what must stay unchanged.

Reflect back a short inventory before naming animation targets: components and states, assets, missing essentials, proposed focal elements. With only an idea or screenshot, keep going with a conceptual storyboard and leave element mapping pending.

## Make the choice visual in words

Offer up to three compact treatments, each with:

- A one-sentence promise and the opening image.
- A causal sequence: this action causes this result.
- A rhythm: quiet opening → quick transition → readable result.
- One or two reference moments and exactly what's borrowed.
- Ending or loop behavior, and the effort difference.

Example treatments for a dashboard:

**Follow the pointer:** logo resolves into a pointer, pointer picks a real filter, chart changes, camera returns to the full dashboard. Best for cause and effect. Needs a deliberate silhouette bridge.

**Build the product:** one card expands into a panel, other panels join, the full UI resolves, then one useful action proves it works. Best for layout and hierarchy. Needs careful shared bounds.

**Editorial feature tour:** bold short statement, close view of one meaningful action, clean cut to the next benefit, composed end card. Best for launches. Needs disciplined copy and reading holds.

Ask for a choice or combination when the user wants to collaborate; if they already asked you to decide and build, decide. Record choices, rejected approaches, open questions, and assumptions in `motion-plan.md` (start from the [template](../assets/motion-plan-template.md)).
