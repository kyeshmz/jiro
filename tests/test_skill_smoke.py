import contextlib
import importlib.util
import io
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest import mock


ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("skill_smoke", ROOT / "recipes/scripts/smoke-skills.py")
smoke = importlib.util.module_from_spec(spec)
spec.loader.exec_module(smoke)


def messages(skill, text):
    return [{"type": "assistant", "content": [
        {"type": "tool", "name": "skill", "state": {"status": "completed", "input": {"id": skill}}},
        {"type": "text", "text": text},
    ]}]


class SmokeTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory(prefix="jiro-smoke-unit-", dir="/tmp/opencode")
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)

    def fake_cli(self, blocked=False, interrupted=False):
        script = self.root / "opencode"
        script.write_text("#!/usr/bin/env python3\n" + f'''
import json
import os
from pathlib import Path
import signal
import sys
import time

args = sys.argv[1:]
registry = Path(__file__).parent / "sessions.json"
if args == ["--version"]:
    print("opencode v2.0.27")
elif args[0] == "run":
    if {interrupted!r}:
        os.kill(os.getppid(), signal.SIGTERM)
        time.sleep(60)
    if {blocked!r}:
        print(json.dumps({{"type": "error", "sessionID": "ses_fixture", "error": {{"type": "provider.auth", "status": 403, "message": "Free tier unavailable"}}}}))
        sys.exit(1)
    print(json.dumps({{"type": "text", "sessionID": "ses_fixture"}}))
elif args[:2] == ["session", "export"]:
    print(json.dumps({{"data": {{"info": json.loads(registry.read_text()), "messages": {messages("minimize-reader-load", "Remove StoreAdapter and StoreProxy pass-through layers. Store owns the mutable state.")!r}}}}}))
elif args[:2] == ["session", "delete"]:
    (Path(__file__).parent / "deleted.txt").write_text(args[2])
    registry.unlink()
elif args[0] == "api":
    if "POST" in args and "/api/session" in args:
        body = json.loads(args[args.index("--data") + 1])
        info = {{"id": "ses_fixture", "title": body["title"], "metadata": body["metadata"],
                 "location": {{"directory": str(Path.cwd())}}, "time": {{"created": 1, "updated": 1, "idle": 1}}}}
        registry.write_text(json.dumps(info))
        print(json.dumps(info))
    elif "/api/session/active" in args:
        print(json.dumps({{"data": {{}}}}))
    elif "session.list" in args:
        print(json.dumps({{"data": [], "cursor": {{}}}}))
    elif "/api/session/ses_fixture" in args and registry.exists():
        print(registry.read_text())
    else:
        sys.exit(1)
else:
    sys.exit(2)
''')
        script.chmod(0o755)
        return script

    def installed(self):
        installed = self.root / "installed"
        shutil.copytree(ROOT / ".opencode/skills", installed)
        return installed

    def test_event_parser_ignores_noise(self):
        events = smoke.parse_events('banner\n{"type":"error","error":{"type":"provider.auth"}}\n[]\n')
        self.assertEqual(len(events), 1)
        self.assertEqual(events[0]["error"]["type"], "provider.auth")

    def test_load_claim_is_not_load_evidence(self):
        loaded, _, _ = smoke.evidence([{"type": "assistant", "content": [
            {"type": "text", "text": "I loaded minimize-reader-load"}
        ]}], "minimize-reader-load")
        self.assertFalse(loaded)

    def test_failed_or_wrong_skill_load_does_not_pass(self):
        wrong = messages("how", "Done")
        self.assertFalse(smoke.evidence(wrong, "minimize-reader-load")[0])
        wrong[0]["content"][0]["name"] = "skill"
        wrong[0]["content"][0]["state"] = {"status": "error", "input": {"id": "minimize-reader-load"}}
        self.assertFalse(smoke.evidence(wrong, "minimize-reader-load")[0])

    def test_transcript_checks_id_and_directory(self):
        data = {"data": {"info": {"id": "ses_fixture", "location": {"directory": str(self.root)}}, "messages": []}}
        self.assertEqual(smoke.transcript(data, "ses_fixture", self.root), [])
        with self.assertRaises(ValueError):
            smoke.transcript(data, "ses_other", self.root)
        with self.assertRaises(ValueError):
            smoke.transcript(data, "ses_fixture", self.root / "other")

    def test_config_pins_models_and_blocks_mutations(self):
        directory = self.root / "repo"
        directory.mkdir()
        smoke.configure(directory, self.root / "installed", "/usr/bin/opencode", smoke.DEFAULT_MODEL, "worktree-cleanup")
        config = json.loads((directory / ".opencode/opencode.json").read_text())
        for agent in config["agents"].values():
            self.assertEqual(agent["model"], smoke.DEFAULT_MODEL)
            self.assertEqual(agent["permissions"][0], {"action": "*", "resource": "*", "effect": "deny"})
            self.assertFalse(any(rule["action"] == "edit" and rule["effect"] == "allow" for rule in agent["permissions"]))
            shell = [rule["resource"] for rule in agent["permissions"] if rule["action"] == "shell"]
            self.assertFalse(any("worktree remove" in command or "push" in command or "rm " in command for command in shell))

    def test_minimize_case_requires_concrete_application(self):
        directory = self.root / "repo"
        smoke.fixture(directory, "minimize-reader-load")
        good = messages("minimize-reader-load", "Remove StoreAdapter and StoreProxy. Store owns the mutable state.")
        self.assertEqual(smoke.validate("minimize-reader-load", directory, None, good)[0], [])
        self.assertTrue(smoke.validate("minimize-reader-load", directory, None, messages("minimize-reader-load", "Looks fine"))[0])

    def test_bro_case_preserves_the_meaning_without_jargon(self):
        directory = self.root / "repo"
        smoke.fixture(directory, "bro")
        good = messages("bro", "I'll run the tests and save the results.")
        self.assertEqual(smoke.validate("bro", directory, None, good)[0], [])
        vague = messages("bro", "I'll do it.")
        self.assertTrue(smoke.validate("bro", directory, None, vague)[0])
        jargon = messages("bro", "I'll run the test pipeline and save the result artifacts.")
        self.assertIn("Restatement retained jargon from the supplied reply",
                      smoke.validate("bro", directory, None, jargon)[0])

    def test_reflect_case_requires_three_reviewers_and_synthesis(self):
        directory = self.root / "repo"
        smoke.fixture(directory, "reflect")
        output = messages("reflect", "## Accepted\nNone\n## Rejected\nAlready covered.\n## Backlog\nNone")
        self.assertIn("All three reflection reviewers and separate synthesis must complete",
                      smoke.validate("reflect", directory, None, output)[0])
        for lens in ("judgment", "tooling", "divergent", "synthesizer"):
            output[0]["content"].append({"type": "tool", "name": "subagent", "state": {
                "status": "completed", "input": {"agent": "general", "prompt": lens, "background": False}
            }})
        self.assertEqual(smoke.validate("reflect", directory, None, output)[0], [])

    def test_effect_case_reports_source_gap_without_generating_code(self):
        directory = self.root / "repo"
        smoke.fixture(directory, "effect")
        output = messages("effect", "Effect v4 source is missing at .opencode/references/effect. "
                          "The testEffect helper and packages/core working directory are OpenCode-specific.")
        self.assertEqual(smoke.validate("effect", directory, None, output)[0], [])
        (directory / "unverified.ts").write_text("// No verified Effect source.\n")
        self.assertIn("Unverified Effect TypeScript code was generated",
                      smoke.validate("effect", directory, None, output)[0])
        source = directory / ".opencode/references/effect"
        source.mkdir(parents=True)
        self.assertIn("Effect source was created despite the source-access gate",
                      smoke.validate("effect", directory, None, output)[0])

    def test_live_smoke_coverage_gaps_are_explicit(self):
        bundled = {path.name for path in (ROOT / ".opencode/skills").iterdir() if path.is_dir()}
        mode_smoke = (ROOT / "scripts/smoke-jiro.ts").read_text()
        self.assertIn('command: "jiro"', mode_smoke)
        self.assertIn('skills: ["jiro"]', mode_smoke)
        self.assertIn('skill: "jiro"', mode_smoke)
        self.assertTrue(set(smoke.CASES).issubset(bundled))
        self.assertEqual(bundled - set(smoke.CASES) - {"jiro"}, smoke.PACKAGING_ONLY)
        self.assertIn("no live cases in that runner", (ROOT / "README.md").read_text())

    def test_audit_keeps_protected_files(self):
        directory = self.root / "repo"
        linked = smoke.fixture(directory, "worktree-cleanup")
        output = messages("worktree-cleanup", "Hold the worktree. scratch.txt is untracked and .env is ignored.")
        self.assertEqual(smoke.validate("worktree-cleanup", directory, linked, output)[0], [])
        (linked / "scratch.txt").unlink()
        self.assertTrue(smoke.validate("worktree-cleanup", directory, linked, output)[0])

    def test_fixture_cli_runs_the_documented_user_path(self):
        directory = self.root / "repo"
        smoke.fixture(directory, "create-verification-skill")
        for command in smoke.COMMANDS:
            result = subprocess.run(command.split(), cwd=directory, capture_output=True, text=True, check=True)
            self.assertTrue(result.stdout.strip())
        state = json.loads((directory / "verification.json").read_text())
        self.assertEqual(state, {"next_id": 2, "notes": [{"id": 1, "text": "smoke", "done": True}]})

    def test_verification_case_rejects_unproven_artifacts(self):
        directory = self.root / "repo"
        smoke.fixture(directory, "create-verification-skill")
        failures, _ = smoke.validate("create-verification-skill", directory, None,
                                     messages("create-verification-skill", "Generated and tested everything"))
        self.assertEqual(len(failures), 4)

    def test_tracked_edits_are_not_silently_accepted(self):
        directory = self.root / "repo"
        smoke.fixture(directory, "minimize-reader-load")
        (directory / "notes.py").write_text("changed\n")
        good = messages("minimize-reader-load", "Remove StoreAdapter and StoreProxy. Store owns the mutable state.")
        self.assertIn("Tracked fixture files were changed", smoke.validate("minimize-reader-load", directory, None, good)[0])

    def test_background_delegation_does_not_count_as_completed_work(self):
        directory = self.root / "repo"
        smoke.fixture(directory, "how")
        output = messages("how", "notes.py uses argparse commands, load and save to persist JSON.")
        output[0]["content"].append({"type": "tool", "name": "subagent", "state": {
            "status": "completed", "input": {"background": True}
        }})
        failures, _ = smoke.validate("how", directory, None, output)
        self.assertTrue(any("Background delegation" in failure for failure in failures))

    def test_provider_failure_blocks_remaining_cases(self):
        binary = self.fake_cli(blocked=True)
        output = self.root / "results"
        with contextlib.redirect_stdout(io.StringIO()):
            status = smoke.main(["--opencode", str(binary), "--skills-dir", str(self.installed()), "--output", str(output),
                                 "--skill", "minimize-reader-load", "--skill", "how"])
        report = json.loads((output / "summary.json").read_text())
        self.assertEqual(status, 1)
        self.assertEqual([case["status"] for case in report["cases"]], ["blocked", "not_run"])
        self.assertFalse(list(output.glob("*/fixture-*")))
        self.assertEqual(sorted(path.name for path in output.iterdir()), ["summary.json"])

    def test_runner_exports_and_checks_real_transcript_shape(self):
        binary = self.fake_cli()
        output = self.root / "results"
        with contextlib.redirect_stdout(io.StringIO()):
            status = smoke.main(["--opencode", str(binary), "--skills-dir", str(self.installed()), "--output", str(output),
                                 "--skill", "minimize-reader-load", "--keep-details"])
        report = json.loads((output / "summary.json").read_text())
        self.assertEqual(status, 0)
        self.assertEqual(report["cases"][0]["status"], "pass")
        self.assertTrue((output / "minimize-reader-load/session.json").exists())
        self.assertTrue((output / "minimize-reader-load/response.md").exists())
        self.assertFalse(list(output.glob("*/fixture-*")))

    def test_summary_only_run_and_explicit_session_deletion(self):
        binary = self.fake_cli()
        output = self.root / "results"
        with contextlib.redirect_stdout(io.StringIO()):
            status = smoke.main(["--opencode", str(binary), "--skills-dir", str(self.installed()), "--output", str(output),
                                 "--skill", "minimize-reader-load", "--delete-sessions"])
        report = json.loads((output / "summary.json").read_text())
        self.assertEqual(status, 0)
        self.assertEqual(report["cases"][0]["status"], "pass")
        self.assertEqual(report["cases"][0]["session_cleanup"]["status"], "deleted")
        self.assertEqual(sorted(path.name for path in output.iterdir()), ["summary.json"])
        self.assertEqual((self.root / "deleted.txt").read_text(), "ses_fixture")

    def test_cleanup_preview_never_deletes_and_confirmation_is_idempotent(self):
        binary = self.fake_cli()
        output = self.root / "results"
        with contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(smoke.main(["--opencode", str(binary), "--skills-dir", str(self.installed()), "--output", str(output),
                                        "--skill", "minimize-reader-load"]), 0)
            self.assertEqual(smoke.main(["--opencode", str(binary), "--cleanup-from", str(output / "summary.json")]), 0)
        self.assertFalse((self.root / "deleted.txt").exists())
        with contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(smoke.main(["--opencode", str(binary), "--cleanup-from", str(output / "summary.json"), "--confirm-delete"]), 0)
            self.assertEqual(smoke.main(["--opencode", str(binary), "--cleanup-from", str(output / "summary.json"), "--confirm-delete"]), 0)
        report = json.loads((output / "summary.json").read_text())
        self.assertEqual(report["cases"][0]["status"], "pass")
        self.assertEqual(report["cases"][0]["session_cleanup"]["status"], "deleted")

    def test_cleanup_refuses_unrelated_or_changed_sessions(self):
        output = self.root / "results"
        directory = output / "minimize-reader-load/fixture-example/taskbook"
        case = {"skill": "minimize-reader-load", "session_id": "ses_fixture", "directory": str(directory)}
        report = {"run_id": "run-example"}
        info = {"id": "ses_fixture", "title": "Normal conversation", "location": {"directory": str(directory)},
                "metadata": {"jiro_smoke": {"kind": "jiro-skill-smoke", "run_id": "run-example", "skill": "minimize-reader-load"}}}
        with self.assertRaises(ValueError):
            smoke.verify_test_session(info, case, output, report)
        info["title"] = "Jiro smoke minimize-reader-load"
        info["metadata"]["jiro_smoke"]["run_id"] = "other-run"
        with self.assertRaises(ValueError):
            smoke.verify_test_session(info, case, output, report)

    def test_cleanup_preserves_ownership_checks_across_rename(self):
        output = self.root / "results"
        directory = output / "minimize-reader-load/fixture-example/taskbook"
        case = {"skill": "minimize-reader-load", "session_id": "ses_fixture", "directory": str(directory)}
        report = {"run_id": "run-example"}
        for title, brand in (("Jiro", "jiro"), ("KStack", "kstack")):
            with self.subTest(brand=brand):
                marker = {"kind": f"{brand}-skill-smoke", "run_id": "run-example", "skill": case["skill"]}
                info = {"id": case["session_id"], "title": f"{title} smoke {case['skill']}",
                        "location": {"directory": str(directory)}, "metadata": {f"{brand}_smoke": marker}}
                smoke.verify_test_session(info, case, output, report)
                marker["run_id"] = "other-run"
                with self.assertRaises(ValueError):
                    smoke.verify_test_session(info, case, output, report)
                marker["run_id"] = report["run_id"]
                info["title"] = f"{'KStack' if brand == 'jiro' else 'Jiro'} smoke {case['skill']}"
                with self.assertRaises(ValueError):
                    smoke.verify_test_session(info, case, output, report)

    def test_session_family_changed_after_test_is_held(self):
        binary = self.fake_cli()
        output = self.root / "results"
        with contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(smoke.main(["--opencode", str(binary), "--skills-dir", str(self.installed()), "--output", str(output),
                                        "--skill", "minimize-reader-load"]), 0)
        registry = self.root / "sessions.json"
        info = json.loads(registry.read_text())
        info["time"].update({"updated": 2, "idle": 2})
        registry.write_text(json.dumps(info))
        with contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(smoke.main(["--opencode", str(binary), "--cleanup-from", str(output / "summary.json"), "--confirm-delete"]), 1)
        self.assertFalse((self.root / "deleted.txt").exists())
        cleanup = json.loads((output / "session-cleanup.json").read_text())
        self.assertEqual(cleanup["cases"][0]["status"], "held")

    def test_rejected_test_can_be_deleted_without_losing_its_outcome(self):
        binary = self.fake_cli(blocked=True)
        output = self.root / "results"
        with contextlib.redirect_stdout(io.StringIO()):
            status = smoke.main(["--opencode", str(binary), "--skills-dir", str(self.installed()), "--output", str(output),
                                 "--skill", "minimize-reader-load", "--delete-sessions"])
        self.assertEqual(status, 1)
        report = json.loads((output / "summary.json").read_text())
        self.assertEqual(report["cases"][0]["status"], "blocked")
        self.assertEqual(report["cases"][0]["failures"], ["Free tier unavailable"])
        self.assertEqual(report["cases"][0]["session_cleanup"]["status"], "deleted")
        self.assertEqual(sorted(path.name for path in output.iterdir()), ["summary.json"])

    def test_active_or_moved_child_blocks_cascading_deletion(self):
        root = {"id": "ses_root", "location": {"directory": "/fixture"}, "time": {"updated": 1, "idle": 1}}
        child = {"id": "ses_child", "parentID": "ses_root", "location": {"directory": "/fixture"}, "time": {"updated": 1, "idle": 1}}
        pages = [{"data": [child], "cursor": {}}, {"data": [], "cursor": {}}, {"data": {"ses_child": {"type": "running"}}}]
        with mock.patch.object(smoke, "api", side_effect=pages), self.assertRaises(ValueError):
            smoke.session_family("opencode", root, self.root, 10)
        child["location"]["directory"] = "/normal-project"
        pages[-1] = {"data": {}}
        with mock.patch.object(smoke, "api", side_effect=pages), self.assertRaises(ValueError):
            smoke.session_family("opencode", root, self.root, 10)

    def test_parameterized_queries_use_verified_operation_id(self):
        with mock.patch.object(smoke, "run", return_value=(0, '{"data": [], "cursor": {}}', "")) as invoked:
            smoke.api("opencode", "GET", "/api/session", self.root, 10, params={"parentID": "ses_fixture"})
        command = invoked.call_args.args[0]
        self.assertEqual(command[:3], ["opencode", "api", "session.list"])
        self.assertIn("parentID=ses_fixture", command)

    def test_interrupted_report_recovery_rejects_later_changes(self):
        output = self.root / "results"
        directory = output / "minimize-reader-load/fixture-example/taskbook"
        case = {"skill": "minimize-reader-load", "session_id": "ses_fixture", "directory": str(directory)}
        report = {"run_id": "run-example", "finished": "1970-01-01T00:00:00.001+00:00"}
        info = {"id": "ses_fixture", "title": "KStack smoke minimize-reader-load", "location": {"directory": str(directory)},
                "time": {"created": 0, "updated": 2, "idle": 2},
                "metadata": {"kstack_smoke": {"kind": "kstack-skill-smoke", "run_id": "run-example", "skill": "minimize-reader-load"}}}
        with mock.patch.object(smoke, "api", return_value=info), mock.patch.object(smoke, "session_family", return_value={"ses_fixture": info}), mock.patch.object(smoke, "run") as deleted:
            result = smoke.clean_session("opencode", case, output, report, self.root, 10, True)
        self.assertEqual(result["status"], "held")
        deleted.assert_not_called()

    def test_reader_load_compatibility_requires_both_actual_loads(self):
        directory = self.root / "repo"
        smoke.fixture(directory, "principle-minimize-reader-load")
        text = "Remove StoreAdapter and StoreProxy. Store owns the mutable state."
        canonical_only = messages("minimize-reader-load", text)
        failures, _ = smoke.validate("principle-minimize-reader-load", directory, None, canonical_only)
        self.assertTrue(any("No successful load of principle-minimize-reader-load" in failure for failure in failures))
        both = messages("principle-minimize-reader-load", "Loading the canonical skill") + canonical_only
        self.assertEqual(smoke.validate("principle-minimize-reader-load", directory, None, both)[0], [])
        self.assertEqual(smoke.loaded_skill_ids(both), ["minimize-reader-load", "principle-minimize-reader-load"])

    def test_timeout_stops_only_the_launched_process_group(self):
        code, _, stderr = smoke.run([sys.executable, "-c", "import time; time.sleep(60)"], self.root, 0.05)
        self.assertEqual(code, 124)
        self.assertIn("timeout", stderr)

    def test_interruption_preserves_report_and_cleans_fixture(self):
        binary = self.fake_cli(interrupted=True)
        output = self.root / "results"
        result = subprocess.run([sys.executable, str(ROOT / "recipes/scripts/smoke-skills.py"),
                                 "--opencode", str(binary), "--skills-dir", str(self.installed()),
                                 "--output", str(output), "--skill", "minimize-reader-load"],
                                capture_output=True, text=True, timeout=10)
        self.assertEqual(result.returncode, 1)
        report = json.loads((output / "summary.json").read_text())
        self.assertEqual(report["cases"][0]["status"], "interrupted")
        self.assertFalse(list(output.glob("*/fixture-*")))

    def test_dry_run_does_not_need_a_cli(self):
        with contextlib.redirect_stdout(io.StringIO()) as output:
            self.assertEqual(smoke.main(["--dry-run"]), 0)
        for name in smoke.CASES:
            self.assertIn(name + ":", output.getvalue())
        for name in smoke.PACKAGING_ONLY:
            self.assertIn(name + ": NOT_RUN (packaging checks only; no live smoke case)", output.getvalue())

    def test_unknown_skills_still_block_even_a_dry_run(self):
        (self.root / ".opencode/skills/new-unknown").mkdir(parents=True)
        with mock.patch.object(smoke, "ROOT", self.root), contextlib.redirect_stderr(io.StringIO()) as errors:
            with self.assertRaises(SystemExit) as failure:
                smoke.main(["--dry-run"])
        self.assertEqual(failure.exception.code, 2)
        self.assertIn("Add test cases for new skills: new-unknown", errors.getvalue())

    def test_full_live_run_is_blocked_before_launch_when_cases_are_missing(self):
        with mock.patch.object(smoke, "find_opencode") as launched, contextlib.redirect_stderr(io.StringIO()) as errors:
            with self.assertRaises(SystemExit) as failure:
                smoke.main([])
        self.assertEqual(failure.exception.code, 2)
        self.assertIn("not a full-bundle live pass", errors.getvalue())
        launched.assert_not_called()


if __name__ == "__main__":
    unittest.main()
