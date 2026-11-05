#!/usr/bin/env bun
import { Command } from "commander"
import { existsSync, readFileSync, readdirSync, statSync } from "node:fs"
import { basename, dirname, extname, join, relative, resolve, sep } from "node:path"
import { spawnSync } from "node:child_process"
import { createHash } from "node:crypto"

export type Finding = { file: string; line: number; rule: string; message: string; pinned?: boolean }

const frontmatterKeys = new Set(["name", "description", "license", "compatibility", "metadata", "disable-model-invocation"])

const markers: { rule: string; pattern: RegExp; fix: string }[] = [
  { rule: "deerflow-path", pattern: /\/mnt\/(skills|user-data)\b/g, fix: "resolve bundled files from the skill base directory and write output to a path the user confirms" },
  { rule: "deerflow-present-files", pattern: /\bpresent_files\b/g, fix: "report the saved path in the reply" },
  { rule: "task-tool", pattern: /`task` tool|\bthe Task tool\b|`Task` (?:call|tool|prompt)|\bTask\(/gi, fix: "use OpenCode's `subagent` tool" },
  { rule: "subagent-type", pattern: /\bsubagent_type\b/g, fix: "pass `agent` to the `subagent` tool" },
  { rule: "general-purpose-agent", pattern: /\bgeneralPurpose\b|["'`]general-purpose["'`]/g, fix: "use the built-in `general` agent" },
  { rule: "run-in-background", pattern: /\brun_in_background\b/g, fix: "pass `background: true` to the `subagent` tool" },
  { rule: "readonly-spawn", pattern: /\breadonly`?:\s*`?(?:true|false)\b/g, fix: "use a permission-restricted agent and forbid edits in the prompt" },
  { rule: "cursor-cloud", pattern: /\benvironment`?:\s*`?"(?:cloud|local)"|\bcloud_base_branch\b/g, fix: "run workers locally and name the branch in the brief" },
  { rule: "ask-question", pattern: /\bAsk(?:User)?Question\b|\ballow_multiple\b/g, fix: "use the `question` tool and its `multiple` option" },
  { rule: "cursor-path", pattern: /(?<![\w.-])\.cursor\//g, fix: "use `.opencode/` paths or the skill base directory" },
  { rule: "claude-plugin-root", pattern: /CLAUDE_PLUGIN_ROOT/g, fix: "resolve files from the skill base directory" },
  { rule: "connector-placeholder", pattern: /(?<![~\w])~~[a-z]/gi, fix: "name the connector category and use MCP tools already connected" },
  { rule: "connectors-file", pattern: /CONNECTORS\.md/g, fix: "inline the connector categories in the skill" },
  { rule: "skill-arguments", pattern: /\$ARGUMENTS\b/g, fix: "forward arguments through a command wrapper in commands/" },
  { rule: "web-tool-name", pattern: /`web_(?:fetch|search)`/g, fix: "use OpenCode's `webfetch` and `websearch` tools" },
  { rule: "v1-docs", pattern: /https:\/\/opencode\.ai\/docs\//g, fix: "link the V2 docs at https://opencode.ai/v2/docs/" },
]

const negation = /\b(?:not|never|no|don't|cannot|unsupported|without|instead of|rather than|avoid|forbids?|forbidden|rejects?|replac(?:e|es|ed|ing)|remov(?:e|es|ed|ing)|retir(?:e|es|ed|ing)|strip(?:s|ped)?|drop(?:s|ped)?|convert(?:s|ed)?)\b|-only\b/i
const clauseBoundary = /[.!?](?:\s|$)|\s[–—]\s|;\s|:\s|\|/g

type Block = { text: string; code: boolean; starts: { offset: number; line: number }[] }

function blocks(source: string): Block[] {
  const result: Block[] = []
  let current: Block | undefined
  let fence: string | undefined
  source.split("\n").forEach((raw, index) => {
    const marker = /^\s*(```+|~~~+)/.exec(raw)?.[1]
    if (marker && (!fence || marker.startsWith(fence))) {
      fence = fence ? undefined : marker
      current = undefined
      return
    }
    if (fence) {
      result.push({ text: raw, code: true, starts: [{ offset: 0, line: index + 1 }] })
      return
    }
    const line = raw.replace(/^\s*>\s?/, "")
    if (!line.trim() || /^\s*([-*+]|\d+\.)\s|^#{1,6}\s/.test(line)) current = undefined
    if (!line.trim()) return
    if (!current) {
      current = { text: "", code: false, starts: [] }
      result.push(current)
    }
    if (current.text) current.text += " "
    current.starts.push({ offset: current.text.length, line: index + 1 })
    current.text += line
  })
  return result
}

function lineAt(block: Block, index: number) {
  return block.starts.findLast((start) => start.offset <= index)!.line
}

function prohibited(text: string, index: number) {
  let start = 0
  for (const boundary of text.slice(0, index).matchAll(clauseBoundary)) start = boundary.index! + boundary[0].length
  return negation.test(text.slice(start, index))
}

function frontmatter(skill: string, file: string, text: string): Finding[] {
  const match = /^---\n([\s\S]*?)\n---(?:\n|$)/.exec(text)
  if (!match) return [{ file, line: 1, rule: "frontmatter", message: "SKILL.md needs YAML frontmatter with name and description" }]
  let data: Record<string, unknown>
  try {
    data = (Bun.YAML.parse(match[1]!) ?? {}) as Record<string, unknown>
  } catch (error) {
    return [{ file, line: 1, rule: "frontmatter", message: `frontmatter is not valid YAML: ${error instanceof Error ? error.message : error}` }]
  }
  const findings: Finding[] = []
  const id = basename(skill)
  const lineOf = (key: string) => 1 + (match[1]!.split("\n").findIndex((line) => line.startsWith(`${key}:`)) + 1 || 0)
  if (!/^[a-z0-9]+(-[a-z0-9]+)*$/.test(id) || id.length > 64) {
    findings.push({ file, line: 1, rule: "skill-id", message: `directory ${id} is not a lowercase kebab-case skill ID of 1-64 characters` })
  }
  if (data.name !== id) findings.push({ file, line: lineOf("name"), rule: "skill-name", message: `name must equal the directory ID ${id}` })
  if (typeof data.description !== "string" || !data.description.trim()) {
    findings.push({ file, line: lineOf("description"), rule: "skill-description", message: "a description is required for OpenCode to advertise the skill" })
  }
  for (const key of Object.keys(data)) {
    if (!frontmatterKeys.has(key)) {
      findings.push({ file, line: lineOf(key), rule: "frontmatter-key", message: `OpenCode V2 does not interpret \`${key}\`. Remove it; use metadata.opencode/autoinvoke, permissions, or a command wrapper` })
    }
  }
  const autoinvoke = (data.metadata as Record<string, unknown> | undefined)?.["opencode/autoinvoke"]
  if (autoinvoke !== undefined && typeof autoinvoke !== "boolean") {
    findings.push({ file, line: lineOf("metadata"), rule: "frontmatter-key", message: "metadata.opencode/autoinvoke must be a boolean" })
  }
  return findings
}

function installRoots(skill: string) {
  const skills = dirname(skill)
  const config = dirname(skills)
  return { skills, allowed: [join(config, "upstream.json"), join(config, "commands") + sep, join(config, "agents") + sep] }
}

function links(skill: string, file: string, text: string): Finding[] {
  const findings: Finding[] = []
  const { skills, allowed } = installRoots(skill)
  for (const block of blocks(text)) {
    if (block.code) continue
    const prose = block.text.replace(/`[^`]*`/g, (code) => " ".repeat(code.length))
    for (const match of prose.matchAll(/\[[^\]]*\]\(([^)\s]+)(?:\s+"[^"]*")?\)/g)) {
      const target = match[1]!.split("#")[0]!
      if (!target || /^[a-z][a-z0-9+.-]*:/i.test(target) || /[<{*]/.test(target)) continue
      const line = lineAt(block, match.index!)
      const path = resolve(dirname(file), decodeURI(target))
      if (!existsSync(path)) {
        findings.push({ file, line, rule: "broken-link", message: `${target} does not exist` })
        continue
      }
      const inSkill = path === skill || path.startsWith(skill + sep)
      const inSkills = path.startsWith(skills + sep) && relative(skills, path).includes(sep)
      if (!inSkill && !inSkills && !allowed.some((root) => path === root || path.startsWith(root))) {
        findings.push({ file, line, rule: "uninstalled-link", message: `${target} points outside what the installer copies, so it breaks in the installed skill` })
      }
    }
  }
  return findings
}

function resources(skill: string, file: string, text: string): Finding[] {
  const findings: Finding[] = []
  const lines = text.split("\n")
  lines.forEach((line, index) => {
    for (const match of line.matchAll(/`(?:<skill-base>\/)?((?:scripts|references|templates|assets|rules)\/[^`\s]+)`/g)) {
      const path = match[1]!
      if (/[<{*$]/.test(path) || path.endsWith("/")) continue
      if (!existsSync(join(skill, path))) {
        findings.push({ file, line: index + 1, rule: "missing-resource", message: `bundled resource ${path} is not in ${basename(skill)}/` })
      }
    }
  })
  return findings
}

function syntax(file: string): Finding[] {
  const run = extname(file) === ".py"
    ? spawnSync("python3", ["-I", "-c", "import ast, sys; ast.parse(open(sys.argv[1], 'rb').read(), sys.argv[1])", file], { encoding: "utf8" })
    : extname(file) === ".sh"
      ? spawnSync("bash", ["-n", file], { encoding: "utf8" })
      : undefined
  if (!run) return []
  if (run.error) return [{ file, line: 1, rule: "script-syntax", message: `could not run a syntax check: ${run.error.message}` }]
  if (run.status === 0) return []
  const output = (run.stderr || run.stdout).trim()
  const line = Number(/line (\d+)/.exec(output)?.[1] ?? 1)
  return [{ file, line, rule: "script-syntax", message: output.split("\n").at(-1) ?? "syntax error" }]
}

function walk(directory: string): string[] {
  return readdirSync(directory).sort().flatMap((name) => {
    if (name === "node_modules" || name === "__pycache__") return []
    const path = join(directory, name)
    return statSync(path).isDirectory() ? walk(path) : [path]
  })
}

function pinnedFiles(skill: string) {
  const catalog = join(dirname(dirname(skill)), "upstream.json")
  if (!existsSync(catalog)) return new Set<string>()
  const imports: { targetRoots?: string[]; fileHashes?: Record<string, string> }[] = JSON.parse(readFileSync(catalog, "utf8")).imports ?? []
  const record = imports.find((entry) => entry.targetRoots?.length === 1 && entry.targetRoots[0] === `skills/${basename(skill)}`)
  return new Set(Object.entries(record?.fileHashes ?? {})
    .filter(([path, digest]) => existsSync(join(skill, path))
      && createHash("sha256").update(readFileSync(join(skill, path))).digest("hex") === digest)
    .map(([path]) => join(skill, path)))
}

export function checkSkill(directory: string): Finding[] {
  const skill = resolve(directory)
  const entry = join(skill, "SKILL.md")
  if (!existsSync(entry)) return [{ file: entry, line: 1, rule: "frontmatter", message: "skill directory has no SKILL.md" }]
  const pinned = pinnedFiles(skill)
  const findings: Finding[] = []
  for (const file of walk(skill)) {
    if (extname(file) !== ".md") {
      findings.push(...syntax(file))
      continue
    }
    const text = readFileSync(file, "utf8")
    if (file === entry) findings.push(...frontmatter(skill, file, text))
    findings.push(...links(skill, file, text), ...resources(skill, file, text))
    for (const block of blocks(text)) {
      for (const { rule, pattern, fix } of markers) {
        for (const match of block.text.matchAll(pattern)) {
          if (prohibited(block.text, match.index!)) continue
          findings.push({ file, line: lineAt(block, match.index!), rule, message: `${JSON.stringify(match[0])} is not an OpenCode V2 reference. Fix: ${fix}` })
        }
      }
    }
  }
  return findings.map((finding) => pinned.has(finding.file) ? { ...finding, pinned: true } : finding)
}

export function skillDirectories(paths: string[]) {
  return paths.flatMap((path) => {
    const target = resolve(path)
    if (existsSync(join(target, "SKILL.md"))) return [target]
    return readdirSync(target).sort().map((name) => join(target, name)).filter((child) => existsSync(join(child, "SKILL.md")))
  })
}

if (import.meta.main) {
  const program = new Command()
    .name("check-opencode-skills")
    .description("Check that skills use OpenCode V2 frontmatter, tools, paths, and installable links. Findings in files whose bytes match upstream.json fileHashes are warnings, because pinned upstream bytes are fixed upstream.")
    .argument("[paths...]", "skill directories, or directories that contain skills", [resolve(import.meta.dir, "../skills")])
    .option("--json", "print findings as JSON")
    .action((paths: string[], options: { json?: boolean }) => {
      const skills = skillDirectories(paths)
      if (!skills.length) program.error("No skills found. Pass a skill directory or a directory of skills.")
      const findings = skills.flatMap(checkSkill)
      const errors = findings.filter((finding) => !finding.pinned)
      if (options.json) console.log(JSON.stringify(findings, null, 2))
      else {
        for (const { file, line, rule, message, pinned } of findings) {
          console.log(`${relative(process.cwd(), file)}:${line} ${pinned ? "warning" : "error"} ${rule} ${message}`)
        }
        const warnings = findings.length - errors.length
        console.log(`${skills.length} skills checked: ${errors.length} errors, ${warnings} warnings in hash-pinned upstream files.`)
      }
      process.exitCode = errors.length ? 1 : 0
    })
  await program.parseAsync()
}
