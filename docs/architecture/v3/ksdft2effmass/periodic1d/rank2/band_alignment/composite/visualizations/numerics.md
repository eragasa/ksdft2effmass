# Visualization numerical contract

Visualization-data constructors validate every plotting array's type, unit, shape,
ordering, and nonnegativity. The visualizer requires a passing aggregate whose data
digest matches the exact canonical bytes. The root `PngFigureRenderer` encodes and
closes each figure.

Coordinates, spectra, defects, hopping norms, ranges, conversion powers, interpolation
errors, deliberate-truncation errors, and total consequences come from the verified
data. Rendering performs no eigensolve, alignment, Fourier transform, truncation, or
error calculation. The same integer ranges are exposed through distinct hopping-
diagnostic and retained-support inventory types. The canonical data bytes remain stable;
the closed render inventory contains six members.
