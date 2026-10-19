---
name: principle-make-operations-idempotent
description: Apply when designing commands, lifecycle operations, or processing loops that face crashes, restarts, and retries. Reconcile actual state with the goal so repeated and partial runs converge to the same result. Use when explicitly invoked as @principle-make-operations-idempotent.
license: MIT
metadata:
  opencode/autoinvoke: false
---

# Make operations idempotent

Read `references/shared-rules.md` before applying this tool. Resolve bundled paths from this skill's base directory. Run project checks in the target repository or assigned worktree.

Derive each state-changing step from what exists, not what a previous run intended. Read current state, compare it with the goal, and apply only the difference. A repeated run should find no work left once the goal is satisfied.

Make every leftover recognizable after a crash. Include locks, temporary files, half-written records, and claimed jobs. Judge staleness using evidence that remains valid wherever the previous run stopped, not an assumption about its usual stopping point.

Write to a temporary path and rename the completed artifact into place when that fits the storage contract. Compare artifact content rather than creation order when content defines the goal. Do not treat an unfamiliar marker or another actor's live lock as stale without evidence.

## Acceptance checks

1. Run the operation twice in a row. Check the same end state and the absence of duplicate effects.
2. Consider every mutation boundary where the previous run could crash. Exercise the relevant interruption and restart cases.
3. Check that each re-execution converges to the intended state without manual cleanup.

If the result depends on an unreconciled leftover, add a reconciliation step. Keep fault injection isolated from live user state. Repeatability does not make an unauthorized mutation safe.

Keep the requested scope and permission gates. Read-only work ends with the reconciliation design and test plan. Commits, pushes, PRs, deploys, global installs, and destructive actions need authorization.
