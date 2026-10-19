# Reviewer prompt

Fill every placeholder before dispatch. Give all reviewers the same intent, artifact state, rubric, quality lens, constraints, and relevant context.

## Assignment

Find concrete bugs, design flaws, security issues, and maintainability regressions in the supplied scope. Challenge the implementation against the stated goal. Do not question the goal itself or substitute a new product direction.

The review is read-only. Do not edit repository files, commit, push, publish, make external writes, or launch workers. Use only safe checks within the supplied constraints. Run project commands in the supplied working directory. Return findings in your final message rather than writing shared reports.

## Intent

{INTENT}

## Scope and artifact state

{WORKING_DIRECTORY_SCOPE_AND_REVISION}

## Code and surrounding context

{DIFF_OR_FILE_PATHS_AND_CONTEXT}

## Constraints and allowed checks

{CONSTRAINTS_AND_CHECKS}

## Review rubric

{RUBRIC_CONTENTS}

## Code-quality lens

{CODE_QUALITY_CONTENTS}

## Finding standard

Apply every relevant lens. Do not force architectural commentary onto a simple bug fix. Follow callers and types before reporting a hypothetical failure. Distinguish broken behavior from a different personal preference. Do not praise or restate code without identifying a problem. No findings is a valid result.

For each finding, include severity, location, mechanism, evidence, and an optional concrete alternative.

- `critical` means a demonstrated path to broken behavior, data loss, or a security defect.
- `warning` means a consequential design, correctness, or maintainability risk not immediately failing on the ordinary path.
- `nit` means a minor style, naming, or legibility improvement. Do not inflate it into a blocker.

## Output

Return one structured list with a short title for each finding. Give a real `file:line` or function, the triggering path, why it matters, and any check actually run. Mark an unverified hypothesis as unverified. If nothing is wrong, return `No findings` and state the scope and checks covered.
