# `solidstate/hamiltonians/effective/lowdinquadratic`

## Responsibility

This package owns a finite selected-space Löwdin quadratic effective Hamiltonian built
from same-frame Cartesian derivatives of represented Hamiltonian, canonical kinetic,
and non-kinetic-remainder operators. Reduction, polynomial evaluation, and directional
contraction remain separate Actions and each evaluates its request once.

Python implementation:
`ksdft2effmass.solid_state.hamiltonians.effective.lowdin_quadratic`.

The package does not select a physical manifold, infer degeneracy, track scalar bands,
convert curvature to mass, establish convergence, or validate physical adequacy.

## Modules

- `reduction.py`: selected/complementary frames, Löwdin resolvent, projected tensors,
  remote-state correction, decomposition, and intrinsic diagnostics;
- `evaluation.py`: evaluation at explicit Cartesian reciprocal offsets;
- `contraction.py`: contraction of the quadratic tensor along explicit
  directions;
- `diagnostics.py`: intrinsic finite-array norms shared by Actions and Result
  validation; it performs no eigensolve or request-to-reduction derivation.

## Scientific reference and claim boundary

The name follows Per-Olov Löwdin, “A Note on the Quantum-Mechanical Perturbation
Theory,” *The Journal of Chemical Physics* 19(11), 1396–1401 (1951),
[doi:10.1063/1.1748067](https://doi.org/10.1063/1.1748067). The bibliographic metadata
was checked against the Crossref DOI record on 2026-10-07. The citation establishes the
provenance of the class-partition construction; it does not validate this package's
finite derivative convention, tolerances, decomposition, or material interpretation.

The authoritative mathematical contract and full citation provenance are in
[`ksdft2Effmass.lowdin-quadratic-effective-hamiltonian.v1.md`](../../../../../../../../specification/ksdft2Effmass.lowdin-quadratic-effective-hamiltonian.v1.md).
