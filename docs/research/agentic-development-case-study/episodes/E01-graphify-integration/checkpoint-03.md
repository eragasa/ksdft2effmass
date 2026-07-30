# E01 checkpoint 03: shared Graphify skill discovery correction

## Required finding record

```text
identifier: E01-F02
category: I
severity: material
stage: human_final_acceptance
status: accepted
```

Description:

```text
Fresh-session pi discovery demonstrated that pi automatically
discovers the repository-local .agents/skills/graphify skill and
shadows the same-named global pi Graphify skill. This contradicts
the previously documented discovery-surface model and creates a
potential duplicate instruction path through .pi/skills/use-graphify.
```

## Exact discovery output

```text
✓ auto (project) ~/repos/ksdft2effmass/.agents/skills/graphify/SKILL.md
✗ ~/.pi/agent/skills/graphify/SKILL.md (skipped)
```

## Corrected discovery model

```text
.agents/skills/
    Shared repository-local agent skills.
    Confirmed discoverable by Codex and pi in this environment.

.pi/skills/
    pi-specific skills that have no shared equivalent.

~/.pi/agent/skills/
    Global pi fallback skills.
    A same-named repository skill may take precedence.

.codex/
    Codex configuration and hooks only when explicitly approved.
```

The repository-local Graphify skill intentionally takes precedence over the
global pi Graphify skill because the project-local version is versioned with the
repository and subject to repository policy. The global pi skill was not modified
or deleted.

## Project/global Graphify skill comparison

Compared paths:

- project: `.agents/skills/graphify/SKILL.md`
- global pi fallback: `~/.pi/agent/skills/graphify/SKILL.md`
- project references: `.agents/skills/graphify/references/`
- global references: `~/.pi/agent/skills/graphify/references/`

### Summary table

| Field | Project skill | Global pi fallback |
|---|---|---|
| name | `graphify` | `graphify` |
| version | `0.9.2` in `.graphify_version` | `0.9.2` in `.graphify_version` |
| description | Same frontmatter description: codebase, architecture, file relationships, project content, existing `graphify-out/`, knowledge graph, god nodes, community detection, query/path/explain. | Same frontmatter description. |
| invocation assumptions | Repository-local copied Codex skill. Step B2 assumes Codex `spawn_agent`, `wait_agent`, and `close_agent`, with `multi_agent = true` under `~/.codex/config.toml`; semantic chunk results are collected in memory. | Global pi fallback skill. Step B2 assumes an Agent tool with `subagent_type="general-purpose"`, chunk files written to disk, and `CHUNK_PATH` substitution. |
| supported hosts | Codex-specific semantic-subagent instructions in the differing Step B2 block; now discovered by pi in this environment through `.agents/skills/`. | pi/Claude-style Agent-tool semantic-subagent instructions. |
| graph-generation behavior | Full Graphify pipeline, `graphify-out/` outputs, structural AST extraction, optional semantic extraction, graph build, clustering, report, HTML, optional exports. | Same overall pipeline. |
| remote-backend behavior | Uses Gemini only if `GEMINI_API_KEY` or `GOOGLE_API_KEY` is already set; otherwise host agent is the LLM. No Anthropic/OpenAI key prompt. | Same remote-backend policy. |
| conflicting instructions | Step B2 and B3 conflict for semantic extraction host mechanics: Codex in-memory spawn/wait/close versus Agent-tool disk chunk files. The project policy overlay constrains repository use but does not claim the host mechanics are equivalent. | Same conflict from the opposite host perspective. |
| material differences | The only substantive `SKILL.md` difference before the local overlay was the semantic subagent dispatch block. Reference files matched. `.graphify_version` differed only by final newline. | Reference files matched; version content was the same string with no trailing newline. |

Material comparison result: matching names and version strings do not prove
equivalent execution semantics. The two skills share the same Graphify pipeline
and safety language, but their semantic-subagent dispatch assumptions differ by
host. For this repository, the shared project skill is authoritative subject to
`.agents/skills/graphify/references/ksdft2effmass-policy.md`.

## Corrective actions recorded

- Added `.agents/skills/graphify/references/ksdft2effmass-policy.md` as a
  repository-local policy overlay.
- Updated `.agents/skills/graphify/SKILL.md` minimally to require reading and
  obeying the policy overlay in this repository.
- Preserved upstream Graphify provenance and version `0.9.2`.
- Removed the duplicate `.pi/skills/use-graphify/` routing skill after migrating
  its repository authority, safety, artifact, and human-intervention rules into
  the shared policy overlay.
- Updated `.pi/skills/choose-next-task/SKILL.md` to use
  `.agents/skills/graphify/SKILL.md` as optional supporting evidence while still
  functioning when Graphify is unavailable.
- Updated active discovery documentation to record observed behavior rather than
  an assumed universal rule.

## Required historical sequence

```text
assumed separate skill surfaces
→ installed Codex project skill under .agents/skills
→ fresh pi session also discovered it
→ global pi skill was shadowed
→ duplicate project routing was identified
→ shared project skill model adopted
→ both hosts verified
```

## Post-correction status target

```text
E01-F01: corrected
E01-F01: accepted as corrected
E01-F02: resolved and accepted
implementation_status: complete
verification_status: passed
human_final_acceptance: accepted
scientific_validation: not_applicable
```


## Human final acceptance

Date: 2026-07-30.

Human final decision: ACCEPT E01. E01-F01 and E01-F02 are accepted as
corrected. The shared project Graphify skill, intentional project-over-global
precedence, removal of the redundant `use-graphify` skill, updated
control-plane policies, documentation, case-study evidence, and verification
results are accepted. E01-F02 is resolved and accepted. E01 is closed as
accepted.

No next task was launched.
