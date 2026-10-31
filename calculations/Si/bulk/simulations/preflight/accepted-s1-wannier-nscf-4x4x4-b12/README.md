# Accepted-S1 first Wannier NSCF candidate preflight

This directory retains compact preflight material for the approved first
qualification candidate of the ten-spatial-orbital component-operator route.

- exact accepted S1 parent and authenticated SCF saved-state manifest;
- full unreduced Gamma-origin `4 x 4 x 4` grid;
- 64 equal-weight points in lexicographic `i,j,k` order with `k` fastest;
- symmetry and time-reversal reduction disabled;
- 12 scalar non-spin bands;
- 42/336 Ry cutoffs;
- fixed occupations;
- `cg` diagonalization with full accuracy and `1.0e-12 Ry` tolerance;
- target Wannier rank 10;
- `Si:sp3;l=0:r=2` trial-projection declaration;
- all 12 bands as the initial outer space, with no frozen inner window; and
- component-operator evidence profile.

The maintained ProjectKoios NSCF runner rendered [`pw.in`](pw.in) in dry-run mode and
verified that it exactly reproduces the approved source input. No calculator was
executed.

## Qualification boundary

The 4x4x4 density and 12-band inventory are first-candidate coordinates informed by
interface precedent. They are not accepted production adequacy. Grid, band, window,
interpolation, band-edge, derivative, and coefficient-transform sensitivity remain
future gates.

## Authorization state

Status: **authorization consumed by one occurrence**.

Exactly one `pw.x` NSCF invocation was performed with zero retries. Native execution
returned zero, but explicit `c_bands` diagnostics block downstream acceptance. Compact
evidence and disposition are retained under
[`../../evidence/sssp-1.3.0-pbe-efficiency-qe-7.5-accepted-s1-wannier-nscf-4x4x4-b12/`](../../evidence/sssp-1.3.0-pbe-efficiency-qe-7.5-accepted-s1-wannier-nscf-4x4x4-b12/).
No retry, Wannier90 preprocessing, `pw2wannier90.x`, or localization is authorized.
