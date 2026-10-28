# Phase 0 inventory and replacement boundary

## Decision

The new Periodic1D implementation completely replaces the current
`ksdft2effmass.periodic1d` source and the calculation-local Python packages. It does not
preserve old Python imports, class names, serializers, workflow-shaped APIs, or live
schema-v1 decoders.

Replacement is admitted only after tests establish the same bounded calculations and
plot data channels described below. The new source must not import, copy, wrap, subclass,
or execute code under a calculation `workflow/` directory. Historical bytes remain
unchanged and recoverable from Git for provenance, but they are not a compatibility
contract for the new runtime.

This inventory is bound to baseline commit
`2a5681b877b5fbf9e1cf8fcdd0c9332d0bc69c63`. No source or artifact is removed by Phase
0.

## Current installed package

The current root exports 31 distinct names. All are scheduled for removal after the
relevant behavioral-parity gate and direct caller migration. No alias or re-export is
planned.

| Current source surface | Exported names | Replacement owner and gate |
|---|---|---|
| `periodic1d.model` | `Periodic1DFourierHamiltonianToyModel`, `Periodic1DBlockHamiltonianToyModel` | Replace with concrete typed parent data owned by `model_systems.mathieu1d`, `periodic1d.fourier_locality`, and the two rank-two owners as applicable; remove after Phases 1--4 migrate callers. |
| `periodic1d.isolated_band.definition` | `Periodic1DIsolatedBandCalculationDefinition` | Replace in `periodic1d.fourier_locality` during Phase 2. |
| `periodic1d.isolated_band.calculate` | `Periodic1DIsolatedBandCalculator` | Replace with the Phase 2 analyzer; do not preserve the Action signature. |
| `periodic1d.isolated_band.results` | `Periodic1DPlaneWaveConvergenceObservation`, `Periodic1DFiniteDifferenceConvergenceObservation`, `Periodic1DIsolatedBandRangeResult`, `Periodic1DIsolatedBandCalculationResult` | Replace with immutable Phase 2 result sections. |
| `periodic1d.isolated_band.serialization` | `Periodic1DIsolatedBandResultJsonSerializer`, qualified `SCHEMA_ID` | Replace with model-owned canonical `to_json()`/`from_json()` bytes; no schema-v1 decoder is required. |
| `periodic1d.isolated_band.verify` | `Periodic1DIsolatedBandResultVerifier`, `Periodic1DIsolatedBandVerificationResult` | Replace with a byte-owning Phase 2 verifier and typed verification aggregate. |
| `periodic1d.multiband_alignment.definition` | `Periodic1DMultibandAlignmentCalculationDefinition` | Replace in `periodic1d.composite_band_alignment` during Phase 3. |
| `periodic1d.multiband_alignment.calculate` | `Periodic1DMultibandAlignmentCalculator` | Replace with the rank-two composite analyzer; do not preserve the Action signature. |
| `periodic1d.multiband_alignment.results` | `Periodic1DMultibandAlignmentDiagnostics`, `Periodic1DMultibandAlignmentRangeResult`, `Periodic1DMultibandAlignmentCalculationResult` | Replace with rank-two composite result sections. |
| `periodic1d.multiband_alignment.serialization` | `Periodic1DMultibandAlignmentResultJsonSerializer`, qualified `SCHEMA_ID` | Replace with the rank-two composite typed wire; no schema-v1 decoder is required. |
| `periodic1d.multiband_alignment.verify` | `Periodic1DMultibandAlignmentResultVerifier`, `Periodic1DMultibandAlignmentVerificationResult` | Replace with a byte-owning rank-two composite verifier. |
| `periodic1d.admissible_sets.definition` | `Periodic1DAdmissibleSetThresholds`, `Periodic1DConstrainedAdmissibleSetCalculationDefinition` | Replace with separate confirmatory, scalar-demonstration, and sensitivity configurations in Phase 4. |
| `periodic1d.admissible_sets.calculate` | `Periodic1DConstrainedAdmissibleSetCalculator` | Replace with the confirmatory analyzer; do not preserve the composed M2 producer call. |
| `periodic1d.admissible_sets.results` | `Periodic1DAdmissibleSetDisposition`, `Periodic1DQuadraticLoss`, `Periodic1DAdmissibleSetLocalityResult`, `Periodic1DAdmissibleSetParameterEvaluation`, `Periodic1DAdmissibleSetCaseResult`, `Periodic1DConstrainedAdmissibleSetCalculationResult` | Replace with study-specific immutable Phase 4 result sections; share behavior only where meaning is unchanged. |
| `periodic1d.admissible_sets.serialization` | `Periodic1DConstrainedAdmissibleSetResultJsonSerializer`, qualified `SCHEMA_ID` | Replace with separate study wires; no schema-v1 decoder is required. |
| `periodic1d.admissible_sets.verify` | `Periodic1DConstrainedAdmissibleSetResultVerifier`, `Periodic1DConstrainedAdmissibleSetVerificationResult` | Replace with separate byte-owning verifiers. |

The root `periodic1d.__init__` re-exports the 31 non-`SCHEMA_ID` names above. The three
subpackages also re-export their family names. Those aggregate import surfaces are all
removed rather than reproduced.

### Current Python callers

Seven Python files outside the package import the current surface:

- `calculations/mathieu1d/src/single_band_fourier_reduction/definition.py`;
- `calculations/mathieu1d/tests/test__SingleBandFourierReductionExperiment.py`;
- `python/src/ksdft2effmass/model_systems/mathieu1d/study/input.py`;
- `python/src/ksdft2effmass/model_systems/mathieu1d/study/records.py`;
- `python/tests/software_verification/ksdft2effmass/periodic1d/test__Periodic1DIsolatedBandCalculator.py`;
- `python/tests/software_verification/ksdft2effmass/periodic1d/test__Periodic1DMultibandAlignmentCalculator.py`; and
- `python/tests/software_verification/ksdft2effmass/periodic1d/test__Periodic1DConstrainedAdmissibleSetCalculator.py`.

The first four move to Phase 1 owners or disappear with the old Mathieu1D package. The
last three are replaced by package-aligned successor tests. Internal imports among the
three current families disappear with the package.

The four Sphinx pages under `doc/sphinx/api/ksdft2effmass/periodic1d/` are replaced by
pages for the concrete successor owners. Architecture v2 pages remain historical
records, not supported import documentation.

## Current serializer and verifier boundary

| Family | Current result schema | Current serializer input | Current verifier input | Replacement disposition |
|---|---|---|---|---|
| M1 isolated band | `ksdft2effmass.periodic1d.isolated-band-calculation-result.v1` | typed `Periodic1DIsolatedBandCalculationResult` | typed result object | Replace completely in Phase 2. |
| M2 multiband alignment | `ksdft2effmass.periodic1d.multiband-alignment-calculation-result.v1` | typed `Periodic1DMultibandAlignmentCalculationResult` | typed result object | Replace completely in Phase 3. |
| M3 constrained sets | `ksdft2effmass.periodic1d.constrained-admissible-set-result.v1` | typed `Periodic1DConstrainedAdmissibleSetCalculationResult` | typed result object | Replace completely in Phase 4. |

The current serializers only encode. They do not reconstruct these result types from
wire bytes, and the current verifiers do not own subject bytes. Therefore none of the
three current runtime schemas qualifies as the target direct lifecycle. The successor
verifiers accept exact immutable bytes and reconstruct their own subjects.

## Historical calculation packages

The removed conference calculation packages are recovered directly from commit
`c5d34a93b4710a4a430738c404c775865d418d42`. Tree objects cover every byte beneath each
package without restoring the directories.

| Package | Git tree | Files | `SHA256SUMS` SHA-256 | Manifest check | Result SHA-256 |
|---|---|---:|---|---|---|
| M1 `isolated-band/` | `418999a90efa3001d2e50a2e7912f126bc30903f` | 18 | `64f16168fa05fefa902f8c2216b1e445c6a0ecd8e28dcebd75c73589833edf5f` | 13/13 entries pass | `c7262e3527a58dfd8fe237fa495549c53a1a65f3e46a98ed6d40673f14b6a394` |
| M2 `multiband-alignment/` | `19af0e6d222b1f41fcb7b2869e1fcd7c2f309cd9` | 19 | `019050d903e01b0f33af1c658af33af6e77653c733f96d661d38595adbfdf73f` | 14/14 entries pass | `3bb30d20f73d2d4ae8ea55a493d50978c5094dbecfcd22237dd8c32760b0f3da` |
| M3 `constrained-admissible-sets/` | `557604ba0893b0f02ec8f69f89e8bfa4cb7786b4` | 30 | `552e93aced1d1771a54878600e9aa667c06bbfd1a4512f56d30f3f7ebcae7ca9` | 25/25 entries pass | `9d95da829b84743386f627c32e9b4a740f2ff602d77a1ff225f295e17f98d2f9` |
| Post-hoc sensitivity | `41efebc31d624bd5f42f669e85b74d7e4343c899` | 14 | `206120018ab27d05ea09978185cdd592aa427135169c3045e7a14c96239515a1` | 13/13 entries pass | `cb667cb753245ea1145164c9e67fcf3bec78a0c8e115b6282c22f63fc604c05f` |

Historical schema declarations are:

| Package | Input schema | Result schema | Verification schema |
|---|---|---|---|
| M1 | `ksdft2effmass.periodic1d.isolated-band-calculation-input.v1` | `ksdft2effmass.periodic1d.isolated-band-calculation-result.v1` | `ksdft2effmass.periodic1d.isolated-band-calculation-verification.v1` |
| M2 | no top-level input schema field | `ksdft2effmass.periodic1d.multiband-alignment-calculation-result.v1` | `ksdft2effmass.periodic1d.multiband-alignment-verification.v1` |
| M3 | `ksdft2effmass.periodic1d.constrained-admissible-set-input.v1` | `ksdft2effmass.periodic1d.constrained-admissible-set-result.v1` | `ksdft2effmass.periodic1d.constrained-admissible-set-verification.v1` |
| Sensitivity | `ksdft2effmass.periodic1d.constrained-admissible-set-threshold-sensitivity-input.v1` | `ksdft2effmass.periodic1d.constrained-admissible-set-threshold-sensitivity-result.v1` | `ksdft2effmass.periodic1d.constrained-admissible-set-threshold-sensitivity-verification.v1` |

These packages contain their own historical producer and standalone verifier scripts.
They are provenance-only Git objects. New source neither imports them nor promises to
decode their bytes.

### Scalar/direct predecessor

The scalar/direct demonstration is represented by the top-level conference package at
the same recovery commit and tree
`672049ec656d503ca6c678bcf67ed36b5606e2d1`. Its result schema is
`icmsep2026.paper1.admissible-set-result.v1`; the result SHA-256 is
`db74cab9a08c7c37de4e2d1940bc65e8ef5acf701d3cc883cb79314803d71ab0`; and
`admissible-sets.png` has SHA-256
`568fab5703ca1c630e01f7d6b3bb0b53e81189eee3668131ff51f369b36092f0`.
Nine of ten entries in its `SHA256SUMS` match the recovered bytes. The exception is
`README.md`: the manifest declares
`80d8729e91a4ee653c86c9e81981a704952ec1a03de2bff3c69a83840ca0ce46`, while the
recovered file is
`7f70548bf18691a28814bfde8e528bcbf33892ecf7dfb7d0b38fb672e1915631`.
This pre-existing documentation mismatch is recorded rather than repaired or ignored.
Scientific result, boundary, plot, report, source, and environment entries pass.

### Publication consumers

Current publication consumers of removed M1--M3 paths are migration obligations, not a
reason to preserve old runtime code:

- M1: `docs/publications/papers/Ragasa2026a/v2/manuscript.tex`;
- M2: the Ragasa2026a v1 evidence ledger, manuscript sources, README, Appendix S3, and
  provenance appendix; the Ragasa2026a v2 manuscript; both Ragasa2026c v1 manuscript
  sources; and the research-monograph current-library crosswalk;
- M3: the Ragasa2026a v1 evidence ledger, manuscript sources, README, Appendix S5, and
  provenance appendix; the Ragasa2026a v2 manuscript; both Ragasa2026c v1 manuscript
  sources and extracted-evidence appendices; the research-monograph current-library
  crosswalk; and the retained-calculation figure README; and
- sensitivity: the Ragasa2026a v1 evidence ledger, README, Appendix S5, and provenance
  appendix; the Ragasa2026a v2 manuscript; and the Ragasa2026c v1 extracted-evidence
  appendices.

Calculation migration ledgers, architecture v2 pages, and old tests also cite these paths.
Each citation moves to a successor execution or an explicit Git locator. No citation is
silently redirected to numerically different evidence.

## Numerical behavioral baselines

The successor does not preserve class layouts, but it must reproduce these finite
scientific channels with the stated current tolerances before the old source can be
removed.

### M1 isolated-band baseline

Current software case:

- potential `0.5 cos(x)`, period `2π`, reciprocal vector and recoil scale `1`;
- plane-wave cutoffs `(1, 2)`, reference cutoff `3`, production cutoff `2`;
- finite-difference points `(7, 9)`;
- parent reduced momenta `(-0.5, 0.0, 0.5)` and two compared bands;
- training mesh `8`, withheld mesh `9`, and ranges `(0, 1, 2)`;
- coordinate tolerance `1e-14`; reconstruction, Hermiticity, Parseval, and imaginary
  tolerances `1e-12` in their declared units.

Parity requires the same parent/training/withheld shapes, disjoint training and withheld
coordinates, complete-transform reconstruction pass, hopping Hermiticity pass, range
inventory, Parseval passes, identified direct fits, band-shape passes, and independent
maximum spectral and hopping defects below `1e-12`. A `1e-3` altered convergence value
must produce a defect above `9e-4`. Separate executions must produce equal canonical
bytes for the frozen controls.

The historical M1 publication baseline additionally reports cutoff-5 error no greater
than `5.31e-13` against its finite cutoff-15 reference and finite-difference error falling
from `1.753e-2` at 31 points to `2.598e-4` at 255 points. These are retained finite values,
not continuum-error claims.

### M2 rank-two composite baseline

Current software case:

- the exact four-by-four onsite and positive-neighbor block matrices in
  `test__Periodic1DMultibandAlignmentCalculator.py`;
- retained rank `2`, training mesh `16`, withheld mesh `33`, ranges `(0, 1, 2, 3)`;
- attack constant angle `0.30` and sine coefficients `(0.65, 0.30)`;
- external-gap lower bound `0.5`, overlap threshold `0.8`;
- orthonormality and reconstruction tolerances `1e-12`, coordinate tolerance `1e-14`,
  Hermiticity tolerance `1e-12`, and verification tolerance `1e-11`.

Parity requires external gap above `0.5`, attacked-frame defect above `0.5`, pointwise
frame and inverse-rotation defects below `1e-12`, one-global-unitary frame defect above
`0.5`, the declared attacked/reference omitted-block ordering, and independent energy and
dimensionless defects below `1e-11`. Rank-deficient global alignment must fail closed.
A `1e-3` changed frame or Hermiticity diagnostic must produce a defect above `9e-4`.

The retained publication values used for data parity include minimum external gap
approximately `1.056646`, minimum neighboring/closure singular value `0.9999829`,
projector defect `3.24e-16`, attacked frame defect `1.506`, attacked operator defect
`0.9972`, pointwise recovery defects `6.77e-16` and `9.83e-16`, one-global-unitary
frame/operator defects `1.131` and `0.744`, range-8 attacked omitted norm `5.65e-5`,
withheld maximum error `7.04e-5`, and independent reconstruction defect `7.43e-15`.
The successor comparison uses the exact recovered JSON values rather than these rounded
publication values.

### M3 confirmatory baseline

Current software case composes the M2 controls above with:

- parameter bounds `(-0.25, 0.25)` and `(0.4, 1.2)`;
- nine angles from `-1.2` through `1.2` in increments of `0.3`;
- compatible thresholds `(0.03, 0.33)` and separated thresholds `(0.03, 0.31)`;
- common witness `(0.0, 1.0)`;
- locality ranges `(0, 1, 2, 3)`, separation resolution `0.05`;
- quadratic tolerance `1e-12` and verification tolerance `1e-11`.

Parity requires one admitted common witness with a nonzero selected angle, one separated
case with no common witness, and a separation lower bound greater than `0.05` and no
greater than its upper bound. Independent dimensionless and energy defects remain below
`1e-11`. A `1e-3` changed withheld diagnostic produces a defect above `9e-4`; changed
roles, training/quadratic correlation, or locality inventory fail closed.

The exact recovered result owns the data comparison. Publication summaries include common
witness training losses `7.59e-16` and `0.3286318914`, separation
`0.0994674010`, and independent defects `1.33e-15` and `4.66e-15`.

### Threshold sensitivity baseline

The sensitivity successor remains a separate post-hoc result. It is bound to the exact M3
result digest and must reproduce the exact recovered fields for the resolution crossing,
compatibility transition, original-model admission threshold, complete threshold grid,
and selected angle. Publication summaries are `0.3137907655`, `0.3192641695`, and
`0.3286318914`; exact comparisons use recovered JSON values. Source-manifest mismatch,
nonzero shift center, either nonzero cross curvature, asymmetry, or nonpositive curvature
must fail closed.

## Plot-data parity

Plot parity is scientific-data parity, not subjective visual resemblance and not PNG byte
equality. For every mapped plot, tests compare the authenticated typed projection against
its predecessor result/figure-data channels with explicit tolerances. The renderer may
change typography, layout, colors, and resolution without changing the represented
values, support boundaries, thresholds, witnesses, or dispositions.

| Successor baseline PNG | Parity reference | Required data-channel parity |
|---|---|---|
| `mathieu1d-finite-reduction.png` | direct typed Mathieu1D execution | parent dispersion, reconstructed dispersion, hopping magnitudes, truncation-error series, and declared case labels |
| `rank1-fourier-locality.png` | recovered M1 result and `figure-data.csv` | parent refinement, complete transform, hopping decay, range study, and withheld error |
| `rank2-band-equivalence-locality.png` | current rank-two development results at the baseline commit | Hamiltonian and band-error channels, cyclic/interpolation/truncation separation, hopping power, and finite attainable range decisions |
| `rank2-alignment-locality.png` | recovered M2 result and `figure-data.csv` | retained spectrum, pointwise/global alignment channels, omitted block norms, and withheld errors |
| `confirmatory-admissible-sets.png` | recovered M3 result and `figure-data.csv` | exact finite angle inventory, common witness, separated case, quadratic boundaries, thresholds, and separation certificate |
| `scalar-direct-admissible-demonstration.png` | recovered direct result, `boundaries.csv`, and `admissible-sets.png` | scalar/direct compatible and separated regions, fixed thresholds, and declared witness or separation values |
| `threshold-sensitivity-finite-ledger.png` | recovered sensitivity result and `figure-data.csv` | finite threshold grid, three named transitions, original threshold, and recorded dispositions only |
| `higher-rank-alignment-locality.png` | current higher-rank development records at the baseline commit | rank/depth inventory, gate outcomes, alignment and sewing diagnostics, support/tail channels, and scalar ledger values |

Mathieu1D Phase 1 is complete. The direct execution is
`calculations/mathieu1d/executions/direct-finite-reduction-n64/`; its exact result,
verification, and authenticated full-figure SHA-256 values are
`83d25e824a0aedf085e77e86a998c02a17d4a51c320375b0bfb395986dae3fe6`,
`61553c16636efc39452706006dc480b827c2f2d04f3e318e02e3c2eec4f24664`, and
`de0ae08bd6e4c16afee074b14a73be2a7efbfa133044fc08ee75492238886b7e`.
The predecessor run tree has been removed; its Git recovery boundary is confined to
`calculations/mathieu1d/legacy-run-retirement.md`.

## Calculation-local Python disposition

Calculation-local code may serve only as a read-only behavioral reference for tests and
crosswalks. New installed source must not import or copy it.

| Current location | Python files | Disposition |
|---|---:|---|
| Retired Mathieu1D calculation-local package | 0 | Phase 1 parity and consumer migration completed; package, legacy scripts, tests, predecessor runs, orphaned input, and schema-v1 files removed from the live tree. |
| `calculations/periodic1d/rank2/band-equivalence-versus-hopping-locality/workflow/` | 21 | Use existing result tables and tests only to specify Phase 3 parity. Write new installed implementations from the scientific specification and canonical PhysKit/Optimization owners. Remove the workflow tree after parity and consumer migration. |
| `calculations/periodic1d/rank2/band-equivalence-versus-hopping-locality/analysis/development/` plotting scripts | 7 | Use only to enumerate predecessor channels. Replace with authenticated source-owned rendering and remove after parity. |
| `calculations/periodic1d/rankN/composite-band-alignment-locality/workflow/` | 11 | Use records and tests only to specify Phase 5 parity. Write the new higher-rank owner independently; remove the workflow tree after parity. |

Development `run_*` scripts remain calculation-owned effect adapters until their direct
three-stage successors pass. Calculation-local tests are replaced by package-aligned
successor tests, not moved unchanged.

## Phase 0 validation

At this baseline:

- the focused M1, M2, M3, and sensitivity suite reports 30 passed and 20 skipped;
- all 20 skips are historical-package tests whose removed directories are intentionally
  absent from the branch;
- all 65 entries across the recovered M1, M2, M3, and sensitivity checksum manifests
  pass direct Git-object verification;
- the scalar/direct manifest has the one recorded README mismatch and 9 passing entries;
- all 9 entries in the latest retained Mathieu1D checksum manifest pass;
- the root export inventory contains 31 unique names and the external Python caller
  inventory contains exactly 7 files; and
- Sphinx builds with warnings treated as errors.

These checks freeze predecessor behavior and recovery only. They do not validate the
future successor or establish scientific acceptance.

## Removal gates

Legacy source can be removed without compatibility code when all applicable gates pass:

1. the successor calculation reproduces the frozen finite controls and every required
   result channel within the unchanged tolerance;
2. independent verification reconstructs the successor from exact result bytes;
3. authenticated plot projections reproduce the mapped predecessor data channels;
4. every maintained caller and publication consumer points to the successor or an exact
   Git locator;
5. no successor source or script imports a calculation `workflow/` directory;
6. public API documentation names only successor owners; and
7. removal is separately authorized.

This is a software and finite-data parity boundary. It does not assert continuum
convergence, material validity, uncertainty quantification, evidence promotion,
publication acceptance, or release status.
