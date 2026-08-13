# Scientific workflow

## Responsibility

The scientific workflow is owned by `ksdft2effmass.workflows`. It owns deterministic calculator-independent scientific workflow contracts without owning calculator formats or project-specific scientific algorithms.

Its generic authority includes:

- scientific service composition contracts;
- calculator-independent simulation specifications;
- the `SimulationExecutor` protocol;
- calculator-independent CPN `Campaign` definitions;
- `CampaignRun` state;
- execution-result record contracts;
- artifact-lineage contracts;
- scientific-analysis and finding record contracts; and
- scientific-disposition record contracts.

Calculator executor implementations remain calculator-package responsibilities. Analysis algorithms, numerical policy, project findings, and project scientific dispositions remain project scientific responsibilities composed through these generic contracts.

## Scientific service boundary

A `ScientificService` exposes one cohesive scientific operation family. It accepts explicit scientific intent and authority, constructs or selects a `Campaign`, initializes a `CampaignRun`, and composes catalogs, executors, analyzers, and persistence. A service is not a mutable plugin registry and does not discover calculators from ambient state.

The service catalog is immutable for one run. Each entry declares accepted inputs, result type, required capabilities, effect class, and authority needs. Catalog membership does not itself authorize execution.

## Execution boundary

A `SimulationExecutor` receives an immutable `Simulation` and returns a `SimulationExecutionResult`. Calculator-specific implementations own executable configuration, process invocation, staging, completion-marker capture, and artifact publication. The generic workflow sees only the protocol and represented results.

A result records observations and findings. It does not claim solver convergence, numerical acceptance, scientific validation, or human disposition.

## Analysis and disposition

A deterministic analyzer maps normalized execution observations to a `ScientificAnalysis`. Its algorithms, units, tolerances, and acceptance rules are explicit. A `ScientificDisposition` is a separate authorized conclusion that references the analyses and declared intended use.

## Package boundary

`ksdft2effmass.workflows` owns `Campaign`, `CampaignRun`, `Simulation`, `SimulationExecutionResult`, `SimulationExecutor`, `ScientificService`, `ArtifactManifest`, `CpnDefinition`, and `CpnMarking` as calculator-independent contracts.

Project-specific campaign definitions, calculator payloads and executor implementations, mechanical I/O, analysis algorithms, numerical policies, findings, and dispositions remain in their owning `ksdft2effmass` subpackages.

## Detailed pages

- [Scientific service model](service-model.md)
- [Simulation model](simulation-model.md)
- [Campaign and CPN model](campaign-and-cpn-model.md)
- [CampaignRun object model](campaign-run.md)
- [Workflow control plane](control-plane.md)
- [Workflow persistence](persistence.md)
- [Artifact and provenance model](artifact-and-provenance-model.md)
- [Scientific read models](read-models.md)
- [Separation from the development harness](../separation-of-harness-and-workflow.md)

## Unresolved issues

- Exact public submodule names within `ksdft2effmass.workflows`.
- Synchronous and asynchronous service execution boundaries.
- Persistence and artifact-store implementation technologies.
- Optional external workflow adapter contracts.
- Campaign catalog versioning and distribution.
