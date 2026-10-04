# `ksdft2effmass.periodic2d.retention`

## Purpose and status

This implemented module owns two-dimensional specializations that bind method-specific
selection data to general parent-qualified periodic retention definitions. It currently
exports one immutable selected-band definition.

## Public contract inventory

| Symbol | Kind | Supported route | Meaning |
|---|---|---|---|
| `Periodic2DSelectedBandRetentionDefinition` | DataObject | `ksdft2effmass.periodic2d.Periodic2DSelectedBandRetentionDefinition` | Bind a contiguous ordered band interval to a two-dimensional parent-qualified retention definition |

## Represented scientific objects

The module represents a **retention definition**: a declaration of which ordered parent
bands are selected and the stable identities governing that selection. It does not
represent a retained mathematical subspace, projector, frame, exact retained operator,
represented matrix, or effective model.

## Invariants, conventions, and failure behavior

- `retention` is exactly `PeriodicRetentionDefinition`.
- `selection` is exactly `ContiguousBandSelection`.
- The parent operator reference has spatial dimension two.
- The general kind is exactly `SELECTED_BANDS`.
- General retained rank equals the inclusive selected-band count.
- Ascending band indices correspond elementwise to ordered retained-state labels.

Wrong semantic types raise `TypeError`; dimension, kind, and rank contradictions raise
`ValueError`. The definition introduces no units, gauge, energy reference, or geometry
because those belong to later retained-space/operator representations and their parent
contracts.

## Dependency and neighboring-owner rules

The module composes the general retention owner from `ksdft2effmass.periodic` and the
reusable interval from `ksdft2effmass.analysis.periodic_bands`. It must not depend on a
campaign, payload decoder, filesystem location, represented matrix, or execution route.

## Class navigation

- [`Periodic2DSelectedBandRetentionDefinition`](Periodic2DSelectedBandRetentionDefinition/index.md)

## Code mapping

| Code path | Symbol kind | Qualified name | Architecture responsibility |
|---|---|---|---|
| `python/src/ksdft2effmass/periodic2d/retention.py` | Module | `ksdft2effmass.periodic2d.retention` | Two-dimensional selection-definition ownership |
| `python/src/ksdft2effmass/periodic2d/retention.py` | Class | `ksdft2effmass.periodic2d.retention.Periodic2DSelectedBandRetentionDefinition` | Defining parent-qualified contiguous-band class |
| `python/src/ksdft2effmass/periodic2d/__init__.py` | Class | `ksdft2effmass.periodic2d.Periodic2DSelectedBandRetentionDefinition` | Supported package-root re-export of the defining class |

## Test mapping

| Test path | Pytest node | Evidence class | Established behavior |
|---|---|---|---|
| `python/tests/software_verification/ksdft2effmass/periodic2d/test__Periodic2DSelectedBandRetentionDefinition.py` | `TestPeriodic2DSelectedBandRetentionDefinition` | Software verification | Exact types, parent dimension, kind, rank, ordering, immutability, and export behavior |

## Sphinx mapping

| Sphinx path | Documented route | Role |
|---|---|---|
| `doc/sphinx/api/ksdft2effmass/periodic2d/retention.rst` | `ksdft2effmass.periodic2d.Periodic2DSelectedBandRetentionDefinition` | User-facing API and scientific boundary |
| `doc/sphinx/concepts/scientific-retention.rst` | General and dimensional retention definitions | Conceptual separation of selections, spaces, operators, and representations |

## Provenance

Original local work under the repository license.

## Evidence

| Evidence kind | Status | Evidence or reason | Reference | Comparator/tolerance | Environment | Validity domain | Accepting authority |
|---|---|---|---|---|---|---|---|
| Software verification | Supported | Exact construction and failure tests | Mapped pytest class | Exact assertions | Supported Python environment | Synthetic definition inputs | Not applicable |
| Numerical verification | Not applicable | No numerical algorithm | Source contract | Not applicable | Not applicable | Not applicable | Not applicable |
| Scientific validation | Not evaluated | Selection adequacy is not assessed | Not applicable | Not applicable | Not applicable | Not applicable | Not applicable |
| Uncertainty quantification | Not evaluated | No uncertainty model | Not applicable | Not applicable | Not applicable | Not applicable | Not applicable |
| Human acceptance | Not evaluated | Review and merge remain separate | Review record when available | Not applicable | Not applicable | Changed contract | Named human authority required |

## Limitations and deviations

No retained subspace or operator specialization is implemented. The preserved isolated
and composite campaign results do not provide authenticated frame or projector
coordinates sufficient to add one without a separate evidence contract.
