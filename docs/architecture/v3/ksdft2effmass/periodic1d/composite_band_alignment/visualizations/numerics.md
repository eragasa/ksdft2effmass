# Visualization numerical contract

Projection constructors validate every plotting array's type, unit, shape, ordering,
and nonnegativity. The visualizer requires a passing aggregate whose projection digest
matches the exact canonical data bytes. The root `PngFigureRenderer` encodes and closes
each figure.

Coordinates, spectra, defects, hopping norms, ranges, conversion powers, interpolation
errors, deliberate-truncation errors, and total consequences come from the authenticated
projection. Rendering performs no eigensolve, alignment, Fourier transform, truncation,
or error calculation. The package migration preserves canonical projection bytes and
the exact three-member inventory.
