---
name: principle-attack-the-premise
description: Apply when two or more fixes that share one premise have failed the same gate. Take a census of which actors hold the imbalance before the next fix, then question the premise instead of writing another fix that assumes it.
license: MIT
metadata:
  opencode/autoinvoke: false
---

# Attack the premise

When two or more fixes that share one premise have failed the same gate, suspect the premise, not the fixes. Each failure under a shared premise is evidence about that premise.

## Pattern

- Write the premise down. It is the one sentence that every failed fix assumed.
- Take a census before the next fix. Count the imbalance per actor. Identify which actors hold it, not just its total size. Write the census as a rerunnable script using [Build the lever](../principle-build-the-lever/SKILL.md).
- Read the skew. If the same few actors hold most of the imbalance on every run, something assigns them that role. Find what assigns it. That assignment is the next question under [Fix root causes](../principle-fix-root-causes/SKILL.md).
- Remove the asymmetry instead of compensating for it. Rotate, randomize, or move the role so no actor holds it on every run. A return path, shared pool, batched hand-off, or periodic rebalance can leave the assignment intact and add work on every run. Prefer the smallest change that removes the cause.

## Stop

Do not start the next fix before the premise is written down and the census exists. If the task authorizes investigation only, report the proposed census and stop before writing or changing behavior.

If the census is even across actors, this imbalance does not support rejecting the premise. Look for the cause elsewhere and keep the census as evidence.

This questions an assumption in the current design. Rebuilding a design around a new requirement is a different task. Keep both within the user's authorized scope.
