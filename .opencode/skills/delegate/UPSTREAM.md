# Upstream sources

Adapted from these sources in `cursor/plugins` at `ccb5507cec1546dc88135c1139c811e6c59115ba`:

- [`pstack/skills/poteto-mode/SKILL.md`](https://github.com/cursor/plugins/blob/ccb5507cec1546dc88135c1139c811e6c59115ba/pstack/skills/poteto-mode/SKILL.md), specifically its Subagents section.
- [`pstack/skills/poteto-mode/playbooks/orchestrate.md`](https://github.com/cursor/plugins/blob/ccb5507cec1546dc88135c1139c811e6c59115ba/pstack/skills/poteto-mode/playbooks/orchestrate.md), specifically bounded briefs, single-writer records, evidence, context relay, and failure accounting.

Both sources were read at this immutable revision. The upstream MIT notice is preserved in [LICENSE](LICENSE).

**Take.** Fresh workers by default; consolidated scope for retries; parent ownership of results; self-contained briefs with goal, scope, context, acceptance, verification, timebox, forbidden work, standing orders, and reports. Each record has one writer. Dependencies carry evidence, not just ordering.

**Adapt.** `delegate` is a new Jiro workflow extracted from those rules, not an upstream skill of the same name. OpenCode `general` / `explore` children replace Cursor Task and poteto-agent dispatches. The parent stores per-attempt briefs and reports in a unique local `.delegation/<task-slug>/run-<n>/` directory, or host scratch for repository-read-only work. Reports use PASS / ISSUES / BLOCKED, with parent acceptance recorded separately. Inherit models unless user-authorized and host-confirmed. Use completion notifications rather than polling. Require a stopped predecessor before a replacement writer.

**Skip.** Poteto's persona and unbundled principles; Cursor cloud placement, `/loop`, nested-coordinator assumptions, and the Bun orchestration CLI; automatic commits, pushes, PRs, merges, deploys, and broad external-action autonomy. This is bounded local delegation, not the full Orchestrate runtime.

The [delegation guide](../../../playbook/delegation/README.md) distinguishes related upstream workflows from installed features. Runtime syntax follows the [OpenCode V2 agents guide](https://opencode.ai/v2/docs/agents) and [skills guide](https://opencode.ai/v2/docs/skills).

**Verification boundary.** Static checks and isolated installation cover packaging, not live fan-out, model diversity, permission enforcement, or full upstream behavioral parity.
