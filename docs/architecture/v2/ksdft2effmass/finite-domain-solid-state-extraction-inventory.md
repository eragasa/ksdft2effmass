# Solid-state extraction inventory for one, two, and three dimensions

## Status and boundary

This is an execution-free implementation-planning inventory requested after adoption of
the finite-domain scientific design. It lists the reusable solid-state concepts visible
in the maintained defect-1D calculations, the accepted defect-2D implementation, and
the accepted finite-domain design, then states how each concept must extend across one,
two, and three spatial dimensions.

“Complete” means complete for those inspected sources and the accepted finite-domain
scope. It does not pre-authorize phonons, electron--phonon coupling, topology,
many-body models, multi-orbital defect-2D work, spin generalization, material-specific
DFT, production Wannier90, implementation, or calculation execution.

HC20 selected the broad `ksdft2effmass.solid_state` composition aggregate. The tables'
earlier focused-owner labels are interpreted as cohesive responsibilities inside that
selected aggregate; types must not be duplicated across structures, electronic
structure, operators, analysis, or campaigns. HC21 further selects dimension-specific
lattice-system types factored from conventional-cell `P/C/I/F/R` centering.

## Dimensional representation rule

Spatial dimension is a closed domain with values one, two, and three. Public contracts
must not accept an unconstrained arbitrary-length coordinate sequence. A proposed
implementation may use one immutable dimension-tagged record with a closed union of
exact coordinate shapes, or three concrete records behind a closed protocol, but it
must satisfy all of the following:

- 1D integer vectors contain exactly one component;
- 2D integer vectors contain exactly two components;
- 3D integer vectors contain exactly three components;
- shapes contain positive built-in integers and reject booleans;
- twist components are finite built-in floats in turns;
- matrix-valued point operations are exactly $d\times d$ built-in-integer matrices;
- site ordering is explicit and fixed as the last axis varying fastest;
- tensor-product dimension and matrix dimension use checked products;
- units, basis identity, energy reference, gauge, geometry, and ordering are explicit;
- a twist lift in $\mathbb R^d$ and its representative in
  $\mathbb R^d/\mathbb Z^d$ are different represented values; and
- dimensional conversion never pads with zero axes or silently drops axes.

The proposed closed coordinate aliases are conceptually:

- 1D: $(x)$ and $(R_x)$;
- 2D: $(x,y)$ and $(R_x,R_y)$; and
- 3D: $(x,y,z)$ and $(R_x,R_y,R_z)$.

These are lattice-index coordinates and displacements, not Cartesian atomic positions
in bohr. A future bridge to `PeriodicStructure` requires an explicit lattice-to-cell
map and is not part of this extraction.

## Extraction inventory

### 1. Dimension, coordinates, and finite lattice geometry

| Capability to extract | Proposed owner and object kind | 1D | 2D | 3D |
|---|---|---|---|---|
| Closed spatial dimension | `LatticeDimension`, immutable enum/value | one axis | two axes | three axes |
| Integer lattice coordinate | `LatticeCoordinate`, DataObject | $(x)$ | $(x,y)$ | $(x,y,z)$ |
| Integer lattice displacement | `LatticeDisplacement`, DataObject | $(R_x)$ | $(R_x,R_y)$ | $(R_x,R_y,R_z)$ |
| Finite periodic shape | `FiniteLatticeShape`, DataObject | $(N_x)$ | $(N_x,N_y)$ | $(N_x,N_y,N_z)$ |
| Cell count | intrinsic shape property | length | area | volume |
| Canonical tensor-product ordering | `LatticeSiteOrdering`, DataObject/enum | $x$ | $x$ outer, $y$ inner | $x$ outer, $y$ middle, $z$ inner |
| Coordinate-to-index map | `FiniteLatticeIndexer`, ActionObject | one stride | two strides | three strides |
| Periodic wrap and quotient vector | `PeriodicImageResolver`, ActionObject returning `PeriodicImageResult` | one quotient | two quotients | three quotients |
| Defect origin and translated placement | `LatticePlacement`, DataObject and `LatticePlacementTransformer` | scalar translation | integer 2-vector | integer 3-vector |
| Minimum-image displacement | `MinimumImageResolver`, ActionObject | signed ring distance | torus displacement | three-torus displacement |
| Core and shell membership | `LatticeNeighborhood` DataObject plus `LatticeNeighborhoodSelector` | intervals | declared 2D norm/shell | declared 3D norm/shell |
| Geometry identity | field on finite representation DataObject | exact length identity | exact ordered shape identity | exact ordered shape identity |

Source concepts include defect-1D `SupercellBasis`, `FoldingControl`, and
`FiniteSizeControl`; defect-2D `ParentControls`, index arithmetic, radius-two shells,
and fixed-area geometry sets. Geometry equality must include dimension, ordered shape,
origin convention, site ordering, and boundary identification. Equal cell counts do not
make geometries compatible.

### 2. Boundary twists, fibers, and meshes

| Capability to extract | Proposed owner and object kind | Dimensional extension |
|---|---|---|
| Unreduced twist lift | `BoundaryTwistLift`, DataObject | one, two, or three finite components in turns |
| Quotient representative | `BoundaryTwistRepresentative`, DataObject | canonical componentwise representative in the declared half-open interval |
| Lift reduction | `BoundaryTwistReducer`, ActionObject | subtract an integer vector; return representative and quotient |
| Twist fiber identity | `TwistFiber`, DataObject | binds dimension, geometry, lift/representative role, gauge, basis, and ordering |
| Complete tensor-product twist mesh | `BoundaryTwistMesh`, DataObject | $n_x$, $n_xn_y$, or $n_xn_yn_z$ points with explicit nesting order |
| Twist transformation | `BoundaryTwistTransformer`, ActionObject | apply an exact integral $d\times d$ lattice operation before declared reduction |
| Boundary-crossing phase | owned by the operator constructor | $\exp[2\pi i\,q\cdot\phi]$ for $q,\phi\in\mathbb R^d$ |
| Uniform-link phase | owned by the production constructor | $\exp[2\pi i\,\phi\cdot R/N]$ componentwise in $d$ axes |
| Twist-distribution summary | analysis ResultObject | center, width, counts, and complete per-fiber records in every dimension |

A boundary-twist mesh is unweighted finite-domain sampling and is not
`KPointSampling`. No implicit conversion is allowed. If a later adapter is required,
it must state reciprocal scale, weights, normalization, lattice map, and whether the
points label primitive Bloch fibers or finite-supercell boundary conditions.

### 3. Translation-invariant parent lattice models

| Capability to extract | Proposed owner and object kind | Dimensional extension |
|---|---|---|
| Scalar hopping term | `ScalarHoppingTerm`, DataObject | displacement has dimension $d$; value is a finite complex energy quantity |
| Canonical hopping inventory | `ScalarHoppingModel`, DataObject | unique lexicographically ordered displacements in $\mathbb Z^d$ |
| Hermitian partner analysis | `HoppingHermiticityAnalyzer`, ActionObject with ResultObject | compare $h_{-R}$ with $h_R^*$ under explicit tolerance |
| Support/range metadata | `HoppingSupport`, DataObject | explicit displacement set plus declared norm/radius policy |
| Range truncation | `HoppingModelTruncator`, ActionObject with residual ResultObject | dimension-independent predicate over declared support metric |
| Axis permutation/reflection | `HoppingModelTransformer`, ActionObject | exact integral operation on every displacement |
| Symmetry covariance | `HoppingSymmetryAnalyzer`, ActionObject | group supplied explicitly; do not infer 1D reflection, 2D $D_4$, or 3D cubic symmetry |
| Bloch fiber evaluation | `BlochHamiltonianEvaluator`, ActionObject | evaluate $\sum_R h_R e^{2\pi i k\cdot R}$ for identified dimension and convention |
| Reciprocal-sample Fourier reconstruction | `HoppingModelReconstructor`, ActionObject with reconstruction residual | one-, two-, or three-dimensional explicit tensor-product sum |
| Canonical content identity | serializer/digest ActionObject | includes dimension, ordering, units, energy reference, rank, and every term |
| Parent bandwidth and edge metadata | analysis ResultObject | derived from an identified parent and declared sampling, never intrinsic unverified fields |

Sources include defect-1D scalar and composite hopping records, analytical-oracle
`HoppingBlock`, independent-route hopping records, defect-2D `ParentHopping`,
`ParentHoppingConstructor`, and accepted parent-truncation diagnostics.

The first implementation slice remains scalar rank one because that is the shared
accepted 1D/2D capability needed by finite-domain effects. Matrix-valued hopping blocks
must be inventoried but deferred as described below; scalar APIs must not be widened to
untyped arrays in anticipation of them.

### 4. Localized perturbations and defect support

| Capability to extract | Proposed owner and object kind | Dimensional extension |
|---|---|---|
| Localized onsite term | `LocalizedOnsiteTerm`, DataObject | one lattice coordinate and finite energy value in $d$ dimensions |
| Directed bond term | `LocalizedBondTerm`, DataObject | start coordinate plus nonzero $d$-dimensional displacement |
| Hermitian completion policy | explicit enum/value on construction request | include declared reverse term or require a complete input inventory |
| Localized perturbation inventory | `LocalizedPerturbation`, DataObject | deterministic term order, one geometry/basis/unit/reference |
| Support identity | `LocalizedSupport`, DataObject | coordinate and bond support relative to an identified origin |
| Perturbation transform | `LocalizedPerturbationTransformer`, ActionObject | transform starts and displacements under an exact lattice operation and translation |
| Perturbation operator construction | `LocalizedPerturbationOperatorConstructor`, ActionObject | sparse represented operator in the declared twist gauge |
| Support comparison | `LocalizedSupportComparator`, ActionObject | exact support equality only after compatible geometry and alignment |

Sources include defect-1D scalar onsite, orbital onsite, nearest-neighbor, range-two,
Gaussian-profile, and finite-support cases; defect-2D `LocalBond`, directional
nearest-neighbor terms, and diagonal range-two terms.

Gaussian profiles, fixed-peak/fixed-integrated normalization, and named defect model
classes remain analysis or campaign policy. The generic extraction owns represented
localized terms and support, not the scientific claim that one inventory is the right
impurity model.

### 5. Integral lattice operations and orientation

| Capability to extract | Proposed owner and object kind | Dimensional extension |
|---|---|---|
| Integral lattice operation | `IntegralLatticeOperation`, DataObject | exact $1\times1$, $2\times2$, or $3\times3$ integer matrix plus identifier |
| Operation validation | intrinsic exact determinant/integer checks where contract requires | typically determinant $\pm1$; accepted subgroup supplied separately |
| Finite-geometry compatibility | `LatticeOperationCompatibilityAuditor`, ActionObject | verify source and target ordered shapes under the operation |
| Site permutation | `FiniteLatticePermutationConstructor`, ActionObject | sparse permutation over $N_x$, $N_xN_y$, or $N_xN_yN_z$ sites |
| Orientation pair | `LatticeOrientationPair`, DataObject | identifies source geometry, target geometry, operation, and twist map |
| Same-parent contrast | analysis ResultObject | physical contrast; no zero expectation |
| Swapped/transformed-parent covariance | analysis ResultObject | algebraic criterion against a separately identified transformed parent |

No dimension receives an implicit symmetry group. Reflection in 1D, rectangular and
square groups in 2D, and orthorhombic or cubic groups in 3D must be supplied as exact
operation inventories by the scientific contract.

### 6. Gauge representations and bridges

| Capability to extract | Proposed owner and object kind | Dimensional extension |
|---|---|---|
| Twist-gauge declaration | `TwistGaugeRepresentation`, closed enum/value | centered uniform-link and quotient seam are initially supported |
| Site-diagonal gauge bridge | `TwistGaugeBridgeConstructor`, ActionObject | phase depends on $r\cdot\phi/N$ across $d$ axes |
| Gauge bridge result | `TwistGaugeBridgeResult`, ResultObject | source/target fibers, sparse diagonal unitary, convention identities |
| Gauge-equivalence comparison | `TwistGaugeEquivalenceAnalyzer`, ActionObject | bridge before matrix residual; never compare raw matrices from different gauges |
| Negative fixed-twist control | campaign verification action | operation must transform the twist fiber rather than hold a generic twist fixed |

Production and independent verification cannot import the same bridge or operator
construction algorithm. Shared DataObjects and serialized contracts are allowed;
shared numerical mechanics are not.

### 7. Finite represented operator construction

| Capability to extract | Proposed owner and object kind | Dimensional extension |
|---|---|---|
| Parent supercell construction | `TwistedSupercellOperatorConstructor`, ActionObject | sparse assembly over dimension-generic wrap, quotient, hopping, and phase records |
| Seam-gauge construction | independent verifier implementation, not production import | Kronecker/seam route generalized independently to 1D/2D/3D |
| Parent-plus-defect composition | existing operator composition or narrow lattice-model action | requires exact represented compatibility before addition |
| Represented basis metadata | reuse/extend operator representation metadata | state space, geometry, cell/orbital/spin ordering, gauge, unit, energy reference, subspace |
| Sparse storage | `ComplexSparseMatrixQuantity` in `ksdft2effmass.operators` | canonical complex128 CSR; no pre-diagonalization dense conversion |
| Hermiticity analysis | existing operator analyzer | fixed representation and explicit tolerance |
| Compatible differencing | existing operator differencer | only same dimension, geometry, basis, gauge, unit, and energy reference |
| Eigensolution | existing operator eigensolver where contract fits | sparse selected states; unsupported complete sparse spectra rejected rather than densified |

The lattice-model owner constructs a scientifically identified represented operator by
consuming generic operator records. `ksdft2effmass.operators` must not import the
lattice-model package or acquire hopping, twist, or impurity policy.

### 8. Primitive-to-supercell folding and route reconciliation

| Capability to extract | Proposed owner and object kind | Dimensional extension |
|---|---|---|
| Primitive/supercell index relation | `LatticeFoldingMap`, DataObject | integer fold along one, two, or three axes |
| Reduced momentum/fiber labels | explicit DataObject distinct from boundary twist | $d$ components with declared reciprocal convention |
| Folding operator | `BlochFiberFoldingConstructor`, ActionObject | normalized tensor-product Fourier map in $d$ dimensions |
| Folding verification | `BlochFiberFoldingAnalyzer`, ActionObject | unitarity, block reconstruction, spectral agreement, and ordering diagnostics |
| Real-space extraction route | analysis ActionObject | compatible aligned parent/doped operators in one finite representation |
| Bloch-fiber extraction route | independent analysis ActionObject | reconstruct through fibers without calling the real-space route |
| Route reconciliation | analysis ResultObject | residuals and provenance for both routes; no averaging or voting |

Sources include defect-1D `FoldingControl`, analytical-oracle supercell construction,
independent real-space and Bloch-fiber routes, and defect-2D folding and two-route gauge
checks. Folding maps must not be represented as boundary-twist meshes merely because
both use Fourier phases.

### 9. Alignment and represented compatibility

| Capability to extract or reuse | Owner | Dimensional extension |
|---|---|---|
| Exact represented compatibility | extend/reuse `ksdft2effmass.operators` compatibility | dimension and every basis/geometry/gauge/unit/reference field must agree |
| Translation alignment | analysis ActionObject | one-, two-, or three-component lattice translation |
| Site permutation alignment | analysis ActionObject | exact finite-lattice permutation |
| Site-phase synchronization | analysis ActionObject | graph over nonzero pristine hoppings in any dimension; disconnected/tied cases stop |
| Energy-reference alignment | analysis ActionObject | explicit scalar conversion with retained identity |
| Basis/orbital unitary alignment | deferred analysis contract | required for matrix-valued rank greater than one |
| Spin-frame alignment | deferred analysis contract | required only with separately authorized spin models |
| Alignment result | ResultObject | selected map, singular values/residuals, ambiguity and stop codes |

Defect-1D `SupercellBasis` and `OperatorCompatibilityAnalyzer` demonstrate required
metadata, while blind alignment and independent-route studies demonstrate translation,
permutation, phase, orbital, spin, and energy-reference attacks. Only scalar spatial
alignment is in the initial finite-domain slice. Existing generic represented-operator
records should be extended or adapted rather than duplicated.

### 10. Locality and residual analysis

| Capability to extract | Proposed owner | Dimensional extension |
|---|---|---|
| Core index set | analysis DataObject/ResultObject | radius around aligned origin using a declared norm and minimum-image convention |
| Shell partition | analysis ActionObject | 1D shells, 2D shells, or 3D shells under one explicitly named metric |
| Core restriction residual | analysis ResultObject | same represented geometry only |
| Exterior residual | analysis ResultObject | complement of declared core |
| Core--exterior coupling | analysis ResultObject | both off-diagonal blocks, Frobenius combined explicitly |
| Maximum-entry residual | existing operator residual mechanics | dimension independent |
| Frobenius residual | existing operator residual mechanics | dimension independent |
| Spectral residual | existing operator residual mechanics | dimension independent |
| Support digest/equality | serializer or support analyzer | structural support, not a substitute for coefficient residuals |
| Model-class fit | analysis ActionObject | candidate basis supplied by the scientific contract; retain every rejected fit |

Radius is not one universal notion. Hopping truncation may use squared Euclidean
lattice displacement, while local shells may use Chebyshev minimum-image distance.
Every record must name its metric. A generic `radius` field without metric identity is
forbidden.

### 11. Spectral, bound-state, and localization diagnostics

| Capability to extract | Proposed owner | 1D | 2D | 3D |
|---|---|---|---|---|
| Host edge and bandwidth | analysis ResultObject | scalar | scalar | scalar |
| Host-edge-referenced binding energy | analysis ResultObject | supported | supported | supported |
| Below-edge state count | analysis ResultObject | supported | supported | supported |
| No-bound-state status | explicit ResultObject status | retained | retained | retained |
| Eigenpair residual | operator/analysis result | supported | supported | supported |
| Degenerate-state projector | existing subspace owner plus analysis policy | fiber-local only | fiber-local only | fiber-local only |
| Core probability | analysis ActionObject | interval core | planar core | volumetric core |
| Inverse participation ratio | analysis ActionObject | scalar | scalar | scalar |
| RMS localization radii | analysis ResultObject | $r_x$ | $(r_x,r_y)$ | $(r_x,r_y,r_z)$ |
| Center of probability | analysis ResultObject | one component | two components | three components |
| Quadrupole/second-moment anisotropy | analysis ResultObject | one value with no orientation claim | symmetric $2\times2$ tensor/invariants | symmetric $3\times3$ tensor/invariants |
| Twist defect-band summary | analysis ResultObject | complete 1D mesh | complete 2D mesh | complete 3D mesh |

Individual eigenvectors are never compared across different twist fibers. Degenerate
states within one fiber use projectors with cluster ranks fixed from the parent before
observing the defect result.

### 12. Finite-domain study channels

| Channel | Reusable study records/actions | 1D | 2D | 3D |
|---|---|---|---|---|
| Measure scaling | `FiniteDomainMeasureStudy` and ResultObject | length sequence | area sequence | volume sequence |
| Fixed-measure shape | `FiniteDomainShapeStudy` and ResultObject | no nontrivial rectangular shape channel | rectangles at fixed area | boxes at fixed volume |
| Orientation | `FiniteDomainOrientationStudy` and ResultObject | reflection/defect orientation where meaningful | explicit shape/defect/parent operations | explicit shape/defect/parent operations |
| Boundary phase | `BoundaryPhaseStudy` and ResultObject | full twist line | full twist grid | full twist volume |
| Adjacent measure change | analysis ResultObject | final length change | final area change | final volume change |
| Fixed-shape contrasts | analysis ResultObject | generally absent | relative to declared reference rectangle | relative to declared reference box |
| Same-parent orientation contrast | analysis ResultObject | no zero expectation | no zero expectation | no zero expectation |
| Transformed-parent covariance | analysis ResultObject | algebraic criterion | algebraic criterion | algebraic criterion |

The four channels remain separate. Dimension-generic code must not create a pooled
finite-domain convergence result. A missing nontrivial 1D shape channel is represented
as inapplicable by contract, not as a zero effect or empty successful sequence.

### 13. Model-class and continuum analyses that remain above the lattice-model owner

The following are reusable scientific analyses but not intrinsic lattice-model state:

- ordered candidate defect-model classes;
- point-onsite, finite-support onsite, isotropic-nearest-neighbor,
  directional-nearest-neighbor, and finite-range nonlocal basis construction;
- least-squares coefficient recovery over real and imaginary represented entries;
- rank and identifiability findings;
- accepted/rejected fit status and complete residual retention;
- continuum profile families and fixed-peak versus fixed-integrated normalization;
- finite-rank resolvent evaluation and rank-one root resolution;
- operator-versus-observable metric contrast studies;
- finite-size convergence policy and nonmonotonicity reporting; and
- route reconciliation and claim boundaries.

These belong to `ksdft2effmass.analysis` or the exact campaign. They may consume
1D/2D/3D lattice-model records but must not be placed on hopping or geometry
DataObjects.

### 14. Serialization, provenance, campaign, and execution boundaries

Extract only generic wire behavior when a reusable persisted contract is actually
required:

- lattice-model serializers own dimension, shape, ordering, units, energy reference,
  rank, displacement terms, twist/gauge, and schema version;
- campaign serializers own exact area/shape/orientation/twist case inventories,
  thresholds, channel results, and historical compatibility;
- provenance records bind source artifacts, implementation identities, accepted-input
  identities, and evidence classification;
- Workflows own exact multi-step campaign orchestration;
- thin CLIs contain only typed adaptation into a Workflow; and
- protected-attempt journaling, exclusive output creation, native-root retention, and
  execution authorization remain campaign/execution-control concerns.

Do not extract `StageC...`, `ParentControls`, attempt authorization, retained path
inventories, report/SVG creation, schedule-order attacks, or campaign-specific JSON
shapes into the lattice-model package.

## Initial implementation slice versus deferred inventory

### Extract in the first authorized slice

The minimum shared 1D/2D/3D-capable slice is:

1. closed spatial dimension and exact integer coordinate/displacement records;
2. finite periodic shape, canonical ordering, index/wrap/quotient actions;
3. scalar hopping term and canonical scalar hopping model;
4. localized scalar onsite and bond perturbation terms;
5. twist lift, reduced representative, tensor-product twist mesh, and gauge declaration;
6. integral lattice operation and geometry-compatibility result;
7. sparse uniform-link supercell operator construction;
8. gauge-bridge result contract;
9. explicit represented metadata interoperating with existing operator records; and
10. software-verification tests covering 1D, 2D, and 3D positive and adverse cases.

This first slice establishes software contracts only. It does not establish the
finite-domain numerical result or authorize accepted-parent reads.

### Extract after the core slice, before a finite-domain runner

1. dimension-generic support, minimum-image, core, and shell records;
2. hopping Hermiticity, support, truncation, symmetry, and transform actions;
3. localized perturbation transforms;
4. finite-lattice permutation and twist-transform actions;
5. production gauge equivalence and compatibility analysis;
6. Bloch-fiber evaluation and primitive/supercell folding contracts needed by the
   campaign;
7. finite-domain channel ResultObjects and diagnostics; and
8. campaign-specific input/result serializers and Workflow.

### Defer pending demonstrated reuse or separate authority

- matrix-valued hopping blocks and orbital rank greater than one;
- orbital-frame, subspace, and spin-frame alignment;
- composite-parent degeneracy studies;
- general Neumann, Robin, or continuum periodic boundary conditions;
- non-orthogonal Bravais-coordinate metric tensors;
- magnetic Peierls phases not representable as boundary twists;
- nonsymmorphic space-group operations and fractional translations;
- atomic-crystal to reduced-lattice-model mapping;
- weighted k-point to boundary-twist adapters;
- Wannier90 native-format loading or production Wannierization;
- 3D cubic symmetry defaults, because symmetry must remain explicit;
- GPU/distributed execution; and
- Rust mappings without an accepted cross-language contract.

## Adversarial completeness checks

A later implementation plan is incomplete if it fails any of these attacks:

1. **Dimension laundering:** a generic sequence accepts zero, four, or mixed dimensions.
2. **Boolean laundering:** `True` passes as a shape or integer coordinate.
3. **Axis hard-coding:** 2D `$x,y$` loops remain hidden in supposedly 3D actions.
4. **Ordering drift:** producer and verifier use different last-axis/first-axis order.
5. **Quotient error:** negative displacements use truncation rather than Euclidean
   division and therefore receive the wrong seam phase.
6. **Lift collapse:** an unreduced twist and reduced representative become one value,
   destroying the explicit gauge bridge.
7. **Sampling conflation:** boundary twists are silently converted to weighted k
   points.
8. **Geometry-by-size:** equal cell counts permit cross-shape matrix subtraction.
9. **Unspecified radius:** Euclidean hopping support and Chebyshev locality shells are
   pooled under one radius.
10. **Symmetry defaulting:** 2D $D_4$ or 3D cubic symmetry is inferred from dimension
    rather than supplied by the parent contract.
11. **Origin ambiguity:** even-size minimum-image ties are resolved differently across
    routes.
12. **Unit/reference erasure:** a scalar complex coefficient loses energy units or
    energy-zero identity.
13. **Premature rank generality:** scalar and block hoppings share erased array types
    without orbital-basis contracts.
14. **Dense regression:** sparse hopping inventories are materialized densely before
    selected-state diagonalization.
15. **Verifier dependence:** independent seam verification imports production wrapping,
    phase, bridge, or observable algorithms.
16. **Cross-fiber vectors:** individual eigenvectors are compared across twists.
17. **Channel pooling:** length/area/volume, shape, orientation, and twist effects are
    combined into one convergence status.
18. **Inapplicable-as-zero:** the absent 1D fixed-measure shape channel is reported as a
    successful zero contrast.
19. **3D memory surprise:** case counts and matrix dimensions are extrapolated without a
    separately authorized resource envelope.
20. **Historical rewrite:** accepted Stage C result identities are rebound to new public
    implementation modules.

## Resulting planning constraint

The solid-state extraction architecture must accommodate every first-slice item in one,
two, and three dimensions without implementing deferred multi-orbital or composite
contracts. The selected `ksdft2effmass.solid_state` aggregate is compatible with this inventory
when it preserves the listed cohesive submodule and dependency boundaries. HC20 and
HC21 resolve package ownership and Bravais-type factoring; they do not authorize
calculation execution.
