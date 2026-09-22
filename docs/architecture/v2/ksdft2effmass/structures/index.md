# `ksdft2effmass.structures` namespace

The implemented `ksdft2effmass.structures` namespace owns application-local physical
structure contracts. Its initial public surface is
[`structures.periodic`](periodic.md), which represents periodic crystal geometry.

Molecular topology is outside `ksdft2effmass` scope. The selected
[structures package boundary](../structures-package-boundary-decision.md) permits an
independent DACP application to use its own `structures.molecular` and
`structures.periodic` contracts without either application importing the other.

The namespace contains no generic `Structure` base class, calculator execution,
electronic sampling, pseudopotential policy, native-format adaptation, or scientific
acceptance. New project-owned periodic structures use the canonical LAMMPS `metal`
unit inventory. Authenticated Materials Project retrieval and mutable pymatgen input
adaptation belong to `ksdft2effmass.integration.materials_project`, not this domain.

`structures.catalog` owns immutable canonical snapshot entries, scientific geometry
roles, tolerance-qualified symmetry results, stable entry serialization, and a domain
repository over the existing opaque atomic revision store. It owns no SQL schema,
credential, remote query, or scientific acceptance policy. The configured mutable
SQLite catalog remains outside Git; compact credential-free manifests remain under
`calculations/**`.
