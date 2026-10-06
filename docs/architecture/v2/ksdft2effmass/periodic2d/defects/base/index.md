# `periodic2d.defects.base`

## Purpose and status

This implemented module separates a nominal scalar-hopping defect model from its finite
represented construction and high-level representation/extraction/locality facade.

## Public contract inventory

| Symbol | Category | Responsibility |
|---|---|---|
| `Periodic2DScalarHoppingDefectModel` | Scientific model | Identified pristine scalar-hopping parent plus finite-support perturbation |
| `Periodic2DDefectRepresentationRequest` | Action request | Model, finite shape, and boundary twist |
| `Periodic2DDefectRepresentationResult` | Represented result | Separate bulk, perturbation, compatibility, and composed defect operators |
| `Periodic2DDefectRepresenter` | ActionObject | Construct compatible finite sparse representations |
| `Periodic2DDefect` | Domain facade | Explicit representation, extraction, and locality routes |

## Mathematical and state-space boundary

The module preserves

$$
H_{\mathrm{def}}=H_0+\Delta H
$$

as a composition of separately identified finite represented operators. Direct addition
requires matching finite shape, twist fiber, scalar basis, energy unit, and energy
reference. Extraction `H_def - H_0` likewise requires prior compatibility; no alignment
is inferred from shape.

## Class navigation

- [`Periodic2DScalarHoppingDefectModel`](Periodic2DScalarHoppingDefectModel/index.md)

The remaining supporting request/result/Action pages are added with their applicable
campaign or supporting-owner dossier. Their public API and equations remain documented
in the Sphinx concept page.

## Code, tests, and Sphinx

| Kind | Path or node | Responsibility |
|---|---|---|
| Code | `python/src/ksdft2effmass/periodic2d/defects/base.py` | Model and represented composition routes |
| Test | `python/tests/software_verification/ksdft2effmass/periodic2d/defects/test__Periodic2DDefect.py::TestPeriodic2DDefect` | Nominal identity, exact represented composition/extraction, potential/operator distinction, and locality response |
| Sphinx | `doc/sphinx/concepts/periodic2d-finite-extent-defects.rst` | Scientist-facing equations and claim boundaries |

## Dependencies and provenance

The module composes reusable `solid_state` finite-lattice types and the nominal
`periodic.Periodic2DDefectModel`. PhysKit-compatible reusable owners do not depend back
on this scientific model. Original local work under the repository license.

## Evidence and limitations

Software verification is supported by synthetic onsite and bond perturbations.
Numerical tests here use exact constructed matrices rather than a continuum oracle.
Scientific validation, uncertainty quantification, and human acceptance are not
evaluated. Material-specific defect inference and alignment remain outside this module.
