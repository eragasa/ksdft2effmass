# `periodic1d.retention`

## Purpose and status

This implemented module specializes general parent-qualified scientific retention for
one-dimensional selected bands and binds mathematical retained spaces to distinct
numerical representations.

## Public inventory

| Symbol | Scientific category | Responsibility |
|---|---|---|
| `Periodic1DSelectedBandRetentionDefinition` | Retention definition | Parent-qualified contiguous band selection |
| `Periodic1DRetainedBandGroupDefinition` | Retention definition | Stable campaign-facing group identity |
| `Periodic1DOrthogonalSpectralRetainedSubspace` | Retained-space representation | Bind one mathematical retained space to an eigenspace embedding |
| `Periodic1DBandFrameRetainedSubspace` | Gauge-dependent retained-space representation | Bind one mathematical retained space to an authenticated reciprocal frame path |

## Class navigation

- [`Periodic1DSelectedBandRetentionDefinition`](Periodic1DSelectedBandRetentionDefinition/index.md)
- [`Periodic1DRetainedBandGroupDefinition`](Periodic1DRetainedBandGroupDefinition/index.md)
- [`Periodic1DOrthogonalSpectralRetainedSubspace`](Periodic1DOrthogonalSpectralRetainedSubspace/index.md)
- [`Periodic1DBandFrameRetainedSubspace`](Periodic1DBandFrameRetainedSubspace/index.md)

## Separation of meanings

A selection definition names intended parent bands but stores no projector. A
`PeriodicRetainedSubspace` identifies a mathematical retained space and representation
witness. A spectral embedding or reciprocal frame represents that space numerically.
A frame additionally chooses gauge. None of these objects is a represented Hamiltonian
or effective model.

## Code, tests, and Sphinx

| Kind | Path | Responsibility |
|---|---|---|
| Code | `python/src/ksdft2effmass/periodic1d/retention.py` | One-dimensional retention and representation bindings |
| Tests | `python/tests/software_verification/ksdft2effmass/periodic1d/test__Periodic1D*Retained*.py` | Parent/rank/dimension/content evidence |
| Sphinx | `doc/sphinx/api/ksdft2effmass/periodic1d/retention.rst` | Public API and separation contract |
| Concept | `doc/sphinx/concepts/scientific-retention.rst` | Scientist-facing retention hierarchy |

## Provenance, evidence, and limitations

Original local work under the repository license. Synthetic tests establish declared
identity, dimension, ordering, and content-binding behavior only. They do not establish
parent correctness, band isolation, convergence, physical adequacy, scientific
validation, uncertainty quantification, or acceptance.
