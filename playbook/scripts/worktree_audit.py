#!/usr/bin/env python3
import argparse
import datetime
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import time


def run(command, cwd):
    env = os.environ.copy()
    # Git status can refresh the index unless optional locking is disabled.
    env["GIT_OPTIONAL_LOCKS"] = "0"
    try:
        return subprocess.run(command, cwd=cwd, env=env, capture_output=True, timeout=60)
    except (OSError, subprocess.TimeoutExpired):
        return subprocess.CompletedProcess(command, 1, b"", b"")


def git(cwd, *args):
    return run(["git", "-C", str(cwd), *args], cwd)


def text(result):
    return os.fsdecode(result.stdout).strip() if result.returncode == 0 else ""


def worktrees(repo):
    result = git(repo, "worktree", "list", "--porcelain", "-z")
    if result.returncode != 0:
        raise ValueError("could not list Git worktrees")
    entries = []
    for record in result.stdout.split(b"\0\0"):
        entry = {}
        for field in record.split(b"\0"):
            if field:
                key, _, value = os.fsdecode(field).partition(" ")
                entry[key] = value
        if "worktree" in entry:
            entries.append(entry)
    return entries


def status_counts(path):
    result = git(path, "status", "--porcelain=v1", "--ignored", "-z")
    if result.returncode != 0:
        return None
    counts = {"tracked": 0, "untracked": 0, "ignored": 0}
    records = iter(result.stdout.split(b"\0"))
    for record in records:
        if not record:
            continue
        code = record[:2]
        if code == b"??":
            counts["untracked"] += 1
        elif code == b"!!":
            counts["ignored"] += 1
        else:
            counts["tracked"] += 1
            if b"R" in code or b"C" in code:
                next(records, None)
    return counts


def base_ref(repo, requested):
    candidates = [requested] if requested else [
        text(git(repo, "symbolic-ref", "--quiet", "refs/remotes/origin/HEAD")),
        "origin/main", "origin/master", "main", "master",
    ]
    for candidate in candidates:
        if candidate and git(repo, "rev-parse", "--verify", f"{candidate}^{{commit}}").returncode == 0:
            return candidate
    if requested:
        raise ValueError(f"base ref does not resolve to a commit: {requested}")
    return ""


def nested_strings(value):
    if isinstance(value, str):
        yield value
    elif isinstance(value, dict):
        for item in value.values():
            yield from nested_strings(item)
    elif isinstance(value, list):
        for item in value:
            yield from nested_strings(item)


def session_matches(exports, entries):
    matches = {entry["worktree"]: [] for entry in entries}
    roots = [Path(entry["worktree"]).resolve() for entry in entries]
    for export in exports:
        try:
            data = json.loads(Path(export).read_text())["data"]
            info = data["info"]
            session_id = info["id"]
            directory = info["location"]["directory"]
            if not isinstance(session_id, str) or not session_id.startswith("ses"):
                raise ValueError("invalid OpenCode session ID")
            location = Path(directory).resolve()
            if not any(location == root or root in location.parents for root in roots):
                raise ValueError("session location is outside the audited worktrees")
            updated = info["time"]["updated"]
            date = datetime.datetime.fromtimestamp(updated / 1000, datetime.timezone.utc).date().isoformat()
            values = [directory, *nested_strings(data["messages"])]
            for path in matches:
                pattern = re.compile(re.escape(path) + r'(?=$|[/\s"\x27`])')
                if any(pattern.search(value) for value in values):
                    matches[path].append((updated, f"{session_id}@{date}"))
        except (OSError, ValueError, KeyError, TypeError, OverflowError) as error:
            print(f"warn: session export not used: {export}: {error}", file=sys.stderr)
    return {path: [label for _, label in sorted(items, reverse=True)] for path, items in matches.items()}


def pull_requests(repo, enabled):
    if not enabled:
        return None
    result = run([
        "gh", "pr", "list", "--state", "all", "--limit", "1000",
        "--json", "number,state,headRefName,headRefOid",
    ], repo)
    if result.returncode != 0:
        print("warn: PR state unavailable; gh is missing or its query failed", file=sys.stderr)
        return None
    try:
        values = json.loads(result.stdout)
        if not isinstance(values, list):
            raise ValueError("expected a PR list")
        return values
    except ValueError:
        print("warn: PR state unavailable; gh returned invalid JSON", file=sys.stderr)
        return None


def cell(value):
    value = str(value).replace("\t", "\\t").replace("\n", "\\n").replace("\r", "\\r")
    return "'" + value if value.startswith(("=", "+", "-", "@")) else value


def audit_row(repo, entry, base, prs, sessions):
    path = entry["worktree"]
    size_text = text(run(["du", "-sk", path], repo))
    try:
        size_kib = int(size_text.split("\t", 1)[0])
    except ValueError:
        size_kib = -1
    head = entry.get("HEAD", "")
    timestamp = text(git(path, "log", "-1", "--format=%ct", "HEAD"))
    age = f"{max(0, (int(time.time()) - int(timestamp)) // 86400)}d" if timestamp.isdigit() else "?"
    branch = entry.get("branch", "").removeprefix("refs/heads/")
    merged = "unknown"
    if base and head:
        result = git(repo, "merge-base", "--is-ancestor", head, base)
        if result.returncode in (0, 1):
            merged = "YES" if result.returncode == 0 else "no"
    counts = status_counts(path)
    dirty = "unreadable" if counts is None else ",".join(f"{key}:{value}" for key, value in counts.items())
    upstream = text(git(path, "rev-parse", "--abbrev-ref", "--symbolic-full-name", "@{upstream}"))
    remote = "detached" if not branch else "no-upstream"
    if upstream:
        ahead = text(git(path, "rev-list", "--count", f"{upstream}..HEAD"))
        behind = text(git(path, "rev-list", "--count", f"HEAD..{upstream}"))
        remote = f"ahead:{ahead},behind:{behind}" if ahead and behind else "unknown"
    branch_prs = [pr for pr in (prs or []) if pr.get("headRefName") == branch]
    pr_state = "unknown" if prs is None else ",".join(f"#{pr['number']}/{pr['state']}" for pr in branch_prs) or "not-found-in-page"
    if any(pr.get("state") == "MERGED" and pr.get("headRefOid") == head for pr in branch_prs):
        merged = "PR"
    if "locked" in entry:
        bucket = "hold-locked"
    elif counts is None:
        bucket = "hold-unreadable"
    elif counts["tracked"]:
        bucket = "hold-wip"
    elif counts["untracked"]:
        bucket = "review-untracked"
    elif counts["ignored"]:
        bucket = "review-ignored"
    elif any(pr.get("state") == "OPEN" for pr in branch_prs):
        bucket = "hold-open-pr"
    elif sessions:
        bucket = "review-session-usage"
    elif merged in ("YES", "PR"):
        bucket = "candidate-needs-usage-check"
    elif merged == "unknown":
        bucket = "hold-merge-unknown"
    else:
        bucket = "review-unmerged"
    row = [size_kib if size_kib >= 0 else "?", age, base or "unknown", merged, dirty, remote, pr_state, ",".join(sessions) or "unverified", bucket, path]
    return size_kib, row


def main():
    parser = argparse.ArgumentParser(description="Read-only worktree audit. No bucket authorizes deletion.")
    parser.add_argument("repo", nargs="?", default=".")
    parser.add_argument("--base", help="local ref used for merge checks; no fetch is performed")
    parser.add_argument("--with-prs", action="store_true", help="query PRs through gh; absent or truncated results remain inconclusive")
    parser.add_argument("--session-export", action="append", default=[], help="explicit OpenCode export file; never scans global storage")
    args = parser.parse_args()
    repo = Path(args.repo).resolve()
    if not repo.is_dir() or git(repo, "rev-parse", "--git-dir").returncode != 0:
        parser.error("not in a Git repository; pass a repository path")
    try:
        entries = worktrees(repo)
        base = base_ref(repo, args.base)
    except ValueError as error:
        parser.error(str(error))
    sessions = session_matches(args.session_export, entries)
    prs = pull_requests(repo, args.with_prs)
    rows = [audit_row(repo, entry, base, prs, sessions[entry["worktree"]]) for entry in entries[1:]]
    print("SIZE_KIB\tAGE\tBASE\tMERGED\tDIRTY\tUPSTREAM\tPR\tSESSION_MATCHES\tBUCKET\tWORKTREE")
    for _, row in sorted(rows, key=lambda item: item[0], reverse=True):
        print("\t".join(cell(value) for value in row))
    print("Session usage is unverified until checked live. Merge and upstream checks use local refs only. No bucket authorizes deletion.", file=sys.stderr)


if __name__ == "__main__":
    main()
