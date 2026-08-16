# Architecture v2

Architecture v2 is the normative prospective architecture for deterministic scientific operations and their supporting development lifecycle. Architecture v1 remains implemented; the migration page alone owns cross-version status. Package-owned pages follow the [prospective `ksdft2effmass` namespace](ksdft2effmass/index.md); repository-wide contracts and live issues remain at this root.

## System overview

```mermaid
flowchart TB
    application["ksdft2effmass.application"]
    persistence["ksdft2effmass.persistence"]
    harness["ksdft2effmass.harness"]
    workflows["ksdft2effmass.workflows"]
    petrinet["ksdft2effmass.petrinet.colored"]
    campaigns["ksdft2effmass.campaigns"]
    calculators["ksdft2effmass.calculators"]
    integration["ksdft2effmass.integration.quantumespresso"]
    periodic["ksdft2effmass.periodic"]
    ksdft["ksdft2effmass.ksdft"]
    analysis["ksdft2effmass.analysis"]

    application --> persistence
    application --> harness
    application --> workflows
    harness --> persistence
    workflows --> persistence
    application --> campaigns
    application --> calculators
    application --> integration
    application --> analysis
    campaigns --> workflows
    calculators --> workflows
    workflows --> petrinet
    integration --> calculators
    integration --> workflows
    integration --> periodic
    integration --> ksdft
    calculators --> periodic
    calculators --> ksdft
    analysis --> workflows
    analysis --> periodic
    analysis --> ksdft
```

The reverse `petrinet.colored → workflows` dependency is forbidden.

## Components

| Component | Subpackage | Responsibility |
|---|---|---|
| Application composition | `ksdft2effmass.application` | Assembles explicit immutable definitions, Tasks, executors, analyzers, stores, repositories, and configuration |
| Shared revision persistence | `ksdft2effmass.persistence` | Owns opaque immutable revision storage and the standard-library SQLite realization, not domain repository meaning |
| Development harness | `ksdft2effmass.harness` | Governs software-development work independently of scientific Workflow state |
| Scientific workflow | `ksdft2effmass.workflows` | Owns ResultObject/Task/Workflow contracts, TaskStartGateSet, discriminated TaskActivation, adapter, replayable WorkflowRun, dispatch envelopes, result ingress, and control |
| Generic colored Petri net | `ksdft2effmass.petrinet.colored` | Owns generic colors, places, transitions, markings, deterministic selection, and pure firing |
| Project composition definitions | `ksdft2effmass.campaigns` | Supplies project-specific composition inputs without owning generic workflow semantics |
| Calculator contracts | `ksdft2effmass.calculators` | Owns project-facing SimulationTasks, Simulation composites, immutable exact inputs/outputs, executable configuration, process records, and consumer-owned executor protocols |
| Quantum ESPRESSO integration | `ksdft2effmass.integration.quantumespresso` | Owns concrete QE serialization, staging, workspace/process invocation, mechanical capture, artifact discovery, native parsing, failure mapping, and observation adaptation |
| Scientific observations | `ksdft2effmass.periodic`, `.ksdft` | Owns neutral geometry and Kohn–Sham observation invariants |
| Scientific analysis | `ksdft2effmass.analysis` | Owns deterministic algorithms, tolerances, and numerical policy |

## Architecture map

### Development harness

- [Overview](ksdft2effmass/harness/index.md)
- [Object model](ksdft2effmass/harness/object-model.md)
- [Development Task model](ksdft2effmass/harness/development-harness.md)
- [Compiler architecture](ksdft2effmass/harness/compiler-architecture.md)
- [Normalized-state validation](ksdft2effmass/harness/validation.md)
- [Repository-wide development conformance](ksdft2effmass/harness/conformance.md)
- [Control plane](ksdft2effmass/harness/control-plane.md)
- [Persistence](ksdft2effmass/harness/persistence.md)
- [Projections](ksdft2effmass/harness/projections.md)
- [Pi subagent boundary](ksdft2effmass/harness/subagents.md)

### Scientific workflow and generic semantics

- [Workflow overview](ksdft2effmass/workflows/index.md)
- [Task, Workflow, and colored-Petri-net adapter](ksdft2effmass/workflows/task-and-colored-petri-net-adapter.md)
- [Generic colored Petri net](ksdft2effmass/petrinet/colored/index.md)
- [WorkflowRun object model](ksdft2effmass/workflows/workflow-run.md)
- [Simulation Task model](ksdft2effmass/workflows/simulation-task-model.md)
- [Control plane](ksdft2effmass/workflows/control-plane.md)
- [Persistence](ksdft2effmass/workflows/persistence.md)
- [Artifact and provenance model](ksdft2effmass/workflows/artifact-and-provenance-model.md)
- [Read models](ksdft2effmass/workflows/read-models.md)

### Calculators, integration, observations, analysis, and composition

- [Prospective package map](ksdft2effmass/index.md)
- [Application composition root](ksdft2effmass/application/index.md)
- [Campaign definitions](ksdft2effmass/campaigns/index.md)
- [Calculator architecture](ksdft2effmass/calculators/index.md)
- [Quantum ESPRESSO calculator contract](ksdft2effmass/calculators/quantum-espresso.md)
- [Integration namespace](ksdft2effmass/integration/index.md)
- [Quantum ESPRESSO integration](ksdft2effmass/integration/quantumespresso/index.md)
- [Periodic observations](ksdft2effmass/periodic/index.md)
- [Kohn–Sham observations](ksdft2effmass/ksdft/index.md)
- [Scientific analysis architecture](ksdft2effmass/analysis/index.md)
- [Scientific analysis](ksdft2effmass/analysis/analysis.md)
- [Repository layout and dependency direction](repository-layout.md)

### Shared contracts

- [Shared revision persistence](ksdft2effmass/persistence/index.md)
- [Human decisions](human-decisions.md)
- [Architecture principles](principles.md)
- [Identity, version, and failure contracts](identity-version-and-failure-contracts.md)
- [Separation of harness and workflow](separation-of-harness-and-workflow.md)

## Reading paths

### Whole system

1. [Architecture principles](principles.md)
2. [Repository layout](repository-layout.md)
3. [Shared revision persistence](ksdft2effmass/persistence/index.md)
4. [Separation of harness and workflow](separation-of-harness-and-workflow.md)
5. [Human decisions](human-decisions.md)
6. [Application composition root](ksdft2effmass/application/index.md)

### Scientific execution

1. [Workflow overview](ksdft2effmass/workflows/index.md)
2. [Generic colored Petri net](ksdft2effmass/petrinet/colored/index.md)
3. [Task and adapter model](ksdft2effmass/workflows/task-and-colored-petri-net-adapter.md)
4. [WorkflowRun object model](ksdft2effmass/workflows/workflow-run.md)
5. [Simulation Task model](ksdft2effmass/workflows/simulation-task-model.md)
6. [Quantum ESPRESSO](ksdft2effmass/calculators/quantum-espresso.md)
7. [Scientific analysis](ksdft2effmass/analysis/analysis.md)

## Related versioned documentation

- [Architecture v1](../v1/index.md) describes the implemented snapshot.
- [Migration from v1 to v2](../migration/v1-to-v2/index.md) owns cutover comparisons.
- [Architecture v2 live issue register](issues/index.md) records current material gaps.

## Status

Architecture v2 is prospective and unimplemented. The live issue register has no open issues. This index grants no implementation, scientific or protected execution, successor activation, publication, release, verification, validation, or human acceptance.
