# `operators.records`

## Purpose and status

This implemented module owns the general dense finite represented-operator record and
its explicit interpreting metadata. It admits finite non-Hermitian matrices and keeps
analysis, compatibility, differencing, alignment, and serialization in separate Actions.

## Public inventory

| Symbol | Category | Responsibility |
|---|---|---|
| `StateSpace` | Representation metadata | Stable finite state-space identity, kind, and positive dimension |
| `Basis` | Representation metadata | Ordered unique labels and orthonormality declaration |
| `Geometry` | Representation metadata | Finite 3D row-vector cell, boundaries, coordinates, and length unit |
| `EnergyReference` | Representation metadata | Exact textual energy-zero and unit convention |
| `OperatorRecord` | Represented operator | Immutable canonical dense matrix plus all interpreting metadata and provenance |

## Class navigation

- [`StateSpace`](StateSpace/index.md)
- [`Basis`](Basis/index.md)
- [`Geometry`](Geometry/index.md)
- [`EnergyReference`](EnergyReference/index.md)
- [`OperatorRecord`](OperatorRecord/index.md)

Source is `python/src/ksdft2effmass/operators/records.py`. The extensive class-facet
software suites under `python/tests/software_verification/ksdft2effmass/operators/`
document constructors, invariants, ownership, value semantics, compatibility, and
serialization. Sphinx API and scientist-facing concepts are in
`doc/sphinx/api/operators.rst` and `doc/sphinx/concepts/operator-records.rst`.
