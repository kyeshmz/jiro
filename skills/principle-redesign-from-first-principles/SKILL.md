---
name: principle-redesign-from-first-principles
description: Apply when integrating a new requirement into an existing design. Shape the system as if that requirement had been there from day one instead of bolting it on.
license: MIT
metadata:
  opencode/autoinvoke: false
---

# Redesign from first principles

When integrating a new requirement, do not merely bolt it onto the existing design. Ask what the design would be if that requirement had been a foundational assumption from the start.

- Read the affected files and understand the current data model, callers, and contracts before proposing a replacement.
- Sketch the whole target shape with the new requirement included. Prefer a coherent model over optional flags and exceptions spread across the old one.
- Propagate the chosen change through affected types, callers, schemas, documentation, examples, and rationale. Update references rather than leaving parallel explanations behind.
- Think about the whole redesign, then deliver it in small verifiable increments. Name the behavior that must remain and verify each step against it.

This is about incorporating a new requirement. [Attack the premise](../principle-attack-the-premise/SKILL.md) instead questions an assumption shared by failed fixes. Do not confuse a new capability with a behavior-preserving refactor.

## OpenCode scope

Resolve linked resources from this skill's base directory. Work in the target repository or assigned worktree. A redesign principle does not authorize an unrelated rewrite, migration, deployment, or commit. If the task is read-only, report the target shape, tradeoffs, and incremental verification plan without implementing it.
