---
name: graphify
description: "Run the already-installed local Graphify CLI only when the human explicitly requests Graphify; never auto-install, auto-trigger, use a remote backend, or treat graph output as authority."
---

# Graphify (local, explicit use only)

Use Graphify only when the current human message explicitly asks to use or run
Graphify. Do not infer Graphify use from an ordinary topology, dependency,
impact, navigation, or next-task question.

Read and obey `references/ksdft2effmass-policy.md` before running a command. The
repository policy overrides upstream Graphify behavior and older integration
records.

## Local executable

Use the existing local installation directly:

```bash
GRAPHIFY_BIN="$HOME/.local/bin/graphify"
```

Before use, verify it without installing, upgrading, or searching for a
replacement:

```bash
test -x "$GRAPHIFY_BIN" && "$GRAPHIFY_BIN" --version
```

The expected validated version is exactly `graphify 0.9.2`. If the executable is
absent or reports another version, stop and report the mismatch. `$HOME` makes
the checked-in contract independent of a developer username while still naming
one fixed installation location; it is not executable discovery. Do not invoke `pip`,
`pipx`, `uv tool install`, `graphify install`, a global skill, an inline Python
fallback, or another Graphify executable.

## Allowed default operations

Only the following local operations are allowed after an explicit Graphify
request:

```bash
env -u GEMINI_API_KEY -u GOOGLE_API_KEY -u MOONSHOT_API_KEY -u DEEPSEEK_API_KEY GRAPHIFY_OUT=graphify-out GRAPHIFY_QUERY_LOG_DISABLE=1 GRAPHIFY_NO_TIPS=1 "$GRAPHIFY_BIN" query "<question>" --graph graphify-out/graph.json
env -u GEMINI_API_KEY -u GOOGLE_API_KEY -u MOONSHOT_API_KEY -u DEEPSEEK_API_KEY GRAPHIFY_OUT=graphify-out GRAPHIFY_QUERY_LOG_DISABLE=1 GRAPHIFY_NO_TIPS=1 "$GRAPHIFY_BIN" path "<node-a>" "<node-b>" --graph graphify-out/graph.json
env -u GEMINI_API_KEY -u GOOGLE_API_KEY -u MOONSHOT_API_KEY -u DEEPSEEK_API_KEY GRAPHIFY_OUT=graphify-out GRAPHIFY_QUERY_LOG_DISABLE=1 GRAPHIFY_NO_TIPS=1 "$GRAPHIFY_BIN" explain "<node>" --graph graphify-out/graph.json
env -u GEMINI_API_KEY -u GOOGLE_API_KEY -u MOONSHOT_API_KEY -u DEEPSEEK_API_KEY GRAPHIFY_OUT=graphify-out GRAPHIFY_QUERY_LOG_DISABLE=1 GRAPHIFY_NO_TIPS=1 "$GRAPHIFY_BIN" affected "<node>" --graph graphify-out/graph.json
env -u GEMINI_API_KEY -u GOOGLE_API_KEY -u MOONSHOT_API_KEY -u DEEPSEEK_API_KEY GRAPHIFY_OUT=graphify-out GRAPHIFY_QUERY_LOG_DISABLE=1 GRAPHIFY_NO_TIPS=1 "$GRAPHIFY_BIN" update "$PWD" [--force]
env -u GEMINI_API_KEY -u GOOGLE_API_KEY -u MOONSHOT_API_KEY -u DEEPSEEK_API_KEY GRAPHIFY_OUT=graphify-out GRAPHIFY_QUERY_LOG_DISABLE=1 GRAPHIFY_NO_TIPS=1 "$GRAPHIFY_BIN" diagnose multigraph --graph graphify-out/graph.json
```

Every allowed command uses a sanitized environment: known semantic-backend keys
are removed, `GRAPHIFY_OUT=graphify-out` prevents an inherited absolute output
override, query logging is disabled, and backend tips are suppressed. Preserve
that complete prefix.

Run `update` only from the repository root after confirming that `$PWD` is that
root and `graphify-out/` is ignored there. It performs local structural code
extraction and may write only under that repository's `graphify-out/`. Do not
pass another path or run it automatically after source changes. Use `--force`
only when the explicit request permits replacing a graph with a smaller rebuild.

For queries, require an existing readable `graphify-out/graph.json`.
`GRAPHIFY_QUERY_LOG_DISABLE=1` is mandatory because Graphify 0.9.2 otherwise
appends query metadata outside the repository. Use the CLI result as advisory
navigation evidence and verify every material conclusion against authoritative
repository files. Do not save query results, reflect lessons, create vocabulary
files, or otherwise mutate graph state during a read-only query.

## Not automatic and not authorized by this skill

Do not automatically:

- invoke Graphify for broad repository questions or next-task selection;
- install, upgrade, discover, or switch Graphify executables;
- rebuild or update the graph after edits or commits;
- run a watcher, server, MCP service, hook, or always-on integration;
- detect and use API keys or select a semantic backend;
- dispatch semantic-extraction subagents;
- clone, fetch, push, ingest URLs, or transmit repository content;
- generate exports outside `graphify-out/`;
- modify production, scientific, test, fixture, specification, or documentation
  files.

Remote semantic processing, external transmission, hooks, servers, dependency
changes, and committed generated artifacts remain protected and require a new,
explicit human authorization. Older integration records do not authorize those
operations.

## Reporting

Report:

- the exact local command run;
- whether it succeeded;
- generated paths or the existing graph queried;
- Graphify warnings, including oversized visualization or graph-integrity
  warnings;
- authoritative files used to verify any material conclusion;
- limitations caused by stale, structural-only, incomplete, or missing graph
  content.

Graphify output cannot approve architecture, establish scientific validity,
record a human decision, launch work, or supersede repository authority.
