# Task E — Quantum ESPRESSO semantic mapping

Status: prospectively superseded for workflow sequencing by P6; never launched

The separate input/result mapping content remains preserved. See `.pi/tasks/backend-neutral-cpn-workflow-architecture.md`.

## Objective

Implement two unidirectional semantic ActionObjects at the neutral/QE boundary.

## Prerequisites

- human acceptance of Tasks B, C, and D.

## Owned actions

```text
QuantumEspressoInputMapper
    KohnShamCalculationSpecification
    + QuantumEspressoNumericalOptions
    → QuantumEspressoInputRecord

QuantumEspressoResultAdapter
    parsed QE output/save records
    + accepted calculation specification
    + execution/manifest identity
    → KohnShamDataset
```

No bidirectional adapter or object owning both mappings is permitted. The result adapter owns named source-to-neutral unit/index/convention conversion and retains source conventions. It does not execute QE, decide SCF convergence, align energy zeros across calculations, or claim scientific validation.

## Completion sequence

Implementation, software and applicable numerical verification, documentation, independent read-only review, parent verification, and human acceptance are required. Acceptance unlocks F and contributes to G and H; it launches none.
