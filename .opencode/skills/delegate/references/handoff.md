# Worker handoff

Fill the brief before dispatch. All fields need a concrete value or an explicit `none` / `not applicable`, not an unresolved placeholder. A small unit may collapse this to a paragraph that still names the goal, scope, acceptance, verification, constraints, and return format.

```text
UNIT         <unit ID and attempt number>
GOAL         <one-sentence outcome; include the overall task goal>
WORKDIR      <absolute repository or assigned worktree path; use it for project commands>
SCOPE        <exact paths and resources this worker exclusively owns, or read-only>
CONTEXT      <applicable instructions, relevant files, predecessor reports and artifacts>
SKILLS       <required skill IDs and references to read before work, or none>
ACCEPTANCE   <observable criteria, one per line>
VERIFY       <literal commands and what they prove; include required SHA and measurement method>
TIMEBOX      <effort/runtime limit; return partial findings if exceeded>
FORBIDDEN    <other workers' paths; parent records; unrequested commits, external writes, cleanup>
STANDING     <all relevant user constraints, including later corrections, copied verbatim>
REPORT       <the return format below; final message must stand on its own>
```

The brief must not claim a permission that the parent lacks. The worker stops and reports BLOCKED if it cannot satisfy the brief within its tools, permissions, or owned paths. Do not weaken acceptance criteria or change a shared contract to pass.

## Worker return format

```text
STATUS: PASS | ISSUES | BLOCKED
unit: <unit ID>
attempt: <attempt number>
summary: <what was achieved>
workdir: <actual absolute path>
branch: <branch, detached, or not applicable>
sha: <exact tested commit SHA, or not applicable; identify uncommitted changes separately>
files_changed: <paths, or none>
verification: <each literal command, exit code, and evidence path; or inspection performed>
method: <required measurement method and sample count, or not applicable>
issues: <every proven issue with evidence, or none>
gaps: <missing access, skipped checks, unmet acceptance, deviations, or none>
```

- **PASS** requires every acceptance criterion and required check to pass. For an inspection-only task, specify exactly what was inspected; it makes no claim about unrun tests.
- **ISSUES** means a check failed or a defect was proved. Report every proven issue, not only the first.
- **BLOCKED** means the work or required verification cannot be completed. Partial findings and touched files still belong in the report. Missing access and missing evidence do not become PASS.

Commit verification records the exact requested SHA. If the working tree was dirty, identify the diff tested; a SHA alone does not identify uncommitted code. Measurement reports also record the requested method, sample count, order, and what one sample means. Re-check after any artifact change that invalidates the evidence.

## Ownership

The parent writes `plan.md`, every brief, and every saved report. Workers may read those files but never change them. Code writers edit only the paths named in SCOPE within their assigned checkout. Artifact writers edit only their own output directory. Shared contracts, logs, build outputs, ports, and Git state need a single owner too.

The parent captures each child's final message, then independently accepts or rejects it. The report is evidence to examine, not a verdict the parent must adopt.
