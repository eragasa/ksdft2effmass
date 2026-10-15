# `ksdft2effmass.analysis.model_adequacy.hopping_shell_hierarchy.results`

## Purpose and status

Prospective immutable proof and result objects for HSH-1. No source module exists.

## Prospective public contract inventory

- [`Periodic2DHoppingShellDisposition`](Periodic2DHoppingShellDisposition/index.md)
- [`Periodic2DHoppingShellQuadraticLoss`](Periodic2DHoppingShellQuadraticLoss/index.md)
- [`Periodic2DHoppingShellSupportCertificate`](Periodic2DHoppingShellSupportCertificate/index.md)
- [`Periodic2DHoppingShellClassResult`](Periodic2DHoppingShellClassResult/index.md)
- [`Periodic2DHoppingShellHierarchyResult`](Periodic2DHoppingShellHierarchyResult/index.md)

No record accepts mutable arrays or unspecified mappings.

## Represented objects

Quadratic-loss objects represent one channel on one active shell slice. Support
certificates represent one conservative directional lower bound in the common maximal
metric. Class results correlate channel geometry, feasible points, distance intervals,
withheld diagnostics, and one disposition. The hierarchy result correlates all classes
with nesting and any critical-class conclusion.

## Invariants, units, and failure behavior

All collections are immutable and canonically ordered. Active-coordinate objects carry
explicit maximal-space indices. Losses and distance bounds are dimensionless; hopping
coefficients remain in the declared parent energy unit; withheld spectral errors retain
that energy unit.

Constructors reject inconsistent optional fields, invalid enum/certificate
combinations, negative bounds, lower bounds above upper bounds, nonzero inactive
coordinates, duplicate shells, non-nested class inventories, and unsupported minimality
claims. Invalid records raise `TypeError` or `ValueError`; they are never normalized or
reclassified silently.

## Dependencies and neighboring owners

These records depend on immutable standard-library types, narrow numerical validation,
and the sibling
`analysis.model_adequacy.losses.DimensionlessPositiveDefiniteQuadraticLoss`. The HSH
wrapper composes rather than subclasses that primitive. These records do not execute
solvers, decode JSON, inspect manifests, or decide human acceptance.

## Class navigation

- [`Periodic2DHoppingShellDisposition`](Periodic2DHoppingShellDisposition/index.md)
- [`Periodic2DHoppingShellQuadraticLoss`](Periodic2DHoppingShellQuadraticLoss/index.md)
- [`Periodic2DHoppingShellSupportCertificate`](Periodic2DHoppingShellSupportCertificate/index.md)
- [`Periodic2DHoppingShellClassResult`](Periodic2DHoppingShellClassResult/index.md)
- [`Periodic2DHoppingShellHierarchyResult`](Periodic2DHoppingShellHierarchyResult/index.md)

## Prospective code mapping

| Planned path | Symbol kind | Planned qualified name | Responsibility |
|---|---|---|---|
| `python/src/ksdft2effmass/analysis/model_adequacy/hopping_shell_hierarchy/results.py` | Module | `ksdft2effmass.analysis.model_adequacy.hopping_shell_hierarchy.results` | Immutable HSH-1 proof/result model |

Class mappings are on the linked class pages.

## Test mapping

Planned result tests mutate active indices, matrix cross terms, feasible points,
certificate fields, distance intervals, dispositions, class ordering, and minimality
claims. See [testing](../testing.md). No test exists.

## Sphinx mapping

No Sphinx page exists. The intended page is
`doc/sphinx/api/ksdft2effmass/analysis/model_adequacy/hopping_shell_hierarchy.rst`.

## Provenance

Original local work under the repository license.

## Evidence

| Evidence kind | Status | Evidence or reason | Validity domain |
|---|---|---|---|
| Software verification | Not evaluated | Records and tests do not exist | None |
| Numerical verification | Not evaluated | No proof object has been reconstructed | None |
| Scientific validation | Not evaluated | Synthetic parent only | None |
| Uncertainty quantification | Not evaluated | No uncertainty semantics | None |
| Human acceptance | Not evaluated | No result exists | None |

## Limitations and deviations

Field-level parameter prose awaits source docstrings. These architecture pages fix
relationships and invariants without pretending that the wire schema is finalized.
