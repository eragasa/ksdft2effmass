# `ksdft2effmass.hamiltonian`

## Purpose and status

This implemented package owns KSD Hamiltonian representations, retained spectral
spaces, spectral reduction, reduction diagnostics, and decomposition of an already
represented Hamiltonian.

Source package: `python/src/ksdft2effmass/hamiltonian/`.

## Source mapping

```text
hamiltonian/
├── __init__.py
├── records.py
├── subspaces.py
├── reduction.py
├── residuals.py
└── decomposition.py
```

- `records.py` owns `Hamiltonian`, `HermitianHamiltonian`, and
  `ReducedHamiltonian`.
- `subspaces.py` owns the explicit coordinate reduction and embedding contract,
  its orthogonal spectral implementation, and retained-eigenpair selection.
- `reduction.py` owns `SpectralReduction`.
- `residuals.py` owns orthogonal spectral-reduction residual meanings.
- `decomposition.py` owns `HamiltonianDecomposition` and its internal stage records.

All listed domain objects are exported deliberately by
`ksdft2effmass.hamiltonian`. They are not re-exported through
`ksdft2effmass.operators`.

## External ownership

Generic quantities, unit conversion, matrix verification, eigensystems, and
real-symmetric spectral decomposition belong to PhysKit. KSD imports their canonical
objects directly from `projectkoios.physkit`; no `ksdft2effmass.linalg` package,
compatibility alias, wrapper, or re-export exists.

## Ownership boundary

A generic mathematical subspace would belong to PhysKit. The KSD
`SpectralSubspace` instead owns the coordinate maps needed to form a correlated
`ReducedHamiltonian`; it therefore belongs to the Hamiltonian-reduction domain.
A projector alone does not define reduced coordinates.

The package does not select a physical model, infer a retained dimension, construct a
Kohn--Sham parent, set residual acceptance, or establish scientific adequacy.
Model-specific composition supplies the represented parent and selection policy.

## Evidence

Focused tests cover dense and sparse parent representations, real and complex
Hamiltonians, orthogonal and explicit oblique coordinate maps, exact Hermitian
refinement, reduction residual meanings, and PIAB1D composition. These are software
and bounded numerical checks, not scientific validation or acceptance.
