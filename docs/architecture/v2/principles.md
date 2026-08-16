# Architecture v2 principles

1. Development `HarnessTask` state and scientific `WorkflowRun` state are separate.
2. `ResultObject` instances, not producer Task objects, are workflow inputs and prerequisites.
3. `Task` is structural and consumes already-bound results plus explicit context.
4. `Workflow` implements Task and may be nested.
5. Run-scoped Task instances and Workflow-owned start gates are distinct from reusable Task definitions.
6. Parent/child membership and ResultObject dependency are orthogonal.
7. Generic colored-Petri-net mechanics are separate from Workflow effects and records.
8. DataObjects and ResultObjects are immutable; effects belong to target-first ActionObjects.
9. Shared persistence stores opaque complete revisions; domain repositories own aggregate validation, serialization, and commit closure through composition.
10. Authority is explicit and never inferred from scheduling, process success, or a terminal marking.
11. Exact artifact identity and provenance are retained without fabricated lineage or recalculation.

## Generic colored Petri net

`ksdft2effmass.petrinet.colored` owns only generic values and pure enablement, deterministic selection, and firing. Selection applies definition-owned total priority, canonical transition identity, and canonical binding order, with no fairness guarantee. The package performs no external effects and imports no workflows.

## Task and Workflow composition

A Task instance has zero or one immutable Workflow-owned `TaskStartGateSet` in `any_of` or `all_of` mode. `TaskActivation` is discriminated as direct, any_of, or all_of; direct carries no gate identity, any_of selects one enabled gate deterministically by stable priority then identity, and all_of records the canonical compatible tuple across every member. Start gates are composition policy, not Task prerequisites.

`ColoredPetriNetWorkflowAdapter` maps Workflow gates and ResultObject token values to generic inputs, constructs `TaskActivation`, remains effect-free while workflow control/dispatch invokes Tasks across accepted authority, maps supplied returned ResultObjects into the immutable external-output-value binding of `ColoredPetriNetFiringInput`, and requests pure firing. The generic firer evaluates all inscriptions, validates produced tokens, and returns successor plus audit facts. Workflow control constructs transition and WorkflowRun records separately.

Start-gate policy states when a Workflow permits a Task instance to execute. The Task input contract states what its execute operation accepts. Gates may be stricter but cannot omit or mismatch required Task inputs.

## Simulation composition

`Simulation` is structural. A concrete `SimulationTask` is a Task. The calculator-owned QE composite is `QuantumEspressoSimulation`, used by `QuantumEspressoSimulationTask`, with exact immutable `QuantumEspressoInput`, a consumer-owned structural `QuantumEspressoExecutor` protocol, and a newly returned immutable `QuantumEspressoOutput` ResultObject. Application composition injects the concrete `integration.quantumespresso` executor implementation; calculators and workflows never import it. Output is not mutated onto a pre-execution object.

## Effect and repository boundaries

`ksdft2effmass.persistence` provides immutable revision values, a structural single-stream `AtomicRevisionStore`, and the initial standard-library `SQLiteAtomicRevisionStore`. Harness and workflow repositories remain domain-owned, bind their exact validators and serializers to the committed bytes, and compose the shared store. There is no generic CRUD repository or persistence inheritance hierarchy. Separate development and scientific SQLite stores/databases are the default; shared implementation does not imply shared physical state or cross-stream transactions.

One exact grant authorizes one exact dispatch. Workflow control and the executor boundary independently check the same immutable authority and effect inputs. Workflow services construct complete candidate successor and obligation units; domain repositories invoke their bound validators and serializers on those exact candidates and verify identity binding before the shared store atomically commits one opaque aggregate revision in one stream. Repositories do not select gates, invoke Tasks, fire generic transitions, or create authority, and an indeterminate commit is never guessed.

Indeterminate external outcomes remain represented. Confirmed result ingress records exact native-output and manifest identities without copying or publishing calculator-produced files; extraction is an explicit read-only transformation over those outputs. Scientific analysis produces findings with explicit claim boundaries; human-reviewed conclusions remain external research records and are not workflow state.

## Claim boundaries

A structural or software check establishes only its declared contract. Process success is not convergence. Exact byte identity is not scientific compatibility. Shared methods, cutoffs, pseudopotential labels/assets, or settings do not establish equivalence. Scientific validation, uncertainty quantification, equivalence, and human acceptance require their own evidence and authority.
