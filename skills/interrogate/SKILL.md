---
name: interrogate
description: Challenge code or a design with independent adversarial reviewers and synthesize a pragmatic verdict without applying fixes. Use for @interrogate, adversarial review, multi-model review, challenge this, stress test this code, find blind spots, or tear this apart.
license: MIT
metadata:
  opencode/autoinvoke: false
---

# Interrogate

Find consequential defects and missed simplifications. The deliverable is a synthesized review, not automatic edits. Independent model families can reveal different blind spots when their selection is authorized. Reviewer personas are not a substitute for that diversity.

Read `references/shared-rules.md`. Resolve all references from the loaded skill base. Keep the whole review read-only. Explicitly forbid repository edits, commits, pushes, external writes, and nested delegation in child prompts. A request to challenge a change does not authorize fixing it.

## Scope

Use the files or diff the user names. For a feature branch, confirm the correct base and inspect the full changeset against it. Include relevant uncommitted work only when it belongs to the requested scope, and record the artifact state reviewed. Do not assume a branch named `main` or discard unrelated edits.

Gather surrounding callers, callees, types, dependency versions, tests, and known constraints. Package paths and context that let reviewers trace behavior beyond a diff.

## Intent

State the intended outcome in one paragraph using the user's request, relevant commit messages, PR description when available, and code. Separate explicit intent from inference. Resolve material uncertainty before dispatch. Do not ask a reviewer to judge an invented goal.

## Review

1. Read `references/reviewer-prompt.md`, `references/rubric.md`, and `references/code-quality-review.md` in full. Fill the same prompt template for every reviewer with the intent, exact artifact state, scope, constraints, and both lenses.
2. Use two fresh reviewer contexts by default. Load `swarm` or `delegate` for bounded briefs, records, and resource isolation. Label reviewers A, B, and onward. Do not assign competing personas to manufacture disagreement.
3. Inherit the current model by omitting `model`. Use distinct model families only when the user explicitly authorizes an override and the host confirms exact IDs. No separate role file or hard-coded defaults are required. If a requested model is unavailable, disclose that gap. Never silently substitute a guessed family default.
4. Use the host's native `subagent` tool with an advertised suitable `general`, `chef`, or permission-restricted review agent, a short `description`, and the completed `prompt`. Use `background: true` for independent reviewers. Do not pass arguments from another agent API or cloud runtime. Permissions come from the selected agent and explicit brief, not an invented argument.
5. Launch independent reviewers together within a sensible cap. Wait for completion notifications without polling. Readers must not race on mutable test resources. Allow only safe read-only checks or isolated scratch probes within the authorization boundary.

If delegation is unavailable, perform a local review and label it self-review. If all reviewers use one model family, label the coverage as same-family. Neither result fulfills a promised independent cross-model review. Report missing reviewers and do not invent their verdicts.

## Synthesize

Read every finding and its evidence. Merge duplicate mechanisms, retaining locations and which reviewers raised each. Independent agreement is a useful signal, not proof. Keep lone findings, especially correctness or security issues. Record explicit disagreements and investigate the disputed execution path.

Read `references/lead-judgment.md`. Act as the lead reviewer rather than a neutral vote counter. Put every finding in one bucket with its source reviewers and a short reason.

- **Act on.** A substantiated correctness, security, or maintainability issue that should block the actual change.
- **Consider.** A legitimate concern whose benefit may not justify addressing it now.
- **Noted.** Valid context or low-impact information without a present action.
- **Dismissed.** Incorrect, preference-only, or missing-context feedback with a concrete explanation.

Do not apply fixes. If the user later authorizes fixes, scope that as a separate implementation task and rerun relevant checks.

## Report

Keep these sections, even when a bucket has no findings.

1. **Intent.** The paragraph established before review.
2. **Reviewers.** Each label, actual model when known, finding count, completion status, and independence limits.
3. **Act on.** Each mechanism, location, evidence, source reviewers, and consequence.
4. **Consider.** Each concern, sources, and cost-benefit tradeoff.
5. **Noted.** Brief contextual findings.
6. **Dismissed.** Each dismissal with its reason.
7. **Agreement map.** Where reviewers agreed or diverged and what the verified evidence supports.

Include reviewed artifact state, checks actually run, and coverage gaps. Do not claim approval merely because reviewers returned no findings.
