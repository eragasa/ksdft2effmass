# Accepted-S1 first Wannier90 localization prepared input

This directory retains the exact prepared-input declaration for the first rank-10
Wannier90 localization candidate. No localization process has been started.

## Closed input inventory

The ordinary non-spin AMN/MMN route contains exactly:

- `silicon.win`, derived from the authenticated preprocessing WIN by adding only
  `write_u_matrices = .true.`;
- the verified 64-point, eight-neighbor `silicon.nnkp` topology;
- the authenticated 64-point/12-band `silicon.eig` table;
- the authenticated 64-point/12-band/rank-10 `silicon.amn` projections; and
- the authenticated 64-point/eight-neighbor/12-band `silicon.mmn` overlaps.

UNK and SPN are neither required nor staged. The output-only WIN change retains the
square gauge and rectangular disentanglement matrices required by the declared
12-band-to-rank-10 construction. It changes no structure, mesh, projections, windows,
or convergence controls and does not require another preprocessing invocation.

The closed inventory is 3,321,145 bytes. The exact prepared WIN is 3,563 bytes,
SHA-256 `4ba2e6642eb831eebd58d59e37b7d9c1035b246cd96e65593394014222b8395a`.

## Candidate occurrence

The prospective process would be exactly:

```text
/Users/eugene/projects/wannier90-3.1.0/wannier90.x silicon
```

Executable SHA-256:
`c826f817f807cf069e16d6e529a52ddc15d2f677101065908bcb2030d7f7d1dd`.

Prospective bounds are one process, 300 seconds, 64 MiB retained bytes, zero retries,
and stop on failure. Required selected outputs are `silicon.wout`, `silicon_hr.dat`,
`silicon_u.mat`, and `silicon_u_dis.mat`.

Mechanical eligibility would require native return code zero, explicit
disentanglement and Wannierisation convergence messages, no maximum-iteration
warning, finite bounded parser results, exact 64-point/12-band/rank-10 dimensions,
ordered k-point correlation, gauge/isometry checks, and real-space Hamiltonian
Hermiticity checks. It would not establish interpolation or operator adequacy.

## Blocker

Status: **superseded without execution**.

This preparation correctly identified that no reviewed provider boundary existed at
the time. ProjectKoios now implements the first rank-reducing localization provider,
and the provider-generated successor preflight is retained under
[`../accepted-s1-wannier90-localization-sp3sstar-provider/`](../accepted-s1-wannier90-localization-sp3sstar-provider/).

No calculator, retry, or successor stage was authorized or executed through this
superseded record.
