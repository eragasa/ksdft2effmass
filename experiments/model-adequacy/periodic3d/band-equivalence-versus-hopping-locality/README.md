# Band Equivalence versus Hopping Locality in 3-D

## Identity and status

This directory is the prospective experiment home for

```text
ksdft2effmass.campaign.model-adequacy.periodic3d.band-equivalence-versus-hopping-locality
```

It is a dimension-specific simple-cubic successor to the 1-D experiment and is
sequenced after review of the square-lattice 2-D protocol. It is not a version, run,
evidence package, or publication identity. A foundational shared KSD implementation now
covers the dimension-general parent, sine rotation, analytic flat correlation, dense
cubic-shell inventory, and a bounded development action. Resource-preflighted,
independently verified `8 x 8 x 8`, `16 x 16 x 16`, and `32 x 32 x 32`
Monkhorst--Pack development composition and plots are maintained by the
[calculation owner](../../../../calculations/periodic3d/rank2/orthogonal/band-equivalence-locality/);
they are neither convergence nor retained evidence. This experiment directory retains
the prospective protocol and bibliography rather than a second executable composition.

Its dimension-general equations reduce exactly to the maintained parent homotopy and
sine rotation when `d = 1`. Matrices, parameter meanings, retained rank, alignment
restriction, and existing matrix/spectral error semantics are preserved; only dimension-specific
geometry, periodic-frame construction, and numerics change. The reconstructed-
Hamiltonian channels exist in the 1-D development implementation; 3-D inherits them only
after the 2-D stage establishes the dimension-general owner contracts.

The scientific system is a simple-cubic-lattice synthetic rank-two retained Hamiltonian
obtained from an exact four-state parent. The finite parent is stated on
`(C^N)^(tensor 3) tensor C^4`: Kronecker translation operators construct the cell--orbital
Hamiltonian, the tensor Fourier transform gives its complete Bloch representation, and
a qualified retained frame gives the complete Wannier/TB representation. Eigenvalue
lists are never used as Hamiltonian operands. The fields preserve coordinate
permutations and global-inversion covariance. Signed-permutation-complete cutoff support
does not imply equality of hopping coefficients across an orbit or a cubic material
model.

## Selected development design

The prospective protocol selects:

- the direct axis-permutation-symmetric extension of the 1-D four-state directed-hopping parent;
- an explicit Kronecker lattice construction with four, not sixty-four, orbitals per cell;
- exact unitary relations among the cell--orbital, Bloch, retained-frame, and Wannier/TB
  representations;
- the two lowest bands in a qualified periodic rank-two retained frame;
- the smooth representation family that mirrors the 1-D sine rotation,
  `U_a(q) = R(a*sum_alpha sin(2*pi*q_alpha)/3)`, with
  `0 <= a <= pi/4`;
- the analytic flat-parent correlation `J_0(2*a/3)^3`;
- complete cubic signed-permutation displacement orbits ordered by squared radius;
- a dense inventory containing every attainable shell through the declared cap;
- equal-accuracy comparisons based on first passing sampled shells and retained block
  counts; and
- explicit projector lifts and aligned Hamiltonian-subtraction contracts; and
- separate parent--retained reconstruction, covariant-equivalence, restricted-alignment,
  cyclic-Nyquist conversion, reconstructed-Hamiltonian interpolation, deliberate
  truncation, total matrix-error, and corresponding spectral-error channels.

The exact parent, mathematical conventions, resource-aware draft sampling design,
qualification gates, open controls, and publication-independent 15-step
execution/verification sequence are stated in
[`experimental-protocol.tex`](experimental-protocol.tex). The sequence uses 3-D tensor
meshes, cubic-orbit shells, and the three-plane Nyquist union; it does not copy lower-
dimensional numerical outcomes.

## Sequencing gate

The completed bounded stages used explicit local resource preflights and matrix-free
tensor execution through the Numerics owner contracts. The `N=32` development action remained below about 760 MB peak memory. This
does not authorize a larger, remote, production, or retained execution, each of which
still requires its applicable resource review and authorization.

## Relationship to other experiments

This family is distinct from:

- the 1-D and 2-D band-equivalence experiments;
- the scalar isotropic 3-D hopping-support hierarchy; and
- every non-orthogonal, anisotropic, or material-specific family.

It may reuse reviewed cubic lattice and orbit capabilities directly from their owners,
but it does not inherit another experiment's thresholds, runs, evidence, or
interpretation.

## Cross-family parity

Implementation and analysis must satisfy the shared
[test and diagnostic parity contract](../../band-equivalence-test-and-diagnostic-parity.md),
including comparable frame, alignment, locality, matrix/spectral consequence,
first-passing-shell, convergence, resource, and verifier diagnostics.

## Current boundary

The protocol remains pre-version despite the bounded three-level ladder owned by the
calculation composition. The mesh points,
shell cap, thresholds, and resource envelopes are development controls. Row-level Paper
1 software parity is complete for every applicable or explicitly inapplicable catalog
quantity, including independent finite-sum reconstruction; this does not establish a
formal convergence disposition or scientific acceptance. Final retained-record schemas
and tolerances, frozen revisions, and evidence
retention.
No
calculation may be described as retained or publication evidence until those controls
are frozen and a separately authorized run is completed.

## Distributed migration ledger

The complete cross-surface inventory and authoritative checklist are maintained with the
calculation owner in
[`calculations/periodic3d/rank2/orthogonal/band-equivalence-locality/README.md`](../../../../calculations/periodic3d/rank2/orthogonal/band-equivalence-locality/README.md)
and [`migration.md`](../../../../calculations/periodic3d/rank2/orthogonal/band-equivalence-locality/migration.md).
