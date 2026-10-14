import { expect, test } from "bun:test"
import { createHash } from "node:crypto"
import { existsSync, readFileSync, readdirSync } from "node:fs"
import { join, resolve } from "node:path"

const root = resolve(import.meta.dir, "..")
const skills = join(root, ".opencode/skills")
const imports = [
  { id: "react-best-practices", files: 76, rules: 70 },
  { id: "composition-patterns", files: 14, rules: 8 },
] as const

for (const item of imports) {
  test(`${item.id} retains its complete pinned WholeEarth source bundle`, () => {
    const directory = join(skills, item.id)
    const manifest = JSON.parse(readFileSync(join(directory, "import-manifest.json"), "utf8")) as {
      repository: string; revision: string; source: string; files: Record<string, string>
    }
    expect(manifest.repository).toBe("wholeearthrobotics/agent-skills")
    expect(manifest.revision).toBe("abd39e05df96b6ce3524050045b9131eb2fea0b3")
    expect(manifest.source).toBe(`skills/${item.id}`)
    expect(Object.keys(manifest.files)).toHaveLength(item.files)
    for (const [relative, digest] of Object.entries(manifest.files)) {
      expect(relative.startsWith("/") || relative.split("/").includes("..")).toBe(false)
      expect(createHash("sha256").update(readFileSync(join(directory, relative))).digest("hex")).toBe(digest)
    }
    const rules = readdirSync(join(directory, "rules")).filter((name) => name.endsWith(".md") && !name.startsWith("_"))
    expect(rules).toHaveLength(item.rules)
    for (const name of ["AGENTS.md", "README.md", "metadata.json", "rules/_sections.md", "rules/_template.md"]) {
      expect(manifest.files[name]).toBeDefined()
    }
    const entry = readFileSync(join(directory, "SKILL.md"), "utf8")
    expect(entry).toMatch(new RegExp(`^name: ${item.id}$`, "m"))
    expect(entry).toContain("license: MIT")
    expect(entry).toContain("author: vercel")
    for (const match of entry.matchAll(/^- `([a-z0-9-]+)`/gm)) {
      expect(existsSync(join(directory, "rules", `${match[1]}.md`))).toBe(true)
    }
    expect(readFileSync(join(directory, "UPSTREAM.md"), "utf8")).toContain(manifest.revision)
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
