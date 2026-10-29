# Numerical contract

The shared visualization package performs no model calculation, eigensolve, basis
transformation, alignment, Fourier transform, fit, norm evaluation, threshold search,
interpolation, truncation, or uncertainty calculation.

Permitted presentation operations are limited to operations whose inputs and meaning are
already fixed by the authenticated family projection, including:

- selecting a recorded finite series;
- choosing axis scales and finite limits;
- arranging supplied arrays into panels;
- drawing markers, lines, bars, intervals, and labels from supplied values;
- applying a projection-recorded normalization or a presentation transform explicitly
  documented by the family; and
- encoding the resulting Matplotlib figure as PNG.

A connected line joins an explicitly ordered finite inventory. It does not create an
interpolant or an unrecorded scientific sample. Logarithmic scales require positive
supplied values; symmetric-logarithmic scales may display exact recorded zeros. Missing,
failed, unresolved, or nonfinite scientific states must be rejected by the projection or
represented explicitly by a family contract rather than silently omitted.

The root package validates generic container properties only. Units, shapes, ordering,
nonnegativity, normalization, correlated lengths, masks, and scientific field meaning
belong to the family projection constructor and independent verifier.

PNG decoding validates an image container. No tolerance on pixels, layout, fonts,
colors, antialiasing, or encoded bytes is implied by that admission. A family that needs
visual-regression evidence must define and own a separate comparison contract.
