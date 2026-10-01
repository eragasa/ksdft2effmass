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
acceptance.
