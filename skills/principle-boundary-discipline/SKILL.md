---
name: principle-boundary-discipline
description: Apply when wiring validation, error handling, or framework adapters. Validate external input at system boundaries, expose domain types, and keep business logic independent of framework wiring. Use when explicitly invoked as @principle-boundary-discipline.
license: MIT
metadata:
  opencode/autoinvoke: false
---

# Boundary discipline

Read `references/shared-rules.md` before applying this tool. Resolve bundled paths from this skill's base directory.

Validate data where it enters the system. Parse raw input into domain types, then trust the established internal contract. Repeated checks inside a validated call chain add noise without strengthening that contract.

- Validate CLI arguments, configuration, network payloads, and external API responses at their entry points. Return useful boundary errors and propagate typed internal failures without repeating validation.
- Expose domain concepts through public interfaces. Keep transport, storage, framework, and wire representations private.
- Keep general-purpose mechanism inside the module and special-purpose policy at its edge.
- Put business logic in pure functions. Keep framework wiring thin and mechanical so the logic can be tested without the framework.
- Make parsing a pure transform from raw input to typed state. Build prompts from structured state. Score and assess state with pure transforms.

Ask whether data is crossing a system boundary before adding a guard. If the contract already guarantees the condition, remove the redundant check. If the guarantee is missing, establish it at the owning boundary instead of trusting an unchecked cast.

Ask whether the shell could call a pure function instead. Extract one when it separates domain logic from framework wiring. Load `code-organization` when this changes module ownership or a public interface.

Keep the requested scope and permission gates. Read-only work stays read-only. Commits, pushes, PRs, deploys, global installs, and destructive actions need authorization.
