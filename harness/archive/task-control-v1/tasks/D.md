# Task D — Quantum ESPRESSO mechanical input/output layer

Status: prospectively superseded for workflow sequencing by P5; never launched

The QE mechanical-I/O content remains preserved. See `.pi/tasks/backend-neutral-cpn-workflow-architecture.md`.

## Objective

Implement deterministic QE mechanical records, rendering, and parsing without owning scientific mapping or execution.

## Prerequisites

- human acceptance of Task A.

## Owned actions

- `QuantumEspressoInputSerializer`: `QuantumEspressoInputRecord → deterministic text`;
- `QuantumEspressoOutputParser`: native output → mechanical parsed record;
- `QuantumEspressoSaveParser`: native save data → mechanical parsed record.

The layer must not import backend-neutral DFT for semantic adaptation, select scientific options, perform neutral unit conversion, run an executable, judge convergence, or construct `KohnShamDataset`. Tests use synthetic fixtures and do not launch QE.

## Completion sequence

Implementation, software-verification tests, documentation, independent read-only review, parent verification, and human acceptance are required. Acceptance contributes to E, F, and H; it launches none.
