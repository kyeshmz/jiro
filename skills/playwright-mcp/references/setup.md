# OpenCode setup

Modified for Jiro from the Microsoft Playwright MCP README. No MCP server is configured by this pack. This recipe is opt-in only when the user explicitly requests MCP setup; do not apply it during ordinary browser verification or upstream maintenance. Node.js 18+ and an available supported browser are required. The example uses the previously reviewed runtime `@playwright/mcp@0.0.83`; the documentation source revision is recorded separately in Jiro's [upstream.json](../../../upstream.json).

Check the target project's existing `.opencode/opencode.json(c)` or `opencode.json(c)` before changing it. OpenCode V2 servers live under `mcp.servers`, not directly under `mcp`. Use the current [V2 MCP guide](https://opencode.ai/v2/docs/mcp-servers) as the source of truth; Microsoft's README also contains a legacy OpenCode example.

When the user asks for project setup, add the local server from that target directory:

```bash
opencode mcp add playwright -- npx -y @playwright/mcp@0.0.83 --headless --isolated --no-webmcp --output-dir artifacts/playwright-mcp
opencode mcp list
```

Do not pass `--global` unless global setup was requested. Do not overwrite an existing `playwright` entry without inspecting its role and preserving needed settings. The checkout's former server configuration was removed at the user's request; `install.sh` copies skills and the Jiro command, not MCP configuration or npm packages. Existing global or inherited server settings are not removed by deleting a project entry.

The CLI command adds the server only. Before using it, also merge the `permissions` rule below into the target project's existing configuration. Preserve unrelated rules and place this rule after any broader `playwright_*` allow rule, because the last matching rule wins. This enforces approval for server-code execution rather than relying only on prose. Do not append a later broad allow rule that cancels the gate.

The equivalent V2 server object is:

```json
{
  "$schema": "https://opencode.ai/config.json",
  "mcp": {
    "servers": {
      "playwright": {
        "type": "local",
        "command": ["npx", "-y", "@playwright/mcp@0.0.83", "--headless", "--isolated", "--no-webmcp", "--output-dir", "artifacts/playwright-mcp"],
        "cwd": ".",
        "timeout": {"startup": 60000}
      }
    }
  },
  "permissions": [
    {"action": "playwright_browser_run_code*", "resource": "*", "effect": "ask"}
  ]
}
```

`npx` resolves the released package when OpenCode starts the server. First use can download it into the npm cache; the config alone does not prove installation or browser availability. If startup fails, inspect the actual error, Node/browser availability, and connection state. Do not silently change package versions, add insecure flags, or delete user profiles to repair startup.

## Profile and worker isolation

- `--isolated` keeps the profile in memory. Closing the browser loses that context's cookies and storage.
- Separate clients sharing a persistent workspace profile can conflict. Separate named CLI sessions or separately connected isolated MCP instances are safer for concurrent workers.
- Separate child chat IDs alone do not prove separate MCP browser contexts. A shared connection, selected tab, output directory, or app data store is a shared mutable resource.
- Loading existing `--storage-state`, persistent profiles, browser extensions, or CDP sessions requires authorization. Authentication state may contain reusable credentials.
- Origin and workspace-access settings are guardrails, not security boundaries. Retain the browser sandbox and host permissions.

## Runtime vs maintenance pins

The npm version is a runtime dependency. `upstream.json` pins the documentation source commit separately. Review the runtime version and documentation pin when updating: compare the selected source paths, confirm the released package's flags and tool schemas, and run an isolated smoke test. Do not advance the source pin merely because `latest` changed.
