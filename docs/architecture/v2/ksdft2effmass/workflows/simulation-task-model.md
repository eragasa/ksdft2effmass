# Simulation Task model

## Definition order for additional calculators

A calculator-specific Simulation Task is not the starting point for a scientific
calculation contract. The calculator-independent QoI and normalized observation
requirements are defined first; effect-free backend capability and exact native
binding follow; project composition then produces run-scoped Task instances. Only
after those inputs and outputs are explicit is a calculator-specific Simulation Task
or executor defined.

The prospective [QoI-first LAMMPS integration](../qoi-first-lammps-integration.md)
records this ordering. It adapts the useful QoI-to-required-calculations direction
observed in `pypospack` without adopting its mutable managers, dynamic registries, or
combined planning/execution objects. This ordering governs future LAMMPS-specific
contracts and does not roll back the existing generic Workflow protocol or control
plane.

## Nominal simulation-Task boundary

`AbstractSimulationTask(AbstractScientificTask)` is the nominal ABC for a scientific
Task that must use the specialized external-dispatch control plane. It adds no second
execution signature, authority, scheduler, registry, or mutable simulation aggregate.
The retired structural `Task`, `Workflow`, and `SimulationTask` protocol model has no
compatibility aliases.

A simulation Task returns immutable `AbstractResultObject` instances only after the separately
authorized executor boundary reports and workflow control admits a confirmed result.
Nominal membership does not authorize an external effect or permit ordinary in-process
WorkflowEngine invocation.

The canonical `ksdft2effmass.integration.quantum_espresso` surface implements the
initial local executor, execution input, `pw.x`/`bands.x` result contracts, four
operation-specific public Task adapters, and an existing immutable Simulation
composition. The accepted target keeps the operation-specific contracts but changes
their execution ownership:

- `QuantumEspressoScfTask` owns one exact SCF operation definition and input;
- `QuantumEspressoNscfTask` owns one exact NSCF definition, input, and predecessor requirements;
- `QuantumEspressoBandPathTask` owns one exact band-path definition, input, and predecessor requirements; and
- `QuantumEspressoBandsExtractionTask` owns one exact bands-extraction definition, input, and predecessor requirements.

Each becomes an `AbstractSimulationTask` with no direct calculator invocation.
`WorkflowTaskBinding` correlates one planned Task instance with one nominal
`AbstractSimulationDispatchEffect`; the binding creates no authority. The existing
`LocalQuantumEspressoExecutor` migrates to that effect ABC and remains behind the
claim and dispatch-entry controls. QE Workflow families are separately implemented and
are not redesigned here. The existing `QuantumEspressoSimulation` receives only the
nominal-ABC reference changes needed by the repository-wide migration.

`AbstractPlaneWaveCalculator` remains the distinct non-authority-bearing generic
calculator ABC and is not inferred from an executor that happens to expose an
incompatible `execute` method. DOS remains deferred until its actual executable and
result boundary exists.

```mermaid
classDiagram
    class AbstractTask
    class AbstractScientificTask
    class AbstractSimulationTask
    class QuantumEspressoScfTask
    class QuantumEspressoNscfTask
    class QuantumEspressoBandPathTask
    class QuantumEspressoBandsExtractionTask
    class QuantumEspressoExecutionInput
    class WorkflowTaskBinding
    class AbstractSimulationDispatchEffect
    class LocalQuantumEspressoExecutor
    class AbstractResultObject
    class QuantumEspressoPwResult
    class QuantumEspressoBandsResult

    AbstractTask <|-- AbstractScientificTask
    AbstractScientificTask <|-- AbstractSimulationTask
    AbstractSimulationTask <|-- QuantumEspressoScfTask
    AbstractSimulationTask <|-- QuantumEspressoNscfTask
    AbstractSimulationTask <|-- QuantumEspressoBandPathTask
    AbstractSimulationTask <|-- QuantumEspressoBandsExtractionTask
    QuantumEspressoScfTask --> QuantumEspressoExecutionInput
    QuantumEspressoNscfTask --> QuantumEspressoExecutionInput
    QuantumEspressoBandPathTask --> QuantumEspressoExecutionInput
    QuantumEspressoBandsExtractionTask --> QuantumEspressoExecutionInput
    WorkflowTaskBinding --> AbstractSimulationTask
    WorkflowTaskBinding --> AbstractSimulationDispatchEffect
    AbstractSimulationDispatchEffect <|-- LocalQuantumEspressoExecutor
    AbstractResultObject <|-- QuantumEspressoPwResult
    AbstractResultObject <|-- QuantumEspressoBandsResult
```

## Quantum ESPRESSO roles

The implemented immutable `QuantumEspressoExecutionInput` contains or references exact
native QE input bytes and exact pseudopotential and predecessor-artifact identities.
It does not own the grouping, variable, or scientific policy used to form input text.
The integration-owned `QePwInputFile` preserves upstream-selected groups and
`QePwInputFileWriter` writes their native text without a provenance schema; workflow
composition may supply those exact retained bytes to an execution input. The initial
SCF, NSCF, band-path, and bands-extraction Tasks use this envelope without changing
artifact identity or scientific-policy ownership. Existing QE inputs and
pseudopotentials remain usable exact artifacts without rendering, conversion,
registration, rerun, or evidence reclassification.

The backend-neutral `AbstractPlaneWaveCalculator` is owned by
`ksdft2effmass.calculators.dft.pw` and supplies no execution authority. The distinct
Workflow `AbstractSimulationDispatchEffect` receives an authority-bearing dispatch
request. `LocalQuantumEspressoExecutor` implements the effect ABC rather than claiming
the calculator ABC's different call signature. Neither abstract boundary mutates
output state onto an input or Task.

Each operation-specific output is an immutable `AbstractResultObject` carrying mechanical
process outputs, calculator-reported and diagnostic observations, and
artifact/provenance identities. It may preserve an exact calculator-reported
completion, convergence, or failure statement, but it makes no independent
convergence, numerical-acceptance, scientific-acceptance, or human-disposition claim.
The new output is correlated in that Task instance's `WorkflowRun` result state.

SCF, NSCF, band-path, and bands-extraction definitions may be reused in multiple
Workflows by constructing new run-scoped Task instances with different exact inputs.
Reuse never means sharing a mutable `prefix`/`outdir`: a downstream Task receives an
immutable predecessor result and stages the identified native state into its own
isolated workspace, then produces a new state or extraction artifact identity. No
generic indirection layer or runtime plugin registry lies between a Task and its
explicitly injected executor.

## Task activation and authority

The Workflow adapter creates a discriminated `TaskActivation`: direct invocation has no gate-set or selected-gate identity, `any_of` identifies one deterministically selected gate/binding, and `all_of` identifies the canonical complete member gate/binding tuple. `SimulationExecutionRequest` then binds one exact operation-specific Task instance, TaskActivation, attempt, concrete executor taken from its validated `WorkflowTaskBinding`, already-bound `AbstractResultObject` inputs, grant, closed `SimulationExecutionAuthorizationResult`, and obligation scope; it does not embed generic `Simulation` or a multi-stage command list. Workflow control obtains one exact `authorized` result for the unused execution grant, verified authority snapshot, and immutable dispatch inputs before committing request, attempt, successor, grant reservation, and dispatch obligation as one supplied atomic unit. Immediately before the external process effect, the executor boundary independently obtains an exact `authorized` result for the same reserved grant, verified authority snapshot, activation/request/context, input artifacts, executable configuration, and resource limits, then performs one expected-revision compare-and-swap claim from `reserved` to `claimed`. Only the successful claimant proceeds.

```mermaid
flowchart LR
    activation["TaskActivation for one SCF, NSCF, band-path, or bands-extraction Task"] --> control["Workflow-control authority check"]
    input["Exact operation input and explicit context"] --> control
    control --> commit["AbstractWorkflowRunRepository atomic obligation commit"]
    commit --> executor_check["Independent executor-boundary authority check"]
    binding["WorkflowTaskBinding<br/>exact nominal effect"] --> executor_check
    executor_check --> executor["LocalQuantumEspressoExecutor<br/>through AbstractSimulationDispatchEffect"]
    executor --> effect["One bounded QE external effect"]
    effect --> output["New operation-specific AbstractResultObject"]
    output --> outcome["Confirmed SimulationDispatchOutcome envelope"]
    outcome --> ingress["TaskResultIngester admission and successor unit"]
```

One grant authorizes one exact dispatch bound to request, Task instance, TaskActivation, attempt, executor, authorization-result, claim, and obligation identities. SCF, NSCF, band-path, and bands-extraction therefore require four distinct activations, attempts, grants, process observations, result ingresses, and CPN firings even when one human checkpoint authorizes the bounded workflow. A claimed grant is consumed for authority purposes even when the external outcome is indeterminate. A retry or new execution requires new operation, activation, request, attempt, obligation, and grant identities. `SimulationDispatchOutcome` is the specialized dispatch envelope: confirmed contains the exact returned operation-specific `AbstractResultObject` and correlation identities, rejected contains failure and no output, and indeterminate contains no invented output and is not automatically redispatched. The envelope is not a second scientific result object. After reconciliation, workflow control constructs the corresponding candidate generic `TaskInvocationOutcome`; confirmed references the exact confirmed envelope and concrete output, while rejected or indeterminate references the matching dispatch without inventing results. For confirmed work, `TaskResultIngester` validates that correlation and atomically admits the output together with the generic outcome and result transition.

## Failure recovery and retry

A calculator-reported failure whose effect and output capture are determinate may be a
typed `AbstractResultObject` inside confirmed dispatch. Confirmation establishes effect and
capture certainty, not successful calculator completion. Application composition maps
operation-specific result facts into generic CPN values; only a result satisfying its
explicit continuation-admission contract can satisfy a downstream Task gate.

Retry control is represented by the Workflow-owned CPN composition. A failure or
unresolved-diagnostic value leads to an explicit recovery-required state. An admitted
resolution may enable either reevaluation of the retained result or a retry-intent
transition. The generic CPN enabler, selector, and firer remain effect-free: they do
not invoke a calculator, modify inputs, wait, or reuse authority. Workflow control
performs any newly enabled effect only after constructing new activation, operation,
attempt, request, obligation, and grant identities and completing the applicable
fresh authorization and dispatch sequence.

The failed attempt, its diagnostic result, and its resolution dependency remain in
ordered Workflow history. A retry never mutates or replaces them. A diagnostic
reclassification may make an otherwise completed retained result admissible without a
new scientific effect; a changed input, execution context, executable configuration,
or scientific setting requires a new exact execution attempt. Every retry topology
has an explicit abandon or bounded-exhaustion path and no direct automatic
failure-to-execution edge. The accepted QE-specific ownership and diagnostic mapping
are recorded in the
[QE diagnostic outcome and retry decision](../calculators/quantum-espresso-diagnostic-outcome-decision.md).

## Exact artifacts and non-equivalence

Same labels, methods, cutoff values, pseudopotential families or assets, or settings across implementations do not establish equivalence. PAW, ultrasoft, and norm-conserving assets; valence/core choices; generation settings; exchange-correlation compatibility; relativistic treatment; projector construction; recommended cutoffs; and formats remain exact represented inputs. Equivalence would require a separately authorized evidence-bearing comparison or validation claim.

External, imported retained, human-authored, and bounded legacy ResultObjects and artifacts retain their actual producer-provenance variant. They may enter a Workflow without fabricated Task lineage or recalculation.

## Normalization path

After `TaskResultIngester` validates the confirmed envelope and candidate generic outcome, admits the returned operation-specific `AbstractResultObject`, and atomically commits the outcome, result transition, and result ingress, explicitly composed native parsers and adapters may map retained native records to `NormalizedObservationSet`, followed by deterministic scientific analysis. Any diagnostic classification required to construct the operation-specific QE result occurs at the integration boundary before that result is returned; richer native parsing and neutral normalization remain post-ingress operations. Human-reviewed conclusions remain external research records. Mechanical execution success does not imply convergence or scientific acceptance.

The project-relevant multi-executable composition is defined by the
[QE--Wannier90 CPN workflow](qe-wannier90-cpn-workflow.md). That CPN owns
artifact-availability dependencies and joins without moving executable behavior
or scientific policy into the generic Petri-net package.

## Package boundary and status

Backend-neutral plane-wave DFT specification, binding, and executor-port contracts belong under `ksdft2effmass.calculators.dft.pw`. QE Task, Simulation, native input/output, configuration, process and diagnostic observations, serialization, staging, workspace/process invocation, native parsing, artifact discovery, failure mapping, and observation adaptation belong to `ksdft2effmass.integration.quantum_espresso`. Application composition injects that concrete implementation; calculators and workflows never import it.

The bounded private fields selected by the
[DFT simulation CPN service decision](dft-simulation-cpn-service-decision.md) apply
only to its retained-result architecture probe. The private
`ksdft2effmass.workflows._dft_scf_nscf_dos` slice implements only the effect-free
composition of three distinct reusable Task-definition identities and their CPN
transitions. Private `QuantumEspressoNscfInput`, `QuantumEspressoDosInput`, and their
mechanical result variants now preserve the bounded exact identities required by the
probe. Neither private slice owns the public QE Task classes, native-state handoff, or
result ingress described on this page. The canonical QE package separately implements
the four selected Task adapters, their immutable Simulation composition, initial
public in-memory execution fields, local executor, and Workflow dispatch effect; its
terminal and workspace-snapshot wires remain integration-private. Durable public wire
contracts, asynchronous interfaces, scheduler adapters, additional operation Task
adapters including DOS, and supported real-QE operation policy remain deferred.
