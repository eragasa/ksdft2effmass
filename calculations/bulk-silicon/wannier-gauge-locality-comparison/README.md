# Silicon DFT–Wannier gauge and locality comparison

## Scientific question

For one explicitly identified silicon retained state space, how do the
Kohn–Sham-coordinate frame, the Wannier90 gauge, a controlled momentum-dependent
unitary attack, and an oracle pointwise recovery redistribute finite real-space
operator blocks without changing the underlying retained operator?

This calculation owner is a **prospective, non-executed protocol**. It does not report
numerical results and does not authorize Quantum ESPRESSO (QE), Wannier90, remote, or
production execution.

## Why this is separate from the synthetic rank-two control

The canonical Periodic1D composite-band calculation establishes the mechanism in a
bounded synthetic model: a momentum-dependent internal rotation can preserve the
retained projector and complete spectrum while changing finite hopping locality. This
silicon calculation is the material-facing follow-up. It must admit actual QE and
Wannier90 artifacts, physical units, a three-dimensional reciprocal mesh, and the
ultrasoft generalized-overlap boundary before interpreting the same mechanism.

The pointwise channel is an **oracle control**, not a replacement for Wannier90. If it
uses the Wannier90 frame as its target, recovery of that frame is true by construction
when the overlap is full rank. Such recovery can test implementation and gauge
sensitivity, but it cannot establish that pointwise Procrustes localization is better
than Wannier90's globally coupled spread optimization.

## Proposed comparison channels

The fixed-subspace comparison uses the following distinct channels at every admitted
reciprocal point:

1. **disentangled retained frame**: the Wannier90 isometry `U_dis` before its square
   gauge rotation;
2. **Wannier90 frame**: `U_dis @ U`;
3. **attacked frame**: a prospectively frozen analytic unitary acts on the right of the
   Wannier90 frame;
4. **pointwise oracle**: right-action Procrustes aligns the attacked frame back to the
   Wannier90 frame independently at each point; and
5. **one-global-unitary control**: one constant right action is fitted over the complete
   mesh.

For an entangled-band calculation, `U_dis` is already a Wannier90-selected retained
subspace. It must not be relabeled as the raw DFT eigenframe. A raw Kohn–Sham band group
may be added only as a separate subspace-selection channel after its dimension,
projector, generalized metric, and correspondence have been declared. Operator
subtraction is prohibited until the compared operators act on an identified common
state space.

## Operator inventory

Every admitted gauge channel is evaluated separately for the same-frame represented:

- retained Hamiltonian `H`;
- canonical kinetic operator `T`; and
- non-kinetic remainder `R = H - T`.

The remainder is not identified as a continuous scalar potential. The calculation
keeps operator role, physical energy unit, energy reference, lattice convention,
reciprocal mesh, state-space identity, and gauge identity explicit.

## Evidence boundary

A read-only silicon kinetic-decomposition prototype remains outside this scoped merge
in the divergent historical prototype worktree and is a prospective donor only. It
contains a rank-four `4 × 4 × 4` finite represented operator analysis, but it explicitly
does not establish authenticated prior production provenance, generalized-overlap
reconstruction, mesh convergence, or scientific validation. This protocol neither
admits those bytes nor reinterprets their reported 64-block truncation study.

Before implementation, the owner must inventory whether the admitted bytes include:

- ordered parent eigenvalues and reciprocal points;
- plane-wave coefficients and canonical kinetic energies;
- `U_dis` and `U` separately, not only their product;
- direct-lattice vectors and mesh ordering;
- Wannier90 spread and native interpolation records when used;
- ultrasoft overlap authority or an explicit limitation; and
- exact source identities and production provenance.

Missing information remains unavailable; it is not inferred from matrix dimensions,
filenames, or numerical agreement.

## Files

- [`protocol.md`](protocol.md): prospective state-space, channel, numerical,
  verification, and evidence protocol.

## Status and nonclaims

No calculation has been run for this comparison. No retained result, threshold decision,
Wannier90 superiority claim, localization guarantee, continuum convergence result,
uncertainty quantification, material validation, publication evidence, or release is
created here.
