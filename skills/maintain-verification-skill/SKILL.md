---
name: maintain-verification-skill
description: Audit a project's verification skill and feature map against source and a complete live feature pass. Use for @maintain-verification-skill or an explicit request to audit or refresh a verification skill.
license: MIT
metadata:
  opencode/autoinvoke: false
---

# Maintain a verification skill

Keep the app's verification instructions accurate for the next person or agent who must prove behavior. Cover every feature file in source and in the running app. Do not turn each prose bullet into a separate test.

Read `references/shared-rules.md` before working. Resolve bundled references from this skill's reported base directory. Resolve the target verification skill's resources from its own base directory. This is an on-demand maintenance pass, not a scheduler.

## State the outcome

End with exactly one outcome.

- `clean` means every feature received source and live coverage. No correction is needed. Create no branch or PR.
- `changed` means proven corrections are ready in the verification skill's own directory. Shipping is separate. If a PR is authorized, use at most one PR for this pass.
- `blocked` means coverage could not finish or corrections could not be proved safely. Name the exact blocker and incomplete features.

## Keep the edit boundary narrow

Edit only the selected verification skill's directory. This includes its `SKILL.md`, feature map, and scripts it owns. Do not edit product code. Do not silently alter a shared harness outside the owned directory.

A mismatch is either documentation drift, a harness gap, or a product regression. A regression stays a finding. Do not rewrite the expected behavior to conceal it. Do not commit, push, open or merge a PR, deploy, delete user state, or install globally without authorization.

## 1. Locate the target

Find a project-local skill with launch and drive instructions plus a feature map. Start under `<target-repository>/.opencode/skills/`, or the existing top-level `skills/` directory for an OpenCode configuration-root repository. Read repository instructions and current changes first.

If several plausible targets remain, ask which one. If none exists, stop and point to `@create-verification-skill`. Do not invent a maintenance target or audit an unrelated skill merely because its ID starts with `verify-`.

## 2. Check the index

Read the feature map's README. Compare the index with sibling feature files. Correct missing, extra, duplicate, and dead entries within scope. Keep this lightweight. Do not add a generated inventory solely for this pass.

Keep concise scratch notes of features, source coverage, live coverage, evidence paths, prerequisites, drift, and outcome. Do not commit the notes by default.

## 3. Read every feature from source

Use one read-only OpenCode subagent per feature when that tool is available. Launch independent readers concurrently with `agent: general`. Give each reader the working directory, feature path, relevant source pointers, original request, and allowed evidence sources. Forbid edits, app driving, commits, and external writes. Do not use unsupported `readonly` or editor-specific spawn arguments.

Inherit the parent model by omitting `model`. An override requires user authorization and host confirmation of the exact model and variant. Do not invent a cheap-model default. If subagents are unavailable, read the same slices directly and disclose the missing parallel pass. The coverage bar does not change.

Each reader returns this shape:

1. Feature summary from the user's point of view.
2. Source entry points with paths and symbols.
3. Likely drift with evidence, or an explicit none.
4. One concise live-verification recipe with observable expected results.

The coordinator owns all live driving. Children never drive the app.

## 4. Reconcile the source wave

Require a returned summary for every feature file. Merge overlapping recipes into as few app states as practical. Spot-check cited drift. Do not redo every clean source claim.

Sweep recent source churn for missing user-facing features. Require a concrete source path before declaring an omission. Add or correct the map only when source and intended behavior support it.

## 5. Drive the complete live pass

Run this pass even when source looks clean. Follow the target skill's launch model. Use one long-lived instance driven serially for a server or UI. Use a fresh isolated session per drive for a short-lived CLI when its Launch section requires that.

Exercise every feature at least once. Preserve these invariants throughout failures and retries:

1. Health-check before the first drive and each fresh isolated session. Health-check again after a failed or surprising drive. Never drive a suspect instance on hope.
2. When the health check cannot see a wedged UI state, reset to a known state or relaunch the owned instance.
3. Keep evidence outside disposable run state. Check its named location after every cleanup.
4. Clean residue from failed iterations. Nothing started by the run outlives its usefulness. For a shared instance, remove only run-owned residue. Do not stop the shared instance.

When the health check itself drifted, fix it within scope and retry once. Restart only what that correction invalidates. Then report `blocked` if the check still cannot establish a usable instance.

Call a feature `verified-unreachable` only when the report names the concrete prerequisite and attempted route. Examples include auth, entitlement, OS support, and external state. This label proves the access boundary, not the feature's behavior. Record a missing prerequisite in the map as drift. Do not count an unexplained failure as coverage.

## 6. Triage and re-prove

- Correct a wrong or missing user-facing description as documentation drift.
- Correct a harness gap when working app behavior cannot be driven. Make owned scripts executable and document their invocation in the target skill.
- Report broken app behavior as a product gap. Keep its fix outside this pass.
- Re-drive every harness correction live. Re-run the affected feature after a map correction that changes its recipe or expected result.

Do final teardown after the last drive, including all re-proofs. Stop only processes the run owns. Preserve evidence and confirm it remains readable.

## 7. Finish without implied shipping

Read every changed file. Report the outcome, feature coverage, unreachable prerequisites, confirmed drift, product findings, commands actually run, evidence paths, and incomplete work.

For `changed`, leave the proven local diff unless shipping was requested. If authorized to open a PR, follow repository gates and use one PR containing only proven verification corrections. For `clean` or `blocked`, create no PR. Do not claim the whole app works when only its mapped features were covered.
