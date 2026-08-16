# Migration from Architecture v1 to Architecture v2

This subtree is the sole maintained cross-version comparison. This index maps the [implemented v1 snapshot](../../v1/index.md) to the [prospective v2 target](../../v2/index.md) without claiming that target components exist.

## Subject crosswalks

- [Coding-standards conformance](coding-standards-conformance.md)
- [Pi harness subagents](pi-harness-subagents.md)
- [Agent execution and deterministic actions](agents.md)

## Current implementation status

- v1 remains implemented.
- Its colored-Petri-net primitives and public abbreviated names remain under `ksdft2effmass.workflows.cpn`.
- The prospective v2 generic package is `ksdft2effmass.petrinet.colored` and uses only full public `ColoredPetriNet*` names.
- No source move, v2 persistence/Task/Workflow/Simulation/Pi-agent-adapter implementation, scientific executable, governed operator, or canonical scientific Workflow is authorized by this migration page.
- Prospective v2 selects `ksdft2effmass.persistence` with a standard-library SQLite initial store realization; the exact wire and SQLite schemas and operational policy remain deferred.
- Durable chain and Task records, not this page, own current development activity.

The v1 `Cpn*` names are implemented public API. Workflow implementations may later use such spellings as private/local import aliases, but v2 does not export or document them as a second prospective public API.

## Responsibility crosswalk

| V1 responsibility or surface | Prospective v2 owner | Disposition | Migration condition |
|---|---|---|---|
| Development Task coordination | Development harness | Retain and narrow | Scientific state separated |
| V1 Python maintained-evidence conformance scripts | Coding-standards conformance with explicit v1-compatible adapters | Retain and narrow | Controlled valid/invalid fixtures establish compatibility; unrelated harness validation remains with its domain owners |
| Existing colored-Petri-net primitives in `workflows.cpn` | `petrinet.colored` generic boundary | Retain v1; move only under later authority | Full-name API and compatibility plan accepted |
| Task-based scientific execution state | `WorkflowRun` | Replace | Workflow persistence exists |
| Shell sequencing | `Workflow` plus `ColoredPetriNetWorkflowAdapter` | Replace | Required behavior demonstrated |
| Producer-Task prerequisites | ResultObject-valued dependency edges plus exact Workflow/WorkflowRun/Task-instance/TaskActivation/attempt/ResultObject producer provenance | Replace | Provenance and dependency contracts accepted |
| Direct calculator runner | Concrete SimulationTask and target-first executor | Replace | Applicable software behavior demonstrated |
| Compact execution records | Concrete immutable ResultObjects and `ArtifactManifest` | Split | Wire contracts accepted |
| Scientific review encoded in Task lifecycle | `ScientificAnalysis` and `ScientificFinding`, followed by human-reviewed external research conclusions | Replace | Analysis lifecycle implemented; no `ScientificDisposition` subsystem or workflow acceptance state is introduced |
| Harness SQLite projections | Development harness projections | Retain and narrow | Scientific state removed; generated projection publication remains separate from ordinary revision storage |
| Revision-storage capability | `persistence.store` plus `persistence.sqlite` | Introduce prospectively | Opaque single-stream contract and stdlib SQLite realization implemented under later authority |
| HarnessState persistence | Domain-owned `HarnessStateRepository` and composed `HarnessStateAtomicRepository` | Retain domain meaning; compose shared store | Exact serializer/validator binding and compatibility gates accepted |
| WorkflowRun persistence | Domain-owned `WorkflowRunRepository` and composed `WorkflowRunAtomicRepository` | Introduce prospectively | Complete aggregate transaction and compatibility gates accepted |
| Direct convergence outputs | Closed artifact producer-provenance variants | Retain at declared evidence class | No rerun or invented WorkflowRun required |
| QE/QEXSD parsing and normalization | Concrete parsers and observation adapter in `.integration.quantumespresso`; normalized set in `.workflows` | Retain and separate | Explicit composition integrated |
| Exact QE input and pseudopotentials | `QuantumEspressoInput` in the QE Simulation composite | Retain exact identities and provenance | No mandatory rendering, conversion, or registration |
| Implemented v1 `.pi/checkpoints` development-decision source | One immutable `DevelopmentDecision` model in `HarnessState`, with unresolved and resolved variants/revisions | Retain through migration, then transform losslessly | Exact request/question/options/scope, verbatim response, unambiguous normalized declared outcome, source/authority identity, status, and predecessor/supersession are preserved; ambiguous/no-match/conflicting responses remain unresolved |
| V1 scientific checkpoint implementation | None | Do not fabricate | Migration creates no `ScientificDecisionRequest` or `ScientificDecisionResolution`; future scientific records require an explicit v2 workflow event |
| Protected-execution decisions | Exact one-dispatch grant referenced by `TaskActivation` and `WorkflowRun` | Replace | Independent control plane verifies reservation/use; a decision record is not a grant |

Project-specific campaign definitions may be re-expressed as composition inputs under `ksdft2effmass.campaigns`; they do not become the generic Workflow or colored-Petri-net aggregate.

## Migration order

1. Preserve and document Architecture v1.
2. Losslessly crosswalk implemented v1 `.pi/checkpoints` into `DevelopmentDecision` revisions only when the exact preservation condition above can be met; keep unresolved/ambiguous records unresolved, retain `.pi/checkpoints` as the implemented source until cutover, and create no scientific resolution.
3. Accept exact v2 public and wire contracts for ResultObject, Task, Workflow, TaskStartGateSet, discriminated TaskActivation, generic colored-Petri-net firing records, closed task/scientific-decision WorkflowTransitionRecord origins, and replayable WorkflowRun.
4. Implement the generic boundary locally without changing the implemented v1 API until a separate migration authorizes it.
5. Implement the shared `AtomicRevisionStore` contract and standard-library `SQLiteAtomicRevisionStore` under separate source authority, retaining indeterminate outcomes and single-stream scope.
6. Implement the domain repositories with exact validator/serializer-to-bytes binding, separate development/scientific stores by default, and independent Workflow membership and result-dependency edges.
7. Implement the calculator-owned QE SimulationTask/composite and its injected `integration.quantumespresso` adapter for the exact tutorial inputs under separate bounded work.
8. Demonstrate applicable direct and Workflow-controlled software behavior without treating it as scientific validation.
9. Retain historical convergence artifacts under their actual producer-provenance variants without recalculation.
10. Preserve human-reviewed conclusions as external research records citing exact analysis identities; do not migrate them into `WorkflowRun` disposition or acceptance state.
11. Remove v1 scientific-execution coupling only after the replacement behavior actually required by retained use passes its accepted compatibility gates.

No step activates its successor. Scientific execution requires separate exact protected-execution authority.

## Exact-artifact and no-recalculation boundary

Existing QE native inputs, pseudopotentials, outputs, and convergence artifacts retain actual content identities, software/settings evidence, provenance, and limitations. They may remain external observations, imported retained fixtures, human-authored compact inputs, or bounded legacy records. Migration does not require rendering, conversion, registration, rerun, assignment to WorkflowRun, fabricated Task provenance, or evidence reclassification.

Same labels, methods, cutoffs, pseudopotential families/assets, or settings across implementations do not establish equivalence. Any equivalence finding requires a separate evidence-bearing comparison or validation claim.

## Package and dependency boundary

The prospective shared package is `ksdft2effmass.persistence`: `persistence.sqlite → persistence.store`, `harness.persistence → persistence.store`, and `workflows.persistence → persistence.store`. `application` constructs explicitly configured, separate development and scientific SQLite stores and composed domain repositories. `persistence` imports no harness, workflow, Petri-net, calculator, analysis, provenance, or application domain. This adds no generic CRUD repository, persistence inheritance hierarchy, cross-stream transaction, or shared physical database.

The required prospective edge is `ksdft2effmass.workflows → ksdft2effmass.petrinet.colored`; the reverse edge is forbidden. Calculators continue to depend on workflow contracts, and workflows do not import calculator packages. Project-facing QE Task, Simulation, immutable input/output, configuration, process-record, and executor-protocol types remain under `ksdft2effmass.calculators`. Concrete QE adaptation is owned by `ksdft2effmass.integration.quantumespresso`, which depends on calculators; calculators never import integration, and application composition injects the concrete implementation.

Potential ProjectKoios extraction remains deferred. Neither ProjectKoios repository is claimed as installed or integrated, and no extraction occurs without separate dependency, licensing, compatibility, and acceptance authority.

## Status

The [Architecture v2 live issue register](../../v2/issues/index.md) has no open issues. This page is a migration crosswalk only: it does not authorize implementation, source moves, scientific execution, successor activation, publication, or release.
