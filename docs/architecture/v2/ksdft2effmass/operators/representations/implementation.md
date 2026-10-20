# Implementation

## Package boundary

Source owner: `python/src/ksdft2effmass/operators/representations/`.

The initializer is documentation-only. Every provisional contract is imported from its
defining module. Neither `ksdft2effmass.operators.representations` nor
`ksdft2effmass.operators` flattens module inventories through re-export.

## Implemented modules

| Module | Responsibility |
|---|---|
| `domains.py` | domain ABC, sample-role enum, momentum mesh composition, translation inventory |
| `spaces.py` | represented-space metadata composition |
| `identities.py` | carrier-local role enums, node identity, and node-identity factory |
| `fields.py` | matrix-field ABC hierarchy and immutable NumPy leaves |

`nodes.py` is reserved for future generic representation nodes and is not implemented.
Transformation enums, edge identities, and request/result/Action ABCs belong to the
sibling `operators.transformations` package.

## Dependency direction

Permitted dependencies are `operators.records`, Project Koios Numerics, NumPy within the
concrete field module, and Python standard-library contracts. This package must not import
`operators.transformations`, a concrete operator-family package, analysis, campaigns,
Workflow, serializers, schemas, retained data, publications, or formal runtime code.

The sibling transformation package may depend on representations. Concrete operator
families may consume both generic packages. Campaigns remain responsible for mesh/case,
threshold, provenance, and retained-evidence policy.

## DataObject implementation

Domain, space, and identity leaves are frozen, slotted dataclasses with intrinsic
validation. NumPy field leaves retain private owned storage. Construction validates exact
domain and dtype, finite three-axis arrays, first-axis/domain correlation, positive matrix
dimensions, and squareness where required. Dimensions are derived rather than accepted as
parallel inputs.

## Failure and compatibility boundary

`TypeError` reports wrong exact nominal or storage types. `ValueError` reports invalid
values, inconsistent dimensions, shapes, nonfinite arrays, duplicate translations, or
domain-cardinality mismatches. Inputs are not repaired, reordered, normalized, or
silently coerced.

There is no Phase 1 codec, schema, retained-result binding, or formal certificate export.
Existing public imports and schema-v1 bytes are unchanged; no compatibility facade is
provided for the discarded provisional singular package path.

## Test mapping

| Test area | Contract established |
|---|---|
| domain tests | mesh composition, roles, translation order, and exact types |
| space tests | metadata composition and basis/space dimension |
| identity tests | carrier-role agreement, derived identity fields, and factory behavior |
| field tests | interfaces, shape, domain, dtype, finiteness, and array ownership |
| dependency-boundary test | `transformations -> representations`, no reverse edge, and no flattened exports |

Passing these tests is software verification only.
