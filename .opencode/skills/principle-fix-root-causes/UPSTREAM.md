# Upstream source

Adapted from [PStack's fix-root-causes principle](https://raw.githubusercontent.com/cursor/plugins/dbf49813a39c1a5389c5e28cb8e4c1c2379e2454/pstack/skills/principle-fix-root-causes/SKILL.md).

The source revision is `dbf49813a39c1a5389c5e28cb8e4c1c2379e2454`. The upstream MIT notice is preserved in [LICENSE](LICENSE).

The OpenCode adaptation uses native invocation metadata. It preserves reproduction, instrumentation, pattern searches, cheap diagnostic signals, and persistent-state investigation. It distinguishes symptom-hiding guards from necessary boundary validation, limits fixes to the requested scope, and requires approval before resetting user state.
