---
name: teach
description: Teach a change or subsystem in plain language so the reader understands it. Run how and why, preserve evidence and confidence, and build the explanation diagram by diagram at the reader's pace. Use for @teach, /teach, teach me this, or help me really understand this change.
license: MIT
metadata:
  opencode/autoinvoke: false
---

# Teach

Explain what a thing is, how it works, and why it is built that way in one plain account at the person's pace. The goal is understanding, not changes to the repository.

Teach builds on `how` and `why`. These are real skill invocations that do their own investigation. Load `unslop` through OpenCode's `skill` tool before drafting the explanation. Resolve any supporting references from each loaded skill's reported base directory. All three companions are bundled with Jiro. If one cannot load, report the missing installation rather than pretending it ran.

## Gather the explanation

1. Decide the few things the reader should understand from why they are asking and what they already know in the conversation. Do not quiz them to extract this context. Skip what they plainly know and put the depth where their question is.
2. Read the relevant code or diff to get oriented. For a subsystem, run both `how` and `why`. Use OpenCode's `subagent` tool with `agent: general` for two independent read-only children. Tell one to load `how` through the `skill` tool and follow it for the scoped runtime question. Tell the other to load `why` and follow it for the scoped rationale question. Include the original request, working directory, relevant paths, and a prohibition on edits, commits, and external writes in both prompts. Do not pass unsupported `readonly` or `subagent_type` arguments. Inherit the model unless the user and host authorize a confirmed override. Each companion owns its own investigation and agent procedures.
3. Run the independent children concurrently when supported. Use background execution only while the parent has independent work, then wait for completion notifications rather than polling. For a small change, one companion may suffice when the other question is already answered by supplied evidence. Say what was omitted and why. Keep `why` narrow through an explicitly scoped question and permitted sources. Let it record skipped categories under its own contract; do not silently discard its coverage gaps.
4. Combine the findings into one explanation. Reword freely for teaching, but keep `why`'s confidence language intact. Its hedges are findings, not style. Preserve citations, competing explanations, and material unknowns. Do not turn an inference into a fact or claim an investigation that failed or never ran.

## Teach at the reader's pace

Start with a plain definition. Name the thing and say what it is in general terms, then tie it to the case in front of you. Give the smallest complete answer first, usually a sentence or two. Build the mechanism, deeper reasons, and edge cases in later layers when the reader asks. A list of functions and constants is reference material, not teaching.

Keep it a conversation. No quizzes, requests to repeat it back, announced pauses, or claims that the next part is hard or important. Do not print stock labels such as "the key insight", "at its core", or "TL;DR". When you would pause, stop and let the reader respond. In a one-shot request, give a complete explanation without a wall of text.

Show the code, diff, or observed debugger result when it makes the mechanism clearer. Build the picture up diagram by diagram. For three or more moving parts, draw a short series in which each diagram redraws the last and adds a single part or edge. Do not save one all-at-once diagram for the end. For an A to B to C flow, show A to B, redraw with C, then redraw with the return edge or next piece as the explanation develops.

Use Mermaid or plain-text diagrams for flows and structures. For spatial ideas such as layout, overlap, or scroll position, use a whiteboard-style image when an authorized image tool is available. Keep labels short and apply the same incremental build-up. If that capability is unavailable or would need unauthorized billing, use a plain-text spatial sketch and state the limitation. Do not install a renderer or claim an image was generated. One simple point needs no diagram.

Write through `unslop` in plain spoken English. Cut filler, not evidence-backed uncertainty. State the concrete mechanism instead of a metaphor or a preview. Use sentence case, keep one name per concept, and split dense sentences. The explanation should be tight, not compressed into fragments.

Keep the task read-only. Do not edit files, commit, push, install tools, or make external writes to illustrate an answer without separate authorization.

**Reply.** Give the explanation itself, never a report about what you did or delivered. Lead with the main point, then teach what it is, how it works, and why. Keep evidence and uncertainty beside the claims they support.
