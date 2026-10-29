# `ksdft2effmass.periodic1d.fourier_locality.visualizations`

## Status and responsibility

Target authenticated visualization package for the closed two-figure native inventory.
It replaces the current singular source module without changing projection bytes,
filenames, scientific values, or rendering policy.

```text
periodic1d/fourier_locality/visualizations/
├── __init__.py
├── data.py
├── figures.py
├── inventory.py
└── visualizer.py
```

## Public classes

- [`Periodic1DFourierLocalityVisualizationData`](Periodic1DFourierLocalityVisualizationData/index.md)
- [`Periodic1DFourierLocalityVisualizationPlotEnum`](Periodic1DFourierLocalityVisualizationPlotEnum/index.md)
- [`Periodic1DFourierLocalityVisualizer`](Periodic1DFourierLocalityVisualizer/index.md)

## Closed figures

1. `rank1-fourier-locality.png`: eight panels for sampled parent bands, finite sampled-gap
   qualification, complete production coefficients, interpolation/refinement,
   production error channels, omitted norms, attained error--complexity masks, and
   threshold passage with sustained status.
2. `rank1-fourier-route-agreement.png`: four panels for direct/mediated coefficient
   defects, construction-sample defects, mediated total errors, and direct total errors.

## Authentication policy

Visualization data is projected by the byte-owning verifier from the admitted result
after the underlying scientific channels have been independently checked. Every
projection field is correlated with its admitted-result source. The visualizer requires
a passing verification whose recorded projection digest equals the exact supplied
projection bytes. Rendering introduces presentation only and publishes figures atomically
through the calling script.

## Exclusions

No Formal-certificate figure, gauge-angle plot, phase optimization, continuum fit,
uncertainty band, inferred smooth frontier, or unauthenticated publication graphic is
supported.

## Related pages

- [Implementation](implementation.md)
- [Schematics](schematics.md)
- [Numerics](numerics.md)
- [Scientific interpretation](scientifics.md)
- [Parent package](../index.md)
- [Shared visualization architecture](../../../visualizations/index.md)
