import { expect, test } from "bun:test"
import { existsSync, readFileSync } from "node:fs"
import { join, resolve } from "node:path"

const root = resolve(import.meta.dir, "..")
const skills = join(root, ".opencode/skills")
const principles = [
  "principle-attack-the-premise",
  "principle-build-the-lever",
  "principle-fix-root-causes",
  "principle-laziness-protocol",
  "principle-foundational-thinking",
  "principle-redesign-from-first-principles",
  "principle-subtract-before-you-add",
  "principle-minimize-reader-load",
] as const

for (const id of principles) {
  test(`${id} has explicit invocation, pinned provenance, and resolvable resources`, () => {
    const directory = join(skills, id)
    const source = readFileSync(join(directory, "SKILL.md"), "utf8")
    const frontmatter = source.match(/^---\n([\s\S]*?)\n---/)?.[1]
    expect(frontmatter).toBeDefined()
    expect(frontmatter).toMatch(new RegExp(`^name: ${id}$`, "m"))
    expect(frontmatter).toMatch(/^description: \S/m)
    expect(frontmatter).toContain("license: MIT")
    expect(frontmatter).toContain("  opencode/autoinvoke: false")
    expect(readFileSync(join(directory, "LICENSE"), "utf8")).toContain("Copyright (c) 2026 Lauren Tan")
    const provenance = readFileSync(join(directory, "UPSTREAM.md"), "utf8")
    expect(provenance).toContain(`cursor/plugins/dbf49813a39c1a5389c5e28cb8e4c1c2379e2454/pstack/skills/${id}/SKILL.md`)
    for (const text of [source, provenance]) {
      for (const match of text.matchAll(/\[[^\]]*\]\(([^)]+)\)/g)) {
        const target = match[1]!
        if (/^[a-z]+:/.test(target) || target.startsWith("#")) continue
        expect(existsSync(resolve(directory, target.split("#")[0]!))).toBe(true)
      }
    }
    const mode = readFileSync(join(skills, "jiro/SKILL.md"), "utf8")
    const canonical = id === "principle-minimize-reader-load" ? "minimize-reader-load" : id
    expect(mode).toContain(`Load \`${canonical}\``)
    const smoke = readFileSync(join(root, "recipes/scripts/smoke-skills.py"), "utf8")
    if (id === "principle-minimize-reader-load") {
      expect(smoke.split("NOTES =")[0]).toContain(`CASES["${id}"] = (`)
      expect(smoke.split("NOTES =")[0]).toContain(`+ CASES["${canonical}"]`)
      expect(smoke.split("NOTES =")[0]).toContain("Both successful loads must appear")
      expect(smoke).toContain(`requirements["${id}"] = requirements["${canonical}"]`)
    } else {
      expect(smoke.split("NOTES =")[0]).toContain(`"${id}":`)
      expect(smoke.slice(smoke.indexOf("requirements ="))).toContain(`"${id}":`)
    }
  })
}

test("principles preserve the census, rerun, and state-deletion gates", () => {
  expect(readFileSync(join(skills, principles[0], "SKILL.md"), "utf8"))
    .toContain("Do not start the next fix before the premise is written down and the census exists")
  expect(readFileSync(join(skills, principles[1], "SKILL.md"), "utf8"))
    .toContain("Make it safe to rerun")
  expect(readFileSync(join(skills, principles[2], "SKILL.md"), "utf8"))
    .toContain("Resetting or deleting user state requires explicit approval")
})

test("reader-load compatibility forwards to one canonical skill", () => {
  const alias = readFileSync(join(skills, "principle-minimize-reader-load/SKILL.md"), "utf8")
  expect(alias).toContain('id: "minimize-reader-load"')
  expect(alias).toContain("../minimize-reader-load/SKILL.md")
  expect(alias).not.toContain("## Apply")
  expect(alias).not.toContain("Layers to trace")
})

test("core principles use portable OpenCode paths and preserve scope", () => {
  for (const id of principles.slice(3, 7)) {
    const body = readFileSync(join(skills, id, "SKILL.md"), "utf8")
    expect(body).toContain("## OpenCode scope")
    expect(body).toContain("base directory")
    expect(body).not.toContain(".cursor/")
    expect(body).not.toContain("generalPurpose")
    expect(body).not.toContain("subagent_type")
    expect(body).not.toContain("/home/kyeshmz/")
  }
  const foundation = readFileSync(join(skills, "principle-foundational-thinking/SKILL.md"), "utf8")
  expect(foundation).toContain("data shape right before writing logic")
  expect(foundation).toContain("Subtract before you add")
  const redesign = readFileSync(join(skills, "principle-redesign-from-first-principles/SKILL.md"), "utf8")
  expect(redesign).toContain("foundational assumption from the start")
  const subtraction = readFileSync(join(skills, "principle-subtract-before-you-add/SKILL.md"), "utf8")
  expect(subtraction).toContain("keep its checks green")
})
