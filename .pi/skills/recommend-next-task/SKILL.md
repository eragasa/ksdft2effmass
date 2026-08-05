---
name: recommend-next-task
description: Determine and recommend the single next repository task after a milestone, review, or implementation completes. Use when the user asks what is next, what to do next, which task should follow, which project branch to pursue, where we are in a new session, or how to continue from the current repository state. Reconstruct state from authoritative repository evidence, dependencies, blockers, validation status, research goals, and publication relevance. Remain read-only and do not create or launch the task until the human selects it.
---

# Recommend Next Task

Use this skill to recommend exactly one next repository task after a milestone,
review, implementation, chain, or human final acceptance completes. The skill is
a planning transition only. It must not create a task, modify a roadmap, edit
code or documentation, launch a chain, assign subagents, record approval, or
begin implementation.

The skill must work in a completely new session. Do not rely on chat history,
remembered recommendations, unstored agent summaries, or assumptions about what
happened in another session. The repository control plane is the authoritative
state. Graphify may be used as an optional acceleration layer for broad topology
and dependency questions, but it is derived evidence only and is never required.

## Trigger phrases

Use this skill when the user asks variants of:

- what is next;
- what should we do next;
- next task;
- continue after completion;
- what follows this milestone;
- which branch should be pursued;
- what should the agents work on now;
- what is the smallest useful next step;
- what should I work on now;
- continue the project;
- start from the repository and tell me the next task;
- I opened a new session--where are we?

## Read-only state reconstruction

Inspect actual repository evidence. Use this order:

1. identify the current repository and applicable control-plane instructions;
2. inspect unresolved checkpoints under `.pi/checkpoints/`;
3. if the current human message appears to answer a checkpoint, stop and invoke
   the shared `.agents/skills/resolve-human-checkpoint/` policy instead of
   recommending a next task;
4. identify active, blocked, accepted, and completed tasks;
5. inspect the latest durable human decisions and any authorized incomplete
   resumption step;
6. if authorized work remains incomplete, report that work as active instead of
   recommending a new task;
7. find the most recent explicit human-final-acceptance record;
8. verify that the accepted task's expected artifacts exist;
9. inspect current source, tests, specifications, and documentation;
10. optionally use the shared project Graphify skill at
   `.agents/skills/graphify/SKILL.md` for broad topology and dependency
   questions, only through its non-writing read-only query profile and within
   approved artifact and external-processing policy;
11. verify graph-derived conclusions against authoritative files;
12. identify unresolved findings or blocked decisions;
13. reconstruct the scientific dependency frontier;
14. generate candidate next tasks;
15. recommend exactly one;
16. stop for human selection.

Inspect applicable files and directories, as they exist in the repository:

- `AGENTS.md` and any narrower control-plane instructions;
- `.pi/tasks/` task records;
- `.pi/chains/` chain definitions;
- `.pi/skills/` skill routing and focused policies;
- `.pi/agents/` agent routing;
- integration-review artifacts referenced by task records;
- roadmap or planning documents;
- research documents;
- architecture documents;
- package structure;
- test tree;
- documentation tree;
- `specification/` and `fixtures/`;
- `graphify-out/graph.json` or `graphify-out/GRAPH_REPORT.md`, if present and
  relevant, as optional derived navigation aids only;
- version-control status and history, when useful.

Do not determine project state from filenames or modification times alone. A task
is complete only when the repository contains the required acceptance state. An
agent summary saying "complete" is not sufficient if the task record remains
blocked or incomplete. Do not ask the human to paste prior checkpoint reports; use
`.pi/checkpoints/`, task records, episode records, and durable decisions to
reconstruct state.

## What to determine

Determine from repository evidence:

1. what has actually been completed;
2. what remains blocked;
3. which dependencies now exist;
4. which scientific boundary is unresolved next;
5. which task would produce an independently validatable result;
6. which task advances the research or publication program;
7. which attractive branches are premature.

If repository evidence conflicts, report the uncertainty instead of silently
selecting an interpretation.

## Missing-state behavior

If the repository does not contain enough information to determine the next task,
do not invent continuity. Report exactly this section shape and stop:

```markdown
## State reconstruction incomplete

### Verified state

<What the repository establishes.>

### Missing information

<Decision, acceptance record, artifact, or roadmap information that is absent.>

### Human input required

<One focused question needed to continue.>
```

Do not create a new status file to fill the gap. If durable state is repeatedly
insufficient, recommend a control-plane improvement for human approval rather
than creating one silently.

## Candidate classification

Classify each serious candidate as exactly one of:

- `core scientific capability` -- required to make the central scientific
  program logically or computationally possible;
- `publishable scientific claim` -- directly produces evidence required for a
  paper, conference result, or defensible scientific conclusion;
- `validation or reproducibility infrastructure` -- reusable support for
  independently checking behavior, provenance, or reproducibility;
- `general engineering infrastructure` -- useful engineering support that is not
  itself the immediate scientific result;
- `premature branch` -- potentially useful, but prerequisites, semantics, or
  validation surface are not yet stable;
- `deferred work` -- valid work that should not consume current attention.

Do not produce an unranked backlog dump.

## Candidate analysis fields

For each serious candidate, report these fields:

| Field | Content |
|---|---|
| Task | Concise name |
| Classification | Core scientific capability, publishable scientific claim, validation or reproducibility infrastructure, general engineering infrastructure, premature branch, or deferred work |
| Objective | One concrete outcome |
| Scientific role | Why the research program needs it |
| Inputs | Existing objects, data, or artifacts |
| Outputs | DataObject, ActionObject, ResultObject, Workflow, document, or dataset |
| Dependencies | Required completed work |
| Validation | How correctness can be tested independently |
| Human decisions | Decisions required before implementation |
| Risk | Scientific, numerical, architectural, or scope risk |
| Publication relevance | Claim or deliverable advanced |
| Why now or later | Dependency-based justification |

## Recommendation rule

Recommend exactly one next task. The recommended task must be the smallest task
that:

- follows from completed work;
- is not blocked by an unresolved prerequisite;
- exposes or resolves the next important scientific boundary;
- produces a concrete artifact;
- has explicit inputs and outputs;
- has an independent validation strategy;
- advances the central research program;
- avoids premature language, workflow, or infrastructure expansion.

Prefer a vertical slice with a complete validation surface over a broad
framework. Do not recommend a new language implementation merely because
compatibility has been prepared. Rust, Julia, Fortran, GPU, distributed, or
workflow branches require an actual scientific or performance need.

## Object-boundary analysis

When the recommended task involves software, identify only the boundaries needed
to assess feasibility:

- DataObjects;
- ActionObjects;
- ResultObjects;
- Workflow objects, if a genuine reusable workflow exists;
- public API;
- validation artifacts;
- documentation deliverables.

Do not turn every integration into a Workflow. Do not design implementation
details beyond task feasibility.

## Optional Graphify use

Use Graphify only as an optional repository-intelligence layer after inspecting
accepted human decisions, task records, and authoritative files. The required
ordering is:

```text
unresolved checkpoints
-> accepted human decisions
-> active task records
-> source/specifications/tests/documentation
-> optional Graphify query
-> verification against authoritative files
-> exactly one recommended next task
-> human task-selection decision
-> stop
```

The skill must still work when Graphify is unavailable, `graphify-out/` is
missing, the graph is stale, or the session is new. In the validated project
environment, both Codex and pi discover repository-local skills under
`.agents/skills`; pi additionally discovers pi-specific skills under
`.pi/skills`; and a project skill may shadow a same-named global pi skill. Use
`.agents/skills/graphify/SKILL.md` as optional supporting evidence when
available, and do not require Graphify for task selection.

Never treat the following as evidence of scientific validity: a passing software
test suite alone, a connected dependency graph, type correctness, successful
serialization, documentation completeness, or agreement between two
implementations without an independent reference. If Graphify is used, cite the
authoritative file that verifies each material conclusion.

## Required output

Use this structure:

```markdown
# Recommend Next Task

## Current verified state

<Completed milestone, available capabilities, remaining blockers.>

## Candidate tasks

<Candidate comparison table.>

## Recommended next task

### Title

<One task title.>

### Problem

<Precise problem statement.>

### Why this is next

<Dependency and scientific justification.>

### Proposed boundaries

- Inputs:
- DataObjects:
- ActionObjects:
- ResultObjects:
- Workflows:
- Outputs:

### Validation

<Analytic, synthetic, regression, or reference-data strategy.>

### Publication contribution

<Claim or research deliverable advanced.>

### Human decisions required

<Questions that must be resolved before implementation.>

## Tasks to defer

<Short explanation of why other attractive branches should wait.>

## Human selection required

No task has been created or started.
```

## Durable completion handoff expectation

When reading completed task records, prefer concise durable handoff information
that identifies:

- objective;
- final status;
- human acceptance;
- artifacts produced;
- public API or scientific result;
- validation evidence;
- known limitations;
- unresolved decisions;
- dependencies now satisfied;
- explicitly deferred work.

A completion handoff describes repository state. It must not recommend or launch
the next task.

## Safeguards

- The skill recommends; the human decides.
- Do not create the recommended task.
- Do not modify roadmap, source, tests, docs, specifications, or task records.
- Do not launch chains or assign agents.
- Do not record approval.
- Do not begin implementation.
- Stop after presenting the recommendation and the human-selection notice.

## CPN invocation and evidence boundary

When represented in a prospective CPN, this skill is human-decision support and
is invoked by the external agent/harness outside guard evaluation. The immutable
request records the task, parent-workflow and attempt identities, repository
snapshot/artifact identities, skill content hash, required authoritative
references, expected output shape, read-only side-effect class, and termination
policy.

The result is an advisory candidate/recommendation artifact, not an accepted task
or launch authorization. It records the request, task, parent-workflow, and
attempt identities; inspected artifact identities; conflicts
or missing state, the single recommendation when available, Graphify use (if
any), warnings, and the required human-selection stop. Repository conflicts or
insufficient state return the documented `State reconstruction incomplete`
result rather than a fabricated recommendation. Retries require an immutable
parent authorization identity or a request's pre-authorized retry policy, use new
attempt identities, and retain earlier recommendations; identical snapshots should yield
observationally equivalent state reconstruction, while a changed snapshot is a
new input. No recommendation may fire a task-creation, task-launch, scientific-
acceptance, or execution-authorization transition.
