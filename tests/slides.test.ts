import { expect, test } from "bun:test"
import { existsSync, readFileSync, realpathSync, statSync } from "node:fs"
import { join, resolve } from "node:path"

const root = resolve(import.meta.dir, "..")
const read = (path: string) => readFileSync(join(root, path), "utf8")
const catalog = JSON.parse(read("upstream.json"))
const record = (id: string) => catalog.imports.find((entry: { id: string }) => entry.id === id)
const frontmatter = (path: string) => Bun.YAML.parse(read(path).split("---", 3)[1]!) as Record<string, unknown>

test("slides is a licensed Jiro native tool with draft first approval", () => {
  const entry = record("slides")
  expect(entry).toMatchObject({
    targetRoots: ["skills/slides"],
    license: "skills/slides/LICENSE",
  })
  expect(entry.upstream.repository).toBe("https://github.com/kyeshmz/jiro.git")
  expect(read("skills/slides/LICENSE")).toBe(read("skills/how/LICENSE"))
  expect(frontmatter("skills/slides/SKILL.md")).toEqual({
    name: "slides",
    description: "Create slide decks and presentations, write a draft outline first, show it for approval, then build the deck. Use when the user mentions slides, slide deck, presentation, deck, pitch deck, Google Slides, or Keynote, or asks to make slides for a talk, update, proposal, or review, even when no file format is named.",
    license: "MIT",
  })
  expect(realpathSync(join(root, "skills/slides/references/shared-rules.md"))).toBe(realpathSync(join(root, "skills/skill.md")))
  const skill = read("skills/slides/SKILL.md")
  for (const section of [
    "### 1. Assess and gather the brief",
    "### 2. Write the draft and show it",
    "### 3. Enforce the text limit",
    "### 4. Add references and comments to every slide",
    "### 5. Revise on feedback",
    "### 6. Build the deck",
    "### 7. Show the result",
  ]) expect(skill).toContain(section)
  expect(skill).toContain("Draft first")
  expect(skill).toContain("500 words per slide")
  expect(skill).toContain("must be split into several slides")
  expect(skill).toContain("no 40 word max")
  expect(skill).toContain("Lists are treated differently")
  expect(skill).toContain("Ordered content goes in its own boxes")
  expect(skill).toContain("Assess the deck from context")
  expect(skill).toContain("Do not ask what the deck is about")
  expect(skill).toContain("2 different text boxes")
  expect(skill).toContain("Show the draft in chat")
  expect(skill).toContain("wait for approval")
  expect(skill).toContain("Titles are allowed")
  expect(skill).toContain("Subtitles are not allowed")
  expect(skill).toContain("Never use a bottom sentence")
  expect(skill).toContain("rounded box")
  expect(skill).toContain("Rounded boxes. No chamfered corners.")
  expect(skill).toContain("native circular bullets")
  expect(skill).toContain("companion Markdown source")
  expect(skill).toContain("not visual layout or editable slide objects")
  expect(skill).not.toContain("Each slide box, card, and callout uses chamfered corners")
  expect(skill).toContain("References field")
  expect(skill).toContain("speaker notes")
  expect(skill).toContain("Google Slides")
  expect(skill).toContain("Keynote")
  expect(skill).toContain("Do not claim that pasting or importing preserves layout")
  expect(skill).toContain("HTML")
  expect(skill).toContain("PPTX")
  expect(skill).not.toMatch(/[\u2013\u2014]/)
  expect(skill).not.toMatch(/\bpoteto\b|\.cursor\/|generalPurpose|subagent_type/)
  expect(existsSync(join(root, "commands/slides.md"))).toBe(true)
  expect(existsSync(join(root, "skills/slides/SKILL.md"))).toBe(true)
  expect(statSync(join(root, "skills/slides/SKILL.md")).isFile()).toBe(true)
})

test("slides command wrapper forwards the exact ID and arguments", () => {
  const command = read("commands/slides.md")
  expect(command).toContain('id: "slides"')
  expect(command).toContain("exact ID `slides`")
  expect(command.match(/\$ARGUMENTS/g)).toHaveLength(1)
  expect(command).toContain("split any slide over 500 words into several slides")
  expect(command).toContain("Assess the subject and audience from context")
  expect(command.split("---", 3)[1]).not.toMatch(/^(agent|model|subtask):/m)
})

test("slides is indexed for users", () => {
  expect(read("README.md")).toContain("[`@slides`](skills/slides/SKILL.md)")
  expect(read("skills/kstack-help/SKILL.md")).toContain("[@slides](../slides/SKILL.md)")
  expect(read("README.md")).toContain("`/slides`")
})
