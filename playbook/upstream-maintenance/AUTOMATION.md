# Automatic upstream skill updates

The [workflow](../../.github/workflows/upstream-skills.yml) checks registered sources daily at 08:23 UTC and can be run manually. It uses the single [upstream.json](../../upstream.json) catalog. Jiro's upstream engineering source is `kyeshmz/opencode-pstack`, not `cursor/plugins` directly. Playwright follows its two Microsoft repositories. React guidance follows `wholeearthrobotics/agent-skills`, and Effect guidance follows `anomalyco/opencode`. It creates at most one tested **draft update PR** per run. It never auto-merges, restores MCP configuration, or mirrors an entire upstream pack.

## Follow the OpenCode port

Jiro's engineering source paths are relative to the port repository, such as `skills/how`, not the historical `pstack/skills/how` path in Cursor's repository. Its commit hashes are distinct from Cursor's hashes. Historical Cursor links remain attribution, not active updater baselines.

Each Jiro entry tracked from this repository also declares `watchPaths` for matching `opencode/skills/<source-id>` overlays and the port's conversion and installation logic. These paths select additional review context, including files added after a historical baseline. They are not imported artifacts or target write permissions. The updater must adapt relevant native-host changes while preserving Jiro naming and writing, task-specific first-use verification, existing improvements, and authorization gates. It must not execute the port installer or copy its model settings. Runtime instructions use Jiro; real upstream identities and historical attribution stay intact.

The tracking migration preserves pending history with these verified snapshot mappings:

| Historical Cursor revision | Matching OpenCode port commit |
| --- | --- |
| `ccb5507cec1546dc88135c1139c811e6c59115ba` | `1215e2ffdc3068c0a89320c16d95a8ba7b7feb99` |
| `11713c683fe4add4fd403ea880580abbc9e0875f` | `85a98f9fa7e1185c95bef2914c783661adaa4fa8` |
| `1dcc2bacde73ddd284803b7af28164d0436198fc` | `84220454f9f2bb61e771c1862fea8d404ffc8ea4` |

Older selected files that match the earliest port snapshot byte for byte use that snapshot as the equivalent imported baseline. Six differing files were reviewed against that snapshot. Their local implementations were retained with explicit skip decisions in `provenance`; `importedRevision` stays null and `reviewedThrough` records the reviewed port commit. This does not claim a new port import or skip forward to current HEAD. The cleanup playbook's genuinely unknown baseline remains blocked.

No checkpoint is reset or rewritten by this migration. A deployed updater with checkpoints for the former policy may require an operator-reviewed policy reset. Do not reuse a Cursor checkpoint for the port repository or edit checkpoint hashes by hand.

## Activate it

Local changes alone do not activate a GitHub workflow. Publish the reviewed skill-sync changes in `kyeshmz/oc-port-agent` and the workflow/runner changes in Jiro's default branch first. Then configure these repository settings:

| Setting | Kind | Value |
| --- | --- | --- |
| `OC_PORT_AGENT_REF` | Actions variable | Full published commit SHA containing `--config`, explicit bootstrap baselines, and `allowSkillEdits`. Floating branches are rejected. |
| `OC_PORT_MODEL` | Actions variable | Operator-selected `provider/model#variant`, confirmed available to that provider. No model is guessed. |
| `OPENCODE_API_KEY` | Actions secret | Provider credential for the selected model. Never commit it or put it in a workflow input. |
| `OC_PORT_API_KEY_ENV` | Optional Actions variable | Provider environment name, default `OPENCODE_API_KEY`; examples include `OPENAI_API_KEY` or `ANTHROPIC_API_KEY`. |
| `OC_PORT_GITHUB_TOKEN` | Optional Actions secret | Narrow target-repository contents/PR token. Otherwise the workflow uses `github.token`. |

Enable GitHub Actions' permission to create pull requests when using the default token. A dedicated token can also let proposed PRs trigger other CI; the default Actions token normally does not. No secret values are needed in source files.

Start with a manual **check** run. It fetches public upstream refs and compares pinned source ranges, without a model call or publication. Then run **sync** to exercise adaptation and draft-PR creation. Successful local tests do not prove this hosted run until it has actually been executed.

## What happens on each run

1. Validate the import inventory. Compile one closed policy per import into ignored `.oc-port/policies/` files, with its source repository, selected paths, mappings, preservation rules, exact skill IDs, and trusted checks.
2. Check each source against its reviewed/imported pin, or its merged, independently namespaced updater checkpoint. A reviewed-only pin is a valid comparison baseline, not an assertion that the source was imported. Validate immutable evidence links for both pins. Missing baselines and mismatched per-source baselines are reported as blocked, never silently reset to HEAD. The cleanup playbook's existing unknown baseline remains blocked.
3. If no selected skill paths changed, stop without calling a model or creating a checkpoint-only PR.
4. If an `oc-port/` PR is already open, wait for its review instead of opening another. Otherwise adapt one pending import in an isolated worktree through the restricted updater.
5. Enforce closed file scope, explicit-invocation metadata, no symlinks or nested skill registration, and unchanged unrelated registry metadata. Check new source pins against the actual fetched head and immutable provenance links. Run the package and maintenance tests, Bash syntax, and whitespace checks.
6. Only after checks pass, the host writes a new checkpoint in the proposal branch and opens a draft PR. It takes effect when a human reviews and merges the proposal. Failed checks preserve the proposal for inspection and never advance the caller's checkpoint.

Skill bodies are adapted as inert reference data, not loaded as instructions for the updater. Only exact named `skills/<id>/` targets are approved in this configuration-directory checkout. Root-level `agents/`, `commands/`, and OpenCode/MCP configuration, workflow files, trusted verification scripts/tests, and updater state remain protected, as do legacy `.opencode/` paths. The explicit policy opt-in is supported by `oc-port-agent`; it is not a wrapper bypass of that tool's host gates.

Each policy names only `upstream.json` as `reviewMetadataPaths`. The proposal gate allows only the selected entry's provenance and source pins to change. A skip cannot alter checksums or skill implementation. An applied bundle change may also update that entry's checksum map. Editing another entry or its ownership, repository, source paths, `watchPaths`, or preservation rules is rejected even though the catalog is shared. An applied result must change a nonmetadata target; changing only source pins cannot masquerade as an adaptation.

The source record distinguishes applied revisions from reviewed-but-skipped revisions. Prior immutable links stay as historical evidence. Source pins, generated policies, and test receipts are not a claim of complete runtime parity; the PR review must assess behavioral changes and untested surfaces.

## Local use

Build the reviewed updater checkout first. Then, from Jiro:

```bash
python3 playbook/upstream-maintenance/scripts/sync.py check --tool /absolute/path/to/oc-port-agent/dist/src/cli.js
python3 playbook/upstream-maintenance/scripts/sync.py check --tool /absolute/path/to/oc-port-agent/dist/src/cli.js --import playwright-cli
```

`sync` invokes the selected model and creates a committed local proposal. It requires a clean target, an operator-selected `OC_PORT_MODEL`, and provider credentials. `--publish --repository <owner/repo> --base <branch>` explicitly adds push and draft-PR publication. Do not use it against an unreviewed branch, silently reset policy checkpoints, or discard unrelated work to make the target clean.

Generated policies are ignored. `.oc-port/checkpoints/` and `.oc-port/reports/` are deliberately **not** ignored: they are committed only in successful proposals and must survive merging. Each policy path has its own checkpoint, so a Microsoft update cannot advance an unrelated Jiro import's history.
