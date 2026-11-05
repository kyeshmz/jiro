#!/usr/bin/env python3
"""Find likely credentials in an OpenCode config folder without printing them.

  scan-secrets.py DIR            scan files on disk (skips .git, node_modules)
  scan-secrets.py --staged DIR   scan only what is staged for the next commit

Prints `file: location (reason)` per finding and exits 1 if anything is found.
Values are never printed.
"""
import json
import os
import re
import subprocess
import sys

KEY_NAME = re.compile(
    r"(api[_-]?key|apikey|token|secret|password|passwd|authorization|"
    r"private[_-]?key|client[_-]?secret|credential)",
    re.I,
)
VALUE_PATTERNS = [
    ("bearer token", re.compile(r"Bearer\s+[A-Za-z0-9._~+/=-]{20,}")),
    ("sk- key", re.compile(r"\bsk-[A-Za-z0-9_-]{20,}")),
    ("github token", re.compile(r"\bgh[pousr]_[A-Za-z0-9]{30,}")),
    ("slack token", re.compile(r"\bxox[abprs]-[A-Za-z0-9-]{10,}")),
    ("aws key", re.compile(r"\bAKIA[0-9A-Z]{16}\b")),
    ("private key", re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----")),
]
ASSIGN = re.compile(
    r"""["']?([A-Za-z0-9_.-]*)["']?\s*[:=]\s*["']([^"'\s]{12,})["']"""
)
SKIP_DIRS = {".git", "node_modules"}
REFERENCE = re.compile(r"\{(env|file):")


PLACEHOLDER = re.compile(
    r"(\$|<|\.\.\.|your|example|placeholder|xxx|here|encoded|changeme|redacted)", re.I
)


def literal(value: str) -> bool:
    return not REFERENCE.search(value)


def looks_real(value: str) -> bool:
    return not PLACEHOLDER.search(value) and re.search(r"\d", value) is not None


def scan_json(obj, path, out):
    if isinstance(obj, dict):
        for k, v in obj.items():
            scan_json(v, f"{path}.{k}", out)
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            scan_json(v, f"{path}[{i}]", out)
    elif isinstance(obj, str) and literal(obj):
        leaf = path.rsplit(".", 1)[-1]
        if KEY_NAME.search(leaf) and len(obj) >= 8 and looks_real(obj):
            out.append((path or ".", "secret-named key with a literal value"))
            return
        for reason, pat in VALUE_PATTERNS:
            if pat.search(obj):
                out.append((path or ".", reason))
                return


def scan_text(text, out):
    for n, line in enumerate(text.splitlines(), 1):
        if not literal(line):
            continue
        hit = None
        for reason, pat in VALUE_PATTERNS:
            if pat.search(line):
                hit = reason
                break
        if not hit:
            m = ASSIGN.search(line)
            if m and KEY_NAME.search(m.group(1)) and looks_real(m.group(2)):
                hit = "secret-named key with a literal value"
        if hit:
            out.append((f"line {n}", hit))


def scan_content(name, text):
    out = []
    if name.endswith(".json"):
        try:
            scan_json(json.loads(text), "", out)
            return out
        except ValueError:
            pass
    scan_text(text, out)
    return out


def disk_files(root):
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
        for f in filenames:
            p = os.path.join(dirpath, f)
            if os.path.getsize(p) <= 1_000_000:
                yield os.path.relpath(p, root), lambda p=p: open(p, "rb").read()


def staged_files(root):
    names = subprocess.run(
        ["git", "-C", root, "diff", "--cached", "--name-only", "--diff-filter=ACMR", "-z"],
        check=True, capture_output=True,
    ).stdout.decode().split("\0")
    for name in filter(None, names):
        yield name, lambda name=name: subprocess.run(
            ["git", "-C", root, "show", f":{name}"], check=True, capture_output=True
        ).stdout


def main():
    args = sys.argv[1:]
    staged = "--staged" in args
    args = [a for a in args if a != "--staged"]
    root = os.path.expanduser(args[0] if args else ".")
    found = 0
    for name, read in (staged_files if staged else disk_files)(root):
        raw = read()
        if b"\0" in raw[:4096]:
            continue
        for where, reason in scan_content(name, raw.decode("utf-8", "replace")):
            print(f"{name}: {where} ({reason})")
            found += 1
    sys.exit(1 if found else 0)


if __name__ == "__main__":
    main()
