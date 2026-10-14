---
name: principle-subtract-before-you-add
description: Apply when sequencing an addition, refactor, or rewrite. Remove confirmed dead code, redundant checks, and empty references first, then build on the simpler base.
license: MIT
metadata:
  opencode/autoinvoke: false
---

# Subtract before you add

When evolving a system, remove complexity first, then build. Leave it simpler and more capable behind the same or a smaller surface.

- Sequence removal before construction. Reduce the shape to its necessary parts before polishing it or adding scaffolding.
- Design for observed usage and the actual requirement, not speculative edge cases.
- Remove redundant validators, parsers, guards, and pass-through layers. Keep required validation at real system boundaries.
- Simplify prompts and documents by removing repeated instructions and excessive templates. Delete an empty reference rather than leaving a stub with no novel content.
- Establish the behavior contract before removing code and keep its checks green. Confirm a path is unused before calling it dead.

Apply [Laziness protocol](../principle-laziness-protocol/SKILL.md) to the size of the change and [Minimize reader load](../minimize-reader-load/SKILL.md) to the structure left behind. Subtraction is not a reason to discard necessary behavior.

## OpenCode scope

Resolve linked resources from this skill's base directory. Work only within the requested target repository or worktree. Preserve unfamiliar user edits, evidence, and state. A read-only task permits a removal plan, not deletion. Destructive state cleanup remains a separate, explicitly approved operation.
