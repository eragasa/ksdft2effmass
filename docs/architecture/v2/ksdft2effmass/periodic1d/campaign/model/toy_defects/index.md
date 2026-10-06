# `periodic1d.campaign.model.toy_defects` target mapping

## Purpose and status

This transitional subpackage owns controlled operation and perturbation definitions
used by one-dimensional defect studies. Row 018 has corrected basis scrambling from a
misleading scientific-model name to an explicit operation definition.

## Child map

| Module | Responsibility | Canonical page |
|---|---|---|
| `alignment` | Site, orbital, phase, and spin basis-scrambling definition, request, result, and constructor | [Basis scrambling](alignment/index.md) |

Other toy-defect modules retain their current owners until the applicable scientific or
campaign rows are audited.

## Boundary

A basis-scrambling definition specifies a controlled unitary coordinate transformation.
It does not identify a physical model, parent operator, retained space, energy shift,
provenance source, or acceptance policy.

## Code and evidence

| Kind | Path | Responsibility |
|---|---|---|
| Package | `python/src/ksdft2effmass/campaigns/periodic_1d/model/toy_defects/__init__.py` | Deliberate public supporting definitions |
| Tests | `python/tests/ksdft2effmass/campaigns/periodic_1d/model/toy_defects/` | Controlled numerical-map evidence |
| Sphinx | `doc/sphinx/api/research-monograph-campaigns.rst` | Current public campaign/support API |

Original local work under the repository license. Synthetic unitary tests are bounded
software/numerical evidence, not physical basis identification.
