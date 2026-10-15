---
name: no-comments
description: Trim the garnish. Spawn Comment Sicko, remove unnecessary comments, fix accepted root-cause findings, and offer enforceable replacements for claimed constraints. Use when explicitly invoked as @no-comments or asked to clean up comments.
license: MIT
metadata:
  opencode/autoinvoke: false
---

# No comments

Bring a fresh comment-hater to the pass. Inspect the findings, remove accepted comments, and fix their in-scope root causes. Never polish a workaround into a shorter alibi.

## Scope

Use the caller's files or diff. Otherwise use the current diff against the caller's base branch, default `main`, including the working tree. Name the exact files and exclusions before dispatch. Preserve unrelated work. A read-only request permits a report, not comment deletion or code changes.

Resolve [references/reviewer-prompt.md](references/reviewer-prompt.md) from this skill's loaded base directory. Run project commands in the target repository, not in the installed tool directory.

## OpenCode execution

Use OpenCode's `subagent` tool. Select `comment-sicko` only when the host advertises that exact agent ID. Otherwise use `general` with the full bundled reviewer prompt. Neither path requires installing a custom agent or another pack.

Give the reviewer the original request, later constraints, absolute working directory, exact scope, and the full reviewer rules. Explicitly forbid file edits, commits, child launches, and external writes. The reviewer returns deletion candidates and flags; the parent owns all accepted edits. A read-only prompt is not a sandbox, so inspect the actual result and reject unauthorized writes.

Start a fresh child. Omit `model` unless the user or applicable host instructions authorize a choice confirmed by the host's model catalog. Do not read or change unrelated global model policy. Use background execution only for independent work and wait for completion notifications rather than polling.

When the caller is following a pstack workflow, honor its existing host-authorized per-role settings. Read only the role configuration that the host instructions require, confirm the exact model ID, and omit `model` for `auto`, `inherit-parent`, missing roles, or unavailable configured models. Report requested-model fallbacks and never change those settings as part of review.

## Steps

1. **Inspect.** Spawn the scoped reviewer with its bundled rules. Defer to its fresh perspective, then verify its evidence yourself.
2. **Accept or reject.** Inspect the report and actual diff. Reject application-code edits by the reviewer, scope escapes, exception-protected deletion proposals, misstated `MUST KILL` reasons, and flags that treat intentional kept code as guilty. Audit missed scoped lint and TypeScript suppressions. Correctness and safety suppressions remain actionable until their root causes are fixed. Before accepting thin `IMPORTANT` or `do not remove` findings, load `how` or `why` on the named symbol. Keep uncertain exception-protected comments untouched and report the missing proof. Rerun one rejected report with a fresh child and the failure named. Reject a second, report it open, and fail the tool. Never reset or discard user changes to retry.
3. **Shape.** Delete accepted narration, banners, commented-out code, and unsupported workaround prose when editing is authorized. Fix trivial accepted flags directly with a dead-path deletion, parameter removal, or the real API. For structural fixes, load `how`, settle caller usage and the smallest target shape, and sketch the accepted set before implementation. Use `architect` only if the host actually provides it. Do not require unbundled principle skills.
4. **Fix and taste.** Implement the smallest root-cause fix inside the fence. Remove named workarounds only as part of a verified fix. If the root cause is out of scope, make only the justified in-scope change and report the rest open. Do not bolt on symptom guards. Inspect the diff and run the scoped checks. Removing a correctness suppression without fixing the error is not a pass.
5. **Encode constraints.** Comments such as `do not remove`, `do not change wording`, or `talk to X before changing` need evidence, not automatic obedience or deletion. Keep proven exceptions about things we cannot change. Offer the cheapest in-scope type, runtime check, behavioral test, or CI lint for an accepted constraint. Wait for interactive approval before adding that enforcement; unattended work requires caller pre-approval. If approved, encode, verify, then delete the redundant comment. Otherwise remove only authorized non-exception comments and report unenforced constraints or out-of-scope work open.
6. **Serve.** Report comments actually deleted, protected keeps, any of your own deletions restored, rejected reports and reruns, design sketches, accepted root-cause fixes, encoding offers, approved encodings, unenforced constraints, checks actually run, and remaining work. In read-only mode, distinguish proposed deletions from actual deletions and skip editing steps with a reason. Do not call blocked verification a pass.

Restore only edits you made, using exact exception evidence. Never use a broad checkout revert to recover one comment. Tool invocation does not authorize commits, pushes, global installation, PRs, deployment, or unrelated external writes.
