---
name: principle-exhaust-the-design-space
description: Apply to a novel UI interaction, product choice, or architectural decision with no useful precedent in the codebase. Compare two or three competing prototypes before choosing a direction, especially when experience depends on feel. Use when explicitly invoked as @principle-exhaust-the-design-space.
license: MIT
metadata:
  opencode/autoinvoke: false
---

# Exhaust the design space

Read `references/shared-rules.md` before applying this tool. Resolve bundled paths from this skill's base directory.

Build two or three meaningfully different prototypes before settling a novel design. Compare them side by side. A variation in styling is not an alternative architecture or interaction.

- State the decision, constraints, and observable acceptance criteria first.
- Find existing project precedent before treating the problem as novel.
- Use small disposable sketches to expose the tradeoff. Throwaway HTML can settle an interaction more cheaply than production code.
- Compare the same core scenario across every prototype. Include feel, feedback, error states, and maintainer cost when relevant.
- Record what each alternative demonstrates, what remains untested, and why the selected direction fits the criteria.

Load `code-organization` for ownership, module, or public-interface decisions. Use Jiro's Prototype recipe when the task calls for an empirical design comparison. Stop building once the prototypes answer the decision.

Keep read-only work read-only. If prototypes are outside the authorized scope, report the alternatives and proposed experiment instead. A preferred prototype is not permission to commit, push, open a PR, deploy, install globally, or delete work.
