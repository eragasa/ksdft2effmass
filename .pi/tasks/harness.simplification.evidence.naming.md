# Normalize the evidence package and naming

Status: proposed_inactive; must complete before `harness-simplification.evidence-and-sqlite`

Task identity: `harness.simplification.evidence.naming`

Predecessor task record: `602bb5d4695b590d7f55effd7bb22a7df27c097f:.pi/tasks/harness-simplification.evidence.pytest-naming.md`

Predecessor task identity: `harness-simplification.evidence.pytest-naming`

Relationship: this Task supersedes that proposed-inactive plan. The predecessor evaluated pytest-specific naming; this replacement instead separates the evidence domain into a subpackage, reserves pytest naming for direct pytest integration, and follows the accepted ActionObject grammar. This is a material proposal change, not a mechanical identifier rename.

Prerequisite: `harness.simplification.api.action-object-grammar:completed`

## Objective

Replace the visually ambiguous flat production family `evidence.py`, `test_evidence.py`, and `test_evidence_*` with an explicit `evidence` domain subpackage. Reserve `test_*.py`, `test__*.py`, and `test_*` function names for actual pytest collection. Reserve `pytest` in production names for components that directly integrate with pytest.

## Package boundary

The target public domain is:

```text
python/src/ksdft2effmass/harness/pi/evidence/
├── __init__.py
├── identifiers.py
└── python_conformance.py
```

`evidence.identifiers` owns evidence-identifier occurrences and auditing. `evidence.python_conformance` owns structural conformance of explicitly supplied evidence-bearing Python modules and metadata. Repository-local discovery, inventory binding, and pytest collection remain outside the generic package.

The public ActionObjects must follow `<DataObject-or-operation-target><Actionizer>`, for example `evidence.IdentifierAuditor` and `evidence.PythonConformanceValidator`. Exact DataObject and ResultObject names must avoid redundant `Evidence` prefixes inside the `evidence` namespace while remaining role-complete and unambiguous.

Resources should use an evidence-first hierarchy, including `harness/pi/schemas/evidence/module-inventory.schema.json` and a semantic evidence-repository-conformance inventory location selected by the task.

## Migration boundary

Human decision: this is pre-release software with no public API consumers requiring compatibility preservation. Apply a hard package and object rename with no compatibility aliases or deprecation period. Synchronize the public family, flat-module imports and exports, command wrappers, schemas, fixtures, evidence inventories, skills, documentation, manifests, issue-code disposition, and actual pytest modules. Retain a complete old/new node map only because the maintained-evidence contract requires identity migration, not for API compatibility.

This naming and packaging concern is independent of `harness.simplification.docs-json`; neither Task consumes the other's outputs. Both follow their actual prerequisites. The later evidence/SQLite task remains inactive and depends on this Task.

## Completion gates

Completion requires accepted exact object inventory and names, the generic/project-local dependency boundary, the contract-required maintained-evidence node map, synchronized source and maintained evidence, focused API and wrapper agreement tests, broader affected checks, one consolidated review, and final human acceptance when required.

## Exclusions and stop boundary

This record does not activate the migration, define SQLite, change evidence meaning or acceptance claims, create pytest integration in the generic package, add dependencies, perform protected execution, or activate successors. It remains proposed and inactive until separately authorized.
