# Sentry Error History

## What this source contains

Error tracking may explain the exceptions, stacks, and trajectories that motivated a check, catch, retry, or fallback.

- Grouped issues with counts, dates, releases, and comments.
- Individual events with stacks, tags, and context.
- Deployment and release records.
- Replays and profiles when available.
- Engineer comments about root cause.

Temporal correlation is useful but is not proof that a particular change fixed an error.

## How to search it

Discover the active error-tracking MCP and exact schemas. The names below are examples. Adapt to Rollbar, Bugsnag, Airbrake, or another available error product.

1. **Orient.** Discover accessible projects and organizations. Tools may resemble `find_organizations` and `find_projects`.
2. **Search related issues.** Use exception classes, symbols, error strings, and file paths. A tool may be called `search_issues`.
3. **Bound by release and time.** Inspect first/last seen, affected releases, and frequency trajectories. Tools may resemble `search_issue_events` and `get_issue_tag_values`.
4. **Read representative events.** Inspect the stack, tags, and breadcrumbs. A tool may resemble `get_sentry_resource`.
5. **Inspect nearby releases.** Correlate release and PR dates. A tool may resemble `find_releases`.
6. **Use AI analyses cautiously.** A capability such as `analyze_issue_with_seer` produces hypotheses, not primary evidence. Do not start a paid or mutating analysis without authorization.

## What good evidence looks like here

- Issue dates aligned with the change, labeled as correlation.
- Stacks passing through the target and demonstrating the handled condition.
- A comment from the PR author explicitly explaining the correction.
- A PR or commit linking an error issue.
- Counts falling after a release containing the target, with competing changes considered.

## Common pitfalls

- **Grouping drift.** An error may move to a new issue after a refactor.
- **Noisy release correlation.** Many commits land in one release.
- **Upstream fixes.** Another system may explain why an error stopped.
- **Resolved is not fixed.** A manually resolved state does not prove a code correction.
- **AI hallucinations.** Return to actual events and stacks.
- **Sampling.** Low counts do not necessarily mean low occurrence.

## What to return

Give issue ID, title, project, first/last seen, counts and known sampling, releases, representative stack excerpt, relationship to the ship date, retrieved link, and author comments.
