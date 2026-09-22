# Structures package boundary decision

## Status and authority

The human responses `recommendation authorized` and `activation authorized` selected
and activated the application-local structures architecture for
`migration.v2.periodic`. The later response `Authorize managed administrative closeout
of migration.v2.periodic` human-accepted and administratively closed its bounded
implementation. This decision governs package ownership and migration; it did not itself authorize
dependency changes, protected execution, scientific acceptance, automatic succession,
release, or publication. The later human response `recommendation authorized yes
through MPRester`, preserved at
`.pi/checkpoints/bulk-silicon-pymatgen-mprester-integration.json`, separately
authorizes the bounded pymatgen/mp-api input integration and canonical metal-unit
structure adaptation. It does not authorize scientific calculations or replacement
of the production PBE-relaxed lattice convention.

## Selected architecture

`ksdft2effmass` and `dacp2transport` retain independent application-owned structure
contracts. Neither application imports the other, and no shared Project Koios
structure package is introduced before semantically equivalent implemented use is
demonstrated in both applications.

Molecular topology and periodic boundary geometry are orthogonal concepts. A future
molecular configuration may compose with an optional periodic cell; molecular and
periodic records do not inherit from one generic `Structure` base class.

The selected `ksdft2effmass` ownership is:

```text
ksdft2effmass.structures.periodic
    direct and reciprocal lattices
    periodic sites and structures
    structure-owned species identity

ksdft2effmass.electronic_structure.sampling
    k-point sampling and weight normalization

ksdft2effmass.calculators.dft.pw
    plane-wave pseudopotential assignments
```

The prospective independent DACP ownership is:

```text
dacp2transport.structures.molecular
    molecular topology, configurations, conformers, and torsional coordinates

dacp2transport.structures.periodic
    optional periodic-cell boundary contracts
```

This repository does not define or implement the DACP contracts.

## Migration and compatibility

The existing `ksdft2effmass.periodic` public import remains only as a bounded
compatibility surface while current consumers migrate to their owning packages. It
must not acquire new behavior or become a second source of class definitions.

Moving a name does not authorize a change in geometry, coordinate, reciprocal-scale,
unit, ordering, tolerance, or compatibility meaning. Pseudopotential labels must not
remain intrinsic reusable structure semantics: any compatibility field retained during
migration is transitional until the plane-wave assignment owner is implemented and
all consumers migrate.

Private represented band observations belong to analysis rather than structures.
Their relocation changes no public API and does not establish alignment, numerical
verification, or scientific validation.

## Deferred decisions

A shared structure package, cross-application serialization contract, universal
chemical-species identity, and stable DACP molecular API remain deferred. Each
requires implemented evidence and separate public-contract and dependency authority.
