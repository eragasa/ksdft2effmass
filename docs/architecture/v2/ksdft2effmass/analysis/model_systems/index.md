# `analysis.model_systems`

## Purpose and status

This implemented subpackage owns reusable, explicitly represented model-system
components and numerical constructions used to verify higher-level scientific routes.
A component or representation definition does not acquire nominal `PeriodicModel`
membership from its historical name.

## Child map

| Child | Responsibility | Canonical page |
|---|---|---|
| `periodic_1d` | Unit-aware one-dimensional Fourier potentials and finite represented fibers | [Periodic 1D model systems](periodic_1d/index.md) |
| `periodic2d` | Two-dimensional finite plane-wave and reciprocal-mesh constructions | [Periodic 2D model systems](periodic2d/index.md) |

## Ownership and dependencies

The package may compose operator quantities and PhysKit lattice primitives. Scientific
parent models explicitly compose these reusable values where appropriate. Campaign
policy, retained bytes, scientific acceptance, and calculator execution do not belong
here.

## Code, tests, and Sphinx

| Kind | Path | Responsibility |
|---|---|---|
| Package | `python/src/ksdft2effmass/analysis/model_systems/__init__.py` | Deliberate public model-system exports |
| Tests | `python/tests/software_verification/ksdft2effmass/analysis/model_systems/` | Software contracts |
| Tests | `python/tests/numerical_verification/ksdft2effmass/analysis/model_systems/` | Analytic and manufactured numerical checks |
| Sphinx | `doc/sphinx/api/model-systems.rst` | Public API |

## Provenance, evidence, and limitations

Original local work under the repository license. Evidence classification belongs to
each object and test. Reusable numerical behavior does not establish material realism,
scientific validation, uncertainty quantification, or acceptance.
