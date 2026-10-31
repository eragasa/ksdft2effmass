# Accepted-S1 revised Davidson NSCF candidate preflight

This directory retains the dry-run preflight for a revised NSCF qualification
candidate. It responds to the first occurrence's 41 `c_bands` warnings covering 44
unconverged eigenvalues.

The candidate preserves the accepted structure, authenticated parent SCF lineage,
full Gamma-origin `4 x 4 x 4` grid, 64-point ordering, 12 bands, 42/336 Ry cutoffs,
fixed occupations, rank-10 target, projection declaration, outer-space policy, and
`1.0e-12 Ry` tolerance. The sole intended numerical change is:

- `diagonalization = 'cg'` → `diagonalization = 'david'`.

Full diagonalization accuracy remains enabled. The maintained ProjectKoios runner
rendered [`pw.in`](pw.in) in dry-run mode and reproduced the approved source input
exactly. No calculator was executed.

## Authorization state

Status: **authorization consumed by one occurrence**.

Exactly one single-process `pw.x` NSCF invocation was performed with zero retries. It
returned zero, printed `JOB DONE`, produced consistent finite 64-point/12-band QEXSD
data, and emitted no `c_bands` unconverged-eigenvalue diagnostics. Compact evidence is
retained under
[`../../evidence/sssp-1.3.0-pbe-efficiency-qe-7.5-accepted-s1-wannier-nscf-4x4x4-b12-david/`](../../evidence/sssp-1.3.0-pbe-efficiency-qe-7.5-accepted-s1-wannier-nscf-4x4x4-b12-david/).

The occurrence is an eligible candidate handoff, not production acceptance. It does
not authorize Wannier90 preprocessing, `pw2wannier90.x`, localization, or any retry.
