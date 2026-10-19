# Review rubric

Use only lenses relevant to the change. Trace concrete execution paths rather than filling a checklist with hypotheticals.

## Correctness

Does the implementation achieve the stated intent on happy and failure paths?

- Check empty inputs, missing values, boundaries, encoding, coercion, overflow, and off-by-one behavior.
- Trace error handling, swallowed failures, stale closures, dangling references, and races.
- Ask what happens on retry or a crash halfway through. Identify missing reconciliation when leftover state changes the result.
- For shared mutable files, branches, or data, check exclusive ownership, isolated state, or structural serialization. A convention is not a lock.

For a suspected missing-value bug, show how a real caller can supply the value and how it reaches the failure.

## Root cause

Read callers, callees, type definitions, and sibling modules before judging the layer of a fix.

- Look for guards masking invariant violations, retries hiding broken contracts, and casts silencing modeling errors.
- Explain why a workaround is necessary and what contract would remove it.
- Check whether the correction belongs in a different owner's boundary.
- Prefer a type constraint, lint rule, runtime check, or test over another comment saying not to make the same mistake.

## Structural integrity

- Validate external data at boundaries and trust established internal types.
- Separate high-level orchestration from low-level detail without creating pass-through layers.
- Check coupling, state ownership, and data structures against actual access patterns.
- Ask whether the requirement looks integrated or bolted onto an obsolete shape.
- Check duplicate internal APIs and transitional paths. Recommend migrating callers and removing a redundant path within scope when no external compatibility requires it.

Do not penalize simple code for lacking abstraction. Duplication can be cheaper than a speculative framework.

## Verification

- Check whether tests exercise behavior rather than implementation details.
- Look for assertions that would catch the actual regression.
- For a bug fix, assess the failing-before and passing-after evidence or the reason a focused test is impractical.
- For an integration boundary, inspect full-path proof rather than an isolated proxy.
- Check the real value rather than inferring liveness from cached state or file timestamps.
- For delegated or asynchronous work, verify output artifacts instead of accepting a summary.

Missing proof is a verification gap, not automatically a demonstrated product bug.

## Complexity budget

- Look for branches, helpers, options, and layers that can disappear without changing behavior.
- Question one-caller abstractions, hypothetical configuration, dead code, unused imports, and vestigial parameters.
- Check whether finished migrations left unnecessary compatibility scaffolding.
- Ask whether each user-facing control or feature earns its implementation cost. A half-finished feature can be worse than no feature.

Prefer simpler code unless the simpler version is wrong.

## Security

Trace the input path to the dangerous operation for every security finding.

- Check untrusted input reaching SQL, shell execution, dynamic evaluation, or unsafe HTML.
- Check authentication and authorization at new endpoints and trust boundaries.
- Check secrets in source, logs, and error messages.
- Check time-of-check versus time-of-use races on security-critical state.

Do not require a second reviewer to agree before investigating a concrete security path.
