# `periodic2d.model`

## Purpose and status

This implemented subpackage owns controlled two-dimensional scientific toy models and
representation-specific definitions demonstrated by periodic2d studies. It does not own
campaign execution or promote finite matrices into scientific parents.

## Public child map

| Child | Responsibility | Canonical page |
|---|---|---|
| `periodic2d.model.toy_models` | Controlled toy parents and their finite representation requests, results, and constructors | [Toy models](toy_models/index.md) |

## Ownership boundary

A scientific parent specifies the modeled system and conventions. Plane-wave bases,
coordinate grids, finite requests, represented matrices, and constructors remain
separate supporting or represented objects. Equal dimensions or shared model fields do
not erase those distinctions.

## Code, tests, and Sphinx

| Kind | Path | Responsibility |
|---|---|---|
| Package | `python/src/ksdft2effmass/periodic2d/model/__init__.py` | Controlled-model namespace |
| Tests | `python/tests/ksdft2effmass/periodic2d/model/` | Model and representation behavior |
| Sphinx | `doc/sphinx/concepts/periodic2d-controlled-reduction.rst` | Scientist-facing model/representation separation |

## Provenance and evidence

Original local work under the repository license. Tests provide software or explicitly
classified numerical evidence for individual owners. Package presence does not establish
scientific validation, uncertainty quantification, or acceptance.

## Limitations

Only demonstrated controlled toy models belong here. Graphene material-reference
physics remains absent pending an authoritative specification.
