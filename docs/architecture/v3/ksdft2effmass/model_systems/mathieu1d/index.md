# `ksdft2effmass.model_systems.mathieu1d`

## Scientific question

For the finite scalar periodic Hamiltonian

\[
H(k)=-\frac{d^2}{dx^2}+0.5\cos x,
\]

how consistently do declared plane-wave and periodic finite-difference representations
resolve sampled parent bands, and how does one selected finite band behave under complete
Fourier transformation and symmetric hopping-range truncation?

This is an implemented controlled model-system vertical slice. It is not the compatible
rank-one control for the other Periodic1D studies and does not establish a continuum
isolation theorem or material validity.

## Direct lifecycle

```text
run_01_calculation.py → run_02_verification.py → run_03_render.py
```

The module-scope scripts declare controls in Python, refuse stage overwrite, and contain
no Workflow, argument parser, registry, custom JSON transport, or calculation kernel.
The retained direct execution is explicitly unsealed.

## Ownership

`model_systems.periodic_1d` owns the unit-aware periodic potential and finite parent
Hamiltonian constructors. `solidstate` and `analysis` own reusable Fourier, truncation,
interpolation, fitting, and diagnostic actions. Mathieu1D owns their model-specific
composition, typed result meaning, independent reconstruction, and authenticated figure
projection.

The calculation root owns the exact controls, execution metadata, claim boundary,
artifact correlation, report, and publication bindings. It does not own a second Python
package or schema-v1 decoder.

## Implemented source map

```text
model_systems/mathieu1d/
├── configuration.py
├── result.py
├── analysis.py
├── verification_values.py
├── verification.py
└── visualizations/
    ├── data.py
    ├── inventory.py
    ├── visualizer.py
    └── figures/
```

The package root exposes only the direct typed lifecycle. The former installed `study/`
package, calculation-local implementation, predecessor executions, input, and JSON
schemas are absent from the live tree.

## Invariants

- Configuration, result, verification, and visualization records are immutable and
  constructor-validated.
- All model values are dimensionless and carry explicit `Unitless()` quantities.
- Parent matrices, finite Fourier transforms, and range reductions remain distinct
  operations with separate diagnostics.
- Training and evaluation reciprocal coordinates are disjoint.
- Verification hashes the exact admitted result bytes and independently reconstructs
  every scientific field without calling the producer.
- Rendering accepts only a passing verification bound to the exact authenticated
  visualization projection.
- The closed rendering inventory contains two figures.
- Passing checks establish finite software and numerical consistency only.

## Public class pages

- [`Mathieu1dConfiguration`](Mathieu1dConfiguration/index.md)
- [`Mathieu1dAnalyzer`](Mathieu1dAnalyzer/index.md)
- [`Mathieu1dRefinementResult`](Mathieu1dRefinementResult/index.md)
- [`Mathieu1dBandSamplesResult`](Mathieu1dBandSamplesResult/index.md)
- [`Mathieu1dTransformResult`](Mathieu1dTransformResult/index.md)
- [`Mathieu1dRangeResult`](Mathieu1dRangeResult/index.md)
- [`Mathieu1dCalculationResult`](Mathieu1dCalculationResult/index.md)
- [`Mathieu1dIndependentVerification`](Mathieu1dIndependentVerification/index.md)
- [`Mathieu1dVerification`](Mathieu1dVerification/index.md)
- [`Mathieu1dVerifier`](Mathieu1dVerifier/index.md)
- [`Mathieu1dVisualizationData`](visualizations/Mathieu1dVisualizationData/index.md)
- [`Mathieu1dVisualizationPlotEnum`](visualizations/Mathieu1dVisualizationPlotEnum/index.md)
- [`Mathieu1dVisualizer`](visualizations/Mathieu1dVisualizer/index.md)

## Package pages

- [Visualization package](visualizations/index.md)
- [Implementation](implementation.md)
- [Numerical contract](numerics.md)
- [Scientific interpretation](scientifics.md)
- [Schematics](schematics.md)
- [Legacy disposition](legacy-disposition.md)
- [Periodic1D family boundary](../../periodic1d/index.md)
