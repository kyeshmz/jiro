---
name: principle-test-behavior-not-implementation
description: Apply whenever writing, changing, reviewing, or retaining a test. Assert the consumer's observable contract so the test catches broken behavior and survives internal restructuring. Use when explicitly invoked as @principle-test-behavior-not-implementation.
license: MIT
metadata:
  opencode/autoinvoke: false
---

# Test behavior, not implementation

Read `references/shared-rules.md` before applying this tool. Resolve bundled paths from this skill's base directory. Run project checks in the target repository or assigned worktree.

Test what a caller, end user, or another service can observe through its interface. Include return values, errors, readable state, and external effects such as a request, written row, or emitted message. Private helpers, internal call order, and intermediate data are implementation details unless the public contract exposes them.

Judge every test against two imagined edits.

- Break the behavior. Return a wrong value, skip an effect, or perform it twice. The test should fail. Loose assertions, expectations computed by the code under test, a copied constant that never exercises its consumer, and assertions on self-built test data can all miss the failure.
- Change the internals. Preserve observable results while restructuring the implementation. The test should keep passing. A failure here exposes coupling that makes refactors expensive without catching a consumer-visible bug.

Keep tests that catch the first edit and survive the second. Rewrite or remove tests that do not, while preserving useful contract coverage. Drive the real interface with concrete input. Derive expected values from the requirement, not a run of the implementation. Assert the full contract without adding promises the interface does not make.

## Contract examples

- For an empty cart that must never charge, asserting no payment-client call is behavior. Pair it with a case that does charge to show the test can observe a call.
- A payload received by an external service is behavior. An internal helper call is not.
- An empty list is the exact contract when nothing matches. It is a hollow check when the scenario should return a record.
- Assert an error type when callers branch on it. Pin exact wording only when that wording is part of the consumer's contract.
- A cross-table key invariant or compile-time type constraint can be the behavior itself. A test need not observe a function call to be useful.

Keep the requested scope and permission gates. A read-only review reports test changes rather than making them. Commits, pushes, PRs, deploys, global installs, and destructive actions need authorization.
