---
name: show-me-your-work
description: Keep a reviewable decision trail for long-running or unattended work using a TSV log with one row per decision. Local by default. Commit it when a reviewer needs the trail to trust the result. Use for @show-me-your-work, autonomous or multi-phase runs, or work a human reviews after stepping away.
license: MIT
metadata:
  opencode/autoinvoke: false
---

# Show me your work

Keep one canonical log.

Resolve the bundled template and helper relative to this skill's base directory. Write the log in the task's working directory, not in the installed skill.

## The format

A single TSV file, one row per decision. Cells stay single-line. Evidence is a pointer, not prose.

Copy `references/decision-log-template.tsv`, which contains the header row, to start a clean log. Use these columns:

- **ts.** ISO8601 timestamp.
- **phase.** The phase or workstream.
- **decision.** What was chosen or done, one line.
- **why.** The reason in plain words. If a principle drove it, say it plainly, not as a jargon tag.
- **evidence.** A link or path that proves it. Use a commit SHA, PR number, `file:line`, or an artifact, trace, or screenshot path. Never a paragraph.
- **result.** The outcome or predicate state. Examples include `tests green`, `reverted`, `pixel-diff 0`, `INCONCLUSIVE`, and `open`.

The following rows are fictional examples of the format, not claims about this run.

```tsv
ts	phase	decision	why	evidence	result
2026-05-24T09:02:00Z	frame	counted the work first, about 100 components and roughly 75 hours	wanted to know the size before starting a long run	commit 3a9f1c2	found 5 things to sort out before starting
2026-05-24T09:40:00Z	harness	took screenshots of the old version before changing anything	so we can compare old against new and catch any visual change	scripts/snapshot.sh, baseline/	saved 120 reference screenshots
2026-05-24T11:15:00Z	widget	moved the widget styles over without changing how it looks	keep the change small and the result identical	commit 7c21e0a, pixel-diff 0	looks identical, tests pass
2026-05-24T12:30:00Z	widget	threw out a helper's work because its screenshots were blank	checked the real files instead of trusting its summary	worktree reset	reverted, tightened the instructions for next time
```

## Logging a row

Write each entry the way you would tell a teammate what you did. Use plain words and concrete actions. Avoid AI speak and abstract jargon. If `unslop` is available, load it for log text too. It is not required to use this skill.

Use `scripts/log.sh <logfile> <phase> <decision> <why> <evidence> <result>`, resolved from this skill's base directory. It stamps `ts`, writes the header on first use, strips stray tabs/newlines, and prefixes any cell starting with `=`, `+`, `-`, or `@` with a single quote. A bare `printf` appending a row works too, but handle those same bytes when cells come from generated or user-supplied text.

Log decision points and checkpoints, not every action. Record a fork chosen, a unit completed with its verification result, a pivot or revert with its trigger, a blocker surfaced, or a gate fixed. For loop runs, write one row per iteration. Skip the trivial and self-evident.

A run is one OpenCode agent session, including its later turns and any summary of it. A pickup, a replacement agent, or a new session starts a new run. When a run adds to a log that already has rows, its first row has phase `start`. So does its first row after another run's `start` row. A run returning to a log in a later turn first reads the log's last rows to see whether another run wrote since. A `start` row names the `ts` range of the preceding rows this run did not write. Its evidence names the actual OpenCode session ID reported by the host. Never invent an ID. Use phase `start` for nothing else.

## Where it lives

By default the log is a working artifact, not committed. Keep it at `decisions.tsv` in the work dir, or `.audit/<task-slug>.tsv` when several efforts run at once. Leave it out of git.

Commit it only when the work is ambitious enough that a reviewer needs the trail to trust the result.

## Rules

- Append-only. A wrong call gets a new row that supersedes it. Never edit or delete history.
- Prefer evidence produced by committed scripts over hand-made one-offs. If available, consult the `encode-lessons-in-structure` principle skill. Do not require it to maintain a log.

## Audit the log against session history

At the end of the run, before handing back, check that the log told the truth. Export only this run's known session ID with `opencode api get /api/experimental/session/<sessionID>/export`. Confirm the export's `data.info.id` and `data.info.location.directory` match the session and working directory being audited. Read its messages and recorded tool calls. Do not scan global session storage or unrelated sessions. If the history cannot be retrieved, report that the transcript audit is incomplete.

Walk this run's rows against what actually happened. Each stretch begins at one of this run's `start` rows, or at the first row if this run created the log. It ends at the next `start` row of another run.

- Check that every row maps to a real decision or action.
- Check that each row's evidence resolves and shows what the row claims.
- A fork, pivot, or abandoned approach that shaped the work but is not logged is a gap. Add it.

Correct the log, not the story. The audit never edits or removes a row, even an invented one. When a row records neither a real decision nor a real action, or its claim or evidence is wrong, add a row that supersedes it with what actually happened and a pointer that resolves. This audit does not check rows outside this run's stretches. If this run's own work shows one of them is wrong, supersede it like any wrong call.

## Cross-model review of the trail

Before handing back, use OpenCode's `subagent` tool to spawn a `general` reviewer on a different model family from the one that did the work, when the host permits that selection. Self-review is not a substitute. Read `~/.config/opencode/instructions/pstack-models.md` if it exists and honor the host's model-selection constraints. Resolve an authorized model through the host's available-models tool before setting `model`. Never guess a model ID or silently substitute the worker's family.

The reviewer receives the audit trail and only this run's session history. Its prompt forbids file edits, commits, and external writes. It flags what the user should pay attention to. It does not redo the work.

- Decisions logged with weak or absent evidence.
- Verification steps skipped or claimed without proof in the history.
- Choices that look risky in hindsight, including premature decisions, scope creep, and papering over a symptom.
- Gaps the user would otherwise miss on a casual skim.

If no authorized model from another family is available, report the missing review. Do not present same-family or self-review as cross-model review.

Every reply for a run that produced a trail ends with an **Attention.** section. Lead with the actual reviewer's model on its own line as `reviewed by <model>`. Then list each flag pointing to specific rows or moments. `No flags` is a valid value. The model name alone is not. If the review could not run, say so instead of claiming a reviewer.

## Reviewing the trail

Read top to bottom, follow the evidence pointers, and spot-check. GitHub renders a committed TSV as a table. `column -s$'\t' -t decisions.tsv` renders it in a terminal.

## Composing this skill

Other skills route their audit trail here instead of inventing one. Load it with OpenCode's `skill` tool using the ID `show-me-your-work` and let it own the format. Do not restate the columns.
