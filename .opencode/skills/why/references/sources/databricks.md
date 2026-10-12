# Databricks Analytics & System Tables

## What this source contains

Databricks can provide product analytics, data-pipeline history, and warehouse telemetry. It complements infrastructure observability with a product and data view.

- Product events and typed, deduplicated dbt models.
- Usage and billing events relevant to cost- or volume-driven decisions.
- Experiment exposure and feature-flag outcome tables.
- System tables such as query history, compute warehouses, billing, and access audit.
- dbt lineage showing upstream and downstream dependencies.
- Exploratory notebooks, when a discovered tool can retrieve them.

Schemas and column names are company-specific. The names below are examples, not confirmed tables.

## How to search it

Discover the active SQL MCP and its read-only execution schema. A tool may be named `execute_sql_read_only`, but confirm it. If execution returns a statement ID and a polling tool is available, poll that result rather than rerunning the query.

Orient before querying:

```sql
SHOW TABLES IN <your_analytics_db>.<schema> LIKE '*<keyword>*';
DESCRIBE TABLE <your_analytics_db>.<schema>.stg_<event>;
```

Time-bound every query. Bracket the change date, usually about 30 days before and after. Use a wider window only with a reason. Confirm the timestamp column before filtering.

Prefer a confirmed typed dbt model over equivalent raw events. Raw sources may contain duplicates and untyped properties. Confirm deduplication keys, property columns, context fields, refresh cadence, and retention. Do not assume every model shares the same columns.

Useful investigation patterns include:

1. **Event usage trajectory.** Count relevant events around the PR merge. A ramp or decay may suggest launch or deprecation. It does not establish intent by itself.
2. **Defensive threshold origin.** Inspect the median, p99, and maximum of the relevant property before the PR. A matching threshold is circumstantial evidence, not proof of the author's choice.
3. **Experiment lookup.** Discover exposure tables and inspect confirmed flag keys and variants near the change date.
4. **Query history.** Use a tight time window and confirmed query-history columns to inspect expensive queries mentioning the table or symbol.
5. **dbt lineage.** Return repository-history leads to the source-control investigator rather than chasing that source yourself.

## What good evidence looks like here

- An exposure record naming the target flag and an explicit ship or conclusion decision.
- A relevant error-classifying event falling after a corrective change, labeled as temporal correlation.
- A stored analysis explicitly explaining a threshold or migration decision.

## Common pitfalls

- **Instrumented is not caused.** Logging an event does not explain why the target code exists.
- **Instrumentation changes.** A volume step may mean logging changed, not behavior.
- **Schema drift.** Today's properties may not have existed when the code was written.
- **Refresh lag.** Recent events may not yet appear in a dbt model. Confirm the lag before using a raw fallback.
- **Unconfirmed tables.** Never report results from assumed table names.
- **Retention gaps.** Missing historical data is not evidence of no activity.
- **Notebook access.** A SQL-only MCP may not retrieve notebooks. Report unavailable notebook evidence as a gap.

## What to return

Give the finding type, confirmed fully-qualified table, exact query, time window, compact numeric summary, relationship to the ship date, and evidence strength. Do not dump raw rows. Follow the active analytics server's metric-catalog and schema-discovery rules when adapting this playbook to another product.
