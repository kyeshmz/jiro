---
name: principle-migrate-callers-then-delete-legacy-apis
description: Apply when replacing an internal API with coordinated caller changes and no external compatibility obligation. Migrate every caller and delete the old API in the same wave instead of retaining a compatibility layer. Use when explicitly invoked as @principle-migrate-callers-then-delete-legacy-apis.
license: MIT
metadata:
  opencode/autoinvoke: false
---

# Migrate callers, then delete legacy APIs

Read `references/shared-rules.md` before applying this tool. Resolve bundled paths from this skill's base directory. Run project checks in the target repository or assigned worktree.

Use one coordinated migration when all three conditions hold.

- No external users depend on backward compatibility.
- The project can absorb coordinated breaking changes.
- The replacement belongs to an authorized simplification or refactor.

Find all callers before choosing this recipe. If callers or compatibility obligations are unknown, establish them first. Do not assume an exported API is private.

1. Define the replacement contract and migrate its callers.
2. Update tests to assert that contract through the callers' interface.
3. Delete the old API and compatibility adapters in the same wave. Delete tests that protect only the superseded implementation, but retain behavioral coverage.
4. Search for remaining references and run the affected static and runtime checks. Verify the replacement before declaring the migration complete.

Do not preserve a fallback only to make the transition look smooth. If external compatibility is real, use a compatibility-aware migration instead of applying this rule.

Keep the requested scope and permission gates. Read-only work ends with the caller inventory and migration proposal. Commits, pushes, PRs, deploys, global installs, and destructive actions need authorization. Do not delete unfamiliar user work.
