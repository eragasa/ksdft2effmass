# Implementation and ownership

## Import surface

Consumers import public types from their defining modules. The package initializer does
not re-export module inventories, and `ksdft2effmass.operators` does not flatten this
package.

## Data ownership

Domain, space, and representation-identity leaves are frozen, slotted dataclasses.
Identity factories are stateless slotted classes. NumPy-backed field leaves are frozen,
slotted dataclasses with private canonical storage exposed through read-only properties.

Exact nominal checks are deliberate. Complete KSD records such as `StateSpace`, `Basis`,
`Geometry`, and `EnergyReference` are composed rather than duplicated. The momentum mesh
is accepted only as the exact Numerics owner type.

## Dependency boundary

Permitted inward dependencies are:

- `ksdft2effmass.operators.records`;
- Project Koios Numerics mesh, typing, and immutable-array contracts;
- NumPy in the field implementation; and
- Python standard-library ABC, dataclass, enum, and typing facilities.

This package must not import transformations, concrete operator-family packages,
analysis, campaigns, Workflow, serializers, schemas, retained data, publications, or
formal runtime code.

## Failure behavior

`TypeError` reports wrong nominal or storage types. `ValueError` reports empty identities,
inconsistent dimensions, malformed inventories, invalid shapes, domain-cardinality
mismatch, or nonfinite values. Inputs are not silently coerced, reordered, normalized, or
repaired.

## Absent interfaces

There is no package-root facade, codec, schema, retained-result contract, certificate
export, representation graph, or identity-to-field node binding in this source tranche.
