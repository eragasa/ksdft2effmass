# Normalize the evidence package and naming

Status: implementation_complete_awaiting_human_acceptance; authorized by the human PI on 2026-08-09; must complete before `harness-simplification.evidence-and-sqlite`

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

## Implemented result

- replaced the two flat production modules with the public `ksdft2effmass.harness.pi.evidence` subpackage;
- assigned identifier records, result, and `IdentifierAuditor` to `evidence.identifiers`;
- assigned explicit Python-source/request/finding/result records and `PythonConformanceValidator` to `evidence.python_conformance`;
- removed all old public aliases and root-package re-exports;
- moved schemas, fixtures, the maintained module inventory, wrappers, resources, and tests to evidence-first names;
- retained the exact eight-object inventory and 85 one-to-one pytest-node mappings under `.pi/evidence/evidence-naming/`; and
- kept repository discovery and pytest collection in the project-local completion gate.

## Validation and limitations

The consolidated independent review reported no material findings. Ruff, mypy, Sphinx warnings-as-errors, 2,869 non-wheel tests, 63 harness validator tests, 422 focused harness tests, structural migration validation, repository evidence conformance, evidence-identifier audit, resource hashes, skill-capability validation, and diff checks pass.

The two wheel tests cannot start because `python/.venv` lacks `pip`. The H3 validator retains exactly its two pre-existing unrelated generic/local leakage and naming-version-boundary findings. Passing software checks establish no scientific validation or UQ.

## Exclusions and stop boundary

This record does not define SQLite, change evidence meaning or acceptance claims, create pytest integration in the generic package, add dependencies, perform protected execution, or activate successors. Human authorization activates only this bounded migration.
