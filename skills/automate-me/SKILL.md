---
name: automate-me
description: Turn the user's working preferences into a personal style skill or update one from explicit feedback and scoped conversation evidence. Use for @automate-me, automate me, capture my working style, or create, update, or refresh my personal mode skill.
license: MIT
metadata:
  opencode/autoinvoke: false
---

# Automate me

Capture a user's distinct working conventions in one concise skill. Use ordinary skill authoring for a task-specific procedure or one narrow habit instead. Do not turn a preference interview into a new general-purpose mode bundle.

Read `references/shared-rules.md`. Resolve resources from the loaded skill base. Load `skill-creator` when available and `unslop` for prose discipline. Use `jiro` only as an example of granularity. Do not copy its preferences into the user's skill.

## Find the target

1. Establish the intended repository, skill ID, scope, and allowed writes. Inspect only relevant project skill locations and any existing skill path the user supplied. Do not search global skill trees or unrelated sessions to infer identity.
2. If an existing personal style skill matches, update it when requested. Otherwise ask whether to update it or start fresh. Preserve its ID, category, and sections not contradicted by new evidence. Ask why a fresh start is needed before discarding an established skill.
3. For an update, use its latest known edit date as the history boundary when available. A Git timestamp can establish that date. If no reliable boundary exists, say so rather than inventing one.

## Gather evidence

Use the active conversation, user-supplied transcripts, or explicitly authorized known session IDs in the target workspace. Do not scan global session storage or other workspaces. Ask for a bounded history source when none is available, or proceed from direct preferences alone.

With enough supplied history, split it into two or three non-overlapping slices. Read them locally or use bounded read-only `delegate` tasks. Give every worker exact permitted paths or session IDs and forbid edits, external writes, further delegation, and unrelated history access. Inherit the current model unless the user authorizes an override and the host confirms it. No role configuration is required.

Look for response length and tone, delegation habits, verification standards, code and prose discipline, worktree and review conventions, and skill-maintenance habits. Return patterns with resolvable evidence pointers. Prefer repeated signals across at least two slices. Drop contradictory or isolated inferred preferences unless the user confirms them. An explicit current preference can stand without repeated historical examples.

## Ask directly

Mining cannot establish intent that never appeared. Ask one or two compact questions with four to six options. Allow several choices for category questions when the host supports it. Use ordinary chat if no structured question tool exists. Start with the areas that matter, follow up on selected areas, and end with one free-form invitation for anything missed.

For an update, ask what changed or remains missing. Do not repeat a full intake or present twenty questions at once.

## Cluster and draft

Group only evidenced, non-default rules. Possible sections include response style, autonomy, understanding first, delegation, code and prose discipline, review and verification, process, and skill maintenance. Omit sections with nothing distinct to say.

Write short operational imperatives. Use the user or the human rather than a person's name in the body. Reference companion skills by exact available ID instead of copying their contents. Do not invent personas, metaphors, permissions, or unsupported host capabilities. A preference cannot override host rules or authorize commits, deployments, deletion, customer messages, or unrelated external writes.

For a new project skill, write `<target-repository>/.opencode/skills/<chosen-id>/SKILL.md` unless the repository is itself an OpenCode configuration checkout with its own layout. Write a global skill only when explicitly requested. Preserve an existing target's established category. Never place generated user skills in this installed pack.

Make `name` match the chosen ID. Describe explicit `@<id>` invocation and the user's requested style, not generic coding keywords. Use one valid YAML description scalar and `metadata.opencode/autoinvoke: false` unless the user explicitly wants automatic application. A `-mode` suffix is optional rather than a host feature.

## Refine and hand back

Apply `unslop` while preserving meaning and justified uncertainty. Show the draft and ask whether it matches the user's style or misses anything. Revise from that feedback. This is subjective output. Do not impose a benchmark loop unless trigger accuracy or a concrete behavioral failure needs testing.

Validate frontmatter, exact IDs, reference resolution, and target placement. Report the target path, captured preferences, evidence limits, and remaining choices. Leave commits, pushes, PR creation, and global installation to explicit authorization. A worktree or PR is not a mandatory final step.
