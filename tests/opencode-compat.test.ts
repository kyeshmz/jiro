import { afterEach, expect, test } from "bun:test"
import { createHash } from "node:crypto"
import { mkdirSync, mkdtempSync, rmSync, writeFileSync } from "node:fs"
import { tmpdir } from "node:os"
import { dirname, join, resolve } from "node:path"
import { spawnSync } from "node:child_process"
import { checkSkill, skillDirectories } from "../scripts/check-opencode-skills"

const root = resolve(import.meta.dir, "..")
let temporary: string | undefined

afterEach(() => {
  if (temporary) rmSync(temporary, { recursive: true, force: true })
  temporary = undefined
})

function fixture(body: string, files: Record<string, string> = {}, frontmatter = "name: sample\ndescription: Sample skill.") {
  temporary = mkdtempSync(join(tmpdir(), "jiro-compat-"))
  const skill = join(temporary, "skills", "sample")
  mkdirSync(skill, { recursive: true })
  writeFileSync(join(skill, "SKILL.md"), `---\n${frontmatter}\n---\n\n${body}\n`)
  for (const [path, text] of Object.entries(files)) {
    mkdirSync(dirname(join(temporary, path)), { recursive: true })
    writeFileSync(join(temporary, path), text)
  }
  return skill
}

const rules = (skill: string) => new Set(checkSkill(skill).map((finding) => finding.rule))

test("every Jiro skill passes the OpenCode compatibility check outside hash-pinned upstream bytes", () => {
  const skills = skillDirectories([join(root, "skills")])
  expect(skills.length).toBeGreaterThan(60)
  expect(skills.flatMap(checkSkill).filter((finding) => !finding.pinned)).toEqual([])
})

test("flags DeerFlow, Claude plugin, and Cursor runtime references with their OpenCode fix", () => {
  const skill = fixture([
    "Run `python /mnt/skills/public/sample/scripts/run.py`, then call the `present_files` tool.",
    'You MUST delegate via the `task` tool with `subagent_type: "general-purpose"` and `run_in_background: true`.',
    "Search ~~knowledge base for notes. See [CONNECTORS.md](../../CONNECTORS.md).",
    "Read ${CLAUDE_PLUGIN_ROOT}/notes.md and ~/.cursor/skills/x. Use AskQuestion, then `web_fetch`.",
    "Spawn workers with `readonly`: `true` and `environment: \"cloud\"`.",
    "/sample $ARGUMENTS",
    "Docs live at https://opencode.ai/docs/skills.",
  ].join("\n\n"), {}, 'name: sample\ndescription: Sample skill.\nargument-hint: "<topic>"\nallowed-tools: Bash')
  expect(rules(skill)).toEqual(new Set([
    "deerflow-path", "deerflow-present-files", "task-tool", "subagent-type", "general-purpose-agent",
    "run-in-background", "connector-placeholder", "connectors-file", "broken-link", "claude-plugin-root",
    "cursor-path", "ask-question", "web-tool-name", "readonly-spawn", "cursor-cloud", "skill-arguments",
    "v1-docs", "frontmatter-key",
  ]))
  const task = checkSkill(skill).find((finding) => finding.rule === "task-tool")!
  expect(task.line).toBe(10)
  expect(task.pinned).toBeUndefined()
  expect(task.message).toContain("OpenCode's `subagent` tool")
})

test("a prohibition or modified-file notice may name a foreign reference, but a later clause cannot hide one", () => {
  expect(rules(fixture([
    "Do not pass unsupported `readonly` or `subagent_type` arguments.",
    "> **Modified file notice:** Jiro replaced DeerFlow's `task` tool and",
    "> `present_files` with OpenCode tools.",
    "```diff",
    "~~~ not a connector",
    "```",
  ].join("\n")))).toEqual(new Set())
  expect(rules(fixture("Delegate through the `task` tool — do not extract metadata yourself."))).toEqual(new Set(["task-tool"]))
})

test("checks skill identity, links that survive installation, bundled resources, and script syntax", () => {
  expect(rules(fixture("Body.", {}, "name: other\ndescription: \"\""))).toEqual(new Set(["skill-name", "skill-description"]))
  const skill = fixture([
    "Read [the guide](references/guide.md) and [provenance](../../upstream.json).",
    "Do not follow [a missing file](references/missing.md) or [the checkout README](../../README.md).",
    "Run `scripts/ok.py`, `scripts/broken.sh`, `scripts/broken.py`, and `scripts/absent.py`.",
  ].join("\n\n"), {
    "skills/sample/references/guide.md": "Guide.\n",
    "upstream.json": "{\"imports\": []}\n",
    "README.md": "Checkout only.\n",
    "skills/sample/scripts/ok.py": "print('ok')\n",
    "skills/sample/scripts/broken.sh": "if then\n",
    "skills/sample/scripts/broken.py": "def broken(:\n",
  })
  const findings = checkSkill(skill)
  expect(findings.map(({ file, rule }) => `${rule} ${file.slice(skill.length + 1)}`).sort()).toEqual([
    "broken-link SKILL.md",
    "missing-resource SKILL.md",
    "script-syntax scripts/broken.py",
    "script-syntax scripts/broken.sh",
    "uninstalled-link SKILL.md",
  ])
  expect(findings.find((finding) => finding.rule === "broken-link")!.message).toContain("references/missing.md")
  expect(findings.find((finding) => finding.rule === "uninstalled-link")!.message).toContain("../../README.md")
  expect(findings.find((finding) => finding.rule === "missing-resource")!.message).toContain("scripts/absent.py")
})

test("only bytes that still match the catalog's fileHashes are downgraded to pinned warnings", () => {
  const notes = "Delegate through the `task` tool.\n"
  const digest = createHash("sha256").update(notes).digest("hex")
  const catalog = JSON.stringify({ imports: [{ targetRoots: ["skills/sample"], fileHashes: { "NOTES.md": digest } }] })
  const skill = fixture("Body.", { "upstream.json": catalog, "skills/sample/NOTES.md": notes })
  expect(checkSkill(skill)).toMatchObject([{ rule: "task-tool", pinned: true }])
  writeFileSync(join(skill, "NOTES.md"), notes + "Edited locally.\n")
  expect(checkSkill(skill)).toMatchObject([{ rule: "task-tool" }])
  expect(checkSkill(skill)[0]!.pinned).toBeUndefined()
})

test("the CLI fails on errors and passes the installed pack", () => {
  const script = join(root, "scripts/check-opencode-skills.ts")
  const failing = spawnSync(process.execPath, ["run", script, fixture("Call the `present_files` tool.")], { encoding: "utf8" })
  expect(failing.status).toBe(1)
  expect(failing.stdout).toContain("error deerflow-present-files")
  const passing = spawnSync(process.execPath, ["run", script], { encoding: "utf8", cwd: root })
  expect(passing.status, passing.stdout).toBe(0)
  expect(passing.stdout).toMatch(/skills checked: 0 errors/)
})
