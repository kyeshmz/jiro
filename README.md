# Kstack

Verified engineering workflows for OpenCode. Kstack is the skill pack. Jiro is its coordinating workflow.

Bring Jiro a task. It picks a recipe, gathers the right tools, and verifies the result before serving it. **Recipes** are task playbooks. **Tools** are reusable OpenCode skills. **Chefs** are Jiro's delegated workers. Jiro checks their work and owns the result. The entry skill is `jiro`, the command is `/jiro`, and the registered worker agent is `chef`.

OpenCode supplies the models, tools, permissions, and runtime capabilities. Jiro supplies the cooking instructions.

## Set up the kitchen

Use an existing OpenCode V2 installation. This checkout's sync CLI uses Bun and Commander. Bash and Git are also required for installation and Git hooks. Sync locking works on macOS and Linux without `flock`.

```bash
git clone https://github.com/kyeshmz/kstack.git
cd kstack
bun install
./install.sh
./install.sh --check
```

The installer copies bundled skills and their resources to `${XDG_CONFIG_HOME:-$HOME/.config}/opencode/skills/`. It installs `/jiro`, `/correct`, `/teach`, and `/unslop` wrappers under `commands/` and Chef under `agents/` in the same config directory. Repository-local links are materialized so global copies are self-contained.

One [upstream.json](upstream.json) catalog identifies the source repository, source paths, pinned revisions, licenses, adaptation notes, and preservation rules for every skill and imported recipe. The React bundles' SHA-256 maps are stored in each entry's `fileHashes`. The installer copies this single catalog to the OpenCode config root too. There are no per-skill provenance files.

- Changed or removed owned entries are archived in the neighboring `opencode-jiro-backups/` directory. Repeated syncs do not replace identical files or create another backup.
- Unrelated skills, commands, agents, and settings are preserved. Source definitions are validated before replacing owned entries.
- Unowned custom or symlinked commands are preserved. Use the matching `@skill-id` to load the skill directly in that case. Ownership manifests and generated-wrapper markers identify managed wrappers for upgrade. Recognized upstream-generated wrappers are backed up and replaced with Jiro's versions.
- Separate manifests track skills, commands, and agents. Legacy skill ownership is recognized on upgrade. Owned directories are exact mirrors, including removal of stale resources. `--check` fails when definitions or ownership manifests differ.

Installation does not configure MCP servers, install browser runtimes, register generated project agents, or change model settings. `bun install` installs only this checkout's sync and test dependencies.

This checkout uses OpenCode's configuration-directory layout: `skills/`, `commands/`, and `agents/` live at the root, without a nested `.opencode/` directory. Install it globally to use the definitions in other projects. It does not configure a browser MCP server or download a runtime automatically. See [Browser station](#browser-station).

### Restock

Run these commands from the Kstack checkout.

```bash
git pull
bun install
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

### First use in a repository

`/jiro initialize this repository` creates and proves a repo-specific verification skill by default. The first task that permits edits does the same if no relevant skill exists. Jiro uses the task's actual UI, CLI, API, or library surface, wraps existing harnesses, and writes `.opencode/skills/verify-<app>/` in the target repository. An OpenCode configuration-root repository uses its existing `skills/` directory instead.

Existing relevant skills are reused. An unrelated verification skill does not suppress setup for another surface. Read-only questions and activation without a task do not create files. Say "skip verification skill" to opt out for a task, or put that preference in repository instructions to keep it for the project. Missing tools or credentials are reported as blockers, never as successful proof. The global installer distributes instructions; it does not initialize the repository it happens to run in.

Three focused commands also work without invoking the whole Jiro workflow:

| Command | Use it when |
| --- | --- |
| `/correct` | You keep correcting agents for the same mistakes. Mine scoped history, prevent each class through architecture, types, lint or CI, then tests, and docs last. Keep a rule-to-enforcement table. |
| `/teach` | You want to understand a change or subsystem. Run `how` and `why`, then build one plain explanation diagram by diagram. |
| `/unslop` | You are cleaning up writing. Remove AI tells while preserving meaning, tone, evidence, and justified uncertainty. |

Use `@correct`, `@teach`, or `@unslop` to load the same skills directly. `teach` stays read-only. `correct` changes only the authorized target and proves checks against past mistakes without committing automatically. `unslop` edits files only when requested.

## Recipe book

Jiro follows four steps:

1. **Prep.** Read the repository's instructions, Git state, and relevant existing changes.
2. **Choose a recipe.** Select a [task-specific workflow](skills/jiro/references/recipes.md) and put its steps into a checklist.
3. **Cook.** Gather the tools needed for investigation, implementation, delegation, or verification and follow the recipe.
4. **Taste and serve.** Inspect the result, run relevant checks, and report evidence and remaining gaps.

The recipe book covers investigations, bug fixes, performance, features, refactoring, prototypes, visual parity, skill authoring, evaluations, delegation, PR work, handoffs, and bespoke runs. Read-only orders stay read-only.

Long runs add a local decision trail. User-facing changes are checked through the project's public surface. Compilation and a worker's summary are not proof of behavior.

Jiro and delegation inherit the active model by default. Companion skills may honor existing host-authorized role settings. Overrides require authorization and confirmed model IDs.

Invoking a skill does not authorize commits, pushes, PRs, merges, deployments, global installation, deletion, or unrelated external writes. Jiro is an instruction pack, not a persistent mode, scheduler, cloud-agent runtime, or automatic upstream mirror.

## Tools on the rack

Most skills are explicitly invoked. The local `code-organization`, `minimize-reader-load`, `worktree-cleanup`, `effect`, `react-best-practices`, and `composition-patterns` skills are also advertised for relevant tasks. Jiro loads companions as its workflow requires. `/jiro`, `/correct`, `/teach`, and `/unslop` have bundled slash-command wrappers.

### Jiro tool coverage

The pinned source-coverage map in `upstream.json` accounts for all 55 original source skill IDs. Twenty use existing Jiro equivalents. Thirty-five are newly adapted tools. Existing Jiro, React, Effect, browser, delegation, and cleanup work remains in place. This is an adapted tool pack, not a second competing mode or a byte-for-byte mirror.

Load the imported tools with `@<skill-id>` or the `skill` tool. The full index is [`@kstack-help`](skills/kstack-help/SKILL.md).

| Area | Imported tools |
| --- | --- |
| Design and investigation | [`@architect`](skills/architect/SKILL.md), [`@arena`](skills/arena/SKILL.md), [`@blast-radius`](skills/blast-radius/SKILL.md), [`@figure-it-out`](skills/figure-it-out/SKILL.md), [`@interrogate`](skills/interrogate/SKILL.md), [`@ketchup`](skills/ketchup/SKILL.md), [`@recall`](skills/recall/SKILL.md). |
| Planning and improvement | [`@automate-me`](skills/automate-me/SKILL.md), [`@benchmark-checklist`](skills/benchmark-checklist/SKILL.md), [`@sharpen`](skills/sharpen/SKILL.md), [`@tdd`](skills/tdd/SKILL.md). |
| Verification | [`@create-formal-verification-skill`](skills/create-formal-verification-skill/SKILL.md), [`@maintain-verification-skill`](skills/maintain-verification-skill/SKILL.md). |
| Writing and TypeScript | [`@in-your-own-words`](skills/in-your-own-words/SKILL.md), [`@technical-writing`](skills/technical-writing/SKILL.md), [`@typescript-best-practices`](skills/typescript-best-practices/SKILL.md). |
| Bot controls | [`@make-bot-ui`](skills/make-bot-ui/SKILL.md) uses an existing authorized backend. |
| Pack guidance | [`@kstack-help`](skills/kstack-help/SKILL.md), [`@setup-kstack`](skills/setup-kstack/SKILL.md). |
| Additional principles | Boundary discipline, structural enforcement, design-space exploration, experience first, number validation, context management, idempotency, caller migration, domain modeling, human-independent progress, outcome focus, real-artifact proof, state isolation, verifiable units, behavioral tests, and type discipline. Each retains its `principle-*` ID. |

The old source mode maps to `jiro`, its help maps to `kstack-help`, and model setup maps to `setup-kstack`. Imported tools read the shared writing contract. They use concise, evidence-backed replies, preserve read-only scope, and leave commits, publishing, deployments, global installation, and destructive actions behind explicit authorization gates. Model setup is optional and does not change your choices during installation.

Supporting examples are not proof that a runtime, backend, browser, model, or credential exists. Tests validate coverage, metadata, resource paths, style routing, and installation. Live behavior across every imported workflow remains unverified.

The additional principles are individually available:

- [`@principle-boundary-discipline`](skills/principle-boundary-discipline/SKILL.md) keeps validation at trust boundaries.
- [`@principle-encode-lessons-in-structure`](skills/principle-encode-lessons-in-structure/SKILL.md) replaces repeated instructions with enforcement.
- [`@principle-exhaust-the-design-space`](skills/principle-exhaust-the-design-space/SKILL.md) compares distinct prototypes.
- [`@principle-experience-first`](skills/principle-experience-first/SKILL.md) puts consumer experience ahead of implementation convenience.
- [`@principle-explain-the-number`](skills/principle-explain-the-number/SKILL.md) checks what a measurement actually measures.
- [`@principle-guard-the-context-window`](skills/principle-guard-the-context-window/SKILL.md) bounds inspection and handoffs.
- [`@principle-make-operations-idempotent`](skills/principle-make-operations-idempotent/SKILL.md) makes repeated and interrupted work converge.
- [`@principle-migrate-callers-then-delete-legacy-apis`](skills/principle-migrate-callers-then-delete-legacy-apis/SKILL.md) completes internal API migrations.
- [`@principle-model-the-domain`](skills/principle-model-the-domain/SKILL.md) encodes valid states and ownership.
- [`@principle-never-block-on-the-human`](skills/principle-never-block-on-the-human/SKILL.md) keeps authorized reversible work moving.
- [`@principle-outcome-oriented-execution`](skills/principle-outcome-oriented-execution/SKILL.md) converges on an explicit migration target.
- [`@principle-prove-it-works`](skills/principle-prove-it-works/SKILL.md) checks the real artifact.
- [`@principle-separate-before-serializing-shared-state`](skills/principle-separate-before-serializing-shared-state/SKILL.md) removes shared writers before adding locks.
- [`@principle-sequence-verifiable-units`](skills/principle-sequence-verifiable-units/SKILL.md) ends each unit at an observed check.
- [`@principle-test-behavior-not-implementation`](skills/principle-test-behavior-not-implementation/SKILL.md) tests the consumer's contract.
- [`@principle-type-system-discipline`](skills/principle-type-system-discipline/SKILL.md) makes illegal states harder to represent.

| Tool | Job in the kitchen |
| --- | --- |
| [`@jiro`](skills/jiro/SKILL.md) | Coordinate chefs, choose a recipe, and own the result from prep through verification. |
| [`@how`](skills/how/SKILL.md) | Know the ingredients. Explain architecture, runtime flow, and ownership without edits. |
| [`@why`](skills/why/SKILL.md) | Trace the recipe's origins. Investigate rationale with citations and confidence. |
| [`@correct`](skills/correct/SKILL.md) | Prevent repeated agent mistakes at the highest effective level and pair each rule with enforcement. |
| [`@teach`](skills/teach/SKILL.md) | Combine `how` and `why` into a plain, paced explanation with stepwise diagrams. |
| [`@unslop`](skills/unslop/SKILL.md) | Remove AI writing patterns without changing meaning or evidence-backed uncertainty. |
| [`@show-me-your-work`](skills/show-me-your-work/SKILL.md) | Keep prep notes. Record an append-only decision trail and audit its evidence. |
| [`@no-comments`](skills/no-comments/SKILL.md) | Trim the garnish. Review unnecessary comments, preserve proven exceptions, and fix accepted root causes. |
| [`@principle-laziness-protocol`](skills/principle-laziness-protocol/SKILL.md) | Keep the prep simple. Prefer deletion, flat call paths, one source of truth, and the smallest useful diff. |
| [`@create-verification-skill`](skills/create-verification-skill/SKILL.md) | Build a tasting routine. Generate and prove an app-specific verification recipe. |
| [`@create-subagent`](skills/create-subagent/SKILL.md) | Define a chef. Write a reusable worker or reviewer with permissions and a reporting contract. |
| [`@delegate`](skills/delegate/SKILL.md) | Assign a station. Hand off bounded work and check the returned artifacts. |
| [`@swarm`](skills/swarm/SKILL.md) | Run several stations. Coordinate parallel coverage or competing attempts. |
| [`@playwright-mcp`](skills/playwright-mcp/SKILL.md) | Optional MCP instructions for an explicit request; no server is configured by this pack. |
| [`@playwright-cli`](skills/playwright-cli/SKILL.md) | Make the tasting repeatable. Use named browser sessions and Playwright tests. |
| [`@bro`](skills/bro/SKILL.md) | Restate the last reply in plain, concise language. |
| [`@reflect`](skills/reflect/SKILL.md) | Review the current session through three lenses and propose durable skill edits for approval. |
| [`@code-organization`](skills/code-organization/SKILL.md) | Shape domain ownership, module boundaries, public interfaces, and enforceable constraints. |
| [`@minimize-reader-load`](skills/minimize-reader-load/SKILL.md) | Reduce tracing layers and hidden or mutable state. |
| [`@effect`](skills/effect/SKILL.md) | Guide Effect v4 services, schemas, layers, workflows, and scoped tests. |
| [`@react-best-practices`](skills/react-best-practices/SKILL.md) | Review React performance, data fetching, bundle size, and rendering. |
| [`@composition-patterns`](skills/composition-patterns/SKILL.md) | Design component APIs, compound components, providers, and explicit variants. |
| [`@principle-foundational-thinking`](skills/principle-foundational-thinking/SKILL.md) | Choose core data structures, access patterns, and ownership before logic. |
| [`@principle-redesign-from-first-principles`](skills/principle-redesign-from-first-principles/SKILL.md) | Integrate a requirement as a day-one assumption and deliver incrementally. |
| [`@principle-attack-the-premise`](skills/principle-attack-the-premise/SKILL.md) | Challenge a premise after repeated fixes fail and require a per-actor census. |
| [`@principle-subtract-before-you-add`](skills/principle-subtract-before-you-add/SKILL.md) | Remove confirmed dead weight before building on a simpler base. |
| [`@principle-minimize-reader-load`](skills/principle-minimize-reader-load/SKILL.md) | Preserve the compatibility ID and load the canonical reader-load skill. |
| [`@principle-build-the-lever`](skills/principle-build-the-lever/SKILL.md) | Make non-trivial work repeatable through a small tool or verification artifact. |
| [`@principle-fix-root-causes`](skills/principle-fix-root-causes/SKILL.md) | Reproduce defects, trace their mechanism, and investigate stale state. |
| [`@worktree-cleanup`](skills/worktree-cleanup/SKILL.md) | Audit finished worktrees and remove only approved paths with fresh usage checks. |
| [`@test-audit`](skills/test-audit/SKILL.md) | Gate new tests and prune duplicate or implementation-coupled proof without losing a contract. |

Supporting references and helpers live beside each `SKILL.md`. Resolve them from the loaded skill's base directory. Installing instructions does not supply the tools, credentials, or integrations they describe.

The six core principles are loaded only when their triggers match. The reader-load compatibility entry points share one authoritative body. Effect work checks the target's version and source APIs rather than cloning Effect or assuming OpenCode's test layout.

The React bundles retain WholeEarth Robotics' complete 70-rule performance guide and 8-rule composition guide at revision `abd39e05df96b6ce3524050045b9131eb2fea0b3`, including compiled guides, templates, and metadata. Their content hashes are preserved in `upstream.json`. Check the target's framework version and composition's React 19 gate before applying version-specific advice. Reflection proposes changes before making edits or filing external backlog items.

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

`install.sh` distributes browser instructions, not browser runtimes or MCP configuration. Use the [MCP setup recipe](skills/playwright-mcp/references/setup.md) only if MCP setup is explicitly requested later. The [Playwright guide](playbook/playwright/README.md) covers both interfaces, evidence, and maintenance.

Separate child chats do not imply separate browsers. Verify the resulting state and side effects, not just click success. Preserve evidence after cleanup and close only owned resources. Authentication state, traces, and network logs may contain secrets.

The `playwright-mcp` entry in [upstream.json](upstream.json) documents a historical fixture smoke test before configuration removal, not current availability. Its `playwright-cli` entry records static import validation; live CLI behavior remains untested. Neither establishes full runtime parity.

## Kitchen layout

| Path | Contents |
| --- | --- |
| `skills/` | The tool rack. Skills, references, helpers, licenses, and shared rules. |
| `upstream.json` | The single source-repository catalog, pins, provenance notes, preservation rules, and bundle checksums. |
| `skills/jiro/references/recipes.md` | The recipe book. Task workflows and verification steps. |
| `commands/` | `/jiro`, `/correct`, `/teach`, and `/unslop` wrappers. |
| `agents/` | Registered OpenCode worker definitions, including Chef. |
| `install.sh` | Global skill and command installer. |
| `scripts/sync-opencode.ts` | The Bun and Commander owner of installation, backups, ownership manifests, and hook setup. |
| `scripts/smoke-jiro.ts` | Scoped mode and command invocation smoke check. |
| `playbook/` | New delegation, browser, and upstream-maintenance guides. |
| `recipes/` | Existing authoring, evaluation, refactoring, cleanup, and smoke workflows. |
| `tests/`, `scripts/tests/` | Bun behavior checks and imported Python package checks. |

`agents/chef.md` defines and installs a scoped chef, Jiro's worker agent, under the exact ID `chef`. Each chef loads `jiro` before working and returns its changes with evidence. Routed skills keep their own agent procedures, and Jiro still reviews every artifact. Jiro does not require another mode or skill pack. Its bundled `arena` and `architect` tools are used only when the task calls for them.

Shared writing, comment, and autonomy rules live in `skills/skill.md`. Existing [skill authoring](recipes/authoring-a-skill.md), [evaluation](recipes/eval.md), [refactoring](recipes/refactoring.md), and [cleanup](recipes/worktree-cleanup.md) recipes are bundled through repository-local links. Some standalone recipes use optional unbundled `skill-creator` or `arena` tooling. Report those gaps rather than substituting another pack.

## Taste tests

Run these checks from the repository root. The imported package and inventory checks also require Python 3.9+.

```bash
bun test
bun run typecheck
python3 -m unittest discover -s scripts/tests -v
python3 -m unittest discover -s playbook/delegation/tests -v
python3 -m unittest discover -s playbook/upstream-maintenance/tests -v
bash -n install.sh scripts/worktree-audit.sh
python3 playbook/upstream-maintenance/scripts/inventory.py --repo .
```

Installer tests use disposable fixtures, not your live global configuration. Packaging checks do not prove browser behavior, custom-agent discovery, multi-agent execution, or upstream parity.

### Invocation smoke tests

The existing runners explicitly invoke skills and inspect only their own known sessions. They do not validate automatic selection quality, cross-model review, background delivery, browser performance, or real worktree deletion.

```bash
bun run smoke:mode
python3 scripts/smoke-skills.py --dry-run
python3 scripts/smoke-skills.py --skill minimize-reader-load --timeout 180
```

The mode runner activates `@jiro` through OpenCode's native skill API and verifies the registered `/jiro` template. It confirms the full skill and shared-rule reads. The twenty-case Python runner checks individual local entry points against isolated fixtures. Nine tools covering delegation, comment review, Playwright, correction, teaching, and writing cleanup have packaging checks and scenario material, but no live cases in that runner. `test-audit` has packaging checks only. The three new command scenarios are in [tests/learning-skills.scenarios.json](tests/learning-skills.scenarios.json). Both runners use `opencode/muse-spark-1.3-contributor-free` by default, with no model fallback or user-setting changes. Explicit model options select only the test run's model. Provider rejection is a blocker, not a passing test.

The individual runner's `--dry-run` lists those ten coverage gaps and all 35 newly imported tools as `NOT_RUN`. The source-coverage map supplies the imported IDs without pretending there are live scenarios for them. A full live run stops before invoking OpenCode while those cases are missing. Use `--skill` to select a supported subset; a subset pass is not a full-bundle live pass. The first-use verification scenarios in [tests/first-use-verification.scenarios.json](tests/first-use-verification.scenarios.json) cover initialization, skill reuse, and read-only opt-out behavior. Scenario definitions are not observed agent runs.

Reports retain `summary.json` under `/tmp/opencode/` by default. Transcripts are inspected in memory, fixtures are isolated, and detailed artifacts are retained only when requested. Worktree cleanup is audit-only. Cleanup verifies recorded session IDs, run ownership, unchanged session families, and inactivity before removing disposable sessions. Active, moved, changed, or unverified sessions are held. The mode runner's `--delete-session` and individual runner's `--delete-sessions` are optional cleanup flags, not blanket deletion approval.

### Keep the recipes current

Follow the [upstream-maintenance playbook](playbook/upstream-maintenance/README.md) when changing imported recipes or tools, or reviewing upstream changes. Keep [upstream.json](upstream.json), license files, and preservation rules aligned.

The OC updater follows `kyeshmz/opencode-pstack` as Jiro's upstream engineering source, including native overlays and conversion changes. It adapts those updates to Jiro rather than following Cursor directly or replacing the local workflow. Historical baselines are mapped to port commits or explicitly reviewed; they are not reset to HEAD. React, Effect, test-audit, and the two Playwright sources remain independent. See the [tracking policy](playbook/upstream-maintenance/AUTOMATION.md).

The inventory reads local metadata without fetching or executing upstream code. Add `--base main` to compare against that local ref. Documentation commits and npm runtime versions are separate pins. The cleanup playbook's original source revision remains unknown; its helper's pin does not establish that baseline.

Maintenance is repository-only, not an installed skill. The [automatic updater](playbook/upstream-maintenance/AUTOMATION.md) checks registered upstreams daily and prepares tested draft update PRs through `oc-port-agent`, using an explicit opt-in for named skill folders. MCP configuration remains removed, and proposals require review before merging.

The workflow must be published on the default branch and configured with a reviewed updater commit, model choice, and provider secret before it is active. The import map supplies per-import policies and independent checkpoints for Jiro's engineering, React, Effect, test-audit, and browser sources. No GitHub App backend or automatic merging is configured.

### Clear the counters safely

The read-only audit requires Bash, Python 3.9+, Git, and `du`.

```bash
scripts/worktree-audit.sh /path/to/repository
```

Use `--base <ref>` for a local comparison ref, `--with-prs` for read-only queries through authenticated GitHub CLI, and repeated `--session-export <file>` arguments for explicitly scoped OpenCode exports. The helper does not fetch refs or scan global session storage.

Audit buckets and historical session evidence do not authorize deletion. Read the [cleanup recipe](recipes/worktree-cleanup.md) before removing anything. It requires approval for the exact deletion set and fresh usage checks. In-use worktrees and uncommitted contents are protected. Never delete OpenCode state as cleanup.

## Credits and licenses

The Jiro entry, core companions, delegation workflows, correction, teaching, writing cleanup, and cleanup playbook adapt selected pstack sources and patterns from `cursor/plugins`. They retain upstream MIT notices. The `correct`, `teach`, and `unslop` imports were selected from the OpenCode pstack checkout and checked against upstream revision `ccb5507cec1546dc88135c1139c811e6c59115ba`. `create-subagent` and `delegate` are Jiro-named adaptations, not upstream skills with those names.

The Playwright imports adapt Microsoft's `microsoft/playwright-mcp` documentation and official `microsoft/playwright-cli` skill. They retain Apache-2.0 licenses, Microsoft attribution, and applicable modified-file notices.

Source repositories and adaptation notes are centralized in `upstream.json`. Existing `LICENSE` files and recipe license sidecars remain beside the imported content. Jiro's native recipes, command wrappers, and upstream-maintenance procedure are repository-authored.

The local Effect port retains its OpenCode provenance. The `test-audit` import adapts OpenClaw's `openclaw/openclaw` skill and retains the OpenClaw Foundation MIT notice. The imported React bundles retain their original MIT declarations and author metadata; their source bundles did not include standalone license files. The refactoring and cleanup recipes retain their license and provenance sidecars. Local verification records do not establish full upstream runtime parity.
