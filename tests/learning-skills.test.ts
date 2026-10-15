import { expect, test } from "bun:test"
import { existsSync, readFileSync } from "node:fs"
import { join, resolve } from "node:path"

const root = resolve(import.meta.dir, "..")
const ids = ["correct", "teach", "unslop"]
const revision = "ccb5507cec1546dc88135c1139c811e6c59115ba"
const read = (path: string) => readFileSync(join(root, path), "utf8")

test("learning and writing skills are explicitly invoked, licensed, and registered for maintenance", () => {
  const registry = JSON.parse(read("upstream.json"))
  for (const id of ids) {
    const text = read(`skills/${id}/SKILL.md`)
    const metadata = text.split("---", 3)[1]
    expect(metadata).toContain(`name: ${id}\n`)
    expect(metadata).toMatch(/^description: \S/m)
    expect(metadata).toContain("license: MIT")
    expect(metadata).toContain("opencode/autoinvoke: false")
    expect(metadata).not.toContain("disable-model-invocation")
    expect(read(`skills/${id}/LICENSE`)).toBe(read("skills/how/LICENSE"))
    const entry = registry.imports.find((item: { id: string }) => item.id === id)
    expect(entry).toMatchObject({
      targetRoots: [`skills/${id}`],
      license: `skills/${id}/LICENSE`,
      sources: [{ path: `pstack/skills/${id}/SKILL.md`, importedRevision: revision, reviewedThrough: null }],
    })
    expect(entry.provenance).toContain(`https://github.com/cursor/plugins/blob/${revision}/pstack/skills/${id}/SKILL.md`)
  }
})

test("slash commands load the exact skills and forward arguments without model or agent overrides", () => {
  for (const id of ids) {
    const command = read(`commands/${id}.md`)
    expect(command).toContain("<!-- jiro:command -->")
    expect(command).toContain(`id: "${id}"`)
    expect(command).toContain(`exact ID \`${id}\``)
    expect(command.match(/\$ARGUMENTS/g)).toHaveLength(1)
    expect(command.split("---", 3)[1]).not.toMatch(/^(agent|model|subagent|subtask):/m)
    expect(read("README.md")).toContain("[`@" + id + "`]")
  }
})

test("correct ranks structural enforcement first and requires historical negative proof", () => {
  const text = read("skills/correct/SKILL.md")
  const levels = [...text.matchAll(/^\d+\. \*\*([^*]+)\*\*/gm)].map((match) => match[1])
  expect(levels).toEqual([
    "Eliminate it with architecture.", "Enforce it with types.", "Test the behavior.", "Write docs or agent rules last.",
  ])
  for (const requirement of [
    "happened twice", "real past mistake", "rejects it and accepts the corrected case",
    "same verification command locally", "expiry date", "a human's approval",
    "| Rule | Mistake evidence | Enforcement | Local and CI command | Proof or gap |",
    "Never guess session IDs", "Do not commit, push",
  ]) expect(text).toContain(requirement)
})

test("teach uses real read-only companions and incremental diagrams without inventing confidence", () => {
  const text = read("skills/teach/SKILL.md")
  for (const id of ["how", "why", "unslop"]) {
    expect(existsSync(join(root, "skills", id, "SKILL.md"))).toBe(true)
    expect(text).toMatch(new RegExp("load `" + id + "`", "i"))
  }
  for (const requirement of [
    "two independent read-only children", "prohibition on edits, commits, and external writes",
    "completion notifications rather than polling", "confidence language intact",
    "redraws the last and adds a single part or edge", "No quizzes",
    "plain-text spatial sketch", "Keep the task read-only",
  ]) expect(text).toContain(requirement)
})

test("unslop retains stable pattern numbers and protects meaning and justified uncertainty", () => {
  const text = read("skills/unslop/SKILL.md")
  const patterns = text.split("## Patterns to detect and fix\n")[1]
  expect([...patterns.matchAll(/^(\d+)\. \*\*/gm)].map((match) => Number(match[1]))).toEqual([
    3, 5, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33,
  ])
  expect(text).toContain("Evidence-backed uncertainty is not excessive hedging")
  expect(text).toContain("Keep citations, necessary qualifications, technical identifiers")
  expect(text).toContain("Edit files only when requested")
  expect(text).not.toContain("Must always apply")
})

test("representative scenarios cover correction, actual teaching investigation, and writing cleanup", () => {
  const scenarios = JSON.parse(read("tests/learning-skills.scenarios.json")).evals
  expect(scenarios.map((scenario: { skill: string }) => scenario.skill)).toEqual(ids)
  for (const scenario of scenarios) {
    expect(scenario.prompt).toContain(`@${scenario.skill}`)
    expect(scenario.expected_output.length).toBeGreaterThan(0)
    expect(scenario.assertions.length).toBeGreaterThan(0)
  }
})
