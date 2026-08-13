# Scientific execution harness

## Target responsibility

The scientific execution harness is conceptually aligned with
`projectkoios.workflows` from the future reusable repository
`eragasa/projectkoios-workflows`. It owns generic deterministic scientific
workflow contracts without owning ksdft2effmass-specific physics or calculator
formats.

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

Calculator executor implementations remain calculator-package responsibilities.
Analysis algorithms, numerical policy, project findings, and project scientific
dispositions remain project scientific responsibilities composed through these
generic contracts.

## Scientific service boundary

A `ScientificService` exposes one cohesive scientific operation family. It
accepts explicit scientific intent and authority, constructs or selects a
`Campaign`, initializes a `CampaignRun`, and composes catalogs, executors,
analyzers, and persistence. A service is not a mutable plugin registry and does
not discover calculators from ambient state.

The service catalog is immutable for one run. Each entry declares accepted
inputs, result type, required capabilities, effect class, and authority needs.
Catalog membership does not itself authorize execution.

## Execution boundary

A `SimulationExecutor` receives an immutable `Simulation` and returns a
`SimulationExecutionResult`. Calculator-specific implementations own executable
configuration, process invocation, staging, completion-marker capture, and
artifact publication. The generic harness sees only the protocol and represented
results.

A result records observations and findings. It does not claim solver convergence,
numerical acceptance, scientific validation, or human disposition.

## Analysis and disposition

A deterministic analyzer maps normalized execution observations to a
`ScientificAnalysis`. Its algorithms, units, tolerances, and acceptance rules
are explicit. A `ScientificDisposition` is a separate authorized conclusion that
references the analyses and declared intended use.

## Reusable package boundary

`projectkoios.workflows` is the target owner for `Campaign`, `CampaignRun`,
`Simulation`, `SimulationExecutionResult`, `SimulationExecutor`,
`ScientificService`, `ArtifactManifest`, `CpnDefinition`, and `CpnMarking` only
where the contracts are genuinely calculator- and project-independent.

Project-specific campaign definitions, calculator payloads and executor
implementations, mechanical I/O, analysis algorithms, numerical policies,
findings, and dispositions remain in their owning project packages. Exact extraction
and import paths are accepted only after tutorial-driven contracts stabilize.
