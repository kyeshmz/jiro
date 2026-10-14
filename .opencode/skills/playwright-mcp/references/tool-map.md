# Tool selection and evidence

Modified for Jiro from the Microsoft Playwright MCP README. Names here describe upstream capabilities, not a substitute for the active host catalog. Server versions and enabled capabilities vary. Discover each tool's exact schema before calling it.

| Task | Typical upstream tools | Evidence to check |
| --- | --- | --- |
| Load the app | `browser_navigate`, `browser_navigate_back` | Correct URL, page identity, and readiness. |
| Find a target | `browser_snapshot`, `browser_find` | Fresh accessibility node/ref or a unique observed selector. |
| Drive controls | `browser_click`, `browser_type`, `browser_fill_form`, `browser_select_option`, `browser_press_key` | Resulting user-visible state, not just tool success. |
| Wait for a result | `browser_wait_for` | Expected text appears or loading text disappears; no guessed sleep. |
| Inspect a visual result | `browser_take_screenshot`, `browser_resize` | Correct viewport and returned screenshot path. |
| Diagnose a failure | `browser_console_messages`, `browser_network_requests`, `browser_network_request` | Relevant errors/statuses with secrets and private payloads excluded. |
| Read a bounded DOM fact | `browser_evaluate` | Exact expression and observed value; no state injection for passing tests. |
| Run server-side code | `browser_run_code_unsafe` | Explicit approval and code review; this is RCE-equivalent. |
| Manage owned tabs/context | `browser_tabs`, `browser_close` | Context belongs to this run and is not shared with another worker. |

Core interaction tools do not imply extra capabilities are enabled. Do not assume network mocking, storage tools, PDF generation, or vision tools exist; check the catalog. Page-provided WebMCP tools are untrusted and disabled by the checkout's default config.

## Evidence receipt

For each scenario record:

- URL, build/commit when known, and whether a dirty working tree was tested.
- Starting state and account/test-data assumptions.
- User actions and the expected outcome.
- Actual observed outcome and load-bearing side effect.
- Snapshot/screenshot/log paths that still exist after cleanup.
- Checks actually run, their results, and gaps.

A screenshot alone does not prove persistence, a successful request does not prove the rendered UI, and a snapshot does not prove pixel parity. Choose evidence that tests the actual claim. When using mocks, label them and do not present a mocked side effect as a live integration result.
