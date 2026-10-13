# kstack

OpenCode skills, agent drafts, and playbooks.

## Skills

The project-local skills live under `.opencode/skills/`. They are explicitly invoked rather than automatically advertised.

- `@create-verification-skill` generates an app-specific verification skill and feature map.
- `@show-me-your-work` records an append-only decision trail and audits its evidence.
- `@how` explains architecture, runtime flow, and code ownership.
- `@why` investigates design rationale across available historical sources.
- `@maintain-upstream` reviews upstream changes and updates which functionality Jiro takes, skips, and preserves as its imported skills and playbooks evolve.

Open this checkout in OpenCode to use the skills. Supporting references and helpers are bundled beside each `SKILL.md`. Resolve their paths from the loaded skill's base directory.

## Upstream maintenance

Run `@maintain-upstream` after changing an imported skill or playbook, adding or removing an import, or asking to bring in changes from `cursor/plugins`. It reviews both the upstream diff and Jiro's current adaptations. It keeps the import map, per-file source revisions, licensing, and take/skip decisions together rather than replacing Jiro with an upstream copy.

The skill covers `create-verification-skill`, `how`, `show-me-your-work`, `why`, and the cleanup playbook with its audit helpers. Its [import map](.opencode/skills/maintain-upstream/references/import-map.json) records the current scope and Jiro-specific preservation rules. Update that map in the same change when the import scope or intended adaptations change. New Jiro-native skills are not upstream imports unless explicitly registered.

Inspect the inventory without fetching upstream, executing its code, or changing files:

```bash
python3 .opencode/skills/maintain-upstream/scripts/inventory.py --repo .
python3 .opencode/skills/maintain-upstream/scripts/inventory.py --repo . --base main
```

The inventory flags unregistered imports, missing files, changed target paths, and unknown source pins. The cleanup playbook currently has an unpinned source link. Its helper's recorded revision does not establish the playbook's revision.

Maintenance is explicit. This skill does not install a scheduled workflow, configure the GitHub App backend, run a paid model, or publish or merge changes automatically. The separate [oc-port-agent](https://github.com/kyeshmz/oc-port-agent) CLI deliberately protects `.opencode/**`; do not bypass that restriction to maintain these skills.

## Shared rules and drafts

- `skills/skill.md` contains shared writing, comment, and autonomy rules.
- `agents/chef.md` is a subagent draft that routes to `kye-mode`.
- `playbook/` contains skill-authoring, evaluation, and worktree-cleanup workflows.

The top-level `skills/` and `agents/` directories are source material, not OpenCode's automatic discovery locations. Chef is not registered as an OpenCode agent yet. Chef and some playbooks refer to skills not bundled here, including `kye-mode`, `arena`, and `principle-*` skills.

## Worktree audit

The audit requires Bash, Python 3.9+, and Git. It is read-only and does not authorize deletion.

```bash
playbook/scripts/worktree-audit.sh /path/to/repository
```

Use `--base <ref>` to select a local comparison ref. Use `--with-prs` to enable a read-only PR query through an authenticated GitHub CLI. Use repeated `--session-export <file>` arguments to supply explicitly scoped OpenCode session exports. Missing session evidence remains unverified.

Read `playbook/worktree-cleanup.md` before any cleanup. The playbook requires approval for the exact deletion set and protects in-use worktrees and uncommitted data.

## Sources and licensing

The four imported skills and cleanup playbook are adapted from the pstack sources in `cursor/plugins` for OpenCode. Each imported skill includes its upstream MIT notice and an `UPSTREAM.md` revision record. The cleanup playbook has matching `worktree-cleanup.LICENSE` and `worktree-cleanup.UPSTREAM.md` files. `maintain-upstream` is Jiro-native, not an imported pstack skill.
