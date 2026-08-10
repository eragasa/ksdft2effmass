<!-- Generated from SQLite control state; do not edit. -->
# Select and explicitly activate the next harness-simplification Task

[Task index](index.md) · [Previous](./harness.simplification.api.action-object-grammar.md) · [Next](./harness.simplification.control.task-catalog-reconciliation.md)

## Status

`superseded_by_direct_human_selection`

## Objective

After prerequisite work is complete, present eligible harness-simplification successors for a current human selection and record exactly one explicit activation without inferring continuation from documentation, completion, ordering, or agent recommendation.

## Parent and prerequisites

- Depends on: `harness.simplification.resources.h3-validator-retirement`

## Authority references

- .pi/chains/harness-simplification.chain.json
- harness/archive/task-control-v1/intake/harness.simplification.control.successor-selection.intake.md

## Authorized scope

- Inspect bounded durable chain and exact Task records to identify prerequisite-eligible inactive harness-simplification candidates.
- Present the eligible choices and their controlling scope, prerequisites, protected boundaries, and unresolved decisions to the human authority.
- After one unambiguous current human selection, update the selected Task and chain activation facts through the applicable durable procedure.

## Completion criteria

- No candidate is presented as active or authorized merely because it is eligible, ordered next, documented, or recommended.
- Exactly one unambiguous current human selection is preserved in durable control state before activation.
- The chain active_task, selected Task status, and explicit activation facts agree, automatic successor activation remains false, and focused state inspection passes.

## Exclusions

- Do not select a successor on behalf of the human, infer approval from silence or prior completion, or activate more than one Task.
- Do not expand the selected Task scope, execute its implementation, perform protected work, or treat a reviewer or deterministic check as human acceptance.
- Do not activate this Task automatically; a later current human instruction must authorize its activation after prerequisites are satisfied.

## Historical source

No archived source.
