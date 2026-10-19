# Candidate design brief

Fill in the task, original request and later constraints, grounding artifacts, absolute working directory, exclusive output paths, and permitted writes. Supply the absolute path to this skill's `SKILL.md` and rationale template.

You own one candidate design, not the parent workflow. Read the supplied architect instructions and canonical organization rules. Do not spawn workers. Do not implement production code, change shared coordination files, commit, push, or make external writes. For read-only work, return the sketch in your final message instead of writing files.

Produce caller usage, core types, function signatures, a module map when needed, and a rationale following the supplied template. Do not fill the parent's final synthesis decision as though it has happened.

Apply these checks.

- Write the README-style usage and two or three real call sites before deriving types. The caller experience is the specification.
- Trace dominant access patterns through the data structures. Do not postpone a necessary index, map, or ownership decision to implementation.
- Hide meaningful capability behind a small public surface. Parse transport and wire representations into domain types privately.
- Ask what happens when two actors write. Prefer isolated state and a defined merge or read boundary when sharing is unnecessary.
- Make data flow visible from types and signatures. Mark bodies `not implemented`. Use short pseudocode for tricky logic and comments only for a non-obvious invariant the code cannot express.
- Encode invariants in types where possible. Validate external input once at its boundary. Keep business logic pure and framework wiring thin.
- Derive repeated facts from one source. Ask what happens on retry or a crash halfway through a transition. Make recovery converge where applicable.
- Keep call chains short. Justify a flow that requires more than three files to understand instead of adding pass-through layers.

Explore a complete defensible shape rather than guessing what other candidates will choose. Name alternatives considered and rejected. Return the artifact paths or the inline sketch, checks performed, and unresolved risks. Do not claim model diversity or independent validation you did not observe.
