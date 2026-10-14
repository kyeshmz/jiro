# Upstream sources

Adapted from PStack in `cursor/plugins` at revision `1dcc2bacde73ddd284803b7af28164d0436198fc`.

- [Architect](https://github.com/cursor/plugins/blob/1dcc2bacde73ddd284803b7af28164d0436198fc/pstack/skills/architect/SKILL.md) supplies caller-first design and comparison of distinct module shapes.
- [Design red flags](https://github.com/cursor/plugins/blob/1dcc2bacde73ddd284803b7af28164d0436198fc/pstack/skills/architect/references/design-red-flags.md) supplies interface depth, ownership, private boundaries, and single-source rules.
- [Model the domain](https://github.com/cursor/plugins/blob/1dcc2bacde73ddd284803b7af28164d0436198fc/pstack/skills/principle-model-the-domain/SKILL.md) supplies domain-based organization and data modeling.
- [Boundary discipline](https://github.com/cursor/plugins/blob/1dcc2bacde73ddd284803b7af28164d0436198fc/pstack/skills/principle-boundary-discipline/SKILL.md) supplies boundary validation and pure business logic.
- [Encode lessons in structure](https://github.com/cursor/plugins/blob/1dcc2bacde73ddd284803b7af28164d0436198fc/pstack/skills/principle-encode-lessons-in-structure/SKILL.md) supplies enforceable constraints instead of repeated instructions.

The OpenCode adaptation bundles the rules in one skill. It uses the available `how`, `why`, and `minimize-reader-load` skills without requiring PStack's unbundled `arena` or model configuration. It does not authorize unrelated rewrites. The upstream MIT notice is preserved in [LICENSE](LICENSE).
