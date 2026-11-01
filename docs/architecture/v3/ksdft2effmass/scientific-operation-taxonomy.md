# Cross-dimensional scientific-operation taxonomy

## Status

This page defines the first implemented nominal ownership layer for scientific
operations shared by rank-two 1D, rank-$N$ 1D, and rank-two 2D/3D studies. It does not
merge their requests, outcomes, retained records, verification scopes, or evidence
identities.

The broad scientific-operation roots remain intentionally interface-free abstract
marker classes. They admit implementations through inheritance, not through structural
attribute matching. Narrow action-role bases may additionally require only the common
scientific identity and execution surface shared by every admitted implementation.
Family classes continue to own their exact scientific fields and validation rules.

## Vocabulary and ownership

### Periodic-1D coordinate geometry

`ksdft2effmass.periodic1d.Periodic1DLatticeGeometry` is an immutable scalar
snapshot of the one-dimensional lattice period. It reconstructs PhysKit
`DirectLattice1D` and `ReciprocalLattice1D` values and uses the latter for the
explicit conversion

\[
q = k/G, \qquad G = 2\pi/a_0.
\]

`Periodic1DReducedCoordinateConvention` nominally identifies the maintained 1D
families that calculate on the centered, half-open reduced coordinate $q$. The
coordinate is dimensionless, but the periodic model is not thereby required to use a
dimensionless direct lattice, energy unit, or operator unit. Its historical `a_0 = 1`
geometry is one explicit reduced-unit selection. New rank-first study specifications
must bind a separate `Periodic1DLatticeGeometry`, normally snapshotted from a caller-
selected PhysKit `DirectLattice1D`. The geometry always requires an explicit PhysKit
`PhysicalUnit` with length dimensionality. A magnitude-one atomic-unit choice is
represented as `a_0 = 1 bohr`, not as a unitless lattice. Action and mass scales remain
with the parent physical model rather than the geometry owner. Geometry is not inserted
into historical retained wires.

### Gauge alignment

`ksdft2effmass.gauge_alignment.GaugeAlignment` identifies retained-space gauge
alignment or an exact applicability boundary. The narrower
`GaugeAlignmentAnalysisIdentity` validates the exact retained rank, gauge group,
ordered alignment-sample count, action side, and inner-product convention shared by the
narrower `GaugeAlignmentAnalysisRequest`, `GaugeAlignmentAnalysis`, and
`GaugeAlignmentAnalyzer` role bases. The analyzer delegates that identity from its bound
request, owns zero-argument execution, and rejects an analysis whose identity drifts from
the request. These bases do not merge family-specific fields, solvers, tolerances,
outcomes, or wires. The corresponding
`Periodic1DGaugeAlignmentAnalysisRequest`, `Periodic1DGaugeAlignmentAnalysis`, and
`Periodic1DGaugeAlignmentAnalyzer` bases add dimensional ownership without selecting a
default lattice, solver, tolerance, or wire.

The rank-first Periodic1D alignment factory dispatches only on exact typed study
specifications. Every specification binds explicit `Periodic1DLatticeGeometry`:

- rank one returns an operator-trivial $U(1)$ applicability action and emits no
  duplicate numerical alignment channels;
- rank two delegates to the bounded composite-band $U(2)$ implementation; and
- rank $N$ delegates to the D1-v1 four-alignment implementation with all numerical
  collaborators supplied explicitly.

The rank-two and rank-$N$ adapters preserve their historical calculation-result bytes.
The selected direct lattice remains study context rather than being injected into those
historical wires.

### Subspace reduction

`ksdft2effmass.subspace_reduction.SubspaceReduction` identifies an explicit map from a
parent state space to a retained state space.

The domain distinguishes:

1. spectral-subspace selection or truncation as the modeling decision;
2. projection onto the retained subspace;
3. orthogonal compression as the finite construction of
   $P H P|_{\operatorname{Ran}P}$; and
4. any later basis transformation inside the retained space.

An external spectral gap qualifies a selected subspace. It is not a reduction error.
Existing Hamiltonian and subspace owners remain authoritative; this package must not
copy their matrix construction or state-space definitions.

Current nominal assignment:

- `ksdft2effmass.hamiltonian.reduction.SpectralReduction`.

The audited periodic families consume already represented retained-space operators; they
do not themselves perform spectral-subspace selection or orthogonal compression. They
therefore do not gain `SubspaceReduction` merely because their models have rank two or
rank $N$.

### Representation equivalence

`ksdft2effmass.representation_equivalence.RepresentationEquivalence` identifies a
comparison of representations after their state spaces, basis conventions, gauge
actions, energy references, units, and sampling geometry have been aligned.

Isospectrality alone does not establish representation equivalence. PhysKit continues
to own physical frame transport, and Project Koios Optimization continues to own
unit-free alignment algorithms. KSD owns the admitted equivalence semantics, result
fields, thresholds, and evidence policy.

Current nominal assignments:

- `Periodic1DRank2PointAnalysis`, which compares the untruncated
  reference and gauge-rotated representations at one amplitude; and
- `Periodic1DRankNRecoveryAnalysis`, which keeps frame recovery and represented-
  operator recovery distinct for one explicitly selected gauge alignment; and
- `BandEquivalenceLocalityRepresentationEquivalenceAnalysis`, which retains the
  family-specific state-space identity, direct-band, covariance, restricted-rotation,
  correlation, and operator-threshold diagnostics for the rank-two 2D/3D family.

The broader 2D/3D point aggregate remains unassigned because it combines qualification,
representation, support-truncation, and numerical-consistency channels. It now composes
the typed representation-equivalence result while projecting the historical scalar
attributes used by the unchanged retained record. This decomposition does not label the
mixed point aggregate as one universal analysis result.

### Hopping locality

`ksdft2effmass.hopping_locality.HoppingLocality` identifies diagnostics on an
unchanged hopping-coefficient representation. It requires concrete owners to declare
the coefficient index space, support geometry, basis, gauge, normalization, and
range inventory. It does not imply coefficient removal or construction of a
finite-support operator.

`ksdft2effmass.periodic1d.hopping_locality.Periodic1DHoppingLocality` specializes
that ownership for coefficients indexed by one-dimensional integer translations.
`Periodic1DRank2HoppingPower`, `Periodic1DRankNHoppingTailResult`, and
`Periodic1DRankNHoppingLocalityAnalysis` adopt this specialization. The rank-two
point analysis remains a mixed representation-equivalence and locality owner and is
not relabeled as a standalone hopping-locality analysis.

### Real-space support truncation

`ksdft2effmass.support_truncation.SupportTruncation` identifies irreversible removal
from an explicitly declared representation support without selecting a physical
domain. `ksdft2effmass.real_space_support_truncation.RealSpaceSupportTruncation`
specializes that root to represented real-space operator support after the basis and
gauge have been fixed.

`ksdft2effmass.periodic1d.support_truncation.Periodic1DSupportTruncation` further
specializes the hierarchy to periodic one-dimensional integer translations. The
mirrored concrete names use `Periodic1DRank2SupportTruncation...` and
`Periodic1DRankNSupportTruncation...` for their request, analyzer, and analysis
surfaces. Historical shorter rank-two request, analyzer, and analysis names remain
identical class aliases.

Admitted geometry-specific policies are:

- symmetric integer ranges in 1D;
- complete metric shells in 2D and 3D; and
- explicit conjugate-closed support groups for anisotropic studies.

PhysKit owns reusable lattice geometry and `LatticeDisplacement`. KSD owns the
immutable admission policies `SymmetricRangeSupport1D`,
`MetricShellSupportInventory`, and `ConjugateClosedSupport`, including which complete
support sets are admitted, which cutoffs are evaluated or selected, and how unresolved
threshold outcomes are retained. The `real_space_support_truncation` domain admits
2D/3D geometry nominally through `MetricGeometry` and basis-resolved geometry through
`BasisResolvedMetricGeometry`. `BandEquivalenceLocalityCase` inherits the latter and
keeps its family-specific serialization. `MetricShellValueAnalyzer` calculates scaled
integer metric values and an explicit rounding defect for any finite periodic
inventory, including a cyclic inventory with unpaired Nyquist representatives.
`MetricShellSupportClassifier` adds the stronger sorted, unique, zero-containing, and
conjugate-closed admission needed to construct `MetricShellSupportInventory` and its
explicitly named `ordinal_shell_indices`. Existing dimensional cutoffs continue to use
the preserved metric values, which need not be contiguous. Historical retained fields
named `shell_index` or `shell_indices` remain unchanged; derived `metric_shell_value`
and `metric_shell_values` properties make their semantics explicit without changing
canonical bytes.

`RealSpaceSupportTruncationToleranceSelector` is the shared 1D/2D/3D cutoff-selection
action. `RankNormalizedMatrixFrobeniusErrors` owns its maximum and root-mean-square
errors; `OrderedEigenvalueErrors` owns its maximum-absolute and root-mean-square errors.
`RealSpaceSupportTruncationErrors` composes those exact immutable values rather than
exposing four unrelated scalar fields. Each immutable
`RealSpaceSupportTruncationComparison` binds one exact support to its reference- and
comparison-route errors. `RealSpaceSupportTruncationToleranceSelectionRequest` owns and
validates the ordered, strictly nested comparison inventory and exposes its typed error
channels. `RealSpaceSupportTruncationToleranceSelection` accepts only that request and
derives all four outcomes, so callers cannot independently supply inconsistent source
and result state. The selector remains the action-facing facade and delegates to this
canonical construction. Selection evaluates the matrix-Frobenius maximum and
ordered-eigenvalue maximum-absolute channels separately for the reference and comparison
models.
When the admitted support sequence is $S_0 \subset S_1 \subset \cdots$, the selected
index is

$$
j_* = \min\{j : E(S_j) \leq \tau\}.
$$

The typed outcome is `MinimumToleranceSatisfyingSupport`; absence of such an index is
`SupportToleranceUnresolved`. The selector does not assume that the sampled errors are
monotone. Family adapters project the exact support back to a symmetric-range or metric-
shell label. Historical retained names such as `first_passing_range` and
`reference_band_shell` remain compatibility fields, not the terminology of the shared
scientific API.

`RealSpaceSupportTruncationFamilyRequest` owns an ordered, unique family-coordinate
inventory. `RealSpaceSupportTruncationFamilyMember` binds one coordinate to one outcome
that nominally inherits `RealSpaceSupportTruncation`, and
`RealSpaceSupportTruncationFamily` enforces complete order-preserving coverage. These
generic values are dimension- and rank-independent and contain no parent-model,
state-space, alignment, sampling, unit, threshold, or retained-wire policy. The
`Periodic1DRank2TruncationFamilyAnalysis` adapter composes the existing rank-two
truncation analyzer at every declared parent scale and derives each point's four support
decisions from the canonical tolerance-selection request. Its independent verifier
reconstructs every member once, delegates member comparison to the focused truncation
verification assessor, and derives expected decision identities through
`Periodic1DRank2TruncationToleranceSelectionIndependentReferenceAnalyzer` without
calling either production selector. This adapter-specific verification does not assign
a generic scientific tolerance or authenticity claim to the family base.

These nominal analysis contracts and derived classifications do not become retained
evidence identities. Hamiltonian and band errors after a cutoff are consequences of
real-space support truncation; they are not spectral-subspace truncation errors.

Current nominal assignments:

- the dimension- and rank-independent `RealSpaceSupportTruncationFamily`;
- `Periodic1DRank2SupportTruncationAnalysis` (also available through the historical
  identical alias `Periodic1DRank2TruncationAnalysis`),
  `Periodic1DRank2TruncationRange`, the support adapter
  `Periodic1DRank2TruncationToleranceSelector`, and the parent-family
  adapter `Periodic1DRank2TruncationFamilyAnalysis`;
- `Periodic1DRankNSupportResult` and the request-bound
  `Periodic1DRankNLocalityAnalysis`; and
- `BandEquivalenceLocalityShellAnalysis` for complete metric shells in the maintained
  2D/3D owner; and
- `RealSpaceSupportTruncationToleranceSelector` and its immutable support-selection
  values, shared by 1D, 2D, and 3D family adapters.

### Numerical consistency

`ksdft2effmass.numerical_consistency.NumericalConsistency` identifies agreement or
stability under one explicitly named finite numerical variation or independent route.

Interpolation, Fourier reconstruction, Parseval balance, mesh refinement, eigensolver
residuals, and independent-route defects remain separate channels. This domain does not
supply a universal score or tolerance and does not convert software agreement into
scientific validation.

`ReciprocalMeshShape` is a rank-independent one-, two-, or three-dimensional axis-size
value. `NestedReciprocalMeshInventory` admits only a common dimension and exact
axiswise integer nesting, with at least one axis strictly refined at every step; it does
not require isotropic refinement. `ReciprocalMeshRefinementFamilyRequest` binds that
mesh inventory to an ordered, unique family-coordinate inventory.
`ReciprocalMeshRefinementFamilyMember` binds one coordinate to one outcome that
nominally inherits `NumericalConsistency`, and `ReciprocalMeshRefinementFamily` enforces
complete order-preserving coverage. These generic values contain no parent-model,
state-space, alignment, threshold, rank, or retained-wire policy. Dimension- and
rank-specific adapters continue to own those semantics and their closed outcome
variants.

Independent family verification remains in memory. Each adapter invokes its existing
independent verifier for every closed member outcome, and
`MemberwiseCompositeVerificationComposer` only supplies stable index prefixes and
composition of the already-produced observations. It performs no scientific
reconstruction and defines no universal comparison tolerance.

Current nominal assignments:

- `PeriodicTensorGridSeparationAnalyzer`, which measures reduced-coordinate torus
  separation without folding that sampling diagnostic into a model error;
- `BandEquivalenceLocalityMetricCovarianceDefectResult`, which retains the
  family-selected 2D or 3D primitive-basis probe identity separately from its maximum
  binary64 squared-length defect; the probe remains campaign-specific rather than a
  universal geometry invariant;
- `ScalarRefinementDiagnostics`;
- the dimension- and rank-independent `ReciprocalMeshRefinementFamily`;
- `Periodic1DRank2MomentumRefinementAnalysis`, its
  `Periodic1DRank2MomentumRefinementFamilyAnalysis` adapter, and
  `Periodic1DRank2AdaptiveAmplitudeAnalysis`;
- `Periodic1DRankNFourierAnalysis`,
  `Periodic1DRankNInterpolationAnalysis`, and
  `Periodic1DRankNRefinementAnalysis`; and
- `BandEquivalenceLocalityRefinementPair`,
  `BandEquivalenceLocalityRefinementAssessment`,
  `BandEquivalenceLocalityAmplitudeMidpointAnalysis`, and
  `BandEquivalenceLocalityFlatAmplitudeResolutionAnalysis`.

The momentum and amplitude outcome unions remain closed, family-specific variants.
Their exact-type admission and existing convergence or exhaustion semantics are
unchanged. Plain 2D/3D refinement and amplitude results gain only nominal ownership;
their retained record projections and canonical mappings remain family-owned.

## Cross-family ownership audit

The current rank-two 1D, rank-$N$ 1D, and rank-two 2D/3D owners crosswalk as follows.
A dash means that the family does not perform a cohesive operation in that domain, not
that evidence has been silently omitted.

| Family | Subspace reduction | Representation equivalence | Hopping locality | Real-space support truncation | Numerical consistency |
|---|---|---|---|---|---|
| rank-two 1D embedded subspace | shared `SpectralReduction` owner upstream; no family-local duplicate | untruncated point analysis | hopping-power values on unchanged coefficients | symmetric-range truncation range and aggregate, with parent-family truncation adapted to the generic truncation family | momentum and adaptive-amplitude refinement, with parent-family momentum refinement adapted to the generic reciprocal-mesh family |
| rank-$N$ 1D alignment | —; retained rank is a model input, not proof of a reduction operation | request-bound frame and represented-operator recovery | symmetric-range coefficient tails and monotonicity on the unchanged Fourier series | symmetric-range support result and locality compatibility aggregate | Fourier reconstruction/Parseval/Hermiticity, shifted interpolation, and mesh refinement |
| rank-two 2D/3D locality | —; the campaign starts from a finite represented parent | typed direct-band, covariance, restricted-alignment, correlation, and threshold result composed by the mixed point aggregate | family-owned shell-power diagnostics | complete metric-shell analysis | covariance-route defect, amplitude resolution, midpoint validation, and adjacent-mesh refinement |

The audit found no competing implementation of Hamiltonian compression, PhysKit
lattice geometry or frame transport, or Project Koios Optimization alignment
algorithms in the nominal-root packages. Dependencies point from family owners toward
the interface-free KSD roots, PhysKit physical primitives, and Optimization numerical
algorithms. None of the six generic roots imports a calculation family.

The family aggregates `Periodic1DRank2Analysis`,
`Periodic1DRankNAlignmentCalculationResult`,
`BandEquivalenceLocalityPointAnalysis`, `BandEquivalenceLocalityCaseAnalysis`, and
`BandEquivalenceLocalityAnalysis` intentionally remain outside these roots because
they combine several scientific operations or evidence channels. Assigning one of
these aggregates to a single root would erase distinctions rather than clarify
ownership.

The former 2D/3D representation-equivalence gap is resolved by an immutable plain
scientific result composed inside `BandEquivalenceLocalityPointAnalysis`. The retained
`PointDiagnostic` continues to project its historical scalar fields, so no field named
`representation_equivalence` enters canonical bytes. No universal cross-family
analysis aggregate is recommended.

## Dependency direction

The intended dependency direction is:

1. Project Koios Optimization supplies unit-free numerical algorithms;
2. PhysKit supplies reusable physical geometry, frame transport, and lattice
   primitives;
3. KSD domain packages supply scientific interpretation, admission, thresholds, and
   immutable results; and
4. calculation-family packages compose these domains into requests, aggregate records,
   verification, and evidence identities.

The six generic nominal roots have no dependency on periodic calculation families,
serialization, plotting, or workflow code.

## Retained-byte and migration rule

Nominal inheritance does not alter dataclass fields, `_mapping()` output, `to_dict()`,
canonical `to_json()`, or any closed wire variant. Existing retained serializers remain
the byte owners. The generic reciprocal-mesh and real-space-support-truncation families
and their rank-two 1D adapters are in-memory scientific values and create no retained
schema or canonical bytes. A future field or schema change requires an explicitly
versioned record rather than reinterpretation of historical bytes.

Migration proceeds by extracting one scientifically cohesive owner at a time. A class
that combines multiple domains is not assigned to whichever root is most convenient;
it is split or projected into immutable domain results while its family aggregate and
evidence identity remain intact.

## Evidence boundary

The nominal-root tests establish importability and inheritance without structural
admission. Focused geometry tests establish the declared 1D direct/reciprocal types and
finite $q \leftrightarrow k$ conversion. Focused family tests also establish that the
new derived geometry and support projections leave selected canonical typed bytes
unchanged. These software checks do not establish complete historical scalar parity,
numerical convergence, scientific correctness, or authentication of retained
calculations. Those checks remain required for each subsequent family migration.
