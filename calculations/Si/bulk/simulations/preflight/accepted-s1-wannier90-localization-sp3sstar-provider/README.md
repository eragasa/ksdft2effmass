# Accepted-S1 first provider-backed Wannier90 localization preflight

This directory retains the exact ProjectKoios-provider preflight for the first rank-10
Wannier90 localization candidate. No localization process has been started.

## Provider boundary

ProjectKoios now implements the first rank-reducing ordinary non-spin AMN/MMN profile.
Its pure preparer authenticates and correlates the closed input inventory without
resolving an executable. Its runner verifies the exact manifest and executable before
creating a fresh output directory, requires explicit execution authorization, invokes
the generic single-attempt executor at most once, and retains provider failures
separately from process status.

The bounded implementation review found no blocking defect after adding unique-physical
input checks, source/output separation, durable output-emission failures, lineage
hashes, exact executable identity, and native output correlation.

Software checks:

- full test suite: 692 passed, 7 skipped, 202 subtests passed;
- focused localization tests: 5 passed;
- Ruff and focused MyPy: passed;
- wheel build: passed;
- full MyPy remains blocked by two pre-existing `preprocessing.py` findings caused by
  the installed PhysKit export mismatch.

These checks establish software behavior only, not scientific adequacy.

## Closed input

The provider-generated manifest binds exactly WIN, NNKP, EIG, AMN, and MMN—five files,
3,321,145 bytes—plus exact preprocessing and converter-result SHA-256 identities. UNK
and SPN are excluded. Dimensions are 64 k points, 12 bands, rank 10, and eight neighbors
per point. The exact prepared WIN retains both gauge and disentanglement matrices.

Manifest SHA-256:
`3066ec192ace13bd5daee88d3c14367eef5d1c2d27021ce7335332dd5776387a`.

## Bounded request

The proposed single command is:

```text
/Users/eugene/projects/wannier90-3.1.0/wannier90.x silicon
```

The Wannier90 3.1.0 executable is 891,048 bytes with SHA-256
`c826f817f807cf069e16d6e529a52ddc15d2f677101065908bcb2030d7f7d1dd`.
Bounds are one process, 300 seconds, 64 MiB retained bytes, zero retries, and stop on
failure.

Required selected outputs are `silicon.wout`, `silicon_hr.dat`, `silicon_u.mat`, and
`silicon_u_dis.mat`. Eligibility requires return code zero; explicit disentanglement,
Wannierisation, and native completion messages; no maximum-iteration warning; bounded
finite parsing; exact dimensions and k-point order; gauge/isometry residual at most
`1.0e-8`; and real-space Hamiltonian Hermiticity residual at most `1.0e-8 eV`.

Status: **authorization consumed; occurrence blocked without retry**.

Exactly one invocation returned zero and native completion, but disentanglement reached
200 iterations with an explicit nonconvergence warning and Wannierisation reached 100
iterations without satisfying its convergence criterion. Provider disposition is
`output-ineligible`. Evidence is retained under
[`../../evidence/sssp-1.3.0-pbe-efficiency-qe-7.5-accepted-s1-wannier90-localization-sp3sstar-blocked/`](../../evidence/sssp-1.3.0-pbe-efficiency-qe-7.5-accepted-s1-wannier90-localization-sp3sstar-blocked/).

No retry, interpolation, component-operator acceptance, Slater–Koster fitting, commit,
or push is authorized.
