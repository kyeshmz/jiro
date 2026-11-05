---
name: opencode-memory
description: Give an OpenCode setup long-term memory and a learning loop, following Anthropic's context-engineering practice. Puts the global config under git, slims the always-loaded AGENTS.md into on-demand skills, adds a markdown memory folder with an append-only inbox, and schedules a nightly "dreaming" job that reviews past sessions, updates memory and proposes rule changes for approval. Use this whenever someone wants their agent to remember things across sessions, stop repeating the same mistakes, learn from past sessions, shrink or clean up AGENTS.md or CLAUDE.md, version their OpenCode config, or mentions memory, dreaming, continual learning or context engineering for their own agent setup. Also use it to run, review or apply a dream ("what did dreaming find", "apply last night's dream").
---

# OpenCode memory

Models get smarter, but they never arrive knowing your machines, projects and
preferences. That knowledge is context, and context compounds: every rule or
memory you curate makes every future session better. This skill sets up four
layers, each built on the one before:

| Step | What you build | Why |
|---|---|---|
| 1. Versioned config | The config folder is a git repo, with no secrets in it | Every memory or rule change can be traced and rolled back |
| 2. Lean AGENTS.md | Only rules that matter in nearly every session stay always-loaded; the rest become skills | Always-loaded context bloats; skills load only when relevant |
| 3. Memory folder | Markdown files agents search with grep, plus an append-only inbox | Agents learn during a session without corrupting shared rules |
| 4. Dreaming | A nightly job that reads the day's sessions and the inbox, updates memory and proposes rule changes | A single session can't see patterns across sessions or spare effort for curation |

Paths below use `$CONFIG` for the OpenCode config folder, normally
`${XDG_CONFIG_HOME:-$HOME/.config}/opencode`. `scripts/` and `references/`
are relative to this skill's folder.

## How to run this skill

- This changes someone's global agent setup. Start with the audit, show the
  plan, and get one go-ahead for the rollout (or per step if they prefer).
- Do the steps in order and finish each with a focused commit. Later steps
  rely on git for rollback.
- When moving text out of AGENTS.md, move it verbatim. A move should change
  where a rule loads, never what it says.
- Never print secret values. Report where a secret is, not what it is.

## Step 0: Audit

Gather these facts and report them in one short table before changing anything:

1. Config folder and whether it is a git repo (`git -C "$CONFIG" status`).
2. Size of the global AGENTS.md (`wc -c`) and its section headings.
3. Inline secrets: `python3 scripts/scan-secrets.py "$CONFIG"` lists files and
   JSON key paths that look like credentials, without values.
4. Existing memory: any `memory/` folder, memory plugins or MCP memory servers.
5. Scheduler: `cronctl`, `launchd` (macOS), `systemd --user` or `cron`.
   Notifier, if any: e.g. `harkctl`, `ntfy`, `terminal-notifier`.

## Step 1: Version the config

1. **Move inline secrets out of config files.** OpenCode replaces
   `{file:/path}` in config values with the file's contents. For each finding,
   write the whole value (including any `Bearer ` prefix) to
   `$CONFIG/secrets/<name>` with mode 600, and replace the value with
   `{file:~/.config/opencode/secrets/<name>}`. Check the config still loads
   (`opencode mcp list`, or start a session) before continuing.
2. **Add `.gitignore`** from `references/gitignore.template`. Merge it with any
   existing file. Ignore anything else the audit flagged: token files, backups
   (`*.bak*`) and service or auth JSON.
3. **Stage and check.** `git init`, `git add -A`, then review
   `git status --short` and run `python3 scripts/scan-secrets.py --staged "$CONFIG"`.
   The scan must print nothing. If something is flagged, unstage it and
   ignore it or fix it.
4. **Commit a baseline** labelled as the pre-memory snapshot.

Leave old backup files alone. Offer to delete them as a separate,
confirmed action, since git replaces them.

## Step 2: Slim AGENTS.md

Sort each section of the global AGENTS.md into one of three kinds:

- **Keep:** it affects nearly every session (response style, git habits,
  execution discipline), or it's a safety rule whose violation is costly even
  in a session that never loads a skill.
- **Move to a skill:** a procedure or set of facts that only matters for some
  tasks (a deploy flow, an account matrix, a posting style, a model table).
- **Merge:** it duplicates an existing skill. Fold it into that skill if the
  skill is local and owned by the user; otherwise treat it as "move".

For each moved section:

1. Create `$CONFIG/skills/<name>/SKILL.md` with the section's text verbatim
   under a clear heading. Write a specific, slightly pushy `description` that
   lists the situations that need it. Use a consistent name prefix for
   personal skills (e.g. `<user>-servers`).
2. Replace the section in AGENTS.md with a one-line pointer: "Before
   <situation>, load the `<name>` skill." Skill descriptions alone
   undertrigger. The pointer costs a line and makes loading reliable.

Aim for a 35–50% smaller AGENTS.md. Report bytes before and after, then commit.

## Step 3: Memory folder

Create this layout (seed only the README; never invent memories):

```text
$CONFIG/memory/
  README.md    index: one line per file and what it holds
  inbox.md     append-only; any session may add an entry
  <topic>.md   curated memories, e.g. preferences.md, tools.md, projects/<name>.md
  dreams/      nightly reports and rotated inboxes
```

Add the block in `references/agents-memory-block.md` to AGENTS.md, with
paths adjusted. It sets up these permissions:

| File | During a session | Dream job |
|---|---|---|
| `memory/inbox.md` | Append only, with a single shell `>>` | Reads, then rotates it away |
| Topic memory files | Read; edit only when the user asks | Edits directly and commits |
| AGENTS.md, skills, config | Read; edit only when the user asks | Proposes changes only |

Appending with `>>` keeps concurrent sessions safe. A read-modify-write edit
can drop another session's entry. Never write secrets or third-party
personal data to memory. Commit.

## Step 4: Dreaming

`scripts/dream.sh` runs one unattended review:

1. Takes a lock, so overlapping runs exit.
2. Rotates `memory/inbox.md` into `memory/dreams/<date>-inbox.md`.
3. Runs `opencode run` with `references/dream-prompt.md`, covering sessions
   since the last successful run (or 24 hours). The dream agent reads sessions
   through the `tools.opencode.session_list` / `session_context` tools,
   splits large batches across subagents, edits topic memory files and writes
   `memory/dreams/<date>.md`.
4. Enforces permissions after the run. Any change outside `memory/` to a
   file that was clean beforehand is reverted, and the revert is noted in the
   report.
5. Commits `memory/`, archives the dream session, saves the run time and
   delivers the report's `Summary:` line.

Settings (environment variables):

- `OPENCODE_CONFIG_DIR`, and `DREAM_WINDOW_HOURS` for the first run's
  window (default 24).
- `DREAM_MODEL`, e.g. `anthropic/claude-opus-5-5#high`.
- `DREAM_PARENT_SESSION`: run the dream as a child of this session, so it
  never shows up as a top-level session. Without it, the dream is a
  top-level session that gets archived after the run.
- `DREAM_REPORT_SESSION`: post the summary into this session as a queued
  message. Use it when the person has a personal-assistant session that
  relays updates. Often this is the same session as `DREAM_PARENT_SESSION`.
- `DREAM_NOTIFY`: any command that receives the summary as its last
  argument (a push notifier, for example).

Ask the person where results should go. If they have an assistant session,
prefer it over push notifications, and schedule the run inside that
assistant's quiet-hours window.

Setup:

1. Copy the script to `$CONFIG/memory/dream.sh` (so it's versioned with the
   memory it maintains) and make it executable.
2. Run it once by hand. Open the report and check that it cites real session
   IDs, that its findings match what happened, and that the notification arrived.
3. Schedule it nightly while the machine is usually on, e.g.
   `cronctl add opencode-dream --schedule "daily at 04:00" -- <path>/dream.sh`.
   Otherwise use launchd or a crontab entry. The scheduled environment needs
   `opencode` and the notifier on `PATH`.
4. Commit.

## Reviewing and applying a dream

When the user asks what dreaming found, or to apply it:

1. Open the newest `memory/dreams/<date>.md` (or the date they name).
2. List its pending proposals: number, one-line change and evidence count.
   Mention memory edits the dream already made in one line.
3. Apply the proposals the user accepts exactly as written. Set each
   proposal's `Status:` to `accepted` or `rejected`. Future dreams read
   rejections and stop proposing them.
4. Commit the applied changes and the updated report together, citing the
   dream date.

To undo a memory edit the dream made, revert its commit
(`git log -- memory/`).
