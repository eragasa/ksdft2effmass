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
    qe_integration["integration.quantum_espresso"]
    wannier90_integration["integration.wannier90"]
    lammps_integration["integration.lammps<br/>(prospective)"]
    structures["structures.periodic"]
    sampling["electronic_structure.sampling"]
    ksdft["ksdft"]
    operators["operators"]
    analysis["analysis"]
    pi_agents["pi.agents"]

    pi_agents --> app
    app --> persistence
    app --> harness
    app --> workflows
    app --> campaigns
    app --> calculators
    app --> qe_integration
    app --> wannier90_integration
    app --> lammps_integration
    app --> analysis
    harness --> persistence
    workflows --> persistence
    workflows --> petrinet
    campaigns --> workflows
    campaigns --> calculators
    campaigns --> analysis
    calculators --> workflows
    calculators --> structures
    calculators --> ksdft
    qe_integration --> calculators
    qe_integration --> workflows
    qe_integration --> structures
    qe_integration --> sampling
    qe_integration --> ksdft
    wannier90_integration --> operators
    lammps_integration --> calculators
    lammps_integration --> workflows
    lammps_integration --> structures
    analysis --> workflows
    analysis --> structures
    analysis --> ksdft
    ksdft --> sampling
    analysis --> operators
```

The reverse `petrinet.colored → workflows` dependency is forbidden.

## Package ownership

| Prospective package | Architecture page | Responsibility |
|---|---|---|
| `ksdft2effmass.application` | [Application](application/index.md) | Explicit composition root |
| `ksdft2effmass.persistence` | [Persistence](persistence/index.md) | Domain-neutral immutable revision storage |
| `ksdft2effmass.serialization` | [Serialization](serialization/index.md) | Type-preserving abstract JSON wire contracts |
| `ksdft2effmass.harness` | [Harness](harness/index.md) | Development-harness contracts and control |
| `ksdft2effmass.workflows` | [Workflows](workflows/index.md) | Scientific Task, Workflow, run, and control contracts |
| `ksdft2effmass.petrinet.colored` | [Colored Petri net](petrinet/colored/index.md) | Generic deterministic CPN values and pure operations |
| `ksdft2effmass.campaigns` | [Campaigns](campaigns/index.md) | Project-specific QoI-study and Workflow composition definitions |
| `ksdft2effmass.calculators` | [Calculators](calculators/index.md) | Shared plane-wave specification and calculator-facing simulation contracts |
| `ksdft2effmass.integration.quantum_espresso` | [Quantum ESPRESSO integration](integration/quantum_espresso/index.md) | Canonical QE-native contracts, loose grouped `pw.x` input writing, QEXSD parsing, diagnostics, and concrete anti-corruption actions |
| `ksdft2effmass.integration.wannier90` | [Wannier90 integration](integration/wannier90/index.md) | Execution-independent typed adaptation of retained native Wannier90 gauge matrices, Hamiltonian blocks, and final localization observations |
| `ksdft2effmass.integration.lammps` (prospective) | [QoI-first LAMMPS integration](qoi-first-lammps-integration.md) | LAMMPS-native contracts and adapters defined only after calculator-independent QoI and atomistic requirements; no Simulation Task is implemented |
| `ksdft2effmass.structures` | [Structures](structures/index.md) | Application-owned physical structure namespace |
| `ksdft2effmass.structures.periodic` | [Periodic structures](structures/periodic.md) | Neutral periodic crystal geometry semantics |
| `ksdft2effmass.electronic_structure` | [Periodic structures and sampling](structures/periodic.md) | Electronic reciprocal-space sampling semantics |
| `ksdft2effmass.periodic` | [Compatibility package](periodic/index.md) | Temporary re-export of the former public periodic inventory |
| `ksdft2effmass.ksdft` | [Kohn–Sham DFT](ksdft/index.md) | Representation-neutral Kohn–Sham semantics |
| `ksdft2effmass.operators` | [Represented operators](operators/index.md) | Finite represented-operator records, serialization, exact compatibility, and narrowly fixed-representation operations |
| `ksdft2effmass.analysis` | [Analysis](analysis/index.md) | Higher-level deterministic scientific analysis |
| `ksdft2effmass.pi.agents` | [Pi agents](pi/agents/index.md) | Outer deterministic Pi request/result adapter |

No additional shared `contracts` package sits beneath these owners. Cross-package
identity/version/failure semantics are defined at the architecture root, while each
listed package owns its nominal runtime values and outward consumers own explicit
boundary adaptation.

## Extraction records

- [Appendix G periodic-1D capability extraction inventory](periodic-1d-capability-extraction-inventory.md)
- [Periodic native-evidence presence audit](periodic-native-evidence-presence-audit.md)
- [Sparse and nonuniform Fourier-transform technology review](sparse-fourier-transform-technology-review.md)
- [Research-monograph software-extraction audit](research-monograph-software-extraction-audit.md)

```{toctree}
:hidden:

periodic-1d-capability-extraction-inventory
periodic-native-evidence-presence-audit
sparse-fourier-transform-technology-review
research-monograph-software-extraction-audit
integration/wannier90/index
serialization/index
```

## Documentation boundary

Package-wide diagrams and discussions live on the nearest package `index.md`;
the [`petrinet` namespace page](petrinet/index.md) provides the parent boundary
for the selected `petrinet.colored` subpackage. The [`pi` namespace
page](pi/index.md) provides the outer integration boundary for the selected
`pi.agents` subpackage.
Topic pages below a package remain package-level architecture unless the owning
architecture explicitly selects an internal module. Architecture v2 currently
defers exact internal submodules and public wire exports, so documentation
filenames must not be interpreted as approved source modules.

Repository-wide principles, human-decision semantics, identity contracts,
dependency direction, issues, and cross-domain separation remain at the
[Architecture v2 root](../index.md).
