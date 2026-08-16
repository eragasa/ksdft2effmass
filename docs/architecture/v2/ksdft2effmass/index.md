# `ksdft2effmass` prospective package architecture

Architecture v2 is organized by the selected prospective Python namespace. This
layout documents package ownership without claiming that the packages are
implemented or authorizing a source move.

## Package map

```mermaid
flowchart TB
    app["application"]
    persistence["persistence"]
    harness["harness"]
    workflows["workflows"]
    petrinet["petrinet.colored"]
    campaigns["campaigns"]
    calculators["calculators"]
    integration["integration.quantumespresso"]
    periodic["periodic"]
    ksdft["ksdft"]
    analysis["analysis"]

    app --> persistence
    app --> harness
    app --> workflows
    app --> campaigns
    app --> calculators
    app --> integration
    app --> analysis
    harness --> persistence
    workflows --> persistence
    workflows --> petrinet
    campaigns --> workflows
    calculators --> workflows
    calculators --> periodic
    calculators --> ksdft
    integration --> calculators
    integration --> workflows
    integration --> periodic
    integration --> ksdft
    analysis --> workflows
    analysis --> periodic
    analysis --> ksdft
```

The reverse `petrinet.colored → workflows` dependency is forbidden.

## Package ownership

| Prospective package | Architecture page | Responsibility |
|---|---|---|
| `ksdft2effmass.application` | [Application](application/index.md) | Explicit composition root |
| `ksdft2effmass.persistence` | [Persistence](persistence/index.md) | Domain-neutral immutable revision storage |
| `ksdft2effmass.harness` | [Harness](harness/index.md) | Development-harness contracts and control |
| `ksdft2effmass.workflows` | [Workflows](workflows/index.md) | Scientific Task, Workflow, run, and control contracts |
| `ksdft2effmass.petrinet.colored` | [Colored Petri net](petrinet/colored/index.md) | Generic deterministic CPN values and pure operations |
| `ksdft2effmass.campaigns` | [Campaigns](campaigns/index.md) | Project-specific composition definitions |
| `ksdft2effmass.calculators` | [Calculators](calculators/index.md) | Calculator-facing simulation contracts |
| `ksdft2effmass.integration.quantumespresso` | [Quantum ESPRESSO integration](integration/quantumespresso/index.md) | Concrete QE anti-corruption actions |
| `ksdft2effmass.periodic` | [Periodic](periodic/index.md) | Neutral periodic geometry semantics |
| `ksdft2effmass.ksdft` | [Kohn–Sham DFT](ksdft/index.md) | Representation-neutral Kohn–Sham semantics |
| `ksdft2effmass.analysis` | [Analysis](analysis/index.md) | Deterministic scientific analysis |

## Documentation boundary

Package-wide diagrams and discussions live on the nearest package `index.md`;
the [`petrinet` namespace page](petrinet/index.md) provides the parent boundary
for the selected `petrinet.colored` subpackage.
Topic pages below a package remain package-level architecture unless the owning
architecture explicitly selects an internal module. Architecture v2 currently
defers exact internal submodules and public wire exports, so documentation
filenames must not be interpreted as approved source modules.

Repository-wide principles, human-decision semantics, identity contracts,
dependency direction, issues, and cross-domain separation remain at the
[Architecture v2 root](../index.md).
