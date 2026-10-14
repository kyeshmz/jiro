import argparse
import json
import os
from pathlib import Path, PurePosixPath
import re
import subprocess
import sys
from urllib.parse import urlparse


def relative_path(value):
    if not isinstance(value, str) or not value or "\\" in value:
        raise ValueError("import paths must be repository-relative")
    if PurePosixPath(value).is_absolute() or any(part in ("", ".", "..") for part in value.split("/")):
        raise ValueError("import paths must be repository-relative")
    if any(ord(character) < 32 for character in value):
        raise ValueError("control characters are not allowed in import paths")
    return value


def contains(root, path):
    return path == root or path.startswith(root + "/")


def upstream_for(registry, entry):
    upstream = entry.get("upstream", registry.get("upstream"))
    if not isinstance(upstream, dict):
        raise ValueError("each import needs an upstream repository and ref")
    repository = upstream.get("repository")
    ref = upstream.get("ref")
    if not isinstance(repository, str) or not isinstance(ref, str) or not ref.strip():
        raise ValueError("each import needs an upstream repository and ref")
    parsed = urlparse(repository)
    if parsed.scheme != "https" or not parsed.netloc or not parsed.path.strip("/") or parsed.username or parsed.password or parsed.query or parsed.fragment:
        raise ValueError("upstream repository must be an HTTPS URL without credentials")
    if any(ord(character) < 32 for character in repository + ref):
        raise ValueError("control characters are not allowed in upstream metadata")
    return {"repository": repository, "ref": ref}


def source_pin_recorded(text, upstream, revision, path):
    repository = upstream["repository"].rstrip("/").removesuffix(".git")
    suffix = "/" + revision + "/" + path
    candidates = [repository + "/blob" + suffix, repository + "/tree" + suffix]
    parsed = urlparse(repository)
    if parsed.hostname == "github.com":
        candidates.append("https://raw.githubusercontent.com" + parsed.path + suffix)
    for url in re.findall(r'https://[^\s<>()\]`"]+', text):
        source = urlparse(url)._replace(query="", fragment="").geturl()
        if any(source == candidate or source.startswith(candidate + "/") for candidate in candidates):
            return True
    return False


def inspect(repo, registry, changed=()):
    if registry.get("version") != 1 or not registry.get("imports"):
        raise ValueError("unsupported or empty import map")
    records = set()
    identifiers = set()
    report = {"imports": [], "unmappedRecords": [], "baselineGaps": [], "errors": []}
    for entry in registry["imports"]:
        identifier = entry["id"]
        if identifier in identifiers:
            raise ValueError("duplicate import id")
        identifiers.add(identifier)
        upstream = upstream_for(registry, entry)
        record = relative_path(entry["record"])
        if record in records:
            raise ValueError("duplicate provenance record")
        records.add(record)
        roots = [relative_path(root) for root in entry["targetRoots"]]
        if not roots or not entry.get("sources") or not entry.get("preserve"):
            raise ValueError("each import needs targets, sources, and preservation rules")
        for path in set(roots + [record, relative_path(entry["license"])]):
            target = repo / path
            if not target.resolve().is_relative_to(repo.resolve()):
                raise ValueError("import path escapes the target repository")
            if not target.exists():
                report["errors"].append("missing target: " + path)
        record_text = (repo / record).read_text(encoding="utf-8") if (repo / record).is_file() else ""
        for source in entry["sources"]:
            relative_path(source["path"])
            if source["path"] not in record_text:
                report["errors"].append("source path missing from provenance: " + record)
            for field in ("importedRevision", "reviewedThrough"):
                revision = source[field]
                if revision is not None and not re.fullmatch(r"[a-f0-9]{40}|[a-f0-9]{64}", revision):
                    raise ValueError("source revisions must be immutable commit hashes or null")
            revision = source["importedRevision"]
            if revision is None:
                report["baselineGaps"].append({"id": identifier, "source": source["path"]})
            elif not source_pin_recorded(record_text, upstream, revision, source["path"]):
                report["errors"].append("source pin or repository missing from provenance: " + record)
        report["imports"].append({
            "id": identifier,
            "upstream": upstream,
            "record": record,
            "sources": entry["sources"],
            "changedTargets": sorted(path for path in changed if any(contains(root, path) for root in roots)),
        })
    discovered = {
        path.relative_to(repo).as_posix()
        for pattern in (".opencode/skills/**/UPSTREAM.md", "playbook/**/*.UPSTREAM.md", "recipes/**/*.UPSTREAM.md")
        for path in repo.glob(pattern)
    }
    report["unmappedRecords"] = sorted(discovered - records)
    return report


def git(repo, *args):
    result = subprocess.run(
        ["git", "-c", "core.fsmonitor=false", "-c", "core.hooksPath=/dev/null", "-C", str(repo), *args],
        env={**os.environ, "GIT_OPTIONAL_LOCKS": "0"}, capture_output=True, check=False,
    )
    if result.returncode:
        raise ValueError("Git metadata could not be read; check the repository and local base ref")
    return result.stdout


def changed_paths(repo, base):
    revision = git(repo, "rev-parse", "--verify", "--end-of-options", base + "^{commit}").decode().strip()
    tracked = git(repo, "diff", "--no-ext-diff", "--no-textconv", "--name-only", "--no-renames", "-z", revision, "--", ".opencode", "playbook", "recipes")
    untracked = git(repo, "ls-files", "--others", "--exclude-standard", "-z", "--", ".opencode", "playbook", "recipes")
    return sorted({path.decode("utf-8") for path in (tracked + untracked).split(b"\0") if path})


def main():
    parser = argparse.ArgumentParser(description="Read Jiro's import inventory without fetching or modifying files")
    parser.add_argument("--repo", type=Path, default=Path.cwd())
    parser.add_argument("--base", default="HEAD", help="local comparison ref; defaults to HEAD")
    args = parser.parse_args()
    try:
        repo = Path(git(args.repo, "rev-parse", "--show-toplevel").decode().strip())
        path = repo / "playbook/upstream-maintenance/references/import-map.json"
        registry = json.loads(path.read_text(encoding="utf-8"))
        report = inspect(repo, registry, changed_paths(repo, args.base))
        print(json.dumps(report, indent=2))
        return 1 if report["errors"] or report["unmappedRecords"] else 0
    except (OSError, ValueError, KeyError, TypeError) as error:
        print("inventory failed: " + str(error), file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
