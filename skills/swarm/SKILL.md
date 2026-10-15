---
name: swarm
description: Fan out parallel workers across separate slices or competing attempts, verify their evidence, and return one report. Use for @swarm, swarm this, parallel coverage, a race, a gauntlet, or exploration partitions.
license: MIT
metadata:
  opencode/autoinvoke: false
---

# Swarm

Fan out N OpenCode child sessions. Partition the work, race the same brief, or mix both. The parent accounts for every worker and returns one verified aggregate.

Resolve references from this skill's loaded base directory. Read `../delegate/references/handoff.md` for briefs and reports and `../delegate/references/run-template.md` for the parent-owned record. `delegate` is bundled with this skill; these references do not depend on a global pstack installation.

Track four phases, using a todo tool when available or the run plan otherwise.

1. Frame
2. Fan out
3. Aggregate
4. Report

## Phase A: Frame

1. State the done predicate and the artifact or report the swarm returns.
2. Choose partition, race, or mixed. For a race, declare `first pass`, `rank all`, or `best-of` and its concrete criteria before spawning. `first pass` means the first result the parent validates, not the first worker that says PASS.
3. Set N from the user or the required independent slices. State a concurrency cap appropriate to available resources. Do not create a large panel for a trivial task.
4. Inherit the parent model unless the user requests model choices and the host permits them. Confirm exact IDs and variants through the host catalog before setting `model`. Omit it for `auto`, `inherit-parent`, absent policy, or unavailable choices. Disclose requested-model fallbacks. For an authorized model race, name the arms up front; same-model replicas are not cross-model review.
5. Give writers separate worktrees or disjoint artifact output directories, with owned paths, generated files, Git state, mutable fixtures, and ports accounted for. If code-writer isolation is unavailable, serialize writes rather than racing in one checkout. Readers must also avoid shared mutable verification resources.
6. Claim `<target-repository>/.delegation/<task-slug>/run-<n>/` with exclusive creation using the next unused integer, or use a unique host-scratch run directory when repository writes are forbidden. If another parent claimed the directory, choose the next integer rather than reusing it. Save the plan and each filled `briefs/<unit-id>-attempt-1.md` before dispatch. The parent alone writes coordination records.
7. For commit verification, put the exact SHAs in each brief. For measurement, include sample count, sample definition, order, and method. Record both in the result. Include the absolute working directory and any requested branch; do not switch the parent's checkout to satisfy a worker.

When the caller is following a pstack workflow, honor its existing host-authorized swarm-worker role settings. Read only the role configuration that the host instructions require and apply the same confirmation and fallback rules as step 4. Do not change user model settings as part of a swarm run.

## Phase B: Fan out

Jiro's swarm workers are chefs. Use the host's `subagent` tool with the advertised `chef` agent for Jiro implementation or review slices, `background: true`, a short `description`, and the filled brief as `prompt`. Use `general` when the chef is unavailable, `explore` for discovery-only slices, or another advertised agent whose role and permissions fit. Omit `model` unless Phase A authorized it. Do not pass Cursor-only cloud or Task arguments.

Launch all independent workers together up to the cap. Refill from queued independent slices when completion notifications arrive. Continue useful parent work; do not sleep or poll. Dependencies wait for accepted results and receive their predecessor's report and artifact pointers.

Every brief stands alone. Include the goal, slice or race arm, working directory, owned paths/resources, constraints, required skills, acceptance criteria, literal verification commands, and the shared PASS / ISSUES / BLOCKED report format. Children cannot see sibling sessions or the parent chat. Do not let them spawn an unplanned second swarm.

Fresh children are the default, including fix rounds and retries. Resume only for costly child-local state, never to check status. Confirm a prior writer has stopped before replacing it; never overlap writers if the host cannot confirm or stop the prior attempt.

## Phase C: Aggregate

Save each final message to `reports/<unit-id>-attempt-<n>.md` and record its actual session ID, reported status, evidence, and parent decision in the plan. Inspect the actual artifacts, diffs, and receipts. Rerun relevant acceptance checks before accepting code changes; self-reported PASS alone is insufficient.

Reject a report missing required SHAs or measurement method. Dispatch one fresh replacement with consolidated constraints and the prior report after confirming the first attempt has stopped. After a second miss, record a gap. A new artifact state invalidates stale receipts. Do not claim commit verification when an unrecorded dirty diff was tested.

For coverage, every required slice needs an accepted result. For a race, apply the declared selection rule to validated results. If best-of combines candidates, verify the combined artifact too. A missing slice, dropout, blocked verifier, or rejected result is not a pass. Record every proven issue, including lone-worker findings; deduplicate without dropping evidence.

Drain every launched child to a terminal state before the final report, even after a first-pass winner. A selected winner does not authorize leaving other writers running. If a child cannot be reconciled, state that the run is incomplete rather than claiming success.

For long or unattended runs, load `show-me-your-work`. The parent alone appends the decisions; workers return evidence instead of writing a shared log.

## Phase D: Report

Return one consolidated report with the done predicate, a compact unit/status/evidence table, issue one-liners, gaps and dropouts, the race rule when used, parent checks actually run, and the run-directory path. Do not paste raw worker dumps.

Do not commit, push, open PRs, deploy, install globally, make destructive cleanup, or perform external writes unless the user authorized them. These local child sessions do not implement Cursor cloud workers, `/loop`, nested coordinators, or pstack's merge automation.
