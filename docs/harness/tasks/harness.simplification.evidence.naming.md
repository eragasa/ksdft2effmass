<!-- Generated from SQLite control state; do not edit. -->
# Normalize the evidence package and naming

[Task index](index.md) · [Previous](./harness.simplification.docs-json.task-model-simplification.md) · [Next](./harness.simplification.resources.h3-validator-retirement.md)

## Status

`completed`: completed; human-accepted on 2026-08-09; must complete before `harness-simplification.evidence-and-sqlite`

## Objective

Replace the visually ambiguous flat production family `evidence.py`, `test_evidence.py`, and `test_evidence_*` with an explicit `evidence` domain subpackage. Reserve `test_*.py`, `test__*.py`, and `test_*` function names for actual pytest collection. Reserve `pytest` in production names for components that directly integrate with pytest.

## Parent and prerequisites

- Depends on: `harness.simplification.api.action-object-grammar`

## Authority references

- .pi/chains/harness-simplification.chain.json
- 602bb5d4695b590d7f55effd7bb22a7df27c097f:.pi/tasks/harness-simplification.evidence.pytest-naming.md
- harness/archive/task-control-v1/tasks/harness.simplification.evidence.naming.md

## Authorized scope

- Replace the visually ambiguous flat production family `evidence.py`, `test_evidence.py`, and `test_evidence_*` with an explicit `evidence` domain subpackage. Reserve `test_*.py`, `test__*.py`, and `test_*` function names for actual pytest collection. Reserve `pytest` in production names for components that directly integrate with pytest.
- Human decision: this is pre-release software with no public API consumers requiring compatibility preservation. Apply a hard package and object rename with no compatibility aliases or deprecation period. Synchronize the public family, flat-module imports and exports, command wrappers, schemas, fixtures, evidence inventories, skills, documentation, manifests, issue-code disposition, and actual pytest modules. Retain a complete old/new node map only because the maintained-evidence contract requires identity migration, not for API compatibility.

## Completion criteria

- Completion requires accepted exact object inventory and names, the generic/project-local dependency boundary, the contract-required maintained-evidence node map, synchronized source and maintained evidence, focused API and wrapper agreement tests, broader affected checks, one consolidated review, and final human acceptance when required.

## Exclusions

- The target public domain is:
- ```text
python/src/ksdft2effmass/harness/pi/evidence/
├── __init__.py
├── identifiers.py
└── python_conformance.py
```
- `evidence.identifiers` owns evidence-identifier occurrences and auditing. `evidence.python_conformance` owns structural conformance of explicitly supplied evidence-bearing Python modules and metadata. Repository-local discovery, inventory binding, and pytest collection remain outside the generic package.
- The public ActionObjects must follow `<DataObject-or-operation-target><Actionizer>`, for example `evidence.IdentifierAuditor` and `evidence.PythonConformanceValidator`. Exact DataObject and ResultObject names must avoid redundant `Evidence` prefixes inside the `evidence` namespace while remaining role-complete and unambiguous.
- Resources should use an evidence-first hierarchy, including `harness/pi/schemas/evidence/module-inventory.schema.json` and a semantic evidence-repository-conformance inventory location selected by the task.
- Human decision: this is pre-release software with no public API consumers requiring compatibility preservation. Apply a hard package and object rename with no compatibility aliases or deprecation period. Synchronize the public family, flat-module imports and exports, command wrappers, schemas, fixtures, evidence inventories, skills, documentation, manifests, issue-code disposition, and actual pytest modules. Retain a complete old/new node map only because the maintained-evidence contract requires identity migration, not for API compatibility.
- This naming and packaging concern is independent of `harness.simplification.docs-json`; neither Task consumes the other's outputs. Both follow their actual prerequisites. The later evidence/SQLite task remains inactive and depends on this Task.
- This record does not define SQLite, change evidence meaning or acceptance claims, create pytest integration in the generic package, add dependencies, perform protected execution, or activate successors. Human authorization activates only this bounded migration.

## Historical source

`harness/archive/task-control-v1/tasks/harness.simplification.evidence.naming.md` (`sha256:af6dc6343b9bdc71c1ad76e29b52cfcb94528f1794f6cd88d34fa084017a07cf`)
