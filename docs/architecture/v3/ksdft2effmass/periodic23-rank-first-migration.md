# Periodic-2D and periodic-3D rank-first capability migration

## Status and claim boundary

This record defines a source-ownership migration. It is not a calculated result,
numerical verification, scientific validation, retained execution, sealing decision, or
publication claim. Existing calculation artifacts retain their original identities and
evidence status.

The migration extends the accepted periodic-1D capability organization to applicable
periodic-2D and periodic-3D capabilities. Mirroring means aligned ownership roles and
class-name vocabulary, not an assertion that dimensional scientific models, meshes,
topological diagnostics, or support geometries are interchangeable.

## Dimensional bases

Each dimension owns one nominal base that fixes only the PhysKit lattice dimension:

- `Periodic1DCapability` fixes `LatticeDimension.ONE`;
- `Periodic2DCapability` fixes `LatticeDimension.TWO`; and
- `Periodic3DCapability` fixes `LatticeDimension.THREE`.

These bases do not choose lattice vectors, physical distances, units, reciprocal
coordinates, meshes, represented bases, gauges, translation inventories, support
policies, algorithms, tolerances, or wire formats.

Dimension-owned geometry uses the exact PhysKit lattice types. The immutable
`Periodic2DLatticeGeometry` snapshots and reconstructs `DirectLattice2D` and derives
`ReciprocalLattice2D`; `Periodic3DLatticeGeometry` does the same with
`DirectLattice3D` and `ReciprocalLattice3D`. Primitive vectors are columns, and the
direct and reciprocal bases satisfy $A^{\mathsf T}B=2\pi I$. Translation indices remain
integer coordinates until these geometry owners map them through the direct lattice;
they do not imply Cartesian distances by themselves.

Applicable capability bases mirror the periodic-1D names by replacing only the
dimensional prefix:

| Periodic-1D owner | Periodic-2D owner | Periodic-3D owner |
|---|---|---|
| `Periodic1DLatticeGeometry` | `Periodic2DLatticeGeometry` | `Periodic3DLatticeGeometry` |
| `Periodic1DBandEquivalence` | `Periodic2DBandEquivalence` | `Periodic3DBandEquivalence` |
| `Periodic1DBandEquivalenceRequest` | `Periodic2DBandEquivalenceRequest` | `Periodic3DBandEquivalenceRequest` |
| `Periodic1DBandEquivalenceAnalysis` | `Periodic2DBandEquivalenceAnalysis` | `Periodic3DBandEquivalenceAnalysis` |
| `Periodic1DBandEquivalenceAnalyzer` | `Periodic2DBandEquivalenceAnalyzer` | `Periodic3DBandEquivalenceAnalyzer` |
| `Periodic1DGaugeAlignment` | `Periodic2DGaugeAlignment` | `Periodic3DGaugeAlignment` |
| `Periodic1DGaugeAlignmentAnalysisRequest` | `Periodic2DGaugeAlignmentAnalysisRequest` | `Periodic3DGaugeAlignmentAnalysisRequest` |
| `Periodic1DGaugeAlignmentAnalysis` | `Periodic2DGaugeAlignmentAnalysis` | `Periodic3DGaugeAlignmentAnalysis` |
| `Periodic1DGaugeAlignmentAnalyzer` | `Periodic2DGaugeAlignmentAnalyzer` | `Periodic3DGaugeAlignmentAnalyzer` |
| `Periodic1DHoppingLocality` | `Periodic2DHoppingLocality` | `Periodic3DHoppingLocality` |
| `Periodic1DHoppingLocalityAnalysisRequest` | `Periodic2DHoppingLocalityAnalysisRequest` | `Periodic3DHoppingLocalityAnalysisRequest` |
| `Periodic1DHoppingLocalityAnalysis` | `Periodic2DHoppingLocalityAnalysis` | `Periodic3DHoppingLocalityAnalysis` |
| `Periodic1DHoppingLocalityAnalyzer` | `Periodic2DHoppingLocalityAnalyzer` | `Periodic3DHoppingLocalityAnalyzer` |
| `Periodic1DSupportTruncation` | `Periodic2DSupportTruncation` | `Periodic3DSupportTruncation` |
| `Periodic1DSupportTruncationAnalysisRequest` | `Periodic2DSupportTruncationAnalysisRequest` | `Periodic3DSupportTruncationAnalysisRequest` |
| `Periodic1DSupportTruncationAnalysis` | `Periodic2DSupportTruncationAnalysis` | `Periodic3DSupportTruncationAnalysis` |
| `Periodic1DSupportTruncationAnalyzer` | `Periodic2DSupportTruncationAnalyzer` | `Periodic3DSupportTruncationAnalyzer` |

## Rank-first naming rule

Applicable rank-specific classes preserve the complete periodic-1D role name and replace
only the dimension prefix. Rank-two and arbitrary-finite-rank roles additionally mirror
one another by replacing only `Rank2` with `RankN`. For example:

- `Periodic1DRank2HoppingLocalityAnalyzer` maps to
  `Periodic2DRank2HoppingLocalityAnalyzer` and
  `Periodic3DRank2HoppingLocalityAnalyzer`;
- `Periodic1DRankNTransportAnalysisRequest` maps to
  `Periodic2DRankNTransportAnalysisRequest` and
  `Periodic3DRankNTransportAnalysisRequest`; and
- rank-two and rank-N support-truncation requests, analyses, analyzers, and results use
  the same suffix vocabulary within each dimension.

Band-equivalence ownership follows domain → periodic → dimension → rank before a
concrete study implementation. Rank nominal capabilities are abstract through their
band-subspace contracts and cannot be constructed as empty scientific objects. Each
dimension therefore owns matching `Rank1`, `Rank2`,
and `RankN` nominal, request, analysis, and analyzer roles. Existing concrete study
classes inherit those rank roles directly: the periodic-1D Fourier-locality calculation
provides the installed rank-one implementation, while the rank-two and rank-N
band-equivalence/hopping-locality studies provide the corresponding higher-rank
implementations. Their existing state and calculation behavior remain authoritative;
the rank layer adds in-memory ownership rather than duplicate producers or wire records.
Serialization remains an IO concern of the existing record owners and is not required by
capability inheritance. Rank capability and analyzer owners are abstract; existing
state-bearing study request and analysis classes remain the concrete operational surfaces.
Periodic-2D and periodic-3D rank-one namespaces remain inert because no
rank-one scientific study is installed there.

The rank vocabulary identifies the band-subspace rank at each momentum, not the
periodic lattice dimension, the ambient parent-state dimension, or a matrix's numerical
rank. Fixed-rank owners expose `band_subspace_rank`; rank-N capabilities, requests, and
analyses expose their `band_subspace_ranks` inventory. These scientific properties make
the nominal capability owners abstract without introducing role identifiers or empty
marker constructors. Concrete model-reduction studies retain their separate
`retained_rank` fields where that provenance is scientifically applicable.

Rank-two classes do not inherit from rank-N classes merely because two is a finite rank.
Both specializations are sibling branches beneath the applicable dimensional
band-equivalence owner and then support their existing concrete aggregate studies.

A retained rank such as four is a value admitted by an applicable rank-N request; it
does not create a `rank4` source namespace. The `periodic2d/rankN` and
`periodic3d/rankN` namespaces currently install the reviewed analytic parent/gauge,
global/pointwise-Procrustes, frame-transport, hopping-locality, support-truncation,
typed-request, case-expansion, aggregate-analysis, immutable aggregate-result, and
bounded independent parent/alignment/transport/Fourier/shell-power/support-selection
reference foundations and typed aggregate verification. Visualization and lifecycle
owners remain absent because the exact rank/depth/case/alignment visualization operands,
invariant reductions, authenticated plot inventory, and bounded rendering resource
envelope have not been selected.
Periodic-1D rank-N vocabulary
is a naming and ownership donor, not authority
to copy one-dimensional algorithms into higher dimensions. The shared decision checklist
is recorded in
[`periodic23-rankN-protocol-selection.md`](periodic23-rankN-protocol-selection.md),
while the eventual scientific selections are owned by
`calculations/periodic2d/rankN/` and `calculations/periodic3d/rankN/`.

## Dependency ownership and reuse

The migration composes installed Project Koios owners rather than recreating their
algorithms:

- PhysKit owns `DirectLattice2D`, `DirectLattice3D`, their reciprocal lattices,
  `DirectLatticeMetric`, finite lattice coordinates and displacements, block hopping
  models, and block-hopping power diagnostics.
- Numerics owns `CenteredUniformMesh`, finite-periodic Fourier transforms and series
  evaluation, Parseval and mesh-Hermiticity diagnostics, immutable NumPy admission,
  Frobenius operations, and complete Hermitian spectra where their contracts apply.
- Optimization owns complex-unitary Procrustes selection, batched NumPy Procrustes
  execution, closed-loop polar transport, and periodic-harmonic optimization.
- KSD retains the scientific request identity, parent-model composition, represented
  state-space alignment, dimension-specific reciprocal-neighbor topology, physical
  metric-shell policy, truncation decisions, tolerances, claim boundaries, retained
  records, lifecycle verification, and authenticated rendering.

A rank-first class may adapt one of these owners to a KSD scientific contract, but it
must not reproduce the dependency's numerical implementation. Independent references
remain independent verification routes rather than production replacements.

## Shared and dimension-owned behavior

Truly dimension-independent numerical arithmetic may remain under a common scientific
owner. Public requests, analyses, results, verification, retained records, and
visualizations that bind a two- or three-dimensional lattice domain belong under the
corresponding `periodic2d` or `periodic3d` rank-first namespace.

The installed `band_equivalence_hopping_locality.rankN` namespace owns the common
periodic rank-N aggregate roles, dimension-neutral leaf-result validation, shared
production Fourier mechanics, and separately implemented independent-reference
arithmetic. The periodic-2D and periodic-3D roles inherit those common contracts
additively while remaining sibling dimensional specializations. Their concrete requests,
analyses, analyzers, results, exact type admission, geometry and topology selections, and
wire identities remain dimension-owned. Production and reference owners are separate;
sharing across spatial dimensions does not make the verifying route call the producer
for the quantity under comparison. This ownership extraction changes no selected
formula or numerical result.

The shared `band_equivalence_hopping_locality` implementation is therefore
migration input rather than the final owner for dimension- and rank-bound public types.
The migration must keep representation equivalence, gauge alignment, frame transport,
hopping-locality diagnostics, and irreversible support truncation scientifically
distinct.

The periodic-2D and periodic-3D rank-two restricted gauge-alignment owners bind two
immutable represented rank-two matrix fields on one tensor-product mesh. They declare a
right action, Euclidean inner product, and retained `U(2)` state-space identity, while
the calculation itself optimizes only the reviewed global real-rotation subgroup. This
restricted global action is not pointwise Procrustes alignment, frame transport,
representation equivalence, or a claim that the singular vectors are physical. The
aggregate band-equivalence/locality action routes the restricted correlation and
operator-threshold calculation through the dimensional owner.

The rank-two pointwise Procrustes owners bind immutable correlated source and target
frame fields, a right `U(2)` action, Euclidean inner product, and the exact Project Koios
numerical-rank and backend-validation policy. Their results retain the dependency-owned
polar factors, complete singular spectra, numerical ranks, residuals, cutoffs, and
backend identity. They do not retain or assign physical meaning to SVD singular vectors,
and rank-deficient completions remain diagnostic rather than unique alignment evidence.

The rank-two frame-transport owners bind an immutable raw retained-frame field and
compose those pointwise owners along each nearest-neighbor axis. They own the
periodic-2D or periodic-3D neighbor topology, link aggregation, loop-closure diagnostics,
and plaquette diagnostics. Closure and plaquette quantities are inapplicable when any
link is numerically rank deficient, with a typed stable reason. These diagnostic actions
do not construct a globally transported higher-dimensional gauge.

The periodic-2D and periodic-3D rank-two hopping-locality owners bind exactly one
reference or comparison channel to an unchanged ordinary Fourier-block inventory. They
use the selected physical-metric shell labels and delegate raw block powers to PhysKit.
Their analyses retain normalized squared Frobenius powers without deleting support.
Twisted-Nyquist contributions remain separate diagnostics, and support-truncation errors
remain separate capability results. The aggregate band-equivalence/locality action now
routes these ordinary-hopping measurements through the dimensional rank-two owners while
retaining common arithmetic internally.

Dimension-qualified rank-two execution, execution-verification, and rendering records
now bind the exact orthogonal or nonorthogonal calculation family to its reviewed study
family. Verification records require dimension-owned authenticated visualization data.
Their wire mappings remain identical to the established direct-lifecycle schema, so
historical periodic-2D unsealed bytes readmit canonically without changing producer
identity, evidence status, sealing status, or scientific claims. Calculation-root scripts
use these rank-first records; historical retained producer scripts remain immutable
provenance.

The periodic-2D and periodic-3D rank-two support-truncation decision owners likewise bind
one reference or comparison channel, one nested metric-shell support inventory, its
calculated total-error sequence, and one tolerance. Matrix-Frobenius and ordered-band
criteria produce separate typed minimum-support or unresolved outcomes. The aggregate
action routes each channel through these owners and only then assembles its historical
paired decision record. This extraction owns the irreversible support-selection policy;
shared finite-periodic evaluation arithmetic may still construct the truncated fields
from which the error sequence is calculated.

## Migration order

1. Install dimensional capability bases and mirrored capability-role bases.
2. Establish inert `rank2` and `rankN` namespaces and automated naming checks.
3. Move rank-two band-equivalence/locality requests, analyses, results, independent
   reference actions, verification actions, authenticated visualization data, and
   visualizers, execution records, execution-verification records, and rendering records
   into each dimensional owner. Generic verification thresholds, plot inventories, and
   wire-schema mechanics may remain shared internally when they bind no dimensional
   scientific choice.
4. Extract gauge alignment, frame transport, hopping locality, and support truncation
   behind their corresponding dimensional bases.
5. Add rank-N specializations only where a finite-rank scientific contract is selected;
   do not create direct calculation entrypoints for an unselected study.
6. Update calculation scripts and tests to import authoritative rank-first modules
   directly, then remove obsolete shared public routes rather than preserving aliases.
7. Validate each calculation family independently. Shared implementation does not merge
   execution identity, retained evidence, or scientific conclusions.

## Current completion boundary

For the selected periodic-2D and periodic-3D rank-two band-equivalence/locality
protocols, rank-first public ownership now covers requests, aggregate analyses and
results, restricted gauge alignment, pointwise Procrustes, frame-transport diagnostics,
hopping-locality diagnostics, support-selection decisions, independent references,
verification actions, authenticated visualization data and rendering actions, execution
records, execution-verification records, and rendering records. Shared modules retain
common arithmetic, dimension-neutral thresholds and plot inventories, and common wire
schema mechanics; they are not alternative public study identities.

This completion statement applies only to installed software contracts. It does not
establish numerical convergence, scientific validation, retained evidence for an
unexecuted study, sealing, publication, or a completed rank-N lifecycle. Periodic-2D and
periodic-3D rank-N currently provide analytic parent/gauge, global/pointwise-Procrustes,
frame-transport, hopping-locality, support-truncation, typed-request, case-expansion,
aggregate-analysis, immutable aggregate-result, and bounded independent parent,
alignment, transport, Fourier, shell-power, and support-selection references plus typed
aggregate verification; visualization, lifecycle, and retained-study ownership remain
pending the dimension-specific projection and resource contracts.

No production or retained calculation is authorized by this migration record.
