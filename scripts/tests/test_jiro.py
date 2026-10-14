from pathlib import Path
import re
import unittest


REPO = Path(__file__).resolve().parents[2]
SKILL = REPO / ".opencode/skills/jiro/SKILL.md"
RECIPES = SKILL.parent / "references/recipes.md"


class JiroStructureTests(unittest.TestCase):
    def test_skill_is_explicit_and_uses_exact_id(self):
        text = SKILL.read_text()
        self.assertTrue(text.startswith("---\nname: jiro\n"))
        self.assertIn("  opencode/autoinvoke: false\n", text)
        self.assertIn("@jiro or /jiro", text)
        self.assertIn("Inherit the current model by omitting `model`", text)

    def test_all_routes_have_executable_checklists(self):
        text = SKILL.read_text()
        table = text.split("## Recipe book\n", 1)[1].split("## Tools\n", 1)[0]
        routes = re.findall(r"^\| [^|]+ \| ([^|]+) \|$", table, re.M)[2:]
        sections = dict(re.findall(r"^## ([^\n]+)\n(.*?)(?=^## |\Z)", RECIPES.read_text(), re.M | re.S))
        for route in routes:
            with self.subTest(route=route):
                self.assertIn(route, sections)
                steps = re.findall(r"^(\d+)\. ", sections[route], re.M)
                self.assertGreaterEqual(len(steps), 4)
                self.assertEqual(steps, [str(number) for number in range(1, len(steps) + 1)])
        self.assertEqual(set(routes), set(sections))

    def test_relative_links_and_bundled_companions_resolve(self):
        for file in (SKILL, SKILL.parent / "UPSTREAM.md"):
            for link in re.findall(r"\]\(([^)]+)\)", file.read_text()):
                if not link.startswith("https://"):
                    with self.subTest(file=file, link=link):
                        self.assertTrue((file.parent / link).is_file())
        for companion in ("how", "why", "show-me-your-work", "create-verification-skill"):
            self.assertTrue((REPO / f".opencode/skills/{companion}/SKILL.md").is_file())
            self.assertIn(f"`{companion}`", SKILL.read_text())

    def test_command_loads_skill_without_model_or_agent_override(self):
        text = (REPO / ".opencode/commands/jiro.md").read_text()
        self.assertIn("exact ID `jiro`", text)
        self.assertEqual(text.count("$ARGUMENTS"), 1)
        frontmatter = text.split("---", 2)[1]
        self.assertNotRegex(frontmatter, r"(?m)^(agent|model|subagent):")

    def test_chef_theme_preserves_technical_skill_ids(self):
        text = SKILL.read_text()
        for heading in ("Mise en place", "Recipe book", "Tools", "Sous-chefs", "Taste and serve"):
            self.assertIn(f"## {heading}\n", text)
        self.assertIn("Recipes are task playbooks", text)
        self.assertIn("Tools are supporting skills", text)

    def test_readme_documents_the_recipe_book_and_all_tools(self):
        text = (REPO / "README.md").read_text()
        self.assertTrue(text.startswith("# Jiro\n"))
        self.assertIn("https://github.com/kyeshmz/jiro.git", text)
        self.assertNotIn("kstack", text)
        self.assertIn("## Recipe book\n", text)
        self.assertIn("## Tools on the rack\n", text)
        for file in (REPO / ".opencode/skills").glob("*/SKILL.md"):
            with self.subTest(skill=file.parent.name):
                self.assertIn(f"[`@{file.parent.name}`]", text)

    def test_readme_links_and_anchors_resolve(self):
        text = (REPO / "README.md").read_text()
        headings = re.findall(r"^#+ (.+)$", text, re.M)
        anchors = {re.sub(r"[^a-z0-9 -]", "", title.lower()).replace(" ", "-") for title in headings}
        for link in re.findall(r"\]\(([^)]+)\)", text):
            with self.subTest(link=link):
                if link.startswith("#"):
                    self.assertIn(link[1:], anchors)
                elif not link.startswith("https://"):
                    self.assertTrue((REPO / link).exists())


if __name__ == "__main__":
    unittest.main()
