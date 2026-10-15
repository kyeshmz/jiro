---
name: principle-laziness-protocol
description: Apply when refactoring, evaluating diff size, or tempted to add abstractions, layers, or signal threading. Bias toward deletion and the smallest change that solves the problem. Use when explicitly invoked as @principle-laziness-protocol or loaded by Jiro.
license: MIT
metadata:
  opencode/autoinvoke: false
---

# Laziness Protocol

Aim for the most result with the least code and complexity.

- **Prefer deletion.** When asked to refactor or improve, look for removals before additions.
- **Maintain a flat call hierarchy.** Avoid deep call chains. A rich interface that hides substantial work is not a deep call chain. If answering a question requires tracing through more than 3 files or layers, flatten it.
- **Consolidate decisions.** Do not repeat the same choice in several places. Put it behind one source of truth and pass the result as a simple flag.
- **Minimize the diff.** Make the smallest change that solves the problem. Fewer lines beat "elegant" boilerplate.
- **Question the threading.** If a task asks you to pass a new signal through types, schemas, pipelines, or similar layers, stop and look for a more direct path.
- **Sweat the small leaks.** Remove tiny pass-throughs, representation leaks, and duplicated choices before they spread. Small leaks compound into permanent coordination costs.

**The test:** If a human developer would find the code exhausting to maintain, it is a bad solution.

Apply within the authorized task. Preserve work you did not make. A read-only question does not authorize flattening or deleting code; report the simpler design instead. This principle does not authorize wider scope or external writes.

Verify the simpler shape against the actual requirement. Fewer lines are not a win if they drop required behavior or necessary boundary validation. Confirm that apparently dead code is unused before deleting it. Use [Minimize reader load](../minimize-reader-load/SKILL.md) to check both indirection and hidden state.

## OpenCode scope

Resolve linked skills from this skill's base directory. Work in the user's target repository or assigned worktree, not the installed stack. An investigation-only request permits recommendations, not edits. This principle does not authorize discarding unrelated files, user state, or test evidence.
