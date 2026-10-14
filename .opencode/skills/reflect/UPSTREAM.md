# Upstream source

Adapted from the [pstack reflect source](https://raw.githubusercontent.com/cursor/plugins/dbf49813a39c1a5389c5e28cb8e4c1c2379e2454/pstack/skills/reflect/SKILL.md) in `cursor/plugins`, linked from its [prompt recipes](https://github.com/cursor/plugins/blob/dbf49813a39c1a5389c5e28cb8e4c1c2379e2454/pstack/skills/poteto-help/references/recipes.md).

The source revision is `dbf49813a39c1a5389c5e28cb8e4c1c2379e2454`. All four reviewer and synthesizer references originate from the same revision. The upstream MIT notice is preserved in [LICENSE](LICENSE).

The port uses OpenCode's explicit-invocation metadata, known-session exports with a disclosed digest fallback, and `general` subagents with authorized model discovery instead of Cursor transcript folders, `Task` arguments, and hardcoded model slugs. Reviewer references recognize actual OpenCode skill loads and paths. Read-only MCP access, transcript injection defenses, three review lenses, separate synthesis, durability tests, existing-skill-first routing, and the Accepted / Rejected / Backlog format are preserved.

Both skill edits and external backlog filing require explicit approval. Structural enforcement stays in the backlog rather than becoming more prompt prose. Skill authoring routes to `skill-creator` when available, with a repository recipe or explicit draft / test / iterate fallback instead of requiring Cursor's built-in `create-skill`.

OpenCode behavior follows the [V2 skills documentation](https://opencode.ai/v2/docs/skills), [agents documentation](https://opencode.ai/v2/docs/agents), and [session API](https://opencode.ai/v2/docs/api).
