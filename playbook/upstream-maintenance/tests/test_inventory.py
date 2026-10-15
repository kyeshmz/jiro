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
REGISTRY = json.loads((REPO / inventory.REGISTRY).read_text())


class InventoryTests(unittest.TestCase):
    def test_existing_imports_and_known_gap(self):
        report = inventory.inspect(REPO, REGISTRY)
        self.assertEqual(len(report["imports"]), len(REGISTRY["imports"]))
        self.assertIn("jiro", [entry["id"] for entry in report["imports"]])
        self.assertEqual(report["errors"], [])
        self.assertEqual(report["unmappedSkills"], [])
        self.assertEqual(report["baselineGaps"], [{
            "id": "worktree-cleanup",
            "source": "pstack/skills/poteto-mode/playbooks/worktree-cleanup.md",
        }])

    def test_local_changes_are_scoped_to_each_import(self):
        report = inventory.inspect(REPO, REGISTRY, [
            "skills/how/SKILL.md",
            "skills/however/SKILL.md",
            "scripts/worktree_audit.py",
            "README.md",
        ])
        imports = {entry["id"]: entry for entry in report["imports"]}
        self.assertEqual(imports["how"]["changedTargets"], ["skills/how/SKILL.md"])
        self.assertEqual(imports["worktree-cleanup"]["changedTargets"], ["scripts/worktree_audit.py"])

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
            record = repo / "skills/new-import/SKILL.md"
            record.parent.mkdir(parents=True)
            record.write_text("Imported source\n")
            report = inventory.inspect(repo, REGISTRY)
            self.assertIn("skills/new-import", report["unmappedSkills"])
            self.assertTrue(report["errors"])

    def test_separate_provenance_records_are_rejected(self):
        registry = copy.deepcopy(REGISTRY)
        registry["imports"][0]["record"] = "skills/jiro/UPSTREAM.md"
        with self.assertRaisesRegex(ValueError, "separate record"):
            inventory.inspect(REPO, registry)

    def test_each_skill_has_one_provenance_owner(self):
        registry = copy.deepcopy(REGISTRY)
        registry["imports"][1]["targetRoots"].append("skills/jiro")
        with self.assertRaisesRegex(ValueError, "multiple provenance owners"):
            inventory.inspect(REPO, registry)

    def test_catalog_checksum_changes_are_not_silently_accepted(self):
        registry = copy.deepcopy(REGISTRY)
        entry = next(entry for entry in registry["imports"] if entry["id"] == "composition-patterns")
        entry["fileHashes"]["README.md"] = "a" * 64
        self.assertIn("bundle checksum mismatch: skills/composition-patterns/README.md", inventory.inspect(REPO, registry)["errors"])

    def test_missing_checksum_entries_are_reported(self):
        registry = copy.deepcopy(REGISTRY)
        entry = next(entry for entry in registry["imports"] if entry["id"] == "composition-patterns")
        del entry["fileHashes"]["README.md"]
        self.assertIn("unrecorded bundle file: skills/composition-patterns/README.md", inventory.inspect(REPO, registry)["errors"])

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
        self.assertFalse(MAINTENANCE.is_relative_to(REPO / "skills"))
        self.assertFalse((REPO / "skills/maintain-upstream").exists())
        self.assertFalse(list(MAINTENANCE.rglob("SKILL.md")))
        self.assertFalse((MAINTENANCE / "README.md").read_text().startswith("---\n"))

    def test_maintenance_is_not_in_the_installer_sources(self):
        installer = (REPO / "install.sh").read_text()
        sync = (REPO / "scripts/sync-opencode.ts").read_text()
        self.assertIn('join(root, kind)', sync)
        self.assertIn("source = sources(root, category)", sync)
        self.assertNotIn("upstream-maintenance", installer)
        self.assertNotIn("upstream-maintenance", sync)
        self.assertNotIn("maintain-upstream", installer)
        installed_ids = {path.parent.name for path in (REPO / "skills").glob("*/SKILL.md")}
        self.assertIn("jiro", installed_ids)
        self.assertTrue(installed_ids.isdisjoint({"maintain-upstream", "upstream-maintenance"}))


if __name__ == "__main__":
    unittest.main()
