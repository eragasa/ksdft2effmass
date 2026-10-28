# `ksdft2effmass.model_systems`

## Purpose

The shared model-system layer owns reusable lifecycle behavior without erasing the
physical and numerical distinctions among model systems. PIAB1D, QHO1D, and Mathieu1D
remain separate scientific owners; they share typed boundaries, verification sequencing,
and presentation mechanics only where that behavior has the same meaning.

## Common typed lifecycle

PIAB1D, QHO1D, and Mathieu1D configurations and results remain concrete model-owned
records with their exact fields, units, shapes, correlations, and wire layouts. The shared layer
begins only where behavior is genuinely identical.

`BaseModelAnalysisVerifier` owns the common subject boundary:

1. require the exact result wire as an immutable built-in `bytes` value;
2. calculate its lowercase SHA-256 identity internally;
3. deserialize those same bytes through the shared typed JSON boundary;
4. reconstruct the model-specific root result;
5. derive the model-specific visualization projection;
6. hash its canonical typed JSON bytes;
7. calculate model-specific independent verification components; and
8. compose the model-specific aggregate verification.

For later consumption, `admit_stored()` repeats that complete derivation from the exact
result bytes and requires canonical byte equality with both the stored aggregate and the
stored visualization projection. It returns the independently recomputed pair rather
than trusting the decoded stored values. This single comparison rejects omitted,
renamed, additional, or altered observations without a second literal inventory of every
dynamically generated comparison name.

`BaseModelAnalysisVerification` owns digest validation, global observation-name
uniqueness, pass reduction, flattened value and tolerance reporting, and access to the
authenticated projection digest. Concrete aggregates retain their component inventories and wire layouts, including the
retained QHO1D layout and Mathieu1D's two-component, 873-comparison aggregate.

The shared layer does not implement scientific references, comparison inventories,
tolerances, acceptance policy, or a nominal analyzer type. PIAB1D, QHO1D, and Mathieu1D
analyzers remain concrete because their executed operations have different signatures.

## Flexible visualization composition

Visualization is separated into independently replaceable responsibilities:

```text
model-specific values
        │
        ▼
BaseModelAnalysisPlot.draw(axis)
        │  one data-to-mark relation
        ▼
BaseModelAnalysisSubplot.draw(axis)
        │  plot composition and axis-local presentation
        ▼
BaseModelAnalysisFigure.draw()
        │  subplot layout and figure-wide presentation
        ▼
BaseModelAnalysisFigureRenderer.visualize()
        │  encoding into an immutable admitted visualization
        ▼
BaseModelAnalysisVisualizer.visualize()
           complete authenticated figure inventory
```

A concrete figure may choose any Matplotlib layout and may compose zero or more
explicit subplot and plot actions. The common layer does not impose a universal grid,
axis count, plot style, or scientific projection. PNG admission remains independent
of plotting and validates the encoded image container only.

## Boundaries

- Model-specific scientific values are not flattened into a universal DTO.
- Shared bases do not select continuum references, finite representations, norms,
  tolerances, convergence meanings, or retained dimensions.
- Independent verification does not call production analyzers.
- Historical result, verification, rendering, and provenance bytes are not rewritten.
- Refactoring presentation code does not establish scientific validation or visual
  equivalence unless an explicit comparison says so.

## Periodic1D relationship

`model_systems.periodic_1d` owns unit-aware finite Fourier potentials and plane-wave or
periodic finite-difference fiber construction. `model_systems.mathieu1d` owns the
concrete Mathieu model. Neither is a generic campaign or a substitute for the
scientifically distinct scalar, composite, admissible-set, and higher-rank families
owned by `ksdft2effmass.periodic1d` and their calculation roots.

The [Periodic1D rewrite plan](../periodic1d/index.md) may reuse the common byte-owning
verification and flexible visualization behavior described here. It does not add a
`model_systems.periodic1d` alias, move lattice behavior out of PhysKit, or impose a
universal periodic result record.

## Implemented children

- [PIAB1D](piab1d/index.md)
- [QHO1D](qho1d/index.md)
- [Mathieu1D](mathieu1d/index.md)
