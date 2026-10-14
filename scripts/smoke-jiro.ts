#!/usr/bin/env bun
import { Command } from "commander"
import { spawnSync } from "node:child_process"
import { homedir } from "node:os"
import { dirname, join, resolve } from "node:path"
import { mkdirSync, mkdtempSync, readFileSync, rmSync, writeFileSync } from "node:fs"

type ToolPart = { type: string; name?: string; state?: { status: string; input?: { id?: string; path?: string }; error?: string } }
type Message = { type: string; skill?: string; content?: ToolPart[]; error?: { type?: string; message?: string } }
type Export = { data: { info: { id: string; location: { directory: string }; time: { updated: number } }; messages: Message[] } }
type Case = ({ command: string } | { skill: string }) & { text: string; skills: string[] }
type Result = { invocation: string; status: "pass" | "fail"; loaded: string[]; failures: string[] }

const cases: readonly Case[] = [
  { skill: "jiro", text: "", skills: ["jiro"] },
  { command: "jiro", text: "Review store.ts without editing it. Propose two simpler ownership shapes, choose one, and identify redundant layers and duplicated mutable state.", skills: ["jiro", "code-organization", "minimize-reader-load"] },
]

const program = new Command()
  .name("jiro-smoke")
  .description("Exercise @jiro and Jiro's installed slash commands in a read-only OpenCode fixture. Retain only a summary.")
  .option("--opencode <binary>", "OpenCode V2 CLI", "opencode")
  .option("--model <id>", "Model for this test session; leave user settings unchanged")
  .option("--delete-session", "Delete only this disposable test session after recording results")
  .action(async ({ opencode, model, deleteSession }: { opencode: string; model?: string; deleteSession?: boolean }) => {
    const output = mkdtempSync("/tmp/opencode/jiro-smoke-")
    const fixture = join(output, "fixture")
    mkdirSync(join(fixture, ".opencode"), { recursive: true })
    writeFileSync(join(fixture, "store.ts"), `class Store {
  items: string[] = []
  list() { return this.items }
}
class StoreProxy {
  items: string[]
  constructor(private store: Store) { this.items = [...store.items] }
  list() { return this.store.list() }
}
class StoreAdapter {
  items: string[]
  constructor(private proxy: StoreProxy) { this.items = [...proxy.items] }
  list() { return this.proxy.list() }
}
`)
    const installed = join(process.env.XDG_CONFIG_HOME || join(homedir(), ".config"), "opencode/skills")
    const permissions = [
      { action: "*", resource: "*", effect: "deny" },
      ...["read", "glob", "grep", "skill"].map((action) => ({ action, resource: "*", effect: "allow" })),
      { action: "external_directory", resource: `${installed}/*`, effect: "allow" },
    ]
    writeFileSync(join(fixture, ".opencode/opencode.json"), JSON.stringify({
      ...(model ? { model } : {}),
      default_agent: "jiro-proof",
      snapshots: false,
      agents: { "jiro-proof": { mode: "primary", steps: 24, permissions, ...(model ? { model } : {}) } },
    }))

    function api(method: string, path: string, data?: unknown, params?: Record<string, string>): string {
      if (params && (method !== "get" || path !== "/api/session")) throw new Error("Unverified parameterized API operation")
      const args = ["api", ...(params ? ["session.list"] : [method, path])]
      if (data !== undefined) args.push("--data", JSON.stringify(data))
      for (const [key, value] of Object.entries(params || {})) args.push("--param", `${key}=${value}`)
      const result = spawnSync(opencode, args, { cwd: fixture, encoding: "utf8", timeout: 180_000 })
      if (result.status !== 0) throw new Error(`OpenCode ${method} ${path} failed: ${result.error?.message || result.stderr.trim()}`)
      return result.stdout
    }

    let sessionID: string | undefined
    let active = false
    const results: Result[] = []
    let failure: string | undefined
    let cleanup = "kept"
    let updated: number | undefined
    function exportSession(): Export {
      if (!sessionID) throw new Error("No owned smoke session exists")
      const history = JSON.parse(api("get", `/api/experimental/session/${sessionID}/export`)) as Export
      if (history.data.info.id !== sessionID || resolve(history.data.info.location.directory) !== fixture) {
        throw new Error("Export does not match this smoke session and fixture")
      }
      updated = history.data.info.time.updated
      return history
    }
    function prompt(text: string) {
      if (!sessionID) throw new Error("No owned smoke session exists")
      const args = ["run", "--standalone", "--session", sessionID, "--agent", "jiro-proof", "--format", "json"]
      if (model) args.push("--model", model)
      args.push(text)
      const result = spawnSync(opencode, args, { cwd: fixture, encoding: "utf8", timeout: 180_000 })
      if (result.status !== 0) {
        exportSession()
        const events = result.stdout.split("\n").flatMap((line) => {
          try { return [JSON.parse(line)] } catch { return [] }
        })
        const reason = events.find((event) => event.type === "error")?.error?.message
        throw new Error(`OpenCode generation failed: ${reason || result.error?.message || result.stderr.trim()}`)
      }
    }
    try {
      const payload = JSON.parse(api("post", "/api/session", {
        title: "Jiro invocation smoke",
        agent: "jiro-proof",
        location: { directory: fixture },
        metadata: { jiro_invocation_smoke: { fixture } },
      }))
      const created = payload.data || payload
      sessionID = created.id
      if (!sessionID) throw new Error("OpenCode did not return the created session ID")
      if (resolve(created.location.directory) !== fixture) throw new Error("Created session is outside this fixture")
      for (const item of cases) {
        const invocation = "command" in item ? `/${item.command}` : `@${item.skill}`
        active = true
        if ("command" in item) {
          const commands = JSON.parse(api("get", "/api/command"))
          if (!commands.data.some((command: { name: string }) => command.name === item.command)) {
            throw new Error(`/${item.command} is not registered`)
          }
          const installedCommand = join(dirname(installed), "commands", `${item.command}.md`)
          const definition = readFileSync(installedCommand, "utf8")
          const sourceCommand = join(resolve(import.meta.dir, ".."), ".opencode/commands", `${item.command}.md`)
          if (definition !== readFileSync(sourceCommand, "utf8")) throw new Error("Installed command differs from Jiro")
          const template = definition.replace(/^---\n[\s\S]*?\n---\s*/, "").trim()
          prompt(template.replaceAll("$ARGUMENTS", item.text))
        } else {
          api("post", `/api/experimental/session/${sessionID}/skill`, { id: item.skill, resume: false })
          prompt("Acknowledge Jiro activation only. No work task is requested; do not invent one.")
        }
        api("post", `/api/experimental/session/${sessionID}/wait`)
        active = false
        const history = exportSession()
        const tools = history.data.messages.flatMap((message) => message.type === "assistant" ? message.content || [] : [])
          .filter((part) => part.type === "tool" && part.state?.status === "completed")
        const loaded = [...new Set([
          ...history.data.messages.filter((message) => message.type === "skill").map((message) => message.skill || ""),
          ...tools.filter((part) => part.name === "skill").map((part) => part.state?.input?.id || ""),
        ])].filter(Boolean)
        const sharedRulesRead = tools.some((part) => part.name === "read" && part.state?.input?.path?.endsWith("/references/shared-rules.md"))
        const requiresSharedRules = item.text.length > 0
        const failures = item.skills.filter((id) => !loaded.includes(id)).map((id) => `Skill not loaded: ${id}`)
        if (requiresSharedRules && !sharedRulesRead) failures.push("Shared rules were not read before the task")
        for (const message of history.data.messages) {
          if (message.type === "assistant" && message.error) {
            failures.push(`${message.error.type || "Model error"}: ${(message.error.message || "Generation failed").slice(0, 240)}`)
          }
        }
        const passed = failures.length === 0
        if (!passed) {
          for (const message of history.data.messages) {
            for (const part of message.content || []) {
              if (part.type === "tool" && part.state?.status === "error") {
                failures.push(`${part.name}: ${(part.state.error || "Tool failed").slice(0, 240)}`)
              }
            }
          }
        }
        results.push({ invocation, status: passed ? "pass" : "fail", loaded, failures })
        if (!passed) throw new Error(`${invocation} did not load the required skills and shared rules`)
      }
    } catch (error) {
      failure = error instanceof Error ? error.message : String(error)
      process.exitCode = 1
    } finally {
      if (active && sessionID) {
        try {
          api("post", `/api/session/${sessionID}/interrupt`)
          api("post", `/api/experimental/session/${sessionID}/wait`)
          active = false
        } catch {
          failure = `${failure || "Invocation failed"}. Session could not be stopped; fixture retained.`
        }
      }
      const summary = join(output, "summary.json")
      const save = () => writeFileSync(summary, JSON.stringify({ sessionID, fixture, model, results, failure, active, cleanup }, null, 2) + "\n")
      save()
      if (deleteSession && sessionID && !active) {
        try {
          const payload = JSON.parse(api("get", `/api/session/${sessionID}`))
          const info = payload.data || payload
          if (info.id !== sessionID || info.parentID || info.title !== "Jiro invocation smoke"
              || resolve(info.location.directory) !== fixture || info.metadata?.jiro_invocation_smoke?.fixture !== fixture
              || updated === undefined || info.time.updated !== updated) {
            throw new Error("Session no longer matches this disposable test")
          }
          const children = JSON.parse(api("get", "/api/session", undefined, { parentID: sessionID, limit: "1" }))
          if (!Array.isArray(children.data) || children.data.length || children.cursor?.next) {
            throw new Error("Unexpected child sessions require separate review before cleanup")
          }
          const activeSessions = JSON.parse(api("get", "/api/session/active"))
          if (activeSessions.data[sessionID]) throw new Error("Test session is still active")
          api("delete", `/api/session/${sessionID}`)
          cleanup = "deleted"
        } catch (error) {
          cleanup = "held"
          failure = `${failure || "Cleanup failed"}. ${error instanceof Error ? error.message : String(error)}`
          process.exitCode = 1
        }
        save()
      }
      if (!active && cleanup !== "held") rmSync(fixture, { recursive: true, force: true })
      console.log(`Summary: ${summary}`)
      for (const result of results) console.log(`${result.invocation}: ${result.status}`)
      if (failure) console.error(failure)
    }
  })

await program.parseAsync()
