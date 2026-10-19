---
name: principle-type-system-discipline
description: Apply when designing types, reviewing signatures, or writing statically typed code. Make illegal states unrepresentable, distinguish semantic primitives, parse external data, exhaust variants, and derive types from authoritative schemas. Use when explicitly invoked as @principle-type-system-discipline.
license: MIT
metadata:
  opencode/autoinvoke: false
---

# Type system discipline

Read `references/shared-rules.md` before applying this tool. Resolve bundled paths from this skill's base directory. Run project checks in the target repository or assigned worktree.

Make the compiler reject impossible states, mismatched primitives, and unhandled variants. Define errors and special cases out of existence where the domain permits it instead of distributing handlers across callers.

- Give semantic primitives distinct types. `UserId` and `OrderId` may both store strings, but callers should not interchange them. Use a branded intersection, a newtype, or the language's equivalent when identical primitives carry different meanings.
- Validate at creation and trust the established type downstream. An unchecked cast does not establish the invariant.
- Treat RPC payloads, JSON, IPC messages, CLI arguments, configuration, environment variables, and database rows as untyped until parsed. Turn each boundary's raw input into the domain model.
- Represent meaningful alternatives explicitly and check variants exhaustively. Adding a variant should expose the callers that need to handle it.
- Derive types from the file that owns the shape. Use the protocol buffer, OpenAPI specification, GraphQL schema, database migration, design-token file, or other authoritative source instead of maintaining a parallel handwritten model.

Load `principle-boundary-discipline` for validation placement and `principle-encode-lessons-in-structure` for durable enforcement. Load `typescript-best-practices` for TypeScript-specific guidance when available. Use the target project's actual language version and APIs rather than assuming a syntax or introducing an unrelated type framework.

Verify both accepted and rejected cases with the project's static checks. Keep runtime boundary tests where the compiler cannot inspect external input.

Keep the requested scope and permission gates. Read-only work stays read-only. Commits, pushes, PRs, deploys, global installs, and destructive actions need authorization.
