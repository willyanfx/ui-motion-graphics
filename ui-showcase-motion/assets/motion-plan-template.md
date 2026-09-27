# Motion plan — <project name>

Film status: <planned | prototyped | previewed | rendered | inspected>  ·  Last updated: <YYYY-MM-DD>

Keep one plan per project and update it in place. Film status tracks evidence — how far the whole film has been built and checked; each scene's status (section 6) tracks approval. Decision tags used throughout: **[decided]** (user chose or confirmed), **[assumed]** (your reversible default), **[open]** (needs input). Evidence tags: **obs** (seen in source/reference — add coverage: overview, dense, or playback), **int** (your reading of it), **prop** (your proposal).

## Current point

| Last approved | In test | Next action |
|---|---|---|
| *S1 hook (v02)* | *S2 pointer timing (v03)* | *Tighten S2 travel, then render S3* |

**Global rules** — feedback that applies to every scene. Add one when a note recurs or the user says "always" or "never".

- *[decided] No overshoot on text or numbers.*

> Rows in *italics* are examples showing the level of detail. Replace or delete them — never ship them. If the project has no references, write "none" in section 3.

## 1. Brief

| Field | Value | Tag |
|---|---|---|
| Takeaway | What the viewer should understand or do after watching | |
| Audience & placement | e.g. Instagram Reel, product page hero, launch post | |
| Canvas | e.g. 1080×1920 @ 30 fps | |
| Runtime | e.g. 12 s | |
| Focus | One interaction / one screen / a journey across screens | |
| Feel | e.g. calm and precise | |
| Renderer | Remotion / Hyperframes | |
| Story shape | Feature proof / problem → relief / before-after / journey / assembly / list / question → answer / loop | |
| Sound | Mode (music-led / sound-design-led / hybrid / voice-led / silent-first), BPM if music-led, loudness target | |
| Must stay unchanged | Layout, copy, brand elements the film must not alter | |

## 2. Chosen treatment

**<Treatment name>** — one-sentence promise.

- Opening image:
- Causal sequence: <action> → <result> → <result>
- Rhythm: e.g. quiet open → quick travel → readable result → still end card
- Ending: composed end frame / seamless loop
- Other directions considered and why not (if any were explored):

## 3. References

| ID | File | Window | What we borrow | What we don't | Evidence |
|---|---|---|---|---|---|
| *R06* | *Collect_UI_-_Tab_animation…* | *0.30–1.10 s* | *Content changes inside a fixed tab container* | *Their portraits and copy* | *obs: dense* |

## 4. Materials and asset map

| Material | Location | State |
|---|---|---|
| *Component source* | *`src/components/ProductGrid.tsx`* | *supplied* |
| Styles & fonts | | |
| Logo (SVG) | | |
| Images / icons / footage | | |
| Sample data | | |
| Audio | | |

## 5. Element map

| Source | Selector / component | Role in the film | Existing behavior (obs) | Planned animation (prop) |
|---|---|---|---|---|
| *`ProductGrid.tsx`* | *`[data-motion-id="filter-new"]`* | *Tap target, S2* | *Filters grid instantly, no transition* | *Pause 200 ms, press, selected state; cards reflow 500 ms (staged — live UI has no transition)* |

Mark unverified selectors `proposed:`.

## 6. Scenes

| ID | Frames `[start, end)` | Seconds | Purpose | Focus | Action → result | Exit / continuity | Reference | Status |
|---|---|---|---|---|---|---|---|---|
| *S1* | *[0, 84)* | *0–2.8* | *Hook* | *Headline* | *Question appears over the full grid* | *Headline fades out over persistent grid, overlap [69, 84)* | *none* | *approved v02* |
| *S2* | *[84, 189)* | *2.8–6.3* | *Show cause* | *"New" filter* | *Camera settles, pointer travels, taps; grid filters* | *Selected state persists* | *R04* | *in test v03* |

Status: `to direct` → `in test` → `revise` → `approved`; a replaced approach becomes `superseded` (keep the row, note what replaced it).

### Sound map

| Frame | Cue | Role | Sync to | Gain | Source / license | Status |
|---|---|---|---|---|---|---|
| *130* | *tap* | *sfx* | *press on "New" filter* | *−6 dB* | *library name, license* | *open* |

## 7. Motion recipes

For each animated element: target · purpose · coordinate space · transform origin · from → to · keyframes · ease/spring · overlap · hold · clipping/layering · reset.

```
S2 pointer (touch indicator)
  target: [data-motion-id="filter-new"] center, minus indicator hotspot (36, 36)
  space: scene wrapper (inside camera)
  camera: push-in 84→108 (24 f), then still 108→189 through press and result
  travel: 110→124 (14 f ≈ 450 ms), cubic-bezier(0.22, 1, 0.36, 1)
  pause: 124→130 (6 f)
  press: scale 1→0.9 over 130→133, back to 1 over 133→137; ripple 130→141
  result: chip state 130→135; cards reflow 136→151, spring 170/26/1
  hold: 151→189 (38 f = 1.27 s ≥ 1.0 s × 1.2 phone)
```

## 8. Transitions & ownership

| Boundary | Out state | In state | Overlap (tail of outgoing scene) | Owner of shared object |
|---|---|---|---|---|
| *S5→S6* | *Selected chip at rest* | *Chip fills frame as end-card background* | *[333, 345)* | *Overlay; source chip hidden at 333, end card shown at 345* |

## 9. Assumptions & open decisions

- [assumed] …
- [open] …

## 10. Build prompt

Implement this plan in <renderer> using the supplied component at <path>. Preserve the mapped elements and their layout. Keep persistent UI mounted across scenes and derive state from the absolute frame. Resolve these open items: <list>. Provide deterministic seeking and a preview. Report render/QA evidence: <frames to check — each press, both sides of each transition, last frame>.

## 11. Verification log

| Date | Stage | Version / file | What was checked | Decision |
|---|---|---|---|---|
| *2026-09-27* | *previewed* | *renders/S2_v03.mp4* | *Press frame 130, result hold, backward seek* | *revise: travel feels slow; keep camera and hold (locked)* |

Name renders by scene and version, and never overwrite an approved one. A "looks good" becomes a row: which version, what's approved, what's still pending.
