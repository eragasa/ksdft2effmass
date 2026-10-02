# `ksdft2effmass.structures.periodic` package

The implemented `ksdft2effmass.structures.periodic` package owns backend-neutral
periodic crystal geometry consumed by calculators, integrations, Kohn--Sham records,
and analysis. The selected
[structures package boundary](../structures-package-boundary-decision.md) keeps this
application owner independent of prospective DACP molecular contracts.

```mermaid
flowchart LR
    calculators["ksdft2effmass.calculators"] --> structures["structures.periodic"]
    integration["integration.quantum_espresso"] --> structures
    ksdft["ksdft2effmass.ksdft"] --> structures
    analysis["ksdft2effmass.analysis"] --> structures
    integration --> sampling["electronic_structure.sampling"]
    ksdft --> sampling
    structures -. forbidden .-> calculator_specific["calculator or integration packages"]
```

The structure owner contains direct and reciprocal lattices, ordered species and
sites, explicit units and coordinate conventions, periodic structures, and the
validator for $A B^T = 2\pi I$. Electronic $k$-point sampling is implemented by
`ksdft2effmass.electronic_structure.sampling`, not by the structure owner.

The `ksdft2effmass.periodic` source package now owns the nominal scientific-model
hierarchy while retaining temporary compatibility imports for the former geometry and
sampling inventory. The accepted
[general periodic-model architecture](../periodic/index.md) governs that model
identity. Crystal geometry remains owned here; periodic scientific models must consume
rather than duplicate it.
Existing schema-version-1 plane-wave compatibility retains a pseudopotential source
label on `AtomicSpecies`; the label is transitional and is not reusable structure
meaning. Moving it to a plane-wave assignment owner requires the separately authorized
aggregate compatibility migration.

The packages do not own calculator invocation, native formats, workflow control,
comparison policy, molecular topology, or scientific acceptance. Private represented
band observations remain outside the new structure owner.
