import { expect, test } from "bun:test"
import { existsSync, readFileSync, readdirSync } from "node:fs"
import { join, resolve } from "node:path"

const root = resolve(import.meta.dir, "..")

test("one root catalog covers every installed skill with an explicit source repository", () => {
  const catalog = JSON.parse(readFileSync(join(root, "upstream.json"), "utf8"))
  expect(catalog.version).toBe(2)
  expect(catalog.upstream).toBeUndefined()
  const skills = readdirSync(join(root, "skills")).filter((id) => existsSync(join(root, "skills", id, "SKILL.md")))
  for (const id of skills) {
    const records = catalog.imports.filter((entry: { targetRoots: string[] }) => entry.targetRoots.includes(`skills/${id}`))
    expect(records, id).toHaveLength(1)
    expect(records[0].upstream.repository).toMatch(/^https:\/\/github\.com\/.+\.git$/)
    expect(records[0].provenance.length).toBeGreaterThan(0)
    expect(records[0].record).toBeUndefined()
  }
  const duplicateFiles = ["skills", "recipes", "playbook"].flatMap((directory) =>
    readdirSync(join(root, directory), { recursive: true })
      .filter((path) => path.endsWith("UPSTREAM.md") || path.endsWith("import-manifest.json"))
      .map((path) => join(directory, path)))
  expect(duplicateFiles).toEqual([])
  expect(existsSync(join(root, "playbook/upstream-maintenance/references/import-map.json"))).toBe(false)
})
