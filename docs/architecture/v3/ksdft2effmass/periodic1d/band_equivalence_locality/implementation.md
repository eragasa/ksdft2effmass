# Implementation

## Ownership

`request.py` validates exact construction and disjoint evaluation meshes, amplitudes,
truncation ranges, and producer numerical tolerances. `results.py` owns immutable
scientific values without mapping or JSON methods. `analysis.py` composes installed
Fourier, cyclic-to-ordinary, interpolation, and truncation owners around harmonic
maximizers configured internally from each request's declared harmonic controls.
Reusable `solidstate.GaugeRotation` definitions bind their matrix rank and all
rotation parameters, while `solidstate.GaugeAttack` evaluates the definition on an
explicit coordinate inventory, validates its unitary matrices against the producer's
declared tolerance, and applies the right-acting similarity transformation. The
installed sinusoidal rank-two rotation supplies the calculation-specific matrix field;
it is not a realized matrix-inventory wrapper.

`records.py` projects the scientific values into `BaseTypedRecord` owners. Reconstruction
from retained bytes instantiates values directly and never reruns the analyzer.
`reference.py` independently reconstructs the same finite quantities with explicit
complex exponential sums and its own Bessel series. `verification.py` readmits exact
canonical result bytes, derives their SHA-256 digest, compares every retained scalar,
hopping inventory/power, and truncation inventory/value channel with the reference, and
authenticates the canonical `retention.visualization_data` projection after independently
checking its scalar, inventory, and matrix channels. Each verified result is itself a
`BaseTypedRecord`: `_mapping()` supplies `to_dict()`, and the final shared boundary owns
canonical `to_json()`/`from_json()` admission. `visualizations` admits that digest before
rendering the closed alignment, locality, and error-channel PNG inventory.

The serialization-free nonflat core lives under
`embedded_subspace/rank2/` and is split into feature-owned packages. `parent_scale/`
owns the exact ambient-rank-four parent, external-gap and PhysKit closed-loop transport,
single-channel cyclic hopping-power inventory, immutable request/results, and the
qualified single-scale analysis. Its public values use closed external-gap-failure,
band-transport backend-failure, band-transport numerically-unresolved, band-transport
threshold-failure, and qualified-parent variants rather than a disposition enum or
nullable diagnostic bundle. Typed upstream band-transport statuses and backend failure
values remain typed in those scientific results. `parent_scale/independent_reference.py`
reconstructs the parent matrices, sampled spectral subspace, polar-link actions through
Hermitian Gram decompositions, loop correction, represented operators, restricted
harmonic maximum, and cyclic Fourier powers without calling production parent,
transport, analysis, or Fourier owners. Feature-owned qualification and analysis
verification remain in `parent_scale/qualification_verification.py` and
`parent_scale/verification.py`.

`parent_family/` owns the ordered onsite-to-full parent-hopping homotopy and its
scientific verification. It composes the existing single-member analyzer without
changing any other control and retains every member as one correlated,
serialization-free family value. `parent_family/independent_reference.py` rebuilds every
family member through the independent direct-formula route. `momentum_refinement/`,
`amplitude_refinement/`, and `truncation/` likewise own their scientific requests,
analyses, independent references, and in-memory verification. None of these scientific
feature packages imports retention or visualization ownership.

`retention/records.py` alone projects the scientific values and closed refinement and
truncation variants to canonical wire values. `retention/visualization_data.py` owns the
canonical typed single-parent, family, and aggregate rendering projections.
`retention/calculation_verification.py` and `retention/verification.py` own exact-byte
authentication, visualization-projection authentication, and aggregate lifecycle
composition; they do not become the public owner of feature verification values.
`embedded_subspace/rank2/visualizations` imports those authenticated projections and
remains the strictly downstream renderer for the closed single-parent, family, and
aggregate refinement/truncation inventories. Retention never imports the local
visualization package. The
single-parent and family verified-result aggregates use the same `to_dict()` to
canonical `to_json()` record path; rendering does not rerun either scientific route.
Stopped single-parent outcomes retain an authenticated empty downstream projection but
are not renderable as qualified scientific figures. The independent route constructs its
centered mesh and materializes every family member directly from primitive retained
fields; it does not call production request mesh or family-member factories. The
verification absolute tolerance is a fixed installed verifier policy exposed read-only
by the request and validated during canonical admission, not a subject-controlled
scientific input.

`momentum_refinement/analysis.py` binds a nested doubling-mesh inventory to one unchanged
embedded request, retains every single-mesh analysis, and classifies the study with
closed qualification-stopped, converged, or unresolved variants. Adjacent-mesh
comparisons keep parent, correlation, threshold, hopping-weight, hopping-power,
maximizing-angle, band-defect, reconstruction-defect, and Parseval channels separate.
Shared parent spectra and projectors are compared at the exactly nested momentum points.
`momentum_refinement/independent_reference.py` constructs every mesh request directly
from primitive fields, uses the independent single-mesh route, and independently repeats
the parent and adjacent-mesh comparisons. `momentum_refinement/verification.py` exposes
an in-memory comparison through the existing `CompositeVerification` infrastructure. It
intentionally defines no new retained mapping, decoder, wire discriminator, or
refinement record. The enclosing calculation record owns its retained representation
and aggregate authentication.

`embedded_subspace/rank2/truncation/` owns the separate ordinary-lattice consequence
study. Its request binds an unchanged embedded template to explicit ordinary cutoffs and
a deterministically shifted disjoint evaluation mesh. Its analyzer reuses one qualified
parent preparation, composes the installed Fourier, negative-Nyquist conversion,
ordinary interpolation, and conjugate-closed truncation owners, and returns either a
closed qualification-stopped outcome or a completed point/range inventory. Scientific
values retain conversion power, ordinary omitted power, interpolation error,
truncation-only error, and total error as separate Hamiltonian and sorted-spectrum
channels. The independent reference reconstructs the parent through the existing
Gram-polar direct route and evaluates Fourier blocks, interpolation, cutoffs, and spectra
with direct finite formulas; it does not call the production parent, analysis, Fourier,
conversion, interpolation, or truncation actions. `truncation/verification.py` compares
that reconstruction in memory and intentionally defines no custom retained mapping.

The KSD transport diagnostic action explicitly labels its derived link quantity as the
maximum primitive-link Frobenius residual. It does not present that derived value as a
verbatim PhysKit or Optimization-owner diagnostic. Reference and attacked hopping powers
are paired only after two complete single-channel inventories have been calculated; no
zero-valued comparison placeholder is used.

## Dependency direction

The implementation depends downward on `ksdft2effmass.solidstate`, including the
generic `GaugeRotation`/`GaugeAttack` boundary, PhysKit quantities
and closed-loop transport, and Project Koios Optimization harmonic maximization. It does
not import calculation or experiment trees. The independent flat reference uses NumPy
directly and does not call the production transform, interpolation, Nyquist-conversion,
or truncation actions. The independent embedded reference depends only on the immutable
request/result values plus numerical primitives; it does not compose the production
parent constructor, PhysKit transporter, production analyzer, or production Fourier
action. The independent truncation route likewise depends on direct formulas rather than
production finite-periodic actions.

## Open implementation work

The embedded-subspace/rank2 core now has canonical aggregate byte admission and
independent verification for its one-mesh parent and bounded parent-hopping family,
including qualification, alignment, and cyclic-locality channels. Its scientific
momentum-refinement, adaptive-amplitude, and truncation values remain serialization-free,
while `Periodic1DRank2CalculationRecord` owns their shared retained
context with the parent family. The record uses `_mapping()` through standard
`to_dict()`/`from_dict()` and canonical `to_json()`/`from_json()` boundaries.
`CalculationWireEnum` is a closed ordinary `Enum`; variant-specific payloads carry no
null padding and use no type registry. The aggregate verifier readmits canonical bytes,
authenticates their SHA-256 identity, and composes the independent family, momentum,
adaptive-amplitude, and truncation verification routes. This establishes bounded
software-route agreement only, not scientific validation. Direct no-overwrite
calculate/verify/render scripts retain the record, its stored verification, and the
closed authenticated six-figure family, momentum-refinement, adaptive-amplitude, and
truncation inventory. Rendering calls stored-verification admission and does not rerun
the independent routes. Authenticated embedded, fully qualified parent-family, and
cohesive calculation projections and their closed PNG inventories are installed. The
read-only donor audit compares 18,513 mapped immutable scalars within `1.0e-13`, but it
also records a non-equivalent momentum disposition, four missing retained truncation
slices, missing five-scale refinement summaries, unactivated pandas diagnostics, and ten
maintained donor consumers. Full parity therefore remains open. The calculation-local
`workflow/` remains tracked pending a later reviewed retirement.
