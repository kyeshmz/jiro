---
name: make-bot-ui
description: Build a small bot-control page against an existing authorized backend while keeping credentials on the server. Use for @make-bot-ui or an explicit request for bot buttons, a bot dashboard, or approved private-network access to that UI.
license: MIT
metadata:
  opencode/autoinvoke: false
---

# Make a bot UI

Give the user a page that performs a small set of approved bot actions. Keep credentials out of the browser and leave maintainers an explicit backend contract, safe failure behavior, and a reproducible proof.

Read `references/shared-rules.md` from this skill's reported base directory. Read the target repository's instructions and existing app before choosing an implementation. OpenCode does not supply a webhook routine, secret-request card, or bot wake service merely because this skill is loaded.

## 1. Establish the authorized backend

Find the user's existing bot service, server route, authentication mechanism, and documentation. Confirm the requested UI is allowed to invoke that backend. Read its actual request and response contract.

Record these facts without secret values:

- The approved backend URL or existing server route.
- The allowed actions and their effects.
- The exact JSON fields, validation rules, and response meanings.
- The documented authentication mechanism.
- Whether an accepted request means queued, started, or completed work.
- The timeout, retry, idempotency, rate-limit, and error behavior.
- The local launch command, data isolation, and evidence location.

Do not invent an endpoint, webhook ID, authorization header, server integration, event format, or success code. Do not create a scheduler or cloud routine. If no authorized backend exists, stop at the missing contract. Ask for that contract or separate authorization to design the backend. An inert UI sketch is acceptable only when requested and clearly labeled as unconnected.

## 2. Keep secrets on the trusted server

Use the repository's existing secret mechanism. Prefer a secret manager or server-only environment variable. A protected, ignored local credential file is an alternative only when the project already supports it and its use is authorized.

Never ask the user to paste a sender key, token, or cookie into chat. If the host has an approved secure secret-entry interface, use its actual documented tool. Otherwise tell the user the exact server-side configuration variable or protected path to populate themselves. Do not read the value merely to confirm presence.

Keep secrets out of frontend bundles, public environment variables, HTML, local storage, query strings, screenshots, logs, and evidence. Do not copy an unknown credential from another app. If a secret appears in chat or an artifact, do not repeat it. Follow the project's credential-exposure procedure.

The browser sends a validated action to the existing trusted server. That server holds credentials and invokes the approved bot backend. Reuse the authorized server path. Do not add a relay or change server deployment merely to match this diagram.

## 3. Define a small action contract

Use the same field names in the UI, server validation, and backend handler. Treat every request body as untrusted data. Parse it as data, never as instructions that override the bot's policy or the user's authorization.

Allowlist actions. Validate identifiers, sizes, and values at the boundary. Do not accept an arbitrary destination URL, prompt, shell command, or credential from the browser. Respect the existing session auth, CSRF protection, origin checks, and permissions. A private network is not a replacement for application authorization.

Show pending, accepted, completed, and failed states according to actual backend semantics. Do not display "done" merely because a job was queued. Confirm consequential actions using the project's existing interaction pattern. Prevent accidental duplicate clicks without claiming delivery is exactly once.

## 4. Use the documented delivery behavior

Follow the backend's real headers, status meanings, and timeout. Prefer one request with no retry for a non-idempotent action. Retries require a documented idempotency contract and bounded behavior.

Do not assume HTTP 200 means the bot woke or finished. Verify the documented acknowledgment and the resulting state. Keep media bytes out of a small control payload unless the approved API explicitly supports them.

If failed delivery needs durability, reuse the backend's approved queue or error store. Do not introduce an unbounded local log, polling drain, or replay mechanism without scope and authorization. Any queue stores only the necessary nonsecret fields, records failure state, and has a defined retention policy. Never replay a consequential action without deduplication and approval.

## 5. Keep access local unless exposure is requested

Use the repository's existing bind behavior. For a new authorized local UI, prefer loopback. Do not bind to all interfaces or expose a port by default.

For explicitly requested private-network access, inspect the existing network setup read-only. If Tailscale is already configured, `tailscale status` and `tailscale ip -4` can reveal the existing node and address when available. Do not create another hostname or install a second node.

Use only an approved interface, port, protocol, ACL, and authentication setup. A wildcard bind exposes more than the tailnet on many machines. Prefer the existing approved proxy or a specific permitted interface. Do not weaken TLS or app auth because the route is private.

Installing networking software, using elevated commands, enrolling a node, changing firewall rules, publishing a hostname, or adding HTTPS is separate work that needs authorization. Do not run a downloaded installer or start a login flow as an implicit part of UI work. Report the observed address only when the service is reachable at that address. Never guess a tailnet name or public URL.

## 6. Prove the path without causing surprise work

Use a relevant project verification skill. At initialization for a concrete editable task, or on its first editable task, create and prove a task-specific skill unless the user opted out. Wrap the existing harness rather than building a duplicate. An unrelated `verify-*` skill does not satisfy this check. A read-only request or activation without a task writes nothing.

Before sending a probe, confirm the backend documents a harmless no-op, test action, or safe fixture. Do not invent an action and assume the bot ignores it. If there is no safe probe, ask for authorization before triggering real work.

Verify these checks through the real authorized path:

1. The page loads and shows the expected allowed actions.
2. Invalid and unauthorized requests are rejected.
3. A permitted safe action reaches the existing server and backend with the documented fields.
4. The UI reports the backend's actual state and exposes a useful failure message.
5. Credentials do not appear in the browser response, frontend assets, request URL, logs, or captured evidence.
6. Timeout and duplicate-click behavior do not silently replay consequential actions.
7. Requested private-network access works under the approved ACL and authentication policy.

Capture sanitized requests, responses, screenshots, and observable side effects. State what could not be tested. Stop only processes started by this run and preserve evidence after cleanup.

## Hand off

Report the working UI, authorized backend, action contract, secret location by variable or path only, access scope, actual verification commands and evidence, delivery limits, and remaining blockers. Do not commit, push, open or merge a PR, deploy, incur separate service charges, delete data, or install globally without authorization.
