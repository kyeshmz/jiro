import { afterEach, beforeEach, expect, test } from "bun:test"
import {
  chmodSync,
  cpSync,
  existsSync,
  lstatSync,
  mkdirSync,
  mkdtempSync,
  readFileSync,
  readdirSync,
  rmSync,
  statSync,
  symlinkSync,
  writeFileSync,
} from "node:fs"
import { dirname, join, resolve } from "node:path"
import { spawnSync } from "node:child_process"

const root = resolve(import.meta.dir, "..")
let temporary: string
let checkout: string
let config: string
let env: NodeJS.ProcessEnv

function write(path: string, text: string) {
  mkdirSync(dirname(path), { recursive: true })
  writeFileSync(path, text)
}

function run(...args: string[]) {
  return spawnSync("bash", [join(checkout, "install.sh"), ...args], { cwd: checkout, env, encoding: "utf8" })
}

function git(...args: string[]) {
  const result = spawnSync("git", args, { cwd: checkout, env, encoding: "utf8" })
  expect(result.status).toBe(0)
  return result
}

beforeEach(() => {
  temporary = mkdtempSync("/tmp/opencode/jiro-sync-")
  checkout = join(temporary, "checkout")
  config = join(temporary, "config/opencode")
  cpSync(join(root, ".opencode"), join(checkout, ".opencode"), { recursive: true, dereference: true })
  for (const file of ["install.sh", "package.json", "bun.lock", "scripts/sync-opencode.ts"]) {
    const target = join(checkout, file)
    mkdirSync(dirname(target), { recursive: true })
    cpSync(join(root, file), target)
  }
  symlinkSync(join(root, "node_modules"), join(checkout, "node_modules"), "dir")
  env = {
    ...process.env,
    XDG_CONFIG_HOME: dirname(config),
    BUN_BIN: process.execPath,
    GIT_CONFIG_NOSYSTEM: "1",
    GIT_CONFIG_GLOBAL: "/dev/null",
    GIT_AUTHOR_NAME: "Jiro fixture",
    GIT_AUTHOR_EMAIL: "fixture@example.invalid",
    GIT_COMMITTER_NAME: "Jiro fixture",
    GIT_COMMITTER_EMAIL: "fixture@example.invalid",
  }
})

afterEach(() => rmSync(temporary, { recursive: true, force: true }))

test("installs Jiro, its command, Chef, and self-contained references", () => {
  write(join(config, "opencode.json"), '{"model":"provider/user-choice"}\n')
  expect(run().status).toBe(0)
  expect(run("--check").status).toBe(0)
  for (const relative of [
    "commands/jiro.md", "agents/chef.md",
    "skills/jiro/SKILL.md",
    "skills/jiro/references/shared-rules.md", "skills/jiro/references/refactoring.md",
    "skills/jiro/references/authoring-a-skill.md", "skills/jiro/references/eval.md",
  ]) {
    const installed = join(config, relative)
    expect(readFileSync(installed, "utf8")).toBe(readFileSync(join(root, ".opencode", relative), "utf8"))
    expect(lstatSync(installed).isSymbolicLink()).toBe(false)
  }
  expect(readFileSync(join(config, "jiro-manifest.txt"), "utf8")).toContain("jiro\n")
  expect(readFileSync(join(config, "jiro-commands-manifest.txt"), "utf8")).toBe("jiro.md\n")
  expect(readFileSync(join(config, "jiro-agents-manifest.txt"), "utf8")).toBe("chef.md\n")
  expect(readFileSync(join(config, "opencode.json"), "utf8")).toBe('{"model":"provider/user-choice"}\n')
})

test("@jiro is the complete skill rather than a forwarding alias", () => {
  const source = readFileSync(join(root, ".opencode/skills/jiro/SKILL.md"), "utf8")
  expect(source).toMatch(/^name: jiro$/m)
  expect(source).not.toContain("jiro-mode")
  expect(source).toContain("## Core principles")
  expect(source).toContain("## Non-negotiables")
  expect(existsSync(join(root, ".opencode/skills/jiro-mode"))).toBe(false)
  expect(existsSync(join(root, ".opencode/commands/jiro-mode.md"))).toBe(false)
  expect(readFileSync(join(root, ".opencode/commands/jiro.md"), "utf8")).toContain('id: "jiro"')
  const smoke = readFileSync(join(root, "scripts/smoke-jiro.ts"), "utf8")
  expect(smoke).toContain('skill: "jiro"')
  expect(smoke).toContain('skills: ["jiro"]')
  expect(smoke).toContain("const requiresSharedRules = item.text.length > 0")
  expect(smoke).toContain("if (requiresSharedRules && !sharedRulesRead)")
})

test("Jiro is the entry skill and its registered workers are chefs", () => {
  const skill = readFileSync(join(root, ".opencode/skills/jiro/SKILL.md"), "utf8")
  const chef = readFileSync(join(root, ".opencode/agents/chef.md"), "utf8")
  expect(skill).toContain("## Chefs")
  expect(skill).toContain("Jiro's workers are chefs")
  expect(chef).toContain("You are a chef, Jiro's worker agent")
  expect(chef).toContain("Load `jiro` through the `skill` tool before working")
  expect(chef).toMatch(/^mode: subagent$/m)
  expect(chef).not.toMatch(/^model:/m)
  for (const path of [
    "README.md", "agents/chef.md", "playbook/delegation/README.md",
    ".opencode/skills/jiro/SKILL.md", ".opencode/skills/jiro/UPSTREAM.md",
    ".opencode/skills/create-subagent/SKILL.md", ".opencode/skills/create-subagent/UPSTREAM.md",
  ]) {
    const text = readFileSync(join(root, path), "utf8")
    expect(text).not.toContain("kye-mode")
    expect(text).not.toMatch(/sous-chefs?/i)
  }
})

test("preserves an unowned custom Jiro command without claiming ownership", () => {
  const command = join(config, "commands/jiro.md")
  write(command, "My custom command.\n")
  expect(run().stdout).toContain("preserved custom /jiro command")
  expect(readFileSync(command, "utf8")).toBe("My custom command.\n")
  expect(readFileSync(join(config, "jiro-commands-manifest.txt"), "utf8")).toBe("")
  expect(run("--check").status).toBe(0)
})

test("preserves a symlinked Jiro command even when formerly managed", () => {
  expect(run().status).toBe(0)
  const command = join(config, "commands/jiro.md")
  const target = join(temporary, "personal-command.md")
  write(target, "<!-- jiro:command -->\nPersonal content.\n")
  rmSync(command)
  symlinkSync(target, command)
  expect(run().status).toBe(0)
  expect(lstatSync(command).isSymbolicLink()).toBe(true)
  expect(readFileSync(target, "utf8")).toBe("<!-- jiro:command -->\nPersonal content.\n")
  expect(run("--check").status).toBe(0)
})

test("upgrades a legacy owned wrapper and preserves the previous content", () => {
  write(join(config, "commands/jiro.md"), "Prior managed wrapper.\n")
  write(join(config, "jiro-commands-manifest.txt"), "jiro.md\n")
  expect(run().status).toBe(0)
  expect(readFileSync(join(config, "commands/jiro.md"), "utf8"))
    .toBe(readFileSync(join(checkout, ".opencode/commands/jiro.md"), "utf8"))
  const [backup] = readdirSync(join(dirname(config), "opencode-jiro-backups"))
  expect(readFileSync(join(dirname(config), "opencode-jiro-backups", backup, "commands/jiro.md"), "utf8"))
    .toBe("Prior managed wrapper.\n")
})

test("rejects a well-formed wrapper without its invocation contract before syncing", () => {
  write(join(checkout, ".opencode/commands/jiro.md"), "---\ndescription: Broken wrapper\n---\nNo arguments.\n")
  expect(run().status).toBe(1)
  expect(existsSync(join(config, "skills/jiro"))).toBe(false)
})

test("the rename retires old owned entry points while preserving their backups", () => {
  write(join(config, "skills/jiro-mode/SKILL.md"), "Prior Jiro skill.\n")
  write(join(config, "commands/jiro-mode.md"), "Prior Jiro command.\n")
  write(join(config, "jiro-manifest.txt"), "jiro-mode\n")
  write(join(config, "jiro-commands-manifest.txt"), "jiro-mode.md\n")
  expect(run().status).toBe(0)
  expect(existsSync(join(config, "skills/jiro-mode"))).toBe(false)
  expect(existsSync(join(config, "commands/jiro-mode.md"))).toBe(false)
  expect(readFileSync(join(config, "skills/jiro/SKILL.md"), "utf8")).toMatch(/^name: jiro$/m)
  const [backup] = readdirSync(join(dirname(config), "opencode-jiro-backups"))
  expect(readFileSync(join(dirname(config), "opencode-jiro-backups", backup, "skills/jiro-mode/SKILL.md"), "utf8"))
    .toBe("Prior Jiro skill.\n")
  expect(run("--check").status).toBe(0)
})

test("a repeated sync preserves installed files and creates no backup", () => {
  expect(run().status).toBe(0)
  const installed = join(config, "skills/jiro/SKILL.md")
  const time = statSync(installed).mtimeMs
  expect(run().stdout).toContain("Synced 0 entries")
  expect(statSync(installed).mtimeMs).toBe(time)
  expect(existsSync(join(dirname(config), "opencode-jiro-backups"))).toBe(false)
})

test("replaces changed entries, removes stale files, and preserves the prior data", () => {
  expect(run().status).toBe(0)
  const installed = join(config, "skills/jiro/references/obsolete.md")
  write(installed, "Prior installed data.\n")
  const rules = join(checkout, ".opencode/skills/jiro/references/shared-rules.md")
  write(rules, "Updated shared rules.\n")
  write(join(config, "skills/unrelated/SKILL.md"), "Unrelated skill.\n")
  expect(run().status).toBe(0)
  expect(existsSync(installed)).toBe(false)
  expect(readFileSync(join(config, "skills/jiro/references/shared-rules.md"), "utf8")).toBe("Updated shared rules.\n")
  expect(readFileSync(join(config, "skills/unrelated/SKILL.md"), "utf8")).toBe("Unrelated skill.\n")
  const backups = join(dirname(config), "opencode-jiro-backups")
  const [backup] = readdirSync(backups)
  expect(readFileSync(join(backups, backup, "skills/jiro/references/obsolete.md"), "utf8")).toBe("Prior installed data.\n")
})

test("archives removed owned entries and leaves unrelated commands and agents alone", () => {
  expect(run().status).toBe(0)
  write(join(config, "commands/unrelated.md"), "Unrelated command.\n")
  write(join(config, "agents/unrelated.md"), "Unrelated agent.\n")
  rmSync(join(checkout, ".opencode/commands/jiro.md"))
  rmSync(join(checkout, ".opencode/agents/chef.md"))
  expect(run().status).toBe(0)
  expect(existsSync(join(config, "commands/jiro.md"))).toBe(false)
  expect(existsSync(join(config, "agents/chef.md"))).toBe(false)
  expect(readFileSync(join(config, "commands/unrelated.md"), "utf8")).toBe("Unrelated command.\n")
  expect(readFileSync(join(config, "agents/unrelated.md"), "utf8")).toBe("Unrelated agent.\n")
  expect(run("--check").status).toBe(0)
})

test("check reports uncommitted edits without replacing installed data", () => {
  expect(run().status).toBe(0)
  const path = "skills/jiro/references/shared-rules.md"
  const before = readFileSync(join(config, path), "utf8")
  write(join(checkout, ".opencode", path), "Uncommitted rules.\n")
  const result = run("--check")
  expect(result.status).toBe(1)
  expect(result.stdout).toContain(`Out of sync: skills/jiro`)
  expect(readFileSync(join(config, path), "utf8")).toBe(before)
  expect(readdirSync(config).some((name) => name.startsWith(".jiro-sync-"))).toBe(false)
})

test("check detects missing ownership manifests", () => {
  expect(run().status).toBe(0)
  rmSync(join(config, "jiro-commands-manifest.txt"))
  expect(run("--check").status).toBe(1)
})

test("invalid source metadata prevents all replacement", () => {
  expect(run().status).toBe(0)
  const installed = join(config, "skills/jiro/SKILL.md")
  const before = readFileSync(installed, "utf8")
  write(join(checkout, ".opencode/skills/jiro/SKILL.md"), "Invalid skill.\n")
  expect(run().status).toBe(1)
  expect(readFileSync(installed, "utf8")).toBe(before)
})

test("unsafe manifests cannot affect paths outside the managed directories", () => {
  expect(run().status).toBe(0)
  const protectedFile = join(config, "protected.md")
  write(protectedFile, "Keep this.\n")
  write(join(config, "jiro-commands-manifest.txt"), "../protected.md\n")
  expect(run().status).toBe(1)
  expect(readFileSync(protectedFile, "utf8")).toBe("Keep this.\n")
})

test("destination symlinks cannot redirect installation into user directories", () => {
  const external = join(temporary, "external")
  write(join(external, "jiro.md"), "Keep this.\n")
  mkdirSync(config, { recursive: true })
  symlinkSync(external, join(config, "commands"), "dir")
  expect(run().status).toBe(1)
  expect(readFileSync(join(external, "jiro.md"), "utf8")).toBe("Keep this.\n")
})

test("legacy ownership is retained across the project rename", () => {
  write(join(config, "kstack-manifest.txt"), "obsolete\n")
  write(join(config, "skills/obsolete/SKILL.md"), "Old installed data.\n")
  expect(run().status).toBe(0)
  expect(existsSync(join(config, "skills/obsolete"))).toBe(false)
  expect(run("--check").status).toBe(0)
})

test("real commits and merges sync the corresponding checkout state", () => {
  git("init", "-b", "main")
  expect(run().status).toBe(0)
  git("add", ".opencode", "install.sh", "scripts/sync-opencode.ts", "package.json", "bun.lock")
  git("commit", "-m", "Initial fixture")
  const relative = "skills/jiro/references/shared-rules.md"
  git("checkout", "-b", "next")
  write(join(checkout, ".opencode", relative), "Committed shared rules.\n")
  git("add", ".opencode")
  git("commit", "-m", "Update shared rules")
  expect(readFileSync(join(config, relative), "utf8")).toBe("Committed shared rules.\n")
  git("checkout", "main")
  expect(run().status).toBe(0)
  expect(readFileSync(join(config, relative), "utf8")).not.toBe("Committed shared rules.\n")
  git("merge", "--ff-only", "next")
  expect(readFileSync(join(config, relative), "utf8")).toBe("Committed shared rules.\n")
  expect(run("--check").status).toBe(0)
})

test("custom hooks and a configured hooks path are preserved", () => {
  git("init", "-b", "main")
  const hook = join(checkout, ".git/hooks/post-commit")
  write(hook, "#!/usr/bin/env bash\nprintf 'custom hook\\n'\n")
  chmodSync(hook, 0o755)
  expect(run().stdout).toContain("Custom hook preserved")
  expect(readFileSync(hook, "utf8")).toBe("#!/usr/bin/env bash\nprintf 'custom hook\\n'\n")
  const custom = join(temporary, "shared-hooks")
  git("config", "core.hooksPath", custom)
  expect(run().stdout).toContain("Custom hooks path preserved")
  expect(existsSync(custom)).toBe(false)
})

test("Commander provides help and rejects unsupported options", () => {
  const help = run("--help")
  expect(help.status).toBe(0)
  expect(help.stdout).toContain("Usage: jiro-sync")
  expect(help.stdout).toContain("--check")
  expect(run("--unknown-option").status).toBe(1)
})
