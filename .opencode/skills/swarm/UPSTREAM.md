# Upstream source

Adapted from [`pstack/skills/swarm/SKILL.md`](https://github.com/cursor/plugins/blob/ccb5507cec1546dc88135c1139c811e6c59115ba/pstack/skills/swarm/SKILL.md) in `cursor/plugins` at `ccb5507cec1546dc88135c1139c811e6c59115ba`. The complete source was read at this immutable revision. The upstream MIT notice is preserved in [LICENSE](LICENSE).

**Take.** Frame, fan out, aggregate, report; partition / race / mixed shapes; declared first-pass / rank-all / best-of selection; isolated outputs; exact commit and measurement receipts; PASS / ISSUES / BLOCKED reports; one replacement for missing required receipts; explicit coverage gaps and dropouts.

**Adapt.** Use local OpenCode `subagent` calls and completion notifications. Inherit models unless user-authorized and host-confirmed. Reuse the bundled delegate contract for durable parent-owned plans, briefs, and per-attempt reports. Inspect artifacts and rerun relevant acceptance checks before accepting code. Account for dirty diffs and drain all launched workers even after finding a winner. Isolation includes checkouts, generated files, Git state, mutable fixtures, and ports.

**Skip.** Cursor cloud workers, Task-only arguments, Cursor model aliases and error-message model guessing, branch switches in the parent's checkout, and nested coordinator / PR-merge automation. Do not import broader poteto-mode autonomy.

Runtime syntax follows the [OpenCode V2 agents guide](https://opencode.ai/v2/docs/agents) and [skills guide](https://opencode.ai/v2/docs/skills).

**Verification boundary.** Packaging checks do not prove live coverage, races, cancellation, model diversity, or full upstream behavioral parity.
