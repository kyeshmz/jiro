# Datadog Telemetry

## What this source contains

Datadog can provide the production runtime record rather than the planned or discussed behavior.

- Metrics such as counters, gauges, and histograms.
- Monitor and alert conditions.
- Curated dashboards.
- APM traces and spans.
- Logs of motivating error conditions.
- Incident timelines and linked postmortems.
- Exploratory notebooks.

## How to search it

Discover the active Datadog tools and schemas. The tool names below are examples. Confirm them before calling anything. Use only read operations.

1. **Identify services.** Tools such as `search_datadog_services` and `search_datadog_service_dependencies` may establish owning teams and upstream/downstream services.
2. **Inspect dashboards and monitors.** Search feature names, service names, and symbols. Record queries and watched thresholds. Tools may resemble `search_datadog_dashboards` and `search_datadog_monitors`.
3. **Inspect metrics.** Search names and retrieve descriptions, units, tags, and time series. Examples include `search_datadog_metrics`, `get_datadog_metric_context`, and `get_datadog_metric`.
4. **Narrow logs.** Search error strings and symbols within a service and time window. Prefer patterns or aggregate summaries over raw dumps. Examples include `search_datadog_logs` and `analyze_datadog_logs`.
5. **Inspect spans and traces.** Use aggregate summaries for frequency and individual traces for mechanics. Examples include `aggregate_spans`, `search_datadog_spans`, and `get_datadog_trace`.
6. **Inspect incidents.** Search near the code's introduction date and retrieve full timelines. Examples include `search_datadog_incidents` and `get_datadog_incident`.

Use a time window around the change date, usually about 30 days before and after. An incident explicitly recording an added defensive check is stronger evidence than a nearby metric spike.

## What good evidence looks like here

- A monitor whose condition matches the code's constraint.
- A dashboard with relevant ownership and creation dates.
- A production spike before a change and stable values afterward, labeled as correlation.
- An incident record naming the code, symbol, or error.
- Logs demonstrating the exact condition the code handles.

## Common pitfalls

- **Correlation is not causation.** Nearby changes may explain improvement.
- **Chart framing.** A chart title shows what its maker watched, not necessarily why a particular line exists.
- **Vanished telemetry.** Renamed metrics and retention cliffs are coverage gaps.
- **Noise at scale.** Bound by service, tag, and time. Aggregate instead of dumping logs.
- **Instrumented is not caused.** Cross-reference observations with textual rationale before claiming motivation.

## What to return

For each item, give its type, name, retrieved link or identifier, owner, dates, exact condition or quote, and relevance. Separate direct rationale from temporal correlation.
