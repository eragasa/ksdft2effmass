---
name: develop-operator-records
description: Implements and reviews finite represented operator records. Use for OperatorRecord, state-space, basis, geometry, energy-reference metadata, Hermiticity analysis, operator-record serialization, and operator comparison prerequisites.
---

# Develop Operator Records

Use this skill only for represented finite operators and their immediate metadata, Hermiticity analysis, serialization, public imports, tests, and Sphinx documentation.

## Load first

Read `references/operator-record-architecture.md` before designing, implementing, testing, or reviewing this area. If split references for serialization, Hermiticity, or comparison exist, load every operator-record reference before acting.

## Target package

The authoritative Python source root is `python/src/`, established by `python/pyproject.toml` package discovery and `docs/conf.py`. The operator package is:

```text
python/src/ksdft2effmass/operators/
├── __init__.py
├── records.py
├── hermiticity.py
├── serialization.py
└── comparison.py
```

The actual Python test root is `python/tests/`. Object tests must mirror the public package hierarchy below that root:

```text
python/tests/ksdft2effmass/<package>/test__<ObjectName>.py
```

Operator-record tests use `python/tests/ksdft2effmass/operators/test__<ObjectName>.py`. Tests for genuine production Workflow objects use `python/tests/ksdft2effmass/workflows/test__<WorkflowName>.py`. Technical integrations that are not domain workflows use `python/tests/ksdft2effmass/integration/test__<IntegrationName>.py`.

Use one principal test module per public operator object: `test__StateSpace.py`, `test__Basis.py`, `test__Geometry.py`, `test__EnergyReference.py`, `test__OperatorRecord.py`, `test__HermiticityResult.py`, `test__HermiticityAnalyzer.py`, `test__OperatorRecordJsonSerializer.py`, `test__OperatorRecordCompatibilityMismatchCode.py`, `test__OperatorRecordCompatibilityIssue.py`, `test__OperatorRecordCompatibilityResult.py`, `test__OperatorRecordCompatibilityAnalyzer.py`, `test__OperatorRecordComparisonResult.py`, `test__OperatorRecordComparator.py`, and `test__IncompatibleOperatorRecordsError.py`. Do not create broad dumping-ground test modules. Do not create an `OperatorRecordWorkflow` for construct-analysis-serializer or comparison integration; route such checks as object tests or technical integration tests according to ownership.

## Human checkpoints

Do not implement before recorded human architecture approval. Escalate only genuine human decisions: material uncertainty with more than one defensible resolution about scientific semantics, architecture, public API, serialized data, compatibility, validation behavior, ownership, or scope. Record durable checkpoints under `.pi/checkpoints/` when escalation is required. Deterministic corrections already implied by approved policy are recorded as agent-resolved corrective findings, revalidated, and continued without a human checkpoint.

## Completion gates

- public API exported from `ksdft2effmass.operators`;
- unit tests cover construction, invariants, immutability, exact equality, Hermiticity analyzer policies, serializer schema behavior, JSON round trips, and public imports;
- public source documentation meets the repository-wide source-documentation standard, including private methods, private attributes, meaningful local-variable comments, validation rules, units, invariants, mathematical notation mapping, and software/scientific-validation boundaries;
- Sphinx conceptual and API documentation are updated and synchronized with source docstrings;
- formatter, linter, static type checker, unit tests, Sphinx `-W` build, public-import smoke test, JSON round-trip test, architecture review, and obsolete-helper scan pass.

Do not turn this into a general linear-algebra skill. Basis alignment and approximate physical comparison are future ActionObjects, not `OperatorRecord` methods.

## Corrective contract update

Use `test__OperatorRecordJsonSerializer.py` for JSON text serialization tests.
Require public versioned schemas, valid and invalid golden fixtures,
deterministic `serialize()` JSON text, strict `deserialize()` behavior, no
cross-object private-method calls, source documentation during implementation,
Sphinx documentation before completion, and read-only integration review after
combined-tree validation.
