# Code Archaeology (git + in-repo)

## What this source contains

- Commit messages, dates, authors, and diffs.
- PR descriptions, review comments, and discussion threads through `gh` or a discovered source-control MCP.
- Inline code comments, TODOs, FIXMEs, and deprecation notes.
- Architectural decision records.
- Tests whose names and assertions may encode motivating edge cases.
- Related files modified in the same commits.
- CHANGELOG entries and release notes.
- Issue and ticket IDs in commits and PR bodies.

This source is tied directly to the code, but it is not necessarily complete. Private PRs, missing history, and unrecorded discussions remain gaps.

## How to search it

Expand the seed commit list. Trace history through renames:

```bash
git log --follow --oneline -- <file>
```

Find commits adding or removing exact text or matching a pattern:

```bash
git log -S '<exact_string_from_code>' -- <file>
git log -G '<regex>' -- <file>
```

Read line history, complete diffs, and a bounded history range:

```bash
git blame -L <start>,<end> <file>
git show <hash>
git log <old>..<new> -p -- <file>
```

For substantive commits, extract PR references and retrieve review context when the CLI is available and authenticated:

```bash
git log -1 --format=%B <hash>
gh pr view <number> --json title,body,author,createdAt,mergedAt,labels,closingIssuesReferences,comments,reviews,files
```

Use discovered source-control MCP tools when needed. Follow the server's instructions and exact schemas rather than assuming tool names.

Look for ADRs, nearby comments, and related tests:

```bash
rg -l -i 'architecture.decision' --glob '*.md'
rg -n -C2 '(TODO|FIXME|HACK|XXX|NOTE)' <target_file>
rg -l '<symbol>' --glob '*test*'
```

## What good evidence looks like here

- A PR description explaining the problem, not merely the change.
- A review thread debating alternatives.
- An inline comment explaining a non-obvious constraint.
- A test naming a specific motivating edge case.
- A commit message referencing a ticket or incident.
- A release note summarizing user-visible rationale.

## Common pitfalls

- **Squash merges.** The branch commits may be gone. Read the PR body and comments.
- **Misleading messages.** A small-refactor label may hide a behavior change. Read the diff.
- **Copied patterns.** Trace the pattern's origin rather than assuming this author invented it.
- **Bot commits.** Dependency updates and automated backports may carry little motivation.
- **Intent from mechanics.** A function name or implementation proves behavior, not author intent. Find textual rationale.

## What to return

For every relevant commit, PR, or comment, include exact quoted text, location, author, date, and whether it is direct or circumstantial evidence.
