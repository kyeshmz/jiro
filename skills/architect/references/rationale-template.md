# Design rationale

Keep the completed rationale near one page. Replace every note with task evidence. Omit boilerplate, not a load-bearing decision.

## Problem

State the consumer's goal and why the shape is non-obvious. Name integration constraints from grounding, including existing types, callers, and invariants crossing the boundary.

## Caller usage

Write this before the type sketch. Show a README-style example and two or three realistic imports and call sites. Show what returns. Reconcile types to valid caller usage when they disagree.

## Shape

Start with data structures, then trace data through signatures and module responsibilities. Name state owners, import direction, typed invariants, validation boundaries, and deliberate non-goals. State the complexity each interface hides and what callers still need to know. Explain why the surface is no larger than needed.

## Synthesis decision

Name the base candidate and why it won. Identify each adapted part and its source candidate. Name rejected parts and reasons. Include the judge's verdict or state that independent judging was unavailable. Record convergence, divergence, and dropouts when present.

## Tradeoffs accepted

Use one bullet per tradeoff. State what is accepted in exchange for what benefit. Explain choices a future maintainer might mistake for an oversight.

## Alternatives considered

Name at least one concrete alternative shape. Compare interface depth, complexity hidden, and complexity exposed to callers. Do not list flavors of the chosen shape. If constraints leave only one viable shape, explain why the other candidate fails. Distinguish alternatives inside a candidate from the independent candidates used for synthesis.

## Open questions and risks

Phrase genuine user decisions as questions. Separate unresolved preferences from risks the implementer can investigate. Label unsupported predictions as guesses.

## Next implementation step

Name the first verifiable unit to build if implementation is authorized. For a design-only task, state that implementation is not part of this run.
