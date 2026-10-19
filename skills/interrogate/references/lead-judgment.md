# Lead judgment

## Resist inflated findings

Adversarial reviewers can fill an empty review with nits. If the findings are only stylistic preferences, say that the code has no substantiated blocking issue. An empty review is valid.

## Separate possible from reachable

A missing-value concern matters only if a real caller can supply that value. Trace the caller, validation, types, and runtime path. Dismiss unreachable cases with evidence. Reviewers seeing only a diff can miss upstream constraints that the lead can inspect.

## Make abstractions earn their cost

Ask what real variation or responsibility requires a proposed helper, interface, or new layer. Simple inline code can be better than a speculative abstraction. Favor an alternative when it deletes substantial complexity, not merely because it looks more uniform.

## Reject preference-only feedback

A different personal implementation is not a defect. Require a concrete correctness, security, maintenance, or verification problem in the current shape. Explain why a preference-only finding was dismissed.

## Restore missing context

Watch for recommendations that change unrelated code, reject an intentional repository pattern, conflict with known constraints, or assume unavailable APIs. Investigate rather than treating limited-context mistakes as bad faith. Dismiss gracefully when context clears the concern. A surrounding pattern can itself be flawed, but the reviewer must show how this change creates or worsens a real issue.

## Take uncomfortable evidence seriously

Independent agreement increases confidence. A concrete execution path, a gap in the lead's mental model, or a newly demonstrated invariant failure matters even from one reviewer. Do not dismiss an inconvenient result to defend the author's choice.

Give correctness and security findings particular scrutiny regardless of vote count. Check the evidence before classifying them. Distinguish a proven failure, a credible unverified risk, and a preference. Preserve the source reviewers and rationale in every bucket.
