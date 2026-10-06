# `PeriodicModelRole`

## Purpose and status

`PeriodicModelRole` is the implemented closed enum that distinguishes controlled toy
models from explicitly specified material-reference models. It is classification
metadata, not a scientific-validation status.

## Public contract

Supported import: `from ksdft2effmass.periodic import PeriodicModelRole`.

| Member | Serialized value | Meaning |
|---|---|---|
| `TOY` | `"toy"` | Controlled model used to study mathematical, numerical, or software behavior |
| `MATERIAL_REFERENCE` | `"material_reference"` | Model intended to represent an explicitly specified material |

Callers requiring this contract use exact enum members rather than coercible strings.

## State, identity, and invariants

The two values are stable role identities. Neither member supplies dimensionality,
model identity, parentage, an operator, representation metadata, provenance, or
acceptance policy. `MATERIAL_REFERENCE` does not imply physical completeness,
convergence, scientific validation, or human acceptance.

## Dependencies and flow

`PeriodicModel` exposes the role. `PeriodicToyModelCatalog` accepts only exact `TOY`
members. Concrete model owners decide and document the applicable role; campaigns do
not mutate it.

## Code and test mapping

| Kind | Path or node | Established responsibility |
|---|---|---|
| Code | `python/src/ksdft2effmass/periodic/model.py:PeriodicModelRole` | Closed role enum |
| Test | `python/tests/software_verification/ksdft2effmass/periodic/test__PeriodicModel.py::TestPeriodicModel` | Concrete nominal models return exact roles |
| Test | `python/tests/software_verification/ksdft2effmass/periodic/test__PeriodicToyModelCatalog.py::TestPeriodicToyModelCatalog::test_constructor__model_role__requires_exact_enum_type` | Role strings cannot substitute for enum members |

## Sphinx mapping

`doc/sphinx/api/ksdft2effmass/periodic/model.rst` documents the supported route and the
material-reference claim boundary.

## Provenance and evidence

Original local work under the repository license. Software verification supports exact
enum use. Numerical verification is not applicable; scientific validation, uncertainty
quantification, and human acceptance are not established.

## Limitations

This enum intentionally does not encode validation, maturity, or campaign status.
