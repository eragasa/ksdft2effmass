# Architecture v2 repository layout

## Target package ownership

```text
projectkoios.bootstrap
    development-harness contracts

projectkoios.workflows
    generic scientific workflow contracts

ksdft2effmass.calculators
    calculator-specific simulation objects and executors

ksdft2effmass.io
    mechanical calculator input/output translation

ksdft2effmass.periodic
    periodic geometry and structure semantics

ksdft2effmass.ksdft
    representation-neutral KS semantics

ksdft2effmass.analysis
    deterministic scientific analysis

ksdft2effmass.campaigns
    project-specific scientific campaign definitions
```

Exact stable import paths remain unresolved until tutorial-driven implementation
demonstrates cohesive contracts. The ownership and dependency direction are
normative even when module spelling remains open.

## Dependency direction

```text
ksdft2effmass.campaigns
    → projectkoios.workflows
    → generic Simulation and artifact contracts

ksdft2effmass.calculators
    → generic Simulation and artifact contracts
    → ksdft2effmass.io

ksdft2effmass.analysis
    → normalized periodic and KS observations
    → generic scientific analysis contracts

project-specific composition
    → projectkoios.bootstrap
```

Forbidden directions include:

```text
projectkoios.workflows
    ✗→ ksdft2effmass.calculators

ksdft2effmass.campaigns
    ✗→ calculator-specific input structures

ksdft2effmass.periodic
    ✗→ calculator packages

ksdft2effmass.ksdft
    ✗→ calculator packages

ksdft2effmass.io
    ✗→ Campaign or CampaignRun

projectkoios.bootstrap
    ✗→ ksdft2effmass scientific policy
```

## Responsibilities

- `projectkoios.bootstrap` owns generic development lifecycle and repository
  operation contracts only.
- `projectkoios.workflows` owns generic CPN, simulation, campaign, execution
  result, artifact-manifest, analysis, and service contracts only when they are
  demonstrably project-independent.
- `ksdft2effmass.calculators` owns executable configuration, calculator-specific
  typed simulation payloads, dispatch, staging, and result capture.
- `ksdft2effmass.io` owns native syntax, parsing, and mechanical translation.
- `ksdft2effmass.periodic` owns geometry, coordinate, unit, and sampling
  semantics.
- `ksdft2effmass.ksdft` owns representation-neutral Kohn–Sham observations and
  plane-wave representation records.
- `ksdft2effmass.analysis` owns deterministic scientific interpretation and its
  numerical policies.
- `ksdft2effmass.campaigns` owns project-specific CPN definitions and simulation
  selections without duplicating CPN execution semantics.

## Extension boundary

Additional calculators enter only after a demonstrated campaign requires them.
They implement the same `SimulationExecutor` boundary with their own typed
payloads and mechanical I/O. Optional adapters to external workflow ecosystems
may be added later without making AiiDA, Airflow, pymatgen, or another framework
a core dependency.
