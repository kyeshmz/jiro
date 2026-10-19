---
name: principle-minimize-reader-load
description: Compatibility entry point for Jiro's Minimize Reader Load skill. Use when reviewing tracing layers or hidden and mutable state.
license: MIT
metadata:
  opencode/autoinvoke: false
---

# Minimize reader load

Use the `skill` tool with `id: "minimize-reader-load"` to load and follow the [canonical Jiro skill](../minimize-reader-load/SKILL.md).

This entry point preserves the upstream principle ID without duplicating its rules. Resolve the linked skill from this skill's base directory, not the shell working directory. Apply the canonical skill only within the user's requested scope.
