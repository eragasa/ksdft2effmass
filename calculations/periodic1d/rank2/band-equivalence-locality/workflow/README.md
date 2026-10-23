# Calculation workflow

This package owns the calculation-specific periodic-1D rank-two band-equivalence and locality workflow: definitions, result records, calculation actions, serialization for the flat development branch, and independent reconstruction checks.

It is not part of the installed `ksdft2effmass` library API. Generic matrix-field, Fourier, optimization, and PhysKit capabilities remain with their canonical reusable owners. The calculation-root `run_*_development.py` files are thin composition and tabulation entrypoints over this package.

Current status: migration-in-progress development workflow. The flat and non-flat branches do not constitute a retained production evidence package, and strict non-flat serialization remains open.
