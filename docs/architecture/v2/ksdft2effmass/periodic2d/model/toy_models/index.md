# `periodic2d.model.toy_models`

## Purpose and status

This implemented subpackage exposes controlled periodic-2D toy parents and their
specific finite representation routes. Explicit imports replace discovery or a dynamic
model registry.

## Public child map

| Module | Responsibility | Canonical page |
|---|---|---|
| `cosine` | Dimensionless period-`2*pi` cosine parent, basis/grid definitions, requests, results, and constructors | [Cosine model](cosine/index.md) |

## Ownership boundary

Toy-model role marks controlled scientific intent. It does not establish that all toy
models share one solver, serializer, observable, tolerance, or comparison route. Finite
plane-wave and finite-difference outputs remain represented objects separate from the
cosine parent.

## Code and evidence mapping

| Kind | Path | Responsibility |
|---|---|---|
| Package | `python/src/ksdft2effmass/periodic2d/model/toy_models/__init__.py` | Deliberate public exports |
| Tests | `python/tests/ksdft2effmass/periodic2d/model/toy_models/` | Source-specific model and representation evidence |
| Sphinx | `doc/sphinx/api/research-monograph-campaigns.rst` | Current public API surface |

## Provenance, evidence, and limitations

Original local work under the repository license. Individual tests establish bounded
software/numerical behavior; no material realism, scientific validation, uncertainty
quantification, or acceptance follows. Canonical class pages are added as their
crosswalk dossiers are audited.
