# E02 evidence index: operator-record validation correction

Episode `E02` prospectively records the repository-wide operator-record
architecture, implementation, VVUQ evidence, documentation, and control-plane
correction accepted on 2026-08-03.

## Accepted task and human decisions

- `.pi/tasks/operator-record-validation-correction.md` is the detailed decision,
  correction, review, verification, limitation, and final-acceptance record.
- `.pi/checkpoints/D054-HC01-hermiticity-result-scalar-typing.json` records the
  accepted typing-only constructor-contract decision.
- `.pi/checkpoints/D069-HC01-jsonschema-test-dependency.json` records the accepted
  optional-development-only `jsonschema` decision.

## Public implementation and specification

- `python/src/ksdft2effmass/operators/` contains the accepted DataObjects,
  ResultObjects, ActionObjects, and comparison Workflow.
- `specification/operator-record/v1/` contains the unchanged public version-1
  wire schema and golden fixtures.
- `python/pyproject.toml` and `python/uv.lock` record the development-only schema
  verification dependency without adding a runtime dependency.

## Verification evidence

- `python/tests/software_verification/ksdft2effmass/` contains migrated software
  contract evidence.
- `python/tests/numerical_verification/ksdft2effmass/` contains the selected
  analytical and floating-point algorithm evidence.
- `docs/verification/` documents evidence ownership, identifiers, acceptance
  criteria, exclusions, and VVUQ boundaries.
- The accepted task record reports 921 passing full-suite cases, 98 focused
  serializer/schema/fixture cases, static and documentation checks, parent
  verification, and independent reviews.

## Limitations and deferred work

E02 does not establish scientific validation, uncertainty quantification, or
Python/Rust conformance. It does not perform basis, gauge, energy-zero, unit, or
geometry alignment; physical-equivalence determination; impurity-operator
interpretation; or a scientific pass/fail decision. No release, publication,
tag, or external calculation was produced.
