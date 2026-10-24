# `ksdft2effmass.operators`

## Purpose and status

`ksdft2effmass.operators` owns KSD Hamiltonian wrappers, spectral subspaces,
compression, residual policy, operator records, and operator-matrix norms. Generic
real-symmetric spectral decomposition and eigensystem records belong to PhysKit;
KSD consumers use `projectkoios.physkit.linalg.eigen.SpectralDecomposition` and
`Eigensystem` directly. The retained KSD complex-Hermitian sparse solver boundary is
separate and does not imply PhysKit support for complex-Hermitian decomposition.
Immutable numerical quantities and matrix-property verification belong to
[`ksdft2effmass.linalg`](../linalg/index.md). Typed state-space and subspace contracts
are assigned prospectively to the separate [`spaces`](../spaces/index.md) owner rather
than added beneath `operators`.

The implemented `hamiltonians.py` module owns the general `Hamiltonian`, its exact
`HermitianHamiltonian` refinement, and `ReducedHamiltonian`. The reduced type binds a
reduced matrix to an abstract `SpectralSubspace` and a parent-coordinate `Hamiltonian`
embedding. The currently implemented `OrthogonalSpectralSubspace` owns the PIAB1D
orthonormal realization. Other
existing modules remain documented by their current source, tests, Sphinx pages, and
older architecture records until touched. This page does not replace those records.

## Ownership boundary

This package establishes finite operator values and operations on already identified
spaces. It does not select a physical model, analytical states, retained dimension,
diagnostic list, parameter sweep, norm interpretation, or scientific acceptance
threshold.

## Dependency rules

`operators` consumes immutable quantities from `ksdft2effmass.linalg` and exact
PhysKit eigensystems for real-symmetric spectral selection; `linalg` must not depend on
`operators`. The prospective `spaces` owner may consume immutable
linear-algebra quantities. `operators` must not depend on `analysis`, model systems,
experiments, calculations, serializers, plotting, or provenance owners.

## Evidence and limitations

Focused tests cover Hermitian refinement, spectral-subspace substitution, and
`ReducedHamiltonian` shape and retention invariants. Matrix-property evidence belongs
to `ksdft2effmass.linalg`. That software
evidence does not establish adequacy of any selected retained space or model.
