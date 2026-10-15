# Organization rules

## Organize around domain knowledge

Group code around the decisions and invariants it owns. Execution order is not ownership. Separate load, validate, transform, and save modules often repeat the same representation and rules across several boundaries.

Use a state machine, typed model, registry, discriminated union, reducer, or other structure when it removes scattered branches, duplicated assumptions, or invalid states. Do not force an abstraction when the existing code is clear and local.

## Hide complexity behind a small interface

A useful module hides substantial decisions behind a simple public surface. Callers should not need to coordinate internal stages or learn the implementation to use the interface.

Keep storage schemas, wire types, framework objects, and protocol details private. Parse external representations into domain types at the boundary. Keep business logic in pure functions and framework wiring thin.

Validate untrusted input at system boundaries. Do not repeat the same checks throughout internal code that already operates on validated types.

## Give state one owner

One module owns each piece of mutable state. Other modules read it or ask the owner to change it. Avoid competing writers and synchronized copies.

Prefer derived values over duplicated state. Remove unnecessary sharing before introducing coordination around it.

## Remove pass-through layers

A method that forwards the same arguments to another method with the same shape adds tracing work without hiding complexity.

Remove it or give the boundary a real responsibility. Keep forwarding boundaries only when they add policy, adaptation, or a distinct abstraction. Do not add a wrapper for a hypothetical second implementation.

## Keep one way to do a task

Multiple equivalent paths accumulate callers and divergent rules. Migrate callers to the chosen path and remove the redundant API within the approved scope.

Do not silently change behavior to simplify the structure. Separate a real bug fix or new feature from a behavior-preserving refactor.

## Make internals unreachable

Prevent external callers from importing private modules. Use package exports, visibility, dependency rules, lint, or build checks so an invalid import fails.

An instruction not to import internals is weaker than a boundary the tooling enforces.

## Keep one source of truth

Derive repeated lists and declarations from one authoritative source. If derivation is not possible, make a check fail when they disagree.

Adding an item should not depend on remembering every hand-maintained copy.

## Encode recurring lessons

When the same correction recurs, prefer a type, metadata flag, lint rule, runtime check, or script that prevents the mistake. If the fix is structural, use the structural fix instead of adding another instruction.

Use prose and a concrete failure example only for constraints that genuinely require judgment and cannot be enforced.
