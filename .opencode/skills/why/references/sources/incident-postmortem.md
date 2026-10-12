# Incident & Postmortem Context

This is a cross-cutting angle, not a separate source. When the target looks defensive, search incident history inside each investigator's own assigned source.

- **Documents.** Search postmortems mentioning the file, feature, or error.
- **Tickets.** Search incident, severity, reliability, and postmortem-action labels.
- **Team chat.** Search incident channels around the code's introduction date.
- **Source control.** Look for incident fixes, defensive checks, and revert/reapply sequences.
- **Infrastructure observability.** Inspect incident timelines and monitors created as follow-up actions.
- **Error tracking.** Inspect issue dates, releases, and stacks through the target.
- **Product analytics.** Inspect error-classifying events and user-visible retries around the incident window.

Fetch a full postmortem when it is within the assigned source. Action items may connect directly to code changes. Record cross-source links as Additional Leads rather than following another investigator's source.

Corroboration across an incident, ticket, postmortem, thread, PR, and error-event trajectory strengthens a reading. Temporal alignment alone does not prove causation. Skip this angle when the target does not look defensive.
