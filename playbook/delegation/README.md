# Chefs and workstations

Jiro carries pstack's core delegation patterns without requiring its full persona or cloud orchestration stack. Chefs are Jiro's OpenCode worker agents. Jiro assigns each chef a bounded station, checks its output, and owns the result. The entry skill is `jiro`, the command is `/jiro`, and the registered worker agent is `chef`. Invoke these tools explicitly in OpenCode.

## Tools and prep notes

| Skill | Purpose | Written output |
| --- | --- | --- |
| [`@jiro`](../../skills/jiro/SKILL.md) | Route an engineering order through its recipe. | A task checklist and evidence-backed final report; loads delegation tools when needed. |
| [`@create-subagent`](../../skills/create-subagent/SKILL.md) | Define a reusable worker or reviewer. | `.opencode/agents/<agent-id>.md` with role instructions, required skills, permissions, and a report contract. Global only when requested. |
| [`@delegate`](../../skills/delegate/SKILL.md) | Hand bounded units to children and check their results. | `.delegation/<task-slug>/run-<n>/plan.md`, `briefs/<unit-id>-attempt-<n>.md`, and `reports/<unit-id>-attempt-<n>.md`. |
| [`@swarm`](../../skills/swarm/SKILL.md) | Run parallel coverage, competing attempts, or a mixture. | The same run directory, plus a slice/status/evidence table and declared race rule in the plan. Returns one consolidated report. |
| [`@how`](../../skills/how/SKILL.md) | Delegate exploration and explain how a subsystem works. | An in-chat explanation with Overview, Key Concepts, How It Works, Where Things Live, and Gotchas as applicable. No source edits. |
| [`@why`](../../skills/why/SKILL.md) | Investigate rationale across available evidence sources. | An in-chat, evidence-backed synthesis with confidence and coverage gaps. No source edits. |
| [`@show-me-your-work`](../../skills/show-me-your-work/SKILL.md) | Keep the parent's decision trail. | `decisions.tsv` or `.audit/<task-slug>.tsv`, append-only. Columns are `ts`, `phase`, `decision`, `why`, `evidence`, `result`. |
| [`@create-verification-skill`](../../skills/create-verification-skill/SKILL.md) | Give workers an app-specific verification recipe. | A project-local `.opencode/skills/verify-<name>/SKILL.md` and supporting feature-map files. |
| [`@playwright-mcp`](../../skills/playwright-mcp/SKILL.md) | Drive a connected browser and verify a live user flow. | Per-run snapshots, screenshots, diagnostic excerpts, and an evidence report. Shared MCP drivers are serialized. |
| [`@playwright-cli`](../../skills/playwright-cli/SKILL.md) | Drive named browser sessions or author Playwright tests. | Browser artifacts, scenario plans, test specs, traces/videos, and test receipts. Each worker owns a named session. |

Coordination records stay local unless the user authorizes committing them. When repository writes are forbidden, `delegate` and `swarm` keep their records in a unique host-scratch directory instead.

Agent definitions and skills are different artifacts:

```text
.opencode/
  agents/reviewer.md                 # reusable role; ID is reviewer
  skills/verify-app/SKILL.md          # reusable procedure; ID is verify-app
.delegation/task-name/run-1/
  plan.md                            # parent-owned goal, constraints, dependencies, status
  briefs/unit-a-attempt-1.md          # parent-owned dispatch contract
  reports/unit-a-attempt-1.md         # parent-captured child's final report
```

`install.sh` distributes bundled skills, references, the `/jiro` command, and the registered `chef` worker directly from root-level `skills/`, `commands/`, and `agents/`. The `.opencode/` example above describes generated artifacts in a target project, not this config-directory checkout. It does not install generated project agents. A generated chef or other specialized agent becomes usable only after OpenCode discovers its definition and advertises its ID; a file write alone is not a successful launch.

## How pstack writes the handoff

pstack's Orchestrate brief names `GOAL`, `SCOPE`, `CONTEXT`, `ACCEPTANCE`, `VERIFY`, `TIMEBOX`, `FORBIDDEN`, `REPORT`, and `STANDING`. Jiro keeps those fields and adds `UNIT`, `WORKDIR`, and `SKILLS`. The filled [handoff contract](../../skills/delegate/references/handoff.md) is saved before dispatch, so a child does not need the parent conversation.

The parent's [run plan](../../skills/delegate/references/run-template.md) records dependencies, owned files and resources, agent and model policy, actual session IDs, worker statuses, parent acceptance, and evidence pointers. Each attempt gets separate brief and report files. The parent alone edits the plan and shared trail. Workers edit only their assigned artifacts.

Reports use `PASS`, `ISSUES`, or `BLOCKED`. A PASS is provisional until the parent inspects the artifact and checks its receipts. Failed checks, absent evidence, and missing coverage never count as passes. Commit checks include exact SHAs and identify tested uncommitted diffs. Measurements include method, sample definition, order, and count.

The [`chef` wrapper](../../agents/chef.md) tells the parent when to select it through its description and loads `jiro` before work. Jiro templates use OpenCode `mode: subagent` and permission rules rather than Cursor-specific fields.

## Related pstack skills and playbooks

These are upstream design references, not additional bundled Jiro capabilities. Sources are recorded in the [pstack source tree](https://github.com/cursor/plugins/tree/ccb5507cec1546dc88135c1139c811e6c59115ba/pstack) and the single [upstream.json](../../upstream.json) catalog.

| Upstream skill or playbook | Delegation role | How it records work | Included here? |
| --- | --- | --- | --- |
| Entry workflow and skill-reading agent wrapper | Choose workflows and route workers through a style wrapper. | Skill and agent Markdown; fresh-task and strict-resume rules. | Adapted as `@jiro` and `chef`. |
| `swarm` | Parallel coverage or races. | Briefs, PASS / ISSUES / BLOCKED receipts, and one aggregate report. | Adapted as `@swarm`. |
| `arena` | Competing artifacts, base selection, and grafting. | Isolated candidates and a synthesis note naming base, grafts, rejections, dropouts, and verification. | No dedicated arena workflow. |
| `architect` | Design through multiple candidates before implementation. | Usage/type sketch or module map, plus a rationale package and synthesis decision. | No. |
| `interrogate` | Independent adversarial reviewers. | Intent, Reviewers, Act On, Consider, Noted, Dismissed, and Agreement Map in one verdict. | No. |
| `figure-it-out` | Design an auditable workflow for an unusual task. | Written phase list, decision trail, and VERIFIED / NOT VERIFIED / INCONCLUSIVE assessments. | No. |
| Multi-phase plan | Prepare a multi-phase or multi-PR program. | Markdown checklist with dependencies, file edits, unit/live/perf checks, review gates, and appendices. | No. |
| Orchestrate | Run a standing multi-day program. | `preferences.md`, `overview.md`, `units.tsv`, `frontier.json`, `ledger.tsv`, `inbox/`, `gates.md`, `decisions.tsv`, and derived `status.md` in the agent store. | Brief, ownership, and evidence patterns only; no runtime or merge automation. |

`create-subagent` and `delegate` are Jiro names for workflows extracted from these patterns, not upstream skills with those names. Their selected sources, license paths, adaptations, and omissions are recorded in [upstream.json](../../upstream.json).

## Orders for the stations

```text
@create-subagent make a project-local read-only accessibility reviewer.
Load our verify-ui skill before reviewing. Do not hardcode a model.

@delegate implement this parser change and add regression tests.
Keep each unit bounded. Inspect the actual diff and test receipts before accepting it.

@swarm inspect each package's public API. One read-only worker per package.
Return one report and show any missing coverage.
```

Models inherit by default. Requested overrides need host authorization and confirmed IDs. Parallel code writers use separate worktrees; artifact writers use separate output directories. Git state, build outputs, mutable fixtures, and ports need isolation too. If isolation is unavailable, serialize writes.

These skills do not authorize commits, pushes, PRs, merges, deploys, global installation, user-data deletion, or external writes. They do not implement Cursor cloud agents, `/loop`, or nested coordinator trees.

## Taste tests

Check packaging without touching real global configuration:

```bash
python3 -m unittest discover -s playbook/delegation/tests -v
python3 playbook/upstream-maintenance/scripts/inventory.py --repo .
```

The [scenario prompts](tests/scenarios.json) describe behavior to exercise in a disposable target repository. Packaging checks are not a live custom-agent discovery test or proof of multi-agent behavior.
