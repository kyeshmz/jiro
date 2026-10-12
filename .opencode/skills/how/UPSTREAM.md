# Upstream source

Adapted from the [pstack how source](https://raw.githubusercontent.com/cursor/plugins/11713c683fe4add4fd403ea880580abbc9e0875f/pstack/skills/how/SKILL.md) in `cursor/plugins`.

The source revision is `11713c683fe4add4fd403ea880580abbc9e0875f`. The explorer and explainer templates originate from the same revision. The upstream MIT notice is preserved in [LICENSE](LICENSE).

The port uses OpenCode `explore` and `general` subagents instead of editor-specific task arguments. Role configuration is read from the OpenCode instructions directory when available. Model choices must be authorized and confirmed by the host. The simple/complex split, parallel exploration, synthesis, and output sections are preserved.

OpenCode behavior follows the [V2 skills documentation](https://opencode.ai/v2/docs/skills) and [agents documentation](https://opencode.ai/v2/docs/agents).
