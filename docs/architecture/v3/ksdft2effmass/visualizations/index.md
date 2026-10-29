# `ksdft2effmass.visualizations`

## Purpose and status

This target Architecture v3 package owns domain-neutral authenticated visualization
mechanics shared by model-system and periodic calculation families. It replaces the
misplaced shared module `ksdft2effmass.model_systems.visualization`; it does not own any
scientific projection, plot inventory, threshold, acceptance decision, or calculation
path.

The architecture is approved before implementation. Until the corresponding source
migration lands, the current singular modules remain the installed runtime and these
pages describe the replacement contract rather than a supported import.

## Target source map

```text
python/src/ksdft2effmass/visualizations/
├── __init__.py
├── data.py
├── figures.py
├── records.py
├── rendering.py
└── visualizer.py
```

The modules own:

| Module | Responsibility |
|---|---|
| `records.py` | Immutable admitted visualization values, including encoded PNG bytes and their closed enum identity. |
| `data.py` | Final canonical typed-JSON behavior for family-defined visualization projections. |
| `figures.py` | Domain-neutral plot, subplot, and figure composition contracts. |
| `rendering.py` | Figure-to-PNG encoding and figure closure. |
| `visualizer.py` | Verification/projection authentication and closed-inventory enforcement. |
| `__init__.py` | Deliberate public exports only. |

## Public contract

The target public types are domain-neutral replacements for the current
`BaseModelAnalysis...` names:

- `BaseVisualization`;
- `PngVisualization`;
- `BaseVisualizationData`;
- `BasePlot`;
- `BaseSubplot`;
- `BaseFigure`;
- `BaseFigureRenderer`;
- `PngFigureRenderer`; and
- `BaseVisualizer`.

Family source imports these types from `ksdft2effmass.visualizations`. The old
`ksdft2effmass.model_systems.visualization` module is removed after all direct callers
migrate. No compatibility shim or alias module remains.

## Dependency direction

The root package may depend on:

- `ksdft2effmass.serialization` for canonical typed projection bytes;
- a root verification-owned authentication interface for pass status and authenticated
  projection digest; and
- Matplotlib only inside figure and rendering mechanics.

It must not import `model_systems`, `periodic1d`, `solidstate`, `calculations`,
`campaigns`, or any family result type. Family visualization packages depend inward on
this root owner.

## Invariants

- Scientific values enter rendering only through an immutable family projection.
- Authentication occurs before any Matplotlib object is created.
- A visualizer requires passing verification of the exact projection bytes.
- A renderer owns presentation and encoding only; it calculates no new scientific
  quantity.
- PNG admission checks the image container, not its scientific meaning.
- Every family owns a closed plot enum and exact renderer-inventory equality.
- Filesystem publication and provenance remain with the direct render script.
- Historical PNG, rendering, verification, and provenance bytes are not rewritten by
  the source migration.

## Family owners

- [`model_systems.piab1d.visualizations`](../model_systems/piab1d/visualizations/index.md)
- [`model_systems.qho1d.visualizations`](../model_systems/qho1d/visualizations/index.md)
- [`model_systems.mathieu1d.visualizations`](../model_systems/mathieu1d/visualizations/index.md)
- [`periodic1d.fourier_locality.visualizations`](../periodic1d/fourier_locality/visualizations/index.md)
- [`periodic1d.composite_band_alignment.visualizations`](../periodic1d/composite_band_alignment/visualizations/index.md)

## Detailed pages

- [Implementation](implementation.md)
- [Numerical contract](numerics.md)
- [Scientific interpretation](scientifics.md)
- [Schematics](schematics.md)
- [Construction and ownership audit](../component-construction-and-visualization-audit.md)
