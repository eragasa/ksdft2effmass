<!-- Generated from SQLite control state; do not edit. -->
# Task D — Quantum ESPRESSO mechanical input/output layer

[Task index](index.md) · [Previous](./C.md) · [Next](./E.md)

## Status

`superseded`: prospectively superseded for workflow sequencing by P5; never launched

## Objective

Implement deterministic QE mechanical records, rendering, and parsing without owning scientific mapping or execution.

## Parent and prerequisites

None.

## Authority references

- harness/archive/task-control-v1/tasks/D.md

## Authorized scope

- `QuantumEspressoInputSerializer`: `QuantumEspressoInputRecord → deterministic text`;
- `QuantumEspressoOutputParser`: native output → mechanical parsed record;
- `QuantumEspressoSaveParser`: native save data → mechanical parsed record.

## Completion criteria

- Implementation, software-verification tests, documentation, independent read-only review, parent verification, and human acceptance are required. Acceptance contributes to E, F, and H; it launches none.

## Exclusions

- The layer must not import backend-neutral DFT for semantic adaptation, select scientific options, perform neutral unit conversion, run an executable, judge convergence, or construct `KohnShamDataset`. Tests use synthetic fixtures and do not launch QE.

## Historical source

`harness/archive/task-control-v1/tasks/D.md` (`sha256:489e1b91d0f68ee5a13e9215260e13a6608a49a3652efc4576031f693bdf0859`)
