---
name: principle-separate-before-serializing-shared-state
description: Apply when concurrent actors could write the same file, branch, key, API, or state object. Remove the shared write target first and serialize structurally only when a single canonical object is required. Use when explicitly invoked as @principle-separate-before-serializing-shared-state.
license: MIT
metadata:
  opencode/autoinvoke: false
---

# Separate before serializing shared state

Read `references/shared-rules.md` before applying this tool. Resolve bundled paths from this skill's base directory.

Ask whether actors need the same mutable object before adding a lock. Shared writes cause intermittent races. Instructions and conventions do not control concurrency.

1. Inventory shared mutable state. Include files actors read and write, branches they push to, keys they update, and APIs they define and consume.
2. Separate independent facts. Give each actor an owned file, key, branch, or state directory. Merge the facts only at the reading or reporting boundary.
3. Check the actual write unit. Two actors updating separate `lastX` fields in one `state.json` still share a write target. Separate `indexer-state.json` and `metrics-state.json` do not share that file mutation.
4. Require a reason for one canonical mutable object. Only then enforce serialization with a lockfile, sequential phases, an exclusive single-writer actor, or atomic compare-and-swap.

Treat a proposed lock as a prompt to revisit ownership, not the default design. Load `code-organization` when changing ownership or module boundaries. Verify the chosen design under overlapping writes, not only in a sequential happy path.

Keep the requested scope and permission gates. Read-only work ends with the ownership design. Commits, pushes, PRs, deploys, global installs, and destructive actions need authorization. Do not remove another actor's state or lock without evidence and approval.
