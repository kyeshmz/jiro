# Upstream source

Copied from [WholeEarth Robotics' composition-patterns skill](https://github.com/wholeearthrobotics/agent-skills/tree/abd39e05df96b6ce3524050045b9131eb2fea0b3/skills/composition-patterns).

The source revision is `abd39e05df96b6ce3524050045b9131eb2fea0b3`. All 14 source files are retained, including the compiled `AGENTS.md`, README, metadata, rule templates, and 8 individual rules.

The only change to a source file is normalizing `name: vercel-composition-patterns` to `name: composition-patterns` in `SKILL.md`. Its body, description, author metadata, and `license: MIT` declaration are unchanged. The source snapshot does not include a standalone license file, so no copyright notice has been invented.

`import-manifest.json` records the pinned repository, source directory, and SHA-256 of every copied file after that name normalization. Jiro adds only that manifest and this provenance record.

OpenCode loads `composition-patterns` from this directory. Resolve `rules/` and `AGENTS.md` from the loaded skill's base directory. The original React 19-only gate is retained. Do not apply that section to React 18 or earlier.
