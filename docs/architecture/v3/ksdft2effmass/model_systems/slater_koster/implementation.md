# Slater--Koster implementation

## Ownership

The reusable package is
`python/src/ksdft2effmass/model_systems/slater_koster/`:

- `geometry.py` uses PhysKit's `DirectLattice3D` and PhysKit scalar quantities rather
  than defining a competing lattice primitive;
- `parameters.py` owns immutable eV parameter records and the stable vector map;
- `model.py` owns bond-direction maps, Bloch assembly, and exact-Hermitian refinement;
- `serialization.py` delegates canonical bytes to `TypedJsonMappingSerializer`; and
- `__init__.py` declares the supported public imports.

Campaign declarations, authorization, scientific coordinates, evidence disposition,
and acceptance remain under `calculations/Si/bulk/`. The reusable package has no
filesystem or calculator effects.

## Numeric boundaries

Public array inputs require NumPy arrays with real integer or floating dtype. Boolean
arrays, numeric strings, nonfinite values, and incorrect shapes are rejected rather
than coerced. Energies require PhysKit `ScalarQuantity` values in `electron_volt`; the
lattice parameter requires `angstrom`. Returned parameter and hopping arrays use
immutable byte-backed binary64 storage. Arithmetic is not clipped; nonfinite phase or
matrix results from binary64 overflow raise `OverflowError`.

## Synthetic verification

Focused tests under
`python/tests/ksdft2effmass/model_systems/slater_koster/` check:

- right-handed primitive geometry and complete first/second shells;
- parameter order, units, immutability, and invalid numeric boundaries;
- $T(-d)=T(d)^\mathsf{T}$ and fixed-zero first-neighbor channels;
- analytic Gamma-point shell sums;
- Hermiticity and spinless time reversal at a generic k point;
- reciprocal-shift gauge covariance and cubic-axis spectral symmetry; and
- deterministic convention-rich typed JSON.

These are software-verification tests with synthetic parameters. They do not validate a
silicon fit or authorize Level 2.
