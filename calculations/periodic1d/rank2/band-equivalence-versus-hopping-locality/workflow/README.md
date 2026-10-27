# Calculation workflow

This package owns the calculation-specific periodic-1D rank-two
band-equivalence-versus-hopping-locality behavior: flat, nonflat, and truncation
definitions; result and verification records; calculation actions; strict development
serialization; independent reconstruction; diagnostic-table admission; and figure
composition.

The nonflat and truncation namespaces remain scientifically distinct. Truncation keeps
cyclic conversion, finite interpolation, deliberate ordinary-lattice truncation, and
total Hamiltonian and spectral consequences in separate channels. The diagnostic bundle
validates producer-owned tables and returns defensive copies; it does not create a
second scientific provenance system.

This package is not part of the installed `ksdft2effmass` public API. Generic
matrix-field, Fourier, optimization, and PhysKit capabilities remain with their canonical
reusable owners. The calculation-root `run_*_development.py` files are explicit effect
adapters over this package.

Current status: migration-in-progress development workflow. Passing software and
reconstruction checks do not create a retained execution, protocol freeze, evidence
package, or scientific validation. Reusable behavior still requires extraction into
cohesive reviewed source owners before a retained direct lifecycle can be proposed.
