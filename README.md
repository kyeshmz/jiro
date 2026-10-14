# Jiro

Your engineering chef for OpenCode.

Bring Jiro a task. It picks a recipe, gathers the right tools, and verifies the result before serving it. **Recipes** are task playbooks. **Tools** are reusable OpenCode skills. **Sous-chefs** are delegated agents whose work Jiro checks.

OpenCode supplies the models, tools, permissions, and runtime capabilities. Jiro supplies the cooking instructions.

## Set up the kitchen

Use an existing OpenCode V2 installation. The installer requires Bash and Python 3. Git is needed to clone and update the repository.

```bash
git clone https://github.com/kyeshmz/jiro.git
cd jiro
./install.sh
```

The installer copies bundled skills and their resources to `${XDG_CONFIG_HOME:-$HOME/.config}/opencode/skills/`. It installs the `/jiro` wrapper under `commands/` in the same config directory.

- Existing global skills and the command are backed up in the neighboring `opencode-jiro-backups/` directory.
- Unrelated skills and settings are preserved. Same-name pack files are overwritten.
- Custom or symlinked `/jiro` commands are preserved. Use `@jiro` to load the skill directly in that case.
- `jiro-manifest.txt` tracks installed tools. Updates remove vanished skill directories from that manifest. Earlier installation manifests are recognized on upgrade, and existing backups are retained. Copying retained directories is an overlay, not an exact mirror.

Installation does not configure MCP servers, install npm packages or browsers, register generated agents, or change model settings.

You can also open this checkout in OpenCode without installing globally. It does not configure a browser MCP server or download a runtime automatically. See [Browser station](#browser-station).

### Restock

Run these commands from the `jiro` checkout.

```bash
git pull
./install.sh
```

The installer adds an automatic post-merge sync hook when `.git` is a directory and no executable hook exists. It leaves existing executable hooks alone and skips linked worktrees. Rerun `./install.sh` explicitly if the hook is unavailable or your checkout uses a custom hooks path.

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

All skills are explicitly invoked rather than automatically advertised. Jiro can load companions as its workflow requires. Only `/jiro` has a bundled slash-command wrapper.

| Tool | Job in the kitchen |
| --- | --- |
| [`@jiro`](.opencode/skills/jiro/SKILL.md) | The chef. Choose a recipe and own the result from prep through verification. |
| [`@how`](.opencode/skills/how/SKILL.md) | Know the ingredients. Explain architecture, runtime flow, and ownership without edits. |
| [`@why`](.opencode/skills/why/SKILL.md) | Trace the recipe's origins. Investigate rationale with citations and confidence. |
| [`@show-me-your-work`](.opencode/skills/show-me-your-work/SKILL.md) | Keep prep notes. Record an append-only decision trail and audit its evidence. |
| [`@no-comments`](.opencode/skills/no-comments/SKILL.md) | Trim the garnish. Review unnecessary comments, preserve proven exceptions, and fix accepted root causes. |
| [`@principle-laziness-protocol`](.opencode/skills/principle-laziness-protocol/SKILL.md) | Keep the prep simple. Prefer deletion, flat call paths, one source of truth, and the smallest useful diff. |
| [`@create-verification-skill`](.opencode/skills/create-verification-skill/SKILL.md) | Build a tasting routine. Generate and prove an app-specific verification recipe. |
| [`@create-subagent`](.opencode/skills/create-subagent/SKILL.md) | Define a sous-chef. Write a reusable worker or reviewer with permissions and a reporting contract. |
| [`@delegate`](.opencode/skills/delegate/SKILL.md) | Assign a station. Hand off bounded work and check the returned artifacts. |
| [`@swarm`](.opencode/skills/swarm/SKILL.md) | Run several stations. Coordinate parallel coverage or competing attempts. |
| [`@playwright-mcp`](.opencode/skills/playwright-mcp/SKILL.md) | Optional MCP instructions for an explicit request; no server is configured by this pack. |
| [`@playwright-cli`](.opencode/skills/playwright-cli/SKILL.md) | Make the tasting repeatable. Use named browser sessions and Playwright tests. |

Supporting references and helpers live beside each `SKILL.md`. Resolve them from the loaded skill's base directory. Installing instructions does not supply the tools, credentials, or integrations they describe.

`@no-comments` uses an advertised Comment Sicko reviewer when available, or a built-in `general` reviewer with bundled rules. No additional agent installation is required. The reviewer reports candidates; the parent owns accepted edits. Legal headers, public API contracts, and proven external constraints are protected.

### Sous-chefs and prep notes

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
| `playbook/` | Delegation, browser, authoring, evaluation, cleanup, and maintenance guides. |
| `scripts/tests/` | Installer and package checks. |
| `agents/`, `skills/` | Drafts and shared source material outside automatic discovery. |

`agents/chef.md` is an unregistered draft that depends on unbundled `kye-mode`. It is not installed. Jiro does not require an installed pstack pack or bundle its `poteto-mode`, `arena`, or `architect`. Laziness Protocol is the only standalone pstack principle currently imported.

## Taste tests

Run these checks from the repository root. Repository tooling requires Python 3.9+.

```bash
python3 -m unittest discover -s scripts/tests -v
python3 -m unittest discover -s playbook/delegation/tests -v
python3 -m unittest discover -s playbook/upstream-maintenance/tests -v
bash -n install.sh playbook/scripts/worktree-audit.sh
python3 playbook/upstream-maintenance/scripts/inventory.py --repo .
```

Installer tests use disposable fixtures, not your live global configuration. Packaging checks do not prove browser behavior, custom-agent discovery, multi-agent execution, or upstream parity.

### Keep the recipes current

Follow the [upstream-maintenance playbook](playbook/upstream-maintenance/README.md) when changing imported recipes or tools, or reviewing upstream changes. Keep the [import map](playbook/upstream-maintenance/references/import-map.json), provenance, licenses, and preservation rules aligned.

The inventory reads local metadata without fetching or executing upstream code. Add `--base main` to compare against that local ref. Documentation commits and npm runtime versions are separate pins. The cleanup playbook's original source revision remains unknown; its helper's pin does not establish that baseline.

Maintenance is repository-only, not an installed skill. No scheduled workflow or GitHub App backend is configured. The separate `oc-port-agent` protects `.opencode/**`; do not bypass that restriction to maintain these skills.

The repository maintainer tracks both Microsoft sources through per-import upstream overrides. The separate `oc-port-agent` CLI has not been configured or changed for this checkout; the import map is not its tracking policy. Updating skill instructions must not restore the removed MCP server configuration.

### Clear the counters safely

The read-only audit requires Bash, Python 3.9+, Git, and `du`.

```bash
playbook/scripts/worktree-audit.sh /path/to/repository
```

Use `--base <ref>` for a local comparison ref, `--with-prs` for read-only queries through authenticated GitHub CLI, and repeated `--session-export <file>` arguments for explicitly scoped OpenCode exports. The helper does not fetch refs or scan global session storage.

Audit buckets and historical session evidence do not authorize deletion. Read the [cleanup playbook](playbook/worktree-cleanup.md) before removing anything. It requires approval for the exact deletion set and fresh usage checks. In-use worktrees and uncommitted contents are protected. Never delete OpenCode state as cleanup.

## Credits and licenses

The Jiro entry, core companions, delegation workflows, and cleanup playbook adapt selected pstack sources and patterns from `cursor/plugins`. They retain upstream MIT notices. `create-subagent` and `delegate` are Jiro-named adaptations, not upstream skills with those names.

The Playwright imports adapt Microsoft's `microsoft/playwright-mcp` documentation and official `microsoft/playwright-cli` skill. They retain Apache-2.0 licenses, Microsoft attribution, and applicable modified-file notices.

Each adapted skill includes its own `LICENSE` and `UPSTREAM.md`. The cleanup playbook has matching sidecar files. Jiro's native recipes, command wrapper, and upstream-maintenance procedure are repository-authored.
