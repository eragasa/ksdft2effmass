# `periodic1d.model`

## Purpose and status

This implemented module owns the complete untruncated one-dimensional Fourier toy parent
and separately identified finite plane-wave representations of that parent.

## Public contract inventory

| Symbol | Category | Responsibility |
|---|---|---|
| `Periodic1DFourierHamiltonianToyModel` | Scientific model | Kinetic law, Fourier potential, model/state-space/domain identities |
| `Periodic1DPlaneWaveParentRepresentation` | Finite parent representation | Basis, mesh, finite operator reference, map, and provenance |
| `Periodic1DPlaneWaveParentRepresentationConstructor` | ActionObject | Explicit finite representation construction |

The untruncated parent and finite Galerkin representation use distinct state-space
identities. Exact retention from the finite parent does not erase discretization error
relative to the untruncated law.

## Class navigation

- [`Periodic1DFourierHamiltonianToyModel`](Periodic1DFourierHamiltonianToyModel/index.md)

The finite representation pages are completed with the row-023 dossier.

## Code, tests, and Sphinx

| Kind | Path or node | Responsibility |
|---|---|---|
| Code | `python/src/ksdft2effmass/periodic1d/model.py` | Parent and finite representation owners |
| Test | `python/tests/software_verification/ksdft2effmass/periodic1d/test__Periodic1DFourierHamiltonianToyModel.py::TestPeriodic1DFourierHamiltonianToyModel` | Parent identity, units, and scale |
| Test | `python/tests/software_verification/ksdft2effmass/periodic1d/test__Periodic1DPlaneWaveParentRepresentation.py` | Finite-parent separation and correlation |
| Sphinx | `doc/sphinx/api/ksdft2effmass/periodic1d/model.rst` | Equation, parent/representation distinction, public API |

## Provenance, evidence, and limitations

Original local work under the repository license. Synthetic tests establish software
behavior. Discretization comparisons are separate numerical evidence and do not prove an
untruncated-parent error bound, material validation, uncertainty quantification, or
acceptance.
