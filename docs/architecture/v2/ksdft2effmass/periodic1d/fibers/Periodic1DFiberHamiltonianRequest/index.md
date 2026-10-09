# `Periodic1DFiberHamiltonianRequest`

**Defined in:** `ksdft2effmass.periodic1d.fibers`

## Role

Immutable shared request for rows `PERIODIC-XWALK-031` and
`PERIODIC-XWALK-032`. It requires stable parent-model, represented-operator, and
finite-state-space identities before either numerical representation is constructed.
The finite and untruncated state-space identities must differ.

## Invariants

- exact nonempty representation and provenance identities;
- exact complete periodic-1D Fourier parent model;
- exact one-dimensional `PeriodicOperatorReference`;
- operator model identity equal to the embedded parent identity;
- distinct finite and untruncated state-space identities; and
- finite reduced momentum in the closed primitive interval `[-0.5, 0.5]`.

## Evidence

`python/tests/software_verification/ksdft2effmass/periodic1d/test__Periodic1DFiberHamiltonianRequest.py`
checks positive identity retention and rejects mismatched parent and state-space
identities. These are software checks, not scientific validation.
