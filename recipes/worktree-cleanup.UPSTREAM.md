# Upstream source

Adapted from the [pstack worktree-cleanup workflow](https://raw.githubusercontent.com/cursor/plugins/main/pstack/skills/poteto-mode/playbooks/worktree-cleanup.md) and [worktree-audit helper](https://raw.githubusercontent.com/cursor/plugins/11713c683fe4add4fd403ea880580abbc9e0875f/pstack/skills/poteto-mode/scripts/worktree-audit.sh) in `cursor/plugins`.

The source revision used for the bundled helper is `11713c683fe4add4fd403ea880580abbc9e0875f`. The upstream MIT notice is preserved in [worktree-cleanup.LICENSE](worktree-cleanup.LICENSE) for the imported recipe and its adapted helpers.

The port uses explicitly supplied OpenCode session exports. It does not scan global chats or delete OpenCode state. Untracked and ignored files require review and scoped approval. Removal is non-forced by default. The helper uses NUL-delimited Git paths, local refs only, and an optional read-only PR query. Historical session matches never authorize deletion.

OpenCode session access follows the [V2 session API](https://opencode.ai/v2/docs/api).
