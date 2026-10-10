# Current-library capability crosswalk and monograph rewrite plan

## Status and scope

This document starts the rewrite of the living research monograph against the
maintained `ksdft2effmass` library. It records the library capabilities that may support
new controlled calculations, the manuscript locations affected by those capabilities,
and the gaps that must be closed before stronger claims are written.

The inspected repository state is commit
`1c9a2f7719b64758a1e7ede4b867acb420a2b6ab`. The calculation artifacts used by a
manuscript revision remain identified by their retained SHA-256 manifests. Later
commits may revise this crosswalk, the calculations, and the manuscript in place.

This is a software-to-evidence planning record. It is not a calculated result,
scientific validation, uncertainty quantification, or authorization to run Quantum
ESPRESSO or Wannier90.

## Architecture documentation and authority

This plan consumes, rather than replaces, the Architecture v2 records. Architecture
documentation owns package responsibilities, dependency direction, migration targets,
and implementation gates; public source and its tests determine what is implemented at
the inspected commit; retained calculations and manifests determine what was actually
calculated.

| Architecture record | Role in this crosswalk |
|---|---|
| [`periodic/index.md`](../../architecture/v2/ksdft2effmass/periodic/index.md) | Governs the separation of scientific models, retained spaces and operators, represented operators, effective models, and executable campaigns. |
| [`periodic/retained-spaces-and-operators.md`](../../architecture/v2/ksdft2effmass/periodic/retained-spaces-and-operators.md) | Prevents retained evidence from being mistaken for a scientifically retained subspace or operator. |
| [`periodic/reduction-and-evidence-boundaries.md`](../../architecture/v2/ksdft2effmass/periodic/reduction-and-evidence-boundaries.md) | Governs alignment, truncation, fitting, route comparison, withheld evidence, negative outcomes, and error separation. |
| [`periodic/campaign-execution.md`](../../architecture/v2/ksdft2effmass/periodic/campaign-execution.md) | Requires immutable campaign state to remain separate from executable Actions and Workflows. |
| [`periodic/current-to-target-class-crosswalk.md`](../../architecture/v2/ksdft2effmass/periodic/current-to-target-class-crosswalk.md) | Identifies implemented foundations and unresolved source migrations; proposed target names are not treated as public APIs. |
| [`periodic-1d-capability-extraction-inventory.md`](../../architecture/v2/ksdft2effmass/periodic-1d-capability-extraction-inventory.md) | Defines the extracted Appendix G lower layers, campaign-owned controls, and outstanding calculation producers. |
| [`periodic2d-capability-parity.md`](../../architecture/v2/ksdft2effmass/periodic2d-capability-parity.md) | Defines the Appendix H parent-capability gate and blocks further defect work until applicable parity requirements are met. |
| [`research-monograph-software-extraction-audit.md`](../../architecture/v2/ksdft2effmass/research-monograph-software-extraction-audit.md) | Supplies the integrated, partially extracted, not extracted, and not-applicable classifications for calculations and manuscript appendices. |
| [`operators/index.md`](../../architecture/v2/ksdft2effmass/operators/index.md) and [`solid-state/index.md`](../../architecture/v2/ksdft2effmass/solid-state/index.md) | Bound fixed-representation operator mechanics and reusable finite-lattice/reciprocal composition respectively. |
| [`periodic-native-evidence-presence-audit.md`](../../architecture/v2/ksdft2effmass/periodic-native-evidence-presence-audit.md) | Records read-only native-artifact authentication without promoting it to a new calculation or material validation. |

Architecture pages can describe an accepted target that is not yet implemented. For
that reason, this plan uses the following status values:

- **maintained** — implemented through a supported public owner at the inspected commit;
- **partially extracted** — reusable public lower layers exist, but one or more
  scientific owners, producers, orchestration steps, or verifiers remain local;
- **historical-only** — retained evidence exists, but the producing route is not the
  supported route for a new calculation;
- **unmerged** — capability appears only outside the inspected commit and is excluded
  from this plan until integrated; and
- **unsupported/planned** — neither a maintained public route nor adequate retained
  evidence presently supports the claim.

When architecture and source status differ, the stricter boundary governs. An accepted
target does not make a class implemented, and an existing class does not satisfy the
target merely because it has a plausible name.

## Rewrite principles

1. The monograph is the long-form living account. It is rewritten when current library
   capabilities and new evidence change the supported narrative.
2. New controlled calculations use maintained public DataObjects and Actions that obey
   the applicable architecture boundary. Frozen historical scripts may remain
   provenance sources, but they are not the preferred implementation for new evidence.
3. A public API and passing software tests establish software behavior only. Numerical
   claims require retained calculation evidence and independent reconstruction;
   material claims require separate scientific validation.
4. Operators are compared only after their state spaces, bases, coordinates, units,
   geometry, gauge, spin convention, and energy reference are made compatible.
5. Projection, basis alignment, finite Fourier transformation, truncation, fitting, and
   model selection remain distinct operations.
6. Training, guard, and withheld samples retain separate roles. Withheld observations
   may diagnose generalization but may not update a fit, threshold, witness, or
   certificate.
7. A feasible witness supports compatibility within its frozen contract. Failed search
   does not establish incompatibility; a positive separation claim requires a certified
   lower bound over the declared domain.

## Capability crosswalk

| Capability | Maintained owner | Current evidence/readiness | Monograph destination | Required next work |
|---|---|---|---|---|
| Represented state-space, basis, geometry, energy-reference, and operator records | `ksdft2effmass.operators` (`StateSpace`, `Basis`, `Geometry`, `EnergyReference`, `OperatorRecord`) | Public typed foundation with compatibility, difference, residual, serialization, and compression Actions | `chapters/operator-comparison.tex`, `chapters/evidence-for-model-adequacy.tex`, and `chapters/current-evidence-boundary.tex`; Appendices C, G, H, and I | Rewrite operator-comparison prose around explicit records; new calculations must not subtract unidentified arrays |
| Compatibility-first operator subtraction and residual analysis | `OperatorRecordCompatibilityAnalyzer`, `OperatorRecordDifferencer`, `OperatorRecordResidualAnalyzer`, `OperatorRecordComparator` | Ready for new finite represented-operator calculations; no alignment or unit inference is performed implicitly | `chapters/operator-comparison.tex` and `chapters/current-evidence-boundary.tex` | Add a controlled adverse case showing fail-closed metadata incompatibility separately from numerical residuals |
| Orthogonal spectral retention and compression | `OrthogonalSpectralSubspaceSelector`, `OperatorCompression` | **Partially extracted:** numerical selection and compression are maintained, but the architecture crosswalk records no complete manuscript-level parent-qualified retained-subspace and exact-retained-operator owner | `chapters/operator-comparison.tex`, `chapters/bulk-representations.tex`, and `chapters/bulk-reduced-models.tex`; Appendix C | Introduce or complete the scientific retained-space/operator owners before a new campaign claims that identity; do not treat `OperatorCompressionResult` alone as the retained operator |
| Nominal periodic scientific-model hierarchy and toy-model catalog | `ksdft2effmass.periodic` | **Maintained foundation:** public one-, two-, and three-dimensional model roles and explicit toy-model catalog; adoption of several historical toy records into that hierarchy remains incomplete | `chapters/model-adequacy.tex`, `chapters/bulk-representations.tex`, and `chapters/current-evidence-boundary.tex`; Appendices G and H | Replace prose that treats calculation scripts as model owners, but do not imply that every current toy record already satisfies nominal model ownership |
| One-dimensional reciprocal meshes, sewing, transported frames, projectors, and pointwise unitary alignment | `ksdft2effmass.solid_state` (`CenteredUniformReciprocalMesh1D`, `PlaneWaveReciprocalSewingConstructor`, `PolarBandFrameTransporter1D`, `BandProjectorPathConstructor1D`, `BandFrameAligner1D`) | Reusable public Actions are ready; alignment is pointwise unitary Procrustes and must not be confused with a constrained physical alignment family | `chapters/composite-band-gauge-alignment.tex` and `chapters/operator-comparison.tex`; Appendix G | Use the foundational derivation to keep pointwise gauge recovery separate from constrained physical alignment families |
| Wilson-loop spectra and phase-set comparison | `WilsonLoopSpectrumCanonicalizer1D`, `WilsonLoopPhaseSetComparator1D` | Public bounded one-dimensional loop diagnostics | `chapters/operator-comparison.tex` and `chapters/evidence-for-model-adequacy.tex`; Appendix G | Use in a new composite calculation with explicit sewing and gauge controls |
| Projected reciprocal operators | `BandProjectedOperatorPathConstructor1D`, `ReciprocalOperatorSamples1D` | Public and ready when parent operators and compatible frames are supplied | `chapters/composite-band-gauge-alignment.tex`, `chapters/operator-comparison.tex`, and `chapters/bulk-reduced-models.tex`; Appendix G | Retain the parent/frame correlation in each result rather than storing only derived hopping blocks |
| Complete matrix-valued reciprocal-to-hopping transform and inverse interpolation | `ReciprocalOperatorFourierTransformer1D`, `BlockHoppingInterpolator1D`, `BlockHoppingModel1D` | Public and ready for scalar or multiband operators on complete uniform meshes | `chapters/composite-band-gauge-alignment.tex`, `chapters/operator-comparison.tex`, and `chapters/bulk-reduced-models.tex`; Appendix G | New results must state the reciprocal mesh, representative convention, units, and reconstruction tolerance |
| Symmetric hopping truncation and omitted-block norm | `BlockHoppingTruncator1D`, `BlockHoppingTruncationResult1D` | Public and ready; omitted-block norm is a representation diagnostic, not a physical energy fraction | `chapters/evidence-for-model-adequacy.tex` and `chapters/bulk-reduced-models.tex`; Appendix G | Add block-resolved and withheld spectral diagnostics for every tested range |
| Weighted direct hopping fit and route comparison | `BlockHoppingLeastSquaresFitter1D`, `BlockHoppingModelComparator1D` | Public and ready; rank and conditioning are retained, and fit weights are explicit | `chapters/evidence-for-model-adequacy.tex`, `chapters/bulk-reduced-models.tex`, and `chapters/current-evidence-boundary.tex`; Appendix G | Recalculate matched and changed-objective routes through the maintained Actions |
| Hopping Hermiticity, Parseval, and scalar band-shape diagnostics | `BlockHoppingHermiticityAnalyzer1D`, `HoppingParsevalAnalyzer1D`, `ScalarHoppingBandShapeAnalyzer1D` | Public and ready; global diagnostics do not replace individual block inspection | `chapters/evidence-for-model-adequacy.tex` and `chapters/current-evidence-boundary.tex`; Appendix G | Add an explicit diagnostic ledger to the new calculation result |
| End-to-end one-dimensional isolated-band calculation | `Periodic1DIsolatedBandCalculator`, `Periodic1DIsolatedBandCalculationResult`, `Periodic1DIsolatedBandResultVerifier`, and `Periodic1DIsolatedBandResultJsonSerializer` | **Prospective canonical producer, verifier, and distinct schema-v1 serializer implemented:** deterministic in-process parent refinement, scalar reciprocal samples, complete hoppings, finite-range diagnostics, direct-route comparison, separate training/withheld evaluation, independent numerical reconstruction, and new wire ownership now belong to `ksdft2effmass.periodic1d.isolated_band`; no retained M1 result is yet claimed | Appendix G; `chapters/current-evidence-boundary.tex` | Freeze and independently run a new result package before citing a calculated M1 outcome; do not rewrite the historical Appendix G `result.json` identity |
| Constrained one-dimensional spectral/operator admissible sets | `Periodic1DConstrainedAdmissibleSetCalculator`, its typed results, schema-v1 serializer, and verifier | **Complete bounded synthetic M3 package:** composes the rank-two M2 baseline with a two-parameter candidate domain, a finite global-rotation family, normalized spectral and operator losses, common-witness and analytic separation routes, disjoint withheld diagnostics, and hopping-locality diagnostics; the corrected public and standalone verification routes pass adversarial role, domain, manifest-correlation, and certificate-premise checks | `chapters/admissible-sets-and-certificates.tex`, `chapters/evidence-for-model-adequacy.tex`, and Appendix G | Preserve the finite-family, synthetic, threshold-relative, and post-hoc sensitivity boundaries in every extracted claim |
| One-dimensional isolated, stress, and composite retained-result correlation and verification | `Periodic1DIsolatedVerifiedWorkflow`, `Periodic1DStressVerifiedWorkflow`, `Periodic1DCompositeVerifiedWorkflow` | **Partially extracted:** maintained read-only verification of reconstructable historical channels; composite and gauge/localization calculation producers remain outstanding | Appendix G; `chapters/current-evidence-boundary.tex` | Preserve as historical verification and implement a new composite producer before claiming a current-library end-to-end composite campaign |
| Wannier90 interface preparation and native artifact verification | Public integration and periodic-1D native-artifact Workflows | Execution-free preparation, parsing, authentication, and verification are available; they do not authorize or execute Wannier90 | `chapters/evidence-for-model-adequacy.tex` and `chapters/bulk-representations.tex`; Appendix G | Rewrite the interface boundary; do not schedule a new external execution without separate authorization |
| Two-dimensional cosine-model plane-wave and finite-difference represented parents | `ksdft2effmass.periodic2d.model.toy_models` | **Partially extracted:** typed requests, constructors, represented results, and cosine parameters are maintained, but the cosine record has not yet completed nominal `Periodic2DModel` adoption and the parity gate remains open | Appendix H; `chapters/operator-comparison.tex` and `chapters/evidence-for-model-adequacy.tex` | Use the maintained representation constructors in a new convergence/common-space calculation while recording the parent-model ownership limitation |
| Two-dimensional common-space operator comparison | `Periodic2DCommonSpaceOperatorComparator` | **Maintained bounded Action:** transports the finite-difference operator into plane-wave space and reports threshold-free operator defects; it does not decide scientific acceptance | `chapters/operator-comparison.tex`; Appendix H | Ready for a new library-native calculation with prospectively declared grids and interpretation rules |
| Two-dimensional retained scalar, composite, topology, optimizer, and Wannier90 campaign records | `ksdft2effmass.periodic2d` campaign DataObjects and verifiers | **Partially extracted/historical-only producers:** historical results can be decoded and independently reconstructed where retained data permit; granular scientific result owners, stress coverage, several result-producing Actions, and native authentication paths remain incomplete or calculation-local | `chapters/evidence-for-model-adequacy.tex` and `chapters/current-evidence-boundary.tex`; Appendix H | Complete the applicable parity-gate owners and public producers before using these channels for a new end-to-end library-native campaign |
| Two-dimensional finite-defect representation, extraction, and locality | `Periodic2DDefectRepresenter`, `Periodic2DDefectPerturbationExtractor`, `Periodic2DDefectLocalityAnalyzer` | **Partially extracted:** public execution-free finite represented-operator capabilities exist; historical Stage A/B/C campaign ownership remains separate | `chapters/impurity-operator-extraction.tex` and `chapters/current-evidence-boundary.tex`; Appendix J | Defer from the first periodic rewrite; the architecture parity gate blocks new periodic2d defect-campaign work until parent capabilities pass |

## Architecture-driven gaps that constrain the rewrite

| Gap | Architectural consequence | Rewrite consequence |
|---|---|---|
| No complete parent-qualified scientific retained-subspace and exact-retained-operator owner is recorded by the active class crosswalk | Numerical frames, compression results, reciprocal samples, and encoded documents cannot individually stand in for the scientific retained object | `chapters/operator-comparison.tex`, `chapters/bulk-representations.tex`, and `chapters/bulk-reduced-models.tex` and Appendices G/H must describe these as supporting representations until the missing owner is implemented |
| The canonical `periodic1d` migration remains incomplete | Current `campaigns.periodic_1d` public APIs are maintained migration input, not proof that the target namespace and object split are complete | Cite exact current imports in calculation provenance and describe the target architecture separately |
| The periodic2d parity gate remains open | Existing campaigns do not substitute for missing stress, typed scientific-result, alignment, hopping-route, and native-authentication owners | M4 may test maintained represented-parent/common-space mechanics; M5/M6 remain blocked on targeted extraction |
| Correlation and verification are more complete than fresh composite production | Successful replay does not demonstrate a current producer route | Preserve retained Appendix G/H findings, but label new end-to-end production claims as planned until public producers exist |
| Native Wannier90 bytes were authenticated read-only | Presence, parsing, and identity checks are not a new localization calculation or scientific validation | Keep native evidence in the historical evidence section and avoid new external execution without separate authorization |
| Periodic2d defect work is gated by non-defect parent parity | Generic finite-domain defect Actions do not complete the historical Stage A/B/C campaign or authorize its proposed execution | Defer Appendix J calculation work from this rewrite phase |

## New controlled-calculation program

The following calculations replace neither the monograph nor its historical evidence.
They provide new evidence for what the maintained library can calculate now.

### M1 — one-dimensional isolated-band library calculation

**Readiness:** complete bounded synthetic evidence package.

`Periodic1DIsolatedBandCalculator` now owns the canonical typed calculation, with a
distinct schema, independently run verifier, report, software record, figure inputs,
and SHA-256 manifests retained under the Conference Paper 1 calculation tree. It
exercises parent refinement, complete Fourier reconstruction, symmetric truncation,
weighted direct fitting, route comparison, Parseval, Hermiticity, and withheld spectral
checks. It does not reuse the historical Appendix G `result.json` wire identity.

### M2 — one-dimensional multiband alignment and locality calculation

**Readiness:** calculated synthetic package reproducible; verification reconciliation
required before citing it as completely independently verified.

`Periodic1DMultibandAlignmentCalculator` composes the maintained frame, alignment,
projection, Fourier-transform, truncation, interpolation, and band-error Actions for a
gapped rank-two parent. The prospectively frozen package under
`calculations/ICMSEP2026/conference/paper_1/multiband-alignment/` retains a known
nonidentity periodic attack, explicit sewing and transport, projected operators,
complete block hoppings, gauge-resolved truncation, and disjoint withheld diagnostics.
The retained source and artifact hashes pass, the retained verifier reproduces its
record, and the calculation currently regenerates the retained result byte for byte.
However, the standalone verifier does not yet compare every encoded definition control
with the frozen input or enforce every frozen threshold, and the public library
verifier omits the retained hopping-Hermiticity channels. Until those gaps are
corrected with provenance preserved, describe the package as a reproducible calculated
synthetic result with incomplete independent-verification coverage. Exact pointwise
Procrustes recovery and the separately constrained one-global-unitary family remain
distinct. Neither channel establishes a general alignment optimizer, material
validity, or uncertainty bounds.

### M3 — constrained nonidentity admissible-set calculation

**Readiness:** complete bounded synthetic evidence package.

`Periodic1DConstrainedAdmissibleSetCalculator` composes the retained M2 baseline with
a prospectively frozen dimensionless two-parameter domain, nine global real rotations,
normalized spectral and operator losses, disjoint training and withheld meshes,
hopping-locality diagnostics, a feasible-witness route, and an analytic separation
certificate. The retained package under
`calculations/ICMSEP2026/conference/paper_1/constrained-admissible-sets/` has passing
source and artifact manifests, corrected public role verification, a standalone
verifier that rejects invalid definition controls, and a maximum reconstruction defect
below its frozen tolerance. The separate threshold-sensitivity package is explicitly
post hoc and independently verifies the source-manifest correlation and the quadratic
premises used by its analytic reduction. M3 establishes only the two retained outcomes
within the frozen synthetic family and thresholds; it does not supply a general
nonconvex alignment solution, physical threshold calibration, material validity, or
uncertainty quantification.

### M4 — two-dimensional represented-parent and common-space calculation

**Readiness:** maintained represented-parent and comparator Actions are available; the
periodic2d parity gate remains open for broader campaign claims.

Construct plane-wave and finite-difference representations of the same separable and
coupled cosine parents, transport them into one explicit common space, and report
spectral and operator refinement separately. Freeze comparison momenta, cutoff/grid
sequences, units, ordering, and energy zero before evaluating the confirmatory cases.

### M5 — two-dimensional shell and gauge-locality calculation

**Readiness:** implementation gap.

Extract maintained producer Actions for the rank-three composite frame, shell-resolved
hoppings, constrained gauge attacks, and withheld interpolation diagnostics. Reuse the
public model constructors and comparison objects; do not invoke calculation-local
historical runners as the new evidence route.

### M6 — topology and optimizer controls

**Readiness:** retained verification exists; fresh producer integration remains.

After M4 and M5, decide which QWZ, Hofstadter, Haldane, continuation, and optimizer-basin
controls materially test the rewritten claims. Keep topological obstruction, optimizer
convergence, and locality as separate questions. Do not rerun Wannier90 merely to
populate this work package.

## Manuscript rewrite order

1. **Appendix G:** revise ownership and procedure descriptions after M1; complete the
   substantive rewrite after M2 and M3.
2. **`chapters/operator-comparison.tex`:** replace generic alignment and subtraction language with the exact
   compatibility, frame-alignment, projected-operator, and common-space contracts.
3. **Appendix H:** revise represented-parent and common-space sections after M4; revise
   shell and gauge-locality sections after M5.
4. **`chapters/evidence-for-model-adequacy.tex`:** update the evidence taxonomy and failure modes using the new verifier
   and withheld-evidence boundaries.
5. **`chapters/current-evidence-boundary.tex`:** replace the present capability inventory with the new calculated
   outcomes only after their independent verifiers pass.
6. **`chapters/conclusions.tex`:** update conclusions last so that synthesis follows evidence.
7. Refresh `navigation-index.md`, `extraction-map.md`, and the conference-paper sources
   only after the monograph rewrite is internally consistent.

## Acceptance gates for manuscript claims

A new calculation may enter the monograph as a calculated numerical-verification result
only when:

- its protocol and input precede confirmatory evaluation;
- its result was produced through maintained library APIs;
- its decisive quantities are independently reconstructed without importing the
  producer;
- training, guard, and withheld roles remain separate;
- state-space, basis, gauge, units, geometry, and energy reference are explicit;
- global losses are accompanied by block/shell and omitted-tail diagnostics where
  applicable;
- every figure is a deterministic view of retained result data;
- the software revision and dirty state are recorded;
- the package SHA-256 manifest passes; and
- the manuscript states the bounded conclusion and limitations.

Passing these gates establishes controlled software and numerical behavior only. It
does not establish material validity, uncertainty quantification, publication status,
or authority for protected external calculation.
