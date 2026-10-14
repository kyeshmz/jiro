---
name: worktree-cleanup
description: Use after a successful push or merge when finishing a task in a temporary Git worktree, or when asked to reclaim disk space from finished worktrees. Verify commit preservation and live usage, then remove only explicitly approved paths without discarding files or deleting branch refs.
---

# Worktree cleanup

Release finished worktrees so their checkouts and build artifacts do not linger on disk. Audit at the end of the task. A push or merge starts the audit, not an automatic deletion. This skill is an agent workflow, not a Git hook.

## 1. Identify the task's worktrees

Limit the audit to worktrees created or used for the current task. Inventory other worktrees only when the user requests a broader cleanup. Do not scan unrelated repositories or global OpenCode session storage.

Read repository instructions. Obtain exact paths from Git, not directory names or guesses. In the examples below, set each quoted variable from verified repository metadata before running it.

```bash
git -C "$repo" worktree list --porcelain -z
```

Parse the NUL-delimited records without splitting paths on whitespace. Record each candidate's path, HEAD, branch, lock state, and size. Measure available space on the candidate's filesystem with `df -k` and its allocated size with `du -sk`.

Never remove the main worktree, a bare repository, a locked worktree, or a checkout the user wants to retain. Age, a branch name, and a directory under a temporary folder are not deletion evidence.

## 2. Verify commit preservation

Record the candidate's exact HEAD. Local remote-tracking refs and the audit helper's merge buckets may be stale. Verify the relevant remote or merge result before proposing removal.

- **After a push.** Identify the actual push destination and full branch ref from the task's push result or verified configuration. Do not assume it is `origin` or the branch's upstream. Query that remote with `git ls-remote --exit-code "$remote" "$branch_ref"`. Match the returned ref exactly. Its tip must equal the candidate HEAD, or a freshly fetched tip must contain HEAD according to `git merge-base --is-ancestor`. A successful push of another branch or an earlier commit does not preserve this checkout's current HEAD.
- **After a merge.** Verify the target branch and refresh only the relevant refs, without pruning. Run `git merge-base --is-ancestor "$head" "$base_ref"` against the verified target tip. Exit status 0 proves ancestry. Status 1 means it is not an ancestor. Any other failure leaves preservation unverified.
- **After a squash or rebase merge.** Ancestry may fail even when the work was integrated. Inspect the specific merged PR and confirm its repository, target branch, and final source HEAD match this candidate. Keep the local branch ref. A merged PR with the same branch name is not enough, especially if commits were added afterward. Without reliable merge evidence, hold the worktree.
- **Detached HEAD.** Require a verified remote or retained ref containing HEAD. If only integration evidence exists, obtain approval to create a local preservation ref before removing the checkout. Do not rely on reflog expiry to preserve commits.

A pushed but unmerged PR can release its local checkout once local work is finished and its current HEAD is preserved. An open PR or a successful push does not by itself establish that local work is finished. Do not push, merge, force-push, or delete a branch just to make cleanup eligible. If network or hosting access fails, report the gap and hold the candidate.

## 3. Inspect files and live usage

For each candidate, inspect staged edits, unstaged edits, untracked files, and ignored files. Ordinary `git status` is not enough. Ignored artifacts can disappear during worktree removal too.

```bash
git -C "$worktree" status --porcelain=v1 --untracked-files=all --ignored -z
git -C "$worktree" diff --stat
git -C "$worktree" diff --cached --stat
```

Show relevant diffs for tracked edits. Name untracked and ignored paths. Treat `.env` files, local databases, recordings, test evidence, nested repositories, and build directories as user data until their ownership and disposability are verified. Do not assume all ignored files are caches. Inspect submodules separately and hold them if their state is uncertain.

Confirm no active session, child agent, editor task, development server, test run, deployment, or runtime needs the path. Review only known session IDs from the current task or a user-approved set. Historical session exports are not a live usage check. If usage cannot be observed, ask the user whether the exact paths are still in use. Missing evidence is a hold.

Finish the current task's writes and stop only processes owned by that task. If the current OpenCode session is rooted in the candidate, move it to the retained main checkout with `tools.opencode.session_move` before removal. Use the retained checkout as the shell working directory. If the session cannot be moved safely, hold the worktree.

## 4. Approve the exact deletion set

Present a short list or table with each exact path, branch and HEAD, preservation evidence, size, live usage result, and files that would be lost. Separate eligible candidates from held worktrees and state each hold reason.

Obtain explicit approval for the exact deletion set before removing anything. A request to write this skill, a successful push, a merge, or an audit bucket is not approval. Prior approval applies only to the named paths and reviewed contents. If HEAD, contents, or usage changes, invalidate that candidate's approval and review it again.

Hold tracked edits and untracked user files until they are preserved outside the candidate or the user explicitly approves discarding the identified contents. Ignored build artifacts may be included in an approved removal only after listing and reviewing them. Never silently stash, clean, reset, or relocate user files.

## 5. Remove only approved worktrees

Immediately before each removal, re-list the worktrees and re-check HEAD, lock state, all file categories, preservation evidence, and live usage. Stop on new or uncertain state.

Run from the retained checkout, using the exact path obtained from Git.

```bash
git -C "$repo" worktree remove -- "$worktree"
```

Keep branch refs, including merged or pushed branches. Do not use `git branch -d`, `git branch -D`, or remote branch deletion as part of this skill.

If Git refuses removal, report the reason and hold that path. Do not retry with `--force`, unlock a worktree, run `git clean`, or fall back to recursive deletion. Discarding identified dirty contents or handling submodules requires a separate, explicitly approved operation, not an automatic retry.

Successful removal needs no blanket prune. If missing worktrees leave stale registrations, run `git worktree prune --dry-run --verbose` and review the full affected set separately. Pruning is repository-wide. Do not run it unless its entire proposed set is approved and unavailable mounts or moved checkouts have been ruled out.

Do not expand cleanup to package caches, simulators, deployments, session data, logs, credentials, or unrelated directories.

## 6. Report the result

Re-list the worktrees and verify each removed path is gone while retained worktrees and branch refs still exist. Measure available space again on the same filesystems.

Report removed paths, preserved branch refs, measured before-and-after available space, and held paths with one reason each. Label pre-removal directory sizes as estimates of reclaimable space. Do not attribute the entire filesystem free-space change to cleanup when concurrent disk activity makes that uncertain.
