# Upstream source

Adapted from the [OpenCode Effect skill](https://raw.githubusercontent.com/anomalyco/opencode/23e3493ab2efb6b8c00725cfd652b7f946af5343/.opencode/skills/effect/SKILL.md) in `anomalyco/opencode`.

The source revision on the `dev` branch is `23e3493ab2efb6b8c00725cfd652b7f946af5343`. The upstream directory contains only `SKILL.md`; there are no bundled references or scripts to import. The repository's MIT notice is preserved in [LICENSE](LICENSE).

The Effect v4 source-first workflow, generator and named-effect guidance, schema and typed-error guidance, explicit layers, and scoped live-test patterns are preserved. The port advertises the skill for Effect tasks, checks the target project's Effect version, keeps source checkouts in the task project, and reports unavailable source access instead of guessing APIs. It treats `packages/core/test/lib/effect.ts` and package-directory test execution as OpenCode-specific examples rather than assuming that layout in every project.

The Effect source repository is a runtime reference, not a vendored dependency of Jiro. Importing or installing this skill does not clone it. Skill discovery follows the [OpenCode V2 skills documentation](https://opencode.ai/v2/docs/skills).
