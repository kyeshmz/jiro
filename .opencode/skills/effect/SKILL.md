---
name: effect
description: Work with Effect v4 TypeScript services, schemas, layers, workflows, and tests. Use when implementing, debugging, or reviewing Effect code.
license: MIT
---

# Effect

Use Effect for typed, composable TypeScript services, schemas, and workflows in projects that already use it. This skill targets Effect v4. Check the project's dependency version first. If it uses v2 or v3, flag the mismatch rather than silently migrating it or mixing APIs.

## Source Of Truth

Use the current Effect v4 source, not memory or older Effect v2/v3 examples.

1. If `.opencode/references/effect` is missing, clone `https://github.com/Effect-TS/effect` there when network access and project writes are permitted. Do this in the task's project, not in the installed skill folder. Do not overwrite an existing checkout. If the source cannot be obtained, report the gap rather than inventing APIs.
2. Confirm the checkout contains Effect v4. Search `.opencode/references/effect` for exact APIs, examples, tests, and naming patterns before answering or implementing Effect-specific code.
3. Also inspect existing repo code for local house style before introducing new patterns.
4. Prefer answers and implementations backed by specific source files or nearby repo examples.

## Guidelines

- Prefer current Effect v4 APIs and project-local patterns over old blog posts, examples, or package-memory guesses.
- Use `Effect.gen(function* () { ... })` for multi-step workflows.
- Use `Effect.fn("Name")` or `Effect.fnUntraced(...)` for named effects when adding reusable service methods or important workflows.
- Prefer Effect `Schema` for API and domain data shapes. Use branded schemas for IDs and `Schema.TaggedErrorClass` for typed domain errors when modeling new error surfaces.
- Keep HTTP handlers thin. Decode input, read request context, call services, and map transport errors. Put business rules in services.
- In Effect service code, prefer Effect-aware platform abstractions and dependencies over ad hoc promises where the surrounding code already does so.
- Keep layer composition explicit. Avoid broad hidden provisioning that makes missing dependencies hard to see.
- In tests, prefer the repo's existing Effect test helpers and live tests for filesystem, git, child process, locks, or timing behavior.
- Do not introduce `any`, non-null assertions, unchecked casts, or older Effect APIs just to satisfy types.
- Do not answer from memory. Verify against `.opencode/references/effect` or nearby code first.

## Testing Patterns

- Discover the target repo's Effect test helpers before choosing one. In the OpenCode source repo, use `testEffect(...)` from `packages/core/test/lib/effect.ts` for tests that exercise Effect services, layers, runtime context, scoped resources, or platform integrations. That path is an OpenCode example, not a dependency to assume or create in other projects.
- Use `it.live(...)` for filesystem, git repositories, HTTP servers, sockets, child processes, locks, real time, and other live platform behavior when the repo's Effect test integration supports it.
- Follow the target repo's documented test commands and working directories. In OpenCode, run package tests from package directories such as `packages/core`, never from its repo root. Do not assume every project has that layout.
- Prefer explicit test layers over ad hoc managed runtimes. Keep dependency provisioning visible in the test file.
- Use scoped fixtures and finalizers for resources that must be cleaned up, including temporary directories, flags, databases, fibers, servers, and global state.
