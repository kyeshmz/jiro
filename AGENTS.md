# Working on Jiro

Preserve unrelated edits. This repository is an OpenCode configuration directory: skills, commands, and agents live directly in `skills/`, `commands/`, and `agents/`. Do not create a nested `.opencode/` directory here. Shared rules live in `skills/skill.md` and recipes in `recipes/`. The mode bundles these through repository-local links. The installer materializes those links so global OpenCode copies are self-contained. General CLI tooling lives in the top-level `scripts/` directory, not `recipes/`.

`upstream.json` is the only provenance catalog. Keep each import's repository, source pins, adaptation notes, preservation rules, and any bundle checksums there. Do not create per-skill provenance records or checksum manifests. Preserve license files and upstream author metadata beside the content they cover. Inventory checks enforce skill coverage, source identity, and checksums.

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
