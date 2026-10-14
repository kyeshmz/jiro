# Upstream source

Copied from `opencode-pstack`'s Laziness Protocol and checked against the immutable [`pstack/skills/principle-laziness-protocol/SKILL.md`](https://raw.githubusercontent.com/cursor/plugins/ccb5507cec1546dc88135c1139c811e6c59115ba/pstack/skills/principle-laziness-protocol/SKILL.md) in `cursor/plugins` at `ccb5507cec1546dc88135c1139c811e6c59115ba`. The upstream MIT notice is preserved in [LICENSE](LICENSE).

- **Take unchanged.** All six rules, their explanatory text, and the maintainer-effort test.
- **Adapt.** Keep the exact `principle-laziness-protocol` ID. Use OpenCode explicit-invocation metadata and let Jiro load it when refactoring, sizing a diff, or considering abstractions and signal threading. Add a scope guard to preserve user work and read-only requests. In the kitchen vocabulary, this tool keeps the prep simple.
- **Skip.** Machine-specific installation paths and unrelated global model settings from the generated OpenCode copy. The principle has no subagent or external-tool dependency.

Static tests check retained source text, metadata, licensing, links, and routing. Those checks do not establish how an agent will apply the principle to every design decision. Source pins and other imports remain unchanged.

The prior local port was adapted from [PStack's laziness-protocol principle](https://raw.githubusercontent.com/cursor/plugins/dbf49813a39c1a5389c5e28cb8e4c1c2379e2454/pstack/skills/principle-laziness-protocol/SKILL.md). Its confirmed-deletion, behavior-preservation, boundary-validation, reader-load link, and target-project scope guidance are retained alongside the six verbatim rules from the newer pin. The merge does not change model settings or require Cursor features.
