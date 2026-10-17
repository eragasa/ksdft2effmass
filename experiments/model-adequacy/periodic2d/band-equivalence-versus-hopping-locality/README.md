# Band Equivalence versus Hopping Locality in 2-D

## Identity and status

This directory is the prospective experiment home for

```text
ksdft2effmass.campaign.model-adequacy.periodic2d.band-equivalence-versus-hopping-locality
```

It is a dimension-specific successor to the maintained 1-D experiment. It is not a
version, run, evidence package, or publication identity. A foundational shared KSD
implementation now covers the dimension-general parent, sine rotation, analytic flat
correlation, dense square-shell inventory, and a bounded development action. A verified
three-level `16 x 16`, `32 x 32`, and `64 x 64` Monkhorst--Pack calculations exist under [`analysis/development/`](analysis/development/) and
[`analysis/development-refinement/`](analysis/development-refinement/). They are
replaceable development output, not a frozen run, convergence result, or scientific
evidence. Family-owned vector PDF and 600-dpi PNG diagnostics are cataloged in
[`analysis/README.md`](analysis/README.md).

Its dimension-general equations reduce exactly to the maintained parent homotopy and
sine rotation when `d = 1`. Matrices, parameter meanings, retained rank, alignment
restriction, and existing matrix/spectral error semantics are preserved; only dimension-specific
geometry and numerics change. The reconstructed-Hamiltonian channels now exist in the
1-D development implementation, but their dimension-general owner contracts and $d=1$
specialization fixtures must be reviewed before 2-D can inherit them.

The scientific system is a square-lattice synthetic rank-two retained Hamiltonian
obtained from an exact four-state parent. The finite parent is stated explicitly on
`(C^N)^(tensor 2) tensor C^4`: Kronecker translation operators construct the cell--orbital
Hamiltonian, the tensor Fourier transform gives its complete Bloch representation, and
a qualified retained frame gives the complete Wannier/TB representation. Eigenvalue
lists are never used as Hamiltonian operands. The fields preserve coordinate exchange
and global-inversion covariance. Signed-permutation-complete cutoff support does not
imply equality of hopping coefficients across an orbit or continuous rotational
symmetry.

## Selected development design

The prospective protocol selects:

- the direct axis-permutation-symmetric extension of the 1-D four-state directed-hopping parent;
- an explicit Kronecker lattice construction with four, not sixteen, orbitals per cell;
- exact unitary relations among the cell--orbital, Bloch, retained-frame, and Wannier/TB
  representations;
- the two lowest bands in a qualified periodic rank-two retained frame;
- the smooth representation family that mirrors the 1-D sine rotation,
  `U_a(q) = R(a*[sin(2*pi*q_x)+sin(2*pi*q_y)]/2)`, with
  `0 <= a <= pi/4`;
- the analytic flat-parent correlation `J_0(a)^2`;
- complete square signed-permutation displacement orbits ordered by squared radius;
- a dense inventory containing every attainable shell through the declared cap;
- equal-accuracy comparisons based on first passing sampled shells and retained block
  counts; and
- explicit projector lifts and aligned Hamiltonian-subtraction contracts; and
- separate parent--retained reconstruction, covariant-equivalence, restricted-alignment,
  cyclic-Nyquist conversion, reconstructed-Hamiltonian interpolation, deliberate
  truncation, total matrix-error, and corresponding spectral-error channels.

The exact parent, mathematical conventions, draft sampling design, qualification gates,
open controls, and publication-independent 15-step execution/verification sequence are
stated in [`experimental-protocol.tex`](experimental-protocol.tex). The sequence uses
2-D tensor meshes, square-orbit shells, and the two-line Nyquist union; it does not copy
1-D numerical outcomes.

## Relationship to other experiments

This family is distinct from:

- the 1-D band-equivalence experiment;
- the scalar 2-D hopping-shell hierarchy; and
- the orthogonal 3-D and non-orthogonal 2-D/3-D band-equivalence families.

It may reuse reviewed lattice and orbit capabilities directly from their owners, but it
does not inherit another experiment's thresholds, runs, evidence, or interpretation.

## Cross-family parity

Implementation and analysis must satisfy the shared
[test and diagnostic parity contract](../../band-equivalence-test-and-diagnostic-parity.md),
including comparable frame, alignment, locality, matrix/spectral consequence,
first-passing-shell, convergence, and verifier diagnostics.

## Current boundary

The protocol remains pre-version despite the bounded three-level development ladder
under [`analysis/development-refinement/`](analysis/development-refinement/). The mesh
points, shell cap, and thresholds are development controls rather than qualified
scientific controls. Row-level Paper 1 parity verification, formal convergence
disposition, final retained-record schemas, certified tolerances,
exact owner revisions, and evidence retention remain open. No calculation may be
described as retained or publication evidence until those controls are frozen and a
separately authorized run is completed.
