# Symmetry

## Status and placement

**Documentation-first incubation design; no executable package or supported import is
claimed by these pages.** The selected incubation namespace is
`ksdft2effmass.symmetry`, with prospective source at
`python/src/ksdft2effmass/symmetry/`. The intended later owner is
`projectkoios.physkit.solidstate.symmetry`. Migration requires separate review; this
is not authorization to change dependencies, relocate existing code, or publish an API.

The goal is reusable solid-state symmetry mathematics, not a silicon-only collection
of operations or a new native-data integration framework. Generality comes from explicit
operation, space, basis, metric and representation contracts, not from assuming every
physical symmetry admits the same finite matrix representation.

## Pages

- [Schematics](schematics.md): objects, ownership and data flow.
- [Numerics](numerics.md): prospective mathematical contracts and verification checks.
- [Science](science.md): interpretation, applicability and scientific limitations.

## Ownership boundary

| Owner | Responsibility |
|---|---|
| Incubating `ksdft2effmass.symmetry` | Declared operations/groups, metric-aware actions and representations, closure/leakage, intertwiners, and qualified sector analysis |
| PhysKit | Existing lattice/quantity/matrix primitives; intended eventual home of the reusable symmetry core |
| Simulations | Native QE/Wannier decoding and backend-specific extraction of symmetry-action data, including required metric and phase conventions |
| KSD calculation/campaign | Scientific source associations, admission, uncertainty assumptions, thresholds, CSD dispositions and successor decisions |

The installed PhysKit already supplies integral lattice-operation primitives under
`projectkoios.physkit.periodic.lattice.symmetry`; reuse admitted primitives rather than
copying them into this namespace. Existing local lattice capabilities are not migrated
or removed by this design.

The existing [sewing package](../sewing/index.md) owns reciprocal-endpoint contracts and
reserves `SymmetrySewing` as a distinct abstract category. Preserve that category and its
unitary/antiunitary distinction. This design does not move its source, change existing
sewing values, or approve a concrete executable signature. Symmetry-action mathematics
and its consumption by sewing must be reconciled explicitly before implementation.

## Staged implementation scope

1. Define explicit finite-group and complex-linear, metric-preserving action contracts;
   test composition, identities, metrics and domain/codomain compatibility.
2. Diagnose whether supplied subspaces are invariant; distinguish leakage, compression
   and genuine induced representations. Add operator-covariance/intertwiner checks.
3. Support ordinary finite-group isotypic projectors only with qualified representation
   and irreducible-character data.
4. Extend deliberately to reciprocal-space sewing, nonsymmorphic/projective or double-
   valued representations, and antiunitary actions/corepresentations. These distinctions
   belong in the design now, but are not implemented capabilities of the initial slice.

Use synthetic analytical examples first, including nonorthogonal bases and deliberately
non-invariant subspaces. Silicon CSD2 is an intended consumer and integration case, not
an implicit definition of the core or a reason to hard-code Gamma, ten orbitals, twenty
bands, a particular pseudopotential, or a campaign threshold.

## Migration criteria

Before migration, identify actual consumers and public imports; separate reusable
mathematics from KSD policy/native adapters; retain operationally immutable values,
explicit numeric contracts, tests and documentation; and review the dependency direction.
PhysKit must not depend on KSD. Update callers deliberately rather than maintain aliases
or dual implementations. Do not invent registries, a universal symmetry result, group
catalog services or parallel array/serialization infrastructure in anticipation of reuse.
