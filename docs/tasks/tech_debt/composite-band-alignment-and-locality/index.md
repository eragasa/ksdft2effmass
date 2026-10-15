# Composite-band alignment and locality technical debt

## Status

`TECH_DEBT`

This record tracks temporary numerical mechanisms retained by the prospective maintained
experiment family
`ksdft2effmass.campaign.periodic-reduction.periodic1d.composite-band-alignment-and-locality`.
It is not an authorization to run, retain, publish, commit, or push an experiment.

Optimization now provides the bounded one-pair complex-unitary Procrustes contract at
`cf551409872a621b4e47d2236ac4ffdc12c187c0`. Band Equivalence versus Hopping Locality
consumes it directly. The broader composite-band donor migration, aggregate alignment,
eigenframes, and path-closure behavior remain separate work and must not silently expand
that owner contract.

## Frozen successor decisions

1. The parity-preserving successor requires backend-qualified eigenvector-diagonal
   frames. It must retain the backend and version and make no claim that frame
   coordinates are canonical across backends or within degenerate eigenspaces.
2. Pointwise and one-global-unitary Procrustes operations reject numerically
   rank-deficient cross-covariances and return no selected transformation. They do not
   construct a deterministic null-space completion.
3. Projector-derived deterministic frames and rank-deficient completion would define
   materially different protocols and are outside the first maintained successor.

## Debt inventory

### `TD-CBAL-001`: backend-qualified dense Hermitian eigenframes

- **Current donor:** `_eigenframes` in
  `python/src/ksdft2effmass/periodic1d/multiband_alignment/calculate.py`.
- **Current mechanism:** direct `numpy.linalg.eigh` eigenvector selection.
- **Owner target:** a reviewed frame-producing operation under
  `projectkoios.numerics.linalg`.
- **Required owner evidence:** complete ordered eigenvalues; selected eigenvector-diagonal
  frame; backend/version identity; residual, orthonormality, input-Hermiticity, and
  boundary-gap diagnostics; explicit behavior for degeneracy and backend failure.
- **KSD removal target:** direct eigensolver frame selection. KSD retains lowest-group
  identity, units, gap meaning, sample roles, and interpretation.
- **Exit condition:** exact owner revision bound, direct owner call, independent KSD
  parity verification, and no forwarding facade.

### `TD-CBAL-002`: pointwise square complex Procrustes

- **Owner availability:** the required generic one-pair solver exists at
  `cf551409872a621b4e47d2236ac4ffdc12c187c0`; this debt remains open only for migration
  of the older composite-band donor and its parity evidence.
- **Current donor:** `BandFrameAligner1D` in
  `python/src/ksdft2effmass/solid_state/frame_alignment.py`.
- **Current mechanism:** direct complete NumPy SVD and polar-factor selection.
- **Owner target:** `projectkoios.optimization.alignment`.
- **Required policy:** source/target orientation, right action, objective, singular
  values, applied numerical-rank cutoff, full-rank acceptance, rank-deficient rejection,
  residual, unitarity, stationarity, conditioning, and failure translation.
- **KSD removal target:** transformation-selecting SVD. KSD retains frame/path identity,
  sewing compatibility, channel role, and interpretation.
- **Exit condition:** reviewed owner operation, exact revision binding, direct
  consumption, independent objective/unitarity reconstruction, and deletion of the
  local selection mechanism without an adapter.

### `TD-CBAL-003`: one-global-unitary aggregate Procrustes

- **Current donor:** `_global_rotation` in
  `python/src/ksdft2effmass/periodic1d/multiband_alignment/calculate.py`.
- **Current mechanism:** ordered equal-weight covariance aggregation followed by direct
  complete NumPy SVD.
- **Owner target:** `projectkoios.optimization.alignment`.
- **Required policy:** the pointwise contract plus ordered aggregate inputs, equal raw
  weights, aggregate orientation, and the same rank-deficient rejection.
- **Exit condition:** reviewed owner aggregate operation, exact revision binding,
  independent KSD reconstruction, and deletion of local selection code.

### `TD-CBAL-004`: polar transport and closure selection

- **Current donor:** `PolarBandFrameTransporter1D` in
  `python/src/ksdft2effmass/solid_state/band_frames.py`.
- **Owner target:** `projectkoios.optimization.alignment`, consuming owner-neutral
  Numerics frame records.
- **Deferred contract:** sewing orientation, endpoint convention, overlap-rank
  acceptance, phase branch/order, degenerate-phase behavior, closure-root failure, and
  retained local-overlap/holonomy diagnostics.
- **Exit condition:** review only after the Procrustes owner contract is stable; then
  replace selection directly without a KSD facade.

## Migration boundary

The historical retained calculation and its manifests remain unchanged. The current KSD
implementation remains supported while this debt is open because the isolated
historical 64/257 regression consumes its result contract. The active Band Equivalence
versus Hopping Locality continuum does not. A wrapper-only
experiment package or duplicate implementation is not an acceptable migration.

The final migration must move the concrete experiment composition, definition, results,
serialization, and verifier under
`experiments/periodic-reduction/composite-band-alignment-and-locality/periodic1d/`, update
the historical regression to consume the maintained experiment contract, and remove the
obsolete concrete KSD composition only after all consumers have moved.
