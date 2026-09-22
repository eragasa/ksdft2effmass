Scientific Task and Workflow model
==================================

The public :mod:`ksdft2effmass.workflows` model separates scientific operation
contracts and represented WorkflowRun state from generic colored-Petri-net mechanics,
external execution, and persistence. It is a software-composition and deterministic
reconstruction contract, not a claim that a calculation ran or that a result is
scientifically valid.

Results and Tasks
-----------------

A ``ResultObject`` is an immutable workflow-facing result protocol.  Each
scientific domain owns its concrete result fields, units, provenance, and
intrinsic invariants.  ``ResultObjectIdentity`` is owner-local and nominal; the
model selects no digest, canonical encoding, or wire format.

A ``Task`` is a structural ActionObject protocol.  Its accepted call boundary is

.. code-block:: python

   execute(
       inputs: tuple[TaskInputBinding, ...],
       context: TaskExecutionContext,
   ) -> tuple[ResultObject, ...]

Inputs are already-bound results with unique names and identities.  Context
identifies the Workflow definition, represented run, run-scoped Task instance,
activation, intended operation, and attempt.  Context supplies correlation only:
it grants no execution authority.  The Task neither discovers prerequisites nor
constructs a durable invocation outcome.

A ``Workflow`` implements ``Task`` structurally and therefore may be nested.
This model records its immutable composition but does not create the distinct
child ``WorkflowRun`` required by a later invocation boundary.

Normalized observation assembly
--------------------------------

After concrete integration extraction, ``NormalizedObservationAssembler`` accepts a
nonempty tuple of exact immutable ``NormalizedObservationSource`` ResultObjects. The
protocol exposes one unchanged schema-version-1 neutral plane-wave Kohn--Sham record,
Workflow artifact and producer identities, source-domain parser and policy identities,
and explicit limitations. It is calculator-independent: Workflow imports the neutral
record contract but no calculator or integration package.

``NormalizedObservationSet`` is a Workflow-owned ResultObject retaining the exact
source objects in caller-declared order. Its result identity must differ from every
source-result identity; source-result identities and exact manifest-revision/entry
pairs must be unique; parser and policy identities and
versions must be nonempty, limitations must be nonempty, unique, and lexically
ordered, and neutral provenance SHA-256 and
byte count must agree with the represented source content identity. Empty or invalid
source sets return a closed ``NormalizedObservationAssemblyFailure`` containing the
exact request and no partial set.

Assembly does not parse native output, convert units, alter the neutral record, resolve
artifacts, persist state, execute a calculator, or establish convergence, numerical
verification, scientific validation, uncertainty quantification, or acceptance.

Composition and start gates
---------------------------

``WorkflowComposition`` contains unique run-scoped ``TaskInstance`` records.
Each instance has zero or one ``TaskStartGateSet``.  The gate set uses exactly
``any_of`` or ``all_of`` composition and may contain zero members.  No gate set
and an empty gate set both provide no automatic activation.

Each gate identifies one generic colored-Petri-net transition and has a
nonnegative integer priority.  Storage order is retained but is not selection
order.  Deterministic member order is ascending priority followed by stable gate
identity.  Start gates are Workflow composition policy and remain separate from
the concrete Task input contract.

Discriminated activation
------------------------

``TaskActivation`` binds the exact Workflow, represented run, Task instance,
operation, attempt, already-bound inputs, and generic selection-result identity.
Its selection is exactly one of:

``direct``
   Carries no gate-set or selected-gate identity.  It is valid only for an
   instance with no gate set or an empty gate set.

``any_of``
   Identifies the instance's exact ``any_of`` gate set and one member gate whose
   generic binding uses the gate's transition.

``all_of``
   Identifies the instance's exact ``all_of`` gate set and one binding for every
   member in canonical priority-then-identity order.

Construction verifies these intrinsic correlations.  It does not establish
colored-Petri-net enablement, choose a binding, invoke a Task, authorize an
effect, or persist Workflow state.

Effect-free colored-Petri-net adapter
-------------------------------------

``ColoredPetriNetWorkflowAdapter`` owns the implemented activation-selection
boundary.  It consumes one immutable ``ColoredPetriNetWorkflowMapping``, an exact
generic definition and predecessor marking, already-bound Task inputs, and explicit
``WorkflowResultTokenMapping`` records.  Each result-token mapping correlates one
result identity and Task input name with one generic binding variable and an
individually identified generic token at one exact place.  Candidate binding values
must equal the mapped token values.  This is supplied correlation data, not an
inferred scientific value conversion.

The Workflow mapping independently controls whether a noncanonical generic selection
is permitted.  The generic definition must also permit directed selection; neither
policy can override the other.  Automatic ``any_of`` selection uses gate priority,
gate identity, and then generic binding order.  Automatic ``all_of`` selection takes
the first mutually compatible complete member tuple, merges equal shared-variable
assignments, and orders the combined binding by the explicitly mapped activation
transition.  Direct activation requires one explicit mapped transition and binding.

The closed adapter result is ``activated``, ``not_enabled``, or ``failure``.  It
retains the complete generic enablement result, any generic selection result, a
content identity, and a ``TaskActivation`` only for ``activated``.  ``not_enabled``
is an expected absence of activation rather than an execution failure.  Mapping,
enablement, permission, selection, and correlation defects fail closed without
constructing an activation.

The adapter does not derive scientific values from ResultObjects, invoke the Task,
construct a durable invocation outcome, fire the selected transition, mutate the
marking, schedule work, persist state, or grant execution authority. Those remain
separate boundaries.

Replayable WorkflowRun state
----------------------------

``WorkflowRun`` is an immutable snapshot-plus-history aggregate for one represented
Workflow execution. All Workflow executions use colored-Petri-net semantics; there is
no alternate DAG-backed run implementation or generic run protocol. The concrete run
DataObjects and replay ActionObject are owned by ``ksdft2effmass.workflows.runs``, while
supported user imports remain available from ``ksdft2effmass.workflows``.

The aggregate binds a stable ``WorkflowRunIdentity`` and immutable revision
to one ``WorkflowDefinitionReference``, one ``WorkflowRuntimeBundleIdentity``, exact
initial and current colored-Petri-net markings, and canonically ordered record tuples.
The definition reference names explicit Workflow, colored-Petri-net, Task-definition,
and schema versions. It contains no executable closure and does not discover a latest
version.

Task-origin history contains ordinary membership, Task activations, append-only attempt
state, closed invocation outcomes, failures, result references, result production, and
explicit dependencies. Multiple ``TaskAttempt`` records may share one stable
``AttemptIdentity`` while retaining distinct state-record identities. A later state
names its immediate state predecessor. A retry uses new activation, operation, and
attempt identities and names one earlier terminal attempt; stale, branching, or
cross-Task retry predecessors fail replay correlation.

Every ``ResultObjectReference`` records concrete type, owning domain, immutable content,
and one closed producer variant. Represented Task and scientific-decision producers
carry exact run-specific lineage. External, imported-retained, human-authored, and
unknown-legacy producers instead retain actual evidence identities and explicit
limitations. Those variants prevent missing historical lineage from being fabricated.
A ``ResultDependency`` records consumption independently of ordinary or nested
membership. A confirmed Task transition closes over all outcome results, production
records, and the exact generic external-output binding.

A nested invocation always identifies a distinct child WorkflowRun. The parent stores
immutable intent and a separate first-terminal observation, with replay-equal child
result identity and explicit admissions only for confirmed exports. An actual
retained combined pending invocation can be the unchanged intent source. The terminal
group requires that source in the actual predecessor; no historical intent is
invented and no second terminal is introduced, including after indeterminate.
The parent never embeds child marking or transition history, and membership alone
does not admit a child result. This remains a schema-version-1 contract.

Scientific execution records retain externally supplied grant, snapshot, authorization,
reservation, claim, request, durable dispatch entry, append-only dispatch observation,
final dispatch outcome, obligation, and disposition identities.
Their constructors and replay are effect-free. ``SimulationExecutionAuthorizer``
compares an exact grant and verified snapshot with either preparation-phase unused
state or claim-phase state reserved to the same obligation. It returns separate
``authorized``, ``denied``, and ``error`` results but issues no authority, reservation,
or claim.

``SimulationDispatchPreparer`` first requires a replay-equal predecessor, evaluates
preparation-phase authority, constructs the complete activation, started-attempt,
closed-authorization, correlation, reservation, and obligation record group, and
requires the resulting candidate to replay equally. ``SimulationDispatchClaimPreparer``
then evaluates a distinct claim-phase authorization and constructs a successor with an
append-only claim over the exact prepared revision. Neither ActionObject persists its
candidate. A typed ``WorkflowRunClaimCommitReceipt`` supplied by the persistence owner
must identify the committed claimed revision, its predecessor, claim record,
authorization result, content, operation, idempotency key, and implementation. On every
authorization-valid, exactly correlated adapter invocation, a persistence-owned
``SimulationDispatchEntryCommitter`` attempts
the separate ``claimed`` to ``dispatch_entered`` compare-and-swap. Only its newly
successful result commits a ``SimulationDispatchEntry``, carries a correlated
``SimulationDispatchEntryReceipt``, and permits effect entry; duplicate, stale, losing, or erroneous results perform no effect. Compare-and-
swap implementation and receipt production remain separately owned.

The architecture-facing ``SimulationDispatchEffect`` protocol is supplied by
application composition. ``SimulationDispatchAdapter`` repeats claim-phase
authorization, checks the exact prepared request, represented successful claim,
obligation, executor, and newly won dispatch-entry receipt, and enters that effect at
most once. A denial, already-entered result, or pre-effect correlation error performs
no effect. A mismatched outcome after effect entry is
indeterminate. An unexpected effect exception propagates and provides neither a
no-effect claim nor automatic retry authority. Applications may
wrap this software-architecture surface in their own physicist-facing APIs. Workflow
control imports no calculator or integration implementation. A confirmed runtime
outcome carries its concrete immutable ``ResultObject`` and exact native-output
manifest references, but does not substitute for later represented Task outcome,
production, generic firing, atomic ingress, or scientific acceptance. The effect-free
``SimulationDispatchReconciler`` reduces exact repeated observations to confirmed,
rejected, indeterminate, conflict, or error without invoking an effect or selecting a
retry.

``SimulationDispatchResultIngressPreparer`` always appends the reconciliation's
``DispatchObservationRecord``. An indeterminate, conflict, or error observation appends
no terminal attempt, generic outcome, final ``DispatchOutcomeRecord``, disposition, or
transition, so the original started attempt and obligation remain pending. One later
confirmed or rejected observation may supply the sole closed terminal record group.
Confirmed ingress requires the concrete result, generic production and reference, one
dispatch-specific ``NativeOutputAdmission``, a successful CPN transition, and one
initial confirmed obligation disposition. The distinct trigger for a later completed
disposition remains deferred. Rejected ingress requires the exact runtime failure and
one rejected disposition. The ActionObject appends those records to an immutable
successor and requires deterministic replay equality; it neither reads native files nor
persists the candidate. ``ResultProductionRecord`` therefore remains generic, while
``NativeOutputAdmission`` alone correlates a confirmed dispatch envelope and production
to the exact supplied native manifest and admitted entries.

Scientific-decision ingress has its own transition origin. Its request identifies the
affected Workflow branch and required response-source and authority-context identities.
Its resolution is an immutable ``ResultObject`` with verbatim and normalized response
state plus no-Task producer provenance. The transition's generic output binding must
contain exactly one string-valued assignment equal to the selected option's value.
Corrections consume the exact effective predecessor;
stale or concurrent branches fail closed. No Task instance, activation, operation, or
attempt is fabricated for decision ingress.

Deterministic replay
--------------------

``WorkflowRunReplayer`` is an effect-free ActionObject. It accepts exactly one
``WorkflowRun`` and one explicitly supplied ``WorkflowRuntimeBundle``. The current
implementation supports WorkflowRun schema version 1, Workflow-definition version 1,
and colored-Petri-net definition version 1. After checking those versions plus the
supported adapter, evaluator, ordering, enablement, selection, and
firing identities, it validates aggregate correlations and applies task-origin and
scientific-decision-origin firing inputs in one zero-based canonical sequence. It
invokes only the pure generic transition firer; it never invokes a Task or external
system.

The closed ``WorkflowRunReplayResult`` outcomes have distinct claim boundaries:

``equal``
   Complete replay reconstructed the exact retained current marking and reports no
   issue.

``unequal``
   Replay completed, but the reconstructed marking differs from the retained current
   marking. The reconstructed marking is retained for comparison.

``unsupported_version``
   A required schema, definition, adapter, or implementation identity is mismatched or
   unsupported. No reconstructed marking is claimed.

``error``
   Correlation, ordering, predecessor, selection, or pure-firing reconstruction failed.
   No reconstructed marking is fabricated.

Replay equality establishes deterministic agreement with the represented software
history only. It does not establish that a Task executed, that an external effect
occurred, that a parent physical model is adequate, or that any result is scientifically
validated.

Exclusions and evidence
-----------------------

The public Workflow model defines no calculator implementation, serializer, wire
schema, persistence repository, persistence-backed atomic result ingester, scientific
analysis, scientific validation, uncertainty quantification, or acceptance state. Its
result-ingress preparer constructs and replay-checks candidates only. The dispatch
adapter invokes only an explicitly injected synthetic or application-owned effect port;
it implements no calculator. Constructor, authorization,
and synthetic dispatch tests are software verification only.
