# Harness Tasks architecture

## Responsibility

`ksdft2effmass.harness.tasks` owns immutable definitions, explicit selection, derived inspection context, and closure records for bounded software-development and documentation work. It does not execute repository operations, scientific workflows, calculators, or analyses.

```mermaid
flowchart LR
    definition["HarnessTask definition"] --> catalog["HarnessTaskCatalog"]
    catalog --> graph["HarnessTaskGraph"]
    graph --> eligibility["Eligibility evaluation"]
    decisions["Resolved human decisions"] --> eligibility
    eligibility --> selection["DevelopmentTaskSelection"]
    selection --> work["Repository work"]
    work --> evidence["Evidence and review references"]
    evidence --> closure["HarnessTaskClosure"]
    closure --> acceptance["Separate acceptance, when required"]
```

A Task describes work. Selection authorizes represented active work. One closure records how that selection ended. Acceptance remains a separate represented fact when required.

## Architecture map

- [Task definition](task-definition.md)
- [Selection and eligibility](selection-and-eligibility.md)
- [Lifecycle](lifecycle.md)
- [Graph and dependencies](graph-and-dependencies.md)
- [Decisions and authority](decisions-and-authority.md)
- [Evidence and review](evidence-and-review.md)
- [Persistence and projections](persistence-and-projections.md)

## Core invariants

- `HarnessTask` has no general mutable lifecycle status or phase machine.
- Selection references an exact Task revision and declared control scope.
- Eligibility is a derived result, not authority.
- Task order and successor relations do not activate work.
- Automatic successor activation is disabled by default.
- One immutable closure ends one selection; completed closure does not imply human acceptance.
- Harness Task state never substitutes for `ScientificWorkflowRun` state.
- Generated projections cannot create or mutate authoritative state.

## Package boundary

```text
ksdft2effmass.harness.tasks
    → generic harness identity, evidence, decision, and repository contracts

ksdft2effmass.harness.tasks
    ✗→ ksdft2effmass.workflow.scientific runtime state
    ✗→ ksdft2effmass.petrinet.colored execution
    ✗→ calculator execution
    ✗→ scientific analysis or disposition
```

A Task may reference immutable implementation or scientific-contract identities when development work concerns those components. Such references grant no scientific execution or acceptance authority.

## Unresolved issues

- Exact `HarnessTaskClosure` wire contract.
- Authority required for non-completed closure dispositions.
- Whether independent repository control scopes may be active concurrently.
- Compatibility and migration policy for current Task JSON records.
- Exact acceptance-record and completion-record wire contracts.
