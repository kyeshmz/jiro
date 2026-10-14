# Jiro

Verified engineering workflows for OpenCode.

Bring Jiro a task. It picks a recipe, gathers the right tools, and verifies the result before serving it. **Recipes** are task playbooks. **Tools** are reusable OpenCode skills. **Chefs** are Jiro's delegated workers. Jiro checks their work and owns the result. The entry skill is `jiro`, the command is `/jiro`, and the registered worker agent is `chef`.

OpenCode supplies the models, tools, permissions, and runtime capabilities. Jiro supplies the cooking instructions.

## Set up the kitchen

Use an existing OpenCode V2 installation. This checkout's sync CLI uses Bun and Commander. Bash, Git, and `flock` are also required for installation and Git hooks.

```bash
git clone https://github.com/kyeshmz/jiro.git
cd jiro
bun install
./install.sh
./install.sh --check
```

The installer copies bundled skills and their resources to `${XDG_CONFIG_HOME:-$HOME/.config}/opencode/skills/`. It installs the `/jiro` wrapper under `commands/` and Chef under `agents/` in the same config directory. Repository-local links are materialized so global copies are self-contained.

- Changed or removed owned entries are archived in the neighboring `opencode-jiro-backups/` directory. Repeated syncs do not replace identical files or create another backup.
- Unrelated skills, commands, agents, and settings are preserved. Source definitions are validated before replacing owned entries.
- Unowned custom or symlinked `/jiro` commands are preserved. Use `@jiro` to load the skill directly in that case. Ownership manifests identify older managed wrappers for upgrade.
- Separate manifests track skills, commands, and agents. Legacy skill ownership is recognized on upgrade. Owned directories are exact mirrors, including removal of stale resources. `--check` fails when definitions or ownership manifests differ.

Installation does not configure MCP servers, install browser runtimes, register generated project agents, or change model settings. `bun install` installs only this checkout's sync and test dependencies.

You can also open this checkout in OpenCode without installing globally. It does not configure a browser MCP server or download a runtime automatically. See [Browser station](#browser-station).

### Restock

Run these commands from the `jiro` checkout.

```bash
git pull
./install.sh
./install.sh --check
```

`bun run sync` and `bun run sync:check` invoke the same installer. Jiro's `AGENTS.md` requires `bun test`, `./install.sh`, and `./install.sh --check` after every completed edit batch, including uncommitted changes.

Managed post-commit and post-merge hooks sync commits and pulls outside agent sessions. Existing custom hooks and `core.hooksPath` are preserved with a warning. No background watcher is installed. Manual edits that do not reach a commit, merge, or agent completion still need `./install.sh`.

## Place an order

Open OpenCode in the repository you want to work on.

```text
/jiro understand this repository and remake the README.

/jiro reproduce the failing save flow, fix the root cause, and verify persistence.

/jiro refactor the parser without changing its public behavior.
```

`@jiro <task>` loads the same entry skill directly. With no supplied task, `/jiro` uses the active conversation or asks what to work on.

## Recipe book

Jiro follows four steps:

1. **Prep.** Read the repository's instructions, Git state, and relevant existing changes.
2. **Choose a recipe.** Select a [task-specific workflow](.opencode/skills/jiro/references/recipes.md) and put its steps into a checklist.
3. **Cook.** Gather the tools needed for investigation, implementation, delegation, or verification and follow the recipe.
4. **Taste and serve.** Inspect the result, run relevant checks, and report evidence and remaining gaps.

The recipe book covers investigations, bug fixes, performance, features, refactoring, prototypes, visual parity, skill authoring, evaluations, delegation, PR work, handoffs, and bespoke runs. Read-only orders stay read-only.

Long runs add a local decision trail. User-facing changes are checked through the project's public surface. Compilation and a worker's summary are not proof of behavior.

Jiro and delegation inherit the active model by default. Companion skills may honor existing host-authorized role settings. Overrides require authorization and confirmed model IDs.

Invoking a skill does not authorize commits, pushes, PRs, merges, deployments, global installation, deletion, or unrelated external writes. Jiro is an instruction pack, not a persistent mode, scheduler, cloud-agent runtime, or full pstack mirror.

## Tools on the rack

Most skills are explicitly invoked. The local `code-organization`, `minimize-reader-load`, `worktree-cleanup`, `effect`, `react-best-practices`, and `composition-patterns` skills are also advertised for relevant tasks. Jiro loads companions as its workflow requires. Only `/jiro` has a bundled slash-command wrapper.

| Tool | Job in the kitchen |
| --- | --- |
| [`@jiro`](.opencode/skills/jiro/SKILL.md) | Coordinate chefs, choose a recipe, and own the result from prep through verification. |
| [`@how`](.opencode/skills/how/SKILL.md) | Know the ingredients. Explain architecture, runtime flow, and ownership without edits. |
| [`@why`](.opencode/skills/why/SKILL.md) | Trace the recipe's origins. Investigate rationale with citations and confidence. |
| [`@show-me-your-work`](.opencode/skills/show-me-your-work/SKILL.md) | Keep prep notes. Record an append-only decision trail and audit its evidence. |
| [`@no-comments`](.opencode/skills/no-comments/SKILL.md) | Trim the garnish. Review unnecessary comments, preserve proven exceptions, and fix accepted root causes. |
| [`@principle-laziness-protocol`](.opencode/skills/principle-laziness-protocol/SKILL.md) | Keep the prep simple. Prefer deletion, flat call paths, one source of truth, and the smallest useful diff. |
| [`@create-verification-skill`](.opencode/skills/create-verification-skill/SKILL.md) | Build a tasting routine. Generate and prove an app-specific verification recipe. |
| [`@create-subagent`](.opencode/skills/create-subagent/SKILL.md) | Define a chef. Write a reusable worker or reviewer with permissions and a reporting contract. |
| [`@delegate`](.opencode/skills/delegate/SKILL.md) | Assign a station. Hand off bounded work and check the returned artifacts. |
| [`@swarm`](.opencode/skills/swarm/SKILL.md) | Run several stations. Coordinate parallel coverage or competing attempts. |
| [`@playwright-mcp`](.opencode/skills/playwright-mcp/SKILL.md) | Optional MCP instructions for an explicit request; no server is configured by this pack. |
| [`@playwright-cli`](.opencode/skills/playwright-cli/SKILL.md) | Make the tasting repeatable. Use named browser sessions and Playwright tests. |
| [`@bro`](.opencode/skills/bro/SKILL.md) | Restate the last reply in plain, concise language. |
| [`@reflect`](.opencode/skills/reflect/SKILL.md) | Review the current session through three lenses and propose durable skill edits for approval. |
| [`@code-organization`](.opencode/skills/code-organization/SKILL.md) | Shape domain ownership, module boundaries, public interfaces, and enforceable constraints. |
| [`@minimize-reader-load`](.opencode/skills/minimize-reader-load/SKILL.md) | Reduce tracing layers and hidden or mutable state. |
| [`@effect`](.opencode/skills/effect/SKILL.md) | Guide Effect v4 services, schemas, layers, workflows, and scoped tests. |
| [`@react-best-practices`](.opencode/skills/react-best-practices/SKILL.md) | Review React performance, data fetching, bundle size, and rendering. |
| [`@composition-patterns`](.opencode/skills/composition-patterns/SKILL.md) | Design component APIs, compound components, providers, and explicit variants. |
| [`@principle-foundational-thinking`](.opencode/skills/principle-foundational-thinking/SKILL.md) | Choose core data structures, access patterns, and ownership before logic. |
| [`@principle-redesign-from-first-principles`](.opencode/skills/principle-redesign-from-first-principles/SKILL.md) | Integrate a requirement as a day-one assumption and deliver incrementally. |
| [`@principle-attack-the-premise`](.opencode/skills/principle-attack-the-premise/SKILL.md) | Challenge a premise after repeated fixes fail and require a per-actor census. |
| [`@principle-subtract-before-you-add`](.opencode/skills/principle-subtract-before-you-add/SKILL.md) | Remove confirmed dead weight before building on a simpler base. |
| [`@principle-minimize-reader-load`](.opencode/skills/principle-minimize-reader-load/SKILL.md) | Preserve the compatibility ID and load the canonical reader-load skill. |
| [`@principle-build-the-lever`](.opencode/skills/principle-build-the-lever/SKILL.md) | Make non-trivial work repeatable through a small tool or verification artifact. |
| [`@principle-fix-root-causes`](.opencode/skills/principle-fix-root-causes/SKILL.md) | Reproduce defects, trace their mechanism, and investigate stale state. |
| [`@worktree-cleanup`](.opencode/skills/worktree-cleanup/SKILL.md) | Audit finished worktrees and remove only approved paths with fresh usage checks. |

Supporting references and helpers live beside each `SKILL.md`. Resolve them from the loaded skill's base directory. Installing instructions does not supply the tools, credentials, or integrations they describe.

The six core principles are loaded only when their triggers match. The reader-load compatibility entry points share one authoritative body. Effect work checks the target's version and source APIs rather than cloning Effect or assuming OpenCode's test layout.

The React bundles retain WholeEarth Robotics' complete 70-rule performance guide and 8-rule composition guide at revision `abd39e05df96b6ce3524050045b9131eb2fea0b3`, including compiled guides, templates, metadata, and content-hash manifests. Check the target's framework version and composition's React 19 gate before applying version-specific advice. Reflection proposes changes before making edits or filing external backlog items.

`@no-comments` uses an advertised Comment Sicko reviewer when available, or a built-in `general` reviewer with bundled rules. No additional agent installation is required. The reviewer reports candidates; the parent owns accepted edits. Legal headers, public API contracts, and proven external constraints are protected.

### Chefs and prep notes

The [delegation guide](playbook/delegation/README.md) covers handoff contracts, ownership, retries, and evidence acceptance.

- Plans, per-attempt briefs, and reports go in `.delegation/<task-slug>/run-<n>/`, or approved host scratch when repository writes are forbidden.
- Reusable agent definitions go in the target project's `.opencode/agents/<id>.md`.
- Verification skills and feature maps go in the target project's `.opencode/skills/verify-<app>/`.
- Decision trails remain local unless committing them is authorized.

The parent owns shared coordination records and checks each child's artifacts. A worker's `PASS` is provisional. Parallel code writers need separate worktrees; artifact writers need private output directories. Git state, fixtures, ports, and browser state also need isolation. Serialize work when isolation is unavailable.

Generated files do not belong in the installed pack. Writing an agent definition does not prove OpenCode has discovered or launched it. A generated verification recipe must be exercised and preserve its evidence after cleanup.

## Browser station

The two Playwright skills use separate interfaces:

| Interface | Runtime requirement | Isolation |
| --- | --- | --- |
| MCP | A connected Playwright MCP server. | Serialize shared drivers unless separate connections and resources are proven. |
| CLI | An existing compatible CLI and browser. Check local help before using imported examples. | Give each worker a unique explicit `-s=<task-worker>` session and private outputs. |

Use the CLI skill or your project's existing browser harness by default. The checkout's MCP server configuration was removed at the user's request. Both instruction skills remain available, but neither enables MCP nor installs a runtime automatically. Existing global or inherited MCP configuration is untouched.

`install.sh` distributes browser instructions, not browser runtimes or MCP configuration. Use the [MCP setup recipe](.opencode/skills/playwright-mcp/references/setup.md) only if MCP setup is explicitly requested later. The [Playwright guide](playbook/playwright/README.md) covers both interfaces, evidence, and maintenance.

Separate child chats do not imply separate browsers. Verify the resulting state and side effects, not just click success. Preserve evidence after cleanup and close only owned resources. Authentication state, traces, and network logs may contain secrets.

The [MCP provenance record](.opencode/skills/playwright-mcp/UPSTREAM.md) documents a historical fixture smoke test before configuration removal, not current availability. The [CLI provenance record](.opencode/skills/playwright-cli/UPSTREAM.md) records static import validation; live CLI behavior remains untested. Neither establishes full runtime parity.

## Kitchen layout

| Path | Contents |
| --- | --- |
| `.opencode/skills/` | The tool rack. Skills, references, helpers, licenses, and provenance. |
| `.opencode/skills/jiro/references/recipes.md` | The recipe book. Task workflows and verification steps. |
| `.opencode/commands/` | The `/jiro` entry wrapper. |
| `install.sh` | Global skill and command installer. |
| `scripts/sync-opencode.ts` | The Bun and Commander owner of installation, backups, ownership manifests, and hook setup. |
| `scripts/smoke-jiro.ts` | Scoped mode and command invocation smoke check. |
| `playbook/` | New delegation, browser, and upstream-maintenance guides. |
| `recipes/` | Existing authoring, evaluation, refactoring, cleanup, and smoke workflows. |
| `tests/`, `scripts/tests/` | Bun behavior checks and imported Python package checks. |
| `agents/`, `skills/` | Chef and shared source material linked into `.opencode/`. |

`agents/chef.md` defines a scoped chef, Jiro's worker agent. `.opencode/agents/chef.md` links to it for discovery and installation under the exact ID `chef`. Each chef loads `jiro` before working and returns its changes with evidence. Routed skills keep their own agent procedures, and Jiro still reviews every artifact. Jiro does not require an installed pstack pack, `poteto-mode`, `arena`, or `architect`.

Shared writing, comment, and autonomy rules live in `skills/skill.md`. Existing [skill authoring](recipes/authoring-a-skill.md), [evaluation](recipes/eval.md), [refactoring](recipes/refactoring.md), and [cleanup](recipes/worktree-cleanup.md) recipes are bundled through repository-local links. Some standalone recipes use optional unbundled `skill-creator` or `arena` tooling. Report those gaps rather than substituting another pack.

## Taste tests

Run these checks from the repository root. The imported package and inventory checks also require Python 3.9+.

```bash
bun test
bun run typecheck
python3 -m unittest discover -s scripts/tests -v
python3 -m unittest discover -s playbook/delegation/tests -v
python3 -m unittest discover -s playbook/upstream-maintenance/tests -v
bash -n install.sh recipes/scripts/worktree-audit.sh
python3 playbook/upstream-maintenance/scripts/inventory.py --repo .
```

Installer tests use disposable fixtures, not your live global configuration. Packaging checks do not prove browser behavior, custom-agent discovery, multi-agent execution, or upstream parity.

### Invocation smoke tests

The existing runners explicitly invoke skills and inspect only their own known sessions. They do not validate automatic selection quality, cross-model review, background delivery, browser performance, or real worktree deletion.

```bash
bun run smoke:mode
python3 recipes/scripts/smoke-skills.py --dry-run
python3 recipes/scripts/smoke-skills.py --skill minimize-reader-load --timeout 180
```

The mode runner activates `@jiro` through OpenCode's native skill API and verifies the registered `/jiro` template. It confirms the full skill and shared-rule reads. The twenty-case Python runner checks individual local entry points against isolated fixtures. The six newly imported delegation, comment-review, and Playwright tools have packaging checks and scenario material, but no live cases in that runner. Both runners use `opencode/muse-spark-1.3-contributor-free` by default, with no model fallback or user-setting changes. Explicit model options select only the test run's model. Provider rejection is a blocker, not a passing test.

The individual runner's `--dry-run` lists those six coverage gaps as `NOT_RUN`. A full live run stops before invoking OpenCode while those cases are missing. Use `--skill` to select a supported subset; a subset pass is not a full-bundle live pass.

Reports retain `summary.json` under `/tmp/opencode/` by default. Transcripts are inspected in memory, fixtures are isolated, and detailed artifacts are retained only when requested. Worktree cleanup is audit-only. Cleanup verifies recorded session IDs, run ownership, unchanged session families, and inactivity before removing disposable sessions. Active, moved, changed, or unverified sessions are held. The mode runner's `--delete-session` and individual runner's `--delete-sessions` are optional cleanup flags, not blanket deletion approval.

### Keep the recipes current

Follow the [upstream-maintenance playbook](playbook/upstream-maintenance/README.md) when changing imported recipes or tools, or reviewing upstream changes. Keep the [import map](playbook/upstream-maintenance/references/import-map.json), provenance, licenses, and preservation rules aligned.

The inventory reads local metadata without fetching or executing upstream code. Add `--base main` to compare against that local ref. Documentation commits and npm runtime versions are separate pins. The cleanup playbook's original source revision remains unknown; its helper's pin does not establish that baseline.

Maintenance is repository-only, not an installed skill. No scheduled workflow or GitHub App backend is configured. The separate `oc-port-agent` protects `.opencode/**`; do not bypass that restriction to maintain these skills.

The repository maintainer tracks both Microsoft sources through per-import upstream overrides. The separate `oc-port-agent` CLI has not been configured or changed for this checkout; the import map is not its tracking policy. Updating skill instructions must not restore the removed MCP server configuration.

### Clear the counters safely

The read-only audit requires Bash, Python 3.9+, Git, and `du`.

```bash
recipes/scripts/worktree-audit.sh /path/to/repository
```

Use `--base <ref>` for a local comparison ref, `--with-prs` for read-only queries through authenticated GitHub CLI, and repeated `--session-export <file>` arguments for explicitly scoped OpenCode exports. The helper does not fetch refs or scan global session storage.

Audit buckets and historical session evidence do not authorize deletion. Read the [cleanup recipe](recipes/worktree-cleanup.md) before removing anything. It requires approval for the exact deletion set and fresh usage checks. In-use worktrees and uncommitted contents are protected. Never delete OpenCode state as cleanup.

## Credits and licenses

The Jiro entry, core companions, delegation workflows, and cleanup playbook adapt selected pstack sources and patterns from `cursor/plugins`. They retain upstream MIT notices. `create-subagent` and `delegate` are Jiro-named adaptations, not upstream skills with those names.

The Playwright imports adapt Microsoft's `microsoft/playwright-mcp` documentation and official `microsoft/playwright-cli` skill. They retain Apache-2.0 licenses, Microsoft attribution, and applicable modified-file notices.

Each adapted skill includes its own `LICENSE` and `UPSTREAM.md`. The cleanup playbook has matching sidecar files. Jiro's native recipes, command wrapper, and upstream-maintenance procedure are repository-authored.

The local Effect port retains its OpenCode provenance. The imported React bundles retain their original MIT declarations and author metadata; their source bundles did not include standalone license files. The refactoring and cleanup recipes retain their license and provenance sidecars. Local verification records do not establish full upstream runtime parity.
