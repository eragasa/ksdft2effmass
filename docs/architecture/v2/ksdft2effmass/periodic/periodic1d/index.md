# `ksdft2effmass.periodic1d`

## Purpose and status

`ksdft2effmass.periodic1d` owns maintained one-dimensional periodic scientific
models, represented-operator transformations, and controlled synthetic calculations.
The namespace is the material-neutral methodological baseline for higher-dimensional
and material-specific programs.

The following controlled calculations are implemented and retained:

- **M1** — isolated-band Fourier reduction and finite-range diagnostics;
- **M2** — rank-two frame alignment, gauge attack, and locality diagnostics; and
- **M3** — constrained spectral/operator admissible sets with a common witness and a
  bounded separation certificate.

M1--M3 perform deterministic local numerical work only. They do not execute Quantum
ESPRESSO, Wannier90, a scheduler, or another external calculator. Their retained
results are synthetic software/numerical evidence, not material validation,
uncertainty quantification, or scientific acceptance.

M4 is a separate draft two-dimensional protocol under
`calculations/ICMSEP2026/conference/paper_1/two-dimensional-common-space/`. It has not
been frozen or executed and has no scientific result.

## Public contract

The supported controlled-study routes are exported from `ksdft2effmass.periodic1d`:

| Child | Responsibility | Status |
|---|---|---|
| [`model`](model/index.md) | Fourier and finite-hopping toy parent models | Implemented |
| [`isolated_band`](isolated_band/index.md) | M1 definition, calculator, results, serializer, and verifier | Implemented and retained |
| [`multiband_alignment`](multiband_alignment/index.md) | M2 rank-two alignment/locality study | Implemented and retained |
| [`admissible_sets`](admissible_sets/index.md) | M3 continuous-parameter, finite-angle admissible-set study | Implemented and retained |

Other `periodic1d` modules own reusable retained-space, hopping, representation, or
campaign capabilities. Those capabilities are not redefined by the M1--M3 packages.

## Ownership boundary

This namespace owns:

- one-dimensional model identities and representation conventions;
- M1--M3 control, result, serialization, and verification contracts;
- separation of training and staggered evaluation roles;
- finite-range hopping and constrained-alignment policy; and
- retained synthetic evidence identities.

Reusable lattice geometry and Bloch finite-difference primitives are owned by PhysKit.
General operator quantities and state-space records are owned by their existing
`ksdft2effmass.operators` and `ksdft2effmass.solid_state` modules. Quantum ESPRESSO and
Wannier90 own first-principles calculation and localization respectively.

## Dependency rules

M3 composes M2; it does not subclass it. M2 and M1 depend on reusable analysis and
solid-state actions. Scientific models may inherit from `Periodic1DModel`; milestones,
calculations, serializers, and verifiers must not form a milestone inheritance tree.
PhysKit must not depend on `ksdft2effmass`.

## Code mapping

| Code path | Symbol kind | Qualified name | Responsibility |
|---|---|---|---|
| `python/src/ksdft2effmass/periodic1d/__init__.py` | Package | `ksdft2effmass.periodic1d` | Deliberate public exports |
| `python/src/ksdft2effmass/periodic1d/model.py` | Module | `ksdft2effmass.periodic1d.model` | Controlled parent models |
| `python/src/ksdft2effmass/periodic1d/isolated_band/` | Package | `ksdft2effmass.periodic1d.isolated_band` | M1 |
| `python/src/ksdft2effmass/periodic1d/multiband_alignment/` | Package | `ksdft2effmass.periodic1d.multiband_alignment` | M2 |
| `python/src/ksdft2effmass/periodic1d/admissible_sets/` | Package | `ksdft2effmass.periodic1d.admissible_sets` | M3 |

## Test mapping

| Test path | Pytest class | Evidence class | Established boundary |
|---|---|---|---|
| `python/tests/software_verification/ksdft2effmass/periodic1d/test__Periodic1DIsolatedBandCalculator.py` | `TestPeriodic1DIsolatedBandCalculator` | Software/numerical verification | M1 composition, determinism, serialization, and reconstruction |
| `python/tests/software_verification/ksdft2effmass/periodic1d/test__Periodic1DMultibandAlignmentCalculator.py` | `TestPeriodic1DMultibandAlignmentCalculator` | Software/numerical verification | M2 alignment-channel separation and tamper detection |
| `python/tests/software_verification/ksdft2effmass/periodic1d/test__Periodic1DConstrainedAdmissibleSetCalculator.py` | `TestPeriodic1DConstrainedAdmissibleSetCalculator` | Software/numerical verification | M3 composition, witnesses, certificates, and strict boundaries |
| `python/tests/software_verification/ksdft2effmass/periodic1d/test__Periodic1DConstrainedAdmissibleSetThresholdSensitivity.py` | `TestPeriodic1DConstrainedAdmissibleSetThresholdSensitivity` | Software verification | Post-hoc source correlation and quadratic-premise rejection |

## Sphinx mapping

The user-facing API is documented by:

- `doc/sphinx/api/ksdft2effmass/periodic1d/model.rst`;
- `doc/sphinx/api/ksdft2effmass/periodic1d/isolated_band.rst`;
- `doc/sphinx/api/ksdft2effmass/periodic1d/multiband_alignment.rst`; and
- `doc/sphinx/api/ksdft2effmass/periodic1d/admissible_sets.rst`.

## Provenance

Original local work under the repository license. Retained calculation chronology and
byte identities are governed by each calculation package, its freeze record,
amendments, and manifests. Documentation amendments use separate current-source and
package sidecars rather than silently rewriting historical manifests. M1 amendment 1
records that its historical source manifest does not correlate with identified commit
`ee89d347`; the current-source sidecar is not represented as execution source.

## Evidence

| Evidence kind | Status | Evidence or reason | Validity domain |
|---|---|---|---|
| Software verification | Supported | Focused M1--M3 tests and independent verifiers | Declared Python contracts and retained inputs |
| Numerical verification | Supported | Reconstruction defects and analytic M3 certificate | Frozen bounded synthetic protocols |
| Scientific validation | Not evaluated | No independent material reference | None |
| Uncertainty quantification | Not evaluated | No uncertainty model | None |
| Human acceptance | Not applicable | Tests and hashes do not authorize publication or scientific acceptance | None |

## Limitations and deviations

The historical `ksdft2effmass.campaigns.periodic_1d` surface remains migration input;
it is not precedent for coupling models, campaigns, and retained documents. The M1
name “isolated band” identifies the frozen calculation route and does not by itself
establish physical spectral isolation. Standalone verifiers avoid producer Actions but
share NumPy/SciPy, eigensolvers, floating-point behavior, and scientific conventions.
