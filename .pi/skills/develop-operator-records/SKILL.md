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
├── compatibility.py
├── difference.py
├── residuals.py
├── comparison.py
├── hermiticity.py
└── serialization.py
```

The comparison-related dependency direction is `records.py` -> `compatibility.py` -> `difference.py` -> `residuals.py` -> `comparison.py`. Earlier layers must not import later layers. `comparison.py` is only the concrete `OperatorRecordComparator` Workflow composition.

The actual Python test root is `python/tests/`. The focused operator-record VVUQ migration is complete. Maintained software-verification object tests use:

```text
python/tests/software_verification/ksdft2effmass/<package>/test__<ObjectName>__<facet>.py
```

Maintained numerical-verification cases use the corresponding `numerical_verification/` hierarchy. Operator-record object tests use `operators/`; tests for the genuine production comparison Workflow use `workflows/`; and technical integrations use `integration/`. Transitional paths under `python/tests/ksdft2effmass/operators/` survive only in historical records and must not be described as active maintained owners.

Use one principal test module per public operator object unless a migrated object is deliberately split into facet modules under the VVUQ hierarchy. `OperatorRecordDifferenceResult` and `OperatorRecordComparisonResult` are currently migrated to `python/tests/software_verification/ksdft2effmass/operators/test__<ObjectName>__construction.py`, `__invariants.py`, and `__value_semantics.py`. Do not use suffixes `__unit.py`, `__verification.py`, or `__validation.py`; input-invariant tests use `invariants`, not scientific validation. The genuine production Workflow `OperatorRecordComparator` currently uses `python/tests/software_verification/ksdft2effmass/workflows/test__OperatorRecordComparator.py`. Do not create broad dumping-ground test modules. Do not create an `OperatorRecordWorkflow` for construct-analysis-serializer; route such checks as object tests or technical integration tests according to ownership.

Apply the research-grade evidence-documentation standard progressively to each migrated operator test surface. Migrated modules document the evidence class, public requirement or mathematics, strategy, oracle, acceptance, exclusions, pass/fail meaning, and scientific-validation/UQ status. Every migrated test has a unique stable evidence identifier and non-tautological requirement/method/oracle/acceptance/interpretation/limitations documentation as applicable. Numerical evidence documents analytical expected values independently of the production algorithm, units, scale regime, tolerance or ULP criterion, zero-exclusion, canonicalization, warnings, and meaningful parameter IDs. Controlled backend replacement is permitted only for documented public error translation and must not be represented as validation of the dependency. Reviews check identifier uniqueness, ownership, oracle independence, failure interpretation, and synchronization with `docs/verification/testing-and-evidence.rst`.

## Human checkpoints

Do not implement before recorded human architecture approval. Escalate only genuine human decisions: material uncertainty with more than one defensible resolution about scientific semantics, architecture, public API, serialized data, compatibility, validation behavior, ownership, or scope. Record durable checkpoints under `.pi/checkpoints/` when escalation is required. Deterministic corrections already implied by approved policy are recorded as agent-resolved corrective findings, revalidated, and continued without a human checkpoint.

## Completion gates

- public API exported from `ksdft2effmass.operators`;
- software-verification tests cover construction, invariants, immutability, exact equality, Hermiticity analyzer policies, serializer schema behavior, JSON round trips, and public imports;
- public source documentation meets the repository-wide source-documentation standard, including private methods, private attributes, meaningful local-variable comments, validation rules, units, invariants, mathematical notation mapping, and software/scientific-validation boundaries;
- Sphinx conceptual and API documentation are updated and synchronized with source docstrings;
- formatter, linter, static type checker, unit tests, Sphinx `-W` build, public-import smoke test, JSON round-trip test, architecture review, and obsolete-helper scan pass.

Do not turn this into a general linear-algebra skill. Basis alignment and approximate physical comparison are future ActionObjects, not `OperatorRecord` methods.

## Accepted corrective contract

The operator-record validation-correction task closed with human final acceptance
on 2026-08-03. No operator-record corrective task or successor task is active.
Serializer evidence is owned by the five maintained
`test__OperatorRecordJsonSerializer__<facet>.py` modules plus the focused schema
and fixture integration modules. Require public versioned schemas, valid and invalid golden fixtures,
deterministic `serialize()` JSON text, strict `deserialize()` behavior, no
cross-object private-method calls, source documentation during implementation,
Sphinx documentation before completion, and read-only integration review after
combined-tree validation.
