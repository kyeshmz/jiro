# Jiro recipe book

Read the recipe selected by Jiro. Copy its numbered steps into the task list before adding task-specific items. These are Jiro-native workflows, not the full pstack playbook collection. Jiro owns the workflow and verifies the work of delegated chefs. Prep establishes the scope, cooking makes the change, and tasting proves the result before serving it.

## Investigation

1. State the question, scope, and evidence needed. Keep the task read-only.
2. Load `how` for architecture or runtime flow. Load `why` for historical rationale. For a supplied trace, inspect the artifact and correlate it with the code path before proposing a cause.
3. Check the relevant claims against source, history, or runtime evidence without making product changes or external writes.
4. Present the answer with evidence, confidence, and coverage gaps. Distinguish observations from inferred causes.

## Bug fix

1. Reproduce the reported defect through the surface the user encounters. Capture the failing result before editing.
2. Load `how` and trace the failure to its root cause. Name the affected data shape and boundary.
3. Add a failing behavioral test when a reliable harness exists. Make the smallest root-cause fix.
4. Repeat the original reproduction, run the regression checks, and inspect the diff for unrelated changes.
5. Report the cause, changed behavior, proof before and after, and any unverified paths.

If reproduction is blocked by unavailable credentials, hardware, or data, name that blocker. Do not claim an unobserved fix works. Continue only with work justified by the available evidence and requested scope.

## Performance

1. Define the user-visible metric, workload, environment, and comparison method. Capture a repeatable baseline.
2. Load `how` and profile the limiting path. Separate a measured bottleneck from a hypothesis.
3. Change one hypothesis at a time. Keep the workload and measurement method comparable.
4. Repeat measurements, check correctness, and keep only demonstrated improvements. For sustained optimization, load `show-me-your-work` and record each iteration against the target and stopping condition.
5. Report before and after results, repeat variability, the limiting factor, and remaining uncertainty.

## Feature

1. Define the consumer's observable behavior and the checks that will prove it.
2. Load `how`. Name the data shape, ownership, caller usage, and boundaries before implementation.
3. Choose the smallest coherent change. For multiple units, name their dependencies and verification checkpoints.
4. Implement and verify each unit through the project's public surface. Use an existing harness or load `create-verification-skill` when one is needed and in scope.
5. Inspect the diff and report the consumer impact, maintainer-facing decisions, checks, and open tradeoffs.

## Refactoring

1. State what structure changes and what behavior must stay identical. Capture baseline checks.
2. Load `how` and identify callers, ownership, and the target shape.
3. Migrate callers in verifiable units. Remove replaced internal paths once no callers remain. Avoid throwaway compatibility layers unless external consumers require them.
4. Repeat the baseline checks and inspect the diff for behavior changes.
5. Report the simpler structure, evidence of preserved behavior, and any compatibility constraint.

## Prototype

1. State the observable fork and the cheapest experiment that could settle it.
2. Build isolated sketches within the authorized scope. Keep their state and writers separate.
3. Run the same user path against each sketch and capture comparable results.
4. Compare the evidence, choose a direction, and distinguish disposable sketches from production changes.
5. Report the choice, tradeoffs, and what still needs production verification.

## Visual parity

1. Capture the reference and current UI at matching viewport, state, content, and scale.
2. Identify measurable differences before editing. Load `how` for ownership of the affected rendering path.
3. Change one bounded visual unit at a time and repeat the same capture.
4. Compare images and verify interactions on the changed surface. Do not treat a screenshot as proof of behavior.
5. Report the comparison artifacts, remaining differences, and interaction checks.

## Authoring a skill

1. Load `skill-creator` if available. Establish the trigger, expected outcome, dependencies, and output scope.
2. Write or update the target skill with bundled resources resolved from its base directory. Keep it out of the installed Jiro pack unless the task is explicitly maintaining that pack.
3. Validate the frontmatter, exact IDs, referenced files, and companion dependencies. Preserve source attribution and licenses for imports.
4. Exercise representative scenarios when behavior is structural. Distinguish static validation from an observed agent run.
5. Report the entry point, routing decisions, validation results, and untested behavior.

## Evaluation

1. Define the behavior being compared, baseline, success criteria, and permitted runtime or provider costs.
2. Load `skill-creator` if available. Build isolated scenarios and keep scoring criteria and variant identities out of candidate prompts.
3. Run identical organic task prompts against the variants using only authorized models and tools. If these are unavailable, report the blocked comparison rather than inventing results.
4. Inspect actual artifacts and scoped tool histories. Compare observed behavior, not the candidates' claims about their process.
5. Report scenario results, coverage, variance, and whether the evidence supports promoting the change.

## Delegation

1. Establish whether the request is a bounded handoff, parallel coverage or a race, or a reusable agent definition.
2. Load `delegate`, `swarm`, or `create-subagent` respectively when available. If the selected skill is absent, report the gap and use the entry skill's supported built-in agents only for bounded one-off work.
3. Follow the selected skill's scope, ownership, isolation, model-authorization, and reporting contract. Require Jiro implementation children to load `jiro` before starting.
4. Inspect the returned artifacts and evidence. Reconcile every child before claiming completion.
5. Report the accepted results, checks actually run, and any unavailable capability. A written agent definition is not proof of a successful launch.

## Review and PR work

1. Determine whether the request is read-only status, review, fixing findings, opening a PR, or merging. Do not infer write authorization from a status question.
2. Inspect the current diff, CI state, and relevant review threads through available source-control tools.
3. Assess each finding against the code and observed behavior. Fix only authorized, substantiated issues. Dismiss noise with a concrete reason.
4. Verify changed paths and report unresolved findings, failing checks, or unavailable evidence. Green CI alone does not establish correctness.
5. Open or merge only when requested, following the repository's gates. Load the host's `writing-pull-requests` skill before creating or editing PR prose when available.

## Session handoff

1. Establish whether the user wants pickup, pause, or a handoff. Inspect the current branch, worktree, diff, and running processes.
2. Read only user-supplied history or known, explicitly scoped OpenCode sessions. Never scan unrelated global session storage.
3. Reconcile previous claims with the current artifacts and rerun the relevant checks before relying on them.
4. For pickup, choose the next playbook and continue. For pause, stop only processes you started and only when their state can be safely preserved.
5. Record the current objective, completed evidence, remaining steps, exact paths, and processes left running. Do not invent session IDs or imply local work survives a closed laptop.

## Bespoke run

1. Define the requested result, scope, stopping condition, authorization gates, and verification evidence.
2. Load `how` for the system map and `show-me-your-work` for a long, unattended, or multi-phase run.
3. Divide the work into dependency-ordered phases with one owner per writable artifact and a check at each boundary. Use a narrower playbook inside each phase.
4. Delegate independent slices when useful. Keep the original brief and later directives in every child prompt. Review each artifact before advancing.
5. Continue within the authorized scope until the stopping condition is met or a concrete blocker prevents progress. Preserve state for handoff if the session must end.
6. Report completed units, evidence, decisions, remaining work, and gates still needing approval. An autonomous request does not authorize deletion, deployment, or merging by itself.
