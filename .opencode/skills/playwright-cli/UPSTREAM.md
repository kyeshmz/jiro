# Playwright CLI skill provenance

This directory imports the official skill documentation from **Microsoft's
`microsoft/playwright-cli`**, pinned to immutable commit
`b85c7a736bb473bf55b584e54a09ffa698d6d871`. It is a Jiro/OpenCode V2 adaptation,
not an upstream release or an installation of the CLI package.

## Exact sources

- [Pinned skill directory](https://github.com/microsoft/playwright-cli/tree/b85c7a736bb473bf55b584e54a09ffa698d6d871/skills/playwright-cli)
- [Pinned reference directory](https://github.com/microsoft/playwright-cli/tree/b85c7a736bb473bf55b584e54a09ffa698d6d871/skills/playwright-cli/references)
- [Pinned README.md](https://github.com/microsoft/playwright-cli/blob/b85c7a736bb473bf55b584e54a09ffa698d6d871/README.md), read for CLI/package identity, local installation, named sessions, and output configuration (`outputDir`). It is not copied here.
- [Pinned upstream LICENSE](https://github.com/microsoft/playwright-cli/blob/b85c7a736bb473bf55b584e54a09ffa698d6d871/LICENSE), reproduced in full in [LICENSE](LICENSE), including Microsoft's copyright notice.
- [Pinned recursive Git tree](https://api.github.com/repos/microsoft/playwright-cli/git/trees/b85c7a736bb473bf55b584e54a09ffa698d6d871?recursive=1), checked for coverage and NOTICE files.

| Local file | Immutable upstream source | Treatment |
| --- | --- | --- |
| [SKILL.md](SKILL.md) | [skills/playwright-cli/SKILL.md](https://github.com/microsoft/playwright-cli/blob/b85c7a736bb473bf55b584e54a09ffa698d6d871/skills/playwright-cli/SKILL.md) | Adapted; prominent modified-file notice in the file. |
| [references/command-catalog.md](references/command-catalog.md) | [Commands section of SKILL.md](https://github.com/microsoft/playwright-cli/blob/b85c7a736bb473bf55b584e54a09ffa698d6d871/skills/playwright-cli/SKILL.md) | Extracted and adapted with a modified-file notice for progressive loading. |
| [references/element-attributes.md](references/element-attributes.md) | [element-attributes.md](https://github.com/microsoft/playwright-cli/blob/b85c7a736bb473bf55b584e54a09ffa698d6d871/skills/playwright-cli/references/element-attributes.md) | Taken unchanged. |
| [references/playwright-tests.md](references/playwright-tests.md) | [playwright-tests.md](https://github.com/microsoft/playwright-cli/blob/b85c7a736bb473bf55b584e54a09ffa698d6d871/skills/playwright-cli/references/playwright-tests.md) | Taken unchanged. |
| [references/pr-attachments.md](references/pr-attachments.md) | [pr-attachments.md](https://github.com/microsoft/playwright-cli/blob/b85c7a736bb473bf55b584e54a09ffa698d6d871/skills/playwright-cli/references/pr-attachments.md) | Taken unchanged. |
| [references/request-mocking.md](references/request-mocking.md) | [request-mocking.md](https://github.com/microsoft/playwright-cli/blob/b85c7a736bb473bf55b584e54a09ffa698d6d871/skills/playwright-cli/references/request-mocking.md) | Taken unchanged. |
| [references/running-code.md](references/running-code.md) | [running-code.md](https://github.com/microsoft/playwright-cli/blob/b85c7a736bb473bf55b584e54a09ffa698d6d871/skills/playwright-cli/references/running-code.md) | Taken unchanged. |
| [references/session-management.md](references/session-management.md) | [session-management.md](https://github.com/microsoft/playwright-cli/blob/b85c7a736bb473bf55b584e54a09ffa698d6d871/skills/playwright-cli/references/session-management.md) | Taken unchanged. |
| [references/storage-state.md](references/storage-state.md) | [storage-state.md](https://github.com/microsoft/playwright-cli/blob/b85c7a736bb473bf55b584e54a09ffa698d6d871/skills/playwright-cli/references/storage-state.md) | Taken unchanged. |
| [references/test-generation.md](references/test-generation.md) | [test-generation.md](https://github.com/microsoft/playwright-cli/blob/b85c7a736bb473bf55b584e54a09ffa698d6d871/skills/playwright-cli/references/test-generation.md) | Taken unchanged. |
| [references/tracing.md](references/tracing.md) | [tracing.md](https://github.com/microsoft/playwright-cli/blob/b85c7a736bb473bf55b584e54a09ffa698d6d871/skills/playwright-cli/references/tracing.md) | Taken unchanged. |
| [references/video-recording.md](references/video-recording.md) | [video-recording.md](https://github.com/microsoft/playwright-cli/blob/b85c7a736bb473bf55b584e54a09ffa698d6d871/skills/playwright-cli/references/video-recording.md) | Taken unchanged. |

## Take / adapt / skip

**Take:** the official command catalog, examples, task/reference structure, and
all ten reference files. References remain unchanged upstream material, not
independent execution authority. The full Apache License 2.0 is included locally;
license text and attribution are retained (LICENSE line endings are normalized
from CRLF to LF). The pinned recursive tree was complete (`truncated: false`)
and contained **no NOTICE-named files**, so there is no upstream NOTICE to copy.

**Adapt:** `SKILL.md` keeps `name: playwright-cli`, adds a scoped description,
`license: Apache-2.0`, and `metadata.opencode/autoinvoke: false`, and removes
`allowed-tools`. That field was a host-specific tool allowlist, not a permission
grant. The new OpenCode section precedes the workflow and explains loaded-base
reference resolution, target-repository execution, local-help feature checks,
unique explicit named sessions on every browser command, isolated/private
artifacts, owned cleanup, profile/attachment consent, secret handling, fresh
snapshot refs, untrusted page/WebMCP content, real-UI verification, scoped
side effects, and preservation of expected test outcomes. Session, installation,
WebMCP, annotation, and PR-attachment prose is adjusted to match those rules.

The command catalog is extracted to a supporting reference so the entry skill
stays below 500 lines. The ten original reference files remain unchanged; the
additional catalog is derived from the same pinned upstream SKILL.md.

**Skip as operational directions:** unattended global/package/browser installs,
`npm init` scaffolding, skill installation, shared/default sessions, global
cleanup or unsolicited data deletion, automatic persistent-profile/CDP/extension
use, page-tool shortcuts for UI verification, automatic PR/issue writes or
uploads, unrequested consequential actions, and test healing that weakens
expectations or silently skips failures. Unchanged examples in the skill and
references must be translated into authorized, locally supported, isolated
commands; their existence is not permission to execute them. No upstream scripts,
binaries, installers, or package configuration are imported or executed.

## Documentation pin versus package version

The commit above identifies **documentation source only**. It is not a version
constraint for `@playwright/cli`, `playwright`, `@playwright/test`, browsers, or
`gh`. Upstream `@latest`, `gh` 2.99+, `--debug=cli`, WebMCP, recording, emulation,
and configuration examples describe that source snapshot; they do not prove
availability or compatibility in a target repository. Read the installed
command's `--help` (and relevant subcommand help) before use. Do not install,
upgrade, or initialize anything solely to make these examples work.

## Verification and limitations

The import is statically checked for frontmatter, relative documentation links,
all eleven upstream skill files, unchanged reference content, full license text,
and the pinned tree's NOTICE coverage. All source was read as inert reference
material. **Live CLI behavior is untested:** no browser commands, CLI help/version
commands, package installs, browser downloads, test suites, session attachments,
recordings, or publishing commands were run for this import. OpenCode runtime
loading and the behavior of installed CLI flags/output isolation also remain
unverified. A future authorized browser task must perform its own local checks.
