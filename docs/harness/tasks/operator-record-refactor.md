<!-- Generated from SQLite control state; do not edit. -->
# Operator-Record DataObject/ActionObject Refactor Task

[Task index](index.md) · [Previous](./operator-record-comparison.md) · [Next](./operator-record-validation-correction.md)

## Status

`human_accepted`: Closed and accepted. Human final acceptance was approved on 2026-07-30 after parent verification. Later operator-record corrections are recorded prospectively in `.pi/tasks/operator-record-validation-correction.md`, accepted on 2026-08-03; they do not erase this task's original chronology or accepted historical evidence. Scientific validation has not been performed and remains outside both tasks.

## Objective

Refactor finite operator records so represented data, Hermiticity analysis, and serialization follow the repository DataObject/ActionObject architecture without unrelated cleanup.

## Parent and prerequisites

None.

## Authority references

- .pi/skills/design-data-action-objects/references/data-action-architecture.md
- .pi/skills/develop-operator-records/references/operator-record-architecture.md
- docs/conf.py
- harness/archive/task-control-v1/tasks/operator-record-refactor.md
- python
- python/pyproject.toml
- python/src
- python/src/ksdft2effmass
- python/src/ksdft2effmass/operators
- python/tests
- python/tests/ksdft2effmass/<package>/test__<ObjectName>.py
- python/tests/ksdft2effmass/integration/test__<IntegrationName>.py
- python/tests/ksdft2effmass/operators
- python/tests/ksdft2effmass/workflows/test__<WorkflowName>.py

## Authorized scope

- DataObject/ActionObject/ResultObject architecture;
- finite operator-record invariants;
- orthonormal-basis restriction;
- geometry and energy-reference conventions;
- Hermiticity analysis;
- strict schema-version-1 specification;
- deterministic JSON text serialization;
- valid and invalid conformance fixtures;
- object-scoped tests;
- public API;
- Sphinx and source documentation;
- control-plane policies and completion gates;
- Python/Rust-compatible wire-format preparation.

## Completion criteria

- The parent pi must independently run the combined unit tests, Ruff formatter check, Ruff lint check, mypy check, Sphinx build with warnings treated as errors, public-import smoke test, JSON round-trip test, architecture-conformance review, obsolete-import scan, and dangling-helper scan.
- A failing gate leaves the task incomplete unless the human explicitly accepts the unresolved failure after receiving its cause and consequences.

## Exclusions

- This acceptance validates software behavior, mathematical data invariants, schema semantics, serialization reproducibility, API organization, and documentation consistency. It does not validate the physical correctness of a represented Hamiltonian, basis alignment between calculations, energy-reference alignment between calculations, Wannier reconstruction accuracy, tight-binding reduction accuracy, impurity extraction, or comparison with first-principles data. Those require separate scientific-validation ActionObjects, Workflows, reference datasets, and acceptance criteria.
- No Rust implementation, schema version `2`, or scientific-validation workflow is started as part of closing this task.

## Historical source

`harness/archive/task-control-v1/tasks/operator-record-refactor.md` (`sha256:ebf51dc2136769f19e739fa0db05e2da11b1fe3fd0971eb80d6e555093117668`)
