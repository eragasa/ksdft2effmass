# Implementation architecture

## Foundational shared slice

The first implementation slice is maintained under:

```text
python/src/ksdft2effmass/analysis/model_adequacy/band_equivalence_locality/
```

It provides:

- `AxisSymmetricFourStateParent`, which evaluates the normalized dimension-general
  directed-hopping parent for `LatticeDimension.ONE`, `.TWO`, and `.THREE`;
- `SeparableSineRotation`, which evaluates the retained-space rotation and direct
  analytic flat-parent correlation `J_0(2a/d)^d`; and
- `SignedPermutationShellInventoryBuilder`, which constructs every attainable square or
  cubic orbit shell through an exact squared-radius cap.

The diagonal-coordinate fixtures establish the 1-D specialization. Square and cubic
orbit tests establish the initial multiplicity, nesting, and conjugate-closure contracts.

## Bounded development action

`DevelopmentCalculator` now repeats the selected parent, graph-frame, projector-lift,
gauge, Monkhorst--Pack Fourier, twisted-Nyquist conversion, square-shell truncation,
withheld-evaluation, and first-passing channels. `DevelopmentVerifier` independently
reconstructs selected parent and band identities and checks stored numerical identities.
The family-owned runners produced replaceable `16 x 16`, `32 x 32`, and `64 x 64`
records under `analysis/development/` and `analysis/development-refinement/`. Tensor FFTs,
separable full Fourier evaluation, and streamed complete shells avoid dense global
cell--orbital and point-by-block phase matrices. Strict family-bound development schemas
reject extra properties and each verification record binds canonical input and result
bytes by SHA-256.

This is software and bounded development evidence only. Complete Paper 1 calculation
parity and a formal mesh/shell convergence disposition remain open; these are not an
immutable run or scientific validation. Final retained-record schemas, tolerances, convergence
actions, and retained serialization remain gated on protocol review.

It will call owner APIs directly:

- Numerics for shared-grid finite Fourier evaluation and complete Hermitian spectra;
- PhysKit for lattice displacements, matrix-valued hopping records, ordinary-lattice
  Hermiticity, explicit conjugate-closed truncation, and model-bound band evaluation;
- Optimization for generic harmonic maximization, Procrustes alignment, and reviewed
  constrained-quadratic operations.

KSD owns the parent, finite lattice/parent/retained space declarations, basis ordering,
projector and gauge identification, aligned-subtraction ledger, square action, dense
attainable-shell inventory, cyclic Nyquist conversion, sample roles, normalization,
error decomposition, dispositions, evidence, and interpretation. The protocol fixes a publication-independent 15-step prospective
execution sequence. The independent verifier must reconstruct every first passing shell
without calling the producer action; immutable run and evidence-package creation remain
separately authorized operations.
