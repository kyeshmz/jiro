# Jiro's browser station

Two tools cover Microsoft's separate browser interfaces:

- [`@playwright-mcp`](../../skills/playwright-mcp/SKILL.md) uses a connected MCP browser for exploration, reproduction, user-flow checks, and snapshots/screenshots.
- [`@playwright-cli`](../../skills/playwright-cli/SKILL.md) imports Microsoft's official CLI skill and references for named browser sessions, Playwright tests, test generation, tracing, video, storage, and request mocking.

The [MCP repository](https://github.com/microsoft/playwright-mcp) recommends [CLI + skills](https://github.com/microsoft/playwright-cli) for coding agents. Its own `.claude/skills/release.md` is a maintainer-release procedure, not a browser automation skill, and is intentionally not imported.

## Setup and installation scope

No MCP server is configured by this pack. The project-only configuration was removed at the user's request; both skills and their maintenance records remain. Use the CLI skill or the project's existing harness by default. Existing global or inherited MCP settings are untouched.

`install.sh` distributes both skills and their references. It does **not** copy MCP configuration, install npm packages, download browsers, or change global OpenCode settings. The retained [setup recipe](../../skills/playwright-mcp/references/setup.md) is opt-in only for an explicit later MCP request. A skill being installed does not mean either browser interface is connected or live-tested.

## Station ownership and evidence

MCP runs retain snapshots, screenshots, relevant console/network excerpts, and receipts under an owned per-run directory such as `artifacts/playwright/<task>/<run>/`. The server's `--output-dir` applies to automatically named files; explicitly named files resolve from the workspace root instead.

CLI commands produce snapshots and session artifacts, normally under `.playwright-cli/`. Test authoring writes a scenario plan, such as `specs/<feature>.plan.md`, and real Playwright spec files with observable assertions. Trace, video, and screenshot paths are included in the final report. Authentication state, traces, and network logs may contain secrets and must not be committed or published casually.

Every CLI worker uses its own named `-s=<task-worker>` session and output directory. A shared MCP connection has shared browser state: child chat IDs do not imply separate contexts. Serialize shared drivers or prove separate MCP instances, profiles, app data, ports, and outputs before fan-out. Close only owned sessions and preserve evidence after teardown.

## Maintenance port list

Both sources are registered in [upstream.json](../../upstream.json):

| Import | Repository | Source selection | Imported revision |
| --- | --- | --- | --- |
| `playwright-mcp` | `microsoft/playwright-mcp` | `README.md`; optional workflow and setup reference only | `b8b4183e099f136cbec0388a6088d4aa2f6b9685` |
| `playwright-cli` | `microsoft/playwright-cli` | `skills/playwright-cli`, including all bundled references | `b85c7a736bb473bf55b584e54a09ffa698d6d871` |

Per-import `upstream` overrides keep these repositories separate from the default `cursor/plugins` source. Each skill carries Apache-2.0 licensing, source provenance, and adaptation/preservation rules. The npm runtime version is a separate pin from the documentation commit. The maintenance inventory reads metadata; it does not fetch upstream, run package code, or prove behavioral parity.

Follow the [maintenance playbook](../upstream-maintenance/README.md) when updating either import. Preserve explicit invocation, V2 config syntax, isolation, authorization gates, evidence capture, and upstream licensing. Check the installed runtime's actual flags and tool schemas rather than blindly copying a newer README.

The repository maintenance procedure reviews both Microsoft repositories. It is not a configured `oc-port-agent` CLI or scheduled updater. Do not restore the removed MCP configuration while updating skills.

## Examples

```text
@playwright-mcp reproduce the settings-save bug on our local app.
Only use an explicitly authorized existing MCP connection; do not set one up.
Use test data, verify persistence after reload, and retain screenshots and errors.

@playwright-cli generate regression tests from the checkout's existing seed test.
Use a named session, write a scenario plan, and run the resulting assertions.

@swarm verify these independent UI scenarios with playwright-cli.
One named browser session, app fixture, and evidence directory per worker.
```

## Taste tests

```bash
python3 -m unittest discover -s scripts/tests -v
python3 -m unittest discover -s playbook/upstream-maintenance/tests -v
python3 playbook/upstream-maintenance/scripts/inventory.py --repo .
```

Packaging/configuration checks and connection status are not an end-to-end browser test. Report the actual live scenarios separately, including any blocked browser or CLI setup.

The [scenario prompts](tests/scenarios.json) cover shared-browser isolation, hostile page instructions, missing CLI setup, and owned-session cleanup. They are evaluation inputs, not claimed passing live runs.
