import os
from pathlib import Path
import re
import shutil
import subprocess
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
SKILLS = ROOT / ".opencode/skills"
IMPORTED = ("show-me-your-work", "reflect", "bro", "effect")
REFLECTION_REFERENCES = (
    "judgment-reviewer.md", "tooling-reviewer.md", "divergent-reviewer.md", "synthesizer.md",
)


class ImportedSkillTests(unittest.TestCase):
    def test_requested_skills_have_invocation_metadata_and_provenance(self):
        for name in IMPORTED:
            with self.subTest(skill=name):
                directory = SKILLS / name
                text = (directory / "SKILL.md").read_text()
                match = re.match(r"\A---\n(.*?)\n---", text, re.S)
                self.assertIsNotNone(match)
                frontmatter = match[1]
                self.assertRegex(frontmatter, rf"(?m)^name: {name}$")
                self.assertRegex(frontmatter, r"(?m)^description: \S")
                self.assertIn("license: MIT", frontmatter)
                if name == "effect":
                    self.assertNotIn("opencode/autoinvoke: false", frontmatter)
                    copyright = "Copyright (c) 2025 opencode"
                    source = r"anomalyco/opencode/[a-f0-9]{40}/\.opencode/skills/effect/SKILL\.md"
                else:
                    self.assertIn("  opencode/autoinvoke: false", frontmatter)
                    copyright = "Copyright (c) 2026 Lauren Tan"
                    source = rf"cursor/plugins/[a-f0-9]{{40}}/pstack/skills/{name}/SKILL\.md"
                self.assertIn(copyright, (directory / "LICENSE").read_text())
                self.assertRegex((directory / "UPSTREAM.md").read_text(), source)

    def test_reflection_bundles_all_prompt_templates(self):
        directory = SKILLS / "reflect"
        text = (directory / "SKILL.md").read_text()
        for filename in REFLECTION_REFERENCES:
            with self.subTest(reference=filename):
                self.assertIn(f"references/{filename}", text)
                reference = (directory / "references" / filename).read_text()
                self.assertIn("untrusted data", reference)
                self.assertIn("external writes", reference)
                if filename != "synthesizer.md":
                    self.assertIn("<ABSOLUTE_PATH>", reference)
                    self.assertIn("<DIGEST IF FILE PATH UNAVAILABLE>", reference)
                else:
                    for lens in ("JUDGMENT", "TOOLING", "DIVERGENT"):
                        self.assertIn(f"<{lens}_OUTPUT>", reference)

    def test_bro_preserves_the_upstream_prompt_body(self):
        text = (SKILLS / "bro/SKILL.md").read_text()
        body = text.split("---", 2)[2].strip()
        self.assertEqual(body, "Restate your last message. Stop using jargon and speak coherently. "
                               "State it more simply and concisely, like one human talking to another.")

    def test_installer_copies_requested_skills_and_keeps_unrelated_skills(self):
        with tempfile.TemporaryDirectory(prefix="jiro-import-install-", dir="/tmp/opencode") as temporary:
            directory = Path(temporary)
            checkout = directory / "checkout"
            shutil.copytree(SKILLS, checkout / ".opencode/skills")
            shutil.copy2(ROOT / "install.sh", checkout / "install.sh")
            (checkout / "scripts").mkdir()
            shutil.copy2(ROOT / "scripts/sync-opencode.ts", checkout / "scripts/sync-opencode.ts")
            (checkout / "node_modules").symlink_to(ROOT / "node_modules", target_is_directory=True)
            config = directory / "config"
            installed = config / "opencode/skills"
            unrelated = installed / "unrelated/SKILL.md"
            unrelated.parent.mkdir(parents=True)
            unrelated.write_text("Unrelated user skill.\n")
            env = os.environ.copy()
            env["XDG_CONFIG_HOME"] = str(config)
            subprocess.run(["bash", str(checkout / "install.sh")], cwd=checkout,
                           env=env, capture_output=True, text=True, check=True, timeout=30)
            manifest = (config / "opencode/jiro-manifest.txt").read_text().splitlines()
            for name in IMPORTED:
                with self.subTest(skill=name):
                    self.assertIn(name, manifest)
                    for path in (SKILLS / name).rglob("*"):
                        if path.is_file():
                            self.assertEqual(path.read_bytes(),
                                             (installed / name / path.relative_to(SKILLS / name)).read_bytes())
            self.assertEqual(unrelated.read_text(), "Unrelated user skill.\n")


if __name__ == "__main__":
    unittest.main()
