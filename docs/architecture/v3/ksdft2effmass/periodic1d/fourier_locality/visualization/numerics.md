# Visualization numerics

Plot coordinates, energies, coefficients, norms, errors, thresholds, masks, flags, and
markers are copied from the authenticated projection. Rendering does not recompute an
eigensystem, Fourier transform, fit, norm, threshold crossing, or dominance relation.

Presentation-only transformations are limited to explicitly reversible or labelled forms
such as coefficient magnitude, normalization by recorded `E_ref`, axis scaling, finite
mask selection, and stacking already recorded series. Symmetric-logarithmic axes display
exact zero diagnostics without clipping them; logarithmic construction-size axes are used
only where every supplied extent is positive.

Connected lines join authored ordered finite inventories. They do not interpolate new
scientific samples. Error--complexity and threshold-passage markers use authenticated
per-mesh masks and flags; no frontier or missing passage is inferred by the renderer.

The shared PNG renderer validates finite arrays, closed plot identifiers, dimensions,
and encoded PNG structure. Atomic publication belongs to `run_03_render.py`, not to the
visualization classes.
