# Word the prompt

A useful prompt states the intent and a check for done. Jiro's recipe supplies the steps. A few plain sentences usually do more work than a prescribed chain of tools.

## Include the facts that change the task

- State the goal or the observed problem.
- Give a pass-or-fail done check. A mood or a duration is not a check.
- Name the proof to show. Use real command output, a flow recording, a stored value, or a before-and-after measurement.
- Include a known symptom, repro step, log, artifact, or link that saves a search.
- State real constraints. "Repro first", "read-only", "zero behavior change", and "let me review before implementation" change the workflow.

## Leave room to solve the problem

Do not prescribe implementation details without a real constraint. Avoid a long sequence of skills that duplicates the recipe. Name a tool when overriding a specific choice.

Keep a guessed cause distinct from an observed symptom. Ask for an independent restatement of a noisy report before offering a theory that narrows the search.

## Load only authorized context

For a long or messy request, ask for the underlying problem in plain words before any edit. A misunderstanding is cheaper to correct there.

In a fresh conversation, supply a state capsule or known history references for `@recall`. Name the topic, workspace, and window. Recall does not discover context by scanning global session storage.

For unfamiliar code, use `@how` for current mechanics and `@why` for historical reasons. Ask `@teach` to explain why a proposal fixes the cause rather than hiding a symptom.

## Settle the design before the plan

Compare structurally distinct options when the decision matters and no precedent settles it. Use screenshots or recordings for a UI choice. Keep prototypes isolated and within the requested scope.

Use a prototype to answer an empirical question. Do not adversarially polish an abstract plan while the crucial assumption is still untested.

For a shared package or API, ask for a README or tutorial before implementation when useful. That caller-facing document becomes a target for proof.

After the design is settled, ask for a plan of small units. Each unit ends in an observable check. A plan-only request does not authorize implementation or PR creation.

## Keep follow-ups short

"Do it", "continue", and "keep going until done" are complete follow-ups when the conversation already holds the scope and authorization. They do not grant unrelated permissions.

Say "new task" when the subject changes. Say "read-only" when a new question should not continue the previous edit.

## Before stepping away

State a concrete goal, a checkable finish condition, permitted actions, and a stopping rule. Ask for a fresh worktree off a named base when isolation is useful. Request a local decision trail for later review.

Authorize commits or external actions explicitly if they are part of the task. Unattended work does not remove deployment, deletion, billing, global-installation, or merge gates. If a gate cannot be resolved without the user, preserve state and report it.

Confirm the verification path works before relying on an unattended run. On explicit repository initialization or the first editable task, create and prove a relevant task-specific skill unless the user opted out. Initialization without another task uses the primary documented surface. Reuse an existing relevant skill and wrap its harness. Formal verification remains explicitly selected.

Do not assume a scheduler, heartbeat, cloud worker, or persistence after the session ends. Continue while the active host supports execution. If blocked, keep the finish condition unchanged and write a precise handoff.

## Steer with one line

- "The goal is to reproduce the bug. I did not ask for a fix yet."
- "Apply prove it works. Show the real output, not just the build log."
- "Use subtract before you add. Remove the confirmed obsolete path before introducing another adapter."
- "Keep this read-only. Compare the options and let me decide."
- "The verification skill covers another feature. Build proof for the changed behavior."

A named principle is useful only after the agent reads its rule and ties it to an actual decision.
