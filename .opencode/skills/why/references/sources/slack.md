# Slack Conversations

## What this source contains

- Discussions of problems and decisions.
- Incident-channel deliberation.
- Design threads debating tradeoffs.
- Answers never captured in formal docs.
- Post-merge discussions explaining revisits.
- DMs only when the available integration can search them within the authorized scope.

Chat evidence is ephemeral. Retention, deleted threads, archived channels, and search quality may limit coverage.

## How to search it

Discover the active chat MCP and exact schemas. Adapt to Discord, Microsoft Teams, or Mattermost when available. Follow the host's authentication workflow. If authentication fails, report the gap. Do not invent an authentication tool or bypass access controls.

1. **Author-bounded search.** Search the PR author's messages near the merge date.
2. **Keyword search.** Include feature names, symbols, misspellings, and casual phrasing.
3. **PR URL search.** Search a retrieved PR URL or its pull-number path.
4. **Error-string search.** Search exact handled errors for incident context.
5. **Channel-scoped search.** Use relevant engineering, project, incident, owning-team, and design-review channels.
6. **Read full threads.** A decision may be in a reply rather than the first message.

## What good evidence looks like here

- A thread explicitly debating alternatives.
- An incident message describing the condition the code handles.
- A reviewer question and an author or lead's answer.
- A meeting reference with a recorded decision.
- A product or customer-facing explanation of an external requirement.

## Common pitfalls

- **Retention cliffs.** Missing old messages are coverage gaps.
- **Unsearched DMs.** Name this limitation rather than implying full coverage.
- **Jokes as decisions.** Casual suggestions are not necessarily considered choices.
- **Context collapse.** Read the whole thread before citing a single message.
- **Auth failures.** Report that the source was not searchable.

## What to return

Give channel, retrieved permalink or thread ID, participants, date range, attributed verbatim quotes, and thread or incident context. Return cross-source links as Additional Leads.
