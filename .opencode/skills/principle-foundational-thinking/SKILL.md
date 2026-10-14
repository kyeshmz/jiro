---
name: principle-foundational-thinking
description: Apply before writing logic to choose core types, data structures, access patterns, and shared-state ownership. Build the foundations that make later work clear.
license: MIT
metadata:
  opencode/autoinvoke: false
---

# Foundational thinking

Structural decisions preserve future choices. Code-level decisions keep the current solution simple.

- Get the data shape right before writing logic. Define core types early, trace the dominant access patterns, and choose structures that fit them.
- Consolidate types and domain models, not every similar line. A few explicit statements can be clearer than a premature abstraction. Check behavior and edge cases rather than optimizing line counts.
- Before sharing state between actors, ask what happens if another actor modifies it concurrently. If the answer is not nothing, isolate the state or establish one owner before adding coordination.
- Build scaffolding first when every later phase benefits from it. Appropriate foundations include shared types, verification, lint, and CI. Put tests before fixes. Do not add infrastructure unrelated to the task.
- Make each increment a coherent abstraction or a useful deepening of an existing one. Do not distribute a new capability across callers as special-case coordination.

[Subtract before you add](../principle-subtract-before-you-add/SKILL.md) comes before scaffolding. Remove confirmed dead weight first, then build on the simpler base. Use [Code organization](../code-organization/SKILL.md) when the data shape changes ownership or module boundaries.

## OpenCode scope

Resolve linked skills from this skill's base directory. Put generated types and checks in the target repository or assigned worktree. A read-only design task ends with the proposed shape and verification plan. It does not authorize implementation, commits, or changes to user model configuration.
