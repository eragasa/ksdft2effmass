# `periodic2d.defects`

## Purpose and status

This implemented subpackage owns controlled finite-extent defects of identified
periodic-2D parents, their finite represented composition and extraction Actions, and
locality diagnostics. It does not infer a defect operator from equal matrix dimensions
or claim material validation.

## Public child map

| Module | Responsibility | Canonical page |
|---|---|---|
| `defects.base` | Scalar-hopping defect model, finite representation request/result, representer, and facade | [Base defect contracts](base/index.md) |
| `defects.extraction` | Compatibility-gated represented subtraction | Current Sphinx concept; canonical page pending supporting-owner audit |
| `defects.locality` | Partition-resolved finite-extent analysis | Current Sphinx concept; canonical page pending supporting-owner audit |

## Ownership boundary

The scientific model keeps pristine bulk identity and finite-support perturbation
separate. A finite representation additionally requires explicit lattice shape and
boundary twist. Compatibility of basis, geometry, unit, and energy reference precedes
composition or subtraction. Locality is measured from a represented difference rather
than inferred from a class name.

## Code, tests, and Sphinx

| Kind | Path | Responsibility |
|---|---|---|
| Package | `python/src/ksdft2effmass/periodic2d/defects/__init__.py` | Deliberate public exports |
| Tests | `python/tests/software_verification/ksdft2effmass/periodic2d/defects/` | Model, representation, extraction, and locality software evidence |
| Sphinx | `doc/sphinx/concepts/periodic2d-finite-extent-defects.rst` | Equations, data flow, test interpretation, and exclusions |

## Provenance and evidence

Original local work under the repository license. Synthetic tests establish represented
software behavior. They do not establish continuum convergence, a material defect,
scientific validation, uncertainty quantification, or acceptance.

## Limitations

No authenticated DFT or Wannier90 defect source is consumed by this subpackage. Basis,
gauge, geometry, and energy-reference alignment must already be explicit.
