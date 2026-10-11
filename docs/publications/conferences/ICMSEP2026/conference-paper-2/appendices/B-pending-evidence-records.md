# Appendix B. Pending Evidence Records

These tables are intentionally incomplete. `Pending` and `Not evaluated` are status
values, not implied numerical results.

## Parent and Wannier qualification

| Evidence group | Required contents | Status |
|---|---|---|
| Parent identity | Lattice, executable, pseudopotential hash, physical branch | Not evaluated |
| Numerical convergence | Cutoffs, mesh, fixed bands, gap, valley, masses | Not evaluated |
| Wannier identity | Projections, windows, centers, spreads, mesh | Not evaluated |
| Withheld interpolation | Direct-parent/Wannier comparisons | Not evaluated |
| Real-space support | Domains, weights, tail diagnostic | Not evaluated |
| Alignment | Symmetry actions, $\mathcal U$, conditioning | Not evaluated |

## Compatibility decision

| Model class | Spectral set | Operator set | Common witness | $[\underline\delta_j,\overline\delta_j]$ | Withheld gates | Disposition |
|---|---:|---:|---:|---:|---|---|
| Nearest-neighbor $sp^3s^\ast$ | Pending | Pending | Pending | Pending | Pending | Not evaluated |
| Second-neighbor extension | Pending | Pending | Pending | Pending | Pending | Not evaluated |
| Selected symmetry corrections | Pending | Pending | Pending | Pending | Pending | Not evaluated |

## Residual attribution

| Diagnostic | Required breakdown | Status |
|---|---|---|
| Spectral residual | Point, band identity, observable, training/withheld role | Not evaluated |
| Operator residual | Onsite/hopping, orbital block, symmetry channel, shell | Not evaluated |
| Search evidence | Starts, budgets, feasible witnesses, exclusion certificate | Not evaluated |
| Sensitivity | Parent, Wannier, stencil, map resolution | Not evaluated |

## Promotion rule

Authenticated values may be promoted to Section III of the manuscript. Before
promotion, every value must retain its source identity, units, basis/gauge and energy
reference, training or withheld role, acceptance rule, and checksum-bound provenance.
Pending entries must not remain in a submission represented as a completed silicon
result.
