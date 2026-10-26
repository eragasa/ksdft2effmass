# Implementation

## Typed calculation aggregate

`Piab1dConfiguration` declares the nondimensional model, boundary convention, parent
dimension, and retained dimension. `Piab1dCalculationResult` composes reusable typed
sections rather than storing anonymous nested mappings:

- `HamiltonianResultSection`;
- `EigensystemResultSection`;
- `SpectralReductionResultSection`;
- `QuadratureResultSection`;
- `AnalyticalSamplingResultSection`;
- `Piab1dDiagnostics`;
- `Piab1dConvergenceResult`;
- `Piab1dSelectionResult`;
- `Piab1dEigenpairSweepResult`;
- `Piab1dResidualNormSweepResult`;
- `Piab1dFiniteAlgebraicDiagnostics`; and
- `KineticPotentialDecompositionResult`.

Each constructor enforces its local field inventory and correlated shape, unit, order,
and convention invariants. The root constructor enforces relationships across sections.
No verifier reparses raw JSON fields.

## Calculation composition

`run_01_calculation.py` declares all scientific and algorithmic controls in Python. It
constructs the PhysKit PIAB1D solution, executes the KSD reduction and diagnostics,
forms the analytical comparison series, executes one shared grid sweep, evaluates the
decomposition shift, and serializes one typed root result.

`Piab1dGridSweepAnalyzer` solves each declared grid once. The resulting eigensolution
feeds eigenpair convergence, residual norms, and finite algebraic diagnostics. This
composition prevents three independent solver loops from producing divergent grid
inventories.

## Independent verification

`Piab1dVerifier` uses the final `BaseModelAnalysisVerifier` subject constructor to
validate the exact result digest and reconstruct `Piab1dCalculationResult`. It then
derives `Piab1dVisualizationData`, computes its SHA-256 digest, and composes
independent reference analyzers through the shared final verification sequence. The
verifier does not accept a caller-authored projection digest.

The independent route reconstructs:

- the finite-difference Hamiltonian;
- discrete and continuum spectra;
- eigensystem and reduction relations;
- quadrature normalization;
- convergence series and retained selection;
- full eigenpair sweeps;
- canonical residual norms;
- finite algebraic diagnostics; and
- kinetic-potential decomposition and model-class projections.

The final `Piab1dVerification` contains operation-named verification components and 79
comparisons. Verification actions and serialized verification values remain separate
objects.

## Authenticated visualization

`Piab1dVisualizer` accepts only a passing `Piab1dVerification` whose authenticated
visualization-data digest matches the supplied typed projection. It constructs one
model-specific figure action and one encoding-only renderer per
`Piab1dVisualizationPlotEnum` member, then checks exact equality between the renderer
inventory and the closed enum. All thirteen figures are separated from PNG encoding.
The spectrum-and-states figure additionally composes separate plot and subplot actions;
the remaining figure actions retain their specialized internal axis composition pending
incremental plot/subplot extraction.

Every figure renderer uses the common in-memory PNG encoding and figure-closure path.
The PNG value decodes image bytes before admission and stores an exact
cross-platform-safe filename. The rendering
script writes through `.figures.incomplete`, publishes the completed directory
atomically, and records result, verification, implementation, runtime, and figure
hashes.

## Serialization boundary

All successor records inherit final `to_dict`, `from_dict`, `to_json`, and `from_json`
behavior from `BaseTypedRecord`. Concrete records implement typed mappings only. Array
and quantity normalization belongs to `ksdft2effmass.serialization`; PIAB1D contains no
successor-specific array transport.

## Historical boundary

Historical flat results, scripts, figures, reports, and checksum entries retain their
original names and exact repository provenance. They do not define successor class
names, plot enum names, result schemas, or implementation paths.
