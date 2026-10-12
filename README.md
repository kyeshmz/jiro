# kstack

OpenCode skills, agent drafts, and playbooks.

## Skills

The project-local skills live under `.opencode/skills/`. They are explicitly invoked rather than automatically advertised.

- `@create-verification-skill` generates an app-specific verification skill and feature map.
- `@show-me-your-work` records an append-only decision trail and audits its evidence.
- `@how` explains architecture, runtime flow, and code ownership.
- `@why` investigates design rationale across available historical sources.

Open this checkout in OpenCode to use the skills. Supporting references and helpers are bundled beside each `SKILL.md`. Resolve their paths from the loaded skill's base directory.

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

The imported skills and cleanup playbook are adapted from the pstack sources in `cursor/plugins` for OpenCode. Each imported skill includes its upstream MIT notice and an `UPSTREAM.md` revision record. The cleanup playbook has matching `worktree-cleanup.LICENSE` and `worktree-cleanup.UPSTREAM.md` files.
