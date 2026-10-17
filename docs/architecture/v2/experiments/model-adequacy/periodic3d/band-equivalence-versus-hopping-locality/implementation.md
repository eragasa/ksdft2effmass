# Implementation architecture

## Foundational shared slice

The shared KSD implementation under

```text
python/src/ksdft2effmass/analysis/model_adequacy/band_equivalence_locality/
```

already evaluates the dimension-general parent and sine rotation, computes the direct
analytic correlation `J_0(2a/d)^d`, and constructs dense cubic signed-permutation shell
inventories. The 3-D tests establish the first cubic orbit multiplicities and conjugate-
closed nesting.

## Bounded development action

`DevelopmentCalculator` repeated the parent, graph-frame, projector-lift, gauge,
Monkhorst--Pack Fourier, twisted-Nyquist conversion, cubic-shell truncation,
withheld-evaluation, and first-passing channels at `8 x 8 x 8`, `16 x 16 x 16`, and
`32 x 32 x 32`. `DevelopmentVerifier` independently reconstructs selected parent and
band identities and checks stored numerical identities. Tensor FFTs, separable full
Fourier evaluation, and one-at-a-time complete-shell fields avoid dense global
cell--orbital and point-by-block phase matrices. Strict family-bound development schemas
and SHA-256 input/result binding cover all three levels.

This is software and bounded development evidence only. Complete Paper 1 calculation
parity and a formal convergence disposition remain open; these records are not an
immutable run or scientific validation. Final retained-record schemas, tolerances,
convergence actions, and retained serialization remain open.

It will call Numerics, PhysKit, and Optimization capabilities directly for their owned
Fourier, lattice-displacement, hopping, band, spectrum, Procrustes, harmonic, and
constrained-quadratic operations.

KSD owns the dimension-general directed-hopping parent, finite lattice/parent/retained
space declarations, basis ordering, projector and gauge identification, aligned-
subtraction ledger, coordinate-permutation and global-inversion covariance checks, the
48-element support-orbit group, dense attainable-shell inventory, three-plane Nyquist
conversion, sample roles, resource caps, scientific error channels, evidence, and
interpretation. The protocol fixes a publication-
independent 15-step prospective execution sequence. The verifier independently
reconstructs geometry, conversion, truncation correlation, and every first passing
sampled shell; immutable run and evidence-package creation remain separately authorized
operations.

Any production, remote, cluster, or cloud execution remains a protected operation and
requires separate authorization and resource preflight.
