Paste this into the global AGENTS.md and adjust the paths. Keep it short;
the dream job does the heavy lifting.

```markdown
## Memory

Long-term memory lives in `~/.config/opencode/memory/` as markdown, indexed in
`memory/README.md`. When a task touches a project, tool or preference you might
have notes on, grep the folder before guessing.

When you learn something a future session would need (the user corrects you,
states a lasting preference, or a command fails and you find what works),
append one line to the inbox with a single shell append:

    printf '%s\n' "- $(date +%F) | <session id> | <project> | <what was learned, with evidence>" >> ~/.config/opencode/memory/inbox.md

Only append to the inbox. Edit other memory files, AGENTS.md or skills only
when the user asks; the nightly dream job curates them. Never record secrets,
credentials or other people's personal data. When the user asks what dreaming
found or to apply a dream, load the `opencode-memory` skill.
```
