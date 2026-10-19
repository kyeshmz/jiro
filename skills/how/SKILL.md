---
name: how
description: Use for how does X work, code walkthroughs before changing something, and placement, ownership, or layering questions such as where should this live or which package owns this. Explains subsystem architecture, runtime flow, and onboarding mental models. Use why for motivation.
license: MIT
metadata:
  opencode/autoinvoke: false
---

# How

Explore the codebase to answer how something works. Produce architectural explanations at the level of a senior engineer onboarding onto a subsystem. Give enough detail to build a working mental model without turning the answer into annotated source code.

## OpenCode execution

Use OpenCode's `subagent` tool. Use `explore` for local code discovery and `general` for explanation. Every child prompt forbids file edits, commits, and external writes. Select a permission-restricted read-only agent when one is available. Do not pass unsupported `readonly` or `subagent_type` arguments.

Read the exact authorized Jiro role-file path supplied by the caller, if any. Do not search for or migrate unrelated global role files. Explorers use the `how explorer` role and explainers use `how explainer`, subject to the host's model-selection rules. Resolve authorized choices through the host's available-models tool before setting `model`. Omit `model` when no override is authorized, no role file is supplied, the role is absent, or its value is `auto` or `inherit-parent`. Never guess a model ID or silently substitute another model.

Resolve templates relative to this skill's base directory. Fill their placeholders and pass their contents to each child. Child sessions start with fresh context. Include the original question, working directory, scope, and relevant code paths in every prompt.

## 1. Assess complexity

If the scope is ambiguous, state your interpretation and explore. The user can redirect.

- **Simple.** A single module, a small utility, or a narrow question such as how function X works needs no explorers. Spawn one explainer that explores and explains in one pass. Build its prompt from `references/explainer-prompt.md` without the explorer-findings section or prose that assumes explorers ran. Go to step 4.
- **Complex.** A subsystem spanning multiple files or services, a cross-cutting feature, or a full architectural overview goes to step 2.

When in doubt, take the simple path.

## 2. Explore (complex only)

Decompose the question into 2 to 4 angles, each a distinct slice of the subsystem. Spawn all explorers concurrently, each with `references/explorer-prompt.md` and its angle filled in. Use background execution for independent work and wait for completion notifications. Do not poll.

## 3. Synthesize (complex only)

Once all explorers have returned, spawn one explainer with `references/explainer-prompt.md` and every explorer's findings filled in.

## 4. Present

Present the explainer's output. Light edits for clarity or context from the conversation are fine. Do not substantially rewrite it.

## Output format

The explanation uses the sections defined in `references/explainer-prompt.md`. Drop any that do not apply. The sections are Overview, Key Concepts, How It Works, Where Things Live, and Gotchas.
