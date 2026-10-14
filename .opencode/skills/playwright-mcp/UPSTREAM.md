# Upstream source

Adapted from [`README.md`](https://github.com/microsoft/playwright-mcp/blob/b8b4183e099f136cbec0388a6088d4aa2f6b9685/README.md) in `microsoft/playwright-mcp` at `b8b4183e099f136cbec0388a6088d4aa2f6b9685`. The upstream Apache-2.0 license and Microsoft attribution are preserved in [LICENSE](LICENSE). Modified files state that they were adapted for Jiro.

**Take.** Accessibility-snapshot-driven browser automation, current tool discovery, isolated profiles, evidence capture, profile concurrency constraints, and the documented security boundary limitations.

**Adapt.** `playwright-mcp` is an optional Jiro workflow based on the server documentation; that repository does not publish a browser-automation SKILL.md. The official CLI skill is imported separately from `microsoft/playwright-cli`. Use explicit OpenCode skill invocation and current V2 `mcp.servers` configuration when setup is explicitly requested. The retained setup recipe uses headless, isolated mode, disables page WebMCP tools, preserves workspace file-access guardrails, and asks before server-code execution. Verify real user flows, serialize shared browser drivers, preserve evidence, and gate setup and external writes.

**Skip.** Legacy OpenCode configuration, global installation by default, personal browser/profile attachment, insecure flags, broad cleanup, and treating snapshots or tool success as behavioral proof.

The repository's [`.claude/skills/release.md`](https://github.com/microsoft/playwright-mcp/blob/b8b4183e099f136cbec0388a6088d4aa2f6b9685/.claude/skills/release.md) prepares Microsoft package releases and is intentionally not imported as an end-user browser skill. The inspected source tree contained no `NOTICE` file.

**Runtime reference.** The optional setup reference uses npm `@playwright/mcp@0.0.83`, confirmed from the npm registry during this import. This released package version is separate from the source-document commit. Advance either only after its relevant review and verification.

**Local removal.** The user subsequently requested removal of the MCP server for now. The project-only `.opencode/opencode.jsonc` file was removed; skills, licenses, source pins, and historical evidence remain. MCP configuration is no longer an imported target. Do not restore or enable it through maintenance, installation, or ordinary browser verification without an explicit request. No global configuration, npm cache, or browser profile was removed.

OpenCode syntax follows the [V2 MCP guide](https://opencode.ai/v2/docs/mcp-servers) and [skills guide](https://opencode.ai/v2/docs/skills). Packaging/configuration validation is not a live browser test; report runtime verification separately.

**Historical import smoke test, before removal.** `opencode mcp list` reported Playwright connected. An owned in-memory HTML fixture was opened in a separate tab, inspected from its saved accessibility snapshot, and clicked through the advertised `browser_click` tool. The status changed from `Ready` to `Interaction passed`, confirmed in both the resulting snapshot and screenshot. The owned tab was closed and the original blank tab retained. Local evidence remains at `artifacts/playwright-mcp/stack-smoke.png` and the timestamped snapshots beside it; these ignored artifacts are not distributed. This validates the earlier basic interaction and evidence capture, not current server configuration, a real application flow, CLI execution, or full upstream parity.
