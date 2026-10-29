# Implementation

## Typed configuration and result

`Mathieu1dConfiguration` owns the direct and reciprocal periods, energy scale, cosine
potential, two parent-representation inventories, sampled momenta, selected band,
complete training mesh, disjoint evaluation mesh, fitting weights, hopping ranges, and
numerical tolerances. Its constructor correlates every inventory before calculation or
deserialization can proceed.

`Mathieu1dCalculationResult` attaches execution metadata and composes four typed
scientific sections:

- `Mathieu1dRefinementResult`: finite reference spectrum and plane-wave and periodic
  finite-difference discrepancies;
- `Mathieu1dBandSamplesResult`: selected and adjacent upper-band samples on disjoint
  training and evaluation inventories;
- `Mathieu1dTransformResult`: complete finite transform, reconstruction, and hopping
  Hermiticity diagnostics; and
- `Mathieu1dRangeResult`: one symmetric range's mediated truncation, independently fit
  direct route, sampled errors, omitted norm, Parseval check, route comparison, and band
  shape diagnostics.

Each section validates local shape, order, unit, and disposition invariants. The root
validates cross-section correlation with the authored configuration. Shared typed JSON
code owns array and quantity transport; Mathieu1D defines no custom wire codec.

## Production composition

`Mathieu1dAnalyzer` constructs the declared `PeriodicFourierPotential1D`, delegates
finite plane-wave and periodic finite-difference fibers to their canonical owners, and
uses ordered eigenspectra for the parent comparisons. It then composes the existing
reciprocal transform, truncation, interpolation, weighted least-squares fit, Parseval,
Hermiticity, route-comparison, and band-shape actions.

The analyzer does not read files, choose an accepted range, or reinterpret sampled gaps
as continuum isolation. `run_01_calculation.py` owns filesystem staging and writes the
configuration and result bytes atomically through an incomplete execution directory.

## Byte-owning independent verification

`Mathieu1dVerifier` receives only immutable result bytes. The shared verifier boundary
computes their SHA-256 identity and reconstructs `Mathieu1dCalculationResult` from those
same bytes. The independent route then:

1. assembles dense plane-wave matrices directly;
2. assembles sparse twisted periodic finite-difference matrices directly;
3. evaluates explicit finite Fourier sums;
4. performs NumPy weighted least squares;
5. reconstructs all result sections and execution metadata;
6. compares the complete typed mapping; and
7. derives and separately compares the visualization projection.

It does not invoke `Mathieu1dAnalyzer` or the reusable transform, truncation, fitting,
interpolation, or diagnostic actions used by production. The aggregate contains 873
comparisons split between independent result reconstruction and projection correlation.

`run_02_verification.py` additionally correlates canonical configuration bytes with the
configuration embedded in the result before writing verification and visualization data
through an incomplete stage.

## Authenticated rendering

`Mathieu1dVisualizationData` stores only values already present in the independently
reconstructed result. Plot actions draw one relation, subplot actions own axis-local
presentation, figure actions own layout, and the root `PngFigureRenderer` encodes
immutable PNG values.
`Mathieu1dVisualizer` requires a passing `Mathieu1dVerification` whose projection digest
matches the supplied data and returns exactly:

- `mathieu1d-finite-reduction.png`; and
- `mathieu1d-publication-summary.png`.

`run_03_render.py` reruns byte-owning verification, compares the complete stored and
fresh verification and projection bytes, checks source digests, and atomically publishes
figures and the execution-bound technical-report snapshot.

## Retirement and retained execution

The direct implementation supersedes the calculation-local package, installed `study/`
package, predecessor scripts and tests, four predecessor executions, schema-v1 input,
and three JSON schemas. The [legacy disposition](legacy-disposition.md) consolidates the
current ownership decision and links the detailed calculation recovery ledgers. No
predecessor byte is a runtime, verification, rendering, report, or publication input.

The sole live execution is
`calculations/mathieu1d/executions/direct-finite-reduction-n64/`. It records a dirty
worktree qualification and remains unsealed. Its existence does not establish release,
publication acceptance, or scientific validation.
