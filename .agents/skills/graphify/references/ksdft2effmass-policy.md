# ksdft2effmass Graphify policy overlay

This repository-local policy overlay applies when the Graphify skill in
`.agents/skills/graphify/` is used in `ksdft2effmass`. The upstream Graphify
skill provenance and version (`0.9.2`) are preserved; this file is a versioned
project policy overlay that must not be silently overwritten by a future
Graphify update.

## Discovery and precedence

In the validated project environment, both Codex and pi discover
repository-local skills under `.agents/skills/`. pi additionally discovers
pi-specific skills under `.pi/skills/`. A project skill may shadow a same-named
global pi skill. The repository-local Graphify skill intentionally takes
precedence over the global pi Graphify fallback because it is versioned with the
repository and subject to repository policy.

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
- Generated outputs belong under the ignored `graphify-out/` directory.
- Do not install, enable, or modify hooks.
- Do not configure, store, request, or rely on API keys.
- Do not use Gemini, Google, OpenAI, Anthropic, or another external semantic
  backend without explicit human approval.
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
