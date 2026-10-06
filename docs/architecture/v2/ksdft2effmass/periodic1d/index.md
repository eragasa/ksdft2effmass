# `ksdft2effmass.periodic1d`

## Purpose and status

This implemented package owns canonical one-dimensional scientific-model, retention,
representation, and effective-model records extracted from historical campaign-local
owners. Phase 5 migration remains active; campaign execution and encoded documents
still live outside this package until their crosswalk rows are completed.

## Public contract

The package root deliberately exports the names in
`python/src/ksdft2effmass/periodic1d/__init__.py::__all__`. Current child owners are:

| Child module | Responsibility | Canonical page |
|---|---|---|
| `periodic1d.hopping` | Finite-hopping toy parent, immutable blocks, exact transform representations, and truncation/fit effective-model results | [Hopping models](hopping/index.md) |
| `periodic1d.model` | Fourier parent and finite plane-wave parent representation | [Fourier parent models](model/index.md) |
| `periodic1d.retention` | Parent-qualified selected-band and represented retained spaces | [One-dimensional scientific retention](retention/index.md) |
| `periodic1d.representations` | Retained-operator reciprocal and hopping bindings | [One-dimensional represented retained operators](representations/index.md) |
| `periodic1d.campaign` | Target owner for one-dimensional campaign definitions, Actions, results, and retained-evidence adapters | [Target campaign architecture](campaign/index.md); source migration remains pending rows `058–066` |

## Ownership boundary

Scientific models are separate from finite fiber matrices, retained spaces, represented
operators, and executable campaigns. A hopping coefficient container acquires exact or
approximate scientific meaning only through its construction result and identified
parent/retained operator. Complete transforms, truncation, and fitting remain distinct.

## Dependency rules

The package may depend inward on general `ksdft2effmass.periodic` contracts and reusable
solid-state numerical objects. It must not import campaign execution, encoded campaign
documents, filesystem paths, or acceptance policy.

## Code and test mapping

| Kind | Path | Responsibility |
|---|---|---|
| Package | `python/src/ksdft2effmass/periodic1d/__init__.py` | Supported one-dimensional API |
| Tests | `python/tests/software_verification/ksdft2effmass/periodic1d/` | Model, retention, representation, and public-route software evidence |
| Sphinx | `doc/sphinx/api/ksdft2effmass/periodic1d/` | User-facing public API |

## Provenance and evidence

Original local work under the repository license. Mapped unit tests establish software
behavior. Numerical verification is attached only to specific numerical Actions;
package availability does not establish scientific validation, uncertainty
quantification, or human acceptance.

## Limitations and deviations

Rows `058–066` remain pending campaign migration. Canonical module/class pages are being
added by crosswalk dossier cohort rather than by declaring untouched legacy surfaces
complete.
