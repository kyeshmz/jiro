---
name: principle-experience-first
description: Apply to product, UX, and feature-scope tradeoffs. Prefer a polished core workflow over implementation convenience or a larger set of rough features. Include API consumers and future maintainers as users. Use when explicitly invoked as @principle-experience-first.
license: MIT
metadata:
  opencode/autoinvoke: false
---

# Experience first

Read `references/shared-rules.md` before applying this tool. Resolve bundled paths from this skill's base directory.

Choose the consumer's experience over implementation convenience. Prefer three polished features over ten rough ones. This sets the target. Foundational thinking sets the sequence of work that reaches it.

- Name who consumes the work. Include the end user, the colleague importing a library or internal API, and the engineer who maintains it next.
- Justify every feature, control, and option by what it improves for those people.
- Tighten the central workflow. Remove or defer features that distract from it rather than increasing the option count.
- Prototype uncertain experience decisions before investing in production code.
- Check transitions, alignment, spacing, feedback, and error states. Small details are part of the behavior people experience.
- Explain the tradeoff from the consumer's and maintainer's perspectives before discussing implementation effort.

Load `principle-foundational-thinking` when ordering the foundations. Do not use polish as a reason to bypass correctness, accessibility, safety, or the user's product direction.

Keep the requested scope and permission gates. Read-only work stays read-only. Commits, pushes, PRs, deploys, global installs, and destructive actions need authorization.
