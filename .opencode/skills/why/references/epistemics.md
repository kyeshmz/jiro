# Epistemics

How to reason about confidence when evidence is historical, fragmentary, and sometimes contradictory. Tell the user without flattening it into false certainty. Code shows what it does, not why it exists. The why lives in commits, PRs, tickets, docs, and conversations. Those sources are incomplete, biased, and sometimes missing. Pretending otherwise produces confident-sounding guesses that mislead the user.

## Confidence Tiers

Every claim in the output must sit in one tier. The tier sets its section and its phrasing.

### 1. Direct

An explicit textual citation answers the question. An author actually wrote something that says why. Code doing X does not prove the author wanted X. Examples include a PR explaining a pagination bug, a ticket naming a customer's security requirement, a comment explaining an upstream API limit, a design doc choosing persistence across restarts, or a chat message explaining why an old approach was flaky.

Use confident, present-tense phrasing with an adjacent citation. State that the code exists because X only when the source says so.

### 2. Supported

Multiple pieces of indirect evidence converge on one conclusion. No single source states it explicitly, but the pattern across sources makes it likely. A performance PR title, a performance ticket label, and surrounding commits touching the same hot path may converge. Several tests exercising very large inputs or contemporaneous PRs naming the same incident may do the same.

Use confident but clearly derived phrasing. Cite each item. Say the evidence points strongly to X and name the specific pieces.

### 3. Inferred

A reasonable reading of the context that nothing explicitly supports. It is your interpretation, not a fact from the record. A production incident followed by a same-day fix may suggest a hotfix. A retry count matching a convention elsewhere may suggest consistency, but does not establish the original reason.

Hedge the claim and make the reasoning explicit. Given A and B, C seems likely because D.

### 4. Speculative

A plausible hypothesis on thin evidence, where other explanations fit equally well. It may be worth presenting because the user may know which is right. Mark it as a guess. A browser workaround or an SLA-derived threshold without contemporary evidence belongs here.

Say one possibility is X, but no direct evidence was found. Usually place it in Competing Hypotheses alongside other possibilities.

### 5. Unknown

You looked and could not find out. This is a valid outcome. Document it.

Name the sources, queries, date ranges, and records searched. Saying no rationale surfaced in six PRs, the ticket tracker, and threshold-matching strings is more useful than saying you could not find out.

## Phrasing Guide

Confidence words imply Direct or Supported evidence and need an immediately adjacent citation. Do not use them for inferences. Examples include because, the reason is, was designed to, fixes, addresses, solves, and the team decided. These phrases claim intent, achieved outcomes, or a group decision.

Hedges signal interpretation rather than report. Use appears to, seems to, likely, suggests, is consistent with, one reading is, plausibly, may have been, and the evidence points toward.

Avoid these words:

- Obviously. If it were obvious, the user would not be asking.
- Clearly. It often precedes a claim that is not clear.
- Of course. It has the same problem.
- Just, as in just X for performance. It is dismissive and often hides uncertainty.
- I think or I believe. You are synthesizing evidence, not giving a personal opinion. Use the evidence suggests instead.

## Avoid Rationalization

Code that makes sense today may have been written for reasons that no longer apply or were wrong at the time. Do not retrofit a clean rationale onto messy history. Do not assume the author did the right thing and work backward to justify it. Do not assume a consistent pattern was intentional when it might be copy-paste. Do not turn absence of evidence into evidence of absence.

## The Sycophancy Trap

Users often embed a hypothesis, such as assuming a design was chosen for performance. Do not simply confirm it. The guess is a prompt for investigation, not a conclusion to validate. Treat it as one candidate among others and check independently. If evidence supports it, say so with citations. If not, say so and present what the evidence does support.

## When Evidence Contradicts

Surface both sources with citations. Do not pick the one that fits a tidier narrative. A compliance ticket and a tech-debt PR framing may both be true, or one may be wrong. Preserve the distinction and let the user judge.

## When Evidence Is Missing

An honest unknown tells the user where the answer was not found. They can ask the original author, product owner, or team lead, or decide the question is not worth pursuing. Filling a gap with a confident guess can mislead their next decision. Name each gap concretely. Include the question, the sources searched, the queries, and whether the result was empty or only tangential.

## Before Finalizing

Check every claim in What We Found and What We Can Reasonably Infer. Each claim has a citation or moves to Inferred or Hypotheses. Its phrasing matches its tier. Do not treat code as evidence of its own intent. Include What We Don't Know. If there are no gaps, verify that the evidence was unusually complete rather than overlooking missing coverage.
