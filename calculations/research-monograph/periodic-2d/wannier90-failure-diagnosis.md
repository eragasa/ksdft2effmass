# Periodic-2D Wannier90 preprocessing failure diagnosis

## Retained failure

The single attempt authorized by
`RM-PERIODIC-2D-WANNIER90-EXECUTION-HC02` stopped during preprocessing:

```text
kmesh_get: something wrong, found too many nearest neighbours
```

The process exited with code 1 after 0.31 s. Maximum resident memory was
22,118,400 bytes and external output was 302,287 bytes, both below the frozen
limits. Wannier90 did not emit `low_triple.nnkp`; therefore the `.mmn` interface
was not generated and localization was not started. No retry occurred.

## Diagnosis

The active reciprocal mesh is $15\times15$, but the frozen `.win` embedded it
in a unit cubic cell with a one-point inactive third direction. The active
neighbor increment has magnitude $2\pi/15$, whereas the first inactive-direction
reciprocal vector has magnitude $2\pi$. Wannier90 3.1.0 constructs a
three-dimensional finite-difference stencil satisfying reciprocal-space
completeness. Before it reaches the inactive-direction vector, it encounters
many shorter in-plane shells. The resulting selected shell multiplicity exceeds
the compiled `num_nnmax = 12` limit and preprocessing stops.

This is an interface-embedding failure, not a failed spread minimization or a
result about localization. The evidence is:

- the tail of `low_triple.wout` enumerates 1,430 candidate vectors before the
  stop;
- the final diagnostic is emitted by `kmesh.F90` when the selected neighbor
  count exceeds `num_nnmax`;
- no `.nnkp` exists; and
- the parent spectrum, rank-three projection, and direct composite calculation
  were not reevaluated by the failed stage.

## Candidate corrections

### A. Balanced inactive lattice length (recommended)

Set the inactive direct-lattice length to 15 while retaining the active unit
cell and the $15\times15\times1$ mesh. Then the inactive reciprocal increment
is $2\pi/15$, equal in magnitude to the active increments. The automatic
three-dimensional stencil is expected to use the six axial neighbors without
encountering the multiplicity limit. The inactive overlap remains the declared
unit transverse form factor.

This changes only the auxiliary three-dimensional embedding used by Wannier90.
Active-plane parent energies, projections, boundary sewing, and direct
composite evidence remain unchanged. Any reported three-dimensional spread must
be decomposed so that only active-plane centers and spreads are compared.

### B. Explicit developer shell selection

Retain the unit cubic embedding but use Wannier90's `devel_flag=kmesh_degen`
and an explicit `.kshell` file to choose a bounded stencil. This preserves the
old cell but introduces a developer-mode shell policy that must be specified and
verified independently.

### C. No retry

Retain the preprocessing failure as the final independent-Wannier90 evidence.
No external localization comparison would be available.

A correction is a new protected attempt and requires a new human checkpoint.
The existing authorization does not permit a retry.
