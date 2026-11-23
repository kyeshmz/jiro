import { expect, test } from "bun:test"
import { readFileSync, realpathSync } from "node:fs"
import { join, resolve } from "node:path"

const root = resolve(import.meta.dir, "..")
const read = (path: string) => readFileSync(join(root, path), "utf8")
const catalog = JSON.parse(read("upstream.json"))
const record = (id: string) => catalog.imports.find((entry: { id: string }) => entry.id === id)
const frontmatter = (path: string) => Bun.YAML.parse(read(path).split("---", 3)[1]!) as Record<string, unknown>
const skill = read("skills/bitwarden/SKILL.md")

test("bitwarden is a licensed Jiro native tool", () => {
  const entry = record("bitwarden")
  expect(entry).toMatchObject({
    targetRoots: ["skills/bitwarden"],
    license: "skills/bitwarden/LICENSE",
  })
  expect(entry.upstream.repository).toBe("https://github.com/kyeshmz/jiro.git")
  expect(read("skills/bitwarden/LICENSE")).toBe(read("skills/how/LICENSE"))
  const meta = frontmatter("skills/bitwarden/SKILL.md")
  expect(Object.keys(meta).sort()).toEqual(["description", "license", "name"])
  expect(meta.name).toBe("bitwarden")
  expect(meta.license).toBe("MIT")
  expect(meta.description).toContain("Bitwarden MCP server")
  expect(meta.description).toContain("tools.bitwarden")
  expect(realpathSync(join(root, "skills/bitwarden/references/shared-rules.md"))).toBe(realpathSync(join(root, "skills/skill.md")))
  for (const section of [
    "## 1. Check the server and the vault",
    "## 2. Find the item without reading secrets",
    "## 3. Use a secret",
    "## 4. Change the vault",
    "## 5. Report",
    "## 6. Install the server",
  ]) expect(skill).toContain(section)
  expect(skill).not.toMatch(/[–—]/)
})

test("bitwarden keeps the master password and raw items out of the context", () => {
  expect(skill).toContain("tools.bitwarden.status()")
  expect(skill).toContain("Continue only when `status` is `unlocked`")
  expect(skill).toContain("Never ask for, accept, or type the master password")
  expect(skill).toContain("Never run `bw login` or `bw unlock` yourself")
  expect(skill).toContain("`list` returns whole items")
  expect(skill).toContain("Never return its raw result")
  expect(skill).toContain("Never fetch `object: \"item\"` to read one field")
  expect(skill).toContain("`create_item` and `edit_item` return the stored item, secrets included")
})

test("bitwarden orders the ways to use a secret by exposure", () => {
  const inBlock = skill.indexOf("**Inside one execute block.**")
  const redirect = skill.indexOf("**Shell redirection.**")
  const reply = skill.indexOf("**Into the reply.**")
  expect(inBlock).toBeGreaterThan(0)
  expect(redirect).toBeGreaterThan(inBlock)
  expect(reply).toBeGreaterThan(redirect)
  expect(skill).toContain('session_file="${XDG_RUNTIME_DIR:-${TMPDIR:-/tmp}}/bitwarden-mcp.session"')
  expect(skill).toContain("umask 077")
  expect(skill).toContain('git check-ignore -q "$target"')
  expect(skill).toContain("Never type a secret value literally")
})

test("bitwarden gates destructive, sharing, and administrative tools", () => {
  for (const gated of ["**`delete`.**", "`permanent: true` cannot be undone", "**`move`.**", "**Any Send.**", "**`device_approval_*` and `confirm`.**", "**Organization administration.**"]) {
    expect(skill).toContain(gated)
  }
  expect(skill).toContain("Do it only with explicit authorization")
  expect(skill).toContain("Never write `BW_SESSION`, `BW_CLIENT_ID`, or `BW_CLIENT_SECRET` into `opencode.json`")
  expect(skill).toContain("run_once_after_opencode-bitwarden-mcp.sh")
})

test("bitwarden command wrapper forwards the exact ID and arguments", () => {
  const command = read("commands/bitwarden.md")
  expect(command).toContain("<!-- jiro:command -->")
  expect(command).toContain('id: "bitwarden"')
  expect(command).toContain("exact ID `bitwarden`")
  expect(command.match(/\$ARGUMENTS/g)).toHaveLength(1)
  expect(command).toContain("tools.bitwarden.status()")
  expect(command).toContain("Never ask for the master password")
  expect(command).toContain("Ask before deleting, moving, or sharing anything")
  expect(command.split("---", 3)[1]).not.toMatch(/^(agent|model|subtask):/m)
  expect(command).not.toMatch(/[–—]/)
})

test("bitwarden is indexed for users", () => {
  expect(read("README.md")).toContain("[`@bitwarden`](skills/bitwarden/SKILL.md)")
  expect(read("skills/kstack-help/SKILL.md")).toContain("[@bitwarden](../bitwarden/SKILL.md)")
  expect(read("README.md")).toContain("`/bitwarden`")
})
