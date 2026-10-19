---
name: tdd
description: Make a bug executable before fixing it when the user explicitly asks for TDD, a failing test, or a regression test, or when a cheap local test target is obvious. Use for @tdd. Skip new test scaffolding when the path is unclear, costly, brittle, or integration-heavy.
license: MIT
metadata:
  opencode/autoinvoke: false
---

# TDD bug fix

Capture intended behavior in a focused regression check that fails before the fix and passes after it. Do not force a bad test to satisfy a process label.

Read `references/shared-rules.md`. Resolve resources from the loaded skill base. Run commands in the target repository and use its existing harness. A request to review tests or explain a bug remains read-only unless the user requests changes.

## Workflow

1. Establish intended behavior, observed behavior, the affected path, and the smallest observable reproduction.
2. Choose the narrowest practical unit, component, integration, or regression check already used for that path. If none is obvious, do not build a broad harness solely for this workflow.
3. Write the smallest test that would have caught the defect before editing production code. Encode intended behavior rather than mirroring implementation details.
4. Run it before the fix. Confirm that it fails for the expected behavioral reason. If it passes or fails because of setup, repair the reproduction or test before changing implementation.
5. Make the smallest root-cause production change that satisfies the intended behavior and preserves nearby contracts. Load `principle-fix-root-causes` when debugging requires a deeper trace.
6. Rerun the regression test and relevant nearby checks. Confirm passing-after evidence and inspect the diff for unrelated changes.

## When a failing test is impractical

Skip new test scaffolding that needs broad harness setup, brittle mocks, slow end-to-end infrastructure, production-only state, vague reproduction, or unrelated fixture churn. Use the closest useful executable check instead. It may be a targeted script, manual reproduction command, browser automation, snapshot comparison, log assertion, or focused integration check.

Prefer no new test over one that mostly tests mocks, locks in implementation details, relies on timing or unrelated global state, needs costly infrastructure for a small fix, or would immediately be deleted. Reuse safe existing tooling. Do not introduce executable helpers merely to name the work TDD.

## Guardrails

- Do not change tests to agree with incorrect behavior.
- Do not weaken assertions unless the expected contract genuinely changed and the reason is explicit.
- Keep the regression focused. Avoid broad fixtures or unrelated coverage expansion.
- Make a flaky test deterministic where possible. State the signal being preserved and any remaining flakiness.
- For a broader failure class, prove the focused regression first. Add sibling coverage only when it earns its scope.
- Do not reset user work, mutate live user state, commit, push, or publish without authorization.

## Report

Name the failing-before test or executable check and the observed failure. Name the passing-after run and nearby validation. If failing-before proof was unavailable, say why and identify the closest check used. Do not describe a test written only after the fix as observed red-green evidence.
