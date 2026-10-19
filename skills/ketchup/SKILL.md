---
name: ketchup
description: Catch the user up on changes in this chat since their previous message and list every decision waiting on them with enough context to decide. Use for @ketchup, /ketchup, or catch me up on what happened in this chat.
license: MIT
metadata:
  opencode/autoinvoke: false
---

# Ketchup

Summarize what changed after the last message the user wrote before invoking this skill. Notifications, tool output, and child reports do not count as user messages. Assume the user remembers that last message and nothing since.

Read `references/shared-rules.md`. Resolve resources from the loaded skill base. Use `bro` for plain language when available, not its restatement task. Say what changed for the user rather than narrating tools. Say the tests pass rather than CI is green. Omit hashes, paths, commands, counts, and build identifiers unless needed for a decision. Use names the user already knows.

## Gather

Keep this turn read-only. Do not change code, start an app or job, generate new screenshots by running the product, post messages, or publish artifacts. Use the active chat and already supplied evidence. Do not scan global history or unrelated sessions.

Collect the parent's work, child reports, and relevant messages since the boundary. Check the current state of known PRs, CI runs, and agents this chat touched through available read-only tools. Do not start a reviewer or resume a worker merely to check status. If current state cannot be checked, label it unknown or last observed. Recheck every number against its source and identify any corrected number.

An action item is a decision or step only the user can take. Include approvals, product choices, irreversible actions, and access blockers. Include unresolved items raised before the last message too. Work the agent can still do is not a user action item. Do not invent a decision to fill a section.

For each pending item, gather its real link when available, user-facing change, evidence for the recommendation, risk, prerequisites, and recommendation. Use unknown for a necessary fact that is missing. An unnecessary optional step is not a required action. If an optional irreversible step awaits approval, give it one plain line without a visual.

## Write

1. Open with one short sentence naming what waits on the user, or say that nothing does. If nothing happened and nothing waits, stop there.
2. Show existing screenshots and videos inline first when they explain a visible change. Follow with a small diagram only when it makes a relationship or choice easier to understand.
3. Give one short bullet per requested outcome. Say what changed and whether it is complete, still running, failed, or not checked. Name bugs found and fixed along the way. Every bullet must stand alone. Do not mark a user-blocked outcome complete or repeat facts reserved for the action items.
4. Add at most three short lines that materially change what the user knows or must do. Then name remaining agent-owned work in one line.
5. List every user-owned call with a recommendation and enough evidence to decide from the reply alone.

Keep the happened-since summary under 100 words, excluding visuals. Spend words on decisions rather than the story. Aim for about 30 words per simple item, but preserve the change, evidence, and risk. Never drop items, replace them with a count, or substitute a link for the facts needed to decide. The reply grows when the number of real decisions grows.

## Fit the decision

For one item, use one bullet with the call, recommendation, user benefit, evidence, and risk. Name it once.

For several items sharing a call, state the call and recommendation once. List each item separately, riskiest first, with its link and known name, benefit, evidence, and risk. Repeat an item-specific recommendation only when it differs. Include prerequisites and irreversible consequences in the recommendation. Explain waiting cost only when it is more than delay, such as a deadline or lost data.

For a choice between options, include every option actually weighed. State what each gains and costs and its current state when relevant. Those costs are the decision's risk. Do not add a redundant risk paragraph. If screenshots show the options, put each gain and cost under its screenshot. Name each relevant PR, issue, or agent with an observed number or link when available. Never invent one.

## Visuals

A screenshot, video, Mermaid diagram, or evidence-backed chart can explain a change. A Markdown table is not a visual. Do not require an unavailable visualization workflow.

Draw relationships, dependency chains, before-and-after mechanisms, or actual options. Do not draw a status list, action-item list, or disconnected boxes. Use at most six boxes with at most eight plain words each. Put a fact in one place instead of repeating it in text and diagrams.

Use only existing captures and observed facts. Never invent numbers or generate a fictional picture of a screen. If a visible change has no capture, mark its summary line No screenshot yet and describe what changed on screen. Link only artifacts that exist and are available in this chat.
