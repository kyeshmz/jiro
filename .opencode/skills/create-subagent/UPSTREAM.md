# Upstream source

Adapted from [`pstack/agents/poteto-agent.md`](https://github.com/cursor/plugins/blob/ccb5507cec1546dc88135c1139c811e6c59115ba/pstack/agents/poteto-agent.md) in `cursor/plugins` at `ccb5507cec1546dc88135c1139c811e6c59115ba`. The source was read at this immutable revision. The upstream MIT notice is preserved in [LICENSE](LICENSE).

**Take.** A reusable agent wraps its required skill and reads it before work. Its description tells the parent when to choose the role. New tasks use fresh children.

**Adapt.** `create-subagent` is a Jiro authoring workflow built around that wrapper pattern, not an upstream skill of the same name. It writes project-local OpenCode V2 `.opencode/agents/<id>.md` definitions. The worker and reviewer templates are new Jiro material. Required skills are checked rather than assumed; models inherit by default; global writes require an explicit request. Permissions and registration behavior follow the [V2 agents guide](https://opencode.ai/v2/docs/agents).

**Skip.** Poteto's persona, mandatory poteto-mode dependency, Cursor `name` / `is_background` fields, and automatic launch of a newly written definition. Jiro's workers are chefs. This checkout installs `agents/chef.md` through `.opencode/agents/chef.md` under the exact ID `chef`, and its worker loads `jiro` before work. Other generated roles still need host discovery before launch.

**Verification boundary.** Packaging checks do not prove live discovery of a new custom ID or runtime compliance with the generated instructions.
