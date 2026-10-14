import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest


REPO = Path(__file__).resolve().parents[2]


class InstallTests(unittest.TestCase):
    def setUp(self):
        self.scratch = tempfile.TemporaryDirectory(prefix="jiro-install-", dir="/tmp/opencode")
        self.addCleanup(self.scratch.cleanup)
        self.root = Path(self.scratch.name)
        self.checkout = self.root / "checkout"
        self.checkout.mkdir()
        shutil.copy2(REPO / "install.sh", self.checkout / "install.sh")
        shutil.copytree(REPO / ".opencode", self.checkout / ".opencode")
        (self.checkout / "scripts").mkdir()
        shutil.copy2(REPO / "scripts/sync-opencode.ts", self.checkout / "scripts/sync-opencode.ts")
        (self.checkout / "node_modules").symlink_to(REPO / "node_modules", target_is_directory=True)
        self.config = self.root / "config"
        self.base = self.config / "opencode"
        self.env = {
            **os.environ,
            "HOME": str(self.root / "home"),
            "XDG_CONFIG_HOME": str(self.config),
            "GIT_CONFIG_GLOBAL": "/dev/null",
            "GIT_CONFIG_NOSYSTEM": "1",
        }
        subprocess.run(["git", "init", "-q", str(self.checkout)], env=self.env, check=True, capture_output=True)

    def install(self):
        return subprocess.run(
            ["bash", str(self.checkout / "install.sh")], cwd=self.checkout,
            env=self.env, capture_output=True, text=True,
        )

    def write(self, path, text):
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text)

    def test_installs_entry_and_all_bundled_resources(self):
        result = self.install()
        self.assertEqual(result.returncode, 0, result.stderr)
        for source in (self.checkout / ".opencode/skills").rglob("*"):
            if source.is_file():
                installed = self.base / "skills" / source.relative_to(self.checkout / ".opencode/skills")
                self.assertEqual(installed.read_bytes(), source.read_bytes())
        command = self.base / "commands/jiro.md"
        self.assertEqual(command.read_bytes(), (REPO / ".opencode/commands/jiro.md").read_bytes())
        self.assertIn("$ARGUMENTS", command.read_text())
        self.assertEqual(
            (self.base / "jiro-manifest.txt").read_text().splitlines(),
            sorted(path.name for path in (self.checkout / ".opencode/skills").iterdir() if path.is_dir()),
        )
        self.assertTrue(os.access(self.checkout / ".git/hooks/post-merge", os.X_OK))
        self.assertEqual(
            (self.base / "agents/chef.md").read_bytes(),
            (self.checkout / ".opencode/agents/chef.md").read_bytes(),
        )
        self.assertFalse((self.base / "skills/maintain-upstream").exists())

    def test_reinstall_backs_up_and_replaces_managed_command(self):
        self.assertEqual(self.install().returncode, 0)
        command = self.base / "commands/jiro.md"
        old = command.read_text() + "\nPrevious managed content.\n"
        command.write_text(old)
        result = self.install()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(command.read_bytes(), (REPO / ".opencode/commands/jiro.md").read_bytes())
        backups = list((self.config / "opencode-jiro-backups").glob("*/commands/jiro.md"))
        self.assertEqual(len(backups), 1)
        self.assertEqual(backups[0].read_text(), old)

    def test_preserves_custom_command_unrelated_skills_and_settings(self):
        command = self.base / "commands/jiro.md"
        unrelated = self.base / "skills/personal/SKILL.md"
        config = self.base / "opencode.json"
        self.write(command, "My custom command.\n")
        self.write(unrelated, "My unrelated skill.\n")
        self.write(config, '{"model":"user-owned"}\n')
        result = self.install()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("preserved custom /jiro command", result.stdout)
        self.assertEqual(command.read_text(), "My custom command.\n")
        self.assertEqual(unrelated.read_text(), "My unrelated skill.\n")
        self.assertEqual(config.read_text(), '{"model":"user-owned"}\n')

    def test_preserves_symlinked_command(self):
        target = self.root / "personal-command.md"
        target.write_text("<!-- jiro:command -->\nPersonal content.\n")
        command = self.base / "commands/jiro.md"
        command.parent.mkdir(parents=True)
        command.symlink_to(target)
        result = self.install()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertTrue(command.is_symlink())
        self.assertEqual(target.read_text(), "<!-- jiro:command -->\nPersonal content.\n")

    def test_invalid_source_fails_before_destination_changes(self):
        command = self.base / "commands/jiro.md"
        self.write(command, "Keep this.\n")
        (self.checkout / ".opencode/commands/jiro.md").write_text("Broken wrapper.\n")
        result = self.install()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("validation failed", result.stderr)
        self.assertEqual(command.read_text(), "Keep this.\n")
        self.assertFalse((self.base / "skills").exists())

    def test_removes_only_stale_manifest_skills(self):
        stale = self.base / "skills/old-jiro/SKILL.md"
        unrelated = self.base / "skills/personal/SKILL.md"
        self.write(stale, "Previously installed.\n")
        self.write(unrelated, "Keep this.\n")
        self.write(self.base / "jiro-manifest.txt", "old-jiro\n")
        result = self.install()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertFalse(stale.parent.exists())
        self.assertEqual(unrelated.read_text(), "Keep this.\n")

    def test_legacy_manifest_is_recognized_and_old_backups_are_retained(self):
        stale = self.base / "skills/old-jiro/SKILL.md"
        legacy_manifest = self.base / "kstack-manifest.txt"
        legacy_backup = self.config / "opencode-kstack-backups/previous/skills/old-jiro/SKILL.md"
        self.write(stale, "Previously installed.\n")
        self.write(legacy_manifest, "old-jiro\n")
        self.write(legacy_backup, "Old backup.\n")
        result = self.install()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertFalse(stale.parent.exists())
        self.assertTrue((self.base / "jiro-manifest.txt").is_file())
        self.assertEqual(legacy_manifest.read_text(), "old-jiro\n")
        self.assertEqual(legacy_backup.read_text(), "Old backup.\n")

    def test_current_manifest_takes_precedence_over_legacy_manifest(self):
        unrelated = self.base / "skills/personal/SKILL.md"
        self.write(unrelated, "Keep this.\n")
        self.write(self.base / "kstack-manifest.txt", "personal\n")
        self.write(self.base / "jiro-manifest.txt", "jiro\n")
        result = self.install()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(unrelated.read_text(), "Keep this.\n")


if __name__ == "__main__":
    unittest.main()
