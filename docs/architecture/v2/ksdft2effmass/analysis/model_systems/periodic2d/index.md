# `analysis.model_systems.periodic2d`

## Purpose and status

This implemented subpackage owns reusable finite two-dimensional periodic numerical
constructions. PhysKit owns primitive direct and reciprocal lattices; this package owns
ksdft-specific representation definitions, requests, results, and Actions until a
separately reviewed reusable migration exists.

## Child map

| Module | Responsibility | Canonical page |
|---|---|---|
| `plane_waves` | Finite spinless scalar plane-wave Bloch operators | [Plane-wave operators](plane_waves/index.md) |
| `finite_differences` | Finite spinless scalar centered-difference Bloch operators | [Finite-difference operators](finite_differences/index.md) |
| `reciprocal_mesh` | Reciprocal neighbors and sewing mechanics | Existing Sphinx API; canonical dossier pending its crosswalk owner |

## Boundary

Finite matrices are representations of declared operators. They are not scientific
models, retained subspaces, exact retained operators, or campaign conclusions. Reduced
coordinates, lattice duality, basis ordering, units, and energy references remain
explicit.

## Code and evidence

| Kind | Path | Responsibility |
|---|---|---|
| Package | `python/src/ksdft2effmass/analysis/model_systems/periodic2d/__init__.py` | Public reusable 2D numerical API |
| Tests | `python/tests/software_verification/ksdft2effmass/analysis/model_systems/periodic2d/` | Invariant evidence |
| Tests | `python/tests/numerical_verification/ksdft2effmass/analysis/model_systems/periodic2d/` | Analytic matrix evidence |
| Sphinx | `doc/sphinx/api/ksdft2effmass/analysis/model_systems/periodic2d/` | User-facing API and mathematics |

Original local work under the repository license. No material validation or uncertainty
claim follows from the represented numerical tests.
