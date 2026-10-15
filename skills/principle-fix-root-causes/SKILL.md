---
name: principle-fix-root-causes
description: Apply when debugging. Reproduce first, trace each symptom to its root cause, instrument instead of guessing, and resist guards that merely silence the failure.
license: MIT
metadata:
  opencode/autoinvoke: false
---

# Fix root causes

Do not fix symptoms. Trace each problem to its root cause and fix it there. Workarounds accumulate while the real bug remains.

## Pattern

- Reproduce first through the real entry point. Keep the failing check so the fix can be verified.
- Ask why until the failure is explained by a concrete mechanism and evidence.
- Do not add a guard solely to hide a symptom. A nil check that silences corrupted internal state is not a root-cause fix. Required input validation still belongs at an actual system boundary.
- If a workaround needs a paragraph-long comment to justify it, reconsider the code rather than explaining away the failure.
- Check the pattern, not just the instance. Search for related cases within the requested scope. Report cases outside that scope instead of silently expanding the change.
- When stuck, instrument. Read the actual error and state rather than guessing.
- If the deciding fact took a deep dig to find, propose a cheap, always-on signal that would have exposed it earlier. Do not claim the signal was implemented if it was only proposed.

## Restart failures

When something fails after a restart, inspect stale persistent state before assuming the code is wrong. Relevant state can include configuration, caches, locks, and serialized data.

If resetting a state file restores behavior, treat that as evidence for state validation, compatibility, or recovery as the fix. Do not make repeated deletion the permanent solution. Inspect and name the affected state first. Resetting or deleting user state requires explicit approval for the identified contents.
