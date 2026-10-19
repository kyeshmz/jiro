---
name: principle-sequence-verifiable-units
description: Apply to multi-step sweeps, migrations, repeated edits, and authorized commit or PR stacks. End each bounded unit at a verification gate before proceeding and order delivery so a reviewer can follow the proof. Use when explicitly invoked as @principle-sequence-verifiable-units.
license: MIT
metadata:
  opencode/autoinvoke: false
---

# Sequence verifiable units

Read `references/shared-rules.md` before applying this tool. Resolve bundled paths from this skill's base directory. Run project checks in the target repository or assigned worktree.

Break work into small units that each end in a checkable state. Verify the current unit before starting the next. A failure caught at its cause is cheaper to localize than one found after a batch.

## Execution

1. Establish a known baseline and record relevant existing failures. Use the intended target branch as the comparison point.
2. Make one coherent change, run its check, and inspect the result.
3. Proceed only when the unit meets its promised gate. If a migration permits planned temporary breakage, declare the expected failures and use the explicit phase boundary instead.
4. Run the per-unit check even when a codemod or generator makes the edits. Cheap repetition is a reason to check more reliably, not to skip it.

Start from clean current trunk when that is the authorized workflow. Do not automatically rebase, discard local work, or rewrite history to obtain it. Preserve unrelated changes and report a stale or dirty baseline when it cannot safely be changed.

## Delivery

When commits or PRs are authorized, order them so a reviewer can replay the argument. Put a failing regression test before its fix. Other useful orders include subtraction before reshaping, baseline capture before treatment, and scaffolding before a feature.

Give each unit an explicit expected state. A test-only regression unit can prove the failure before the next unit turns it green. Do not present that expected failure as an unexplained passing build or land a broken shared state outside the agreed delivery plan.

Use `principle-prove-it-works` to keep the checks direct and `principle-build-the-lever` to make them cheap to repeat.

Keep read-only work read-only. Sequencing does not authorize commits, pushes, PRs, deploys, global installs, rebases, or destructive actions.
