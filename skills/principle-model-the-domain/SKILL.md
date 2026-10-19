---
name: principle-model-the-domain
description: Apply before writing stateful logic or when conditionals and repeated shape assumptions spread across files. Encode domain states, invariants, ownership, and access patterns in the data structure. Use when explicitly invoked as @principle-model-the-domain.
license: MIT
metadata:
  opencode/autoinvoke: false
---

# Model the domain

Read `references/shared-rules.md` before applying this tool. Resolve bundled paths from this skill's base directory.

Put the domain in the data structure instead of distributing it across conditionals. A matching structure removes invalid states and branches. Choose it while writing the feature rather than leaving recovery to a future refactor.

- Use a state machine instead of scattered booleans, phases, or lifecycle checks.
- Use a typed model instead of loose parameters and repeated shape assumptions.
- Use a map, registry, lookup table, or discriminated union instead of branching across files.
- Use a reducer or command/event model instead of unrelated state mutations.
- Organize a module around one body of domain knowledge. Execution stages such as load, validate, transform, and save do not establish ownership.
- Gather repeated behavior, ownership, or invariants behind a small module boundary.
- Choose a queue, cache, index, graph, tree, or normalized collection when the access pattern warrants it.

If none fits, write down what the code must never allow and how callers read the data. Find the smallest structure that encodes those requirements. Load `code-organization` when settling module ownership or public interfaces.

Keep boring local code when its shape is already clear and unlikely to grow. Reject an abstraction that adds indirection without removing branches, duplicated rules, invalid states, or lifecycle risk.

Reconsider the model when a feature adds another branch to a growing chain or a second boolean that must track the first. Phase-named modules that repeat domain rules are another warning.

Keep the requested scope and permission gates. Read-only work stays read-only. Commits, pushes, PRs, deploys, global installs, and destructive actions need authorization.
