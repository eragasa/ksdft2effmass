# `Periodic1DRetainedBandGroupDefinition`

## Purpose and status

This implemented row-020 DataObject gives one parent-qualified selected-band retention
definition a stable nonempty campaign-facing group identity.

## Public contract and invariants

Supported import:
`from ksdft2effmass.periodic1d import Periodic1DRetainedBandGroupDefinition`.
The exact built-in string `identifier` must be nonempty, and `retained_bands` must be the
exact selected-band definition type. Convenience properties expose its selection,
lower/upper indices, and rank without copying or weakening parent qualifications.

## Scientific boundary

A group is a named retention definition. It is not a projector, frame, gauge,
represented matrix, retained operator, or effective model. Group naming adds no
physical compatibility or equivalence claim.

## Code and evidence mapping

| Kind | Path or node | Established behavior |
|---|---|---|
| Code | `python/src/ksdft2effmass/periodic1d/retention.py:Periodic1DRetainedBandGroupDefinition` | Stable group identity and delegation |
| Test | `TestPeriodic1DRetainedBandGroupDefinition::test_construction__group__preserves_parent_qualified_order_and_rank` | Exact nested record, order, and rank |
| Test | `TestPeriodic1DRetainedBandGroupDefinition::test_construction__identifier__rejects_empty_group_identity` | Nonempty identity failure |
| Sphinx | `doc/sphinx/api/ksdft2effmass/periodic1d/retention.rst` | Public API |

## Provenance and limitations

Original local work under the repository license. Synthetic software tests do not
establish band isolation, convergence, scientific validation, uncertainty, or
acceptance.
