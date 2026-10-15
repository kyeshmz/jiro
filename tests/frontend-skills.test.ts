import { expect, test } from "bun:test"
import { createHash } from "node:crypto"
import { existsSync, readFileSync, readdirSync } from "node:fs"
import { join, resolve } from "node:path"

const root = resolve(import.meta.dir, "..")
const skills = join(root, "skills")
const catalog = JSON.parse(readFileSync(join(root, "upstream.json"), "utf8"))
const imports = [
  { id: "react-best-practices", files: 76, rules: 70 },
  { id: "composition-patterns", files: 14, rules: 8 },
] as const

for (const item of imports) {
  test(`${item.id} retains its complete pinned WholeEarth source bundle`, () => {
    const directory = join(skills, item.id)
    const record = catalog.imports.find((entry: { id: string }) => entry.id === item.id)
    expect(record.upstream.repository).toBe("https://github.com/wholeearthrobotics/agent-skills.git")
    expect(record.sources[0].importedRevision).toBe("abd39e05df96b6ce3524050045b9131eb2fea0b3")
    expect(record.sources[0].path).toBe(`skills/${item.id}`)
    const hashes = record.fileHashes as Record<string, string>
    expect(Object.keys(hashes)).toHaveLength(item.files)
    for (const [relative, digest] of Object.entries(hashes)) {
      expect(relative.startsWith("/") || relative.split("/").includes("..")).toBe(false)
      expect(createHash("sha256").update(readFileSync(join(directory, relative))).digest("hex")).toBe(digest)
    }
    const rules = readdirSync(join(directory, "rules")).filter((name) => name.endsWith(".md") && !name.startsWith("_"))
    expect(rules).toHaveLength(item.rules)
    for (const name of ["AGENTS.md", "README.md", "metadata.json", "rules/_sections.md", "rules/_template.md"]) {
      expect(hashes[name]).toBeDefined()
    }
    const entry = readFileSync(join(directory, "SKILL.md"), "utf8")
    expect(entry).toMatch(new RegExp(`^name: ${item.id}$`, "m"))
    expect(entry).toContain("license: MIT")
    expect(entry).toContain("author: vercel")
    for (const match of entry.matchAll(/^- `([a-z0-9-]+)`/gm)) {
      expect(existsSync(join(directory, "rules", `${match[1]}.md`))).toBe(true)
    }
    expect(record.provenance).toContain(record.sources[0].importedRevision)
  })
}

test("Jiro routes React work and keeps the composition version gate", () => {
  const jiro = readFileSync(join(skills, "jiro/SKILL.md"), "utf8")
  for (const { id } of imports) expect(jiro).toContain(`Load \`${id}\``)
  expect(jiro).toContain("target's React and framework versions")
  const composition = readFileSync(join(skills, "composition-patterns/SKILL.md"), "utf8")
  expect(composition).toContain("React 19+ only")
  expect(composition).toContain("React 18 or earlier")
})
