# `ksdft2effmass.hamiltonian.records`

## Purpose and status

This implemented module owns typed finite Hamiltonian representations.

Source: `python/src/ksdft2effmass/hamiltonian/records.py`.

## Contracts

`Hamiltonian` owns one nonempty square real or complex dense or sparse PhysKit matrix
quantity with explicit units. It does not assume Hermiticity.

`HermitianHamiltonian` refines `Hamiltonian`. Direct construction and
`from_hamiltonian()` use PhysKit `MatrixVerifier` with zero relative and absolute
tolerances and preserve the matrix quantity unchanged.

`ReducedHamiltonian` binds:

- its inherited reduced-coordinate matrix;
- one `SpectralSubspace` that defines the retained coordinates; and
- one parent-coordinate embedded `Hamiltonian`.

Construction checks types, units, and dimensions. It does not infer a coordinate map,
perform reduction, or impose tolerance-dependent acceptance.

## Ownership boundary

PhysKit owns generic quantities and matrix verification. KSD owns the Hamiltonian
meaning, the reduction correlation, and outward acceptance policy. Consumers import
PhysKit objects directly; KSD defines no generic linear-algebra compatibility layer.

Numerical construction belongs to `SpectralReduction`. Model systems own why a
spectral space and dimension are selected.

## Evidence

Focused tests establish construction, exact-Hermitian refinement, abstract subspace
substitution, and reduced/embedded shape and unit invariants. They do not establish
physical adequacy of a retained Hamiltonian.
