---
name: kunpeng-midjourney
description: Design, rewrite, and critique Midjourney prompts using Kunpeng's curated visual-direction system and 84 style presets. Use when the user requests Midjourney imagery, Midjourney style selection, prompt refinement, reference-image strategy, or stylize/chaos/raw parameter guidance; do not activate for another image engine unless the user wants Midjourney-compatible output.
---

# Kunpeng Midjourney Visual Director

Turn the user's visual intent into a concise Midjourney prompt without changing the requested subject, count, identity, action, relationship, product structure, layout, aspect ratio, or required text.

## Workflow

1. Extract a fact lock before styling: subject, count, identity, action, spatial relationship, environment, composition, deliverable, and exclusions. Treat these as immutable unless the user asks to change them.
2. Choose one primary visual mechanism from [references/style-index.md](references/style-index.md). Search the full catalog with `python3 scripts/mj_style.py search "<need>"` when no obvious match exists.
3. Read the exact preset with `python3 scripts/mj_style.py show <style-id>`. Prefer `production-calibrated` for predictable production and `director-calibrated` for an open art-direction brief.
4. Write one compact English prompt in this order:
   - subject identity and action
   - environment and spatial relationship
   - composition and camera
   - lighting and color
   - material or medium
   - finish and exclusions
5. Keep parameters separate from prose when the target client exposes structured fields. Append flags only when the user needs a paste-ready Midjourney command.
6. Return the selected style, final prompt, parameters, and any important exclusions. If the user asks for only the prompt, return only the prompt.

## Prompt Rules

- Preserve user facts. Do not invent people, dialogue, props, symbols, text, brands, actions, or relationships to make the image feel more cinematic.
- Use concrete visual mechanisms instead of `masterpiece`, `best quality`, `stunning`, or stacks of synonyms.
- For photography and cinema, lead with the subject and action. For illustration, craft, print, or material-led work, lead with the medium so Midjourney does not drift toward photorealism.
- Use one primary style. Add at most one secondary mechanism when it solves a specific need; do not blend unrelated style labels.
- Describe camera position, scale cue, foreground, depth, and light only when they affect the composition.
- Do not imitate living artists or protected franchises. Translate references into observable mechanisms such as symmetry, palette, lens behavior, brushwork, fabrication, or lighting.
- Do not promise exact typography. When exact text is essential, recommend a text-capable image model or compositing workflow.
- Do not use this skill for multi-shot storyboard continuity unless the user explicitly chooses Midjourney for that task.

## Parameters

Default to V8.2, `stylize 300`, `chaos 0`, and raw off. Switch modes deliberately:

- `faithful`: identity, product, documentary, or strict composition work. Start near `stylize 140`, `chaos 0`, raw on.
- `balanced`: normal visual development. Start near `stylize 300`, `chaos 0`, raw off.
- `exploratory`: genuinely different directions. Start near `stylize 300`, `chaos 25`, raw off.

The selected preset may override these baselines. User-specified parameters always win. Read [references/parameters.md](references/parameters.md) before using style references, image weights, weird, client-specific versions, or advanced parameter changes.

## References

- Browse the compact catalog in [references/style-index.md](references/style-index.md).
- Read exact templates and parameters from [references/style-catalog.json](references/style-catalog.json).
- For complex briefs, references, exact text, or consistency constraints, read [references/prompt-method.md](references/prompt-method.md).
- If an Agent needs to hand the result to a user-configured client or API, read [references/client-integration.md](references/client-integration.md). This file documents data handoff only and does not prescribe a provider.
- Use `scripts/mj_style.py` for deterministic search, lookup, and prompt composition instead of manually copying catalog entries.

## Boundaries

This is a prompt-only skill. It does not contain network requests, endpoints, API keys, authentication, provider routing, billing logic, or generation code. Its normal result is a prompt package for the user or another Agent. Only hand that package to an external image service when the user separately requests generation and has configured that service themselves.
