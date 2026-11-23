---
description: Use, generate, or store a Bitwarden vault secret without leaking it
---

<!-- jiro:command -->
Load the `bitwarden` skill with OpenCode's `skill` tool using `id: "bitwarden"`, the exact ID `bitwarden`. Read it in full and follow it for this task in the current chat. Treat the text below as the request. Check `tools.bitwarden.status()` first and continue only when the vault is unlocked. Never ask for the master password. Return only identifying fields from vault results, and show a secret value only when the request explicitly asks to see it. Ask before deleting, moving, or sharing anything. If no request is supplied, report the vault status and ask what to do.

$ARGUMENTS
