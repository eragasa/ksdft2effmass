# Graphify Codex/pi Integration Task

## Status

Implementation complete for Graphify integration and the E01 control-plane closeout correction. E01-F01, E01-F02, and E01-F03 were accepted on 2026-07-30. A bounded post-closeout trigger-collision correction was directed on 2026-08-07; it changes routing policy but does not reopen E01 or launch another task. E01 remains closed as accepted. Scientific validation is not applicable to this control-plane/developer-tooling task.

## Post-closeout trigger-collision correction

Human response preserved verbatim: “resolve the skill collision”.

Normalized decision: remove the overlapping automatic trigger between Graphify
and `recommend-next-task`. `recommend-next-task` exclusively owns ordinary
next-task questions. Graphify runs only when the current human message explicitly
requests Graphify; ordinary topology, dependency, impact, and navigation
questions remain normal repository-analysis requests and do not implicitly run
Graphify. This supersedes only the earlier E01 provisions that allowed Graphify
to be invoked automatically as optional next-task or broad-topology support.
Graphify remains available as an explicit, local, advisory tool under the
previous no-hook, no-external-processing, no-authority, and ignored-output
boundaries.

The correction contracts the active entry runbook to the supported local CLI
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

## Decision record: Option B approved

### Decision

Manually integrate Graphify 0.9.2 as an optional, read-only repository-analysis tool for Codex and pi without running the Graphify project installer.

### Context

The repository now has a completed operator-record refactor and a repository-local `choose-next-task` skill. The human requested integration of Graphify with OpenAI Codex and pi to support repository topology, dependency, impact, navigation, and next-task analysis. Graphify must remain a derived navigation aid, not an authoritative source of project state or scientific meaning.

Read-only inspection found Graphify 0.9.2 installed at `/Users/eugene/.local/bin/graphify`. The command `graphify install --project --platform codex` would create a Codex skill but would also write an always-on Graphify section to `AGENTS.md` and install `.codex/hooks.json`. The repository requires explicit human approval before modifying `AGENTS.md`, installing hooks, enabling remote semantic processing, or transmitting unpublished research externally.

### Options considered

1. Run `graphify install --project --platform codex` as-is.
   - Would install the project-local Codex skill.
   - Would also modify `AGENTS.md` automatically and install `.codex/hooks.json`.
   - Rejected because hooks and generic always-on policy were not approved.
2. Manually copy the Graphify 0.9.2 Codex skill and references into `.agents/skills/graphify/`, then add narrow repository policy manually.
   - Preserves project-local shared skill discovery in the validated environment.
   - Avoids installer-controlled `AGENTS.md` edits.
   - Avoids hooks and global configuration changes.
   - Approved and later corrected after pi also discovered `.agents/skills/graphify/`.
3. Defer Codex installation and add pi-only routing.
   - Safest but incomplete relative to the requested Codex integration.
   - Rejected as the primary path.

### Human resolution

Option B is approved.

Approved actions:

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

### Consequences

Graphify may assist repository navigation, dependency analysis, impact analysis, and task selection. Graphify output is derived and may be incomplete or stale. Every material Graphify-derived conclusion must be checked against authoritative repository files.

Authority hierarchy:

```text
1. Explicit human decisions
2. AGENTS.md
3. Accepted task and decision records
4. Public scientific specifications and schemas
5. Production source
6. Tests and validation fixtures
7. Human-reviewed documentation
8. Graphify-derived repository graph
```

Graphify output is never an architectural decision record, scientific specification, validation result, source of scientific truth, or approval authority.

### Affected files and agents

Expected affected control-plane and developer-documentation files:

- `AGENTS.md`;
- `.gitignore`;
- `.agents/skills/graphify/SKILL.md`;
- `.agents/skills/graphify/references/`;
- `.agents/skills/graphify/.graphify_version`;
- `.pi/skills/choose-next-task/SKILL.md`;
- `.agents/skills/graphify/references/ksdft2effmass-policy.md`;
- `.pi/tasks/graphify-integration.md`;
- `docs/development/ai-assisted-development.rst`;
- `docs/development/agent-control-plane.rst`;
- `docs/research/agentic-development-case-study.rst`;
- `docs/research/agentic-development-case-study/`;
- `docs/index.rst`;
- repository-layout documents only if necessary to document control-plane locations.

Expected unaffected areas:

- production source code;
- object tests and validation fixtures;
- scientific specifications;
- scientific algorithms;
- research results.

### Date

2026-07-30

### Explicitly prohibited actions

Do not:

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

## Completion targets

- Shared Graphify project skill installed manually in `.agents/skills/graphify/`.
- Narrow Graphify policy recorded in `AGENTS.md`.
- shared Graphify discovery and optional use in `choose-next-task` documented.
- Generated-artifact retention policy recorded and `graphify-out/` ignored.
- Case-study protocol and E00/E01 records created.
- Sphinx developer documentation added.
- Narrow Graphify validation run completed or explicitly blocked.
- JSON, skill, Sphinx, discovery, no-hook, no-API, no-production-change, dry-run, and integration-review gates run.
- E01 record updated with implementation status, validation status, and human-final-acceptance state.


## Verification summary

Implementation status: complete.
Verification status: pending for the E01-F03 control-plane closeout correction.
Scientific validation: not_applicable.
Human final acceptance: accepted on 2026-07-30 for E01-F01 and E01-F02; pending for E01-F03.

Validation evidence for the accepted E01-F01/E01-F02 work includes JSON syntax checks, JSON Schema validation for E00/E01 episode records, skill frontmatter checks, Codex and pi fresh-session skill discovery, duplicate-skill scans, no-hook checks, no API-key configuration check, ignored `graphify-out/` check, Sphinx warning-as-error build, Graphify code-only local validation, fresh-session `choose-next-task` dry run, and read-only integration review. E01-F03 closeout validation is being recorded separately in the current correction.

The broader approved Graphify scope containing documentation was attempted without API keys and blocked by the Graphify CLI because semantic extraction for docs requires an LLM backend. No external backend was enabled and no repository content was transmitted externally. A code-only approved subset from `python/src` and `python/tests` was used for local AST-only validation and produced `graphify-out/graph.json`. Generated outputs remain ignored.


## Material finding E01-F01

Status: corrected and accepted by human final decision on 2026-07-30.

Finding: Graphify 0.9.2 installer source placed the Codex skill under `.codex/skills`, but current official Codex documentation specifies repository-local skills under `.agents/skills`. The original validation checked file presence rather than actual fresh Codex discovery.

Correction: The repository-local Codex Graphify skill was moved to `.agents/skills/graphify/`, the obsolete `.codex/skills/graphify/` copy was removed, and a fresh Codex exec session from the repository root reported the `graphify` skill at `/Users/eugene/repos/ksdft2effmass/.agents/skills/graphify/SKILL.md`.

Historical evidence is preserved in `docs/research/agentic-development-case-study/episodes/E01-graphify-integration/checkpoint-02.md` and the E01 episode record.

## Material finding E01-F02

Status: corrected and accepted by human final decision on 2026-07-30.

Finding: Fresh-session pi discovery demonstrated that pi automatically discovers the repository-local `.agents/skills/graphify` skill and shadows the same-named global pi Graphify skill. This contradicted the previous documented discovery-surface model and identified a duplicate project-local Graphify routing path through `.pi/skills/use-graphify`.

Correction: `.agents/skills/graphify/` is now the shared repository-local Graphify skill for both Codex and pi in the validated project environment. A repository policy overlay was added at `.agents/skills/graphify/references/ksdft2effmass-policy.md`, the duplicate `.pi/skills/use-graphify/` routing skill was removed, and active documentation now records the observed shared-skill and project-over-global precedence model.

Historical evidence is preserved in `docs/research/agentic-development-case-study/episodes/E01-graphify-integration/checkpoint-03.md` and the E01 episode record.


## E01-F03 process correction: checkpoint granularity

Status: corrected and accepted by human final decision on 2026-07-30.

Finding: Human governance became unnecessarily burdensome when the control plane
treated administrative recordkeeping, deterministic correction, workflow
resumption, and closeout recording as separate human decisions after the
substantive human decision was already supplied.

Correction: The control plane now distinguishes deterministic agent correction,
standing delegated decision, and genuine human decision. Deterministic
corrections and standing delegated decisions are recorded, revalidated, and
continued automatically. Genuine human decisions are stored as durable JSON
checkpoints under `.pi/checkpoints/`; the shared
`.agents/skills/resolve-human-checkpoint/` skill records unambiguous human
responses, clears checkpoints, resumes authorized work, reruns validation, and
reports outcomes without requiring special human wording. New-session,
chain-resumption, and final-acceptance behavior now use durable state instead of
requiring the human to paste checkpoint reports or send administrative prompts.

Evidence paths:

- `AGENTS.md`
- `.agents/skills/resolve-human-checkpoint/SKILL.md`
- `.pi/checkpoints/README.md`
- `.pi/checkpoints/checkpoint.schema.json`
- `.pi/checkpoints/fixtures/`
- `.pi/checkpoints/validate_checkpoints.py`
- `.pi/skills/choose-next-task/SKILL.md`
- `.pi/chains/operator-record-refactor.chain.json`
- `docs/development/agent-control-plane.rst`
- `docs/development/ai-assisted-development.rst`
- `docs/research/agentic-development-case-study.rst`
- `docs/research/agentic-development-case-study/episodes/E01-graphify-integration/episode.json`

## Human final acceptance

Date: 2026-07-30 for E01-F01 and E01-F02.

Human final decision already recorded: E01-F01 and E01-F02 are accepted as
corrected. The shared project Graphify skill, intentional project-over-global
precedence, removal of the redundant `use-graphify` skill, updated Graphify
control-plane policies, documentation, case-study evidence, and verification
results were accepted.

Current closeout acceptance: E01-F03 process correction and final E01 closeout
accepted on 2026-07-30.

Final state:

```text
E01-F01: accepted as corrected
E01-F02: resolved and accepted
E01-F03: accepted as corrected
implementation_status: complete
verification_status: passed
human_final_acceptance: accepted
scientific_validation: not_applicable
```

No next task was launched.
