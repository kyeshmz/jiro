# kstack

OpenCode skills, agent drafts, and playbooks.

## Skills

The project-local skills live under `.opencode/skills/`. They are explicitly invoked rather than automatically advertised.

- `@create-verification-skill` generates an app-specific verification skill and feature map.
- `@show-me-your-work` records an append-only decision trail and audits its evidence.
- `@how` explains architecture, runtime flow, and code ownership.
- `@why` investigates design rationale across available historical sources.

Open this checkout in OpenCode to use the skills. Supporting references and helpers are bundled beside each `SKILL.md`. Resolve their paths from the loaded skill's base directory.

## Repository maintenance

Upstream maintenance is internal to this repository. Follow the [maintenance playbook](playbook/upstream-maintenance/README.md) after changing an imported skill or playbook, adding or removing an import, or reviewing changes from `cursor/plugins`. Keep what Jiro takes, skips, and preserves aligned with its current adaptations.

The [import map](playbook/upstream-maintenance/references/import-map.json) covers the four imported skills and cleanup playbook. Update it with provenance records when the import scope or preservation rules change. New Jiro-native skills are not upstream imports unless explicitly registered.

Inspect the inventory without fetching upstream, executing its code, or changing files:

```bash
python3 playbook/upstream-maintenance/scripts/inventory.py --repo .
python3 playbook/upstream-maintenance/scripts/inventory.py --repo . --base main
```

The inventory flags unregistered imports, missing files, changed target paths, and unknown source pins. The cleanup playbook currently has an unpinned source link. Its helper's recorded revision does not establish the playbook's revision.

These maintenance files are repository-only tooling, not an OpenCode skill or an installed user feature. `install.sh` does not copy them. No scheduled workflow or GitHub App backend is configured. The separate [oc-port-agent](https://github.com/kyeshmz/oc-port-agent) CLI deliberately protects `.opencode/**`; do not bypass that restriction to maintain these skills.

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

The four imported skills and cleanup playbook are adapted from the pstack sources in `cursor/plugins` for OpenCode. Each imported skill includes its upstream MIT notice and an `UPSTREAM.md` revision record. The cleanup playbook has matching `worktree-cleanup.LICENSE` and `worktree-cleanup.UPSTREAM.md` files. The upstream-maintenance playbook is repository-authored tooling, not part of the installed skill bundle.
