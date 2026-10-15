import argparse
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import re
import subprocess
import sys
from urllib.parse import urlparse


REGISTRY = "upstream.json"


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


def upstream_for(entry):
    upstream = entry.get("upstream")
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
    if registry.get("version") != 2 or not registry.get("imports"):
        raise ValueError("unsupported or empty upstream catalog")
    identifiers = set()
    owners = {}
    report = {"imports": [], "unmappedSkills": [], "baselineGaps": [], "errors": []}
    for entry in registry["imports"]:
        identifier = entry["id"]
        if identifier in identifiers:
            raise ValueError("duplicate import id")
        identifiers.add(identifier)
        upstream = upstream_for(entry)
        if "record" in entry:
            raise ValueError("provenance belongs in upstream.json, not a separate record")
        provenance = entry.get("provenance")
        if not isinstance(provenance, str) or not provenance.strip():
            raise ValueError("each import needs provenance notes")
        roots = [relative_path(root) for root in entry["targetRoots"]]
        if not roots or not entry.get("sources") or not entry.get("preserve"):
            raise ValueError("each import needs targets, sources, and preservation rules")
        for root in roots:
            parts = PurePosixPath(root).parts
            if len(parts) > 1 and parts[0] == "skills":
                skill = "/".join(parts[:2])
                if skill in owners and owners[skill] != identifier:
                    raise ValueError("skill has multiple provenance owners: " + skill)
                owners[skill] = identifier
        for path in set(roots + [relative_path(entry["license"])]):
            target = repo / path
            if not target.resolve().is_relative_to(repo.resolve()):
                raise ValueError("import path escapes the target repository")
            if not target.exists():
                report["errors"].append("missing target: " + path)
        for source in entry["sources"]:
            relative_path(source["path"])
            if source["path"] not in provenance:
                report["errors"].append("source path missing from provenance: " + identifier)
            for field in ("importedRevision", "reviewedThrough"):
                revision = source[field]
                if revision is not None and not re.fullmatch(r"[a-f0-9]{40}|[a-f0-9]{64}", revision):
                    raise ValueError("source revisions must be immutable commit hashes or null")
            revision = source["importedRevision"]
            if revision is None:
                report["baselineGaps"].append({"id": identifier, "source": source["path"]})
            elif not source_pin_recorded(provenance, upstream, revision, source["path"]):
                report["errors"].append("source pin or repository missing from provenance: " + identifier)
        hashes = entry.get("fileHashes")
        if hashes is not None:
            if not isinstance(hashes, dict) or not hashes or len(roots) != 1:
                raise ValueError("file hashes need one bundle root and a nonempty SHA-256 map")
            bundle = repo / roots[0]
            for path, digest in hashes.items():
                relative_path(path)
                if not isinstance(digest, str) or not re.fullmatch(r"[a-f0-9]{64}", digest):
                    raise ValueError("file hashes must be SHA-256 digests")
                target = bundle / path
                if not target.resolve().is_relative_to(bundle.resolve()):
                    raise ValueError("hashed file escapes the bundle")
                if not target.is_file() or hashlib.sha256(target.read_bytes()).hexdigest() != digest:
                    report["errors"].append("bundle checksum mismatch: " + roots[0] + "/" + path)
            actual = {path.relative_to(bundle).as_posix() for path in bundle.rglob("*") if path.is_file()}
            for path in sorted(actual - set(hashes)):
                report["errors"].append("unrecorded bundle file: " + roots[0] + "/" + path)
        report["imports"].append({
            "id": identifier,
            "upstream": upstream,
            "sources": entry["sources"],
            "changedTargets": sorted(path for path in changed if path == REGISTRY or any(contains(root, path) for root in roots)),
        })
    discovered = {
        path.parent.relative_to(repo).as_posix()
        for path in repo.glob("skills/*/SKILL.md")
    }
    report["unmappedSkills"] = sorted(discovered - set(owners))
    for directory in ("skills", "recipes", "playbook"):
        for path in (repo / directory).rglob("*"):
            if path.name.endswith("UPSTREAM.md") or path.name == "import-manifest.json":
                report["errors"].append("retired provenance file: " + path.relative_to(repo).as_posix())
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
    paths = (REGISTRY, "skills", "commands", "agents", "scripts", "opencode.json", "opencode.jsonc", ".opencode", "playbook", "recipes")
    tracked = git(repo, "diff", "--no-ext-diff", "--no-textconv", "--name-only", "--no-renames", "-z", revision, "--", *paths)
    untracked = git(repo, "ls-files", "--others", "--exclude-standard", "-z", "--", *paths)
    return sorted({path.decode("utf-8") for path in (tracked + untracked).split(b"\0") if path})


def main():
    parser = argparse.ArgumentParser(description="Read Jiro's import inventory without fetching or modifying files")
    parser.add_argument("--repo", type=Path, default=Path.cwd())
    parser.add_argument("--base", default="HEAD", help="local comparison ref; defaults to HEAD")
    args = parser.parse_args()
    try:
        repo = Path(git(args.repo, "rev-parse", "--show-toplevel").decode().strip())
        path = repo / REGISTRY
        registry = json.loads(path.read_text(encoding="utf-8"))
        report = inspect(repo, registry, changed_paths(repo, args.base))
        print(json.dumps(report, indent=2))
        return 1 if report["errors"] or report["unmappedSkills"] else 0
    except (OSError, ValueError, KeyError, TypeError) as error:
        print("inventory failed: " + str(error), file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
