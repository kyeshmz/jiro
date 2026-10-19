---
name: arena
description: Generate independent candidates for one task, score them against a private rubric, select a base, and synthesize the strongest coherent result. Use for @arena, arena this, throw it in the arena, or competing attempts at a nontrivial artifact.
license: MIT
metadata:
  opencode/autoinvoke: false
---

# Arena

Produce one verified artifact from competing attempts. Keep Frame, Fan out, Cross-judge, Pick, Graft, and Verify in a task list or checklist.

Read `references/shared-rules.md`. Resolve resources from the loaded skill base. Run project commands in the target repository or assigned worktree. Load `swarm` for isolation, handoff records, and reconciliation. This skill adds candidate comparison and synthesis, not a scheduler or another entry mode.

## Frame

1. State the artifact, requested scope, and observable done predicate. Use the same task and grounding for every candidate.
2. Define three to six concrete, gradeable success criteria before dispatch. Keep the selection rubric out of candidate prompts. The rubric is for the parent and judge, not a target candidates can game.
3. Use two candidates by default. Add seats only for distinct directions or justified generation coverage. Inherit the current model by omitting `model`. Use different models only when the user authorizes them and the host confirms exact IDs. No role file, family fallback, or guessed model is required. Same-model replicas are not cross-model review.
4. Give each writer a separate worktree or disjoint artifact directory. Include generated output, Git state, ports, and mutable fixtures in the ownership check. Serialize code writes if isolation is unavailable. A read-only request permits no repository edits or external writes. Candidates return text when artifact writes are not authorized.

## Fan out

Use the host's native `subagent` tool with an advertised `chef` or suitable `general` agent, a short `description`, a self-contained `prompt`, and `background: true` for independent work. Do not pass Cursor-only arguments. Launch candidates together up to the resource cap and wait for completion notifications without polling.

Every brief includes the original task, accumulated constraints, absolute working directory, grounding pointers, owned paths, allowed writes, artifact contract, verification commands, and a short rationale naming alternatives rejected. Forbid nested fanout and shared coordination writes. Omit `model` unless Frame authorized it.

Account for every launched child before finishing. If a candidate returns no usable output, record the dropout and compare the remaining candidates. If the caller requires two shapes and fewer survive, obtain another bounded attempt or report the comparison incomplete. When delegation is unavailable, compare local drafts only if useful and label the loss of independence.

## Cross-judge

After all candidate writers stop, give one fresh read-only judge the rubric and path-labeled candidates. Explicitly forbid edits, commits, and external writes. Ask for criterion-level scores, a recommended base, and reasons. Use a different model family only when authorized and available. Report a same-model or unavailable judge honestly.

Run judging alongside the parent's own reading. Do not expose candidate self-rankings as evidence or ask the judge to inspect unfinished output.

## Pick

Read every candidate end to end. Score each criterion, then compare the judge's reasoning. A disagreement requires examining both rationales and the rubric, not averaging scores blindly. Pick the base a maintainer can extend without breaking invariants. Break a close tie in favor of clearer ownership or the smaller useful API.

## Graft

Revisit every losing candidate for worthwhile parts. Usually one or two ideas deserve adapting. Integrate them under the base's mental model rather than pasting incompatible pieces together. Use `principle-redesign-from-first-principles` when the combination changes the shape.

If candidates converge, record consensus and skip unnecessary grafting. If they diverge because the task was underspecified, reframe before rerunning. Do not average incompatible interpretations into an artifact nobody designed.

## Verify

Verify the synthesized artifact itself against the done predicate through the project's existing harness or public surface. Candidate checks do not prove a combined result. If a missed failure came from the task contract, reframe. If a candidate already caught it, revisit the graft. Do not hide the failure with an unrelated patch.

Do not delete worktrees, commit, push, open a PR, install globally, or make external writes without authorization. Preserve discarded candidates until any requested cleanup has an approved exact scope.

## Report

Return the synthesized artifact and a short synthesis note. Include the rubric, chosen base and why, judge verdict and limitations, each graft with its source, rejected ideas and reasons, convergence or divergence, dropouts, parent verification, and remaining gaps.
