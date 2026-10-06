# `PeriodicModel`

## Purpose and status

`PeriodicModel` is the implemented nominal abstract root for periodic scientific
models. It provides category membership only and deliberately owns no representation or
execution behavior.

## Public contract

Supported import: `from ksdft2effmass.periodic import PeriodicModel`.

Concrete subclasses provide read-only properties:

- `model_id: str` — stable nonempty identity owned and validated by the concrete model;
- `model_role: PeriodicModelRole` — exact toy or material-reference role; and
- `spatial_dimension: Literal[1, 2, 3]` — normally enforced by a nominal dimension
  branch.

The root cannot be instantiated while these abstract properties are absent.

## Scientific boundary

Membership says that an object identifies a modeled periodic system. It does not make
the object a Hamiltonian, retained subspace, exact retained operator, represented
matrix, effective model, encoded document, or campaign. Those objects require explicit
parentage and construction routes.

## Invariants and failures

The abstract contract is enforced by Python's abstract-base machinery. Exact identity
validation belongs to concrete models because the abstract class stores no data. The
catalog separately rejects root-only objects whose reported dimension is not supported
by nominal dimension-branch membership.

## Dependencies and flow

Dimension-specific model bases inherit this root. Retention records refer to stable
parent identities rather than embedding arbitrary `PeriodicModel` instances. Campaigns
may consume concrete models, but this class imports no campaign policy.

## Code and test mapping

| Kind | Path or node | Established responsibility |
|---|---|---|
| Code | `python/src/ksdft2effmass/periodic/model.py:PeriodicModel` | Abstract nominal model root |
| Test | `python/tests/software_verification/ksdft2effmass/periodic/test__PeriodicModel.py::TestPeriodicModel::test_constructor__abstract_contract__requires_identity_and_role` | Missing identity and role prevent instantiation |
| Test | `python/tests/software_verification/ksdft2effmass/periodic/test__PeriodicModel.py::TestPeriodicModel::test_inheritance__dimensions__uses_nominal_branches` | Dimension branches retain root membership |

## Sphinx mapping

`doc/sphinx/api/ksdft2effmass/periodic/model.rst` documents the public route.

## Provenance and evidence

Original local work under the repository license. Software verification supports the
nominal contract. The class performs no numerical calculation; scientific validation,
uncertainty quantification, and human acceptance are not established.

## Limitations

The class is intentionally not a generic evaluator, serializer, registry entry,
structural protocol, or campaign base.
