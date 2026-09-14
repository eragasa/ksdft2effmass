# `ksdft2effmass.calculators` package

## Responsibility

`ksdft2effmass.calculators` owns backend-neutral calculator vocabularies and narrow
structural ports. Its canonical plane-wave DFT surface is
`ksdft2effmass.calculators.dft.pw`; the `pw` segment means the plane-wave method, not
Quantum ESPRESSO's `pw.x` executable. Shared fields are limited to concepts with
demonstrated calculator-independent meaning and do not form a universal native input,
executor, electronic-structure base class, or plugin registry. External-system input,
output, executable, diagnostic, artifact, and concrete execution meaning belongs to
`ksdft2effmass.integration.<external_system>`. Integrations may depend inward on
calculator and Workflow contracts; neither generic package imports an integration.

```mermaid
flowchart LR
    activation["TaskActivation"] --> control["Workflow-control authority check"]
    exact_input["Exact calculator input and explicit context"] --> control
    control --> unit["Validated successor + exact grant reservation + dispatch obligation"]
    unit --> repository["WorkflowRunRepository atomic complete-unit commit"]
    repository --> executor_check["Independent executor-boundary authority check"]
    executor_check --> adapter["Injected integration executor"]
    adapter --> effect["Calculator-specific bounded process effect"]
    effect --> result["Concrete immutable ResultObject"]
    result --> outcome["SimulationDispatchOutcome envelope"]
    outcome --> ingress["TaskResultIngester admission"]
    ingress --> repository
    ingress --> parser["Integration-owned native parsers and semantic adapter"]
    parser --> observations["Workflow-owned NormalizedObservationSet"]
```

Backend-neutral calculator meaning, concrete integration execution and parsing,
neutral-record invariants, workflow aggregation, and scientific analysis have separate
owners. The accepted
[plane-wave DFT and QE package-ownership decision](quantum-espresso-package-ownership-decision.md)
places every QE-specific contract and implementation in
`ksdft2effmass.integration.quantum_espresso`.

## Shared contracts

| Object | Responsibility |
|---|---|
| `PlaneWaveCalculator` | Runtime-checkable structural port parameterized by exact integration-owned input and output types; conformance supplies no authority or registry |
| `PlaneWaveSimulationSpecification` | Compact portable candidate containing exact physical-branch identity, wavefunction cutoff, and observation requirements |
| `PlaneWaveBackendSupplement` | Reference to one exact integration-owned typed native supplement |
| `PlaneWaveBackendBinding` | Complete portable specification plus exact selected backend supplement |
| `PlaneWaveBackendCompilationCompiled` / `PlaneWaveBackendCompilationFailure` | Closed successful or fail-closed binding result without partial plans |

These records do not form a universal electronic-structure calculator base. The shared
[plane-wave QoI and parameter-study architecture](../plane-wave-parameter-studies.md)
describes portable scientific and numerical concepts while every integration retains
its exact native supplement, input, output, diagnostic, artifact, and mechanical
contracts. A runtime plugin registry or generic scientific tag dictionary is not part
of this boundary.

## Initial private SCF-to-bands slice

The human-selected [DFT simulation CPN service decision](../workflows/dft-simulation-cpn-service-decision.md)
introduced a private `_dft` probe with concrete QE and ABINIT SCF and
fixed-density-bands input/output records, closed `SimulationTypeInput` and
`SimulationTypeOutput` unions, and a narrow structural `DftCalculator` port.
The records carry only exact input, pseudopotential, process-observation,
continuation-state, and result identities needed by the probe. Direct artifact-owned
software verification covers nominal field preservation, variant separation,
intrinsic rejection, immutability, structural protocol conformance, and absence from
the supported package surface. This bounded private slice is human-accepted and
administratively closed. The records are not exported from the package root and do not
implement dispatch, authority, native parsing, convergence interpretation, or a stable
public calculator contract. The later package-ownership decision supersedes this
probe as a placement precedent: backend-neutral contracts migrate to `dft.pw`, while
QE and ABINIT native records belong to their respective integrations.

## Explicit execution boundary

Workflow control checks the exact unused grant, TaskActivation, explicit execution context, exact input artifacts, executable configuration, and resource ceiling. `SimulationExecutionRequest` binds the exact Task instance, TaskActivation, attempt, executor, already-bound ResultObject inputs, grant, and obligation scope without embedding a generic Simulation aggregate. Workflow control then constructs the complete request/attempt/successor/grant-reservation/dispatch-obligation unit for atomic repository commit. The repository commits only that supplied unit and neither chooses a start gate nor invokes a Task.

Immediately before the process effect, the concrete integration implementation of the
backend-neutral target-first plane-wave executor protocol independently requires an
exact `authorized` `SimulationExecutionAuthorizationResult` for the same reserved
grant, verified authority snapshot, context, exact native integration input,
configuration, and limits. It then performs one expected-revision compare-and-swap
claim from `reserved` to `claimed`; only the successful claimant executes. Missing,
stale, mismatched, revoked, consumed, out-of-scope, unverifiable, duplicate, or losing
inputs cause no execution. One grant covers one exact dispatch; retry or a new attempt
requires new activation, operation, request, attempt, obligation, and grant identities.

`SimulationDispatchAdapter` owns dispatch orchestration and the closed confirmed, rejected, or indeterminate `SimulationDispatchOutcome` envelope. The effect-free `ColoredPetriNetWorkflowAdapter` owns only gate/value mapping, discriminated TaskActivation construction, confirmed returned-ResultObject mapping, and pure-firing composition. The calculator package owns the backend-neutral executor port; the injected integration owns concrete native input and immutable result meaning, the bounded external effect, and the returned concrete ResultObject. Confirmed dispatch carries that exact returned object and correlations rather than creating a second result object. Indeterminate work retains its original identities and is not automatically redispatched. `TaskResultIngester` and explicit extraction specifications remain workflow-owned; calculator-produced files are not republished by result ingress. After reconciliation, workflow control constructs the corresponding candidate generic `TaskInvocationOutcome`. For confirmed work, `TaskResultIngester` validates its correlation to the specialized envelope and atomically admits the concrete result with the generic outcome and result transition; rejected or indeterminate generic outcomes reference their exact specialized outcome without results.

## Exact inputs and claims

Existing native inputs and pseudopotential artifacts remain usable under their actual content identities and provenance without rendering, conversion, registration, rerun, or evidence reclassification. Shared labels, nominal methods, elements, cutoffs, pseudopotential families/assets, or settings do not establish equivalence. Any equivalence assertion requires a separately authorized evidence-bearing comparison or validation claim.

## Pages

- [Plane-wave QoIs and parameter studies](../plane-wave-parameter-studies.md)
- [Quantum ESPRESSO](quantum-espresso.md)
- [Plane-wave DFT and QE package ownership](quantum-espresso-package-ownership-decision.md)
- [QE task-contract boundary decision](quantum-espresso-task-contract-boundary-decision.md)

## Deferred implementation details

- Whether demonstrated repeated integrations eventually justify an additional calculator-independent process protocol beyond existing project-owned request/observation records.
- Remote and scheduler adapter contracts.
- Standard resource-observation vocabulary.
- Exact public serialization and wire contracts.
