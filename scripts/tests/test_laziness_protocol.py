from pathlib import Path
import re
import unittest


REPO = Path(__file__).resolve().parents[2]
TOOL = REPO / ".opencode/skills/principle-laziness-protocol"
UPSTREAM_BODY = '''Aim for the most result with the least code and complexity.

- **Prefer deletion.** When asked to refactor or improve, look for removals before additions.
- **Maintain a flat call hierarchy.** Avoid deep call chains. A rich interface that hides substantial work is not a deep call chain. If answering a question requires tracing through more than 3 files or layers, flatten it.
- **Consolidate decisions.** Do not repeat the same choice in several places. Put it behind one source of truth and pass the result as a simple flag.
- **Minimize the diff.** Make the smallest change that solves the problem. Fewer lines beat "elegant" boilerplate.
- **Question the threading.** If a task asks you to pass a new signal through types, schemas, pipelines, or similar layers, stop and look for a more direct path.
- **Sweat the small leaks.** Remove tiny pass-throughs, representation leaks, and duplicated choices before they spread. Small leaks compound into permanent coordination costs.

**The test:** If a human developer would find the code exhausting to maintain, it is a bad solution.'''


class LazinessProtocolTests(unittest.TestCase):
    def test_source_rules_are_retained_verbatim(self):
        text = (TOOL / "SKILL.md").read_text()
        self.assertIn(UPSTREAM_BODY, text)
        self.assertEqual(len(re.findall(r"^- \*\*", text, re.M)), 6)

    def test_explicit_identity_and_scope_guard(self):
        text = (TOOL / "SKILL.md").read_text()
        self.assertTrue(text.startswith("---\nname: principle-laziness-protocol\n"))
        self.assertIn("opencode/autoinvoke: false", text)
        self.assertIn("Preserve work you did not make", text)
        self.assertIn("A read-only question does not authorize", text)
        self.assertNotIn("pstack-models", text)

    def test_source_pin_license_and_links(self):
        record = (TOOL / "UPSTREAM.md").read_text()
        self.assertIn("/ccb5507cec1546dc88135c1139c811e6c59115ba/pstack/skills/principle-laziness-protocol/SKILL.md", record)
        self.assertIn("Copyright (c) 2026 Lauren Tan", (TOOL / "LICENSE").read_text())
        for target in re.findall(r"\]\(([^)]+)\)", record):
            if not target.startswith("https://"):
                self.assertTrue((TOOL / target).is_file())

    def test_jiro_routing_and_readme(self):
        text = (REPO / ".opencode/skills/jiro/SKILL.md").read_text()
        self.assertIn("load `principle-laziness-protocol` in full", text)
        self.assertIn("[`@principle-laziness-protocol`]", (REPO / "README.md").read_text())


if __name__ == "__main__":
    unittest.main()
