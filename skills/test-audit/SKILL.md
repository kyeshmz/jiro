---
name: test-audit
description: "Writing/changing/reviewing/sweeping tests: reject duplicate or implementation-coupled proof; remove test-only production seams. Use for @test-audit, a test audit or pruning sweep, or when Jiro routes a test-value review."
license: MIT
metadata:
  opencode/autoinvoke: false
---

# Test Audit

> **Modified file notice:** Jiro adapted this skill from OpenClaw's `test-audit`
> at commit `6f638fd0aa42b91267bb5056ccb25df7e64b3101` for OpenCode V2. It changed
> the frontmatter, added the OpenCode section, replaced links to OpenClaw-only
> testing guides, and labeled OpenClaw examples in this file,
> [CAMPAIGN.md](CAMPAIGN.md), and [references/audit.md](references/audit.md).
> See [upstream.json](../../upstream.json)
> for provenance and [LICENSE](LICENSE) for the MIT notice.

- Authoring gates every new/changed test.
- Audits: remove low-value proof in coherent owner batches; never chase deletion counts.
- Whole-subsystem campaign: read [CAMPAIGN.md](CAMPAIGN.md) first.

## OpenCode use

- Resolve `CAMPAIGN.md`, `references/`, and `LICENSE` from the loaded skill's
  base directory. Run discovery, tests, and edits in the target repository.
- Upstream wrote this skill for OpenClaw. Its commands, scripts, CI lanes, and
  Telegram campaign are examples. Use the target repository's instructions,
  test runner, changed-file checks, dead-code checks, and CI routing. Report a
  missing equivalent instead of inventing one.
- A read-only review or audit reports candidates and edits nothing. Delete
  tests or production seams only inside the requested scope. Commits, pushes,
  PRs, and merges need explicit authorization.

## Authoring gate

Before adding test, answer:

1. Protected observable behavior, invariant, or independent contract?
2. Credible regression that makes it fail?
3. Why existing proof misses it? Each contract: one primary owner at strongest
   boundary. Another layer needs distinct transport/lifecycle risk. Extend
   tables/shared fixtures; consolidate repeated setup.
4. Export, flag, wrapper, injection hook with no production caller needed?
   Move proof to real boundary instead.

- Use the target repository's testing guide and
  [behavioral test principle](../principle-test-behavior-not-implementation/SKILL.md).
- Regressions must fail pre-fix for intended reason, pass after repair; report
  unavailable baseline proof.
- One owner regression covers bug; never replay at every crossed layer.
- Behavior-preserving refactors should not break test.

## Junk patterns

- Reject self-comparisons, copied inventories, source greps,
  implementation/call-shape assertions, duplicate contracts, test-only seams,
  subject-generated expected values, mocks supplying asserted behavior.
- Fixtures must not fabricate owner receipts/order or claim persistence path
  never writes.
- Negative controls must fail at intended guard; names must match exercised behavior.
- Auditing candidates: use [full checklist](references/audit.md#junk-patterns).

## Retention bar

- Keep independent API, SDK, protocol, config, migration, storage, security,
  platform, default, prompt-byte, generated-language, package, release,
  architecture, observable-ordering contracts. Static/slow ≠ disposable.
- Source inspection must survive identifier-only refactors and guard independent
  user-facing contract.
- Baseline failures may be bugs to repair, not tests to delete.

## Audit and validation

- Before audit edit: read [candidate evidence and workflow](references/audit.md#candidate-evidence);
  inspect full owners/callers/history; record remaining proof before deletion.
- Delete obsolete production seams with tests; never optimize for deletion counts.
- Follow the target repository's proof policy and
  [prove-it-works](../principle-prove-it-works/SKILL.md); never edit a checkout
  during its active test run; run owner/sibling proof + changed checks; then
  review the diff skeptically.
- Report causes, retained contracts, proof/cost, production versus test LOC,
  follow-ups. Commit/push/land only with task authority.
