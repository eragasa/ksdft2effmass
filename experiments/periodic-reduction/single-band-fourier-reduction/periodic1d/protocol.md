# Immutable experiment version `v1`

## Identity

- Family: `ksdft2effmass.campaign.periodic-reduction.periodic1d.single-band-fourier-reduction`
- Version: `ksdft2effmass.campaign.periodic-reduction.periodic1d.single-band-fourier-reduction.v1`
- Historical publication alias: `M1`
- Evidence class: controlled local synthetic numerical verification

Version `v1` freezes the historical M1 model and discretization controls while adding
positive fitting weights, explicit objective-construction and evaluation roles,
caller-selected hopping ranges, sampled external-gap diagnostics, typed immutable
records, owner API composition, canonical strict-schema serialization, and a
producer-independent reconstruction route.

## Mathematical conventions

The parent is

\[
H(k)=-\frac{d^2}{dx^2}+0.5\cos x,\qquad a=2\pi,\quad G=1,\quad E_G=1.
\]

All quantities are dimensionless. The energy reference is the fixed parent-model zero;
no post-fit energy shift is admitted. Reduced momentum is `k/G` in one reciprocal
period. The complete transform uses

\[
t_R=N^{-1}\sum_j e^{-2\pi i R k_j/G}E(k_j),\qquad
E(k)=\sum_R e^{+2\pi i R k/G}t_R.
\]

The forward transform alone carries `1/N`. The training role is the complete 64-point
centered half-open mesh. The evaluation role is the disjoint 257-point staggered mesh
`-1/2 + (i + 1/65)/257`. Evaluation cannot update coefficients, ranges, weights, or
tolerances.

## Frozen controls

- plane-wave sweep: `3, 5, 7, 9, 11`;
- finite represented plane-wave reference: `15`;
- production plane-wave cutoff: `11`;
- finite-difference grids: `31, 63, 127, 255`;
- parent coordinates: `-1/2, -1/4, 0, 1/4, 1/2`;
- compared parent bands: lowest three ordered bands;
- selected band: zero-based band `0`;
- hopping ranges: `0, 1, 2, 3, 4, 6, 8`;
- direct-fit weights: 64 strictly positive unit weights;
- coordinate tolerance: `1e-14`;
- reconstruction, Hermiticity, Parseval, and imaginary tolerances: `1e-12` in
  their declared units.

The sampled training and evaluation external gaps are diagnostics. A positive sampled
gap is not a continuum isolation certificate. No range is scientifically accepted.

## Verification and failure policy

The independent verifier must not call `SingleBandFourierReductionExperiment` or
`SingleBandHoppingReductionWorkflow1D`. It directly reconstructs parent matrices,
spectra, band selection, sampled gaps, Fourier coefficients, interpolation, weighted
least squares, rank, conditioning, route defects, omitted-block locality, Parseval,
Hermiticity, bandwidth, curvature, and imaginary residuals.

A retained run passes only when strict structure checks pass and both energy and
squared-energy reconstruction defects are within their frozen tolerances. A failed
producer, schema validation, digest check, or independent verification is retained as
a failed attempt only if explicitly labeled; it must not replace publication evidence.
Passing establishes bounded software and finite-protocol numerical consistency only.

## Historical predecessor

The exact predecessor locator is Git revision
`9a65849d886d5be499b2664e2b653c3983fab06e`, path
`calculations/ICMSEP2026/conference/paper_1/isolated-band/`, Git tree
`418999a90efa3001d2e50a2e7912f126bc30903f`, with historical `input.json`,
`result.json`, `verification.json`, and `SHA256SUMS` SHA-256 digests retained in each
successor run's `provenance.json`. Historical files are not modified.
