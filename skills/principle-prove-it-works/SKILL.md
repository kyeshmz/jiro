---
name: principle-prove-it-works
description: Apply before declaring a task complete. Check the real artifact through its public surface and compare concrete observed results with the requirement rather than trusting compilation, proxies, or worker summaries. Use when explicitly invoked as @principle-prove-it-works.
license: MIT
metadata:
  opencode/autoinvoke: false
---

# Prove it works

Read `references/shared-rules.md` before applying this tool. Resolve bundled paths from this skill's base directory. Run project checks in the target repository or assigned worktree.

Check the actual output directly. Compilation, file timestamps, cached screenshots, derived state, and a chef's self-report do not prove the behavior the consumer needs.

- Run the feature through its real interface and compare concrete observed results with the requirement.
- Check process liveness directly rather than inferring it from a file or status derived elsewhere.
- Read the authoritative value rather than a cache or a representation that may be stale.
- Inspect the actual scoped diff and resulting artifacts before accepting delegated work.
- When verification fails, inspect the observation method before concluding the system is broken. Do not discard a valid failure merely because the check is inconvenient.

Build a deterministic rerunnable check when it makes the comparison reliable. Run it and retain its output as a visible artifact. Load `principle-build-the-lever` for the smallest useful harness. A script that only reports its own success is still a proxy.

For large or complex work, load `show-me-your-work` when an auditable trail is requested or required by the active recipe. Keep the trail local unless committing it is authorized. A proof artifact is not automatic permission to commit it.

Report checks actually run, observed results, and unavailable or unverified behavior. State what remains unknown instead of declaring completion from indirect evidence.

Keep the requested scope and permission gates. Read-only work stays read-only. Commits, pushes, PRs, deploys, global installs, and destructive actions need authorization.
