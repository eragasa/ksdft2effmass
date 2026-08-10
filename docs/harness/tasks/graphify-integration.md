<!-- Generated from SQLite control state; do not edit. -->
# Graphify Codex/pi Integration Task

[Task index](index.md) · [Previous](./evidence-branch-orchestration-profile.md) · [Next](./harness-simplification.agents.executable-tool-placement-contract.md)

## Status

`human_accepted`: corrected and accepted by human final decision on 2026-07-30.

## Objective

Manually integrate Graphify 0.9.2 as an optional, read-only repository-analysis tool for Codex and pi without running the Graphify project installer.

## Parent and prerequisites

None.

## Authority references

- .agents/skills/graphify
- .codex/hooks.json
- .pi/skills/choose-next-task/SKILL.md
- graphify-out
- harness/archive/task-control-v1/tasks/graphify-integration.md

## Authorized scope

- manually install Graphify 0.9.2 project skill under `.agents/skills/graphify/`;
- do not run `graphify install --project --platform codex`;
- do not create `.codex/hooks.json`;
- do not install any hooks;
- do not enable Gemini, OpenAI API, or any external semantic-processing backend;
- do not configure or store API keys;
- add a narrow Graphify policy to `AGENTS.md`;
- update `.pi/skills/choose-next-task/SKILL.md` so Graphify is optional supporting evidence;
- use `.agents/skills/graphify/` as the shared repository-local Graphify skill when fresh-session discovery demonstrates pi can discover it;
- add `graphify-out/` to `.gitignore`;
- treat generated Graphify artifacts as locally persistent but untracked;
- require separate human review before committing a curated `GRAPH_REPORT.md`;
- treat Graphify integration as prospective case-study episode `E01`;
- treat the completed operator-record refactor as retrospective pilot episode `E00`.

## Completion criteria

- Human response preserved verbatim: “resolve the skill collision”.
- Normalized decision: remove the overlapping automatic trigger between Graphify
and `recommend-next-task`. `recommend-next-task` exclusively owns ordinary
next-task questions. Graphify runs only when the current human message explicitly
requests Graphify; ordinary topology, dependency, impact, and navigation
questions remain normal repository-analysis requests and do not implicitly run
Graphify. This supersedes only the earlier E01 provisions that allowed Graphify
to be invoked automatically as optional next-task or broad-topology support.
Graphify remains available as an explicit, local, advisory tool under the
previous no-hook, no-external-processing, no-authority, and ignored-output
boundaries.
- The correction contracts the active entry runbook to the supported local CLI
profile. The copied upstream reference files remain retained compatibility
snapshots but are not active procedures and are not linked from the entry skill;
the repository policy and entry skill govern. The retained `.graphify_version`
identifies the compatible CLI/reference version, not verbatim provenance for the
project-specific entry skill. Read-only commands must disable Graphify 0.9.2
query logging; structural updates are restricted to this repository's ignored
`graphify-out/` path. During independent review, a `query --help` probe was
interpreted by Graphify 0.9.2 as a query and appended one entry to the external
user query log; it did not change repository files and is retained as disclosed
partial-effect evidence rather than silently deleted. No scientific, production,
external-execution, release, or successor-task scope is authorized.
- Shared Graphify project skill installed manually in `.agents/skills/graphify/`.
- Narrow Graphify policy recorded in `AGENTS.md`.
- shared Graphify discovery and optional use in `choose-next-task` documented.
- Generated-artifact retention policy recorded and `graphify-out/` ignored.
- Case-study protocol and E00/E01 records created.
- Sphinx developer documentation added.
- Narrow Graphify validation run completed or explicitly blocked.
- JSON, skill, Sphinx, discovery, no-hook, no-API, no-production-change, dry-run, and integration-review gates run.
- E01 record updated with implementation status, validation status, and human-final-acceptance state.

## Exclusions

- run `graphify install --project --platform codex`;
- create or modify `.codex/hooks.json`;
- install git hooks or Codex hooks;
- enable Gemini, OpenAI, Google, or another remote semantic-processing backend;
- configure or store API keys;
- modify global Codex, pi, or Graphify configuration;
- modify the global pi Graphify skill;
- install another Graphify version;
- transmit unpublished repository content externally;
- commit generated graph artifacts without separate human approval;
- modify production code, tests, scientific specifications, fixtures, scientific algorithms, or research results;
- treat Graphify output as scientific validation or architectural approval;
- create or launch the next scientific/software task.

## Historical source

`harness/archive/task-control-v1/tasks/graphify-integration.md` (`sha256:1329a7d7a4c2e9b5ff0c7202fd55550079b8c449051d49d924146be9aee0ea55`)
