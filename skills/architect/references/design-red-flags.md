# Design red flags

Screen each candidate before synthesis. Apply `code-organization` as the canonical rule set. Use these questions to revise or reject a shape.

## Shallow module

Does the public surface hide substantial capability and policy? Callers should not coordinate several methods for one operation, choose internal stages, or learn the implementation to use the API. A capable module is not a long call chain.

## Information leakage

Does one private representation, policy, or protocol decision appear in several modules? Keep transport types, wire formats, storage schemas, and framework objects behind the boundary. Parse into domain types rather than publicly re-exporting external representations.

## Temporal decomposition

Are modules split by execution order instead of knowledge? Separate load, validate, transform, and save stages often repeat the same representation and invariants. Group decisions with their owner even when its methods run at different times.

## Pass-through methods

Does a forwarding method hide complexity or add policy, adaptation, or a distinct abstraction? Remove a layer that only forwards the same arguments in the same shape.

## Split ownership

Can several modules write the same state or maintain copies of it? Give state one owner. Let other modules read it or request changes. Remove needless sharing before adding synchronization.

## Equivalent paths

Can callers complete the same task in several ways? Choose one path and migrate internal callers within scope. Preserve required external compatibility deliberately rather than leaving accidental dual APIs.

## Importable internals

Can a caller bypass the intended interface? Enforce privacy through exports, visibility, lint, package rules, or build checks. An instruction not to import internals is weaker than an import that fails.

## Hand-synced lists

Must adding an item update several equivalent lists? Derive them from one source. If derivation is impossible, make the build fail when they disagree.
