# Prompts worth copying

Replace illustrative paths, IDs, fixtures, and checks with real ones. These are prompt examples, not executable commands or proof that a tool is installed. Use `@<skill-id>` for skills. `/jiro` works when its bundled wrapper is installed.

## Understand

- `@jiro read the supplied thread. Restate the underlying problem in plain English. Keep this read-only.`
- `@in-your-own-words restate the goal and constraints in this request before starting.`
- `@sharpen improve this brief around the user's outcome. Do not implement it.`
- `@jiro investigate why <symptom> occurs. Give the evidence, known facts, and competing hypotheses. Do not change code.`
- `Use @how to explain <subsystem>. Use @why to investigate the recent regression.`
- `@recall my work on <topic> last week using these supplied exports. Then read <issue>. Stay within this workspace.`
- `@teach explain why this implementation is better than <alternative>. Name the tradeoffs.`
- `@jiro take over this branch using the supplied handoff. Read the decision log and current diff. Continue without redoing proved work.`

## Build

- `@jiro users get duplicate writes after a retry. Reproduce it first. Fix the root cause and verify the original case.`
- `@jiro reproduce this through @verify-<app>. If it also fails on the base branch, fix it and show before-and-after evidence.`
- `@jiro reproduce <bug>. If a cheap reliable test exists, use @tdd. Fix it and rerun the original reproduction.`
- `@jiro add <behavior>. Keep <current output> byte-identical. Verify both paths.`
- `@jiro move <code> into one module without changing behavior. Capture the current output and prove it is unchanged.`
- `@jiro <operation> takes <time> on <fixture>. Profile the cause. Show comparable before-and-after runs and correctness checks.`

On explicit repository initialization or the first editable task, Jiro creates and proves task-specific verification by default. Initialization without another task uses the primary documented surface. Existing relevant skills are reused. Existing harnesses are wrapped. To opt out for the task, say "skip verification skill". Do not treat the opt-out as proof of behavior.

## Design and plan

- `@jiro prototype distinct options for <feature>. Keep their state isolated. Capture comparable screenshots for review.`
- `@jiro design <feature> with @architect. Answer empirical questions with prototypes. Stop for my review before implementation.`
- `@jiro draft a tutorial showing how a caller uses <package>. Use @teach to explain the tradeoff against the current API. Do not implement yet.`
- `@arena give a second opinion on this approach within the stated read-only scope.`
- `@jiro turn this settled design into small verifiable units. Each unit needs its own check. The plan is the deliverable.`
- `@jiro plan the migration from <library> to <target>. Preserve the current behavior, including known bugs, unless the plan explicitly calls out an approved change.`

## Review and authorized shipping

- `@interrogate review this branch skeptically. Do not change files. Report real bugs or behavioral regressions and read prior dismissals.`
- `@swarm check each package under <dir> against its existing check command. Use one isolated reader per package. Return one report.`
- `@jiro prepare the requested PR from the verified local changes. Follow repository gates and put evidence in the description. Do not merge.`
- `@jiro check PR <number> for outstanding reviews and CI failures. Status only. Do not push or change files.`
- `@jiro address substantiated findings on PR <number>. Keep unrelated work intact. Push only if that action is explicitly authorized in this request.`
- `@jiro merge the named verified PR after its required checks and repository gates pass. Stop if the head changes or a blocker remains.`

The last example is an explicit merge request, not a default workflow step. Commit, push, PR, merge, deployment, billing, deletion, and global installation remain separate authorization decisions.

## Away and back

- `@jiro I am stepping away. Complete <goal> in a fresh worktree off <base>. Done means <checks>. Keep a local decision log. Do not commit or publish. If blocked, preserve the work and write the exact blocker.`
- `@show-me-your-work catch me up on this supplied run and decision log. Include everything that still needs my decision.`
- `@jiro plan this independent queue in dependency order. Name one owner and one proof per item. Do not start or publish until I approve the plan.`
- `@jiro pause safely. Stop only processes this run owns. Preserve the uncommitted work and write a handoff with exact paths and remaining checks.`
- `@reflect propose lessons from this session that would change a future decision. Wait for approval before editing skills.`
- `@bro` restates the assistant's last reply in plain language.

A local instruction pack does not provide a background wake service. Do not promise work continues after the host session ends. A long run still needs an observable stopping condition and a working verification path.
