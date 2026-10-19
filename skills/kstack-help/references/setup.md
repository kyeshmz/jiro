# Set up the pack

Kstack supplies instructions for an existing OpenCode V2 installation. Jiro is the coordinating skill. The source checkout uses Bun, Bash, and Git. Installing it does not configure a provider, browser runtime, MCP server, or bot backend.

When installation is requested, inspect the source checkout's README and installer before executing them. The source repository is `https://github.com/kyeshmz/kstack.git`. A normal installation from a chosen checkout is:

```sh
bun install
./install.sh
./install.sh --check
```

Run those commands in that source checkout, not in the project being verified or an installed skill directory. Do not run them from a help-only request. The installer writes the user's global OpenCode skill, command, agent, and catalog copies. Global installation requires authorization. It preserves unrelated settings and archives replaced managed content.

In the repository being worked on, use `@jiro <task>` or the installed `/jiro` command. `@jiro initialize this repository` requests repo-local verification setup. The first editable task also creates and proves a relevant verification skill when none exists, unless explicitly opted out. An unrelated verification skill does not cover another surface. Existing harnesses are reused.

Use `@kstack-help` to choose a tool without starting work. Use `@setup-kstack` only to propose or change requested role models and budget. Missing role choices inherit the active model. A plain role file is not an automatic loader, and real model overrides still require authorization and host confirmation.

If an exact skill ID is unavailable, inspect the installed source and host permissions. Report a missing installation rather than silently switching packs. A new session may be needed to discover newly installed definitions. Do not promise live discovery until it has been observed.
