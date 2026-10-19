---
name: principle-guard-the-context-window
description: Apply when context is filling with large outputs, long files, repeated reads, or fan-out planning. Bound each phase and retain evidence-linked summaries rather than raw bulk. Use when explicitly invoked as @principle-guard-the-context-window.
license: MIT
metadata:
  opencode/autoinvoke: false
---

# Guard the context window

Read `references/shared-rules.md` before applying this tool. Resolve bundled paths from this skill's base directory.

Protect room for reasoning and verification. Context overflow can degrade reasoning, lose constraints during compression, and halt the task.

- Size phases before starting them. Cap files, output volume, and turns per phase. Account for the cost of setup, tool results, handoffs, and verification.
- Search for the relevant section before reading bulk. Keep required full-skill reads intact, but avoid repeated reads of unchanged evidence.
- Save large payloads as scoped artifacts. Keep the decision, essential findings, uncertainty, and exact artifact pointers in the main thread.
- When delegation is authorized and useful, give a chef the bulk inspection and request a bounded summary with evidence. Give it the original brief, later constraints, working directory, owned scope, allowed writes, and acceptance checks.
- Otherwise narrow the local phase rather than silently spawning workers. Context pressure does not authorize delegation.

Use native supported tool arguments for chefs. Inherit the current model by omitting `model`. Set a model only when authorized and its exact ID is confirmed by the host. Load `delegate` when available for a bounded handoff.

Do not substitute a summary for evidence you need to verify. Inspect the relevant artifact before accepting a claim. Keep searches within the active task and authorized repository or session scope.

Keep the requested scope and permission gates. Read-only work and read-only chefs stay read-only. Commits, pushes, PRs, deploys, global installs, and destructive actions need authorization.
