import { expect, test } from "bun:test"
import { createHash } from "node:crypto"
import { readFileSync, readdirSync, statSync } from "node:fs"
import { join, resolve } from "node:path"

const root = resolve(import.meta.dir, "..")
const directory = join(root, "skills/opencode-memory")

test("opencode-memory retains its complete, unchanged pinned source bundle", () => {
  const catalog = JSON.parse(readFileSync(join(root, "upstream.json"), "utf8"))
  const record = catalog.imports.find((entry: { id: string }) => entry.id === "opencode-memory")
  expect(record.upstream).toEqual({ repository: "https://github.com/R44VC0RP/skills.git", ref: "main" })
  expect(record.sources).toEqual([{
    path: "skills/opencode-memory",
    importedRevision: "0623f2ea9800f277e0e4e89bcc50a5290de3ab0f",
    reviewedThrough: null,
  }])
  const hashes = record.fileHashes as Record<string, string>
  const files = readdirSync(directory, { recursive: true })
    .filter((path) => statSync(join(directory, path)).isFile()).sort()
  expect(files).toHaveLength(6)
  expect(Object.keys(hashes).sort()).toEqual(files)
  for (const [path, digest] of Object.entries(hashes)) {
    expect(createHash("sha256").update(readFileSync(join(directory, path))).digest("hex"), path).toBe(digest)
  }
  for (const path of ["scripts/dream.sh", "scripts/scan-secrets.py"]) {
    expect(statSync(join(directory, path)).mode & 0o777, path).toBe(0o755)
  }
  expect(record.provenance).toContain(record.sources[0].importedRevision)
})
