# Upstream source

Adapted from the [pstack show-me-your-work source](https://raw.githubusercontent.com/cursor/plugins/11713c683fe4add4fd403ea880580abbc9e0875f/pstack/skills/show-me-your-work/SKILL.md) in `cursor/plugins`.

The source revision is `11713c683fe4add4fd403ea880580abbc9e0875f`. The log template and helper originate from the same revision. The upstream MIT notice is preserved in [LICENSE](LICENSE).

The port uses OpenCode session exports instead of editor transcript folders. It uses OpenCode subagents, authorized model discovery, and an explicit gap when cross-family review cannot run. Companion prose skills are optional. The TSV format, append-only corrections, run boundaries, and spreadsheet-formula escaping are preserved.

OpenCode behavior follows the [V2 skills documentation](https://opencode.ai/v2/docs/skills), [agents documentation](https://opencode.ai/v2/docs/agents), and [session API](https://opencode.ai/v2/docs/api).
