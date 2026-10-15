# Optimization extraction register

## Purpose

This task register is the authoritative KSD queue for reusable behavior that belongs in
`projectkoios.optimization`. It records completed migrations, remaining owner work,
blocking decisions, and the KSD implementation that should disappear or never be added.

- Semantic ownership is the extraction gate; a second KSD implementation or second
  consumer is not required.
- One concrete KSD need is sufficient to request the smallest complete owner contract.
- Later consumers may broaden an owner contract, but KSD must not duplicate the
  mechanism while waiting for them.
- KSD calls reviewed Optimization contracts directly when their unit-free boundaries
  already fit; pass-through KSD facades are not a migration goal.
- Historical calculation source and retained evidence remain unchanged even when their
  reusable mathematics receives a maintained owner implementation.

## Current owner baseline

Live KSD development resolves the reviewed Optimization/Numerics owner revision
`cf551409872a621b4e47d2236ac4ffdc12c187c0` in the root and **Band Equivalence versus
Hopping Locality** locks. PhysKit revision
`07b2a1ee3ccd07926e90f43b4d1046efccc5ad8c` resolves that same exact owner revision.
The immutable single-band version-one experiment separately
retains its authentic execution-time dependency pair.

- The live revision includes every completed capability listed below. Least-squares,
  affine/quadratic, support, selection, and finite-series public contracts are unchanged
  from the earlier reviewed owner baseline; the intervening consumed-source change is a
  qualified typing refactor.
- The invariant-only `projectkoios.numerics.linalg` Hermitian spectral-subspace
  capability was introduced at owner revision
  `23e1c88772f1bc9a1505cd25df5418cd945a76fa`; it does not supply composite-band
  eigenframes.
- The current successor adds deterministic dense positive-definite box-quadratic
  minimization, exact continuous periodic-harmonic maximization, dependency-free complex
  matrix Frobenius values, and fail-closed complex-unitary pairwise Procrustes alignment.
  Band Equivalence versus Hopping Locality directly consumes the harmonic, Frobenius
  through PhysKit, and Procrustes capabilities.
- Exact dependency resolution is software provenance, not scientific validation.
- No KSD commit, release, retained calculation, or publication claim follows from this
  task status.

## Completed extractions

These capabilities have reviewed owner implementations and are consumed through exact
Optimization contracts.

| Capability | Optimization owner surface | KSD donor or consumer | KSD status |
|---|---|---|---|
| Positive-weight real/complex multiple-right-hand-side linear least squares | `projectkoios.optimization.least_squares` | `python/src/ksdft2effmass/analysis/hopping_fits.py` and the single-band reduction experiment | Owner-integrated; KSD retains only domain construction, units, hopping meaning, and diagnostics |
| Complex affine-residual quadratic construction over real parameters | `projectkoios.optimization.affine` | Historical 64/257 regression and M3 formulas | Owner-integrated in regression only; KSD supplies ordered complex observations, raw positive weights, normalization, and labels |
| Positive-definite completed-square quadratic records and evaluation | `projectkoios.optimization.quadratic` | Periodic-1D admissible-set calculations and successor experiment | Owner-integrated |
| Exact two-dimensional closed-rectangle quadratic minimization | `projectkoios.optimization.quadratic` | Historical two-parameter M3 regression | Owner-integrated; it is not an arbitrary-dimensional box solver |
| Full-ellipsoid support points | `projectkoios.optimization.quadratic` | M3 support-bound construction | Owner-integrated; KSD separately binds and checks the scientific domain-containment evidence |
| Ordered finite-family filtering and first-on-exact-tie selection | `projectkoios.optimization.selection` | Historical finite alignment-angle regression | Owner-integrated in regression only |
| Arbitrary-dimensional dense positive-definite box-quadratic minimization | `projectkoios.optimization.quadratic.box` | Isotropic-2D hopping-shell hierarchy active dimensions 1 through 36 | Owner-implemented and exact-revision-bound; threshold-design consumption is next |
| Exact continuous periodic-harmonic maximization | `projectkoios.optimization.selection.harmonic` | Band Equivalence versus Hopping Locality | Owner-integrated directly; KSD owns physical coefficients and interpretation, with no finite-angle inventory or PhysKit facade |

## Next extraction sequence

The isotropic two-dimensional model-adequacy experiment drives the next owner work. The
sequence prevents KSD from adding another local convex solver or certificate
implementation.

1. **Completed:** implement and bind arbitrary-dimensional closed-box minimization for
   a positive-definite quadratic;
2. implement capability-specific intersection-feasibility evidence for the selected
   supported convex-set representation;
3. implement support-function strict-separation certificates and their independent
   validation contract;
4. add box-clipped support or distance only if the frozen domain is not covered by a
   verified full-ellipsoid-containment premise; and
5. bind these owner capabilities directly from the experiment and do not create a KSD
   solver facade or certificate framework.

## Remaining extraction queue

### Arbitrary-dimensional box-constrained quadratic minimization

This is the first Optimization slice needed by the multidimensional hopping-support
hierarchy. The existing exact rectangle capability is intentionally two-dimensional and
must not be stretched into an undocumented general solver.

- **Status:** `OWNER_IMPLEMENTED_AND_BOUND` at `projectkoios-optimization@f6bdecc418e46240087d1dfb1c22dac396cdc455`; direct experiment consumption and threshold design remain downstream work.
- **KSD need:** minimize a positive-definite quadratic over a declared finite-dimensional
  closed coefficient box and distinguish minimum, minimizer, active bounds, and verified
  optimality information.
- **Owner contract:** unit-free dimensions, deterministic ordering, strict finite inputs,
  explicit numerical tolerances, bounded failure behavior, and independent optimality
  checks.
- **KSD removal target:** no multidimensional active-set, enumeration, clipping, or
  generic quadratic-programming implementation may be added under `python/src/` or an
  experiment package.
- **KSD retains:** coefficient meaning, units, box selection, channel threshold,
  normalization, sample roles, and interpretation.

### Intersection-feasibility witness

A common-witness claim is a mathematical feasibility operation before it acquires KSD
model-adequacy meaning. The owner capability must be bounded to explicit supported set
representations rather than presented as a universal admissible-set framework.

- **Status:** `OWNER_ARCHITECTURE_REQUIRED`.
- **KSD need:** return an identified feasible point satisfying the complete joint
  constraints, or a non-success result that cannot be misread as infeasibility.
- **Owner contract:** explicit set representation, domain, tolerance, residuals, and
  failure semantics; solver convergence alone is not a witness.
- **KSD removal target:** generic feasible-pair search and validation mathematics must
  not be implemented as KSD infrastructure.
- **KSD retains:** scientific channel construction, thresholds, finite-family identity,
  experiment correlation, and compatibility disposition.

### Support-function strict-separation certificate

Optimization owns the reusable convex-analysis relationship among support functions, a
strictly separating direction, the directional separation margin, and the dual-norm
distance lower bound for explicitly supported set representations.

- **Status:** `OWNER_ARCHITECTURE_REQUIRED`.
- **KSD need:** a reconstructable positive lower bound that can be compared with an
  experiment-owned resolution.
- **Owner contract:** source/target orientation, supported convex-set representations,
  nonzero direction, support bounds, strict margin, metric/dual-norm inputs, mathematical
  validity conditions, validation, and failure behavior.
- **Numerics dependency:** interval, directed-rounding, or conservative-enclosure
  arithmetic belongs in `projectkoios.numerics` when required by the certificate.
- **KSD removal target:** reusable support-gap, dual-norm, outward-rounding, and generic
  certificate-validation algorithms must not remain or be added as maintained KSD
  infrastructure.
- **KSD retains:** metric choice and normalization, scientific sets, resolution,
  experiment data instantiating owner-defined premises, provenance, evidence wrapper,
  disposition, and interpretation.

### Box-clipped support or set distance

The existing owner support capability applies to the complete ellipsoid. It does not
claim support or distance for an ellipsoid intersected with a box.

- **Status:** `CONDITIONAL_OWNER_SLICE`.
- **Trigger:** the frozen experiment cannot verify that every required full-ellipsoid
  support point lies inside its declared coefficient box.
- **Owner contract:** an explicit supported clipped-set representation and a bounded
  support, distance, or strict-separation operation; no arbitrary-set claim.
- **KSD removal target:** KSD must not introduce its own generic clipped-set distance
  solver when containment fails.
- **KSD behavior before extraction:** retain `unresolved` or `invalid-premise` rather
  than promote failed search to separation.

### Square complex pointwise Procrustes

The reusable operation selects a square unitary that minimizes the declared Frobenius
frame residual for one candidate/reference pair.

- **Status:** `PARTIALLY_OWNER_INTEGRATED`; the generic one-pair capability exists at
  `cf551409872a621b4e47d2236ac4ffdc12c187c0` and the Band Equivalence versus Hopping
  Locality producer consumes it directly. The older `BandFrameAligner1D` donor remains
  separate technical debt.
- **KSD donor:** `BandFrameAligner1D` in
  `python/src/ksdft2effmass/solid_state/frame_alignment.py`.
- **Owner target:** `projectkoios.optimization.alignment`.
- **Required contract:** source/target orientation, right action, objective,
  normalization, singular values, numerical rank, applied cutoff, residual, unitarity,
  stationarity, condition reporting, backend identity, and nonuniqueness behavior.
- **Selected nonuniqueness policy:** reject numerically rank-deficient inputs and return
  no transformation; deterministic null-space completion is outside this consumer contract.
- **KSD removal target:** the transformation-selecting SVD/polar mechanism in
  `BandFrameAligner1D`; new KSD experiments call the owner operation directly. The
  experiment's independent verifier retains a separate reconstruction path rather than
  calling the producer action.
- **KSD retains:** frame identities, path/sewing compatibility, channel meaning, units,
  and scientific interpretation.

### One-global-unitary aggregate Procrustes

This capability selects one unitary from an ordered aggregate of pointwise
cross-covariances. It is a different feasible family from pointwise alignment, not a
numerical approximation to it.

- **Status:** `TECH_DEBT` while the owner completes the already-authorized box-quadratic slice.
- **KSD donor:** `_global_rotation` in
  `python/src/ksdft2effmass/periodic1d/multiband_alignment/calculate.py`.
- **Owner target:** `projectkoios.optimization.alignment`.
- **Required contract:** ordered batch semantics, aggregation weights, cross-covariance
  orientation, the complete square-Procrustes diagnostics, and the same fail-closed
  rank-deficient rejection policy as the pointwise operation.
- **KSD removal target:** `_global_rotation` and any duplicate aggregate SVD selection.
- **KSD retains:** the scientific meaning of the one-global-unitary channel and M2's
  selected equal training-point aggregation.

### Polar frame transport and closure selection

Neighborwise transport repeatedly selects Procrustes transformations and then selects a
closure/holonomy correction. It is optimization behavior, not a matrix-application
utility.

- **Status:** `BLOCKED_UPSTREAM_CONTRACTS`.
- **KSD donor:** `PolarBandFrameTransporter1D` in
  `python/src/ksdft2effmass/solid_state/band_frames.py`.
- **Owner target:** `projectkoios.optimization.alignment`, consuming owner-neutral
  Numerics frame/path records.
- **Prerequisites:** stable Procrustes behavior; KSD's eigenframe requirement; sewing
  orientation; phase branch/order; degenerate-phase handling; deterministic completion;
  and closure-root failure behavior.
- **KSD removal target:** neighborwise transformation selection and distributed closure
  selection from the maintained KSD implementation.
- **KSD retains:** path ordering, sewing meaning, overlap threshold meaning, sample role,
  closure interpretation, and experiment diagnostics.

## Intentionally not Optimization work

The following remain outside the Optimization owner even when they consume its
capabilities.

- Numerics owns direct finite Fourier transforms, invariant Hermitian spectra/projectors,
  frame/projector algebra, interval arithmetic, and application of already supplied
  transformations.
- PhysKit owns lattice, hopping, units, energy references, and other physics-semantic
  records and operations.
- KSD experiments own physical models, features, weights, thresholds, metric choice,
  sample roles, certificate-method binding, evidence correlation, dispositions, and
  interpretation.
- Quantum ESPRESSO owns electronic-structure execution and Wannier90 owns localization.

## Authoritative supporting records

This register summarizes, but does not replace, the detailed mathematical contracts in:

- [`multiband_alignment/owner-boundary.md`](../../../architecture/v2/ksdft2effmass/periodic/periodic1d/multiband_alignment/owner-boundary.md);
- [`composite-band alignment technical debt`](../../tech_debt/composite-band-alignment-and-locality/index.md);
- [`admissible-set-evidence-semantics.md`](../../../architecture/v2/ksdft2effmass/analysis/model_adequacy/admissible-set-evidence-semantics.md);
- [`periodic2d/implementation.md`](../../../architecture/v2/experiments/model-adequacy/periodic2d/implementation.md); and
- [`periodic3d/implementation.md`](../../../architecture/v2/experiments/model-adequacy/periodic3d/implementation.md).

The Optimization repository maintains its owner-side execution tasks under
`docs/tasks/active/ksdft2effmass-migration/`. This KSD register remains the authoritative
consumer inventory and must be updated whenever an item changes owner status, blocking
decision, exact owner revision, KSD donor, or removal target.
