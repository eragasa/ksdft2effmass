# Quantum ESPRESSO task-contract boundary decision

## Problem

**Observed fact.** The active Task must choose the public taxonomy, names, and
ownership of Quantum ESPRESSO (QE) ``SimulationTask`` and ``Simulation`` contracts
before implementation.

**Human choice.** The central question is whether public tasks represent QE
executable roles, scientific operations, or parameterized operation definitions.

## Observed current behavior

**Observed fact.** Workflow ``Task`` is a structural ActionObject for one reusable
scientific operation in ``ksdft2effmass.workflows.model``.

**Observed fact.** ``PlaneWaveCalculator[InputT, OutputT]`` is the existing
backend-neutral execution port in ``ksdft2effmass.calculators.dft.pw``.

**Observed fact.** Current QE execution types are executable-oriented:
``QuantumEspressoProgram`` has ``PW`` and ``BANDS`` roles, with corresponding
``QuantumEspressoPwResult`` and ``QuantumEspressoBandsResult`` records in
``ksdft2effmass.integration.quantum_espresso``.

**Observed fact.** ``LocalQuantumEspressoExecutor`` already owns the concrete
one-attempt effect and Workflow dispatch adaptation. Workflow retains authority,
history, result ingress, and retry control.

**Observed fact.** The pre-decision simulation-task architecture described SCF,
NSCF, and DOS Task adapters as prospective roles rather than accepted public names.

**Inference.** Executable roles and scientific operations are not equivalent:
``pw.x`` can perform SCF, NSCF, relaxation, and band-path operations with different
predecessor and continuation contracts.

## Decision requirements

**Accepted requirement.** QE-specific contracts belong in
``ksdft2effmass.integration.quantum_espresso``; generic plane-wave contracts remain
in ``ksdft2effmass.calculators.dft.pw``.

**Accepted requirement.** One Workflow Task represents one reusable scientific
operation and returns immutable ``ResultObject`` values.

**Accepted requirement.** No option may introduce a backend registry, generic QE
facade, authority service, retry policy, process implementation, or public
persistence format.

**Accepted requirement.** Existing executable-oriented input, process, diagnostic,
and result records remain valid mechanical evidence.

**Human choice resolved.** The human selected operation-specific public Task
contracts through the response ``B``.

## Option A

**Conceptual model**
Public adapters follow executables: ``QuantumEspressoPwTask`` and
``QuantumEspressoBandsTask``, with matching executable-oriented simulations.

**Authority**
Workflow authority remains unchanged; program selection comes from
``QuantumEspressoProgram``.

**Ownership/dependency**
Tasks remain QE-integration-owned and depend inward on ``PlaneWaveCalculator`` and
Workflow protocols.

**Runtime/dispatch**
Each adapter validates ``PW`` or ``BANDS`` and delegates to the existing executor.

**Migration**
Add thin wrappers around current execution inputs and result types; no compatibility
aliases are needed.

**Reversibility**
Easy initially, but later splitting ``QuantumEspressoPwTask`` into scientific
operations would change public contracts.

**Failures**
Executable mismatches fail locally; scientific-operation mismatches must be detected
by application policy or identities.

**Complexity**
Lowest initial type and implementation count.

**Maintenance**
Simple for executor changes, but mode-specific constraints become scattered.

**Context-window consequences**
Smallest immediate review surface.

**Future compatibility**
Easy to add executables; weak representation of differing operations performed by
one executable.

**Advantage**
Matches the current ``PW``/``BANDS`` input and result taxonomy closely.

**Risk**
Treats an executable as a scientific Task and obscures SCF, NSCF, relaxation, and
band-path dependency semantics.

## Option B

**Conceptual model**
Public adapters represent scientific operations. The initial set is
``QuantumEspressoScfTask``, ``QuantumEspressoNscfTask``,
``QuantumEspressoBandPathTask``, and ``QuantumEspressoBandsExtractionTask``. Each
uses an immutable operation-specific simulation composition while retaining
``QuantumEspressoPwResult`` or ``QuantumEspressoBandsResult`` as mechanical
execution evidence. DOS remains deferred until its executable/result boundary
exists.

**Authority**
Workflow selects and authorizes one exact operation. Executable selection remains an
integration detail constrained by the Task contract.

**Ownership/dependency**
Operation-specific adapters and simulation compositions belong in
``integration.quantum_espresso``; generic Workflow and plane-wave packages import no
QE types.

**Runtime/dispatch**
Each Task admits only its exact inputs and predecessor results, then delegates one
effect through the existing calculator/executor boundary. Multi-stage work remains
Workflow composition.

**Migration**
Add new public adapters without replacing existing inputs, results, or executor
behavior. No historical Task lineage or compatibility alias is fabricated.

**Reversibility**
Shared private mechanics can later be factored without changing public operation
names.

**Failures**
Wrong predecessor kinds, program bindings, or result correlations fail at the narrow
operation boundary.

**Complexity**
Moderate: more explicit classes and tests than Option A.

**Maintenance**
Each operation owns its own invariant set; adding an operation requires a deliberate
new contract.

**Context-window consequences**
Review can stay localized to one operation instead of loading all ``pw.x`` modes.

**Future compatibility**
Extends to relaxation, DOS, dielectric, and other operations only when their actual
contracts exist.

**Advantage**
Matches the accepted meaning of Workflow Task and makes scientific dependencies
explicit without changing mechanical result evidence.

**Risk**
Can produce excessive public classes if operations are added speculatively rather
than from demonstrated workflows.

## Option C

**Conceptual model**
Publish one generic ``QuantumEspressoSimulationTask[InputT, ResultT]`` and one
``QuantumEspressoSimulation``, parameterized by a closed
``QuantumEspressoOperationDefinition``.

**Authority**
Application composition supplies the exact operation definition; Workflow still
owns authorization and dispatch.

**Ownership/dependency**
The generic QE Task and operation-definition variants remain integration-owned.

**Runtime/dispatch**
The operation definition selects allowed program, input, predecessor, and result
combinations before delegation.

**Migration**
Add an operation-definition hierarchy over current records and create instances for
SCF, NSCF, band path, and bands extraction.

**Reversibility**
Concrete adapters could later wrap the generic Task, but the generic public contract
would remain a compatibility obligation.

**Failures**
Invalid definition/type combinations require central discriminant validation and
closed failure results.

**Complexity**
Highest initial generic typing and validation complexity.

**Maintenance**
Fewer public Task classes, but one central definition model accumulates every
operation rule.

**Context-window consequences**
Changes often require loading the generic Task, operation variants, typing, and
dispatch logic together.

**Future compatibility**
New operations may be added as variants without new Task classes.

**Advantage**
Avoids public class proliferation while preserving explicit operation identities.

**Risk**
May become a QE mini-registry or generic facade and shift compile-time distinctions
into runtime discriminant logic.

## Three-option comparison

**Observed comparison.** All three options preserve Workflow-owned authority and
history, integration-owned QE behavior, immutable state, and the absence of a public
persistence format.

| Criterion | Option A | Option B | Option C |
|---|---|---|---|
| Matches scientific Task semantics | Weak | Strongest | Strong |
| Reuses current executable records | Strongest | Strong | Strong |
| Explicit predecessor contracts | Weak | Strongest | Strong |
| Initial complexity | Lowest | Moderate | Highest |
| Risk of premature abstraction | Low | Moderate | Highest |
| Risk of public type proliferation | Low | Highest | Low |
| Local reviewability | Moderate | Strongest | Weak |
| Future operation growth | Executable-centered | Deliberate contracts | Central variants |

## Recommendation

**Recommendation.** Option B: operation-specific Task adapters.

**Inference.** Option B best preserves the accepted distinction between a scientific
operation, a QE executable invocation, and a mechanical result. It also keeps failure
and predecessor rules local and reviewable.

**Implementation consequence.** The first implementation child covers only SCF,
NSCF, band-path calculation, and bands extraction. DOS and other operations remain
deferred until their concrete execution/result boundaries exist.

## Deferred questions

**Deferred question.** Whether operation-specific simulation compositions should
become public independently of their Task adapters; the initial implementation may
keep them narrowly exposed.

**Deferred question.** Public serialization, scheduler interfaces, real-QE
diagnostic signatures, retry topology, and additional executables.

**Deferred question.** Scientific acceptance criteria for SCF, NSCF, or band results;
these do not belong to this software-contract decision.

## Human decision required

**Human response.** ``B``.

**Normalized decision.** Option B: use operation-specific SCF, NSCF, band-path, and
bands-extraction Task contracts under
``ksdft2effmass.integration.quantum_espresso`` while retaining existing
executable-oriented result records as mechanical evidence.

**Implementation consequence.** The decision is resolved, but the dependent
implementation child remains blocked until this decision Task receives separately
authorized administrative closeout. No implementation or automatic successor
activation follows from this selection.
