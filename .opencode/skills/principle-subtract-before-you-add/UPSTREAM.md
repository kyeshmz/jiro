# Upstream source

Adapted from [PStack's subtract-before-you-add principle](https://raw.githubusercontent.com/cursor/plugins/dbf49813a39c1a5389c5e28cb8e4c1c2379e2454/pstack/skills/principle-subtract-before-you-add/SKILL.md) at revision `dbf49813a39c1a5389c5e28cb8e4c1c2379e2454`.

OpenCode conversion follows the [existing port's installer](https://github.com/kyeshmz/opencode-pstack/blob/84220454f9f2bb61e771c1862fea8d404ffc8ea4/scripts/install-opencode.py) and [conversion rules](https://github.com/kyeshmz/opencode-pstack/blob/84220454f9f2bb61e771c1862fea8d404ffc8ea4/scripts/opencode-transform.py). Removal-first sequencing, observed usage, and prompt simplification are retained. The adaptation requires verified behavior, preserves necessary boundary validation, and separates code simplification from unauthorized deletion of user state. The upstream MIT notice is preserved in [LICENSE](LICENSE).
