import json
from pathlib import Path
import re
import unittest


REPO = Path(__file__).resolve().parents[3]
SKILLS = REPO / "skills"
IDS = ("create-subagent", "delegate", "swarm")


class DelegationPackageTests(unittest.TestCase):
    def test_metadata_and_license(self):
        upstream_license = (SKILLS / "how/LICENSE").read_text()
        for identifier in IDS:
            with self.subTest(skill=identifier):
                directory = SKILLS / identifier
                text = (directory / "SKILL.md").read_text()
                metadata = re.match(r"\A---\n(.*?)\n---\n", text, re.S).group(1)
                self.assertIn("name: " + identifier, metadata)
                self.assertRegex(metadata, r"(?m)^description: \S")
                self.assertIn("opencode/autoinvoke: false", metadata)
                self.assertEqual((directory / "LICENSE").read_text(), upstream_license)

    def test_shared_contract_and_templates_are_bundled(self):
        swarm = (SKILLS / "swarm/SKILL.md").read_text()
        for name in ("handoff.md", "run-template.md"):
            reference = "../delegate/references/" + name
            self.assertIn(reference, swarm)
            self.assertTrue((SKILLS / "swarm" / reference).is_file())
        for name in ("agent-template.md", "read-only-agent-template.md"):
            self.assertTrue((SKILLS / "create-subagent/references" / name).is_file())

    def test_reviewer_template_has_v2_permissions_and_inherits_model(self):
        template = (SKILLS / "create-subagent/references/read-only-agent-template.md").read_text()
        self.assertIn("mode: subagent", template)
        for action in ("edit", "shell", "subagent"):
            self.assertRegex(template, rf"action: {action}\n\s+resource: \"\*\"\n\s+effect: deny")
        self.assertNotRegex(template, r"(?m)^model:")
        self.assertNotIn("is_background:", template)

    def test_imports_have_exact_source_pins_and_records(self):
        registry = json.loads((REPO / "upstream.json").read_text())
        entries = {entry["id"]: entry for entry in registry["imports"]}
        for identifier in IDS:
            with self.subTest(skill=identifier):
                entry = entries[identifier]
                record = entry["provenance"]
                for source in entry["sources"]:
                    self.assertRegex(source["importedRevision"], r"^[a-f0-9]{40}$")
                    self.assertIn("/" + source["importedRevision"] + "/" + source["path"], record)

    def test_local_document_links_resolve(self):
        documents = [REPO / "playbook/delegation/README.md"]
        documents += [path for identifier in IDS for path in (SKILLS / identifier).rglob("*.md")]
        for document in documents:
            for target in re.findall(r"\]\(([^)]+)\)", document.read_text()):
                if "://" in target or target.startswith("#"):
                    continue
                with self.subTest(document=document, target=target):
                    self.assertTrue((document.parent / target.split("#")[0]).exists())

    def test_scenarios_cover_all_new_workflows(self):
        scenarios = json.loads((Path(__file__).parent / "scenarios.json").read_text())["evals"]
        for identifier in IDS:
            self.assertTrue(any("@" + identifier in scenario["prompt"] for scenario in scenarios))


if __name__ == "__main__":
    unittest.main()
