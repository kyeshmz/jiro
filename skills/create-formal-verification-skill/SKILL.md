---
name: create-formal-verification-skill
description: Generate and prove a project-local formal verification skill for a high-risk invariant, race, parser, retry, or unsafe operation. Use when explicitly invoked as @create-formal-verification-skill or when the user selects formal verification beyond behavioral tests.
license: MIT
metadata:
  opencode/autoinvoke: false
---

# Create a formal verification skill

Give the user a checked property they can trust without learning the verification language. Leave the next maintainer one reproducible command and an honest account of its limits.

Read `references/shared-rules.md` before working. Resolve bundled resources from this skill's reported base directory. Write generated skills into `<target-repository>/.opencode/skills/<skill-id>/SKILL.md`, not this installed pack. Write a global skill only when explicitly requested.

If the target is an OpenCode configuration-root repository, use its existing top-level `skills/` layout instead of creating a nested `.opencode/` directory.

Formal verification is an explicit choice. It is not mandatory during initialization or every first task. A behavioral verification skill remains the default for a concrete editable task unless the user opts out. Reuse a relevant existing skill and wrap an existing harness rather than duplicating it. An unrelated verification skill does not cover this task. A read-only question or activation without a task creates no files.

## Choose a promise that matters

A test checks selected examples. Formal verification checks all cases in a stated model, all inputs within a bound, or all inputs covered by a proof. None of those claims means that the whole product is correct.

1. Read repository instructions, relevant changes, and the code that owns the promise. Preserve unrelated work.
2. Start in the area the user named. Otherwise find the promise whose failure harms users most and whose failure cases tests rarely reach.
3. State the property in one plain sentence. State the user harm in another sentence.
4. Name the code paths, state, inputs, concurrency, and external assumptions that the claim covers.

Choose the strongest useful target, not the easiest demonstration. Ask only for intent or authorization that source and runtime evidence cannot settle.

## Let the question choose the tool

Use the least costly tool that answers the actual question.

| Question | Candidate approach |
| --- | --- |
| Can events occur in an unsafe order? | Model-check a small, faithful design model. TLA+ can fit concurrent or distributed designs. |
| Can this implementation overflow, violate memory safety, or break a data-structure invariant? | Use a verifier that checks the implementation where practical. |
| Does the property hold for every size when a finite bound is insufficient? | Use an unbounded proof or proof assistant. |
| Is the relevant tool already part of the repository? | Reuse it before introducing another toolchain. |

Check the target language, tool version, licensing, and local runtime. Prefer a tool maintainers can reproduce. Explain the choice and rejected alternatives briefly. Installing a tool globally, starting a separately billable service, or uploading private source needs authorization. If the required tool is unavailable, report the blocker. Do not substitute an unexecuted model for proof.

## Build checks that can fail

- Trace every modeled state and transition to concrete source paths and symbols. Use the repository's nouns.
- Match atomic steps to actual atomic operations. Do not hide an interleaving inside a modeled indivisible step.
- Name bounds, fairness assumptions, environment behavior, trusted primitives, and excluded failure modes.
- Show each property fail on a broken variant. Remove a check or reorder a real step in isolated scratch work.
- Preserve a current-code failure as a finding. Explain the counterexample in the code's terms. Do not weaken the property, omit a transition, or change product code merely to make the check green.
- Distinguish an implementation defect from a modeling defect. Investigate the trace against the implementation before classifying either.
- Make the run cheap enough for relevant changes. Provide one command, a reproducible version, expected exit behavior, and a named evidence location.

Keep scratch mutations separate from user changes. Do not use a broad reset or checkout to undo them. Prefer an isolated copy or worktree whose creation is in scope. Cleanup must not remove findings or proof artifacts.

## Generate an agent-facing verification skill

Choose a unique ID such as `verify-<area>-formal` from the actual target. Match its directory and frontmatter name. Include a description with the verified area and change triggers. Leave no placeholder commands, paths, properties, or bounds in the generated output.

The generated skill must let a fresh agent do all of this:

1. Decide whether the current diff touches the verified code or an assumption.
2. Locate the implementation, model or proof, property, and their source correspondence.
3. Prepare the exact tool version and run the check with one documented command.
4. Read the result and preserve traces, logs, versions, and exit status.
5. Tell a real bug from a modeling error without relaxing the claim to obtain a pass.
6. Update the model when an intended code change alters its assumptions or transitions.
7. Repeat negative proof after a material verification change.

Add an enforceable drift signal when practical. A source fingerprint check, a targeted test, or a review gate can flag changes to mapped code. Explain what the signal detects and misses. A prose reminder alone is not automatic drift detection.

## Prove the generated instructions

Follow the generated skill cold, using its own commands.

1. Record the baseline result. It may contain a real finding.
2. Make an isolated scratch change that breaks the property in the real implementation.
3. Run the generated check and show that it catches that break. A model-only mutation does not replace this code-linked test.
4. Restore only the scratch change and rerun. Confirm the original passing result or the original findings.
5. Clean up run-owned processes and scratch state. Confirm the evidence still exists at the documented path.

If the check misses the break, repair the model, mapping, or instructions. Do not alter the mutation until an unrelated failure makes the check look useful. A generated skill that was not executed is a draft.

## Hand off

Report the property and user harm, tool and reason, code correspondence, bounds and assumptions, current findings, negative-proof result, exact rerun command, evidence paths, and exclusions. Tell counterexamples as short sequences of real operations. Suggest another target only when a close candidate emerged from the investigation.

Do not commit, push, open or merge a PR, deploy, or change product code without authorization. A formal finding does not authorize its fix.
