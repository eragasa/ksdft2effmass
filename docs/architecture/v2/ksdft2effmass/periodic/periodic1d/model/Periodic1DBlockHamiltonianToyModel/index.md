# `Periodic1DBlockHamiltonianToyModel`

## Purpose

Immutable scientific definition of the finite-range matrix-valued parent used by M2.

## Contract

The model binds a nonempty identity, a `BlockHoppingModel1D`, and an energy-valued
Hermiticity tolerance. Every representative $R$ must have an opposite representative
$-R$ and satisfy

$$
\lVert T_R-T_{-R}^{\dagger}\rVert_F\leq\varepsilon_H
$$

after converting the tolerance to the hopping-block energy unit.

## State space and units

Each block acts on the same finite internal cell space declared by the hopping model.
The model does not select a retained band group or a frame. All blocks and the tolerance
carry compatible energy dimensions.

## Invariants and failures

Construction raises `TypeError` for wrong exact boundary types and `ValueError` for an
empty identity, negative/incompatible tolerance, a missing opposite block, or a defect
above tolerance.

## Mapping

- Source: `python/src/ksdft2effmass/periodic1d/model.py`
- Sphinx: `doc/sphinx/api/ksdft2effmass/periodic1d/model.rst`
- Main consumer: `Periodic1DMultibandAlignmentCalculationDefinition`

## Evidence and limitations

M2 tests exercise exact parent correlation and Hermiticity. The class is a synthetic
parent definition, not a retained-space selector, material Hamiltonian, or validation
result.
