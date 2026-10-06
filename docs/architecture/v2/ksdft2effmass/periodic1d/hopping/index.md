# `periodic1d.hopping`

## Purpose and status

This implemented module owns the finite-hopping 1D toy parent, its immutable directed
block data, and typed construction results that distinguish complete operator
representations from truncation- and fit-derived effective models.

## Public contract inventory

| Symbol | Category | Responsibility |
|---|---|---|
| `Periodic1DHoppingBlock` | Supporting representation data | One directed matrix coefficient at an integer cell displacement |
| `Periodic1DFiniteHoppingToyModel` | Scientific model | Parent-qualified configured finite Hermitian hopping family |
| `Periodic1DCompleteHoppingRepresentationResult` | Represented operator result | Complete finite-mesh Fourier route bound to an exact retained operator |
| `Periodic1DTruncatedHoppingEffectiveModelResult` | Effective-model result | Explicit finite-range truncation route |
| `Periodic1DFittedHoppingEffectiveModelResult` | Effective-model result | Explicit weighted fitting route |

All are supported through `ksdft2effmass.periodic1d`. Row 011 owns the first two
contracts; row 014 owns the exact/effective route distinction for the result classes.

## Scientific and numerical boundary

A block tuple represents directed coefficients `H_R`. The configured toy parent requires
`H_R = H_{-R}^dagger` under one declared absolute tolerance. The model does not identify
a particular Bloch fiber or supercell matrix. Complete Fourier transformation is a
representation route; discarding blocks or estimating them by fitting constructs an
approximation and therefore a different result type.

## Invariants and failure behavior

Blocks own nonempty square finite `complex128` matrices in immutable C-order storage.
The model requires exact nonempty identity and unit strings, a nonempty exact tuple,
sorted unique contiguous displacements containing zero, one common orbital dimension,
and pairwise Hermiticity. Boolean and string arrays are rejected rather than coerced.

## Class navigation

- [`Periodic1DHoppingBlock`](Periodic1DHoppingBlock/index.md)
- [`Periodic1DFiniteHoppingToyModel`](Periodic1DFiniteHoppingToyModel/index.md)
- [`Periodic1DCompleteHoppingRepresentationResult`](Periodic1DCompleteHoppingRepresentationResult/index.md)
- [`Periodic1DTruncatedHoppingEffectiveModelResult`](Periodic1DTruncatedHoppingEffectiveModelResult/index.md)
- [`Periodic1DFittedHoppingEffectiveModelResult`](Periodic1DFittedHoppingEffectiveModelResult/index.md)

## Code, tests, and Sphinx

| Kind | Path or node | Responsibility |
|---|---|---|
| Code | `python/src/ksdft2effmass/periodic1d/hopping.py` | Defining module |
| Test | `python/tests/software_verification/ksdft2effmass/periodic1d/test__Periodic1DFiniteHoppingToyModel.py::TestPeriodic1DFiniteHoppingToyModel` | Parent identity, block storage, exact scalar boundaries, Hermiticity, and retired routes |
| Sphinx | `doc/sphinx/api/ksdft2effmass/periodic1d/hopping.rst` | Public equations, invariants, and route distinctions |

## Provenance and evidence

Original local work under the repository license. Synthetic tests provide software
verification of row 011. They do not establish a material Hamiltonian, numerical
convergence, scientific validation, uncertainty quantification, or acceptance.

## Limitations

The textual energy unit is retained exactly but not interpreted or converted here.
Primitive-fiber and supercell construction remain separate numerical owners.
