---
name: minimize-reader-load
description: Use when reviewing or shaping code that is hard to trace. Reduce the layers between a question and its answer, shrink hidden and mutable state, and reject abstractions that add more reading work than they remove.
license: MIT
---

# Minimize reader load

Maintainability is the work a reader must do to understand code. Track two independent axes.

- **Layers to trace.** Indirections between the question and its answer.
- **State to hold.** Hidden or mutable context the reader must keep in mind.

Line count and architectural labels are proxies, not the goal. A flat file with many globals can be as hard to understand as a stack of adapters. Guard both axes.

## Apply

1. Pick a real question a maintainer needs to answer. Trace the relevant path and name the state that can affect its result.
2. Collapse wrappers and pass-through layers that cost more than they save. Keep a boundary when it hides meaningful decisions, adapts a representation, or adds required policy.
3. Make adjacent layers change the abstraction. Repeating the same methods and arguments does not compress understanding.
4. Prefer a simple interface that hides substantial complexity. Do not make callers learn both the public surface and its implementation rules.
5. Shrink state scope. Prefer pure returns over mutations, locals over fields, fields over module state, and module state over globals. Derive values instead of synchronizing copies.
6. Establish each invariant once at its owning boundary, rather than in every consumer.
7. Before adding a layer or state, identify the reading work it removes elsewhere. If it does not earn its cost, do not add it. Preserve behavior and verify any structural change.

## Check

Can a new reader answer "Where does X come from?" and "What can change X?" in under 30 seconds? Use this as a review heuristic, not a measured result unless a reading exercise was actually timed.

Report the specific layers removed, the state scope reduced, and any complexity that remains necessary. Do not claim a readability improvement from fewer lines alone. A review does not authorize unrelated edits.
