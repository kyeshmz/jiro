import { afterEach, beforeEach, expect, test } from "bun:test"
import { lockSync } from "proper-lockfile"
import {
  chmodSync,
  cpSync,
  existsSync,
  lstatSync,
  mkdirSync,
  mkdtempSync,
  readFileSync,
  readdirSync,
  renameSync,
  rmSync,
  statSync,
  symlinkSync,
  utimesSync,
  writeFileSync,
} from "node:fs"
import { tmpdir } from "node:os"
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
  const scratch = join(tmpdir(), "opencode")
  mkdirSync(scratch, { recursive: true })
  temporary = mkdtempSync(join(scratch, "jiro-sync-"))
  checkout = join(temporary, "checkout")
  config = join(temporary, "config/opencode")
  for (const kind of ["skills", "commands", "agents"]) {
    cpSync(join(root, kind), join(checkout, kind), { recursive: true, dereference: true })
  }
  for (const file of ["install.sh", "package.json", "bun.lock", "upstream.json", "scripts/sync-opencode.ts"]) {
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
    "upstream.json",
    "commands/jiro.md", "agents/chef.md",
    "commands/correct.md", "commands/teach.md", "commands/unslop.md",
    "skills/correct/SKILL.md", "skills/correct/LICENSE",
    "skills/teach/SKILL.md", "skills/teach/LICENSE",
    "skills/unslop/SKILL.md", "skills/unslop/LICENSE",
    "skills/jiro/SKILL.md",
    "skills/jiro/references/shared-rules.md", "skills/jiro/references/refactoring.md",
    "skills/jiro/references/authoring-a-skill.md", "skills/jiro/references/eval.md",
  ]) {
    const installed = join(config, relative)
    expect(readFileSync(installed, "utf8")).toBe(readFileSync(join(root, relative), "utf8"))
    expect(lstatSync(installed).isSymbolicLink()).toBe(false)
  }
  expect(readFileSync(join(config, "jiro-manifest.txt"), "utf8")).toContain("jiro\n")
  expect(readFileSync(join(config, "jiro-commands-manifest.txt"), "utf8")).toBe("correct.md\njiro.md\nteach.md\nunslop.md\n")
  expect(readFileSync(join(config, "jiro-agents-manifest.txt"), "utf8")).toBe("chef.md\n")
  expect(readFileSync(join(config, "opencode.json"), "utf8")).toBe('{"model":"provider/user-choice"}\n')
})

test("the checkout is a config root without nested OpenCode definitions", () => {
  expect(existsSync(join(root, ".opencode"))).toBe(false)
  expect(run().status).toBe(0)
  const names = readdirSync(join(root, "skills")).filter((name) => statSync(join(root, "skills", name)).isDirectory()).sort()
  expect(readFileSync(join(config, "jiro-manifest.txt"), "utf8")).toBe(names.map((name) => `${name}\n`).join(""))
  expect(existsSync(join(checkout, ".opencode"))).toBe(false)
  expect(readdirSync(join(config, "skills")).every((name) => statSync(join(config, "skills", name)).isDirectory())).toBe(true)
})

test("all migrated pstack tools install with self-contained shared writing rules", () => {
  const catalog = JSON.parse(readFileSync(join(root, "upstream.json"), "utf8"))
  const choices = "# User model choices\nswarm workers: inherit-parent\n"
  write(join(config, "instructions/pstack-models.md"), choices)
  expect(run().status).toBe(0)
  for (const id of new Set<string>(Object.values(catalog.pstackMigration.skills))) {
    expect(existsSync(join(config, "skills", id, "SKILL.md")), id).toBe(true)
    const shared = join(config, "skills", id, "references/shared-rules.md")
    if (existsSync(shared)) {
      expect(lstatSync(shared).isSymbolicLink(), id).toBe(false)
      expect(readFileSync(shared, "utf8")).toBe(readFileSync(join(root, "skills/skill.md"), "utf8"))
    }
  }
  expect(readFileSync(join(config, "instructions/pstack-models.md"), "utf8")).toBe(choices)
  expect(existsSync(join(config, "instructions/kstack-models.md"))).toBe(false)
  expect(run("--check").status).toBe(0)
})

test("the installer does not fall back to a nested OpenCode source tree", () => {
  mkdirSync(join(checkout, ".opencode"))
  cpSync(join(checkout, "skills"), join(checkout, ".opencode/skills"), { recursive: true })
  rmSync(join(checkout, "skills"), { recursive: true })
  const result = run()
  expect(result.status).toBe(1)
  expect(result.stderr).toContain("Source skills directory missing")
  expect(existsSync(join(config, "skills"))).toBe(false)
})

test("a checkout already in the global config directory remains intact", () => {
  const destination = join(temporary, "opencode")
  renameSync(checkout, destination)
  checkout = destination
  config = destination
  env.XDG_CONFIG_HOME = temporary
  const skill = join(checkout, "skills/jiro/SKILL.md")
  const before = statSync(skill).mtimeMs
  expect(run().status).toBe(0)
  expect(run("--check").status).toBe(0)
  expect(statSync(skill).mtimeMs).toBe(before)
  expect(existsSync(join(checkout, ".opencode"))).toBe(false)
})

test("installation and checks do not require the flock executable", () => {
  const bin = join(temporary, "bin")
  write(join(bin, "flock"), "#!/bin/sh\necho 'flock must not be called' >&2\nexit 97\n")
  chmodSync(join(bin, "flock"), 0o755)
  env.PATH = `${bin}:${env.PATH}`
  expect(run().status).toBe(0)
  expect(run("--check").status).toBe(0)
})

test("sync waits for an existing config lock before installing", async () => {
  mkdirSync(config, { recursive: true })
  const lockfilePath = join(config, ".jiro-sync.lock.d")
  const release = lockSync(config, { lockfilePath, stale: 60_000 })
  const child = Bun.spawn(["bash", join(checkout, "install.sh")], { cwd: checkout, env, stdout: "pipe", stderr: "pipe" })
  try {
    await Bun.sleep(200)
    expect(child.exitCode).toBeNull()
    expect(existsSync(join(config, "skills/jiro"))).toBe(false)
  } finally {
    release()
  }
  expect(await child.exited).toBe(0)
  expect(existsSync(lockfilePath)).toBe(false)
  expect(run("--check").status).toBe(0)
})

test("sync recovers a stale lock left by an interrupted process", () => {
  const lockfilePath = join(config, ".jiro-sync.lock.d")
  mkdirSync(lockfilePath, { recursive: true })
  const stale = new Date(Date.now() - 120_000)
  utimesSync(lockfilePath, stale, stale)
  expect(run().status).toBe(0)
  expect(existsSync(lockfilePath)).toBe(false)
})

test("@jiro is the complete skill rather than a forwarding alias", () => {
  const source = readFileSync(join(root, "skills/jiro/SKILL.md"), "utf8")
  expect(source).toMatch(/^name: jiro$/m)
  expect(source).not.toContain("jiro-mode")
  expect(source).toContain("## Core principles")
  expect(source).toContain("## Non-negotiables")
  expect(existsSync(join(root, "skills/jiro-mode"))).toBe(false)
  expect(existsSync(join(root, "commands/jiro-mode.md"))).toBe(false)
  expect(readFileSync(join(root, "commands/jiro.md"), "utf8")).toContain('id: "jiro"')
  const smoke = readFileSync(join(root, "scripts/smoke-jiro.ts"), "utf8")
  expect(smoke).toContain('skill: "jiro"')
  expect(smoke).toContain('skills: ["jiro"]')
  expect(smoke).toContain("const requiresSharedRules = item.text.length > 0")
  expect(smoke).toContain("if (requiresSharedRules && !sharedRulesRead)")
})

test("Jiro is the entry skill and its registered workers are chefs", () => {
  const skill = readFileSync(join(root, "skills/jiro/SKILL.md"), "utf8")
  const chef = readFileSync(join(root, "agents/chef.md"), "utf8")
  expect(skill).toContain("## Chefs")
  expect(skill).toContain("Jiro's workers are chefs")
  expect(chef).toContain("You are a chef, Jiro's worker agent")
  expect(chef).toContain("Load `jiro` through the `skill` tool before working")
  expect(chef).toMatch(/^mode: subagent$/m)
  expect(chef).not.toMatch(/^model:/m)
  for (const path of [
    "README.md", "agents/chef.md", "playbook/delegation/README.md",
    "skills/jiro/SKILL.md", "skills/create-subagent/SKILL.md",
  ]) {
    const text = readFileSync(join(root, path), "utf8")
    expect(text).not.toContain("kye-mode")
    expect(text).not.toMatch(/sous-chefs?/i)
  }
})

test("Jiro instructions and guides do not retain the retired mode or worker", () => {
  const documents = ["README.md", "playbook/delegation/README.md"]
  for (const kind of ["skills", "commands", "agents"]) {
    documents.push(...readdirSync(join(root, kind), { recursive: true, encoding: "utf8" })
      .filter((path) => path.endsWith(".md"))
      .map((path) => join(kind, path)))
  }
  for (const path of documents) {
    expect(/poteto/i.test(readFileSync(join(root, path), "utf8")), path).toBe(false)
  }
  expect(readdirSync(join(root, "skills")).filter((name) => /poteto/i.test(name))).toEqual([])
})

test("preserves an unowned custom Jiro command without claiming ownership", () => {
  const command = join(config, "commands/jiro.md")
  write(command, "My custom command.\n")
  expect(run().stdout).toContain("preserved custom /jiro command")
  expect(readFileSync(command, "utf8")).toBe("My custom command.\n")
  expect(readFileSync(join(config, "jiro-commands-manifest.txt"), "utf8")).toBe("correct.md\nteach.md\nunslop.md\n")
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

test("preserves custom and symlinked companion commands without claiming ownership", () => {
  write(join(config, "commands/correct.md"), "My correction command.\n")
  const target = join(temporary, "personal-teach.md")
  write(target, "Personal teaching command.\n")
  symlinkSync(target, join(config, "commands/teach.md"))
  write(join(config, "jiro-commands-manifest.txt"), "teach.md\n")
  const result = run()
  expect(result.status).toBe(0)
  expect(result.stdout).toContain("preserved custom /correct command")
  expect(result.stdout).toContain("preserved custom /teach command")
  expect(readFileSync(join(config, "commands/correct.md"), "utf8")).toBe("My correction command.\n")
  expect(lstatSync(join(config, "commands/teach.md")).isSymbolicLink()).toBe(true)
  expect(readFileSync(target, "utf8")).toBe("Personal teaching command.\n")
  expect(readFileSync(join(config, "jiro-commands-manifest.txt"), "utf8")).toBe("jiro.md\nunslop.md\n")
  expect(run("--check").status).toBe(0)
})

test("adopts generated pstack companion commands and archives their previous definitions", () => {
  const previous = "---\ndescription: Pstack command\n---\n<!-- generated by pstack install.sh (do not edit: overwritten on reinstall) -->\nUse the `skill` tool with `id: \"correct\"`.\n\n$ARGUMENTS\n"
  write(join(config, "commands/correct.md"), previous)
  expect(run().status).toBe(0)
  expect(readFileSync(join(config, "commands/correct.md"), "utf8")).toBe(readFileSync(join(root, "commands/correct.md"), "utf8"))
  const [backup] = readdirSync(join(dirname(config), "opencode-jiro-backups"))
  expect(readFileSync(join(dirname(config), "opencode-jiro-backups", backup, "commands/correct.md"), "utf8")).toBe(previous)
  expect(run("--check").status).toBe(0)
})

test("upgrades a legacy owned wrapper and preserves the previous content", () => {
  write(join(config, "commands/jiro.md"), "Prior managed wrapper.\n")
  write(join(config, "jiro-commands-manifest.txt"), "jiro.md\n")
  expect(run().status).toBe(0)
  expect(readFileSync(join(config, "commands/jiro.md"), "utf8"))
    .toBe(readFileSync(join(checkout, "commands/jiro.md"), "utf8"))
  const [backup] = readdirSync(join(dirname(config), "opencode-jiro-backups"))
  expect(readFileSync(join(dirname(config), "opencode-jiro-backups", backup, "commands/jiro.md"), "utf8"))
    .toBe("Prior managed wrapper.\n")
})

test("rejects a well-formed wrapper without its invocation contract before syncing", () => {
  write(join(checkout, "commands/jiro.md"), "---\ndescription: Broken wrapper\n---\nNo arguments.\n")
  expect(run().status).toBe(1)
  expect(existsSync(join(config, "skills/jiro"))).toBe(false)
})

test("rejects a marked companion wrapper with the wrong skill ID before syncing", () => {
  write(join(checkout, "commands/teach.md"), "---\ndescription: Broken teaching wrapper\n---\n<!-- jiro:command -->\nLoad the exact ID `why`.\n\n$ARGUMENTS\n")
  const result = run()
  expect(result.status).toBe(1)
  expect(result.stderr).toContain("/teach must load the exact skill ID and forward arguments")
  expect(existsSync(join(config, "skills/teach"))).toBe(false)
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
  const rules = join(checkout, "skills/jiro/references/shared-rules.md")
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
  rmSync(join(checkout, "commands/jiro.md"))
  rmSync(join(checkout, "agents/chef.md"))
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
  write(join(checkout, path), "Uncommitted rules.\n")
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

test("catalog changes are checked, synced once, and backed up alongside definitions", () => {
  expect(run().status).toBe(0)
  const installed = join(config, "upstream.json")
  const before = readFileSync(installed, "utf8")
  write(join(checkout, "upstream.json"), before + "\n")
  const checked = run("--check")
  expect(checked.status).toBe(1)
  expect(checked.stdout).toContain("Out of sync: upstream.json")
  expect(readFileSync(installed, "utf8")).toBe(before)
  expect(run().status).toBe(0)
  expect(readFileSync(installed, "utf8")).toBe(before + "\n")
  const [backup] = readdirSync(join(dirname(config), "opencode-jiro-backups"))
  expect(readFileSync(join(dirname(config), "opencode-jiro-backups", backup, "upstream.json"), "utf8")).toBe(before)
  expect(run().stdout).toContain("Synced 0 entries")
  expect(run("--check").status).toBe(0)
})

test("an invalid catalog prevents all installation", () => {
  write(join(checkout, "upstream.json"), '{"version": 1, "imports": []}\n')
  expect(run().status).toBe(1)
  expect(existsSync(join(config, "upstream.json"))).toBe(false)
  expect(existsSync(join(config, "skills/jiro"))).toBe(false)
})

test("invalid source metadata prevents all replacement", () => {
  expect(run().status).toBe(0)
  const installed = join(config, "skills/jiro/SKILL.md")
  const before = readFileSync(installed, "utf8")
  write(join(checkout, "skills/jiro/SKILL.md"), "Invalid skill.\n")
  expect(run().status).toBe(1)
  expect(readFileSync(installed, "utf8")).toBe(before)
  expect(existsSync(join(config, ".jiro-sync.lock.d"))).toBe(false)
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

test("real commits and pulls sync the corresponding checkout state", () => {
  git("init", "-b", "main")
  expect(run().status).toBe(0)
  git("add", "skills", "commands", "agents", "install.sh", "scripts/sync-opencode.ts", "package.json", "bun.lock")
  git("commit", "-m", "Initial fixture")
  const relative = "skills/jiro/references/shared-rules.md"
  git("checkout", "-b", "next")
  write(join(checkout, relative), "Committed shared rules.\n")
  git("add", "skills")
  git("commit", "-m", "Update shared rules")
  expect(readFileSync(join(config, relative), "utf8")).toBe("Committed shared rules.\n")
  git("checkout", "main")
  expect(run().status).toBe(0)
  expect(readFileSync(join(config, relative), "utf8")).not.toBe("Committed shared rules.\n")
  git("pull", "--ff-only", ".", "next")
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
