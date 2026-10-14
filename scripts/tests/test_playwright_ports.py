import json
from pathlib import Path
import re
import unittest


REPO = Path(__file__).resolve().parents[2]
SKILLS = REPO / ".opencode/skills"


class PlaywrightPortTests(unittest.TestCase):
    def test_mcp_config_is_removed_and_not_a_maintenance_target(self):
        self.assertFalse((REPO / ".opencode/opencode.jsonc").exists())
        registry = json.loads((REPO / "playbook/upstream-maintenance/references/import-map.json").read_text())
        entry = next(entry for entry in registry["imports"] if entry["id"] == "playwright-mcp")
        self.assertNotIn(".opencode/opencode.jsonc", entry["targetRoots"])
        self.assertTrue(any("do not restore server configuration" in rule for rule in entry["preserve"]))

    def test_skills_are_explicit_and_keep_apache_license(self):
        for identifier in ("playwright-mcp", "playwright-cli"):
            with self.subTest(skill=identifier):
                directory = SKILLS / identifier
                text = (directory / "SKILL.md").read_text()
                metadata = re.match(r"\A---\n(.*?)\n---\n", text, re.S).group(1)
                self.assertIn("name: " + identifier, metadata)
                self.assertIn("opencode/autoinvoke: false", metadata)
                self.assertIn("license: Apache-2.0", metadata)
                self.assertNotIn("allowed-tools:", metadata)
                license_text = (directory / "LICENSE").read_text()
                self.assertIn("Version 2.0, January 2004", license_text)
                self.assertIn("Copyright (c) Microsoft Corporation.", license_text)
                self.assertRegex(text.lower(), r"modified|adapted")

    def test_all_official_cli_references_are_bundled(self):
        expected = {
            "element-attributes.md", "playwright-tests.md", "pr-attachments.md", "request-mocking.md",
            "running-code.md", "session-management.md", "storage-state.md", "test-generation.md",
            "tracing.md", "video-recording.md",
        }
        self.assertEqual({path.name for path in (SKILLS / "playwright-cli/references").glob("*.md")}, expected | {"command-catalog.md"})
        self.assertLess(len((SKILLS / "playwright-cli/SKILL.md").read_text().splitlines()), 500)

    def test_playwright_ports_are_registered_separately(self):
        registry = json.loads((REPO / "playbook/upstream-maintenance/references/import-map.json").read_text())
        entries = {entry["id"]: entry for entry in registry["imports"]}
        for identifier in ("playwright-mcp", "playwright-cli"):
            entry = entries[identifier]
            self.assertEqual(entry["upstream"]["repository"], f"https://github.com/microsoft/{identifier}.git")
            record = (REPO / entry["record"]).read_text()
            for source in entry["sources"]:
                self.assertIn("/" + source["importedRevision"] + "/" + source["path"], record)
            self.assertTrue((REPO / entry["license"]).is_file())

    def test_local_links_and_optional_setup_remain_valid(self):
        documents = [REPO / "playbook/playwright/README.md"]
        for identifier in ("playwright-mcp", "playwright-cli"):
            documents.extend((SKILLS / identifier).rglob("*.md"))
        for document in documents:
            prose = re.sub(r"```.*?```|`[^`\n]+`", "", document.read_text(), flags=re.S)
            for target in re.findall(r"\]\(([^)]+)\)", prose):
                if "://" in target or target.startswith("#") or "<" in target:
                    continue
                with self.subTest(document=document, target=target):
                    self.assertTrue((document.parent / target.split("#")[0]).exists())
        setup = (SKILLS / "playwright-mcp/references/setup.md").read_text()
        self.assertIn("@playwright/mcp@0.0.83", setup)
        self.assertIn("opt-in only", setup)
        example = json.loads(re.search(r"```json\n(.*?)\n```", setup, re.S).group(1))
        server = example["mcp"]["servers"]["playwright"]
        self.assertEqual(server["type"], "local")
        self.assertEqual(server["command"][:3], ["npx", "-y", "@playwright/mcp@0.0.83"])
        for flag in ("--headless", "--isolated", "--no-webmcp"):
            self.assertIn(flag, server["command"])
        self.assertNotIn("--no-sandbox", server["command"])
        self.assertNotIn("--allow-unrestricted-file-access", server["command"])
        self.assertNotIn("enabled", server)
        self.assertEqual(example["permissions"], [{
            "action": "playwright_browser_run_code*", "resource": "*", "effect": "ask",
        }])


if __name__ == "__main__":
    unittest.main()
