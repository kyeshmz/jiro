import copy
import importlib.util
import json
from pathlib import Path
import subprocess
import tempfile
import unittest


MAINTENANCE = Path(__file__).resolve().parents[1]
REPO = MAINTENANCE.parents[1]
SPEC = importlib.util.spec_from_file_location("inventory", MAINTENANCE / "scripts/inventory.py")
inventory = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(inventory)
REGISTRY = json.loads((MAINTENANCE / "references/import-map.json").read_text())


class InventoryTests(unittest.TestCase):
    def test_existing_imports_and_known_gap(self):
        report = inventory.inspect(REPO, REGISTRY)
        self.assertEqual(len(report["imports"]), len(REGISTRY["imports"]))
        self.assertIn("jiro", [entry["id"] for entry in report["imports"]])
        self.assertEqual(report["errors"], [])
        self.assertEqual(report["unmappedRecords"], [])
        self.assertEqual(report["baselineGaps"], [{
            "id": "worktree-cleanup",
            "source": "pstack/skills/poteto-mode/playbooks/worktree-cleanup.md",
        }])

    def test_local_changes_are_scoped_to_each_import(self):
        report = inventory.inspect(REPO, REGISTRY, [
            ".opencode/skills/how/SKILL.md",
            ".opencode/skills/however/SKILL.md",
            "recipes/scripts/worktree_audit.py",
            "README.md",
        ])
        imports = {entry["id"]: entry for entry in report["imports"]}
        self.assertEqual(imports["how"]["changedTargets"], [".opencode/skills/how/SKILL.md"])
        self.assertEqual(imports["worktree-cleanup"]["changedTargets"], ["recipes/scripts/worktree_audit.py"])

    def test_duplicate_ids_are_rejected(self):
        registry = copy.deepcopy(REGISTRY)
        registry["imports"].append(registry["imports"][0])
        with self.assertRaisesRegex(ValueError, "duplicate import"):
            inventory.inspect(REPO, registry)

    def test_unsafe_paths_are_rejected(self):
        for path in ("../outside", "/outside", "a/../b", "a\\b", "a\nfile"):
            with self.subTest(path=path), self.assertRaises(ValueError):
                inventory.relative_path(path)

    def test_changed_pin_needs_matching_provenance(self):
        registry = copy.deepcopy(REGISTRY)
        registry["imports"][0]["sources"][0]["importedRevision"] = "a" * 40
        self.assertTrue(inventory.inspect(REPO, registry)["errors"])

    def test_changed_source_path_needs_matching_provenance(self):
        registry = copy.deepcopy(REGISTRY)
        registry["imports"][0]["sources"][0]["path"] = "pstack/skills/not-the-recorded-source"
        self.assertTrue(inventory.inspect(REPO, registry)["errors"])

    def test_unregistered_import_is_reported(self):
        with tempfile.TemporaryDirectory() as directory:
            repo = Path(directory)
            record = repo / ".opencode/skills/new-import/UPSTREAM.md"
            record.parent.mkdir(parents=True)
            record.write_text("Imported source\n")
            report = inventory.inspect(repo, REGISTRY)
            self.assertIn(".opencode/skills/new-import/UPSTREAM.md", report["unmappedRecords"])
            self.assertTrue(report["errors"])

    def test_invalid_revision_is_rejected(self):
        registry = copy.deepcopy(REGISTRY)
        registry["imports"][0]["sources"][0]["importedRevision"] = "main"
        with self.assertRaisesRegex(ValueError, "immutable"):
            inventory.inspect(REPO, registry)

    def test_cli_is_read_only(self):
        before = subprocess.check_output(["git", "status", "--porcelain=v1", "--untracked-files=all"], cwd=REPO)
        result = subprocess.run(["python3", str(MAINTENANCE / "scripts/inventory.py"), "--repo", str(REPO)], capture_output=True)
        after = subprocess.check_output(["git", "status", "--porcelain=v1", "--untracked-files=all"], cwd=REPO)
        self.assertEqual(result.returncode, 0, result.stderr.decode())
        self.assertEqual(before, after)
        self.assertEqual(len(json.loads(result.stdout)["imports"]), len(REGISTRY["imports"]))

    def test_maintenance_is_outside_opencode_skill_discovery(self):
        self.assertFalse(MAINTENANCE.is_relative_to(REPO / ".opencode"))
        self.assertFalse((REPO / ".opencode/skills/maintain-upstream").exists())
        self.assertFalse(list(MAINTENANCE.rglob("SKILL.md")))
        self.assertFalse((MAINTENANCE / "README.md").read_text().startswith("---\n"))

    def test_maintenance_is_not_in_the_installer_sources(self):
        installer = (REPO / "install.sh").read_text()
        sync = (REPO / "scripts/sync-opencode.ts").read_text()
        self.assertIn('join(root, ".opencode", kind)', sync)
        self.assertIn("source = sources(root, category)", sync)
        self.assertNotIn("upstream-maintenance", installer)
        self.assertNotIn("upstream-maintenance", sync)
        self.assertNotIn("maintain-upstream", installer)
        installed_ids = {path.parent.name for path in (REPO / ".opencode/skills").glob("*/SKILL.md")}
        self.assertIn("jiro", installed_ids)
        self.assertTrue(installed_ids.isdisjoint({"maintain-upstream", "upstream-maintenance"}))


if __name__ == "__main__":
    unittest.main()
