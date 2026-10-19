---
name: principle-outcome-oriented-execution
description: Apply to planned rewrites and migrations with explicit phase boundaries. Converge on a verifiable target architecture instead of preserving every intermediate state with throwaway compatibility code. Use when explicitly invoked as @principle-outcome-oriented-execution.
license: MIT
metadata:
  opencode/autoinvoke: false
---

# Outcome-oriented execution

Read `references/shared-rules.md` before applying this tool. Resolve bundled paths from this skill's base directory. Run project checks in the target repository or assigned worktree.

Optimize for the intended, verifiable end state. Temporary compatibility code can become permanent debt when every intermediate edit must preserve the old shape.

Use this only for an authorized rewrite or migration with explicit phases.

1. Define the target architecture and completion criteria before changing it.
2. Declare where temporary breakage is acceptable. Bound it to planned, scoped, reversible work. Do not extend that allowance to production or shared consumers.
3. Keep high-signal checks running for the areas being changed. Use explicit phase gates rather than treating every edit as a release.
4. At each declared boundary, verify its promised state before building on it. Load `principle-sequence-verifiable-units` to size those units.
5. Run full static and runtime verification at completion. Remove transitional scaffolding that no longer serves the target.

Do not call planned breakage an excuse for an unknown state. Name expected failures and their phase, distinguish new failures, and stop when the actual result violates the plan.

Keep the requested scope and permission gates. Read-only work ends with the migration plan. Commits, pushes, PRs, deploys, global installs, and destructive actions need authorization. Preserve unrelated changes.
