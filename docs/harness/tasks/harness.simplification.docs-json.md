<!-- Generated from SQLite control state; do not edit. -->
# Migrate documentation and the JSON control surface

[Task index](index.md) · [Previous](./harness.simplification.control.task-catalog-reconciliation.md) · [Next](./harness.simplification.docs-json.authority-catalog.md)

## Status

`completed`: completed; all child Tasks are completed under Option C file-per-Task JSON authority, the consolidated-review findings have contract-consistent dispositions, and no child is active

## Objective

Correct the synchronization and authority delta between human-readable `docs/`, transitional Task records, and the selected JSON control surface. Preserve human-authored intake and documentation-owned subject matter while moving operational control fields to JSON-backed generated reference pages.

## Parent and prerequisites

- Depends on: `harness.simplification.api.action-object-grammar`

## Authority references

- .pi/chains/harness-simplification.chain.json
- docs
- harness/archive/task-control-v1/tasks/harness.simplification.docs-json.md

## Authorized scope

- Correct the synchronization and authority delta between human-readable `docs/`, transitional Task records, and the selected JSON control surface. Preserve human-authored intake and documentation-owned subject matter while moving operational control fields to JSON-backed generated reference pages.

## Completion criteria

- The parent is complete when each decomposed Task completes, their inputs and outputs agree, deterministic corrections are applied, unresolved findings have explicit dispositions, and one consolidated parent integration review passes. No extra parent acceptance step is required unless a material human-owned choice remains.

## Exclusions

- Markdown Task records are transitional and non-executable. Before the JSON Task contract exists, only a current explicit human instruction may activate one exact Task. No child activates automatically, parent completion is not computed, scope is not inferred from the identifier hierarchy, and chain evaluation does not interpret Markdown decomposition.
- Generic harness code may own neutral explicit-input inventory, hashing, extraction-result, relationship, partition-validation, schema-validation, and rendering mechanics. Project-local code owns repository roots, authority policy, document roles, Task identities, control schemas, projection profiles, and human decisions. Generic code must not depend on `.pi/` or ksdft2effmass-specific identities.

## Historical source

`harness/archive/task-control-v1/tasks/harness.simplification.docs-json.md` (`sha256:1aa1601ab692acee446ae35c188edeacee545ad488e5e6a65b31037bedc5fd96`)
