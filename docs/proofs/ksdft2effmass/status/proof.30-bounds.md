# PRF-30: Bounds

[Proof registry](../proof-status.md) · Depends on applicable parts of [PRF-10](proof.10-operator-alignment.md) and [PRF-20](proof.20-reduction.md)

## Status

`proposed`: candidate residual, perturbation, and existence bounds are recorded, but their hypotheses and usefulness for the target systems remain unproved.

## Objective

Convert representation-controlled operator residuals into well-posed crossover criteria, spectral or eigenspace error statements, and continuum-parameter existence or identifiability results.

## Authority and prerequisites

- `PRF-10.03` aligned impurity operator.
- `PRF-20.01` gauge-constrained locality.
- `PRF-20.03` atomistic-to-continuum comparison.
- Declared norms, projectors, tolerances, spectral windows, and target observables.

## Decomposition

| ID | Obligation | Status | Prerequisites | Owner |
|---|---|---|---|---|
| `PRF-30.01` | Prove the spatial residual properties and define a tolerance-dependent crossover radius with correct existence or attainment language. | `proposed` | `PRF-20.01`, `PRF-20.03` | [Spatial residual and crossover](../bounds/spatial-residual-and-crossover.md) |
| `PRF-30.02` | Derive spectral, binding-energy, and invariant-subspace bounds from declared operator perturbations and spectral gaps. | `proposed` | `PRF-10.03`; relevant reduced operator from `PRF-20` | [Operator-to-observable errors](../bounds/operator-to-observable-errors.md) |
| `PRF-30.03` | Establish existence of continuum fits and separate it from uniqueness, stability, and physical identifiability. | `proposed` | `PRF-20.03`, `PRF-30.01` | [Continuum fitting and identifiability](../bounds/continuum-fitting-identifiability.md) |

## Completion criteria

- Every bound identifies its norm, finite or infinite state space, and tolerance.
- Crossover existence is distinguished from attainment and from numerical estimation.
- Eigenspace bounds use invariant subspaces where degeneracy makes individual eigenvectors non-identifiable.
- Parent-model, discretization, excluded-space, and reduction errors remain separate.
- Identifiability requires more than existence of a minimizer and includes a declared stability criterion.

## Exclusions

- A worst-case operator bound is not represented as sharp without evidence.
- A small spectral error is not treated as a small operator error.
- Numerical agreement does not replace the proof of the stated inequality.
