# `Periodic1DSupercellOperatorMetadata`

**Defined in:** `ksdft2effmass.periodic1d.supercell_operators`

## Role

Immutable complete interpreting metadata for a represented dense supercell operator.
It carries state-space and basis identities, exact ordered labels, explicit embedded
cell vectors, geometry conventions, energy reference/unit, and structured provenance.

## Invariants

Exact tuple containers are required for labels and cell rows. Canonical `StateSpace`,
`Basis`, `Geometry`, and `EnergyReference` owners validate nonempty identities, unique
labels, finite linearly independent cell vectors, and exact conventions. No metadata is
inferred from a future matrix.

## Evidence

`test__Periodic1DSupercellOperatorMetadata.py` checks complete explicit construction
and rejection of erased label containers.
