# `Periodic1DSelectedBandRetentionDefinition`

## Purpose and status

This implemented row-019 DataObject binds an inclusive contiguous zero-based band
interval to one complete one-dimensional `PeriodicRetentionDefinition`.

## Public contract

Supported import:
`from ksdft2effmass.periodic1d import Periodic1DSelectedBandRetentionDefinition`.
`band_indices` returns ascending parent-band indices in the same order as
`retention.ordered_state_labels`.

## Invariants and failure behavior

Both fields require exact public semantic types. The parent operator is one-dimensional,
the construction kind is `SELECTED_BANDS`, and retained rank equals the interval's band
count. Type failures raise `TypeError`; semantic mismatches raise `ValueError`.

## Scientific boundary

The record identifies intended parent bands and preserves parent operator, ambient
state-space, reciprocal-domain, construction, assumptions, provenance, ordering, and
rank. It stores no eigenvalues, projector, frame, gauge, represented operator, or
finite matrix. Band indices alone do not prove isolation or continuity.

## Code and evidence mapping

| Kind | Path or node | Established behavior |
|---|---|---|
| Code | `python/src/ksdft2effmass/periodic1d/retention.py:Periodic1DSelectedBandRetentionDefinition` | Parent-qualified selection |
| Test | `TestPeriodic1DSelectedBandRetentionDefinition::test_construction__fields__binds_parent_selection_and_order` | Parent, interval, order, and rank correlation |
| Tests | Other methods in the same class | Dimension, kind, rank, and public-export failures |
| Sphinx | `doc/sphinx/api/ksdft2effmass/periodic1d/retention.rst` | Public API and scientific boundary |

## Provenance and limitations

Original local work under the repository license. Synthetic tests establish software
relations only, not isolation, projector accuracy, convergence, material validity,
uncertainty, or acceptance.
