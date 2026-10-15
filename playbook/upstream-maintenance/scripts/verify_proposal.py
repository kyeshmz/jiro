import json
from pathlib import Path
import sys

import inventory


REGISTRY = inventory.REGISTRY


def verify(repo, identifier):
    before = json.loads(inventory.git(repo, "show", f"HEAD:{REGISTRY}"))
    current = json.loads((repo / REGISTRY).read_text())
    packet = json.loads((repo / ".oc-port/context/packet.json").read_text())
    plan = packet["plan"]
    report = json.loads((repo / ".oc-port/result.json").read_text()) if plan["selections"] else {"decisions": []}
    expected = next(entry for entry in before["imports"] if entry["id"] == identifier)
    actual = next(entry for entry in current["imports"] if entry["id"] == identifier)
    upstream = inventory.upstream_for(expected)
    if packet["upstream"] != upstream:
        raise ValueError("packet repository does not match the selected import")
    if plan["selections"]:
        if [selection["id"] for selection in plan["selections"]] != [identifier]:
            raise ValueError("proposal contains another selection")
        if len(report["decisions"]) != 1 or report["decisions"][0]["selection"] != identifier:
            raise ValueError("proposal needs exactly one decision for the selected import")
        status = report["decisions"][0]["status"]
        if status not in ("applied", "skipped"):
            raise ValueError("blocked or invalid proposal")
        if plan["to"] not in actual["provenance"]:
            raise ValueError("selected review must record the actual upstream head in provenance")
    else:
        status = "unchanged"
    permitted = json.loads(json.dumps(before))
    replacement = next(entry for entry in permitted["imports"] if entry["id"] == identifier)
    if len(actual["sources"]) != len(expected["sources"]):
        raise ValueError("source scope changed")
    if status in ("applied", "skipped"):
        replacement["provenance"] = actual["provenance"]
    if status == "applied" and "fileHashes" in expected:
        replacement["fileHashes"] = actual["fileHashes"]
    for old, new, allowed in zip(expected["sources"], actual["sources"], replacement["sources"]):
        if status == "applied":
            if new["importedRevision"] != plan["to"] or new["reviewedThrough"] not in (None, plan["to"]):
                raise ValueError("applied source pins must identify the actual tested upstream head")
        elif status == "skipped":
            if new["importedRevision"] != old["importedRevision"] or new["reviewedThrough"] != plan["to"]:
                raise ValueError("skip must retain the imported pin and record the reviewed head")
        elif new != old:
            raise ValueError("unchanged source metadata must not advance")
        allowed["importedRevision"] = new["importedRevision"]
        allowed["reviewedThrough"] = new["reviewedThrough"]
    if current != permitted:
        raise ValueError("proposal changed unrelated metadata, source paths, mappings, or preservation rules")
    checked = inventory.inspect(repo, current)
    if checked["errors"] or checked["unmappedSkills"]:
        raise ValueError("proposal provenance or inventory is invalid: " + json.dumps(checked["errors"]))
    if any((repo / path).exists() for path in ("opencode.json", "opencode.jsonc", ".opencode/opencode.json", ".opencode/opencode.jsonc")):
        raise ValueError("proposal restored the removed MCP configuration")


def main():
    try:
        if len(sys.argv) != 2:
            raise ValueError("usage: verify_proposal.py <import-id>")
        verify(Path.cwd(), sys.argv[1])
        print("PASS: selected import provenance, scope, pins, and MCP-removal gate")
        return 0
    except (OSError, ValueError, KeyError, StopIteration) as error:
        print("proposal rejected: " + str(error), file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
