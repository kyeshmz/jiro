import copy
import importlib.util
import json
import os
from pathlib import Path
import shutil
import sys
import tempfile
import unittest
from unittest.mock import patch


MAINTENANCE = Path(__file__).resolve().parents[1]
REPO = MAINTENANCE.parents[1]
sys.path.insert(0, str(MAINTENANCE / "scripts"))
import sync
import verify_proposal
import inventory
sys.path.pop(0)
REGISTRY = json.loads((REPO / sync.REGISTRY).read_text())
SCRATCH = Path(tempfile.gettempdir()) / "opencode"


class SyncTests(unittest.TestCase):
    def test_compiler_preserves_repository_baselines_and_closed_skill_scope(self):
        for identifier in ("jiro", "playwright-cli", "playwright-mcp"):
            entry = next(entry for entry in REGISTRY["imports"] if entry["id"] == identifier)
            policy = sync.compile_policy(REPO, entry)
            self.assertEqual(policy["upstream"], inventory.upstream_for(entry))
            self.assertEqual(policy["baselineCommit"], entry["sources"][0]["importedRevision"])
            self.assertEqual(policy["allowSkillEdits"], [identifier])
            self.assertNotIn(".opencode/**", policy["selections"][0]["targetPaths"])
            self.assertEqual([path for path in policy["selections"][0]["targetPaths"] if path.startswith("skills/")], sorted([entry["license"], f"skills/{identifier}/**"]))
            for protected in ("agents/**", "commands/**", "opencode.json", "opencode.jsonc", ".opencode/**"):
                self.assertIn(protected, policy["protectedPaths"])
            self.assertIn("playbook/upstream-maintenance/scripts/**", policy["protectedPaths"])
            self.assertIn("playbook/**/tests/**", policy["protectedPaths"])
            self.assertEqual(policy["reviewMetadataPaths"], [sync.REGISTRY])
            self.assertTrue(any("Use Jiro for runtime instructions" in rule for rule in policy["preserve"]))
            self.assertNotIn("model", policy["opencode"])
        self.assertEqual(sync.compile_policy(REPO, REGISTRY["imports"][0])["verification"][0]["args"][0], "playbook/upstream-maintenance/scripts/verify_proposal.py")

    def test_missing_mixed_or_config_baselines_cannot_silently_sync(self):
        cleanup = next(entry for entry in REGISTRY["imports"] if entry["id"] == "worktree-cleanup")
        with self.assertRaisesRegex(ValueError, "unknown"):
            sync.compile_policy(REPO, cleanup)
        entry = copy.deepcopy(next(entry for entry in REGISTRY["imports"] if entry["id"] == "playwright-cli"))
        entry["sources"].append({"path": "README.md", "importedRevision": "a" * 40, "reviewedThrough": None})
        with self.assertRaisesRegex(ValueError, "differ"):
            sync.compile_policy(REPO, entry)
        entry["sources"].pop()
        for target in (".opencode/opencode.jsonc", "opencode.json", "opencode.jsonc", "agents/chef.md", "commands/jiro.md"):
            entry["targetRoots"] = [target]
            with self.subTest(target=target), self.assertRaisesRegex(ValueError, "configuration"):
                sync.compile_policy(REPO, entry)
        for target in ("skills", "skills/**", "skills/skill.md", "skills/Invalid"):
            entry["targetRoots"] = [target]
            with self.subTest(target=target), self.assertRaisesRegex(ValueError, "exact named skill"):
                sync.compile_policy(REPO, entry)

    def test_port_overlays_and_conversion_changes_are_selected_as_context(self):
        entry = next(entry for entry in REGISTRY["imports"] if entry["id"] == "arena")
        policy = sync.compile_policy(REPO, entry)
        watched = policy["selections"][0]["upstreamPaths"]
        for path in ("opencode/skills/arena", "scripts/opencode-transform.py", "scripts/install-opencode.py"):
            self.assertIn(path, watched)
            self.assertIn(path + "/**", watched)
        self.assertEqual(policy["allowSkillEdits"], ["arena"])
        self.assertNotIn("scripts/**", policy["selections"][0]["targetPaths"])

    def test_reviewed_port_baseline_does_not_claim_an_import_or_bootstrap_at_head(self):
        entry = next(entry for entry in REGISTRY["imports"] if entry["id"] == "reflect")
        self.assertIsNone(entry["sources"][0]["importedRevision"])
        self.assertEqual(entry["sources"][0]["reviewedThrough"], "1215e2ffdc3068c0a89320c16d95a8ba7b7feb99")
        policy = sync.compile_policy(REPO, entry)
        self.assertEqual(policy["baselineCommit"], entry["sources"][0]["reviewedThrough"])
        self.assertNotEqual(policy["baselineCommit"], REGISTRY["pstackMigration"]["revision"])

    def fixture(self, identifiers=("playwright-cli", "playwright-mcp")):
        temp = tempfile.TemporaryDirectory(prefix="skill-sync-", dir=SCRATCH if SCRATCH.is_dir() else None)
        self.addCleanup(temp.cleanup)
        root = Path(temp.name)
        registry = copy.deepcopy(REGISTRY)
        registry["imports"] = [entry for entry in registry["imports"] if entry["id"] in identifiers]
        for entry in registry["imports"]:
            for value in entry["targetRoots"]:
                source = REPO / value
                target = root / value
                target.parent.mkdir(parents=True, exist_ok=True)
                if source.is_dir():
                    shutil.copytree(source, target)
                else:
                    shutil.copy2(source, target)
        destination = root / sync.REGISTRY
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_text(json.dumps(registry))
        return root, registry

    def test_check_reports_port_context_changes_without_a_model_or_target_scope_expansion(self):
        root, registry = self.fixture(("arena",))
        paths = ["scripts/opencode-transform.py", "opencode/skills/arena/SKILL.md"]
        plan = {"selections": [{"id": "arena"}], "from": registry["imports"][0]["sources"][0]["importedRevision"], "to": "b" * 40, "changedPaths": paths + ["docs/unrelated.md"]}
        with patch.object(sync, "command", return_value=json.dumps(plan)) as command, patch.dict(os.environ, {}, clear=True):
            result = sync.run(root, Path("/owned/tool/cli.js"), "check")
        self.assertEqual(command.call_count, 1)
        self.assertEqual(command.call_args.args[0][2], "check")
        self.assertIsNone(result["proposal"])
        self.assertEqual(result["imports"][0]["paths"], paths)
        self.assertEqual(result["imports"][0]["repository"], "https://github.com/kyeshmz/opencode-pstack.git")
        policy = json.loads((root / ".oc-port/policies/arena.json").read_text())
        self.assertEqual(policy["allowSkillEdits"], ["arena"])
        self.assertIn("scripts/**", policy["protectedPaths"])
        self.assertNotIn("scripts/**", policy["selections"][0]["targetPaths"])

    def test_check_never_calls_model_and_sync_creates_only_one_proposal(self):
        root, _ = self.fixture()
        calls = []
        def command(args, repo, env=None):
            calls.append((args, env))
            if args[1].endswith("cli.js"):
                return json.dumps({"selections": [{"id": "pending"}], "from": "a" * 40, "to": "b" * 40, "changedPaths": ["README.md"]})
            return '::add-mask::test-fixture\n' + json.dumps({"status": "proposal", "branch": "oc-port/fixture"})
        with patch.object(sync, "command", side_effect=command), patch.dict(os.environ, {"OC_PORT_MODEL": "provider/operator-selected-model"}, clear=True):
            result = sync.run(root, Path("/owned/tool/cli.js"), "check")
            self.assertIsNone(result["proposal"])
            self.assertEqual(len(calls), 2)
            calls.clear()
            result = sync.run(root, Path("/owned/tool/cli.js"), "sync")
            self.assertEqual(result["proposal"]["result"]["status"], "proposal")
            self.assertEqual(len([call for call in calls if call[0][1].endswith("action.js")]), 1)
            self.assertTrue(all(call[0][2] == "check" for call in calls[:2]))

    def test_pending_sync_requires_an_operator_model(self):
        root, _ = self.fixture()
        plan = json.dumps({"selections": ["pending"], "from": "a" * 40, "to": "b" * 40, "changedPaths": []})
        with patch.object(sync, "command", return_value=plan), patch.dict(os.environ, {}, clear=True):
            with self.assertRaisesRegex(ValueError, "OC_PORT_MODEL"):
                sync.run(root, Path("/owned/tool/cli.js"), "sync")

    def test_proposal_gate_rejects_unrelated_metadata_and_wrong_pins(self):
        root, before = self.fixture()
        identifier = "playwright-cli"
        entry = next(entry for entry in before["imports"] if entry["id"] == identifier)
        head = "b" * 40
        packet = {"upstream": inventory.upstream_for(entry), "plan": {"to": head, "selections": [{"id": identifier}]}}
        directory = root / ".oc-port/context"
        directory.mkdir(parents=True)
        (directory / "packet.json").write_text(json.dumps(packet))
        (root / ".oc-port/result.json").write_text(json.dumps({"decisions": [{"selection": identifier, "status": "applied"}]}))
        current = copy.deepcopy(before)
        updated = next(item for item in current["imports"] if item["id"] == identifier)
        updated["sources"][0]["importedRevision"] = head
        updated["provenance"] += "\nReviewed head " + head + "\n"
        (root / sync.REGISTRY).write_text(json.dumps(current))
        with patch.object(inventory, "git", return_value=json.dumps(before).encode()), patch.object(inventory, "inspect", return_value={"errors": [], "unmappedSkills": []}):
            verify_proposal.verify(root, identifier)
            for path in ("opencode.json", "opencode.jsonc", ".opencode/opencode.json", ".opencode/opencode.jsonc"):
                config = root / path
                config.parent.mkdir(parents=True, exist_ok=True)
                config.write_text("{}\n")
                with self.subTest(path=path), self.assertRaisesRegex(ValueError, "MCP configuration"):
                    verify_proposal.verify(root, identifier)
                config.unlink()
            other = next(item for item in current["imports"] if item["id"] != identifier)
            previous_notes = other["provenance"]
            other["provenance"] += "Unrequested change to another import."
            (root / sync.REGISTRY).write_text(json.dumps(current))
            with self.assertRaisesRegex(ValueError, "unrelated"):
                verify_proposal.verify(root, identifier)
            other["provenance"] = previous_notes
            updated["upstream"]["ref"] = "unrequested"
            (root / sync.REGISTRY).write_text(json.dumps(current))
            with self.assertRaisesRegex(ValueError, "unrelated"):
                verify_proposal.verify(root, identifier)
            updated["upstream"]["ref"] = entry["upstream"]["ref"]
            updated["watchPaths"] = ["scripts/unrequested.py"]
            (root / sync.REGISTRY).write_text(json.dumps(current))
            with self.assertRaisesRegex(ValueError, "unrelated"):
                verify_proposal.verify(root, identifier)
            del updated["watchPaths"]
            updated["sources"][0]["importedRevision"] = "c" * 40
            (root / sync.REGISTRY).write_text(json.dumps(current))
            with self.assertRaisesRegex(ValueError, "actual tested"):
                verify_proposal.verify(root, identifier)

    def test_workflow_is_scheduled_pinned_and_never_auto_merges(self):
        workflow = (REPO / ".github/workflows/upstream-skills.yml").read_text()
        self.assertIn("schedule:", workflow)
        self.assertIn("workflow_dispatch:", workflow)
        self.assertIn("vars.OC_PORT_AGENT_REF", workflow)
        self.assertIn("secrets.OPENCODE_API_KEY", workflow)
        self.assertIn("vars.OC_PORT_MODEL", workflow)
        self.assertIn("sync.py sync", workflow)
        self.assertNotIn("pull_request_target", workflow)
        self.assertNotIn("--auto", workflow)
        self.assertNotIn("pr merge", workflow)


if __name__ == "__main__":
    unittest.main()
