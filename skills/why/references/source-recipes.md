# Source recipes

The why skill spawns one investigator per available evidence category. Each reads one source-specific recipe below. The recipes are concrete examples for common MCPs. Adapt them for another MCP in the same category.

Discover exact tool names and schemas in the active OpenCode catalog before calling them. The examples do not establish that a tool or table exists. Follow each server's own routing, schema, permission, and privacy instructions. Do not write to external systems during investigation.

| Category | Recipe | Example source |
| --- | --- | --- |
| Source control history | [code-archaeology.md](./sources/code-archaeology.md) | Git and `gh` |
| Issue / ticket tracker | [linear.md](./sources/linear.md) | Linear, adaptable to Jira, GitHub Issues, Plane, or Shortcut |
| Long-form documents | [notion.md](./sources/notion.md) | Notion, adaptable to Confluence, Google Docs, or Coda |
| Real-time team chat | [slack.md](./sources/slack.md) | Slack, adaptable to Discord, Microsoft Teams, or Mattermost |
| Infrastructure observability | [datadog.md](./sources/datadog.md) | Datadog, adaptable to New Relic, Honeycomb, Grafana, or Splunk |
| Error / exception tracking | [sentry.md](./sources/sentry.md) | Sentry, adaptable to Rollbar, Bugsnag, or Airbrake |
| Product analytics warehouse | [databricks.md](./sources/databricks.md) | Databricks SQL, adaptable to Snowflake, BigQuery, ClickHouse, dbt, or another analytics MCP |

Add [incident-postmortem.md](./sources/incident-postmortem.md) if the target looks defensive, such as null checks, retries, timeouts, rate limits, feature flags, egress guards, or OOM handlers.
