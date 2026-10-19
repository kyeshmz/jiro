# Code-quality review

Look beyond local cleanup for a restructuring that preserves behavior while deleting substantial complexity. Recommend changes rather than implementing them during review. Tie each concern to the actual scope and constraints.

## Dimensions

1. **Structural simplification.** Look for a reframing that removes whole branches, helpers, modes, conditionals, or layers. Deleting moving parts is better than spreading the same complexity over more files. Show the concrete simpler shape and the behavior it preserves.
2. **File growth.** Treat a change that pushes a file from below 1,000 lines to above 1,000 as a strong smell. Ask whether coherent helpers, components, or modules should be extracted. A clear structural reason can justify the size. Do not split a file merely to meet a number.
3. **Branching growth.** Flag ad hoc conditions and special cases tangled into unrelated flows. Consider a domain helper, typed state machine, or proper owner when it removes the scattering. Do not replace straightforward local branches with a needless abstraction.
4. **Direct implementation.** Prefer boring, maintainable code over brittle magic. Question generic mechanisms hiding simple data assumptions, identity wrappers, thin abstractions, and pass-through helpers that add no policy or clarity.
5. **Types and boundaries.** Inspect unnecessary optionality, `unknown`, `any`, casts, and silent fallbacks masking unclear invariants. Prefer a clear typed model and explicit validation boundary when the domain supports one.
6. **Canonical ownership.** Keep feature logic out of unrelated shared paths and private implementation details out of public APIs. Reuse an existing appropriate helper. Name the package, service, or module that should own misplaced logic.
7. **Orchestration and atomicity.** Question needless serialization of independent work and related updates that can leave state half-applied. Prefer isolated parallel work or atomic transitions when they reduce brittleness. Do not frame micro-optimization as a structural defect without evidence.

## Priority and approval bar

Prioritize missed substantial simplifications and structural regressions, then tangled branches, then ownership and type boundaries, then file size and smaller legibility issues.

Treat consequential incidental complexity, unjustified file growth across the threshold, scattered feature checks, unnecessary wrappers, cast-heavy contracts, duplicated canonical helpers, and misplaced logic as presumptive blockers when a concrete better shape exists. Explain the cost and allow a justified constraint to resolve the concern. Correct ordinary behavior alone does not erase a material maintainability regression.

Be direct and serious, not rude. Do not soften a major structural defect into a naming suggestion. Do not invent a defect merely to sound demanding. The lead reviewer decides whether the demonstrated benefit earns the scope and cost.
