---
name: create-subagent
description: Create or update a reusable OpenCode subagent with a clear role, required skills, permissions, and reporting contract. Use for @create-subagent, create a subagent, or make a specialized worker or reviewer. Use delegate for a one-off child session.
license: MIT
metadata:
  opencode/autoinvoke: false
---

# Create a subagent

Write a reusable agent definition, not just a prompt for one child session. Adapt pstack's skill-reading wrapper to the user's role without importing poteto-mode or its unbundled dependencies.

Resolve `references/` from this skill's loaded base directory. Work in the user's target repository, not the installed skill directory.

## 1. Define the role

State what the agent does, when the parent should choose it, whether it may edit, and what it returns. For a one-off task, use the built-in `general` or `explore` agent through `delegate`; no agent file is needed.

Jiro's workers are called chefs. Use the advertised `chef` agent for a one-off Jiro implementation or review task. A reusable Jiro-specific chef must load the exact `jiro` skill before working. Preserve explicit user-chosen IDs for specialized roles and confirm that the host advertises them before launch.

Choose a unique lowercase kebab-case ID. Check existing project and global agents for collisions, including built-in IDs. Preserve an existing definition's location and unrelated instructions when updating it. Do not replace a different role with the same name without the user's approval.

## 2. Choose the location and dependencies

Default to `<target-repository>/.opencode/agents/<agent-id>.md`. Create a global agent only when requested, under `${XDG_CONFIG_HOME:-$HOME/.config}/opencode/agents/<agent-id>.md` after resolving the config directory.

An agent is a Markdown file with `description` and `mode: subagent` frontmatter. Its filename determines its ID. A reusable workflow is a separate `.opencode/skills/<skill-id>/SKILL.md` file with `name` and `description` frontmatter. Do not put agent definitions in `.opencode/skills/` or the repository's draft `agents/` directory.

If the agent must follow a skill, verify that skill exists and include an instruction to load it in full before work. Read its supporting references when the skill requires them. Missing required skills are `BLOCKED`, not permission to skip the wrapper. Jiro chefs load `jiro`; do not replace it with `poteto-mode` or require another unbundled skill unless it is actually available in the target environment.

## 3. Write the definition

Use `references/agent-template.md` for a worker or `references/read-only-agent-template.md` for a reviewer. Fill every placeholder and remove sections that genuinely do not apply.

Keep the reusable role in the agent body. The parent supplies the task-specific goal, working directory, file ownership, constraints, and exact verification commands in each dispatch. This keeps old task details out of later runs.

Default to inheriting the parent model by leaving `model` unset. Set it only when the user requests a model, the host permits the override, and the host's model catalog confirms the exact `providerID/modelID` and optional `#variant`. Do not copy Cursor model aliases or alter global model policy.

Use current OpenCode V2 `permissions` rules with `action`, `resource`, and `effect`. The reviewer template denies edits, shell commands, and child-agent launches. If a reviewer needs a verification command, add a narrow shell exception after the deny rule only when authorized. Review permissions for any external tools it needs too. A prompt saying "read-only" is not a filesystem or network sandbox.

Keep child spawning denied unless the requested role genuinely needs coordination and the host supports it. Do not grant broader permissions to bypass a host restriction.

## 4. Validate and hand back

- Check the frontmatter against the current [OpenCode V2 agents guide](https://opencode.ai/v2/docs/agents).
- Check required skills, reference paths, permissions, and the report format. Leave no template placeholders.
- Confirm the ID is advertised by the host before trying to launch it. Writing a definition does not guarantee it is immediately available in this running session. If absent, report that it needs configuration rediscovery, typically in a new session; do not invent a successful launch.
- When the user also requests a smoke test and the ID is available, launch a fresh child with a harmless bounded task. Inspect its result. Otherwise distinguish file validation from a live test.

Return the file path, agent ID, role, required skills, permission choices, validation performed, and any discovery or test gap. Do not install globally, commit, or push unless requested.
