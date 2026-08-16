<!-- Generated from SQLite control state; do not edit. -->
# Operator-record validation correction

[Task index](index.md) · [Previous](./operator-record-refactor.md) · [Next](./quantumespresso.simulations.md)

## Status

`human_accepted`: closed — accepted by human final decision on 2026-08-03

## Objective

correct and verify the maintained operator-record architecture, implementation, evidence classification, source/Sphinx documentation, public schema integration, and control plane without expanding scientific scope.

## Parent and prerequisites

None.

## Authority references

- .pi/agents
- .pi/chains
- .pi/skills
- docs
- docs/verification/operator-record-residual-analyzer.rst
- docs/verification/testing-and-evidence.rst
- harness/archive/task-control-v1/tasks/operator-record-validation-correction.md
- numerical_verification/ksdft2effmass/operators/test__OperatorRecordResidualAnalyzer__analytical_norms.py
- numerical_verification/ksdft2effmass/operators/test__OperatorRecordResidualAnalyzer__floating_point.py
- python/src/ksdft2effmass
- python/tests
- python/tests/ksdft2effmass/<package>/test__<ObjectName>.py
- python/tests/numerical_verification/ksdft2effmass/<package>/test__<ObjectName>__<facet>.py
- python/tests/software_verification/ksdft2effmass/<package>/test__<ObjectName>__<facet>.py
- python/tests/software_verification/ksdft2effmass/operators/test__OperatorRecordCompatibilityIssue.py
- python/tests/software_verification/ksdft2effmass/operators/test__OperatorRecordCompatibilityMismatchCode.py
- python/tests/software_verification/ksdft2effmass/operators/test__OperatorRecordDifferencer.py
- software_verification/ksdft2effmass/operators/test__OperatorRecordResidualAnalyzer__contract.py
- specification

## Authorized scope

- Authorized scope includes `AGENTS.md`, relevant `.pi/skills/`, `.pi/agents/`, `.pi/chains/`, `.pi/tasks/`, maintained source under `python/src/ksdft2effmass/`, tests under `python/tests/`, required synchronization in `specification/`, and maintained Sphinx documentation under `docs/`.

## Completion criteria

- Python 3.14 version check, package metadata validation, dependency check, Ruff format check, Ruff lint check, mypy, maintained-module inventory, public API versus object-test inventory, targeted record/Hermiticity/compatibility/comparison/serializer tests, integration tests, full pytest, schema and fixture validation, public-import smoke test, JSON round trip, deterministic serialization, source/Sphinx synchronization audit, no-`:undoc-members:` scan, no-dangling-helper scan, no-cross-private-call scan, invalid-state-fabrication scan, stale API and terminology scan, and Sphinx warning-as-error build.
- Objective: correct and verify the maintained operator-record architecture,
implementation, evidence classification, source/Sphinx documentation, public
schema integration, and control plane without expanding scientific scope.
- Final status: complete and accepted by the human PI on 2026-08-03. The accepted
public result is the finite fixed-representation operator-record API with
explicit compatibility, represented-difference, residual-analysis, comparison
Workflow, Hermiticity, and deterministic version-1 JSON serialization ownership.
The public schema and fixture corpus remain version 1.
- Artifacts produced or corrected include the operator package, progressively
migrated software- and numerical-verification tests, focused Sphinx verification
pages, optional-development schema verification dependency, two resolved human
checkpoint records, and prospective case-study episode `E02`.
- Validation evidence: 921 full-suite and 98 focused serializer/schema/fixture
cases passed; Ruff format and lint, mypy, Sphinx warnings-as-errors, lock and
wheel dependency-separation checks, checkpoint validation, `git diff --check`,
parent verification, and independent reviews passed.
- Known limitations: scientific validation, uncertainty quantification, Rust
implementation, and Python/Rust conformance were not performed. No basis,
gauge, energy-zero, unit, or geometry alignment; physical-equivalence decision;
impurity interpretation; release; publication; tag; or external calculation is
part of this task.
- Unresolved decisions: none. Dependencies satisfied: the active correction and
both human checkpoints are closed. Explicitly deferred work remains outside this
task and requires a separately selected and approved task. This handoff records
state only and does not recommend or launch subsequent work.

## Exclusions

- Graphify integration is excluded unless an active reference is directly broken. Remote processing, hooks, global skills, releases, tags, publication claims, and new scientific capabilities are excluded.

## Historical source

`harness/archive/task-control-v1/tasks/operator-record-validation-correction.md` (`sha256:f3c253f93fc3319670eae813858823bde118bac91c30de2a4060f16f3a1f1225`)
