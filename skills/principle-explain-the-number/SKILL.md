---
name: principle-explain-the-number
description: Apply before trusting, reporting, or acting on a measured speedup, regression, throughput, latency, or evaluation result. Identify the measured limiter and rule out alternative explanations with evidence. Use when explicitly invoked as @principle-explain-the-number.
license: MIT
metadata:
  opencode/autoinvoke: false
---

# Explain the number

Read `references/shared-rules.md` before applying this tool. Resolve bundled paths from this skill's base directory. Run project checks in the target repository or assigned worktree.

A real output is not yet a trustworthy measurement. Explain what the number measures, what bounds it, and why competing explanations do not fit the evidence.

1. Ask why the result is not twice as good. Identify the limiting resource or code path from a profile or system counters captured during the run. Map that observation to source. A guess from reading code is not a measured limiter.
2. List what else the result could measure. Check errors, skipped work, cached work, code that never ran, an untuned comparison side, noise, and a component too small to explain the end-to-end result.
3. Rule out each plausible alternative with evidence. Do not report an improvement when the treatment did less work or either side used an unfair setup.
4. Keep the run count, spread, limiter, configuration, and evidence with the number in notes or a linked artifact.

Load `benchmark-checklist` for a performance measurement when available. For an evaluation, check that every trial did the task, the gap holds across trials and any models actually tested, and the scenario matters. Do not invent cross-model evidence or select another model without host-confirmed availability and authorization.

Treat missing run counts, missing spread, or an unnamed limiter as incomplete evidence. If claimed time savings exceed the time the changed component took, investigate the measurement before claiming a speedup.

Use `principle-prove-it-works` to check that the output itself is real. This tool explains the number derived from it. Report unavailable measurement capabilities and unresolved explanations honestly.

Keep the requested scope and permission gates. Read-only work stays read-only. Commits, pushes, PRs, deploys, global installs, and destructive actions need authorization.
