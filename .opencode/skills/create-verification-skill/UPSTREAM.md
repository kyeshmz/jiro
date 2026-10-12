# Upstream source

Adapted from the [pstack create-verification-skill source](https://raw.githubusercontent.com/cursor/plugins/11713c683fe4add4fd403ea880580abbc9e0875f/pstack/skills/create-verification-skill/SKILL.md) in `cursor/plugins`.

The source revision is `11713c683fe4add4fd403ea880580abbc9e0875f`. The bundled feature-map examples come from the same revision. The upstream MIT notice is preserved in [LICENSE](LICENSE).

The OpenCode adaptation writes generated skills under `.opencode/skills/`. It uses `@create-verification-skill` for explicit invocation and OpenCode metadata to disable automatic invocation of the generator. It resolves bundled references from the loaded skill's base directory. The maintenance skill is optional.

OpenCode behavior follows the [V2 skills documentation](https://opencode.ai/v2/docs/skills).
