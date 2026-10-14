from pathlib import Path
import re
import unittest


REPO = Path(__file__).resolve().parents[2]
TOOL = REPO / ".opencode/skills/no-comments"


class NoCommentsTests(unittest.TestCase):
    def test_explicit_id_and_bundled_reviewer(self):
        text = (TOOL / "SKILL.md").read_text()
        self.assertTrue(text.startswith("---\nname: no-comments\n"))
        self.assertIn("opencode/autoinvoke: false", text)
        self.assertIn("references/reviewer-prompt.md", text)
        self.assertIn("Otherwise use `general`", text)
        self.assertIn("when the host advertises that exact agent ID", text)
        self.assertNotIn("subagent_type:", text)
        self.assertFalse((REPO / ".opencode/agents/comment-sicko.md").exists())

    def test_all_protected_exception_classes_are_present(self):
        reviewer = (TOOL / "references/reviewer-prompt.md").read_text()
        for exception in ("Legal or license headers", "external dependency", "prettier-ignore", "public API contract", "Issue or RFC links"):
            with self.subTest(exception=exception):
                self.assertIn(exception, reviewer)
        self.assertIn("do not edit", reviewer.lower())
        self.assertIn("do not spawn children", reviewer.lower())
        self.assertIn("Actual deletion count is zero", reviewer)

    def test_parent_edits_and_retry_are_scoped(self):
        text = (TOOL / "SKILL.md").read_text()
        self.assertIn("parent owns all accepted edits", text)
        self.assertIn("Rerun one rejected report", text)
        self.assertIn("Reject a second", text)
        self.assertIn("Never reset or discard user changes", text)
        self.assertIn("Keep uncertain exception-protected comments untouched", text)
        self.assertIn("Wait for interactive approval", text)
        self.assertIn("A read-only request permits a report", text)
        self.assertEqual(re.findall(r"^(\d+)\. ", text, re.M), ["1", "2", "3", "4", "5", "6"])

    def test_source_license_and_local_links(self):
        self.assertIn("Copyright (c) 2026 Lauren Tan", (TOOL / "LICENSE").read_text())
        record = (TOOL / "UPSTREAM.md").read_text()
        for path in ("pstack/skills/no-comments/SKILL.md", "pstack/agents/comment-sicko.md"):
            self.assertIn("/ccb5507cec1546dc88135c1139c811e6c59115ba/" + path, record)
        for file in (TOOL / "SKILL.md", TOOL / "UPSTREAM.md"):
            for target in re.findall(r"\]\(([^)]+)\)", file.read_text()):
                if not target.startswith("https://"):
                    self.assertTrue((file.parent / target).is_file())

    def test_jiro_routes_to_the_tool(self):
        self.assertIn("load `no-comments`", (REPO / ".opencode/skills/jiro/SKILL.md").read_text())
        self.assertIn("[`@no-comments`]", (REPO / "README.md").read_text())


if __name__ == "__main__":
    unittest.main()
