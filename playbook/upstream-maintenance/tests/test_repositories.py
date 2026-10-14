import copy
import importlib.util
import json
from pathlib import Path
import subprocess
import tempfile
import unittest


MAINTENANCE = Path(__file__).resolve().parents[1]
REPO = MAINTENANCE.parents[1]
SPEC = importlib.util.spec_from_file_location("port_inventory", MAINTENANCE / "scripts/inventory.py")
inventory = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(inventory)
REGISTRY = json.loads((MAINTENANCE / "references/import-map.json").read_text())
SCRATCH = Path(tempfile.gettempdir()) / "opencode"


class UpstreamRepositoryTests(unittest.TestCase):
    def test_existing_imports_inherit_default_repository(self):
        self.assertEqual(inventory.upstream_for(REGISTRY, {"id": "how"}), REGISTRY["upstream"])

    def test_playwright_imports_resolve_their_own_repositories(self):
        entries = {entry["id"]: entry for entry in inventory.inspect(REPO, REGISTRY)["imports"]}
        for identifier in ("playwright-mcp", "playwright-cli"):
            self.assertEqual(entries[identifier]["upstream"], {
                "repository": f"https://github.com/microsoft/{identifier}.git", "ref": "main",
            })
        self.assertEqual(entries["how"]["upstream"], REGISTRY["upstream"])

    def test_incomplete_or_unsafe_override_is_rejected(self):
        overrides = [
            None,
            {"repository": "https://github.com/microsoft/playwright-mcp.git"},
            {"repository": "http://github.com/microsoft/playwright-mcp.git", "ref": "main"},
            {"repository": "https://user:secret@github.com/microsoft/playwright-mcp.git", "ref": "main"},
            {"repository": "https://github.com/microsoft/playwright-mcp.git?token=secret", "ref": "main"},
            {"repository": "https://github.com/microsoft/playwright-mcp.git", "ref": "main\n"},
        ]
        for override in overrides:
            with self.subTest(override=override), self.assertRaises(ValueError):
                inventory.upstream_for(REGISTRY, {"upstream": override})

    def test_mcp_reference_changes_are_scoped_without_restoring_config(self):
        reference = ".opencode/skills/playwright-mcp/references/setup.md"
        report = inventory.inspect(REPO, REGISTRY, [reference, ".opencode/opencode.jsonc"])
        entries = {entry["id"]: entry for entry in report["imports"]}
        self.assertEqual(entries["playwright-mcp"]["changedTargets"], [reference])
        self.assertEqual(entries["playwright-cli"]["changedTargets"], [])

    def test_repository_override_must_match_pinned_provenance(self):
        registry = copy.deepcopy(REGISTRY)
        entry = next(entry for entry in registry["imports"] if entry["id"] == "playwright-mcp")
        entry["upstream"]["repository"] = REGISTRY["upstream"]["repository"]
        report = inventory.inspect(REPO, registry)
        self.assertTrue(any(entry["record"] in error for error in report["errors"]))

    def test_pin_matching_supports_blob_tree_and_raw_but_not_other_repositories(self):
        upstream = {"repository": "https://github.com/microsoft/playwright-mcp.git", "ref": "main"}
        revision = "a" * 40
        for prefix in (
            "https://github.com/microsoft/playwright-mcp/blob/",
            "https://github.com/microsoft/playwright-mcp/tree/",
            "https://raw.githubusercontent.com/microsoft/playwright-mcp/",
        ):
            with self.subTest(prefix=prefix):
                self.assertTrue(inventory.source_pin_recorded(f"[source]({prefix}{revision}/README.md)", upstream, revision, "README.md"))
        for prefix in (
            "https://github.com/cursor/plugins/blob/",
            "https://github.com/microsoft/playwright-mcp-other/blob/",
            "https://raw.githubusercontent.com/cursor/plugins/",
        ):
            with self.subTest(prefix=prefix):
                self.assertFalse(inventory.source_pin_recorded(prefix + revision + "/README.md", upstream, revision, "README.md"))
        self.assertFalse(inventory.source_pin_recorded("https://github.com/microsoft/playwright-mcp/blob/" + revision + "/README.md-old", upstream, revision, "README.md"))
        self.assertTrue(inventory.source_pin_recorded("https://github.com/microsoft/playwright-mcp/tree/" + revision + "/skills/example/SKILL.md", upstream, revision, "skills/example"))

    def test_config_paths_are_discovered_by_git_inventory(self):
        with tempfile.TemporaryDirectory(prefix="port-inventory-", dir=SCRATCH if SCRATCH.is_dir() else None) as directory:
            root = Path(directory)
            subprocess.run(["git", "init", "-q", str(root)], check=True, capture_output=True)
            subprocess.run(["git", "-c", "user.name=Fixture", "-c", "user.email=fixture@example.test", "commit", "--allow-empty", "-qm", "fixture"], cwd=root, check=True, capture_output=True)
            config = root / ".opencode/opencode.jsonc"
            config.parent.mkdir()
            config.write_text("{}\n")
            self.assertIn(".opencode/opencode.jsonc", inventory.changed_paths(root, "HEAD"))

    def test_override_does_not_change_default_or_other_sources(self):
        before = copy.deepcopy(REGISTRY)
        inventory.inspect(REPO, REGISTRY)
        self.assertEqual(REGISTRY, before)


if __name__ == "__main__":
    unittest.main()
