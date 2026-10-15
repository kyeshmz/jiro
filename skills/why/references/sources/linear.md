# Linear Tickets

## What this source contains

- Issues describing features, bugs, and motivation.
- Project docs, PRDs, and specs attached to issues.
- Parent/sub-issue relationships.
- Comments clarifying scope or rationale.
- Labels indicating compliance, customer requests, performance, or incidents.
- Status updates, attachments, and linked PRs.

Tickets may capture the product or business forcing function missing from the code review.

## How to search it

Discover the active ticket MCP and its exact schemas. Names such as `get_issue`, `list_issues`, and `get_project` are examples. Adapt to Jira, GitHub Issues, Plane, or Shortcut when that is the available source.

1. **Start with linked tickets.** Fetch ticket IDs from the code anchor and read descriptions and comments.
2. **Search keywords.** Use feature names, symbols, and business terms. Try several phrasings.
3. **Walk the issue tree.** Parents often carry broader rationale than tactical sub-issues.
4. **Read project docs.** Inspect attached specs and rationale within this source.
5. **Check labels and milestones.** They may explain external constraints and deadlines.

## What good evidence looks like here

- A description naming the business problem.
- A comment recording a choice and its rejected alternative.
- A parent initiative explaining broader scope.
- An attached PRD or spec.
- Relevant customer, compliance, incident, or performance labels.

## Common pitfalls

- **Scope drift.** Closed and reopened tickets may describe different work.
- **Mechanical templates.** Generic improve-user-experience wording may not answer the question.
- **Stale plans.** Compare ticket dates and later updates to the code's ship date.
- **Duplicate chains.** Follow duplicate relationships to the canonical ticket.
- **Restricted access.** Report the gap rather than guessing about inaccessible issues.

## What to return

Give ticket ID, title, verbatim motivation, labels, parent, project, author, dates, and a retrieved link. Return cross-source PR or chat links as Additional Leads.
