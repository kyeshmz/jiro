---
name: architect
description: Sketch caller usage, types, signatures, ownership, and module boundaries before implementation. Compare distinct shapes and revisit a sketch that produces repeated workarounds. Use for @architect, architect this, design this, or a nontrivial architecture decision.
license: MIT
metadata:
  opencode/autoinvoke: false
---

# Architect

Load `code-organization` as the canonical owner of design rules. This compatibility entry point adds candidate synthesis, a design rationale, an optional checkpoint, and the loop from implementation back to the sketch. It does not require an agent named `architect`.

Read `references/shared-rules.md`. Resolve bundled files from this skill's loaded base directory. Work in the target repository. Keep a design-only request read-only apart from explicitly requested design artifacts. A request to sketch does not authorize implementation, commits, or external writes.

Track Ground, Sketch, Agree, Implement, and Reconsider in a task list or short checklist. Skip implementation phases when the request ends at design.

## Ground

1. Load `how` for each affected subsystem. Establish runtime flow, callers, types, state owners, and integration constraints. A file list is not grounding. Reuse evidence already gathered for this task.
2. Load `why` when changing ownership or layering requires the existing rationale. Treat established constraints as design inputs, not guesses.
3. Skip existing-system grounding only for genuinely greenfield work with no surrounding integration.

## Sketch

1. Write README-style caller usage and two or three realistic call sites first. Derive types and signatures from that usage.
2. Compare at least two structurally distinct candidates. Whole shapes count. Small variations of one shape do not. Load `arena` for independent candidate generation and synthesis when useful. A local comparison is acceptable when delegation is unavailable, but it is not independent review.
3. Give each candidate the grounding and `references/runner-prompt.md`. Fill in the task, absolute working directory, owned output paths, constraints, and required evidence. Candidates produce sketches, not production changes, and do not launch their own workers.
4. Screen every candidate with `references/design-red-flags.md` and the canonical organization rules. Compare meaningful complexity hidden behind each public surface, not implementation ease alone. Prefer a change that is correct for the repository when a maintainer sees only one local example.
5. Select one coherent base and adapt worthwhile parts of the others. Record the choice, rejected shapes, grafts, judge availability, and verification in a task-local rationale following `references/rationale-template.md`. Never edit the bundled template to record a run. Inherit the current model unless the user authorizes an override and the host confirms its exact ID. No separate role file is required.

Use one type-and-signature sketch for a small change. Use a module map plus core types for larger work. Mark sketch bodies `not implemented` and use brief pseudocode only where it clarifies a hard decision. Keep scaffolds isolated from runnable code unless the user requested that integration.

## Agree

Proceed within the requested scope by default. Pause after synthesis when the user asks for a checkpoint or an unresolved product preference blocks the design. Present the usage, shape, tradeoffs, and open questions before asking for a decision.

For authorized implementation work, the sketch is the contract. A separate scaffold commit is optional and requires commit authorization. Load `interrogate` if adversarial pressure on the sketch is requested or warranted. Human pushback is new grounding evidence. Re-ground and compare shapes again rather than defending a stale sketch.

## Implement

Replace sketch bodies with code and verify each unit. Surface deviations instead of silently expanding the contract. For a missing parameter or new exception, decide whether the sketch missed a constraint, the requirement changed, or the implementation exceeds scope.

## Reconsider

Revisit the architecture when implementation shows a pattern, not merely one hard edge case.

- The same workaround appears in unrelated code.
- Unrelated edge cases need the same special branch.
- Types need `any`, casts, or optional fields that are always present in practice.
- Shared writers require a lock where the sketch promised isolated state.
- Callers must learn private rules to use the interface.
- At least two independent implementation deviations have the same shape.

Complex data alone does not condemn a design. When the pattern is real, load `how` over the implementation, then `principle-redesign-from-first-principles` and `principle-subtract-before-you-add`. Redesign with the new constraints treated as original requirements. Return to Sketch. Replace only artifacts this task owns. Preserve unrelated work and do not reset a checkout to discard a sketch.

## Report

Return the usage-first sketch, module map when needed, and completed rationale. Name the chosen shape, alternatives, interface depth, synthesis decision, accepted tradeoffs, open questions, and first implementation step. Include checks actually run and any unavailable independent comparison. For implementation work, add deviations and behavior verification.
