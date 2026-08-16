# Migration from Architecture v1 to Architecture v2

This subtree is the sole maintained cross-version comparison. This index maps the [implemented v1 snapshot](../../v1/index.md) to the [prospective v2 target](../../v2/index.md) without claiming that target components exist.

## Subject crosswalks

- [Pi harness subagents](pi-harness-subagents.md)

## Current implementation status

- v1 remains implemented.
- Its colored-Petri-net primitives and public abbreviated names remain under `ksdft2effmass.workflows.cpn`.
- The prospective v2 generic package is `ksdft2effmass.petrinet.colored` and uses only full public `ColoredPetriNet*` names.
- No source move, v2 persistence/Task/Workflow/Simulation implementation, scientific executable, or canonical scientific Workflow is authorized by this migration page.
- Prospective v2 selects `ksdft2effmass.persistence` with a standard-library SQLite initial store realization; the exact wire and SQLite schemas and operational policy remain deferred.
- Durable chain and Task records, not this page, own current development activity.

The v1 `Cpn*` names are implemented public API. Workflow implementations may later use such spellings as private/local import aliases, but v2 does not export or document them as a second prospective public API.

## Responsibility crosswalk

| V1 responsibility or surface | Prospective v2 owner | Disposition | Migration condition |
|---|---|---|---|
| Development Task coordination | Development harness | Retain and narrow | Scientific state separated |
| Existing colored-Petri-net primitives in `workflows.cpn` | `petrinet.colored` generic boundary | Retain v1; move only under later authority | Full-name API and compatibility plan accepted |
| Task-based scientific execution state | `WorkflowRun` | Replace | Workflow persistence exists |
| Shell sequencing | `Workflow` plus `ColoredPetriNetWorkflowAdapter` | Replace | Required behavior demonstrated |
| Producer-Task prerequisites | ResultObject-valued dependency edges plus exact Workflow/WorkflowRun/Task-instance/TaskActivation/attempt/ResultObject producer provenance | Replace | Provenance and dependency contracts accepted |
| Direct calculator runner | Concrete SimulationTask and target-first executor | Replace | Applicable software behavior demonstrated |
| Compact execution records | Concrete immutable ResultObjects and `ArtifactManifest` | Split | Wire contracts accepted |
| Scientific review encoded in Task lifecycle | `ScientificAnalysis` and `ScientificDisposition` | Replace | Scientific lifecycle implemented |
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

## Selected v2 model

`ResultObject` is an immutable workflow-facing category whose concrete domains own intrinsic invariants. `Task` consumes already-bound ResultObjects plus explicit context and returns ResultObjects. `Workflow` implements Task and may be nested. Run-scoped Task instances have zero or one `TaskStartGateSet` in `any_of` or `all_of` mode. `TaskActivation` is discriminated as direct (no gate identities), any_of (one deterministic gate/binding), or all_of (canonical compatible complete tuple).

`ColoredPetriNetWorkflowAdapter` maps gates and supplied ResultObject values to `ksdft2effmass.petrinet.colored`, constructs TaskActivations only for Task-origin work, remains effect-free while workflow control/dispatch invokes Tasks across the accepted authority boundary, and maps supplied values into immutable `ColoredPetriNetFiringInput`. For scientific-decision ingress it maps the supplied resolution for the exact request-identified transition/binding without a Task, TaskActivation, or attempt. Pure firing evaluates output inscriptions, validates produced tokens, and returns successor plus audit facts. Parent/child membership and ResultObject dependency remain orthogonal.

`Simulation` is structural. Calculator-owned `QuantumEspressoSimulationTask` contains or uses `QuantumEspressoSimulation`, whose roles are immutable `QuantumEspressoInput`, the consumer-owned structural `QuantumEspressoExecutor` protocol, and produced immutable `QuantumEspressoOutput` ResultObject. Application composition injects the concrete `integration.quantumespresso` implementation, which owns serialization, staging, workspace/process invocation, native parsing, artifact discovery, failure mapping, and observation adaptation. The output is returned as a new object and correlated in WorkflowRun state. `SimulationExecutionRequest` binds exact Task-instance/activation/attempt/executor/input/grant/obligation identities without embedding generic Simulation. Confirmed `SimulationDispatchOutcome` envelopes the returned `QuantumEspressoOutput`; `TaskResultIngester` admits that concrete object, and no second execution-result object exists.

WorkflowRun persistence uses exact initial/current marking snapshots plus canonical ordered transition records and explicit Task-instance, activation, attempt, request, failure, result-production/dependency, authority/outcome, obligation, and scientific decision request/resolution state. Each transition record has exactly one task or scientific-decision origin; the latter carries exact request/resolution identities and prohibits TaskActivation/attempt. Replay must equal the stored current marking and consumes a recorded resolution without prompting. See the prospective [human-decision contract](../../v2/human-decisions.md).

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
10. Remove v1 scientific-execution coupling only after the replacement behavior actually required by retained use passes its accepted compatibility gates.

No step activates its successor. Scientific execution requires separate exact protected-execution authority.

## Exact-artifact and no-recalculation boundary

Existing QE native inputs, pseudopotentials, outputs, and convergence artifacts retain actual content identities, software/settings evidence, provenance, and limitations. They may remain external observations, imported retained fixtures, human-authored compact inputs, or bounded legacy records. Migration does not require rendering, conversion, registration, rerun, assignment to WorkflowRun, fabricated Task provenance, or evidence reclassification.

Same labels, methods, cutoffs, pseudopotential families/assets, or settings across implementations do not establish equivalence. Any equivalence finding requires a separate evidence-bearing comparison or validation claim.

## Package and dependency boundary

The prospective shared package is `ksdft2effmass.persistence`: `persistence.sqlite → persistence.store`, `harness.persistence → persistence.store`, and `workflows.persistence → persistence.store`. `application` constructs explicitly configured, separate development and scientific SQLite stores and composed domain repositories. `persistence` imports no harness, workflow, Petri-net, calculator, analysis, provenance, or application domain. This adds no generic CRUD repository, persistence inheritance hierarchy, cross-stream transaction, or shared physical database.

The required prospective edge is `ksdft2effmass.workflows → ksdft2effmass.petrinet.colored`; the reverse edge is forbidden. Calculators continue to depend on workflow contracts, and workflows do not import calculator packages. Project-facing QE Task, Simulation, immutable input/output, configuration, process-record, and executor-protocol types remain under `ksdft2effmass.calculators`. Concrete QE adaptation is owned by `ksdft2effmass.integration.quantumespresso`, which depends on calculators; calculators never import integration, and application composition injects the concrete implementation.

Potential ProjectKoios extraction remains deferred. Neither ProjectKoios repository is claimed as installed or integrated, and no extraction occurs without separate dependency, licensing, compatibility, and acceptance authority.

## Unresolved target decisions

The complete current live set is recorded in the [Architecture v2 live issue register](../../v2/issues/index.md):

- selection identity and scientific authority grants: [007](../../v2/issues/007-selection-identity-closure.md), [010](../../v2/issues/010-scientific-authority-grants.md);
- Workflow replay, persistence commit and reconstruction, scientific-decision ingress, Task invocation, and publication: [020](../../v2/issues/020-workflow-replay-integrity-ownership.md), [021](../../v2/issues/021-persistence-commit-read-reconciliation-closure.md), [022](../../v2/issues/022-scientific-decision-trust-provenance-correction.md), [023](../../v2/issues/023-task-workflow-simulation-invocation-semantics.md), [024](../../v2/issues/024-publication-policy-store-reconciliation.md);
- bounded conformance execution and target-operation binding: [030](../../v2/issues/030-bounded-conformance-execution.md), [033](../../v2/issues/033-target-operation-identity-binding.md); and
- scientific disposition and harness-publication authority/outcome: [029](../../v2/issues/029-scientific-disposition-ownership-semantics.md), [032](../../v2/issues/032-harness-publication-authority-outcome.md).

Exact persistence bytes and wire schemas, SQLite layout and operational policy, asynchronous and scheduler interfaces, optional QE operations, structured-rendering policy, and later extraction or source moves remain deferred where they do not block current semantic closure.

## Live issues and claim boundary

The selected lean persistence architecture introduces only immutable shared revision/commit/result values, structural `AtomicRevisionStore`, standard-library `SQLiteAtomicRevisionStore`, and composed domain atomic repositories. It is prospective and unimplemented; exact schemas and operations remain deferred where they are not required for current semantic closure.

The [Architecture v2 live issue register](../../v2/issues/index.md) is the sole live set and contains issues 007, 010, 020–024, 029–030, and 032–033. Inclusion does not select an outcome or authorize work; the issues are reviewed and resolved one at a time.

This claims no v2 implementation, software verification, numerical verification, calculation or recalculation, protected-execution authority, scientific validation, uncertainty quantification, equivalence, rerun, or human software acceptance.
