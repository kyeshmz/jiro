---
name: typescript-best-practices
description: Apply domain modeling, boundary validation, sound narrowing, schema-derived types, real tests, and structured telemetry to TypeScript. Use for @typescript-best-practices or when explicitly asked to apply these rules to .ts or .tsx work.
license: MIT
metadata:
  opencode/autoinvoke: false
---

# TypeScript best practices

Make invalid states harder to construct and valid code easier for the next maintainer to trust. Apply these rules to the requested change, not as authorization for a repository-wide rewrite.

Read `references/shared-rules.md` from this skill's reported base directory. Load `principle-type-system-discipline` first. Load `principle-boundary-discipline` for parsing and adapter work. If a companion cannot load, report the missing skill and apply the concrete rules here without claiming it ran.

Read [references/patterns.md](references/patterns.md) for examples before changing the corresponding pattern. Check the project's TypeScript version, compiler options, schema library, and existing conventions. Examples explain shapes. They are not evidence that a dependency or API version is installed.

| Rule | Apply it this way |
| --- | --- |
| Discriminated unions | Model mutually exclusive states with a shared literal discriminant. Avoid boolean and optional-field bags that allow contradictions. |
| Branded types | Separate primitives with distinct meanings. Follow an existing brand convention. Otherwise use `& { readonly __brand: "X" }`. Produce a brand through actual validation, not a bare cast. |
| Constructive modeling | Choose a shape whose construction rules exclude illegal values. Use `[T, ...T[]]` for nonempty data or `[T, T][]` for pairs. A plain numeric duration still needs validation if negative values are illegal. |
| Simplest total type | Keep `T[]` while operations remain total. Strengthen to a nonempty type only when an operation otherwise needs `!`, a cast, or a supposedly impossible throw. Returning `undefined` can also be an honest total result. |
| `unknown` over `any` | Treat external input as `unknown` until parsed. Do not leak an untyped payload into business logic. |
| Schemas before guards | Use the repository's runtime schema system before hand-writing property-by-property guards. Derive the TypeScript type from that schema where practical. Do not add another schema dependency for one check. |
| Avoid unchecked `as` | A cast does not validate at runtime. Prefer construction, narrowing, parsing, or a better signature. If an irreducible boundary needs an assertion, isolate it and document the validated evidence. |
| Narrowing order | Prefer a discriminant switch, then `in`, then `typeof` or `instanceof`, then a sound user-defined guard. An assertion is the last resort after validation. |
| Type guards | Verify the whole claim. Name predicates `isX` or `hasX`. A false predicate hides the bug behind a safety promise. |
| Exhaustiveness | Use an inline `never` assignment in the default arm so an added variant fails compilation. Preserve value-returning or void control flow as appropriate. |
| `satisfies` over an assertion | Check an expression against the intended shape without replacing its inferred type. Understand contextual typing. `satisfies` is not runtime validation. |
| Boundary validation | Parse external data into a named domain type at entry. Keep `Record<string, unknown>` at that boundary. Trust established internal types instead of repeatedly revalidating them. |
| Derived types | Derive from authoritative generated schemas and existing declarations. Reach for `Pick`, `Omit`, `Parameters`, `ReturnType`, `Awaited`, and `typeof` before duplicating a shape. |
| Object arguments | Prefer named fields where positional values are easy to swap. Keep a measured hot path allocation-free when object creation matters. |
| Real tests | Run what can run locally. Prefer real framework test primitives, leak checks, and disposal checks. Verify UI in a running build. Mock only an external system that cannot run here or an established boundary. |
| Structured telemetry | Use the repository's structured logger with safe identifiers and enough context to investigate failures. Avoid `console.log` in shipped application code. Intentional CLI output follows the CLI's contract. |

## Verify the changed behavior

Run the repository's actual typecheck and relevant behavioral checks. A clean typecheck does not prove runtime validation, persistent state, or UI behavior. Exercise malformed boundary input and valid behavior where the change affects parsing.

For a concrete first editable task, follow Jiro's default of creating and proving a task-specific verification skill unless the user opts out. Reuse a relevant existing skill. Wrap an existing harness rather than duplicating it. An unrelated verification skill does not satisfy this task. A read-only review or activation without a task creates no files.

Report the type or boundary improved, commands actually run, observed behavior, and remaining limitations. Do not commit, push, open a PR, deploy, install globally, delete data, or change model settings without authorization.
