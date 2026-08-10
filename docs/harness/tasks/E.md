<!-- Generated from SQLite control state; do not edit. -->
# Task E — Quantum ESPRESSO semantic mapping

[Task index](index.md) · [Previous](./D.md) · [Next](./EVIDENCE-DOC-1.md)

## Status

`superseded`: prospectively superseded for workflow sequencing by P6; never launched

## Objective

Implement two unidirectional semantic ActionObjects at the neutral/QE boundary.

## Parent and prerequisites

None.

## Authority references

- harness/archive/task-control-v1/tasks/E.md

## Authorized scope

- ```text
QuantumEspressoInputMapper
    KohnShamCalculationSpecification
    + QuantumEspressoNumericalOptions
    → QuantumEspressoInputRecord
- QuantumEspressoResultAdapter
    parsed QE output/save records
    + accepted calculation specification
    + execution/manifest identity
    → KohnShamDataset
```
- No bidirectional adapter or object owning both mappings is permitted. The result adapter owns named source-to-neutral unit/index/convention conversion and retains source conventions. It does not execute QE, decide SCF convergence, align energy zeros across calculations, or claim scientific validation.

## Completion criteria

- Implementation, software and applicable numerical verification, documentation, independent read-only review, parent verification, and human acceptance are required. Acceptance unlocks F and contributes to G and H; it launches none.

## Exclusions

- No bidirectional adapter or object owning both mappings is permitted. The result adapter owns named source-to-neutral unit/index/convention conversion and retains source conventions. It does not execute QE, decide SCF convergence, align energy zeros across calculations, or claim scientific validation.

## Historical source

`harness/archive/task-control-v1/tasks/E.md` (`sha256:5b25f8431e43fb15584a2042ad2e81c2ecda432e70ac578c8934f87b27f0c4ff`)
