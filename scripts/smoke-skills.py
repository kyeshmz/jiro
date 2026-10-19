#!/usr/bin/env python3
"""Exercise installed Jiro skills through OpenCode V2 and retain outcomes."""

import argparse
import csv
import datetime
import json
import os
from pathlib import Path
import re
import shutil
import signal
import subprocess
import sys
import tempfile
import time
import uuid


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_MODEL = "opencode/muse-spark-1.3-contributor-free"
CASES = {
    "bro": "For this isolated fixture, use this supplied previous assistant reply as the input to restate: 'I will orchestrate the verification pipeline and serialize the resultant execution artifacts.' Preserve its meaning in plain language: run the tests and save the results. Do not explain the skill or add new work.",
    "code-organization": "Review design.py without editing it. Propose two distinct module shapes. Explain state ownership, public interfaces, private boundaries, and which alternative you reject.",
    "react-best-practices": "Review this supplied React performance scenario only: independent user and project fetches are awaited sequentially, and a filtered list is copied into state by an effect. Read the installed rules/async-parallel.md and rules/rerender-derived-state-no-effect.md. Propose parallel fetching and render-time derivation, with concrete rule references. Do not claim the Python fixture is a React app or that a benchmark ran. No files may be edited.",
    "composition-patterns": "Review this supplied React component API only: one Composer component uses isThread, isEditing, and isForwarding flags and passes internal state through every child. Read rules/architecture-avoid-boolean-props.md and rules/state-context-interface.md. Propose compound components or explicit variants with a provider owning state and a state/actions/meta context interface. The supplied target version is React 18, so explain that the React 19-only rule must be skipped. This is a review only; do not implement it.",
    "effect": "This Python-only fixture has no Effect dependency, local Effect source checkout, or packages/core test helpers. Network access, cloning, and project writes are forbidden. Apply the skill's source-of-truth gate: report the missing .opencode/references/effect source and do not supply unverified Effect API code. Explain why OpenCode's testEffect helper and packages/core test working directory cannot be assumed here. Do not introduce Effect or create a source checkout.",
    "minimize-reader-load": "Review design.py without editing it. Trace StoreAdapter to StoreProxy to Store. Identify both pass-through layers and duplicated mutable state. Propose a simpler shape and explain the remaining necessary complexity.",
    "principle-attack-the-premise": "Review this supplied scenario only: two fixes, increasing buffers and adding retries, both failed the same fairness check. They assumed workers receive equivalent work, but repeated observations show worker A holds 90 pending items while B and C hold 5 each. State the shared premise and the rerunnable per-actor census needed before another fix. Investigate how the role is assigned rather than compensating for it. No census script or fix may be written in this read-only test; distinguish the proposal from collected evidence.",
    "principle-build-the-lever": "Review a proposed twenty-file configuration-key rename done by hand or delegated to twenty workers. Propose the smallest codemod that can do or verify it. Explain how one hand-done unit becomes the comparison baseline and how the tool is made safe to rerun. This is planning only: do not write a tool or claim one was built.",
    "principle-fix-root-causes": "Review this supplied restart-failure scenario only: a version-2 state reader crashes on a persisted version-1 record. Suggested fixes are adding a nil check or deleting all caches. Give a reproduction and instrumentation plan, trace the schema mismatch, propose a cheap diagnostic signal, and explain why deleting user state needs approval. Do not claim the fixture app actually has this defect or change any files.",
    "principle-laziness-protocol": "Review design.py without editing it. Compare removing redundant StoreAdapter and StoreProxy layers with adding another abstraction. Propose the smallest change that removes duplicate decisions and preserves behavior. This is a read-only review, not permission to delete files or user state.",
    "principle-foundational-thinking": "For this read-only design proposal, tasks need stable IDs, fast lookup by ID, and concurrent readers while one actor updates task state. Choose the core types, data structures, dominant access patterns, and state owner before proposing business logic. Explain concurrency isolation and which verification scaffolding should come first. Do not implement the proposal.",
    "principle-redesign-from-first-principles": "Review a new multi-tenant requirement for a previously single-tenant task store. Treat tenant identity as a day-one assumption rather than threading an optional tenant flag through every layer. Propose the target data model, ownership, caller and schema changes, affected documentation, and small verified delivery steps. This is a proposal only; do not edit the fixture or claim a migration ran.",
    "principle-subtract-before-you-add": "Review an addition whose proposed base has unused wrappers, repeated internal validation, and documentation stubs with no novel content. Give a subtraction-first plan based on observed usage, preserve necessary boundary validation, and name the behavior checks needed before removal. No files or user state may be deleted in this read-only test.",
    "how": "Explain how notes.py parses commands, persists notes in JSON, and marks an item done. Use the skill's simple path and a read-only explainer. Cite the actual functions and files. Do not edit anything.",
    "why": "Investigate why notes.py keeps stable numeric IDs rather than using positions in the list. Consult the local Git history and distinguish direct evidence from inference. External MCP, hosting, and web sources are unavailable by test policy. Report those gaps. Use read-only investigators and synthesis as prescribed. Do not edit anything.",
    "show-me-your-work": "Keep decisions.tsv while examining the taskbook CLI. Log a concrete decision to use the documented CLI commands rather than edit its data file. Run the documented help command and record its actual result and evidence. Audit only this run's known session history. Use --standalone when invoking the OpenCode API. No other model family is authorized, so report the missing cross-model review honestly in Attention.",
    "reflect": "Reflect on this supplied fictional session digest, not the harness setup conversation. The prior transcript is unavailable; label digest-only evidence. Digest: a prior agent successfully loaded create-verification-skill, generated a verification skill for notes.py, and twice claimed that the CLI workflow passed without running it or checking evidence artifacts. The user corrected both claims. Review whether this calls for skill prose, structural enforcement, or rejection because the existing skill already covers it. Read the actual installed create-verification-skill before accepting any body edit. Complete all three review lenses and separate synthesis, even if they find no durable edits. Return Accepted, Rejected, and Backlog. No skill edits or external backlog filing are approved.",
    "create-verification-skill": "Generate and prove verify-taskbook for the CLI in notes.py. Use README.md's exact direct CLI commands with verification.json for isolation. Map add, list, and done. Write evidence under evidence/. Use those direct commands rather than creating a shell harness. Launch no persistent processes. Leave the proof artifacts intact.",
    "worktree-cleanup": "Audit the finished linked worktree listed by Git. Do not remove anything: no deletion is approved. Identify its untracked scratch.txt and ignored .env, verify the local merge evidence if possible, and explain why it must be held. No push, fetch, force, prune, or process stopping is authorized.",
}
CASES["principle-minimize-reader-load"] = (
    "This tests the compatibility entry point, not just the canonical behavior. First call the skill tool "
    "with id principle-minimize-reader-load. Then follow its instruction to load minimize-reader-load. "
    "Both successful loads must appear in this session; do not skip the first because it forwards to the second. "
    + CASES["minimize-reader-load"]
)
PACKAGING_ONLY = frozenset({
    "correct", "create-subagent", "delegate", "no-comments", "playwright-cli", "playwright-mcp", "swarm", "teach", "unslop",
} | (set(json.loads((ROOT / "upstream.json").read_text())["pstackMigration"]["skills"].values()) - set(CASES) - {"jiro"}))
NOTES = '''import argparse
import json
from pathlib import Path


def load(path):
    return json.loads(path.read_text()) if path.exists() else {"next_id": 1, "notes": []}


def save(path, state):
    path.write_text(json.dumps(state, indent=2) + "\\n")


def main():
    parser = argparse.ArgumentParser(description="taskbook CLI")
    parser.add_argument("--data", type=Path, required=True)
    commands = parser.add_subparsers(dest="command", required=True)
    commands.add_parser("add").add_argument("text")
    commands.add_parser("list")
    commands.add_parser("done").add_argument("id", type=int)
    args = parser.parse_args()
    state = load(args.data)
    if args.command == "add":
        state["notes"].append({"id": state["next_id"], "text": args.text, "done": False})
        state["next_id"] += 1
        save(args.data, state)
    elif args.command == "done":
        note = next((note for note in state["notes"] if note["id"] == args.id), None)
        if note is None:
            parser.error("unknown note ID")
        note["done"] = True
        save(args.data, state)
    print(json.dumps(state["notes"]))


if __name__ == "__main__":
    main()
'''
DESIGN = '''class Store:
    def __init__(self):
        self.items = []

    def list(self):
        return self.items


class StoreProxy:
    def __init__(self, store):
        self.store = store
        self.items = list(store.items)

    def list(self):
        return self.store.list()


class StoreAdapter:
    def __init__(self, proxy):
        self.proxy = proxy
        self.items = list(proxy.items)

    def list(self):
        return self.proxy.list()
'''
COMMANDS = [
    "python3 notes.py --help",
    "python3 notes.py --data verification.json add smoke",
    "python3 notes.py --data verification.json list",
    "python3 notes.py --data verification.json done 1",
]


def find_opencode(explicit):
    candidates = [explicit] if explicit else [
        os.environ.get("OPENCODE_BIN"), shutil.which("opencode2"), shutil.which("opencode"),
        str(Path.home() / ".opencode/bin/opencode2"), str(Path.home() / ".opencode/bin/opencode"),
    ]
    for candidate in candidates:
        if candidate and Path(candidate).is_file() and os.access(candidate, os.X_OK):
            return str(Path(candidate).resolve())
    raise ValueError("OpenCode CLI not found. Set --opencode or OPENCODE_BIN to the V2 binary.")


def run(command, cwd, timeout, env=None):
    process = subprocess.Popen(command, cwd=cwd, env=env, stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE, text=True, start_new_session=True)
    try:
        stdout, stderr = process.communicate(timeout=timeout)
        return process.returncode, stdout, stderr
    except (subprocess.TimeoutExpired, KeyboardInterrupt) as error:
        os.killpg(process.pid, signal.SIGTERM)
        try:
            stdout, stderr = process.communicate(timeout=5)
        except subprocess.TimeoutExpired:
            os.killpg(process.pid, signal.SIGKILL)
            stdout, stderr = process.communicate()
        if isinstance(error, KeyboardInterrupt):
            raise
        return 124, stdout, stderr + "\nOpenCode exceeded the per-case timeout.\n"


def git(directory, *args):
    env = os.environ.copy()
    env.update({"GIT_CONFIG_NOSYSTEM": "1", "GIT_CONFIG_GLOBAL": "/dev/null",
                "GIT_AUTHOR_NAME": "Jiro fixture", "GIT_AUTHOR_EMAIL": "fixture@example.invalid",
                "GIT_COMMITTER_NAME": "Jiro fixture", "GIT_COMMITTER_EMAIL": "fixture@example.invalid"})
    result = subprocess.run(["git", "-C", str(directory), *args], env=env,
                            capture_output=True, text=True, timeout=30, check=True)
    return result.stdout


def fixture(directory, skill):
    directory.mkdir()
    (directory / "notes.py").write_text(NOTES)
    (directory / "design.py").write_text(DESIGN)
    (directory / ".gitignore").write_text(".env\nverification.json\nevidence/\ndecisions.tsv\n.opencode/\n")
    (directory / "README.md").write_text(
        "# taskbook\n\nA short-lived Python CLI. No dependencies or server.\n\n"
        "Use these commands in order from this directory. They create one isolated note.\n\n"
        + "\n".join(f"```bash\n{command}\n```\n" for command in COMMANDS)
        + "\nverification.json is disposable fixture data. Evidence belongs under evidence/.\n")
    git(directory, "init", "-b", "main")
    git(directory, "add", "notes.py", "design.py", "README.md", ".gitignore")
    git(directory, "commit", "-m", "Use stable numeric note IDs so completing a note does not depend on list position")
    if skill == "worktree-cleanup":
        linked = directory.parent / "finished worktree"
        git(directory, "worktree", "add", "-b", "finished", str(linked))
        (linked / "scratch.txt").write_text("Untracked fixture data. Do not discard during the audit.\n")
        (linked / ".env").write_text("FIXTURE_ONLY=not-a-secret\n")
        return linked
    return None


def permissions(directory, installed, binary, writable):
    rules = [{"action": "*", "resource": "*", "effect": "deny"}]
    for action in ("read", "glob", "grep", "skill", "execute"):
        rules.append({"action": action, "resource": "*", "effect": "allow"})
    for path in (directory.parent, installed):
        rules.append({"action": "external_directory", "resource": str(path) + "/*", "effect": "allow"})
    for relative in writable:
        for path in (relative, str(directory / relative)):
            rules.append({"action": "edit", "resource": path, "effect": "allow"})
    shell = COMMANDS + ["df -k *", "du -sk *"]
    for command in ("status", "diff", "log", "show", "rev-parse", "merge-base", "for-each-ref"):
        shell.extend([f"git {command} *", f"git -C * {command} *"])
    shell.extend(["git worktree list *", "git -C * worktree list *"])
    helper = installed / "show-me-your-work/scripts/log.sh"
    shell.extend([f'bash "{helper}" decisions.tsv *', f"bash {helper} decisions.tsv *",
                  f'"{helper}" decisions.tsv *', f"{helper} decisions.tsv *"])
    for executable in (binary, "opencode", "opencode2"):
        for method in ("get", "GET"):
            shell.append(f"{executable} api --standalone {method} /api/experimental/session/ses*/export")
    rules.extend({"action": "shell", "resource": command, "effect": "allow"} for command in shell)
    return rules


def configure(directory, installed, binary, model, skill):
    writable = {"show-me-your-work": ["decisions.tsv", ".audit/*"],
                "create-verification-skill": [".opencode/skills/verify-taskbook/*", "evidence/*"]}.get(skill, [])
    rules = permissions(directory, installed, binary, writable)
    agents = {}
    for agent in ("skill-smoke", "general", "explore", "title", "summary", "compaction"):
        agent_rules = list(rules if agent == "skill-smoke" else permissions(directory, installed, binary, []))
        if agent == "skill-smoke":
            agent_rules.extend({"action": "subagent", "resource": child, "effect": "allow"}
                               for child in ("general", "explore"))
        agents[agent] = {"model": model, "steps": 24, "permissions": agent_rules}
        if agent == "skill-smoke":
            agents[agent]["mode"] = "primary"
    config = {"$schema": "https://opencode.ai/config.json", "model": model,
              "default_agent": "skill-smoke", "snapshots": False, "agents": agents}
    path = directory / ".opencode/opencode.json"
    path.parent.mkdir()
    path.write_text(json.dumps(config, indent=2) + "\n")


def parse_events(stdout):
    events = []
    for line in stdout.splitlines():
        try:
            event = json.loads(line)
        except json.JSONDecodeError:
            continue
        if isinstance(event, dict):
            events.append(event)
    return events


def transcript(data, session_id, directory):
    payload = data.get("data", data)
    info = payload["info"]
    if info["id"] != session_id or Path(info["location"]["directory"]).resolve() != directory.resolve():
        raise ValueError("Exported session does not match this test's ID and directory")
    return payload["messages"]


def loaded_skill_ids(messages):
    loaded = set()
    for message in messages:
        if message.get("type") == "skill" and isinstance(message.get("skill"), str):
            loaded.add(message["skill"])
        if message.get("type") != "assistant":
            continue
        for part in message.get("content", []):
            state = part.get("state", {})
            if part.get("type") == "tool" and part.get("name") == "skill" and state.get("status") == "completed":
                skill_id = state.get("input", {}).get("id")
                if isinstance(skill_id, str):
                    loaded.add(skill_id)
    return sorted(loaded)


def evidence(messages, skill):
    tools, texts = [], []
    for message in messages:
        if message.get("type") != "assistant":
            continue
        for part in message.get("content", []):
            if part.get("type") == "text":
                texts.append(part["text"])
            if part.get("type") == "tool" and part.get("state", {}).get("status") == "completed":
                tools.append(part)
    return skill in loaded_skill_ids(messages), tools, "\n".join(texts)


def validate(skill, directory, linked, messages):
    loaded, tools, text = evidence(messages, skill)
    failures = [] if loaded else [f"No successful load of {skill} appears in the session transcript"]
    if not text.strip():
        failures.append("No assistant output")
    requirements = {
        "bro": [r"(run|test|check)", r"(save|keep|record)", r"(result|happen|output)"],
        "code-organization": [r"(owner|ownership)", r"(interface|public)", r"(alternative|candidate|option)", r"(reject|prefer|choose|chosen)"],
        "react-best-practices": [r"(parallel|Promise\.all)", r"(deriv|render)", r"async-parallel", r"rerender-derived-state-no-effect"],
        "composition-patterns": [r"(compound|variant)", r"(provider|context)", r"state", r"actions", r"meta", r"React 18", r"(skip|avoid|not use|do not use|not apply)"],
        "effect": [r"\bv4\b", r"\.opencode/references/effect", r"(missing|unavailable|blocked|absent)", r"testEffect", r"packages/core"],
        "minimize-reader-load": [r"StoreAdapter", r"StoreProxy", r"(state|mutable)", r"(remove|collapse|eliminate|inline)"],
        "principle-attack-the-premise": [r"(premise|assumption)", r"census", r"(actor|worker)", r"(assign|role|rotate|random)"],
        "principle-build-the-lever": [r"codemod", r"(rerun|re.run|repeat|idempoten)", r"(compar|baseline|diff)", r"(propos|not built|not implemented|not created|planning)"],
        "principle-fix-root-causes": [r"(reproduc|failing)", r"(persist|state|schema|version)", r"(instrument|signal|log|diagnos)", r"(approval|approve|permission|not delet|no delet)"],
        "principle-laziness-protocol": [r"(delet|remov|inline|collaps)", r"(small|minimum|minimal|least)", r"(decision|source of truth|duplica)"],
        "principle-foundational-thinking": [r"(type|model|structur|shape)", r"(access|lookup|map|index)", r"(concurr|actor|isolat|shar)", r"(before|first|scaffold)"],
        "principle-redesign-from-first-principles": [r"tenant", r"(model|type|schema)", r"(caller|reference|doc)", r"(increment|step|verif|test)"],
        "principle-subtract-before-you-add": [r"(remov|delet|subtract|dead)", r"(before|first)", r"(behavio|contract|test|verif)", r"(boundar|input|validat)"],
        "how": [r"notes\.py", r"\bload\b", r"\bsave\b", r"(argparse|pars|command)", r"(json|persist)"],
        "why": [r"(stable|numeric)", r"(commit|git|history)", r"(direct|supported|evidence)", r"(unavailable|gap|not searched|not accessible)"],
        "show-me-your-work": [r"Attention", r"(unavailable|missing|not authorized|could not|not performed|not run)"],
        "reflect": [r"^## Accepted\b", r"^## Rejected\b", r"^## Backlog\b"],
        "worktree-cleanup": [r"scratch\.txt", r"\.env", r"(hold|held|retain|keep|not remov|no delet|blocked)"],
    }
    requirements["principle-minimize-reader-load"] = requirements["minimize-reader-load"]
    for pattern in requirements.get(skill, []):
        if not re.search(pattern, text, re.I | re.M):
            failures.append(f"Output missing case evidence matching {pattern}")
    if skill in ("how", "why") and not any(tool["name"] == "subagent" for tool in tools):
        failures.append("Required read-only delegation was not observed")
    delegates = [tool for tool in tools if tool["name"] == "subagent"]
    requested_rules = {
        "react-best-practices": ["rules/async-parallel.md", "rules/rerender-derived-state-no-effect.md"],
        "composition-patterns": ["rules/architecture-avoid-boolean-props.md", "rules/state-context-interface.md"],
    }
    for rule in requested_rules.get(skill, []):
        if not any(tool["name"] == "read" and tool["state"].get("input", {}).get("path", "").endswith(f"/{skill}/{rule}") for tool in tools):
            failures.append(f"Requested bundled rule was not read: {rule}")
    if skill == "principle-minimize-reader-load" and not evidence(messages, "minimize-reader-load")[0]:
        failures.append("Compatibility entry point did not load the canonical reader-load skill")
    if any(tool["state"].get("input", {}).get("background") for tool in delegates):
        failures.append("Background delegation was used despite this standalone test's foreground requirement")
    if skill == "why" and len(delegates) < 2:
        failures.append("Both investigation and separate synthesis delegation must complete")
    if skill == "reflect" and len(delegates) < 4:
        failures.append("All three reflection reviewers and separate synthesis must complete")
    if skill == "bro" and re.search(r"\b(orchestrat\w*|pipeline|serializ\w*|artifact\w*)\b", text, re.I):
        failures.append("Restatement retained jargon from the supplied reply")
    if skill == "effect":
        if (directory / ".opencode/references/effect").exists():
            failures.append("Effect source was created despite the source-access gate")
        if any(directory.rglob("*.ts")) or any(directory.rglob("*.tsx")):
            failures.append("Unverified Effect TypeScript code was generated")
    if skill == "show-me-your-work":
        logfile = directory / "decisions.tsv"
        rows = list(csv.reader(logfile.read_text().splitlines(), delimiter="\t")) if logfile.exists() else []
        if len(rows) < 2 or rows[0] != ["ts", "phase", "decision", "why", "evidence", "result"] or any(len(row) != 6 for row in rows):
            failures.append("A populated six-column decision log was not produced")
    if skill == "create-verification-skill":
        generated = directory / ".opencode/skills/verify-taskbook"
        skillfile = generated / "SKILL.md"
        body = skillfile.read_text() if skillfile.exists() else ""
        if not re.match(r"\A---\n.*?name:\s*verify-taskbook\n.*?description:\s*\S.*?\n---", body, re.S):
            failures.append("Generated verification skill has missing or invalid frontmatter")
        if not (generated / "features/README.md").exists() or len(list((generated / "features").glob("*.md"))) < 4:
            failures.append("Feature map does not include an index and three CLI features")
        statefile = directory / "verification.json"
        state = json.loads(statefile.read_text()) if statefile.exists() else {}
        if not any(note.get("text") == "smoke" and note.get("done") is True for note in state.get("notes", [])):
            failures.append("Documented add/list/done workflow was not completed")
        if not any(path.is_file() for path in (directory / "evidence").rglob("*")):
            failures.append("No retained proof artifact")
    if linked and (not linked.exists() or not (linked / "scratch.txt").exists() or not (linked / ".env").exists()):
        failures.append("Audit-only worktree or protected fixture files were removed")
    try:
        git(directory, "diff", "--exit-code")
        git(directory, "diff", "--cached", "--exit-code")
    except subprocess.CalledProcessError:
        failures.append("Tracked fixture files were changed")
    return failures, text


def write_report(output, report):
    temporary = output / ".summary.json.tmp"
    temporary.write_text(json.dumps(report, indent=2) + "\n")
    temporary.replace(output / "summary.json")


def api(binary, method, path, cwd, timeout, data=None, params=None, standalone=False):
    if params:
        if method != "GET" or path != "/api/session":
            raise ValueError("No verified operation ID for this parameterized API request")
        target = ["session.list"]
    else:
        target = [method, path]
    command = [binary, "api"] + (["--standalone"] if standalone else []) + target
    if data is not None:
        command.extend(["--data", json.dumps(data)])
    for key, value in (params or {}).items():
        command.extend(["--param", f"{key}={value}"])
    code, stdout, stderr = run(command, cwd, timeout)
    if code:
        raise ValueError(f"OpenCode {method} {path} failed with exit {code}")
    return json.loads(stdout) if stdout.strip() else None


def session_info(payload):
    return payload.get("data", payload)


def verify_test_session(info, case, output, report):
    expected_directory = Path(case["directory"]).resolve()
    expected_case = output.resolve() / case["skill"]
    if (expected_directory.name != "taskbook" or not expected_directory.parent.name.startswith("fixture-")
            or expected_directory.parent.parent != expected_case):
        raise ValueError("Recorded directory is not this report's generated test fixture")
    # Old reports retain their original title and ownership marker.
    titles = {f"Jiro smoke {case['skill']}": "jiro", f"KStack smoke {case['skill']}": "kstack"}
    brand = titles.get(info.get("title"))
    if (info.get("id") != case["session_id"] or info.get("parentID")
            or not brand
            or Path(info["location"]["directory"]).resolve() != expected_directory):
        raise ValueError("Session ID, title, parent, or directory no longer matches the test")
    marker = {"kind": f"{brand}-skill-smoke", "run_id": report.get("run_id"), "skill": case["skill"]}
    if report.get("run_id"):
        if (info.get("metadata") or {}).get(f"{brand}_smoke") != marker:
            raise ValueError("Session does not have this run's test ownership marker")
    else:
        saved = expected_case / "session.json"
        if not saved.is_file():
            raise ValueError("Legacy report has no saved ownership evidence")
        exported = json.loads(saved.read_text())
        original = exported.get("data", exported)["info"]
        if original.get("time", {}).get("updated") != info.get("time", {}).get("updated"):
            raise ValueError("Legacy test session changed after its result was recorded")


def session_family(binary, root, cwd, timeout):
    family, pending = {root["id"]: root}, [root["id"]]
    while pending:
        parent = pending.pop()
        cursor = None
        for _ in range(10):
            params = {"parentID": parent, "limit": 100}
            if cursor:
                params["cursor"] = cursor
            page = api(binary, "GET", "/api/session", cwd, timeout, params=params)
            for child in page["data"]:
                if child.get("parentID") != parent or child["id"] in family:
                    raise ValueError("Unexpected session in the scoped child-session listing")
                family[child["id"]] = child
                pending.append(child["id"])
            cursor = page.get("cursor", {}).get("next")
            if not cursor:
                break
        else:
            raise ValueError("Session family exceeds the cleanup page limit")
        if len(family) > 1000:
            raise ValueError("Session family exceeds the cleanup size limit")
    active = api(binary, "GET", "/api/session/active", cwd, timeout)["data"]
    if set(family) & set(active):
        raise ValueError("A test session or child session is still active")
    for info in family.values():
        if info["location"]["directory"] != root["location"]["directory"]:
            raise ValueError("A child session was moved outside the test fixture")
        times = info.get("time", {})
        if times.get("updated", 1) > times.get("idle", 0):
            raise ValueError("A session has no verified completed drain")
    return family


def clean_session(binary, case, output, report, cwd, timeout, confirmed):
    try:
        root = session_info(api(binary, "GET", f"/api/session/{case['session_id']}", cwd, timeout))
        verify_test_session(root, case, output, report)
        family = session_family(binary, root, cwd, timeout)
        versions = {session_id: info.get("time", {}).get("updated") for session_id, info in family.items()}
        if report.get("run_id") and not case.get("session_versions"):
            if not report.get("finished"):
                raise ValueError("Test session family was not captured before cleanup")
            cutoff = int(datetime.datetime.fromisoformat(report["finished"]).timestamp() * 1000)
            if any(updated is None or updated > cutoff for updated in versions.values()):
                raise ValueError("A test session changed after the interrupted run was recorded")
        if case.get("session_versions") and versions != case["session_versions"]:
            raise ValueError("The test session family changed after its outcome was recorded")
        if not report.get("run_id") and any(info.get("time", {}).get("updated", 0) > root["time"]["updated"] for info in family.values()):
            raise ValueError("A legacy child session changed after the parent test completed")
        result = {"status": "preview", "sessions": len(family)}
        if confirmed:
            code, stdout, stderr = run([binary, "session", "delete", case["session_id"]], cwd, timeout)
            if code:
                raise ValueError(f"Session deletion failed with exit {code}")
            result["status"] = "deleted"
        return result
    except (OSError, ValueError, KeyError, subprocess.SubprocessError) as error:
        return {"status": "held", "reason": str(error)}


def cleanup_report(binary, path, timeout, confirmed):
    if path.name != "summary.json":
        raise ValueError("--cleanup-from must name a summary.json produced by this runner")
    report = json.loads(path.read_text())
    output = path.parent.resolve()
    results = []
    seen = set()
    for original in report["cases"]:
        case = dict(original)
        if not case.get("session_id"):
            continue
        if case["session_id"] in seen or not re.fullmatch(r"ses[_a-zA-Z0-9]+", case["session_id"]):
            raise ValueError("Invalid or duplicate session ID in the report")
        seen.add(case["session_id"])
        if case.get("session_cleanup", {}).get("status") == "deleted":
            result = {"status": "already_deleted"}
        elif case["status"] in ("running", "not_run") or case["skill"] not in CASES:
            result = {"status": "held", "reason": "Test case is not completed or recognized"}
        else:
            if not case.get("directory"):
                invocation = json.loads((output / case["skill"] / "invocation.json").read_text())
                case["directory"] = invocation["cwd"]
            result = clean_session(binary, case, output, report, ROOT, timeout, confirmed)
        if confirmed and result["status"] == "deleted":
            original["session_cleanup"] = result
            write_report(output, report)
        results.append({"skill": case["skill"], "session_id": case["session_id"], **result})
        print(f"{result['status'].upper():8} {case['skill']} {case['session_id']}", flush=True)
    (output / "session-cleanup.json").write_text(json.dumps({"confirmed": confirmed, "cases": results}, indent=2) + "\n")
    return 1 if any(result["status"] == "held" for result in results) else 0


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--model", default=DEFAULT_MODEL)
    parser.add_argument("--opencode", help="Path to the OpenCode V2 CLI")
    parser.add_argument("--skill", action="append", choices=sorted(CASES), help="Run only this skill; repeatable")
    parser.add_argument("--skills-dir", type=Path, help="Installed global Jiro skills directory")
    parser.add_argument("--output", type=Path, help="New results directory; must not already exist")
    parser.add_argument("--timeout", type=int, default=300, help="Seconds per run or export")
    parser.add_argument("--dry-run", action="store_true", help="Print cases without invoking OpenCode")
    parser.add_argument("--keep-details", action="store_true", help="Retain transcripts and proof files for debugging")
    parser.add_argument("--delete-sessions", action="store_true", help="Delete this run's verified test sessions after recording their outcomes")
    parser.add_argument("--cleanup-from", type=Path, help="Preview cleanup of sessions recorded in an existing summary.json")
    parser.add_argument("--confirm-delete", action="store_true", help="Confirm deletion of the sessions named by --cleanup-from")
    args = parser.parse_args(argv)
    if args.timeout <= 0:
        parser.error("--timeout must be positive")
    if args.confirm_delete and not args.cleanup_from:
        parser.error("--confirm-delete requires --cleanup-from")
    if args.cleanup_from:
        if args.skill or args.delete_sessions or args.keep_details or args.output or args.dry_run:
            parser.error("Cleanup mode cannot be combined with run options")
        try:
            return cleanup_report(find_opencode(args.opencode), args.cleanup_from.resolve(), args.timeout, args.confirm_delete)
        except (OSError, ValueError, KeyError, subprocess.SubprocessError) as error:
            print(str(error), file=sys.stderr)
            return 2
    source = ROOT / "skills"
    names = list(dict.fromkeys(args.skill or sorted(path.name for path in source.iterdir() if path.is_dir() and path.name != "jiro")))
    missing = set(names) - CASES.keys()
    unknown = missing - PACKAGING_ONLY
    if unknown:
        parser.error("Add test cases for new skills: " + ", ".join(sorted(unknown)))
    if args.dry_run:
        print(f"Model: {args.model}")
        for name in names:
            if name in CASES:
                print(f"{name}: {CASES[name]}")
            else:
                print(f"{name}: NOT_RUN (packaging checks only; no live smoke case)")
        return 0
    if missing:
        parser.error("No live smoke cases for: " + ", ".join(sorted(missing))
                     + ". Use --skill to select supported cases; this is not a full-bundle live pass.")
    installed = (args.skills_dir or Path(os.environ.get("XDG_CONFIG_HOME") or str(Path.home() / ".config")) / "opencode/skills").resolve()
    try:
        binary = find_opencode(args.opencode)
        version = subprocess.run([binary, "--version"], capture_output=True, text=True, timeout=20, check=True).stdout.strip()
        if not re.search(r"\bv?2\.", version):
            raise ValueError(f"OpenCode V2 required; found {version}")
        for name in names:
            for path in (source / name).rglob("*"):
                if path.is_file() and (not (installed / name / path.relative_to(source / name)).is_file() or path.read_bytes() != (installed / name / path.relative_to(source / name)).read_bytes()):
                    raise ValueError(f"Installed {name} differs from Jiro. Run ./install.sh before testing.")
        parent = Path("/tmp/opencode")
        parent.mkdir(exist_ok=True)
        output = args.output.resolve() if args.output else Path(tempfile.mkdtemp(prefix="jiro-skill-smoke-", dir=parent))
        if args.output:
            output.mkdir(parents=True, exist_ok=False)
    except (ValueError, OSError, subprocess.SubprocessError) as error:
        print(str(error), file=sys.stderr)
        return 2
    report = {"model": args.model, "opencode": binary, "version": version,
              "run_id": uuid.uuid4().hex,
              "started": datetime.datetime.now(datetime.timezone.utc).isoformat(), "cases": [],
              "limitations": ["Explicit invocation smoke tests, not automatic selection or exhaustive evaluations.",
                              "External investigations and cross-model review are not covered.",
                              "Delegation runs in foreground; background notification delivery is not covered.",
                              "Worktree cleanup is audit-only; removal is explicitly denied."]}
    env = os.environ.copy()
    env["PATH"] = str(Path(binary).parent) + os.pathsep + env.get("PATH", "")
    blocked = None
    def interrupted(signum, frame):
        raise KeyboardInterrupt
    previous_handler = signal.signal(signal.SIGTERM, interrupted)
    write_report(output, report)
    try:
        for name in names:
            if blocked:
                report["cases"].append({"skill": name, "status": "not_run", "reason": blocked})
                write_report(output, report)
                print(f"NOT_RUN  {name}", flush=True)
                continue
            case_output = output / name
            case_output.mkdir()
            started = time.monotonic()
            result = {"skill": name, "status": "running", "failures": []}
            report["cases"].append(result)
            write_report(output, report)
            try:
                with tempfile.TemporaryDirectory(prefix="fixture-", dir=case_output) as temporary:
                    directory = Path(temporary) / "taskbook"
                    linked = fixture(directory, name)
                    configure(directory, installed, binary, args.model, name)
                    result["directory"] = str(directory)
                    metadata = {"jiro_smoke": {"kind": "jiro-skill-smoke", "run_id": report["run_id"], "skill": name}}
                    created = session_info(api(binary, "POST", "/api/session", directory, args.timeout,
                                               data={"title": f"Jiro smoke {name}", "agent": "skill-smoke", "metadata": metadata},
                                               standalone=True))
                    result["session_id"] = created["id"]
                    verify_test_session(created, result, output, report)
                    write_report(output, report)
                    prompt = (f"Load the exact skill {name} with the skill tool before doing the task. "
                              "Use only the fixture repository and installed skill resources. "
                              f"Only {args.model} is authorized for every agent; do not select other models. "
                              "This is a noninteractive standalone CLI test. Override background delegation with "
                              "foreground subagent calls (background false). Wait for every delegate and complete "
                              "the skill's synthesis before your final reply; do not end by saying you are waiting. "
                              "No external writes, network tools, commits, pushes, or deletion are authorized. "
                              + CASES[name])
                    command = [binary, "run", "--standalone", "--format", "json", "--auto", "--agent", "skill-smoke",
                               "--model", args.model, "--session", result["session_id"], "--title", f"Jiro smoke {name}", prompt]
                    if args.keep_details:
                        (case_output / "invocation.json").write_text(json.dumps({"command": command, "cwd": str(directory)}, indent=2) + "\n")
                    code, stdout, stderr = run(command, directory, args.timeout, env)
                    if args.keep_details:
                        (case_output / "events.jsonl").write_text(stdout)
                        (case_output / "stderr.log").write_text(stderr)
                    result["exit_code"] = code
                    events = parse_events(stdout)
                    errors = [event.get("error", {}) for event in events if event.get("type") == "error"]
                    session_ids = {event["sessionID"] for event in events if isinstance(event.get("sessionID"), str)}
                    if errors or code != 0:
                        result["status"] = "fail"
                        result["failures"] = [error.get("message", str(error)) for error in errors] or [f"CLI exited {code}"]
                        if any(error.get("type", "").startswith("provider.") for error in errors):
                            result["status"] = "blocked"
                            blocked = result["failures"][0]
                    elif session_ids != {result["session_id"]}:
                        result["status"] = "fail"
                        result["failures"] = ["No unambiguous session ID in the JSON event stream"]
                    else:
                        session_id = result["session_id"]
                        export_code, exported, export_error = run([binary, "session", "export", "--standalone", session_id], directory, args.timeout, env)
                        if args.keep_details:
                            (case_output / "session.json").write_text(exported)
                            (case_output / "export.stderr.log").write_text(export_error)
                        if export_code:
                            result["status"] = "fail"
                            result["failures"] = [f"Session export exited {export_code}"]
                        else:
                            messages = transcript(json.loads(exported), session_id, directory)
                            result["loaded_skills"] = loaded_skill_ids(messages)
                            failures, text = validate(name, directory, linked, messages)
                            result["failures"] = failures
                            result["status"] = "fail" if failures else "pass"
                            if args.keep_details:
                                (case_output / "response.md").write_text(text + "\n")
                    for relative in (("decisions.tsv", "verification.json", "evidence", ".opencode/skills") if args.keep_details else ()):
                        artifact = directory / relative
                        if artifact.is_dir():
                            shutil.copytree(artifact, case_output / "artifacts" / relative)
                        elif artifact.is_file():
                            target = case_output / "artifacts" / relative
                            target.parent.mkdir(parents=True, exist_ok=True)
                            shutil.copy2(artifact, target)
            except (OSError, ValueError, KeyError, subprocess.SubprocessError) as error:
                result["status"] = "fail"
                result["failures"] = [str(error)]
            result["seconds"] = round(time.monotonic() - started, 2)
            if result.get("session_id"):
                try:
                    root = session_info(api(binary, "GET", f"/api/session/{result['session_id']}", ROOT, args.timeout))
                    family = session_family(binary, root, ROOT, args.timeout)
                    result["session_versions"] = {session_id: info.get("time", {}).get("updated") for session_id, info in family.items()}
                except (OSError, ValueError, KeyError, subprocess.SubprocessError) as error:
                    result["session_cleanup"] = {"status": "held", "reason": str(error)}
            write_report(output, report)
            if args.delete_sessions and result.get("session_id"):
                result["session_cleanup"] = clean_session(binary, result, output, report, ROOT, args.timeout, True)
                write_report(output, report)
            if not args.keep_details and not any(case_output.iterdir()):
                case_output.rmdir()
            print(f"{result['status'].upper():8} {name}", flush=True)
    except KeyboardInterrupt:
        for case in report["cases"]:
            if case["status"] == "running":
                case["status"] = "interrupted"
                case["failures"] = ["Runner interrupted before this case completed"]
        completed = {case["skill"] for case in report["cases"]}
        report["cases"].extend({"skill": name, "status": "not_run", "reason": "Runner interrupted"}
                               for name in names if name not in completed)
    finally:
        signal.signal(signal.SIGTERM, previous_handler)
        report["finished"] = datetime.datetime.now(datetime.timezone.utc).isoformat()
        write_report(output, report)
        print(f"Results: {output / 'summary.json'}", flush=True)
    passed = len(report["cases"]) == len(names) and all(case["status"] == "pass" for case in report["cases"])
    cleanup_ok = not any(case.get("session_cleanup", {}).get("status") == "held" for case in report["cases"])
    return 0 if passed and cleanup_ok else 1


if __name__ == "__main__":
    sys.exit(main())
