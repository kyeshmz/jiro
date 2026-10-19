---
name: setup-kstack
description: Configure only the requested Kstack role models and reasoning budget using authorized host-confirmed choices. Use for @setup-kstack, configure Kstack models, or an explicit request to change role choices. Project-local configuration is the default.
license: MIT
metadata:
  opencode/autoinvoke: false
---

# Set up Kstack role choices

Let the user control model cost and reasoning for the roles they choose. Leave every other setting unchanged. Model setup is optional. Without an authorized role override, workers inherit the parent model.

Read `references/shared-rules.md` from this skill's reported base directory. Read target repository instructions before proposing a destination. This skill writes a plain Markdown role file. It does not install a plugin, change global model settings, or create an automatically applied rule.

## 1. Establish the requested scope

Name the requested roles, target repository, and whether this is a proposal or an approved write. Prefer `<target-repository>/.opencode/instructions/kstack-models.md`.

When the target is itself an OpenCode configuration root, follow its existing top-level `instructions/` layout instead. Do not create a nested `.opencode/` directory against repository guidance.

Use a global role file only when explicitly requested. Resolve the actual OpenCode config directory from the host environment or user instructions. Its usual location is `${XDG_CONFIG_HOME:-$HOME/.config}/opencode/`. The global role file, when requested, is `instructions/kstack-models.md` under that directory.

Do not change `opencode.json`, `opencode.jsonc`, `cli.json`, `AGENTS.md`, provider settings, agent definitions, permissions, or another role file. Do not install or synchronize the pack as a side effect. If existing host instructions name a different role file, report the mismatch. Do not silently migrate it or claim that a new path is already wired into workers.

A request for advice, read-only inspection, or activation without concrete choices writes nothing. Show a proposal and wait for approval before writing.

## 2. Discover exact available models

Use the host's available-models tool or the installed CLI's documented model listing. Read its actual schema or local help before calling it. Discover provider IDs, model IDs, and supported variants. Do not translate another host's slugs or append an effort suffix by guess.

`inherit-parent` and `auto` both mean omit the worker's `model` argument. They are aliases, not provider model IDs. They require no model override. Every other choice requires user authorization and confirmation from the active host catalog. A user-supplied ID alone is not host confirmation.

If discovery is unavailable, retain inheritance or the existing untouched choices. Ask for a way to verify the requested model before writing a new real model ID. Do not substitute a nearby model silently.

## 3. Read and preserve current choices

Read the selected role file if it exists. Read applicable host instructions that govern model overrides. Preserve its budget, role values, comments, and unrelated content unless the user requested their change.

For an absent requested role, propose `inherit-parent`. Missing roles inherit. Unknown or retired role lines remain untouched. Report them separately rather than deleting them during setup.

The supported role vocabulary is retained below so requests map to the right workflow. A listed role does not guarantee that its tool is installed or that the host permits an override.

| Role | Meaning |
| --- | --- |
| `feature, refactoring` | Implementation work for feature and structure changes. |
| `bug-fix` | Bug-fix implementation. |
| `perf-issue` | Performance investigation and implementation. |
| `hillclimb` | Repeated measured optimization. |
| `judgment and prose` | Design judgment, synthesis, and writing. |
| `hardest tasks` | Tasks the user specifically assigns to a stronger model. |
| `how explorer` | Source exploration for mechanics. |
| `how explainer` | Explanation of mechanics. |
| `why investigators` | Source-specific historical investigation. |
| `why synthesizer` | Synthesis of historical findings. |
| `reflect tooling` | Tooling-focused reflection. |
| `reflect judgment, divergent, synthesizer` | Other reflection roles. |
| `arena runners` | A comma-separated list, one candidate per entry. |
| `arena cross-judge pool` | A list from which a permitted judge is chosen. |
| `swarm workers` | Worker default unless an authorized race arm specifies a choice. |
| `architect runners` | A comma-separated panel list. |
| `interrogate reviewers` | A comma-separated reviewer list. |

Read a routed skill before promising its interpretation of these roles. Role configuration does not authorize delegation or make same-model review independent.

## 4. Ask about budget and show the mapping

Use the host's `question` tool when available. Otherwise ask in ordinary text. Name the current budget and requested roles. Present every proposed change with its current value and exact replacement.

Offer these budget preferences when the user wants a budget change:

- `unlimited` requests the highest confirmed reasoning option.
- `large` requests a high reasoning option.
- `medium` requests a balanced confirmed option.
- `small` requests a lower-cost confirmed option.
- Inherit keeps the parent model and reasoning behavior.

These are preferences, not portable provider variants. Map them only to variants the host actually confirms. Explain when a model offers no matching option. Do not claim a cost or speed improvement without measurement. Do not lower or raise unrequested roles to make the table uniform.

Panel list entries determine the number of workers in workflows that use that contract. Alias entries still count. A judge pool supplies a choice, not a worker per entry. A shorter panel can reduce calls, but a role file alone does not launch anything.

Wait for approval of the destination, requested role mapping, and any budget change. Revalidate each real model and variant immediately before writing.

## 5. Write only approved role settings

Use plain Markdown. Keep one line per requested role, with comma-separated panel entries where needed. Update existing requested lines in place. Do not rewrite the whole file or add untouched roles just to match a template.

This example shows the format, not a mandatory full-file output:

```text
# Kstack model configuration
# budget: inherit parent
feature, refactoring: inherit-parent
bug-fix: inherit-parent
how explorer: inherit-parent
arena runners: inherit-parent, inherit-parent
arena cross-judge pool: inherit-parent, inherit-parent
swarm workers: inherit-parent
```

Use exact host-confirmed model references for approved non-alias choices. Keep reasoning metadata in the existing file format or the host's documented reference syntax. Do not invent a variant suffix.

Read the result back and compare the scoped diff. Confirm that only the approved roles and budget changed. A rerun with identical choices must make no change.

## 6. Report the explicit read contract

Report the exact absolute path written. Tell the coordinator to pass that path to every relevant worker and require an explicit read before selecting its model. For example, say "Read `/absolute/project/.opencode/instructions/kstack-models.md` for the requested role. Omit `model` for an absent role, `auto`, or `inherit-parent`."

Replace the example with the actual written path in the handoff. Do not leave a placeholder in a worker prompt. Do not assume a file name, plugin, session refresh, or configuration loader makes a plain role file take effect. Report consumers that still read another path as an integration gap. Changing their instructions is separate authorized work.

## 7. Keep verification task-specific

On explicit repository initialization, or on the first editable task, follow Jiro's Repository verification setup and create and prove a task-specific verification skill by default unless the user opts out. Initialization without another task uses the primary documented surface. Reuse a relevant existing skill. Wrap the repository's existing harness rather than duplicating it. A `verify-*` skill for another feature or surface does not suppress this work.

Use `create-verification-skill` for behavioral proof. Formal verification remains an explicitly selected workflow through `create-formal-verification-skill`. Write generated project skills to `<target-repository>/.opencode/skills/<skill-id>/SKILL.md`. For an OpenCode configuration-root repository, follow its existing top-level `skills/` layout instead of nesting another `.opencode/` directory.

A configuration-only question, read-only setup proposal, or activation without a project task does not create a verification skill. Report missing tools or credentials as blockers. Do not claim an unexecuted generated skill is proved. Do not commit, push, open or merge a PR, deploy, delete data, incur separate service charges, or install globally without authorization.
