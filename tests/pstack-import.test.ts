import { expect, test } from "bun:test"
import { existsSync, readFileSync, readdirSync, realpathSync } from "node:fs"
import { dirname, join, resolve } from "node:path"

const root = resolve(import.meta.dir, "..")
const read = (path: string) => readFileSync(join(root, path), "utf8")
const catalog = JSON.parse(read("upstream.json"))
const migration = catalog.pstackMigration
const existing = new Set([
  "bro", "correct", "create-verification-skill", "how", "jiro", "no-comments",
  "principle-attack-the-premise", "principle-build-the-lever", "principle-fix-root-causes",
  "principle-foundational-thinking", "principle-laziness-protocol", "principle-minimize-reader-load",
  "principle-redesign-from-first-principles", "principle-subtract-before-you-add", "reflect",
  "show-me-your-work", "swarm", "teach", "unslop", "why",
])
const imported = [...new Set<string>(Object.values(migration.skills))].filter((id) => !existing.has(id))

test("the pinned OpenCode pstack inventory has a target for every source skill", () => {
  expect(migration.repository).toBe("https://github.com/kyeshmz/opencode-pstack.git")
  expect(migration.revision).toBe("21d2804fb2ac7aa4f9fdd93a5b82465c86296eb5")
  expect(migration.mirroredCursorRevision).toMatch(/^[a-f0-9]{40}$/)
  expect(Object.keys(migration.skills)).toHaveLength(55)
  expect(migration.skills["poteto-mode"]).toBe("jiro")
  expect(migration.skills["poteto-help"]).toBe("kstack-help")
  expect(migration.skills["setup-pstack"]).toBe("setup-kstack")
  for (const id of Object.values<string>(migration.skills)) {
    expect(existsSync(join(root, "skills", id, "SKILL.md")), id).toBe(true)
    const owners = catalog.imports.filter((entry: { targetRoots: string[] }) =>
      entry.targetRoots.some((path) => path === `skills/${id}` || path.startsWith(`skills/${id}/`)))
    expect(owners, id).toHaveLength(1)
  }
})

for (const id of imported) {
  test(`${id} is a native, licensed Jiro tool with shared writing rules`, () => {
    const source = read(`skills/${id}/SKILL.md`)
    const metadata = source.match(/^---\n([\s\S]*?)\n---/)?.[1] || ""
    expect(metadata).toContain(`name: ${id}\n`)
    expect(metadata).toMatch(/^description: \S/m)
    expect(metadata).toContain("license: MIT")
    expect(metadata).toContain("opencode/autoinvoke: false")
    expect(Bun.YAML.parse(metadata)).toMatchObject({ name: id, license: "MIT", metadata: { "opencode/autoinvoke": false } })
    expect(read(`skills/${id}/LICENSE`)).toBe(read("skills/how/LICENSE"))
    expect(source).toContain("references/shared-rules.md")
    expect(realpathSync(join(root, "skills", id, "references/shared-rules.md")))
      .toBe(realpathSync(join(root, "skills/skill.md")))
    expect(source).not.toMatch(/poteto|\.cursor\/|generalPurpose|subagent_type|\{\{CONFIG_DIR\}\}/i)
    expect(source).not.toMatch(/[\u2013\u2014]/)
    const directory = join(root, "skills", id)
    for (const file of readdirSync(directory, { recursive: true, encoding: "utf8" }).filter((path) => path.endsWith(".md"))) {
      const markdown = join(directory, file)
      for (const match of readFileSync(markdown, "utf8").matchAll(/\[[^\]]*\]\(([^)]+)\)/g)) {
        const path = match[1]!.split("#")[0]!
        if (!path || /^[a-z]+:/i.test(path) || path.includes("<")) continue
        expect(existsSync(resolve(dirname(markdown), path)), `${id}/${file}: ${path}`).toBe(true)
      }
    }
  })
}

test("first-use verification is default, task-specific, idempotent, and permission-aware", () => {
  const skill = read("skills/jiro/SKILL.md")
  const setup = skill.split("## Repository verification setup\n")[1]?.split("## Recipe book")[0] || ""
  for (const requirement of [
    "by default", "initializes Jiro or Kstack", "first task that permits repository edits",
    "does not need to ask", "explicit opt-out", "read-only", "Activation without a task",
    "Reuse a relevant verification skill", "unrelated `verify-*`", "tests alone",
    "load `create-verification-skill`", "before product implementation", "existing harness",
    "Launch, doctor, drive", "evidence survives cleanup", "blockers, not proof",
    "parent owns setup", "Children reuse", "do not add a global first-use flag",
  ]) expect(setup, requirement).toContain(requirement)
  expect(skill).not.toContain("If none exists and building one fits the task")
  expect(read("skills/jiro/references/recipes.md")).toContain("Repository verification setup")
  expect(read("skills/create-verification-skill/SKILL.md")).toContain("first editable task")
})

test("Jiro routes every newly imported principle without preloading the entire pack", () => {
  const skill = read("skills/jiro/SKILL.md")
  for (const id of imported.filter((id) => id.startsWith("principle-"))) {
    expect(skill, id).toContain(`\`${id}\``)
  }
  expect(skill).toContain("Load only those that change a decision")
})

test("imported design workflows preserve comparison, isolation, and task-local artifacts", () => {
  const arena = read("skills/arena/SKILL.md")
  for (const phase of ["Frame", "Fan out", "Cross-judge", "Pick", "Graft", "Verify"]) {
    expect(arena).toContain(`## ${phase}`)
  }
  expect(arena).toContain("Keep the selection rubric out of candidate prompts")
  expect(arena).toContain("separate worktree or disjoint artifact directory")
  expect(read("skills/architect/SKILL.md")).toContain("task-local rationale")
  expect(read("skills/architect/SKILL.md")).toContain("Never edit the bundled template")
  expect(read("skills/figure-it-out/SKILL.md")).toContain("Jiro's Repository verification setup")
})

test("the shared writing contract does not grant unrelated external writes", () => {
  const rules = read("skills/skill.md")
  expect(rules).toContain("Short declarative sentences")
  expect(rules).toContain("consumer and the maintainer")
  expect(rules).toContain("Keep read-only requests read-only")
  expect(rules).toContain("Do not commit, push, open or merge a PR")
  expect(rules).not.toContain("external actions (team chat")
})
