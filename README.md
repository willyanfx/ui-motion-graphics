# UI Showcase Motion

An agent skill for planning UI showcase videos from product ideas, reference clips, and existing HTML/CSS/JS or React components.

It helps shape the story, analyze references, plan scenes and motion, and prepare a Remotion or Hyperframes handoff using `motion-plan.md` and `timeline.json`. It also guides review of prototypes and exported videos.

## Install

Requires Node.js and npm. Choose your agent:

```sh
# Codex
npx skills add willyanfx/ui-motion-graphics -a codex

# Claude Code
npx skills add willyanfx/ui-motion-graphics -a claude-code

# Other supported agents: choose interactively
npx skills add willyanfx/ui-motion-graphics
```

Run inside your project, or add `-g` to install across projects. See the [Skills CLI documentation](https://github.com/vercel-labs/skills#supported-agents) for supported agents.

## Use

Ask your agent: “Use the ui-showcase-motion skill to plan a 15-second product demo from my UI.”

Share your component, assets, and any reference clips. Optional video-analysis helpers require Python 3, Pillow, FFmpeg, and FFprobe. Reference videos are not bundled.

## Checks

```sh
python3 ui-showcase-motion/scripts/validate_timeline.py ui-showcase-motion/assets/timeline.example.json
PYTHONDONTWRITEBYTECODE=1 python3 ui-showcase-motion/tests/test_regressions.py
```

The example is a complete planning timeline with explicitly unresolved sources and audio. The validator checks structure; it does not verify assets or rendering. Media regression tests require Pillow, FFmpeg, and FFprobe and use temporary synthetic clips.
