---
name: kstack-help
description: Explain Kstack setup, Jiro recipes, tool selection, verification, model choices, and recovery from a drifting run. Use for @kstack-help or an explicit question about how to use this pack without starting the work.
license: MIT
metadata:
  opencode/autoinvoke: false
---

# Kstack help

Answer the question, give one usable prompt, and link the file that supports the answer. A help question does not start implementation, delegation, installation, or a provider run. The user decides whether to send the suggested prompt.

Read `references/shared-rules.md` from this skill's reported base directory. Resolve every bundled reference from that directory, not the shell's working directory. Read the routed skill before recommending its details. Its current instructions own the workflow when this index disagrees.

A direct work request is different. For "use Jiro to fix this bug", load `jiro` and carry out the authorized task. Do not keep answering help when the user has asked for work.

## Find the actual need

Infer the need from the conversation. A named question such as "which tool reviews a PR?" goes straight to that route. If the need is still unclear, ask one question with these choices:

- Get set up.
- Start a task with Jiro.
- Pick a tool for a situation.
- Fix a run that went wrong.
- Adapt the workflow.

Answer only the selected area. Inspect state only when it changes the answer. Missing role configuration means inheritance, not an undisclosed pack default. Missing verification for the task means there is no proven task-specific driving recipe yet. An unrelated `verify-*` directory is not proof of coverage.

When setup or cost matters, offer `@setup-kstack` at most once in the conversation. It is optional. It proposes only requested role changes and waits for approval. Declining it keeps the parent model. Do not turn a help answer into configuration writes.

## Get set up

Read the bundled [setup guide](references/setup.md). If the user supplied a source checkout, read its current README before running an installation. Kstack is an OpenCode pack. Jiro is its coordinating workflow. Runtime tools, browsers, credentials, and backend integrations come from the host or project, not from skill Markdown.

Installation and role configuration are separate actions. Do not install globally, edit settings, or run the checkout's sync commands from a help question. When the user requests installation, follow the actual repository instructions and preserve unrelated OpenCode configuration.

Use `@setup-kstack` only if the user wants to choose role models or reasoning preferences. It prefers a project-local plain Markdown role file. The coordinator and workers must read its exact reported path explicitly. It does not depend on an automatic configuration loader or an always-applied rule.

Cost comes from actual provider calls, reasoning, worker count, and repeated proof. Inherit the parent model unless an override is authorized and host-confirmed. A panel list usually creates one worker per entry. A judge pool instead supplies a selection. Shorten unnecessary panels or choose confirmed lower-cost models when appropriate. Do not promise savings without measurements.

## Start a task with Jiro

Read [Jiro](../jiro/SKILL.md) and its [recipe book](../jiro/references/recipes.md). Give it a goal, a pass-or-fail done check, evidence to show, and real constraints. Jiro picks the recipe and copies its steps into the task checklist. Skipped steps retain their reasons.

Read [references/prompting.md](references/prompting.md) before helping word a task. Use [references/recipes.md](references/recipes.md) for examples. Do not hand-write a long sequence of skills when the recipe already supplies the order. Name a skill only to override a particular choice.

`@jiro` loads the entry skill. `/jiro` is a bundled command wrapper when installed and available. Other skill IDs are not automatically slash commands. Use `@<skill-id>` or the native `skill` tool with the exact ID. Explicit-only skills can still be loaded by Jiro when their workflow calls for them.

Jiro applies its workflow to the active task and follow-ups in the conversation. A new task needs a fresh scope and recipe. "New task" is a useful steer. This is an instruction contract, not a promise of a persistent product mode, cloud runtime, scheduler, or background wake mechanism.

## Initialize verification by default

Explicit repository initialization, or the first task that permits edits, creates and proves a task-specific verification skill unless the user opts out. Initialization without another task uses the primary documented surface. Reuse a relevant existing skill. Wrap an existing test or driving harness instead of rebuilding it. Check the actual UI, CLI, API, library, or other changed behavior.

Generated project skills belong under `<target-repository>/.opencode/skills/`. An OpenCode configuration-root repository follows its existing top-level `skills/` layout. Never write a target project's generated skill into this installed pack. Global output requires an explicit request.

A read-only question or activation without a task writes nothing. "Skip verification skill" is an explicit task opt-out. A repository instruction can make that preference project-wide. An opt-out from generating a skill is not permission to report unchecked behavior as proved.

Read `create-verification-skill` for behavioral proof and `maintain-verification-skill` for the upkeep pass. A generated skill is proved only after its instructions run and evidence survives cleanup. Missing tools, auth, or fixtures are blockers. Formal verification uses `create-formal-verification-skill` only when explicitly selected. It is not required at every initialization.

## Pick a tool

Start with Jiro for a nontrivial end-to-end task. Name a focused skill directly when the user wants a narrower result. Read it before giving one example prompt.

| The user wants to | Skill |
| --- | --- |
| Coordinate a verified engineering task. | [@jiro](../jiro/SKILL.md). |
| Check understanding of their goal before work. | [@in-your-own-words](../in-your-own-words/SKILL.md). |
| Improve an outcome-focused task brief. | [@sharpen](../sharpen/SKILL.md). |
| Trace current runtime behavior and ownership. | [@how](../how/SKILL.md). |
| Find historical rationale or the origin of a number. | [@why](../why/SKILL.md). |
| Understand a change through a plain explanation. | [@teach](../teach/SKILL.md). |
| Rebuild work context from supplied or explicitly scoped history. | [@recall](../recall/SKILL.md). |
| Catch up on this conversation and decisions waiting on them. | [@ketchup](../ketchup/SKILL.md). |
| Prove what a small diff could break elsewhere. | [@blast-radius](../blast-radius/SKILL.md). |
| Settle types, callers, and module design before implementation. | [@architect](../architect/SKILL.md). |
| Compare complete attempts at one brief and combine the best result. | [@arena](../arena/SKILL.md). |
| Partition independent coverage or declare a race. | [@swarm](../swarm/SKILL.md). |
| Review a diff skeptically with permitted independent reviewers. | [@interrogate](../interrogate/SKILL.md). |
| Fix a bug through a cheap, reliable failing test. | [@tdd](../tdd/SKILL.md). |
| Gate new tests or prune duplicate and implementation-coupled proof. | [@test-audit](../test-audit/SKILL.md). |
| Apply TypeScript modeling and boundary rules. | [@typescript-best-practices](../typescript-best-practices/SKILL.md). |
| Review comments and remove unsupported garnish. | [@no-comments](../no-comments/SKILL.md). |
| Remove AI writing tells without changing meaning. | [@unslop](../unslop/SKILL.md). |
| Apply a structured technical-writing standard. | [@technical-writing](../technical-writing/SKILL.md). |
| Hear the last assistant reply in plain language. | [@bro](../bro/SKILL.md). |
| Generate and prove task-specific behavioral verification. | [@create-verification-skill](../create-verification-skill/SKILL.md). |
| Audit a verification skill and every mapped feature. | [@maintain-verification-skill](../maintain-verification-skill/SKILL.md). |
| Explicitly verify a formal property beyond tests. | [@create-formal-verification-skill](../create-formal-verification-skill/SKILL.md). |
| Vet a measured performance number. | [@benchmark-checklist](../benchmark-checklist/SKILL.md). |
| Design a rigorous large or cross-cutting run. | [@figure-it-out](../figure-it-out/SKILL.md). |
| Keep and audit a local decision trail. | [@show-me-your-work](../show-me-your-work/SKILL.md). |
| Configure only requested role models and budget. | [@setup-kstack](../setup-kstack/SKILL.md). |
| Draft a personal workflow from authorized history evidence. | [@automate-me](../automate-me/SKILL.md). |
| Propose durable lessons from a completed task. | [@reflect](../reflect/SKILL.md). |
| Prevent repeated mistakes through structural enforcement. | [@correct](../correct/SKILL.md). |
| Build bot controls against an existing authorized backend. | [@make-bot-ui](../make-bot-ui/SKILL.md). |
| Make a bounded handoff to a worker. | [@delegate](../delegate/SKILL.md). |
| Define a reusable project agent. | [@create-subagent](../create-subagent/SKILL.md). |
| Shape module ownership and public interfaces. | [@code-organization](../code-organization/SKILL.md). |
| Reduce layers and hidden or mutable state. | [@minimize-reader-load](../minimize-reader-load/SKILL.md). |
| Verify browser flows with an available local runtime. | [@playwright-cli](../playwright-cli/SKILL.md). |
| Audit finished worktrees before approved removal. | [@worktree-cleanup](../worktree-cleanup/SKILL.md). |
| Find their way around this pack. | `@kstack-help`. |

For another installed skill, read its frontmatter and route by its description. Do not claim a tool is installed solely because this table names it. Report missing companions rather than substituting another pack.

### Distinguish close calls

- `how` explains mechanics. `why` explains reasons. `teach` combines findings into a paced explanation.
- `arena` repeats one brief across attempts. `swarm` partitions coverage or named race arms. Separate worktrees, ports, data, browsers, and outputs where attempts could collide.
- `architect` can continue into implementation after design. Ask for a checkpoint when the user wants approval before writes.
- `interrogate` reviews the changed code. `blast-radius` investigates effects outside it and proves the important safety claim.
- `recall` uses supplied or explicitly scoped prior history. `ketchup` covers this chat. Session handoff resumes a named branch or thread.
- `figure-it-out` designs a bounded run. Multi-day coordination still needs actual host capabilities and an explicit handoff plan. Skill Markdown does not keep work alive after a session ends.
- `in-your-own-words` restates the user's intent. `bro` simplifies the assistant's reply.

## Choose recipes and principles

Recipes are sections of Jiro's recipe book, not automatically registered skills or slash commands. Read the current recipe before describing its steps. A status question stays read-only. A request to open a PR is not a request to merge it. "Babysit" or "get it green" does not authorize shipping.

For a plan-only request, keep the deliverable a plan. Settle empirical design questions with authorized prototypes when appropriate. Do not silently implement a design checkpoint or create a new planning command.

Principle skills own their individual rules. Load only matching principles in full. A short steer such as "prove it works" should change a concrete decision. Name that decision with evidence, not a decorative principle citation. Do not maintain a second copy of a canonical principle body.

## Recover a drifting run

| Symptom | Grounded response |
| --- | --- |
| The workflow faded during a long conversation. | Restate the active task and load `jiro` again. Do not promise persistent mode mechanics. |
| A question became implementation. | Say "new task" and "read-only". Re-scope before further writes. |
| A role choice had no effect. | Check the exact role file path and whether the coordinator and worker explicitly read it. Verify authorization and the host catalog. |
| Cost exceeded expectations. | Inspect actual worker count and repeated calls. Offer requested role or panel changes without guessing prices. |
| A skill did not load itself. | Load its exact ID explicitly. Check registration and permissions. Explicit-only metadata is intentional. |
| Workers overwrote each other. | Stop conflicting writes and establish isolated owners and worktrees. Separate runtime state too. |
| An unattended run made activity but no result. | Replace the duration with a pass-or-fail finish condition. Check the verification path and stopping rule. |
| Success rests on a green build. | Require the real command, user flow, stored value, or profile and its evidence. |
| History is missing. | Ask for supplied exports or known scoped sessions. Do not scan global session storage. |
| A backend or browser is assumed. | Check actual availability and report the missing capability before claiming live proof. |

Read [references/prompting.md](references/prompting.md) for short corrective prompts. Unattended work remains bounded by authorization. It does not authorize commits, pushes, PRs, merges, deployments, billing, deletion, global installation, or customer messages by implication.

## Adapt the workflow

Use `automate-me` only with user-supplied or explicitly authorized history. Use `reflect` to propose lessons and wait for approved edits. Use Jiro's Authoring a skill and Evaluation recipes for a known workflow or behavior comparison. Use `skill-creator` when the host provides it.

Fix a misbehaving skill as a scoped skill task. Do not hide that edit inside unrelated feature work. Generate project skills in the target repository and preserve license notices. A file written and statically validated is not a live agent evaluation.

## Reply

Lead with the answer. Give at most one tailored example prompt in a code block. Link the actual file you read. Do not invent public plugin URLs, source links, session IDs, or runtime proof. Keep the answer short unless the user asked for the full map.
