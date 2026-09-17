# Wannier90 comparison preflight

## Status and authority

This preflight governs the local Wannier90 comparison authorized by the human
instruction preserved verbatim as `ok let's do the wannier90` in checkpoint
`RM-PERIODIC-1D-W90-RUN-HC01`. It does not authorize Quantum ESPRESSO,
material-specific inputs, remote execution, dependency changes, or production
claims.

## Executable

- Command: `/Users/eugene/.local/bin/wannier90.x`
- Reported version: Wannier90 3.1.0
- Installed executable identity documented in
  `docs/computational/wannier90-3.1.0-installation.md`
- Invocation mode: one local process, no MPI launcher

The version probe exits successfully and emits the installation's previously
documented `IEEE_OVERFLOW_FLAG` notice. The scientific run must retain stderr so
that the notice and any input-specific diagnostics remain visible.

## Input system

The source states are synthetic plane-wave eigenvectors of

$$
\hat H=-\frac{\hbar^2}{2m}\frac{d^2}{dx^2}+V_0\cos(Gx)
$$

with $a=2\pi$, $G=1$, $E_G=1$, $V_0/E_G=0.5$, reciprocal cutoff $P=15$, and a
uniform $128\times1\times1$ mesh. Two independent seeds retain exactly two
bands and two Wannier functions:

- `low_pair`: energy-ordered bands 0--1;
- `higher_pair`: energy-ordered bands 2--3.

No disentanglement is used. The interface generator owns the `.win`, `.eig`,
`.mmn`, and `.amn` files. It must derive neighbor overlaps from the same parent
states and exact reciprocal sewing used by the direct composite calculation.
Identity trial projections in the retained eigenbasis provide the initial
`.amn` matrices; this is an explicit numerical convention rather than a
material-orbital claim.

## Scale and resource envelope

Each seed has two bands, two Wannier functions, 128 reciprocal points, and a
$31$-component plane-wave parent basis. Expected execution is seconds to a few
minutes per preprocessing/localization stage, one local process, less than
512 MiB memory, and less than 50 MiB total new output. More than five minutes,
512 MiB resident memory, or 50 MiB output is outside this authorization and
requires stopping and reporting.

## Commands and anticipated outputs

For each seed, the authorized stages are:

```text
wannier90.x -pp <seed>
wannier90.x <seed>
```

Anticipated interface and native outputs include `.nnkp`, `.wout`, `.chk`,
centers and spreads, unitary matrices where exposed, interpolated eigenvalues,
and real-space Hamiltonian blocks. Native and scratch outputs remain in an
external run directory. The repository retains only sanitized textual inputs,
compact manifests, checksums, extracted comparison results, plots, and the
mini-paper update.

## Stop conditions

Stop without retry if either seed reports malformed interface data, nonfinite
values, a localization failure, resource-envelope exceedance, or an input choice
that would require changing the frozen parent, mesh, rank, projections,
convergence settings, or symmetry policy. Successful execution establishes only
an independently implemented localization result for this illustrative model;
it does not establish scientific validation or human acceptance.

## First preprocessing attempt

The authorized first `low_pair` preprocessing invocation exited with code 1
after 0.15 seconds and a measured maximum resident size of 21,954,560 bytes.
Wannier90 could not satisfy its three-dimensional B1 finite-difference condition
within the default first 36 reciprocal shells for the $128\times1\times1$ mesh
and suggested increasing `search_shells`. No `.nnkp` file was created; the
higher-pair preprocessing and both localization stages were not attempted.

This is an input-embedding preprocessing failure, not a localization result.
The exact attempt is recorded in `wannier90-attempt.json`. Because the resolved
checkpoint prohibited retrying a failed scientific stage, no automatic retry
was made. Checkpoint `RM-PERIODIC-1D-W90-RETRY-HC02` subsequently authorized the bounded
`search_shells = 130` correction while leaving the parent, mesh, bands,
projections, overlap convention, localization settings, and resource envelope
unchanged. Both corrected preprocessing stages completed and both localization
stages exited successfully. Neither localization met the frozen $10^{-12}$
spread convergence criterion within 500 iterations. The process facts and
nonconverged result are retained separately in `wannier90-execution.json` and
`wannier90-result.json`. A later iteration-only study also failed for the low
pair. Read-only diagnosis then identified the documented preconditioner as the
smallest objective-preserving remedy. Checkpoint
`RM-PERIODIC-1D-W90-PRECONDITIONED-HC06` authorized fresh runs adding only
`precond = true`; both pairs satisfied the unchanged convergence rule. Their
process and comparison records are `wannier90-preconditioned-execution.json`
and `wannier90-preconditioned-result.json`.
