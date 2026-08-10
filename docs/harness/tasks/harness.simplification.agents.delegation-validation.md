<!-- Generated from SQLite control state; do not edit. -->
# Validate delegation to the durable agent set

[Task index](index.md) · [Previous](./harness.extraction.md) · [Next](./harness.simplification.api.action-object-grammar.md)

## Status

`completed`

## Objective

Verify that the currently selectable durable project and harness agents can receive bounded nonmutating delegation through the supported runtime while disabled historical phase agents remain unavailable, without treating discoverability or a successful probe as Task authority, implementation correctness, or acceptance.

## Parent and prerequisites

- External prerequisite: `harness-simplification.agents.historical-retirement`

## Authority references

- .pi/chains/harness-simplification.chain.json
- .pi/settings.json
- docs/harness/ksdft2effmass.harness.002.001.003.md
- docs/harness/ksdft2effmass.harness.002.001.009.md
- harness/archive/task-control-v1/intake/harness.simplification.agents.delegation-validation.intake.md

## Authorized scope

- Read the exact durable agent records, project-level disabled-agent configuration, supported runtime agent inventory, and applicable delegation procedure.
- Run at most one bounded fresh-context nonmutating capability probe for each currently selectable durable project or harness agent, using explicit prompts that grant no implementation, mutation, protected-action, or successor authority.
- Record exact runtime identities, run identifiers, terminal statuses, declared access modes and skills, malformed or unavailable results, and any mismatch between durable records, discovery configuration, and runtime delegation behavior.
- Produce one compact project-local software-verification report and obtain one consolidated independent read-only review of the report and its declared runtime evidence.

## Completion criteria

- The selectable durable-agent inventory and disabled historical-agent inventory agree with the exact maintained records and project configuration, with every discrepancy reported rather than normalized away.
- Every selectable durable agent has exactly one retained bounded probe disposition, and no disabled historical agent is launched merely to demonstrate that it is disabled.
- Probe results establish only discovery and delegation transport behavior; they do not claim agent correctness, Task authorization, scientific validity, protected-action authority, or human acceptance.
- The independent review has no unresolved material finding, focused structural checks pass, unrelated repository state is preserved, and no dependency or lockfile changes occur.
- On completion the Task becomes completed, chain active_task returns to null, automatic successor activation remains false, and no successor is activated.

## Exclusions

- Do not edit durable or historical agent records, revive or delete historical agents, change project discovery configuration, add another dispatcher or replay layer, or redesign the delegation runtime.
- Do not assign production implementation, documentation mutation, test mutation, scientific work, external execution, release work, or another Task through a capability probe.
- Do not add dependencies, change lockfiles, implement SQLite or evidence persistence, reopen H0-H4, or activate review-dispatch-idempotency, evidence-and-sqlite, scientific, publication, release, or protected work.

## Historical source

No archived source.
