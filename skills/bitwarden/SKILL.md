---
name: bitwarden
description: Use the Bitwarden MCP server to look up, use, generate, and store secrets in the user's Bitwarden vault without leaking them into chat, files, logs, or commits. Use when the user asks for a password, username, TOTP code, API key, secure note, or other credential from Bitwarden, wants a secret saved to or changed in their vault, wants a Bitwarden Send, or when tools.bitwarden calls are about to be made. Also use to install, connect, or unlock the Bitwarden MCP server.
license: MIT
---

# Bitwarden

The `bitwarden` MCP server ([bitwarden/mcp-server](https://github.com/bitwarden/mcp-server)) drives the user's `bw` CLI. Every value a tool returns enters the model context and reaches the model provider. This skill keeps that to the minimum and keeps secrets out of replies, files, logs, and commits.

Read `references/shared-rules.md`. Resolve resources from the loaded skill base.

## 1. Check the server and the vault

The tools live under `tools.bitwarden.*` in Code Mode. Find them with `search({ namespace: "bitwarden" })`. No namespace means the server is not configured or not connected. Go to section 6.

Call `await tools.bitwarden.status()` before anything else. Continue only when `status` is `unlocked`.

- **`unauthenticated`.** The user runs `bw login` in their own terminal.
- **`locked`.** The user runs `bitwarden-mcp unlock` in their own terminal, then reconnects `bitwarden` in `/mcps`. That launcher comes from the dotfiles install in section 6. On a machine with a desktop session, `tools.bitwarden.unlock()` instead opens a native password dialog the model never sees. Under a headless OpenCode service it refuses to run.

Never ask for, accept, or type the master password. Never run `bw login` or `bw unlock` yourself. If the user pastes the master password into chat, do not use it, and tell them it is now in the transcript.

Call `tools.bitwarden.sync()` first when the user says the item changed recently on another device.

## 2. Find the item without reading secrets

`list` returns whole items. That includes `login.password`, `login.totp`, `notes`, card numbers, identity fields, and custom fields. Never return its raw result. Keep only the identifying fields inside the execute block:

```js
const items = await tools.bitwarden.list({ type: "items", search: "github" })
return items.map((item) => ({
  id: item.id,
  name: item.name,
  username: item.login?.username,
  uris: item.login?.uris?.map((entry) => entry.uri),
}))
```

Narrow with `search`, `url`, or `folderid`. When more than one item plausibly matches, show the filtered list and ask which one. Pass the chosen `id` to every later call. A `get` whose search term matches several items fails.

## 3. Use a secret

Choose the first path that fits. Each one puts less into the context than the next.

1. **Inside one execute block.** When the secret is only an input to another Code Mode call or a `fetch`, read it and use it in the same block. Return only the outcome.

   ```js
   const token = await tools.bitwarden.get({ object: "password", id: itemId })
   const response = await fetch("https://api.example.com/me", {
     headers: { Authorization: `Bearer ${token}` },
   })
   return { status: response.status }
   ```

   Never return the value, an object that contains it, or a response body or error that might echo it.

2. **Shell redirection.** When the value must land in a file or one command's environment, read it with `bw` so it never prints. This needs the session file that `bitwarden-mcp unlock` writes. Without that file, use path 3 or ask the user.

   ```sh
   session_file="${XDG_RUNTIME_DIR:-${TMPDIR:-/tmp}}/bitwarden-mcp.session"
   (umask 077 && BW_SESSION="$(cat "$session_file")" bw get password "$item_id" >"$target")
   test -s "$target"
   ```

   Before writing inside a repository, prove the target is ignored with `git check-ignore -q "$target"`. Afterward, do not print, diff, or search the target. For a process, scope the value to one command, as in `API_TOKEN="$(...)" command`. Do not export it into a persistent shell.

3. **Into the reply.** Show a secret only when the user explicitly asks to see that value. Fetch only the needed field with `get` and `object` set to `password`, `username`, `totp`, or `notes`. Never fetch `object: "item"` to read one field. A TOTP code expires within about 30 seconds, so return it right away.

Never type a secret value literally into a command, a file's contents, or a tool argument. It would persist in the transcript. Never send a secret to a commit, PR, issue, log, scheduled prompt, subagent prompt, or another MCP server unless the user named that destination.

## 4. Change the vault

Generate a password and store it in the same execute block, so the new value never returns:

```js
const password = await tools.bitwarden.generate({ length: 32, special: true })
const item = await tools.bitwarden.create_item({
  name: "example.com",
  type: 1,
  login: { username: "user@example.com", password, uris: [{ uri: "https://example.com" }] },
})
return { id: item.id, name: item.name }
```

`create_item` and `edit_item` return the stored item, secrets included. Return only its `id` and `name`.

Creating or editing the item the user asked for is authorized by that request. Confirm the exact item name and `id` before `edit_item`.

Ask before each of these, naming the exact objects:

- **`delete`.** It moves the item to trash, and `restore` brings it back. `permanent: true` cannot be undone. Ask separately for it.
- **`move`.** It shares a personal item into an organization.
- **Any Send.** It shares data outside the vault. Report its URL, expiry, and access limit.
- **`device_approval_*` and `confirm`.** They grant account or organization access.
- **Organization administration.** This covers members, groups, policies, collections, subscriptions, and imports.

File Sends, attachments, and attachment downloads need `BW_ALLOWED_DIRECTORIES` in the server environment. The server rejects every file path without it. Report that rather than working around it.

## 5. Report

Name each item by name and `id`, the operation, and where any secret went. That is a file path, one command, or one request. Never include a secret value unless the user asked to see it. State when a value entered the conversation, and why.

## 6. Install the server

Installation changes global OpenCode configuration. Do it only with explicit authorization.

The `kyeshmz/dotfiles` chezmoi repository installs it through `run_once_after_opencode-bitwarden-mcp.sh` on its `full` profile. That hook installs pinned `@bitwarden/mcp-server` and, outside macOS, a pinned `bw` into `~/.local/share/bitwarden-mcp`. macOS takes `bw` from the Brewfile. The hook registers the server with `opencode mcp add bitwarden --global -- ~/.local/bin/bitwarden-mcp`. That launcher comes from `private_dot_local/bin/executable_bitwarden-mcp` and reads the session from the runtime file. On a machine without chezmoi, copy the launcher to `~/.local/bin/bitwarden-mcp` with mode 755, then run the hook with `sh`.

Otherwise follow the upstream README. Never write `BW_SESSION`, `BW_CLIENT_ID`, or `BW_CLIENT_SECRET` into `opencode.json`. Use `{env:NAME}` substitution or a launcher that reads them at start.

Prove the install. `opencode mcp list` shows `bitwarden` connected, and `tools.bitwarden.status()` returns a status. The organization administration tools also need `BW_CLIENT_ID` and `BW_CLIENT_SECRET` from an organization API key. The dotfiles launcher does not set them.
