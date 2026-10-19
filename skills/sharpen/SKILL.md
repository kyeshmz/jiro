---
name: sharpen
description: Sharpen a task before executing it by checking the expert method, the user's real goal, and the useful level of specification. Keep one outside correctness check. Use for @sharpen or /sharpen.
license: MIT
metadata:
  opencode/autoinvoke: false
---

# Sharpen

Read `references/shared-rules.md`. Resolve resources from the loaded skill base. Apply this framing to the active task, not as permission to expand it.

Before starting, ask yourself how a strong expert would approach the work. Identify the raw sources they would read, the methods they would use, and an outside check that can falsify a wrong result. Use evidence independent of the answer's own persuasive wording.

Establish what the user actually wants. Check whether the task is over-specified or under-specified. Loosen a constraint that does not serve the goal as readily as adding a missing one. Do not override an explicit requirement or decide a genuine user preference silently. Ask only when that choice or missing authorization blocks useful progress.

Fold in only what makes the work better, not bigger. Keep at least one outside correctness check at a proportionate cost. A source comparison, reproducible test, observed artifact, or independent review can provide it. If the check is unavailable, disclose the limit instead of claiming validation.

Then perform the requested task through its appropriate recipe. Do not narrate this framing as a separate deliverable unless asked. Keep read-only work read-only and retain the original task's output and evidence requirements.
