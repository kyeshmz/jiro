# Upstream sources

Adapted from `opencode-pstack`'s `no-comments` tool and Comment Sicko reviewer. The inspected checkout records upstream revision `ccb5507cec1546dc88135c1139c811e6c59115ba`. Both files were checked against the immutable `cursor/plugins` sources:

- [`pstack/skills/no-comments/SKILL.md`](https://raw.githubusercontent.com/cursor/plugins/ccb5507cec1546dc88135c1139c811e6c59115ba/pstack/skills/no-comments/SKILL.md).
- [`pstack/agents/comment-sicko.md`](https://raw.githubusercontent.com/cursor/plugins/ccb5507cec1546dc88135c1139c811e6c59115ba/pstack/agents/comment-sicko.md).

The installed OpenCode copy was also inspected for tool-name conversion. Its machine-specific paths and global model configuration are not copied. The upstream MIT notice is preserved in [LICENSE](LICENSE).

## Selection

- **Take.** Fresh adversarial comment review, the five protected exception classes, scoped `MUST KILL` flags, parent acceptance, one rejected-report retry, root-cause fixes, approved constraint encodings, and explicit open work.
- **Adapt.** Use OpenCode's `subagent` tool with supported arguments. Use the advertised `comment-sicko` agent or a built-in `general` child with the full bundled reviewer rules. The reviewer is read-only; the parent owns accepted edits and verifies their effects. Preserve inherited models, explicit invocation, target-repository execution, and loaded-base resource resolution. Jiro calls this tool trimming the garnish.
- **Safety adaptation.** Hold uncertain protected exceptions and request evidence rather than deleting on doubt. Never discard user changes or broadly revert a checkout to retry. A correctness suppression is removed with a verified root-cause fix, not in a way that leaves broken code. Read-only requests produce proposed deletions only.
- **Skip.** Cursor Task fields, mandatory `architect` and `principle-*` dependencies, unconditional deletion of ambiguous exceptions, hardcoded global paths/model policy, and installation of a custom reviewer agent. An available `architect` is optional; otherwise `how` and a scoped design sketch establish the target shape.

`references/reviewer-prompt.md` is the adapted reviewer body. It is a bundled prompt, not an automatically registered OpenCode agent. Static packaging checks do not establish full upstream parity or live reviewer behavior.

This checkout also preserves the older installed OpenCode port's conditional integration with host-authorized pstack role settings. Ordinary Jiro review still inherits the active model. A pstack caller uses only its required role configuration and confirmed model IDs without changing user settings.

**Read-only smoke test.** The adapted rules were passed to the advertised `comment-sicko` agent for one owned JavaScript fixture. It proposed removing two narration comments, protected the SPDX license header and public API doc comment, reported no structural flags, and left the file unchanged. This covers that small classification case only. The `general` fallback, actual deletion/root-cause fixes, retry behavior, and constraint-encoding flow remain untested live.
