# ksdft2effmass Graphify policy overlay

This repository-local policy applies when the Graphify skill in
`.agents/skills/graphify/` is used in `ksdft2effmass`. The validated local
Graphify version is `0.9.2`. This policy must not be silently overwritten by a
future Graphify update.

## Invocation and local executable

Graphify is manually invoked only when the current human message explicitly
requests Graphify. Ordinary topology, dependency, impact, navigation, and
next-task questions do not trigger it.

Use only the existing executable at `$HOME/.local/bin/graphify`, validated as
Graphify 0.9.2. `$HOME` avoids embedding a developer username but does not permit
executable discovery or fallback. Do not use a same-named global skill as a
fallback, install or upgrade the package, or emulate the CLI with inline Python.
If this exact location is unavailable or has a different version, report the
mismatch and stop.

## Authority limits

Graphify is optional. Its outputs are derived navigation aids and may be stale,
incomplete, or wrong. Graphify output is non-authoritative and cannot approve
architecture, establish scientific validity, record human decisions, supersede
accepted task records, or launch another task.

Every material scientific, numerical, architectural, or task-state conclusion
suggested by Graphify requires verification against authoritative repository
files before it is used or reported as project state.

## Safe operation

- Graph generation or regeneration must remain read-only with respect to
  production source, specifications, fixtures, tests, and documentation.
- Generated outputs belong under this repository's ignored `graphify-out/`
  directory; do not pass another corpus root to `update`.
- Launch every Graphify command with known semantic-backend keys removed,
  `GRAPHIFY_OUT=graphify-out`, `GRAPHIFY_QUERY_LOG_DISABLE=1`, and
  `GRAPHIFY_NO_TIPS=1`. This prevents inherited output redirection, keeps backend
  credentials out of the process, and disables Graphify 0.9.2's external query
  log.
- Do not rebuild or update a graph automatically after edits, commits, or session
  startup.
- Do not install, enable, or modify hooks, watchers, servers, or always-on
  integrations.
- Do not configure, store, request, detect, or rely on API keys; remove known
  backend-key variables from the Graphify process environment.
- Do not use Gemini, Google, OpenAI, Anthropic, another external semantic
  backend, or semantic-extraction subagents without explicit human approval.
- Do not transmit unpublished repository content externally without explicit
  human approval.
- Do not modify global pi, Codex, or Graphify configuration or global skills.

## Verification and intervention

For every material Graphify-derived claim, identify the claim, inspect the
authoritative source file, and report the verification path. If graph-derived
evidence conflicts with instructions, accepted records, source, tests,
specifications, or documentation, state the uncertainty and pause for human
intervention. Human intervention is also required before enabling external
semantic processing, installing hooks, committing generated graph artifacts, or
using Graphify output to settle scientific meaning or architecture.
