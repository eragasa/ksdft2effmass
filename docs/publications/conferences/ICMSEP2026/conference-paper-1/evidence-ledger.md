# Numerical-statement and figure-provenance ledger

## Purpose and status

This ledger maps the numerical statements and figures in `manuscript.md` and
`manuscript.tex` to retained repository evidence. It is a synchronization aid, not an
independent scientific acceptance decision. Paths are repository-relative.

Evidence classes remain distinct:

- the new isolated-band and multiband-alignment packages are prospectively frozen
  controlled numerical verification;
- the earlier periodic-2d package is historical controlled-model evidence with its
  own protocol;
- the direct admissible-set package is a separate prospectively frozen analytic and
  numerical demonstration;
- M3 composes M2 into a prospectively frozen finite-family constrained-admissible-set
  calculation with a retained amendment chain;
- the M3 threshold-sensitivity diagram is explicitly post-hoc analytic reanalysis of
  the sealed M3 quadratics, not a prospective prediction; and
- none of these packages is material validation or uncertainty quantification.

## Proof and verification map

| Pillar | Established statement | Location and boundary |
|---|---|---|
| Gauge-orbit decomposition | A nonempty compact admissible family and continuous finite loss attain the orbit minimum; frame transport preserves the orbit loss; frame excess is nonnegative | Supplementary Appendix S1; compactness is conditional on the frozen admissible family being closed in finite-rank $U(r)$ |
| Set separation | Quadratic sublevel sets have certified enclosing radii; the reverse triangle inequality gives a positive lower bound when center distance exceeds the radius sum | Section 2.4, Appendix B, and S5; the direct and M3 values apply only to their distinct frozen contracts |
| Constructive decision rules | A common threshold-feasible witness proves $\delta^\ast=0$; any feasible pair supplies an upper bound | Section 2.4, Appendix B, and S5; Pareto or nondominated status alone proves neither membership nor separation |
| Computational reconstruction | Standalone retained verifiers strictly decode JSON and rebuild the finite protocols without importing their producer Actions | Appendix A and S2--S5; shared libraries, conventions, and runtime mean these are not independent physical or continuum oracles |
| Cryptographic integrity | Retained manifests detect byte changes relative to recorded SHA-256 digests | Package `SHA256SUMS` and protocol-freeze records; hashes alone are not trusted timestamps and do not independently prove chronology |

There is no material-specific locality theorem in the present evidence. In particular,
the synthetic M2 result cannot be cited as a physical bound for Si:P, Si:B, or another
material system.

## Numerical statements

| Manuscript statement | Retained source | Retained location or field | Verification/provenance boundary |
|---|---|---|---|
| 1D cutoff-5 plane-wave error $5.31\times10^{-13}E_G$ | `calculations/ICMSEP2026/conference/paper_1/isolated-band/result.json` | `plane_wave_convergence` entry with `cutoff=5` | `verification.json` passes; sealed by package `SHA256SUMS` |
| 1D finite-difference errors $1.753\times10^{-2}E_G$ at 31 points and $2.598\times10^{-4}E_G$ at 255 points | same | `finite_difference_convergence` entries with `point_count=31,255` | same |
| 64-point reconstruction error $4.17\times10^{-17}E_G$ | same | `complete_transform.reconstruction_maximum_frobenius_error` | same |
| withheld maximum errors $4.62\times10^{-2}E_G$ at range 0 and $9.47\times10^{-9}E_G$ at range 8 | same | `range_study` entries with `maximum_range=0,8`, `withheld_maximum_absolute_error` | withheld coordinates are frozen and disjoint; same verifier and seal |
| largest matched direct/mediated coefficient defect $7.38\times10^{-17}E_G$ and sampled maximum defect $1.56\times10^{-16}E_G$ | same | maxima over `range_study[*].direct_mediated_comparison` | same; algebraic matched-route control only |
| M2 minimum external gap $1.057$ and minimum link/closure singular value $0.99998$ | `calculations/ICMSEP2026/conference/paper_1/multiband-alignment/result.json` | `alignment_diagnostics.external_gap_minimum` and `minimum_neighbor_or_closure_overlap_singular_value` | prospectively frozen local synthetic package; independent verification passes |
| M2 projector defect $3.24\times10^{-16}$, attacked frame defect $1.506$, and attacked operator defect $0.997$ | same | `alignment_diagnostics` | invariant projector and frame-dependent matrix channels remain distinct |
| M2 pointwise recovery defects $6.77\times10^{-16}$ and $9.83\times10^{-16}$; global-unitary frame/operator defects $1.131$ and $0.744$ | same | pointwise and constrained fields in `alignment_diagnostics` | pointwise oracle is not relabeled as the constrained family |
| M2 range-8 attacked omitted norm $5.65\times10^{-5}$ and withheld maximum error $7.04\times10^{-5}$ | same | `range_study` entry with `maximum_range=8`, `attacked` | disjoint withheld points are evaluation-only; package seal and verifier apply |
| M2 independent maximum reconstruction defect $7.43\times10^{-15}$ | `calculations/ICMSEP2026/conference/paper_1/multiband-alignment/verification.json` | `energy_maximum_absolute_defect` | below frozen $10^{-11}$ tolerance; no material or acceptance claim |
| M3 common witness $(0,1)$ with training losses $7.59\times10^{-16}$ and $0.3286318914$ | `calculations/ICMSEP2026/conference/paper_1/constrained-admissible-sets/result.json` | first `cases` entry, `common_witness` | compatible only for spectral/operator thresholds $0.03/0.33$ and the frozen finite alignment family |
| M3 certified separation $\delta^\ast=0.0994674010$ above resolution $0.05$ | same | second `cases` entry, equal `separation_lower_bound` and `separation_upper_bound` | finite global-rotation components and unclipped quadratic ellipsoids only; not an unrestricted-family theorem |
| M3 library/standalone defects $1.33\times10^{-15}$ and $4.66\times10^{-15}$ | `verification.json` and `standalone-verification.json` in the M3 package | maximum-defect fields | below frozen $10^{-11}$ tolerance; amendment 9 adds adversarially tested role and positive-tolerance checks without changing the numerical result; verifier shares numerical dependencies and conventions |
| Post-hoc M3 resolution crossing $0.3137907655$, compatibility transition $0.3192641695$, and original-model admission threshold $0.3286318914$ | `calculations/ICMSEP2026/conference/paper_1/constrained-admissible-sets-threshold-sensitivity/result.json` | named threshold fields | exact reanalysis at fixed $\tau_S=0.03$; verifier checks source-manifest correlation, zero shifts, both cross terms, symmetry, and positive curvature; not prospective or physically calibrated |
| Wannier90 bridge projector/aligned-operator defects $2.65\times10^{-10}$ and $3.57\times10^{-10}E_G$; constrained-family operator defect $1.490E_G$ | `calculations/research-monograph/periodic-2d/wannier90-balanced-result.json` | retained frame and represented-operator comparison channels | historical authorized synthetic execution; portable verifier passes; not M2 or first-principles evidence |
| Wannier90/direct radius-50 omitted norms $2.72\times10^{-4}E_G$ and $5.90\times10^{-3}E_G$ | same and the retained sensitivity-study records | shell-tail diagnostics | finite-case bridge only; the six-case study is nonmonotone and does not establish convergence or optimality |
| exact complete-mesh witness $(1,-1/4)$ and $\delta^\ast=0$ | `calculations/ICMSEP2026/conference/paper_1/result.json` | `compatible_complete_mesh` | `verify_result.py`, `report.md`, and parent-package seal |
| certified $0.452\leq\delta^\ast\leq0.500$ | same | `separated_restricted_training` | exact rational enclosure plus retained verifier |
| restricted-center withheld RMS $0.7211E_G$ | same | `separated_restricted_training` withheld diagnostics | withheld points are diagnostic only |
| 2D product-spectrum defect $3.55\times10^{-14}E_G$ | `calculations/research-monograph/periodic-2d/result.json` and `report.md` | `separable_reference`; report “Separable reconstruction control” | historical periodic-2d protocol and checksum manifest |
| mixed hopping norm grows from $3.00\times10^{-15}E_G$ to $1.94\times10^{-3}E_G$ | same | `coupling_continuation`; report “Coupling continuation” | same |
| strongest-coupling withheld RMS $5.75\times10^{-2}E_G$ to $1.70\times10^{-6}E_G$ and training reconstruction $1.11\times10^{-15}E_G$ | same | coupling/shell observations; report “Shell convergence” | same; training and withheld roles remain distinct |
| anisotropic principal masses $1.184m$, $2.112m$ and symmetry defect $3.60\times10^{-14}E_G$ | same | `anisotropy_control`; report “Anisotropy control” | controlled model, not material masses |
| composite mesh spectral defect $1.22\times10^{-15}E_G$, Wilson-phase defect $2.22\times10^{-15}$, and zero total Chern diagnostic | `calculations/research-monograph/periodic-2d/composite-result.json` and `report.md` | `gauge_invariant_comparison`; periodic-2d report “Composite-band gauge control” | historical composite protocol and checksum manifest |
| spread changes $24.90a^2$ to $67.70a^2$ | same | `smooth_projected_gauge.localization` and `controlled_rough_gauge.localization` | corrected projected-gauge values documented in `composite-projected-gauge-correction.md` |
| radius-18 omitted norm changes $1.38\times10^{-2}E_G$ to $5.25\times10^{-1}E_G$ | same | smooth and rough finite-range diagnostics | same |

## Figure provenance

| Manuscript figure | Retained image | Data source | Generation/provenance |
|---|---|---|---|
| Figure 1, 1D isolated-band summary | `calculations/ICMSEP2026/conference/paper_1/isolated-band/isolated-band-summary.png` | new schema-v1 `result.json`; panel-(d) values also retained in `figure-data.csv` | generated by sealed `run.py`; independently reconstructed by `verify_result.py`; package `SHA256SUMS` |
| Figure 2, M2 multiband alignment summary | `calculations/ICMSEP2026/conference/paper_1/multiband-alignment/multiband-alignment-summary.png` | M2 schema-v1 `result.json`; finite-range values also retained in `figure-data.csv` | generated by sealed `run.py`; independently reconstructed by `verify_result.py`; package `SHA256SUMS` |
| Figure 3, direct admissible sets | `calculations/ICMSEP2026/conference/paper_1/admissible-sets.png` | parent-package `result.json` | parent `run.py`, independent `verify_result.py`, report, and checksum manifest |
| Figure 4, 2D scalar summary | `calculations/research-monograph/periodic-2d/summary.png` | periodic-2d `result.json` | historical periodic-2d retained package and checksum manifest |
| Figure 5, composite gauge/locality summary | `calculations/research-monograph/periodic-2d/composite-summary.png` | `composite-result.json` | historical composite retained package; corrected projected-gauge record |
| Appendix direct-set figure | `calculations/ICMSEP2026/conference/paper_1/admissible-sets.png` | parent-package `result.json` | same source as Figure 3; repeated presentation, not independent evidence |
| Appendix S3 M2 figure | `calculations/ICMSEP2026/conference/paper_1/multiband-alignment/multiband-alignment-summary.png` | same M2 result and figure-data CSV as Figure 2 | repeated presentation, not independent evidence |
| Appendix S4 Wannier90 bridge figure | `calculations/research-monograph/periodic-2d/wannier90-balanced-summary.png` | retained balanced result and portable evidence | separate historical synthetic bridge; no external rerun and no first-principles or material claim |
| Appendix S5 M3 figure | `calculations/ICMSEP2026/conference/paper_1/constrained-admissible-sets/constrained-admissible-sets-summary.png` | M3 `result.json` and `figure-data.csv` | generated by final amended `run.py`; independently reconstructed; package checksum manifest passes |
| Appendix S5 post-hoc threshold-sensitivity figure | `calculations/ICMSEP2026/conference/paper_1/constrained-admissible-sets-threshold-sensitivity/operator-threshold-sensitivity.png` | sensitivity `result.json` and `figure-data.csv`, derived from sealed M3 quadratics | explicitly post-hoc analytic reanalysis; separate hardened verifier checks the decisive premises and reconstructs the complete grid with zero reported defect |

## Synchronization rules

1. Update a manuscript value only from the retained source named above.
2. Do not silently move a historical claim into the new isolated-band schema.
3. Do not convert maximum error, RMS error, coefficient norm, sampled norm, or
   operator Frobenius discrepancy into one another.
4. Do not describe numerical-consistency tolerances as confidence levels or
   uncertainties.
5. Rebuild and independently verify the owning package before changing a retained
   number or figure.
6. If any sealed digest changes, update this ledger only after reviewing the new
   protocol, result, verification, report, and checksum boundary.
