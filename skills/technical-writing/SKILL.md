---
name: technical-writing
description: Write or review technical prose with Diátaxis structure, Google developer style, STE instruction rules, and Global English syntax. Use for @technical-writing or an explicit request to apply this standard to docs, RFCs, READMEs, PR descriptions, or commit messages.
license: MIT
metadata:
  opencode/autoinvoke: false
---

# Technical writing

Write so a tired engineer understands on the first read. Give readers the outcome they need. Leave maintainers accurate names, evidence, and instructions they can keep current.

Read `references/shared-rules.md` from this skill's reported base directory. Apply all four layers below. Load `unslop` for the prose this task touches. That skill owns the pattern catalog. Do not edit unrelated writing or the writing skills themselves.

## Keep the rules subordinate to meaning

- Cut words that do no work. Replace "in order to" with "to". Delete "it is important to note that".
- Prefer the short everyday word. Use "use", "help", and "do". A longer word must add precision.
- When a rule makes a sentence worse, find another sentence or leave it alone. Mechanical compliance is not clarity.
- Use the codebase's real symbols, files, flags, and commands. Do not replace them with synonyms.
- Do not invent jargon. Say "move", "delete", or "a budget that only decreases". Define a useful named pattern on first use.

If you find a new recurring abstract metaphor, propose its plain replacement in the reply. Show a small suggested diff to the relevant `unslop` rule. Do not change that skill without authorization.

## Keep the rhythm readable

Short sentences can still vary in length. Keep one thought in each sentence. Split distinct instructions or claims. Do not stretch a sentence merely to vary the rhythm.

Be specific. "A column rename fails the build" tells the reader more than "schema changes can cause issues". Explanation can weigh tradeoffs and state a supported judgment. Reference stays factual.

## 1. Pick one document mode

Use the Diátaxis questions. Does the content support action or understanding? Does it serve learning or work?

| Purpose | Mode |
| --- | --- |
| Action for learning | Tutorial. |
| Action for work | How-to. |
| Understanding for work | Reference. |
| Understanding for learning | Explanation. |

Apply the distinction to the whole document and to misplaced sentences. Split and link distinct modes instead of mixing them.

### Tutorial

Own the learner's success. Open with what the learner builds. Make each step produce a visible result early. State expected output, a changed prompt, or a log line. Keep explanations to a short clause and a useful link. Use concrete commands and a consistent "we" voice.

Do not insert reference tables or optional detours into the learning path.

### How-to

Solve a real goal, not an operation the machine can perform. Assume competence. Give actions without background digressions or completeness for its own sake. Link explanations and reference separately.

Allow judgment and branches. Put a condition before its action. Name the guide for the task, such as "Calibrate the radar array".

### Reference

Describe facts for lookup. State options, limits, defaults, errors, and version constraints precisely. Mirror the described system's structure. Generate facts from code when practical.

Do not add tutorial narration, persuasion, or unsupported confidence. If a fact is unknown, say it is unknown. A reference tone does not justify removing a real uncertainty.

### Explanation

Answer one bounded why question. Make the topic understandable away from the product. Include relevant history, constraints, design decisions, alternatives, and tradeoffs. A concept title should tolerate "About" before it.

Separate evidence from inference. A supported opinion belongs here, not in reference.

## 2. Address the reader directly

Apply Google developer style.

- Use "you" and the present tense. Reserve "will" for an event that genuinely happens later.
- Say who does what. Prefer "the compiler checks" over "is checked". Passive is useful only when the actor is unknown or irrelevant.
- Write instructions as commands. Use "Click **Submit**." Avoid "should be done".
- Put the condition before the guarded instruction. Put the common case before exceptions.
- Sound like a knowledgeable colleague. Avoid buzzwords, figurative language, and "please" in instructions. Do not call procedures "simple", "easy", or "quick".
- Do not announce unshipped work as a promise. Avoid repeated sentence openings.
- Give links descriptive text. Prefer the page title or destination purpose over "click here".
- Use sentence-case headings. Use a bare verb phrase for a task and a noun phrase for a concept. Keep one H1 and do not skip heading levels.
- Number sequences. Use bullets for unordered items. Introduce lists with complete sentences and keep their items parallel.
- Put code in code font and UI labels in bold. Use serial commas. Say when a list is partial instead of writing "etc.".

## 3. Make instructions load one at a time

Apply STE instruction rules.

- Give one instruction per sentence. Give one thought per sentence elsewhere.
- Inspect instructions over about 20 words and other sentences over about 25. Split them when that improves comprehension.
- Put a warning or condition before the action it guards.
- Keep necessary articles. "Remove the backup file" is less ambiguous than "Remove backup file".
- Give each word one meaning. If "check" means inspect, do not also use it to mean restrain.
- Pick one word for each action. Do not alternate "start" and "initiate" for the same operation.
- Use direct commands rather than passive narration. Write "Install the component".
- Remove unnecessary words ending in "-ing". Keep technical terms and grammar that need them.

## 4. Remove competing readings

Apply Global English syntax.

- Put "only" and "not" beside the words they modify. "Only fails on growth" and "fails only on growth" make different claims.
- Break up noun strings. Write "the script that checks the proto-import budget" instead of "the proto import budget check script".
- Give "it", "they", "this", and "which" one obvious referent. Repeat the noun when needed.
- Keep verbs in each clause. Write "Phase 2 moves the runtime" rather than "Phase 2 the runtime".
- Keep small words that show structure. Do not drop "that" when the sentence needs it.
- Repeat articles when they distinguish separate things. Use "the client and the host" for two actors.
- Make grouping explicit with "both ... and", "either ... or", or "if ... then".
- Use periods instead of semicolons or long dashes. Give parenthetical thoughts their own sentences when they matter.
- Do not form plurals with "(s)". Avoid prose slashes and "and/or". Keep literal paths, commands, URLs, and syntax unchanged.
- Name each thing consistently. Do not cycle through metaphors for one mechanism.
- Avoid idioms, Latin abbreviations, colloquialisms, and metaphors that make translation harder.

## Respect the repository and the request

Apply sentence rules to PR descriptions and commit messages. Diátaxis does not classify those short briefings. Keep a PR body readable in about a minute. Link bulky measurements and logs rather than pasting raw worker output or SHA lists. Writing a PR description does not authorize opening a PR or making a commit.

Use product copy guidelines for UI strings. Follow repository indentation in code snippets. Prefer tabs when the repository has no rule. Use real paths. Ground counts and directory trees in the actual checkout and give the command that regenerates them.

Preserve citations, legal notices, exact technical syntax, and justified uncertainty. Do not invent links or stronger claims. In a review, report material problems with proposed replacements. In an editing task, return or write the corrected text within the authorized scope.

## Worked example

Before.

> Configuration of the proto import budget check script parameters is performed via budget.json. It is important to remember that running with --write should only be done when lowering the budget. If exceeded, CI fails.

After.

> `budget.mjs` reads the committed budget from `budget.json` and counts files that import protos. If the count exceeds the budget, CI fails. Run `budget.mjs --write` only to lower the budget.
