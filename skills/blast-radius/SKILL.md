---
name: blast-radius
description: Trace what a change can break beyond its diff and prove the load-bearing safety fact against real code. Use for @blast-radius, blast radius of X, what could this break, or a small diff whose downstream effects are uncertain.
license: MIT
metadata:
  opencode/autoinvoke: false
---

# Blast radius

Find downstream breakage that a caller list alone cannot reveal. `how` establishes behavior. `why` establishes rationale. This skill tests the facts that make a change safe.

Read `references/shared-rules.md`. Resolve resources from the loaded skill base. Keep a review read-only. Do not edit product files, commit, post findings, or run a destructive reproduction without authorization. Use existing checks or an isolated scratch probe when safe. If proof needs otherwise forbidden writes, report the gap instead of treating this workflow as permission.

## Ground the change

Read the diff, changed and removed symbols, affected contracts, and non-obvious behavioral differences. Use `why` for relevant commit or PR context and `how` when runtime flow is unclear. Confirm the actual base and artifact state rather than assuming a branch named `main`.

## Find the safety fact

Identify the one or two facts on which most safety claims depend. For example, an operation might only evict already-dead entries and have no other side effect. Spend effort establishing that fact instead of listing speculative risks.

Track each fact on this evidence ladder and say where it stops.

1. Assertion only. Unsupported on its own.
2. A real `file:line` or pinned library source.
3. A traced bad case that cannot reach the failure.
4. An executable probe of real code with an assertion that fails if the fact is wrong.
5. Reproduction in the running application.

Advance as far as is cheap and safe. A convincing explanation is not runtime proof. Usually one small probe of the exact shipped library function is more useful than a long writeup.

## Follow the hidden boundaries

1. Inspect the called library's pinned version and local patches, not just its name or current online documentation.
2. Establish execution timing, including microtasks, lifecycle, unmount, and teardown. Do not transfer one framework's lifecycle assumptions to another.
3. Trace JSON responses, database columns, wire formats, feature flags, other languages reading the same bytes, and consumers several hops away.
4. Cite real code and observed contracts. A scoped search that finds no caller can be evidence with a stated limit. Never invent a consumer or API.
5. Separate confirmed risks from checked-and-cleared cases. Give each risk a concrete mechanism, likelihood, and impact. Label inferred likelihood or unobserved cost as such.

## Prove the fact

Call the real code with the relevant bad case. Use the project's existing test harness or an isolated scratch script that imports the exact dependency the application ships. Check concrete outputs and fail loudly. Read the probe before running it and isolate persistent state, network effects, ports, and credentials. Do not mutate live user data to establish safety.

For a large or wide change, use `arena` for competing read-only analyses or `swarm` for distinct coverage slices. Give each worker the same safety question and constraints. Parent verification still decides which claims hold. Inherit models unless an override is explicitly authorized and available. Do not describe same-model analysis as cross-model evidence.

## Report

- **What changed.** Include behavior that is not obvious in the diff.
- **The safety fact.** State the fact, evidence level reached, probe and observed output. Mark it unproven if proof is missing.
- **Risks.** Give mechanism, location, likelihood and impact with uncertainty labels, and the cheapest check. Show proof for consequential confirmed failures.
- **Cleared cases.** State what was examined and why the failure does not occur.
- **Before merging.** Name any missing gate and the cheapest test or reproduction that would settle it. Do not merge or publish as part of this review.

Use `unslop` for the writeup when available. Preserve technical precision and remove private information before any authorized public sharing.
