---
name: create-verification-skill
description: Generate a project-local verification skill that drives your app the way a user does, for any language, framework, or platform. Use when explicitly invoked as @create-verification-skill, when asked to make a control skill for a repo, or when a project has no scripted way to prove UI, CLI, or service behavior.
license: MIT
metadata:
  opencode/autoinvoke: false
---

# Create a verification skill

Every serious project needs a scripted way to drive the real app and prove behavior. Launch it, exercise a feature the way a user would, and capture evidence. This skill generates a project-local skill at `.opencode/skills/verify-<app>/` tailored to the repo. Write the output for the next agent, not for a human. It will be read cold, mid-task, by an agent that has never seen the app.

OpenCode loads skills through the `skill` tool using the exact skill ID. Supporting files are not loaded automatically. Resolve bundled references relative to this skill's base directory. Write generated files into the target repository, not into this generator's directory or a global installation.

Jiro calls this tool by default during repository initialization or the first editable task without a relevant verification skill. Reuse a matching skill and preserve custom helpers instead of regenerating them. Existing tests are a driver to wrap, not a reason to omit the skill. Follow the task's surface rather than choosing an unrelated app in the same repository. Honor explicit opt-outs and read-only scope. When the target is itself an OpenCode configuration root, use its existing `skills/verify-<app>/` directory instead of creating a nested `.opencode/` directory.

## 1. Interview the repo, not the user

Answer these from the codebase and only ask the user what you cannot observe:

- **Surface.** What does a user actually touch? A web UI, a CLI/TUI, a desktop app, an API, a mobile app, a library? A repo can have several. Pick the surface the active task touches, or the primary documented surface for initialization, and note the rest.
- **Run.** How does the app start locally? Prefer the repo's own documented dev command from package scripts, a Makefile, or the README quickstart. Note ports, env vars, seed data, and auth.
- **Drive.** How can an agent interact with it programmatically? Prefer existing harnesses such as Playwright/Cypress specs, expect scripts, PTY helpers, curl-able endpoints, or a debug port. Only then pick a generic recipe. Use browser/CDP for web and Electron, a tmux/PTY harness for CLI/TUI, or plain HTTP for services. Confirm the chosen harness is available in the active OpenCode session or through the repo's own commands. Do not assume an MCP integration is installed.
- **Observe.** What evidence can be captured? Screenshots, terminal transcripts, response bodies, logs, exit codes, and DB state.
- **Isolate.** Can two instances run side by side using separate ports, data dirs, and profiles? If not, say so in the generated skill. Refuse to double-drive a shared instance.

If the checkout does not build or start as-is, fix that first within the requested scope or report the blocker precisely before generating. A skill written against a broken base teaches wrong steps. When an irrelevant missing asset blocks startup, such as a static dir the API never serves or a sample config, the generated skill may create it. Mark it as verification scaffolding and remove it in cleanup.

## 2. Generate the skill

Write `.opencode/skills/verify-<app>/SKILL.md` with YAML frontmatter. Set `name: verify-<app>` and a `description` that names the app, the surface, and when to reach for it. Match the skill ID to the directory name. Include a description so OpenCode advertises the generated skill.

Include these sections, each grounded in what the interview actually found. Leave no placeholders in the generated output:

- **Launch.** Give the exact command that starts the app for verification and how to tell it is ready. Use a log line, a port answering, or a prompt. Include teardown. For a short-lived CLI or TUI there is no server to keep alive. Build the binary or install deps once, then start each drive in its own isolated PTY or tmux session.
- **Doctor.** Give one read-only check that answers whether this instance is worth driving. Check the process, version/build, port ownership, and auth as applicable. An agent runs this first whenever anything looks off.
- **Drive.** Give the harness recipe with real selectors and commands from this repo, not examples. Prefer stable handles such as ARIA labels, data attributes, prompt strings, and route paths over coordinates and tab order.
- **Evidence.** State what to capture for a proof and where it goes. Exercise the real user path, not internal setters or test-only endpoints. Capture the action and the resulting state, not just the final screen. Verify side effects such as files written, rows inserted, and messages sent alongside what is visible. Use mocks only where a production boundary already isolates the external system. When the safe path is a dry-run or test mode, verify what it actually skips by observing files, network activity, and git refs. Do not trust its name. Some dry-runs still touch the network or open a browser.
- **Cleanup.** Explain how to tear down instances the run created. Never kill by process name. Kill what you started. Cleanup removes instances and scratch state, never the evidence. Proof artifacts survive teardown in a location the skill names.
- **Helpers.** Make every script the skill ships executable and show its invocation in the skill body. A helper the reader has to reverse-engineer is not a helper.

## 3. Seed the feature map

Create `.opencode/skills/verify-<app>/features/README.md` plus one file per relevant user-facing feature you can identify on the selected surface. Aim for the top 3-5 to start when that many exist, from routes, commands, menus, or docs. Do not invent features to meet a count or expand into unrelated applications. Follow the shape in [`references/feature-map-example/`](references/feature-map-example/), with a README index and one file per feature. These are structural examples, not runnable commands for the target app. Replace their app names, commands, selectors, and paths with what the repo actually provides.

Each file answers, from the user's point of view, what the feature is, how to reach it, how to drive it with the harness, and what observable end state proves it works. Use these four H2s in order:

1. `Sub-features`.
2. `How to get to it (user POV)`.
3. `Driving it with <harness>`.
4. `Gotchas`.

The map is the repo's maintained verification source. A proof that drives one convenient entry point is incomplete when the map lists others.

## 4. Prove the generated skill before handing it over

Run its own instructions end to end once. Launch, doctor, drive one mapped feature, capture evidence, and clean up. One feature is enough for this initial proof. The map exists so later runs can cover the rest.

After cleanup, confirm the evidence still exists at the named location. A cleanup that eats the proof fails this step. Fix what fails and run the generated cleanup after every failed iteration too. Do not strand processes and ports. A generated skill that was never executed is a draft, not a deliverable.

## 5. Offer the maintenance loop

If `maintain-verification-skill` is available, point the user at `@maintain-verification-skill` in OpenCode for keeping the map honest as the app changes. Otherwise, explain that the feature map must be updated when user paths, harness commands, or proof requirements change. Do not claim a maintenance skill is installed when it is not. Suggest a cadence only if they ask.
