---
name: principle-build-the-lever
description: Apply to non-trivial edits, migrations, analyses, and checks. Build the tool that does or proves the work instead of working by hand. Leave an artifact a reviewer can rerun.
license: MIT
metadata:
  opencode/autoinvoke: false
---

# Build the lever

When the work is not trivial, build the tool that does it instead of doing it by hand. A codemod, generator, or script performs the work consistently and leaves one artifact a reviewer can inspect and rerun.

Default to building the lever. Skip it only for a couple of obvious edits that can be checked at a glance. A one-off still earns a lever when the tool makes the work checkable.

- Do the first unit by hand to learn the recipe, then build the tool. Rerun it on that unit and compare with the hand-done version. Make it safe to rerun.
- Use a codemod or script for edits, a generator for repetitive files, a query for analysis, and a rerunnable check for verification. Follow the target repository's tooling conventions.
- A deterministic lever beats fan-out. If the tool can process every unit in one pass, run it directly rather than delegating hand edits.
- When delegation is authorized and useful, the lever can be a skill every worker reads. Put the recipe, verification contract, and do-not-touch boundaries in one artifact outside the workers' write scope.
- Applying this principle produces a file. If no codemod, script, generator, or delegate skill was produced, describe the lever as proposed, not built. An investigation-only request does not authorize writing it.
- Keep the lever with the project when the work outlives the session. Commit it only when committing is part of the authorized task.

Build the smallest tool that does or proves the job, not a framework. Verify it against the real artifact, not merely a successful build or its own self-report.

This makes the current work repeatable and reviewable. Turning a recurring instruction into a durable type, lint, or runtime guard is the separate structural concern covered by [Code organization](../code-organization/SKILL.md).
