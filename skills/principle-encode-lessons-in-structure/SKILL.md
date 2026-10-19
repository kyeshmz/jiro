---
name: principle-encode-lessons-in-structure
description: Apply when the same instruction is written twice or a correction keeps recurring. Encode the rule as a type, lint, metadata flag, runtime check, or script instead of adding more prose. Use when explicitly invoked as @principle-encode-lessons-in-structure.
license: MIT
metadata:
  opencode/autoinvoke: false
---

# Encode lessons in structure

Read `references/shared-rules.md` before applying this tool. Resolve bundled paths from this skill's base directory.

Turn a repeated correction into an enforceable constraint. Another instruction leaves the same failure possible and asks the next reader to remember more.

1. Name the recurring failure and the invariant it violates.
2. Put enforcement where the invariant is owned. Prefer a type, lint, metadata flag, runtime check, or rerunnable script over another reminder.
3. Check that the enforcement rejects the known failure and accepts the intended behavior.
4. When the structural fix is sufficient, use that fix alone. Do not retain a duplicate instruction as a second maintenance surface.

If the lesson needs judgment that a check cannot encode, make one instruction prominent and include a concrete example of the failure. Explain why enforcement would be misleading rather than adding a brittle approximation.

Load `correct` when the task asks to prevent a recurring agent mistake. Let it own history evidence, structural enforcement, and negative proof.

Keep the requested scope and permission gates. Read-only work ends with the proposed enforcement. Commits, pushes, PRs, deploys, global installs, and destructive actions need authorization.
