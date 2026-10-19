---
name: reflect
description: Spawn three parallel review subagents over the active session, surface durable learnings, and route each to a concrete skill edit or structural backlog item. Use for @reflect, /reflect, or when the user says reflect.
license: MIT
metadata:
  opencode/autoinvoke: false
---

# Reflect

Mine the current conversation for durable learnings, then route them into skill edits.

Invoke when the user says "reflect", "@reflect", or "/reflect". Skip when the conversation is trivial, off-topic, or already covered by an existing skill the parent followed correctly. One-offs are not learnings.

Resolve all bundled references relative to this skill's base directory.

## 1. Locate the active session history

Export only this conversation's known OpenCode session ID with `opencode api get /api/experimental/session/<sessionID>/export`. Confirm the export's `data.info.id` and `data.info.location.directory` match the session and working directory being reviewed. Read its messages and recorded tool calls. Do not scan global session storage, list unrelated sessions, or search editor transcript folders.

Never guess a session ID. If the host does not expose the current ID or the export cannot be retrieved, pass a tight digest of the current conversation instead and state the history gap. Include decisions, corrections, verification results, actual skill loads, and relevant tool calls. Do not present the digest as a complete transcript. Use an export in memory when possible. If a file is needed, keep it scoped to this task and share only its exact path.

## 2. Spawn three reviewers in parallel

Use OpenCode's `subagent` tool with `agent: general`. Each prompt forbids file edits, commits, and external writes. Keep read-only MCP capabilities available to verify the tickets, chat threads, and traces the history references. OpenCode controls access through agent permissions, not a `readonly` spawn flag. Do not pass Cursor-specific `Task` arguments or disable MCP access to simulate read-only review.

Read the exact authorized Jiro role-file path supplied by the caller, if any. Do not search for or migrate unrelated global role files. Use the role lines below, subject to the host's model-selection rules. Resolve authorized choices through the host's available-models tool before setting `model`. Omit `model` when no override is authorized, no role file is supplied, the role is absent, or its value is `auto` or `inherit-parent`. Never guess a model ID or silently substitute another model. Report an unavailable requested model rather than claiming it ran.

| Lens | Role line | Prompt template |
|---|---|---|
| Judgment | `reflect judgment, divergent, synthesizer` | `references/judgment-reviewer.md` |
| Tooling | `reflect tooling` | `references/tooling-reviewer.md` |
| Divergent | `reflect judgment, divergent, synthesizer` | `references/divergent-reviewer.md` |

Pass each template verbatim, substituting the history path or digest where marked. Include the working directory, original goal, and actual skill paths or IDs. Child sessions start with fresh context. Spawn the independent reviewers concurrently in background child sessions when supported, then wait for completion notifications. Do not poll. If the host requires foreground delegation, run the same three lenses in foreground and say that parallel review was unavailable.

Reviewers return findings in the subagent response body. If any review fails, report the missing lens and include the gap in synthesis rather than inventing findings.

## 3. Synthesize

Spawn one `general` synthesizer using the `reflect judgment, divergent, synthesizer` role under the same model-selection rules. Its prompt forbids file edits, commits, and external writes but permits read-only evidence lookups.

Pass `references/synthesizer.md` verbatim, with each reviewer's full output inlined where marked. Include the same history path or digest, working directory, and any review gaps. The synthesizer reads target skills before accepting body edits and returns an Accepted / Rejected / Backlog list.

## 4. Structural enforcement check

Move any Accepted item that a lint rule, script, metadata flag, or runtime check would enforce more reliably to Backlog. If available, consult the `encode-lessons-in-structure` principle skill. It is not required to run this check.

## 5. Apply after approval

Present the synthesizer's full Accepted / Rejected / Backlog output and wait for explicit approval before applying any Accepted edit. The user picks the subset and may redirect routings. Skill changes affect future agents. Do not auto-apply.

Backlog items are proposals, not authorization to write to an external tracker. File them only when the user approves the items and destination. Otherwise leave them in the report. Do not invent a tracker, issue, or filing result.

Follow each approved row's Routing exactly:

- Trivial existing-skill edit, such as a one-line bullet, a tightened sentence, or a stale fact corrected. The parent does it directly.
- Substantive existing-skill edit, such as a new section, a new pattern table, or more than about ten lines. Load `skill-creator` if available and run its draft / test / iterate loop. Otherwise follow the repository's skill-authoring recipe, or draft, test, and iterate explicitly when none is available.
- `tune description: <skill path>`. Use `skill-creator`'s description-optimization loop when available. Otherwise test representative trigger and non-trigger prompts before declaring the change effective.
- `new skill via skill-creator: <kebab-name>`. Use `skill-creator` when available. Otherwise follow the repository's authoring recipe and validate the new skill's shape and behavior.

If the environment ships a `SKILL.md` validator, run it on every touched skill before declaring done. At minimum, check frontmatter, referenced files, and cross-skill links. Do not claim behavioral validation from a frontmatter-only check.

## 6. Summarize for the user

After approved work, use a short list with no preamble. Include only applicable entries:

- Edits applied. `<skill path>`. What changed, one line each.
- New skills created. `<skill path>`. One line each, rarely.
- Backlog filed. `<issue title>` and its actual link, one line each.
- Backlog proposed but not filed. One line each.
- Dropped. One line per rejected finding and its reason from the synthesizer.
