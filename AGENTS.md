# Working on Jiro

Preserve unrelated edits. Jiro's discoverable skills, commands, and agents live in `.opencode/`. Shared rules live in `skills/skill.md` and recipes in `recipes/`. The mode bundles these through repository-local links. The installer materializes those links so global OpenCode copies are self-contained. General CLI tooling lives in the top-level `scripts/` directory, not `recipes/`.

## Required local sync

After each completed batch of Jiro changes, run these commands from this checkout before reporting completion or handing off:

```bash
bun test
./install.sh
./install.sh --check
```

Sync uncommitted edits too. A commit or pull is not required. If validation or synchronization fails, report the failure and do not claim that local OpenCode is current. Do not change model settings or unrelated OpenCode configuration as part of sync.

Use Bun and Commander for new CLI tooling. Do not introduce Python tooling. Run `bun install` once before using the sync CLI or its tests.

The installer also installs managed post-commit and post-merge hooks. These sync commits and pulls outside agent sessions. Existing custom hooks are preserved. If a custom hooks path or hook prevents automatic setup, report it and keep running the explicit completion commands above.
