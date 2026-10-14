---
name: code-organization
description: Use when designing or changing module layout, ownership, public interfaces, or shared state. Organize around domain knowledge, hide implementation decisions, and enforce boundaries instead of adding layers or instructions.
license: MIT
---

# Code organization

Read `references/organization-rules.md` before shaping the code. Apply the rules to the affected subsystem, not as permission for a repository-wide rewrite.

## Workflow

1. Ground the change in the existing callers, data model, module boundaries, and state owners. Use `@how` when the subsystem is unfamiliar. Use `@why` when changing ownership or layering requires understanding the existing rationale.
2. Write the caller's usage first. Derive the public types and signatures from realistic imports and calls, not the other way around.
3. For a non-trivial reshape, compare at least two structurally distinct candidates. Sketch module responsibilities, interfaces, state ownership, and import direction before implementing. Keep boring code when its shape is already clear and local.
4. Screen each candidate against the organization rules. Prefer the smallest public surface that hides meaningful complexity. Do not confuse a capable module with a long call chain.
5. Apply `@minimize-reader-load`. Name the layers a reader must trace and the hidden or mutable state they must understand. A new abstraction must remove more work than it creates.
6. Encode the chosen boundaries in exports, package rules, types, lint, or build checks. Derive repeated lists from one source. Do not substitute a warning in a document for a structural constraint that can be enforced.
7. Implement within the requested scope. For a behavior-preserving reorganization, capture current behavior before moving code and verify equivalence afterward. If repeated workarounds expose a wrong shape, reconsider it rather than bolting on another layer.

## Report

Name the chosen shape, the alternative rejected, the complexity hidden behind each public boundary, and what enforces ownership. For a refactor, include the behavior held fixed and the verification result. State any remaining risks or unenforced constraints.
