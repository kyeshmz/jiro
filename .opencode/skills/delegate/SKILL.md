---
name: delegate
description: Scope work into bounded child-agent tasks, write self-contained briefs, and verify their results. Use for @delegate, delegate this, split work among subagents, or hand a phase to a worker. Use swarm for parallel coverage or races and create-subagent for a reusable agent definition.
license: MIT
metadata:
  opencode/autoinvoke: false
---

# Delegate work

The parent owns the result. Give each child a bounded task, preserve its evidence, and check its work rather than forwarding its summary.

Resolve `references/` from this skill's loaded base directory. Read `references/handoff.md` before dispatching and use `references/run-template.md` for the coordination record. These are instructions for OpenCode child sessions, not a cloud scheduler or permission grant.

## 1. Frame

State the goal and a checkable done predicate. Decide what is worth delegating; do a trivial step directly when writing its brief would cost more than doing it.

Break the task into verifiable units with explicit dependencies. Parallelize independent work only. For a parallel coverage matrix or race, use `swarm`; it uses the same handoff contract.

Jiro's delegated workers are chefs. Use the advertised `chef` agent for scoped Jiro implementation or review work. Use `explore` for discovery without edits and `general` when a routed skill needs it or the chef is unavailable. Select another custom agent only when its ID is advertised and its permissions and dependencies fit. Use `create-subagent` if the user wants a reusable role. Never dispatch an unknown agent ID or assume `general` can spawn grandchildren.

Inherit the parent model by default. Set a child `model` only for a user-authorized choice that the host permits and its current catalog confirms. Omit it for `auto`, `inherit-parent`, a missing policy, or an unavailable choice, and disclose a requested-model fallback. Do not read or change unrelated global model policy.

## 2. Write the handoff

Create a unique run directory at `<target-repository>/.delegation/<task-slug>/run-<n>/`, choosing the next unused integer. Keep `plan.md`, `briefs/`, and `reports/` there. If repository writes are forbidden, use a unique run directory in the host-provided scratch location instead. State which location you chose. Do not overwrite another run or commit these records without authorization.

Claim the run directory with exclusive creation. If another parent already created it, choose the next integer; do not merge a new run into an existing directory.

The parent is the only writer of coordination records. Before launching, save each filled brief as `briefs/<unit-id>-attempt-1.md` and add it to the plan. Read-only children return reports in their final messages; they do not write report files themselves.

Give each writer exclusive owned paths and resources. Concurrent code writers need separate worktrees; concurrent artifact writers may use disjoint output directories. Include generated files, build outputs, Git state, ports, and mutable fixtures in the ownership check. If isolation cannot be established, serialize the writers. Never let children update a shared plan or decision log.

Every brief includes the original goal, accumulated user constraints, working directory, acceptance criteria, exact verification commands, required skills, and output format. File pointers replace large payloads, not the goal or constraints. Include upstream evidence needed by dependent units; children cannot see the parent chat or sibling sessions.

## 3. Dispatch

Use the host's `subagent` tool with `agent`, a short `description`, the filled brief as `prompt`, and `background: true` for independent work. Omit `sessionID` for a fresh child. Do not pass Cursor-only `subagent_type`, `environment`, `cloud_base_branch`, `run_in_background`, or a made-up working-directory argument. Put the absolute working directory in the prompt and tell the child to use it for project commands.

Launch independent units together. Start a dependent unit only when its predecessor's result has been accepted and the necessary artifacts are available in its assigned checkout. Continue useful parent work while children run. Wait for completion notifications, not sleep or polling loops.

## 4. Verify and reconcile

Save each terminal report to `reports/<unit-id>-attempt-<n>.md`. Update the plan with the actual returned session ID, status, evidence paths, and the parent's acceptance decision. Use `unknown` when an ID is not provided; never invent one.

Read every result. Inspect the actual changed files or diff and verification receipts. Rerun the relevant acceptance checks before accepting code changes. A worker's PASS is provisional until this review. Missing evidence, failed checks, and coverage gaps are not passes. Record what was inspected, what was rerun, and what remains unverified.

For a fix round or retry, use a fresh child with consolidated scope, all later constraints, and the previous report and artifact pointers. Keep each attempt's brief and report. Resume with `sessionID` only when costly state truly lives in that child, such as an uncommitted checkout or running process. A status check is not a reason to resume.

Before replacing a writer, confirm the previous writer has stopped. If the host cannot stop or confirm it, do not launch an overlapping writer. Bound retries to one replacement per failed unit by default, then record a gap and the next action. Reject stale results against the current artifact; do not undo user changes to retry.

For long or unattended work, load `show-me-your-work` and let it own the append-only decision trail. The parent logs accepted units, forks, and blockers; children never append to the shared trail.

## 5. Report

Return one consolidated summary with the done predicate, each unit's accepted status, changed artifacts, checks actually run, gaps, and the run-directory path. Account for every child as accepted, failed, blocked, or replaced. Do not claim completion while a child that could still affect the result remains running.

Stay within the user's authorization. Delegation does not authorize commits, pushes, PRs, deploys, global installation, destructive cleanup, or external writes.
