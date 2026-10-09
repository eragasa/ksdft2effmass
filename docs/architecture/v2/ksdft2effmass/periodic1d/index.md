# `ksdft2effmass.periodic1d`

## Purpose and status

This implemented package owns canonical one-dimensional scientific-model, retention,
representation, effective-model, and canonical campaign records extracted from
historical campaign-local owners. Phase 5 migration remains active: rows 030--032 and
058--066 now have canonical owners here; later periodic-2D campaign rows remain
separate migration work.

## Public contract

The package root deliberately exports the names in
`python/src/ksdft2effmass/periodic1d/__init__.py::__all__`. Current child owners are:

| Child module | Responsibility | Canonical page |
|---|---|---|
| `periodic1d.fibers` | Shared parent-qualified finite-fiber request | [Fiber requests](fibers/index.md) |
| `periodic1d.finite_differences` | Half-open grids and twisted sparse represented fibers | [Finite-difference fibers](finite_differences/index.md) |
| `periodic1d.hopping` | Finite-hopping toy parent, immutable blocks, exact transform representations, and truncation/fit effective-model results | [Hopping models](hopping/index.md) |
| `periodic1d.model` | Fourier parent and finite plane-wave parent representation | [Fourier parent models](model/index.md) |
| `periodic1d.plane_waves` | Ordered finite plane-wave represented fibers | [Plane-wave fibers](plane_waves/index.md) |
| `periodic1d.retention` | Parent-qualified selected-band and represented retained spaces | [One-dimensional scientific retention](retention/index.md) |
| `periodic1d.representations` | Retained-operator reciprocal and hopping bindings | [One-dimensional represented retained operators](representations/index.md) |
| `periodic1d.supercell_operators` | Explicit metadata adaptation to general dense represented-operator records | [Supercell operators](supercell_operators/index.md) |
| `periodic1d.campaign` | Canonical owner for migrated one-dimensional campaign definitions, Actions, results, and retained-evidence adapters | [Campaign architecture](campaign/index.md); rows `058–066` are implemented |

## Ownership boundary

Scientific models are separate from finite fiber matrices, retained spaces, represented
operators, and executable campaigns. A hopping coefficient container acquires exact or
approximate scientific meaning only through its construction result and identified
parent/retained operator. Complete transforms, truncation, and fitting remain distinct.

## Dependency rules

Scientific-model, retention, and representation modules may depend inward on general
`ksdft2effmass.periodic` contracts and reusable solid-state numerical objects. They
must not import campaign execution, encoded campaign documents, filesystem paths, or
acceptance policy. The separate `periodic1d.campaign` child may compose those scientific
owners but not reverse that dependency.

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

Historical row-030 artifacts without explicit cell vectors, exact ordered state labels,
and structured provenance remain unmigrated; the canonical constructor does not infer
those values.
Canonical module/class pages are added by crosswalk dossier cohort rather than by
declaring untouched legacy surfaces complete.
