---
name: principle-never-block-on-the-human
description: Apply when tempted to ask whether to do reversible work already inside the user's request. Make a reasonable execution decision, verify it, and present the result without taking over product direction or bypassing authorization. Use when explicitly invoked as @principle-never-block-on-the-human.
license: MIT
metadata:
  opencode/autoinvoke: false
---

# Never block on the human

Read `references/shared-rules.md` before applying this tool. Resolve bundled paths from this skill's base directory.

Keep authorized execution moving while the human supervises asynchronously. A reviewable implementation choice usually costs less to correct than a needless approval pause.

- Make a reasonable decision for reversible work inside the request. Do the work, verify it, and explain the decision instead of asking whether to start.
- Observe facts you can check yourself. Do not ask the user to run an available check or answer a question the repository settles.
- Record an in-scope problem and fix its cause in the next bounded unit. Keep unrelated findings separate rather than turning them into new work.
- Present assumptions, evidence, and meaningful tradeoffs so the user can course-correct.
- Ask for genuine product direction or missing authorization. The human owns the product goal. The tool owns execution within that goal.

Reversibility is not blanket permission. Keep investigations and read-only reviews read-only. Do not commit, push, open or merge a PR, deploy, install globally, make separately billable calls, or send external messages without authorization. Pause before data deletion, force-pushes to shared branches, customer messages, and other irreversible writes.

An unattended-work request does not remove these gates. If one action is blocked, continue independent authorized work where possible and report the exact blocker.
