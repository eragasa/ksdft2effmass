back_to: [[ksdft2Effmass.computational.01]]
# Task 01.02.01: Implement the operator-record schema

## Status

`Passed`

## Objective

Implement the operator-record schema. The task produces the artifact Tested `OperatorRecord` required by the downstream dependency graph.

## Prerequisites

[[ksdft2Effmass.computational.01.01.01|01.01.01]].

Each prerequisite must be represented by its accepted versioned artifact and validation record.

## Inputs

- the current research-plan definitions;
- documented physical or numerical decisions;
- the shared repository and test environment;
- every versioned artifact supplied by the prerequisites.

## Procedure

1. Translate the relevant physical or mathematical definition into an explicit computational specification.
2. Implement the specification, schema, or metric without relying on undocumented defaults.
3. Construct a minimal controlled example with a known expected result.
4. Run validation and regression checks.
5. Store the accepted artifact and its provenance record.

## Outputs

Primary output:

Tested `OperatorRecord` infrastructure in
`python/src/ksdft2effmass/operators/` with package exports in
`python/src/ksdft2effmass/operators/__init__.py`. Maintained evidence lives under
`python/tests/software_verification/ksdft2effmass/` and
`python/tests/numerical_verification/ksdft2effmass/`, including focused operator,
Workflow, serializer/schema, fixture, Hermiticity, geometry, and residual-analysis
owners. The earlier single-file test paths in the computational record below are
historical paths from the initial implementation state.

The output must be accompanied by its input manifest, software and environment record, validation results, and sufficient metadata to identify its state space, basis, geometry, and energy convention where applicable.

## Acceptance Criteria

- the artifact is explicit, versioned, and machine-readable where applicable;
- a controlled regression example reproduces the expected result;
- physical assumptions and numerical approximations are distinguished;
- the declared output exists and can be reconstructed from the stored inputs;
- all task-specific numerical tolerances are recorded with a pass/fail result;
- unresolved failures are not propagated as accepted downstream inputs.

## Validation Record

Record:

$$
\text{reference},
\qquad
\text{candidate},
\qquad
\text{metric},
\qquad
\text{tolerance},
\qquad
\text{result}.
$$

## Unlocks

- [[ksdft2Effmass.computational.01.03.01|01.03.01]]
- [[ksdft2Effmass.computational.01.03.02|01.03.02]]

## Failure Conditions

The task fails if its primary artifact cannot be reproduced, if its required comparison space is undefined, if validation depends only on visual agreement, or if the reported result changes beyond tolerance under an unrecorded numerical choice.

## Accepted follow-up validation state

The repository-wide operator-record validation correction was accepted on
2026-08-03 with 921 full-suite cases and 98 focused serializer/schema/fixture
cases passing, plus Ruff, mypy, Sphinx warnings-as-errors, dependency/lock,
checkpoint, whitespace, and independent integration-review gates. `jsonschema`
is a development/test dependency only; mandatory runtime dependencies remain
NumPy and SciPy. This is software verification plus the explicitly documented
numerical-verification cases, not scientific validation, UQ, physical validation,
or Rust conformance.

The accepted infrastructure includes finite record storage, Hermiticity analysis,
version-1 JSON serialization, exact compatibility auditing, represented
subtraction of already-compatible records, residual metrics, and comparison
composition. Basis/gauge alignment, unit conversion, energy-zero alignment,
geometry transformation, physical impurity identification, scientific
validation, UQ, and Rust remain outside this completed task.

## Historical computational record

- run identifier: local implementation session, 2026-07-28
- code version: `416ef8a` at task start
- software environment: Python `3.14.6`; NumPy available through the local Python environment; pytest `9.1.1`; ruff available through the local Python environment
- input manifest: `PhysicalSpecification-v1`; `NumericalSpecification-v1`; research notes distinguishing operators, finite matrix representations, state spaces, bases, geometry, and energy references
- output manifest: `python/src/ksdft2effmass/operators/records.py`; `python/src/ksdft2effmass/operators/__init__.py`; `python/src/ksdft2effmass/__init__.py`; `python/tests/test_operator_record.py`; `python/tests/test__import.py`
- validation record: `python3 -m ruff check .`; `python3 -m ruff format --check .`; `python3 -m pytest tests` from `python/`
- completion date: 2026-07-28
