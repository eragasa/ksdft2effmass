# Implementation

## Request and upstream admission

`Periodic1DConstrainedAdmissibleSetAnalysisRequest` binds one immutable configuration to
exact built-in `bytes`. Construction decodes the canonical
`Periodic1DCompositeBandAlignmentCalculationResult`, rejects noncanonical bytes, checks
the configured SHA-256, and requires a rank-two upstream result. The concrete analyzer
also receives a `Periodic1DCompositeBandAlignmentVerifier`; it neither constructs an
upstream producer nor synthesizes a verifier from `None`.

## Production composition

`Periodic1DConstrainedAdmissibleSetAnalyzer.execute()` first authenticates the upstream
wire and then derives the finite spectral and angle-resolved operator quadratics. It
uses the established `ReciprocalOperatorSamples1D`, `BlockHoppingInterpolator1D`,
`ReciprocalOperatorFourierTransformer1D`,
`CenteredEvenMeshCyclicToOrdinaryConverter1D`, and `BlockHoppingTruncator1D` owners.
There is no local interpolation, Fourier, truncation, cyclic-conversion, or JSON kernel.

The result embeds the canonical composite result and correlates its digest, quadratic
values, proof-point diagnostics, configured range inventory, and separation geometry in
constructors. `BaseTypedRecord` owns canonical typed JSON; the provisional replacement
contains no compatibility serializer for the historical M3 schema.

## Verification and rendering

`Periodic1DConstrainedAdmissibleSetIndependentReferenceAnalyzer` uses direct NumPy
formulas for the finite Fourier sums, interpolation sums, quadratics, ellipsoid extrema,
witnesses, separation bounds, evaluation losses, and locality diagnostics. It does not
invoke the production M3 analyzer or represented-operator production actions.

`Periodic1DConstrainedAdmissibleSetVerifier` owns the exact M3 result bytes through
`BaseModelAnalysisVerifier`. It independently verifies the embedded composite bytes and
uses a closed component-to-observation inventory for explicitly named quadratic,
witness, certificate, locality, and visualization comparisons. Verification does not
walk serialized fields recursively or admit comparisons by name prefix. It authenticates
both result and projection SHA-256 values. The projection composes existing typed
threshold and parameter-evaluation domain sections with only the case context and
plotting axes needed by the two figures; it does not flatten a parallel row inventory or
duplicate locality matrices.

`Periodic1DConstrainedAdmissibleSetVisualizer` accepts only the passing typed
verification and digest-bound projection. Its closed inventory is
`confirmatory-admissible-sets.png` and
`confirmatory-admissible-locality-channels.png`. Figure actions choose marks and axes but
calculate no new scientific values.
