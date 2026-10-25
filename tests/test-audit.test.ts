import { expect, test } from "bun:test"
import { existsSync, readFileSync, readdirSync } from "node:fs"
import { dirname, join, resolve } from "node:path"

const root = resolve(import.meta.dir, "..")
const directory = join(root, "skills/test-audit")
const catalog = JSON.parse(readFileSync(join(root, "upstream.json"), "utf8"))
const slug = (heading: string) => heading.trim().toLowerCase().replace(/[^a-z0-9 -]/g, "").replace(/ /g, "-")

test("test-audit is a pinned, licensed OpenClaw import", () => {
  const record = catalog.imports.find((entry: { id: string }) => entry.id === "test-audit")
  expect(record.upstream).toEqual({ repository: "https://github.com/openclaw/openclaw.git", ref: "main" })
  expect(record.targetRoots).toEqual(["skills/test-audit"])
  expect(record.sources).toHaveLength(1)
  expect(record.sources[0].path).toBe(".agents/skills/test-audit")
  expect(record.sources[0].importedRevision).toMatch(/^[a-f0-9]{40}$/)
  expect(record.provenance).toContain(`openclaw/openclaw/tree/${record.sources[0].importedRevision}/.agents/skills/test-audit`)
  const license = readFileSync(join(root, record.license), "utf8")
  expect(license).toStartWith("MIT License")
  expect(license).toContain("Copyright (c) 2026 OpenClaw Foundation")
  const metadata = readFileSync(join(directory, "SKILL.md"), "utf8").match(/^---\n([\s\S]*?)\n---/)?.[1] || ""
  expect(Bun.YAML.parse(metadata)).toMatchObject({ name: "test-audit", license: "MIT", metadata: { "opencode/autoinvoke": false } })
})

test("every bundled test-audit link resolves from the skill directory", () => {
  const markdown = readdirSync(directory, { recursive: true, encoding: "utf8" }).filter((path) => path.endsWith(".md"))
  expect(markdown.sort()).toEqual(["CAMPAIGN.md", "SKILL.md", "references/audit.md"])
  for (const file of markdown) {
    const source = join(directory, file)
    for (const match of readFileSync(source, "utf8").matchAll(/\[[^\]]*\]\(([^)\s]+)\)/g)) {
      if (/^[a-z]+:/i.test(match[1]!)) continue
      const [path, anchor] = match[1]!.split("#")
      const target = path ? resolve(dirname(source), path) : source
      expect(existsSync(target), `${file}: ${match[1]}`).toBe(true)
      if (!anchor) continue
      const headings = [...readFileSync(target, "utf8").matchAll(/^#+ (.+)$/gm)].map((heading) => slug(heading[1]!))
      expect(headings, `${file}: ${match[1]}`).toContain(anchor)
    }
  }
})

test("Jiro routes test audits to test-audit", () => {
  expect(readFileSync(join(root, "skills/jiro/SKILL.md"), "utf8")).toContain("load `test-audit`")
  expect(readFileSync(join(root, "skills/kstack-help/SKILL.md"), "utf8")).toContain("(../test-audit/SKILL.md)")
})
