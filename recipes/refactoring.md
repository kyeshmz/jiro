# Refactoring

Change the structure without changing behavior. A bug fix or new feature belongs in a separate, explicitly scoped change.

1. **Capture the contract.** Read the affected subsystem and its callers. Use `@how` when needed. Before moving code, write or run a characterization test, snapshot, or equivalence harness that captures current behavior. Type checking and lint alone do not establish equivalence.
2. **Name the missing structure.** Apply `@code-organization`. Identify the domain model, ownership, or boundary the code needs. Keep boring code when it is already clear and local. The reshape should remove repeated rules, invalid states, or unnecessary indirection.
3. **Choose the target shape.** Sketch the module layout, interfaces, import direction, and state owners. Compare distinct shapes for non-trivial changes. State which decisions each public interface hides.
4. **Subtract before adding.** Remove confirmed dead code, redundant validation, orphan references, and wrappers that do not earn their cost. Stay within the requested scope and preserve unfamiliar user work.
5. **Move in small verified steps.** Keep the behavior checks green after each move. Migrate all callers before removing an old API within the approved scope. Search strings, documentation, and configuration for usages that symbol renaming can miss. Do not leave parallel old and new paths just to avoid finishing the migration.
6. **Prove equivalence.** Compare old and new outputs, replay a recorded baseline, or run the affected behavior against the real artifact. Report the exact check and result. A successful build alone is not proof.
7. **Check reader load.** Apply `@minimize-reader-load`. Name the layers removed and the state scope reduced. If the reshape does not reduce reading work anywhere, do not keep it merely because it looks tidier.
8. **Hand off cleanly.** Summarize the change and remaining risks. Commit, push, or open a PR only when the user requests it or the active task already authorizes it. After an authorized push or merge, use `@worktree-cleanup` for finished temporary checkouts.

**Reply.** Report the structure changed, the behavior held fixed, the equivalence evidence, the reader-load improvement, and any candidates rejected. State explicitly if no new behavior shipped.
