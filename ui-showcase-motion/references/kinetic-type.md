# Kinetic type and loops

Use this module when type carries a beat: a hook, a chapter title, a feature list, pricing, a CTA, or a whole social loop. In a UI showcase, type beats frame the proof — they don't replace it. A fully type-led reel is right when the product is itself typographic (fonts, editors, design tools) or the brief is a teaser with no UI to show yet.

## Source set (L-series)

Lexington Motion's "Foundry" reel templates, [product page](https://lexingtonthemes.com/remotion/type-foundry-reel-templates), sampled 2026-09-27. Ten public preview videos, each 10.0 s, 1080×1920; the page states Remotion 4, React, TypeScript, Google Fonts, 30 fps, content passed as props. Each preview got 10 frames at 0.5, 1.5 … 9.5 s, drawn from the page's own video elements. **Coverage: sampled overview only** — nothing between 1 s samples, no source code, no audio. Durations below are bounded by that spacing.

These are commercial templates. Borrow the mechanism, not their layouts, copy, fonts, or palettes. If the user owns the pack, the plan can name a template as a starting point; otherwise don't rebuild one frame-for-frame.

| ID | Template | Observed (obs: overview) | Reusable principle (int) |
|---|---|---|---|
| L01 | Weights | Stacked repetitions of a two-word name, each line at a different weight; weights roll down the stack from thin to black. Small pill labels top and bottom. Palette inverts dark → light around 5 s. | A variable axis animated with a phase offset per line reads as a wave, not a flicker |
| L02 | Glyphs | Full-width rows of glyphs drift horizontally under a fixed header (name, glyph count, weights). Rows reveal clipped from the top. A square-tile wipe near 4.5 s and again near 9.5 s swaps lavender ↔ navy. | Endless rows under a fixed header show breadth; a tile wipe marks the loop's halves |
| L03 | Specimen | Lines of place names alternate solid and outlined; the solid/outline assignment shifts between samples. A vertical band wipes across near 4.5 s and 9.5 s, inverting the palette. | Solid vs outline marks one active item in a list without moving the layout |
| L04 | Licences | Rounded pills (formats, features) drop in one by one, tilted at mixed angles, piling up. A large price line appears under the pile, then pills tumble out downward and the palette inverts; repeats. | A pile of tags reads as "lots included" fast; a gravity exit clears the stage for a loop |
| L05 | Trial | A type tester: text types in with a caret; a pointer drags a weight slider and the sample thickens; a size slider pushes the sample past the frame. Cut to a mixed-weight headline on white, a pointer clicks a button that changes to a confirmation state; a colored panel rises from the bottom. | **Control drives preview** — the closest to a UI showcase: one drag, one visible result, then a CTA with a state change |
| L06 | Takeover | Fixed poster grid: giant two-line headline, subhead, logo box, footer. Background color changes every ~1–2 s; at some changes the headline letters squash to thin horizontal slivers at mixed heights and restore. Subhead copy changes per chapter. | Keep the grid; change color and one line of copy per chapter. Letter squash works as a chapter punctuation |
| L07 | Stretch | One condensed word with a single large stat below. The label steps through weight names 100 → 700 while a bulge of heavier, wider letters travels across the word; color changes per step. | A traveling "lens" over letters shows an axis range while the word stays readable |
| L08 | Knockout | A weight name and its number per chapter. The headline's letters grow at staggered, jagged heights until they cover the frame — the letters are already the next chapter's background color, so they become the new background. | **Type-as-wipe**: the outgoing headline turns into the incoming background, one continuous object |
| L09 | Column | A 3D advertising column rotates in steps; each face is a pricing poster (tier, one line, price). The background color matches the face in front, ~2–3 s per face. | A rotating solid turns pricing tiers into one object with a clear "next" |
| L10 | Tilt | Full-width color bands scroll upward, one short word per band, building a sentence; the conveyor settles on a CTA poster (URL, big number) held for ~4 s, then continues into the opening bands. | A conveyor builds a sentence word by word, stops for the CTA, and loops by construction |

## System rules across the set (int)

- **One fixed grid per film.** Metadata, logo box, and footer never move; only the headline, one copy line, and color change. Same principle as R06's persistent container.
- **Scale contrast.** Tiny UI-like labels (pills, captions, footer) against giant display type. The small layer carries facts; the large layer carries attitude.
- **Flat, cycling palette.** Four or five flat colors plus black and white, reassigned per chapter so type and background trade roles.
- **Midpoint inversion.** A 10 s loop is two halves split by a wipe or palette swap, so repeats feel less monotonous.
- **Everything is a prop.** Words, numbers, weights, colors, and CTA copy are inputs; motion is computed from them. Plan type beats the same way (see [timeline fields](#timeline-fields)).

## Adaptations for UI showcase films (prop)

| Need | Borrow | Adaptation |
|---|---|---|
| Show a control's effect | L05 | Pointer drags a real slider, toggle, or picker; the preview updates every frame from the control's value. Apply the [pointer rules](motion-choreography.md#pointer-and-identity) — settle the camera before the grab |
| "Everything included" | L04 | Integrations, features, or plan inclusions as pills that pile, then a price or CTA line with a proper hold; the gravity exit clears for the next scene or loop |
| Pricing tiers | L09 | Three or four tier faces on a rotating column or card drum; hold each price as a statistic |
| Chapter titles in a feature tour | L06, L08 | Fixed title grid with per-chapter color; the knockout wipe hands off to the next chapter's UI background |
| Hook for a font, editor, or design tool | L01, L07 | A variable axis wave on the product name, resolving to one still weight before the UI appears |
| Breadth of a library or catalog | L02, L03 | Marquee rows of component names, templates, or logos under a fixed header; outline/solid marks the one about to be demonstrated |
| Closing CTA for a loop | L10 | Conveyor of benefit words into the end card; the conveyor carries the seam back to frame 0 |

## Starting values (prop)

Creative defaults at 30 fps, frames in brackets; tune in preview. None of these are measured from the L-series.

| Move | Start at | Notes |
|---|---|---|
| Per-letter stagger | 1–2 f per character | Cap the total near 12 f; stagger words, not letters, for anything over ~12 characters |
| Variable-axis sweep, one line | 1.2 s [36] thin → black | Phase offset 3–5 f between stacked lines; `Easing.bezier(0.65, 0, 0.35, 1)` |
| Letter squash punctuation | 10 f total | `scaleY` 1 → 0.08 → 1 from the baseline, 1 f stagger, random heights seeded per letter |
| Knockout wipe | 15 f | Letters scale 1 → ~10× with exit ease, 1–2 f stagger; switch the background on the first fully covered frame |
| Tile wipe | ~18 f | 4×7 grid on 1080×1920, diagonal stagger 1 f, each tile 6–8 f |
| Pill drop | 4–6 f apart | Spring 250/16/1, rotation ±4–12° seeded per pill; stop adding at ~9 pills |
| Gravity exit | 15 f | `Easing.bezier(0.64, 0, 0.78, 0)` on y, rotation grows 1.5×, 1 f stagger from the top of the pile |
| Column step | 18 f per face | Spring 170/20/1 or ease-in-out; face hold ≥ 1.8 s (statistic hold × 1.2 on phone) |
| Chapter length | ≥ 1.8 s | Headline hold × 1.2 on phone; a one-word chapter can go to ~1.2 s only if the idea repeats |
| Typed text | 2 f per character | Caret steady while typing, blinking ~0.5 s when idle; don't type more than ~16 characters on camera |

Reading holds from [motion choreography](motion-choreography.md#reading-holds) still apply: the text must be undistorted and still for the whole hold.

## Guardrails

- **Distort display words only.** Squash, stretch, and knockout are for one to three display words and resolve before the hold. Never distort UI labels, body copy, prices at their hold, or chart text.
- **Real axes only.** A weight wave needs a variable font with that axis; stepping between static weights snaps and flickers. Check the font's license covers video and embedding.
- **Load before measuring.** Fit giant words after the font is loaded, and freeze the measurement so seeking matches playback. Watch the first frames for a fallback-font flash.
- **One transition family plus one accent.** Knockout + squash + tile wipe + conveyor in one 15 s film is a sampler, not a story.
- **Keep the tags honest.** Pills and price lines are claims — use the product's real features and prices, or label placeholders.

## Loops

A loop is a scene whose last frame hands off to frame 0. Put the seam inside a transition (a wipe, a conveyor, a gravity exit), never inside a hold, so the jump is covered by motion. Frame `durationInFrames − 1` must lead into frame 0 exactly as any frame leads into the next: same positions, colors, and axis values once the transition completes, and the same velocities. A pointer or spring still moving at the last frame must be moving the same way at frame 0, or the seam shows as a hitch even when positions match. For a two-half loop, make the second half the first with swapped colors and derive both from one function of `frame % half`. Decide early whether the placement loops (Reels, web backgrounds) or ends on a still end card; don't do both. A music loop must match the film loop exactly ([beat grid](sound-design.md#music-and-the-beat-grid)).

## Timeline fields

Add these to [`timeline.json`](../assets/timeline.example.json) when a project uses type beats; keep the existing field names.

```json
{
  "loop": { "seamless": true, "seamTransition": "T-conveyor", "halves": 2 },
  "props": { "name": "Product", "palette": ["#111111", "#F5F2EA", "#F2C94C", "#4A7FE0"], "features": ["Offline mode", "Shared boards"] },
  "scenes": [
    {
      "id": "S1-title",
      "start": 0, "end": 60,
      "elements": [
        {
          "id": "title",
          "target": "prop:name",
          "split": "chars",
          "stagger": { "frames": 1, "from": "start" },
          "keyframes": [
            { "frame": 0,  "fontVariation": { "wght": 100 } },
            { "frame": 36, "fontVariation": { "wght": 900 }, "ease": "cubic-bezier(0.65, 0, 0.35, 1)" }
          ],
          "fit": { "width": 950, "measure": "after-font-load" },
          "seed": "title-squash"
        }
      ]
    }
  ]
}
```

`loop` and `props` sit at the top level beside `canvas`; element fields go inside a scene as usual. `split` is `chars | words | lines`; `seed` makes jitter (heights, rotations) repeat on every render; `prop:` targets resolve from the `props` block.

## Implementation notes

Check the renderer's current docs before writing code.

- **Remotion:** drive `fontVariationSettings` (or a numeric `fontWeight` on a variable font) from `interpolate()`; load fonts through `@remotion/google-fonts` or `@remotion/fonts` and wait before measuring; `@remotion/layout-utils` has `fitText()` and `measureText()` for sizing a word to a width; use `random(seed)` for deterministic jitter. Split text into per-character spans in React. A column or drum works with CSS `perspective`, `transform-style: preserve-3d`, and `rotateY` per face. Expose words, numbers, and colors as composition props with a schema so they can be edited in Studio.
- **Hyperframes:** tween per-character spans on the paused GSAP timeline; animate the `font-variation-settings` string or a variable weight; give every split and random value an explicit end state so seeking is exact.

## Verification additions

On top of [render verification](render-verification.md): play the seam at least twice in a row (`ffmpeg -stream_loop 1 -i render.mp4 -c copy loop-check.mp4`); step the last 5 and first 5 frames and compare each moving object's per-frame displacement across the seam; confirm the axis actually changes continuously (inspect adjacent frames mid-sweep); check that giant words don't clip at the canvas edge except where intended; check no fallback font appears in frame 0–3; confirm every distorted word is fully restored before its hold starts.
