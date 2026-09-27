# Creative discovery

First extract what is already known: product, audience, message, destination, duration, references, available UI, renderer, sound, constraints. Mark unknowns; do not turn all of them into immediate questions.

For a vague request, a useful first round is:

1. What should someone understand or want to do after watching? If uncertain, offer feature demonstration, product introduction, or design portfolio showcase.
2. What should be the hero: one interaction, a complete screen, or a journey across screens? Ask for the idea in plain language, not a technical spec.
3. Which feeling fits: calm and precise, playful and elastic, or bold and fast? Invite a reference ID and a specific moment they like or dislike.

Once the direction is clearer, resolve only the next consequential gaps: placement/aspect ratio, approximate length, logo/CTA, available HTML or React, sound/voiceover, and Remotion versus Hyperframes. Suggest reasonable defaults with their consequences. Example: “I suggest a 15-second draft with three feature beats; that leaves room to read the result.” These are draft choices, not reference measurements.

If the user supplies HTML first, inventory it while asking about the story. If they bring an already chosen storyboard, skip ideation and refine choreography. If they ask for an exact reference adaptation, clarify which visual qualities matter while retaining their chosen direction.

## Bring in the actual component

Once the intended story is understood, invite the user to share the component before finalizing element-specific scenes. Follow [component and asset intake](build-handoff.md#collect-the-component-and-assets). Accept a workspace path, pasted source, or attached files; use what is already available instead of asking them to send it again.

Explain what is useful in plain language: the HTML or React component, its CSS and JavaScript, and the logo/images/icons/fonts or other assets it uses. Then ask which parts should be featured, which interaction or before/after state matters, and what must stay unchanged. Ask only the unanswered questions needed for the next step.

Inspect the materials and reflect back a short inventory before naming animation targets: available components and states, available assets, missing essentials, and proposed focal elements. If only an idea or screenshot is available, continue with a conceptual storyboard and keep implementation mapping pending.

## Make the choice visual in words

Offer up to three compact treatments, each with:

- A one-sentence promise and opening image.
- A causal sequence: this action causes this result.
- A rhythm description: quiet opening → quick transition → readable result, for example.
- One or two reference moments and precisely what is borrowed.
- Ending/loop behavior and a practical effort difference.

Example treatments for a dashboard, all explicitly proposals:

**Follow the cursor:** logo resolves into a pointer, pointer chooses a real filter, chart changes, camera returns to the full dashboard. Good for demonstrating cause and effect. Needs a deliberate silhouette bridge.

**Build the product:** one card expands into a panel, other panels join, the complete UI resolves, then one useful action proves the system works. Good for layout and hierarchy. Needs careful shared bounds.

**Editorial feature tour:** bold short statement, close view of one meaningful action, clean cut to the next benefit, composed product end card. Good for launch stories. Needs disciplined copy and reading holds.

Ask for a choice or combination when the user wants collaboration; do not require formal approval if they already asked you to decide and build. Record choices, rejected approaches, open questions, and assumptions in `motion-plan.md` so refinements stay consistent.
