---
name: figure-it-out
description: Design and execute an auditable workflow when no narrower recipe fits a large migration, multi-part change, or unattended task. Scale rigor to risk, verify each hypothesis, and keep a decision trail. Use for @figure-it-out or figure it out.
license: MIT
metadata:
  opencode/autoinvoke: false
---

# Figure it out

Design the workflow before changing the product. The first deliverable is a sequence of phases with concrete checks and an audit trail. Prefer a narrower Jiro recipe when one already fits. Do not mirror a whole mode to solve one task.

Read `references/shared-rules.md`. Resolve bundled resources from the loaded skill base. Load `jiro` and read its core principles and service boundaries. Track Frame, Design, Run, Log, and Verify in a task list or short checklist, then insert the concrete work units before final verification.

## Frame

Ground the system with `how` before committing to a plan. Reuse findings already established for this task. State these facts before a long run.

- A falsifiable done predicate and the real artifact that will demonstrate it.
- A quantified scope, including rough units, effort, dependencies, and observed blockers.
- A stopping condition and authorization boundaries.
- A rigor level justified by reversibility, blast radius, and one-way doors.

Rigor means gates and evidence, not trying harder. Bias upward for irreversible decisions and broad effects. Use fewer gates for reversible, low-stakes work.

Present framing and tradeoffs before a multi-hour run. Use one checkpoint unless the user has already authorized unattended execution. Do not ask the user to investigate facts you can observe. Unattended work still does not authorize commits, pushes, PRs, deletion, deployment, paid calls, global installation, or unrelated external writes.

## Design

1. Decompose the task into atomic, independently reviewable units. Sequence the riskiest unknown first.
2. Follow Jiro's Repository verification setup and establish the pre-change baseline before feature work. Reuse a relevant verification skill. If none exists and setup is not explicitly opted out or read-only, load `create-verification-skill` and wrap the target project's existing harness. Make the result comparable as old value versus new value. Report a blocked baseline without inventing proof.
3. For an unsettled one-way-door design, load `architect` or `code-organization` to compare shapes. Skip this for mechanical work with a concrete shape. Do not run a second candidate tournament over an already settled design without new evidence.
4. Choose parallel seams only where ownership is clear. Load `delegate` for bounded handoffs and `swarm` for parallel coverage. Give code writers separate worktrees and artifact writers disjoint directories. Serialize when isolation is unavailable. Inherit the current model unless the user authorizes an override and the host confirms its exact ID. No role file is required.
5. Write down the phase list, dependencies, acceptance checks, and recovery plan. This is the playbook the human can audit.

Run project work in the target repository or assigned worktree. Keep records local to the task, not in the installed skill. For a read-only task, preserve that boundary across every phase and child brief. Do not build product changes under the name of investigation.

## Run

Treat each unit as an experiment. State a hypothesis, make the smallest owned change, and measure the real artifact against its predicate. Keep a change only when the evidence supports it. Undo only this task's unsuccessful edits without resetting or discarding unrelated work. Verify a unit before starting a dependent one.

Inspect artifacts rather than trusting self-reported success. When a check passes suspiciously easily, question the observation method. Pair meaningful delegated work with a parent or separate judge check. If a worker games the gate, reject its result and tighten the contract. If the gate is wrong, fix it in its own verifiable change rather than bypassing it. Never overlap a replacement writer with one still running.

Use exactly VERIFIED, NOT VERIFIED, or INCONCLUSIVE for a unit's evidence verdict. Inconclusive is not a pass. Preserve negative results and blockers.

## Log

Load `show-me-your-work` and let it own the decision-trail format and audit. Record forks, completed units and checks, rejected attempts, pivots, and blockers as they happen. The parent alone writes the shared trail. Children return evidence.

Keep the trail uncommitted by default. Commit or publish it only when authorized. Audit only the current run and explicitly supplied history. Do not scan global sessions. Report missing transcript access or cross-model review rather than inventing an audit.

## Verify and report

Test the complete result against the original predicate through the real product, not just a harness proxy. Inspect the scoped diff and reconcile every child. Encode recurring corrections in types, lint, tests, or runtime gates when a structural check fits the task.

Return the designed playbook, rigor level and reason, decision-trail path, completed units, evidence verdicts against the original predicate, checks actually run, and open decisions or blockers. Include the trail's required Attention section and its real review limitations. A written plan is not an executed run.
