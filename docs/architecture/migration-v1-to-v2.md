# Migration from Architecture v1 to Architecture v2

This page is the sole maintained cross-version comparison. It maps the
[implemented v1 snapshot](v1/index.md) to the [normative v2 target](v2/index.md)
without claiming that target components already exist.

## Current implementation status

At this boundary:

- v1 remains the implemented architecture;
- `harness.architecture-v2.plan` remains inactive and planning-only;
- `harness.architecture-v2.simulation-execution` is the sole active development
  Task, but implementation has not begun;
- no public v2 `Campaign`, `CampaignRun`, `Simulation`, `SimulationExecutor`,
  `SimulationExecutionResult`, `ScientificService`, `ScientificAnalysis`, or
  `ScientificDisposition` implementation exists;
- the existing backend-neutral CPN primitives are implemented locally under
  `ksdft2effmass.workflows.cpn`;
- `projectkoios.bootstrap` and `projectkoios.workflows` are target reusable
  ownership boundaries, not integrated dependencies; and
- no scientific executable or canonical scientific campaign is authorized by
  this migration plan.

## Responsibility crosswalk

| V1 responsibility or surface | V2 owner | Disposition | Migration condition |
|---|---|---|---|
| Development Task coordination | Development harness | Retain and narrow | Scientific state separated |
| Direct calculator runner | Calculator executor | Replace | Tutorial parity demonstrated |
| Task-based scientific execution state | `CampaignRun` | Replace | CPN campaign persistence exists |
| Shell sequencing | CPN `Campaign` | Replace | Direct/CPN equivalence passes |
| Compact execution records | `SimulationExecutionResult` and `ArtifactManifest` | Split | Wire contracts accepted |
| Scientific review encoded in Task lifecycle | `ScientificAnalysis` and `ScientificDisposition` | Replace | Scientific lifecycle implemented |
| Harness SQLite projections | Development harness projections | Retain and narrow | Scientific state removed |
| Existing CPN primitives | ProjectKoios Workflows target | Retain/extract later | Stable tutorial implementation |
| Direct convergence outputs | Project scientific fixture catalog (`bootstrap_fixture`; not ProjectKoios Bootstrap) | Retain as evidence | Retain independently; canonical rerun is required only before replacement as primary campaign evidence |
| Task JSON and chain active selection | `HarnessTask` and `DevelopmentTaskSelection` | Retain and narrow | Development-only semantics verified |
| Generic provenance records | Workflows artifact/result contracts plus project records | Split | Identity and wire boundaries accepted |
| QEXSD parser and semantic construction | `ksdft2effmass.io`, `.periodic`, and `.ksdft` | Retain | Simulation result normalization integrated |
| Operation-specific artifact retention | `ArtifactManifest` policy | Replace incrementally | Tutorial and convergence artifact roles represented |
| Calculator-specific scientific parameters in direct inputs | Typed `Simulation` payload | Replace | Exact input identity and replay parity pass |
| Human protected-execution decisions in chain history | Scientific execution authority referenced by `CampaignRun` | Replace | Independent scientific control plane persists authority |

## Package and extraction crosswalk

| Implemented v1 location | V2 target responsibility | Migration disposition |
|---|---|---|
| `ksdft2effmass.harness.pi` and `.local` | `projectkoios.bootstrap` plus project composition | Extract only stable project-independent development contracts |
| `ksdft2effmass.workflows.cpn` | `projectkoios.workflows` CPN foundation | Retain locally until tutorial Campaign contracts stabilize, then extract |
| `ksdft2effmass.provenance` | generic workflow artifact/result contracts and project provenance | Split by demonstrated generic ownership |
| `ksdft2effmass.io.quantum_espresso.qexsd` | `ksdft2effmass.io` | Retain as calculator mechanics |
| `ksdft2effmass.periodic` | `ksdft2effmass.periodic` | Retain |
| `ksdft2effmass.ksdft` and `.pw` | `ksdft2effmass.ksdft` | Retain |
| calculation-specific shell runners | `ksdft2effmass.calculators` | Replace after deterministic replay and tutorial parity |
| scientific Task definitions | `ksdft2effmass.campaigns` | Re-express only after CPN Campaign contract exists |
| calculation-specific analysis JSON/prose | `ksdft2effmass.analysis` | Replace with deterministic analyzers while retaining source fixtures |

Neither ProjectKoios repository is claimed as an installed or integrated
component. Extraction occurs only after local implementation demonstrates a
calculator-independent contract and acceptance explicitly authorizes the move.

## Architecture-documentation disposition

The former `docs/harness/architecture-v2/` pages mixed three categories. Their
content was classified paragraph by paragraph and disposed as follows:

| Former content | Classification | Maintained destination |
|---|---|---|
| Current Task, chain, control, SQLite, CLI, validation, and execution descriptions | v1 implemented description | `architecture/v1/index.md` |
| Two-harness, simulation, Campaign/CPN, artifact, control, persistence, and package responsibilities | v2 normative target | subject pages under `architecture/v2/` |
| Current-to-target maps, proposed slice chronology, bootstrap-execution comparison, and cutover conditions | cross-version migration material | this page |
| Repeated status banners, duplicate candidate inventories, and obsolete per-file planning narration | obsolete duplicate | deleted; Git history retained |

The former unversioned architecture pages were handled the same way. Implemented
CPN, QEXSD, periodic, provenance, proof, repository, and external-store facts are
summarized in the self-contained v1 snapshot. Target ownership is stated in v2.
Superseded prospective module trees and chronological planning prose are not
retained as parallel architecture authority.

## Migration order

1. Freeze and document Architecture v1.
2. Establish v2 simulation and execution-result contracts.
3. Implement native QE tutorial simulations.
4. Verify direct execution against accepted tutorial observations.
5. Implement calculator-independent `Campaign` as CPN.
6. Express tutorials as `Campaign` objects.
7. Verify direct-versus-CPN equivalence.
8. Persist `CampaignRun` independently of `HarnessTask` state.
9. Ingest direct convergence outputs as project scientific `bootstrap_fixture` records, not as ProjectKoios Bootstrap state.
10. Implement deterministic convergence analysis.
11. Re-express convergence as a scientific `Campaign`.
12. Execute canonical convergence campaign.
13. Extract stable generic contracts into `projectkoios-workflows`.
14. Reduce the development harness toward `projectkoios-bootstrap`.
15. Remove v1 scientific-execution coupling after parity.

Every step is a separate bounded development outcome. No step activates its
successor, and steps involving scientific execution require separate exact
protected-execution authority.

## Tutorial parity boundary

The accepted silicon SCF and bands observations are the first parity fixtures.
Direct replay and CPN-controlled replay must use the same simulation identities,
canonical input identities, executor contract, result identities, warnings, and
injected failures. CPN control may add ordering, authorization, synchronization,
and terminal-state semantics only.

Parity is software-verification evidence. It does not rerun a calculator, accept
a scientific result, or establish numerical or scientific validation.

## Convergence cutover

The 18 direct convergence invocations remain historical bootstrap execution
facts. Here `bootstrap` describes their development-era evidence classification;
it does not assign them to ProjectKoios Bootstrap. Their inputs, runner,
executable and PseudoDojo identities, process
results, output identities, resources, warnings, and external locations remain
fixtures. They are not rewritten into a `CampaignRun`.

A canonical convergence campaign exists only after:

1. simulation and result contracts are accepted;
2. calculator execution and artifact handling pass tutorial parity;
3. CPN campaign semantics and independent `CampaignRun` persistence pass;
4. deterministic convergence analysis is implemented; and
5. a new exact scientific execution receives human authorization.

Only the resulting authorized execution may produce the canonical scientific
`CampaignRun`. Its scientific disposition remains separately human-owned.

## Unresolved target decisions

The following remain deliberately open until implementation evidence exists:

- exact stable import paths within `projectkoios.bootstrap` and
  `projectkoios.workflows`;
- whether all generic contracts are extracted together or in smaller accepted
  packages;
- the exact public module names under `ksdft2effmass.calculators`, `.campaigns`,
  and `.analysis`;
- wire formats for `Campaign`, `CampaignRun`, `Simulation`,
  `SimulationExecutionResult`, `ArtifactManifest`, `ScientificAnalysis`, and
  `ScientificDisposition`;
- persistence technology for scientific state;
- public protocol versus concrete composition boundaries beyond the demonstrated
  `SimulationExecutor` family; and
- optional adapter contracts for external workflow ecosystems.

These open import and package decisions do not weaken the normative dependency
and authority boundaries in Architecture v2.

## Removal condition

V1 scientific-execution coupling may be removed only after direct tutorial
behavior, CPN tutorial behavior, result and artifact identity, failure
propagation, persisted `CampaignRun`, and scientific-analysis boundaries all pass
independent verification. Historical inputs, observations, and human decisions
remain retained according to their evidence and provenance roles.
