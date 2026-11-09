---
name: slides
description: Create slide decks and presentations, write a draft outline first, show it for approval, then build the deck. Use when the user mentions slides, slide deck, presentation, deck, pitch deck, Google Slides, or Keynote, or asks to make slides for a talk, update, proposal, or review, even when no file format is named.
license: MIT
---

# Slides

Build a short presentation the user can approve before any file is made. The rule for this skill is draft first, build second, and keep every slide light on text.

Read `references/shared-rules.md` from this skill's reported base directory. Resolve every bundled reference from that directory, not the shell working directory.

## When to use this skill

Use this skill when the user wants slides or a presentation. That includes a pitch, an update, a walkthrough, a proposal, a status report, and a teaching deck. Also use it when the user says make me a deck or turn this into slides. Also use it when the user wants a deck they can paste into Google Slides or Keynote later. Do not use it for a plain document or a chat summary unless the user asks for slides.

## Quick start

Run it like this:

```text
/slides Turn the Q3 results into a 10 slide update for the team.
```

Or load it directly:

```text
@slides Make a 5 slide pitch for the new onboarding flow.
```

The first step is always a draft. The draft goes in chat. No deck file is made before the user approves the draft.

## Workflow

### 1. Assess and gather the brief

Assess the deck from context. Do not ask what the deck is about or who the audience is. Infer the subject and the likely audience from the request, the conversation, and any supplied files or links. Use that assessment in the draft header.

Ask one round only with the `question` tool when it is available. Ask only for details that context cannot settle:

- Goal. What decision or outcome the slides should drive.
- Length. How many slides and how long the talk runs, when the request states none.
- Format. Default to a browser-ready HTML deck and a companion Markdown source. Support other requested formats with available tools.
- Sources. Which notes, files, numbers, or links to ground the slides in, when none are supplied.
- Style. Tone, branding, and any must avoid content.

State the assessed subject and audience in the draft header so the user can correct them in one pass. When the context is truly thin, make the lightest honest assessment and flag the uncertainty in the draft. Do not turn the topic or the audience into a direct question.

### 2. Write the draft and show it

Show the draft in chat before building anything. The draft is the contract for the deck. The user approves the story, not the styling.

Use this structure for the draft:

```markdown
# Deck title

Audience. Goal. Slide count. Format. Paste target or none.

## Slide 1. Title
Takeaway. One sentence the slide must land.
Bullets. Up to 4 short bullets.
Speaker notes. What to say out loud. Keep script detail here.
References. Sources and comments for every claim on this slide.
Visual. Chart, screenshot, diagram, or none.
```

Keep the same fields on every slide. The draft must show the full arc in order. Title slide, problem or context, evidence or walkthrough, decision or next step, and closing. Put the ask or the decision early when the deck is a pitch or a proposal.

Titles are allowed. One title per slide. Subtitles are not allowed. Do not add a subtitle line under the deck title or under any slide title. Do not add a subtitle field to the draft template. If extra framing is needed, put it in speaker notes or in the first bullet.

Never use a footer. Do not add a bottom sentence to describe or summarize the slide or the deck, and do not add a source label or attribution line at the bottom. The bottom area is empty except for a slide number when needed. Sources live in speaker notes and slide comments only, never as visible text at the bottom.

Show the draft in the chat reply. Then stop and wait for approval. Use the `question` tool with these choices when it is available.

- Approve draft and build
- Revise draft first
- Build a shorter version

Do not build files while the draft is unapproved. Do not rename an unapproved draft as final.

### 3. Enforce the text limit

Every slide carries minimal text. Talk is spoken. Slides carry the point, not the script.

- There is no 40 word max. Judge each slide by format, not by a single word count for all slides.
- Prose paragraphs stay minimal. A paragraph on a slide is a sign to split or move detail into speaker notes.
- Lists are treated differently. A bunch of words that belong in a list can carry more total words when each item stays short and scannable. Judge a list by whether a reader can scan it at a glance, not by word count alone.
- Hard cap is 500 words per slide. Anything over 500 words on one slide is too much and must be split into several slides before building.
- Split when a slide mixes two ideas, runs past 4 bullets, or needs a paragraph to explain itself. The fix is more slides, not smaller font.
- Move detail into speaker notes. Notes can carry the full explanation. Visible text stays short.
- Cut filler sentences. Each bullet should be a scannable phrase or a short claim with evidence.
- Ordered content goes in its own boxes. When items deserve order, such as steps, sequence, or rank, place each item in its own rounded box with its number. Do not stack all ordered items into one bullet list in the visual deck.
- Never add a footer. Do not place a bottom sentence, source label, or attribution line at the bottom of any slide. Slide number is the only allowed bottom element.

Check the draft against this limit and say the word count, the format call, or the split decision for any slide near the cap. List heavy slides need a scannability call. The build must keep the same cap.

### 4. Add references and comments to every slide

Every factual claim needs a source. The source lives in the slide comments and in the speaker notes.

- Give every slide a References field in the draft. List the source for each bullet and each number in the draft. Keep sources in comments and speaker notes only. Do not put a short label on the slide.
- Map each claim to its source in the draft. Vague credit like sources above is not enough. Each bullet or number should be traceable to one named source.
- In the built deck, embed the same comments in speaker notes on every slide. In HTML, add an HTML comment per slide and a notes section with the full reference. In PPTX, add the full reference to speaker notes.
- Do not add a visible footer. Attribution lives only in slide comments and speaker notes. Keep full links and notes in the comments, never as visible footer text.
- Label estimates as estimates. Say who estimated and from what data when that is known.
- Flag any claim with no source at draft time. Do not build around an ungrounded claim.

### 5. Revise on feedback

Apply the change to the draft and show the revised draft again. Keep the same show and approve loop until the user approves or asks you to proceed with a noted gap.

When the user corrects tone, audience, or length, update the draft header so the approved version states the final choice.

### 6. Build the deck

Build only after approval. Build to the approved draft. Do not add new claims in the build step.

Output rules:

- Default output is a browser-ready HTML deck and a companion Markdown source. Keep the same slide order, visible wording, speaker notes, and references in both. Use a heading for each slide, standard Markdown lists, and `---` between slides. Keep notes and references labeled separately from visible slide text.
- Use ordinary semantic lists and native circular bullets. Do not use decorative or custom bullet glyphs. In HTML use `ul` and `li` with standard disc markers. In an editable presentation use native bullet lists.
- Make the HTML copy friendly with separate title and content elements and simple lists. Markdown preserves text and list structure, not visual layout or editable slide objects. Explain that the user may need to recreate formatting and copy notes into the target application. Do not claim that pasting or importing preserves layout or separate text boxes unless tested in the target application.
- For Google Slides or Keynote, provide the Markdown and HTML. Give concise copy steps. State which target applications and import or paste behaviors were actually tested.
- Add a PPTX build when the user asks for it or needs to edit in PowerPoint. Use a checked local toolchain for PPTX generation. Check what is installed before claiming it exists.
- Save to a path the user confirms. Never write into the installed skill directory.
- Match the approved slide order and titles. Each slide title is the takeaway where possible. Do not add subtitles in the build. Do not add a footer or bottom summary sentence in the build.
- Keep visible text under the same limit as the draft. Speaker notes carry the script.
- Add a visual where the draft calls for one. Use a simple chart, table, or diagram. In speaker notes and comments, name the source for every number or mark it as an estimate from the draft. Do not label numbers with visible footer text.
- Give slide boxes, cards, and callouts rounded corners. Do not chamfer their corners.
- Use a plain slide canvas and an unfilled title text box. Reserve background fills for content boxes that group items such as bullets or numbered steps. Do not add a decorative title banner or other filled background elements.
- Keep the title separate from body text and visuals. Use a content-sized text box for the title and for each independent body block, label, or caption. Grouping frames and layout containers are separate from these text boxes.

#### Fit text boxes to their content

Always size every text box to its actual content plus modest, consistent padding. This applies to titles, body text, lists, labels and captions in HTML, PowerPoint, Google Slides and other presentation formats. Tight bounds make text easier to select, move and edit without invisible boxes overlapping neighbouring content.

- Preserve the intended font size. Resize the box to fit the text, rather than shrinking text to fit a fixed box. If the content cannot fit on the slide at a readable size, shorten it or split the slide.
- Measure using the actual font, weight, size, line spacing, paragraph spacing, bullet indents and internal margins. Fit single-line boxes to the text width and height. For multiline text, choose the width for the intended wrapping, then fit the height to the wrapped content. Leave only padding and a small font-metric tolerance around the text.
- Put alignment and spacing in the surrounding layout. Do not use oversized text boxes, empty paragraphs or arbitrary minimum heights to position text. Cards and group frames may be larger for visual grouping; their text boxes still fit their own content.
- In HTML, measure the text-bearing element rather than its enclosing grid cell or card. In editable exports, write measured text-box dimensions and use resize-shape-to-fit-text when the format supports it. Do not rely on shrink-to-fit or on the receiving application to repair the dimensions.
- Refit after wording, font or wrapping changes. Inspect rendered text bounds against the box interior for clipping, overlap and excessive empty space. Repeat this check after a requested target-app import when that app is available, and report an untested import honestly.

### 7. Show the result

Show the user what was built. Report what the proof shows.

- List each output file path.
- Show the final slide list in chat.
- Share a preview when a browser tool is available. A screenshot of the first slide or the slide list is enough to prove the file renders.
- Name the text limit check result. State the max words on any slide and any splits you made.
- Name the title rule check. Confirm titles are present and subtitles are absent.
- Name the footer check. Confirm no footer element appears on any slide. Slide number is the only bottom element when needed.
- Name the box check. Confirm boxes have rounded corners and title and content sit in separate elements or text boxes.
- Name the text-box fit check. Confirm text boxes fit their content with appropriate padding at the intended font size, without clipping or oversized empty bounds.
- Check that the title has no background fill and that filled boxes are used only to group content.
- Confirm standard list bullets and the companion Markdown source. Report any copy or import behavior that was not tested.
- Name the references check. Confirm each slide has comments with sources.
- Give the paste steps when the user wants Google Slides or Keynote. Keep the steps short.
- Say what remains unproved. Missing images, unverified numbers, or untested rendering are gaps, not proof.

Check that the files exist, the visual deck renders, and both outputs match the approved draft. Report untested paste or import behavior as a limitation.

## Guardrails

- Draft first. No deck before explicit approval.
- Minimal text on every slide. Over 500 words means split.
- Titles allowed. Subtitles banned.
- Never use a footer. No bottom sentence, no source label, no attribution line. Slide number is the only bottom element.
- Rounded boxes. No chamfered corners.
- Plain slide canvas and unfilled title. Background fills only on content boxes that group items.
- Use standard native bullets, not custom bullet glyphs.
- Include a companion Markdown source by default.
- Keep title and body text separate. Fit every text box to its content and padding; preserve readable font sizes.
- References and comments on every slide. No claim without a source.
- Prefer copy-friendly output. Verify target-app paste behavior before claiming it works.
- Keep chat as the home for drafts unless the user asks for a file.
- Do not edit the installed pack or global config unless asked.
- Do not commit, push, open a PR, or deploy unless asked.

## Reply

Lead with the draft or the finished deck path. For a draft reply, show the draft itself and the approval question. For a finished reply, list the files, the slide list, the word count check, the title and references checks, and the paste steps when they apply.
