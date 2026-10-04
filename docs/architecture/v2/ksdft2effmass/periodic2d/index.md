# `ksdft2effmass.periodic2d`

## Purpose and status

`ksdft2effmass.periodic2d` owns canonical two-dimensional scientific definitions,
represented-space comparisons, controlled defects, and provisional campaign surfaces.
The package is implemented. Scientific-model adoption is partial, and campaign
architecture remains under the Phase 7 migration.

The package now owns a parent-qualified selected-band retention definition. That
DataObject declares a selection contract only; it does not claim that preserved
periodic2d campaign results contain a retained subspace or exact retained operator.

## Public contract

The package root deliberately exports supported two-dimensional campaign records,
comparison Actions and results, defect records and Actions, encoded-document owners,
and `Periodic2DSelectedBandRetentionDefinition`. Exact supported names are declared by
`ksdft2effmass.periodic2d.__all__`.

| Child owner | Public responsibility | Canonical page |
|---|---|---|
| `periodic2d.retention` | Parent-qualified two-dimensional selected-band retention definitions | [Retention definitions](retention/index.md) |
| `periodic2d.campaign` | Provisional two-dimensional campaign identities and the typed one-band input definition | [Periodic2d migration boundary](../periodic/periodic2d/index.md) |
| `periodic2d.compare` | Explicit represented-operator transport and threshold-free comparison | [Periodic2d migration boundary](../periodic/periodic2d/index.md) |
| `periodic2d.defects` | Controlled finite-extent scalar-hopping defect definitions and represented analyses | [Periodic2d migration boundary](../periodic/periodic2d/index.md) |
| `periodic2d.model` | Two-dimensional toy-model and representation-specific definitions | [Periodic2d migration boundary](../periodic/periodic2d/index.md) |
| `periodic2d.run` | Preserved executable campaign families and encoded-document owners | [Periodic2d capability-parity gate](../periodic2d-capability-parity.md) |

Canonical module and class pages for untouched legacy owners remain documentation
migration work; the topic pages above continue to state their current architecture.

## Ownership boundary

This package may specialize the general contracts from `ksdft2effmass.periodic` for
exactly two periodic dimensions. It owns project-specific identity, provenance,
retention, comparison, and campaign policy. Reusable direct and reciprocal lattice
primitives remain owned by PhysKit. Generic finite represented operators remain owned
by `ksdft2effmass.operators`.

A selected-band interval does not supply parent-model, parent-operator, ambient-space,
reciprocal-domain, projector, frame, gauge, or provenance identity. Equal dimensions,
rank, spectra, or route names do not establish those meanings.

## Dependency rules

Permitted direct dependencies include the general `ksdft2effmass.periodic` contracts,
reusable analysis and operator records, and pinned PhysKit lattice primitives. Campaign
and filesystem behavior must not flow into scientific retention DataObjects. PhysKit
must not depend on this package.

## Child map

- [Retention definitions](retention/index.md)
  - [`Periodic2DSelectedBandRetentionDefinition`](retention/Periodic2DSelectedBandRetentionDefinition/index.md)
- [Periodic2d migration boundary](../periodic/periodic2d/index.md)
- [Periodic2d capability-parity gate](../periodic2d-capability-parity.md)

## Code mapping

| Code path | Symbol kind | Qualified name | Architecture responsibility |
|---|---|---|---|
| `python/src/ksdft2effmass/periodic2d/__init__.py` | Package | `ksdft2effmass.periodic2d` | Deliberate public two-dimensional API |
| `python/src/ksdft2effmass/periodic2d/retention.py` | Module | `ksdft2effmass.periodic2d.retention` | Parent-qualified two-dimensional retention definitions |
| `python/src/ksdft2effmass/periodic2d/retention.py` | Class | `ksdft2effmass.periodic2d.retention.Periodic2DSelectedBandRetentionDefinition` | Defining selected-band retention class |
| `python/src/ksdft2effmass/periodic2d/__init__.py` | Class | `ksdft2effmass.periodic2d.Periodic2DSelectedBandRetentionDefinition` | Supported package-root re-export of the defining class |

## Test mapping

| Test path | Pytest node | Evidence class | Established behavior |
|---|---|---|---|
| `python/tests/software_verification/ksdft2effmass/periodic2d/test__Periodic2DSelectedBandRetentionDefinition.py` | `TestPeriodic2DSelectedBandRetentionDefinition::test_public_api__package__exports_supported_definition` | Software verification | The package deliberately exports the two-dimensional retention definition |

## Provenance

Original local work under the repository license.

## Evidence

| Evidence kind | Status | Evidence or reason | Reference | Comparator/tolerance | Environment | Validity domain | Accepting authority |
|---|---|---|---|---|---|---|---|
| Software verification | Supported | Exact export and invariant tests | Mapped pytest class | Exact assertions | Supported Python environment | New retention definition | Not applicable |
| Numerical verification | Not applicable | Definition performs no numerical construction | Source contract | Not applicable | Not applicable | Selection metadata | Not applicable |
| Scientific validation | Not evaluated | No model-adequacy claim | Not applicable | Not applicable | Not applicable | Not applicable | Not applicable |
| Uncertainty quantification | Not evaluated | No uncertainty model | Not applicable | Not applicable | Not applicable | Not applicable | Not applicable |
| Human acceptance | Not evaluated | Review and merge remain separate | Review record when available | Not applicable | Not applicable | Changed contract | Named human authority required |

## Limitations and deviations

The new canonical package page maps the retention slice introduced by this change.
Untouched legacy modules do not yet have complete canonical module/class mirrors and are
not silently declared complete here. Existing migration and capability pages remain the
authoritative status records for those owners.
