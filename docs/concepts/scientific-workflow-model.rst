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
only child identities, terminal observation, replay-equal child result identity, and
explicit exported-result admissions. It never embeds the child marking or transition
history, and membership alone does not admit a child result.

Scientific execution records retain externally supplied grant, snapshot, authorization,
reservation, claim, request, dispatch outcome, obligation, and disposition identities.
They are control state only: their constructors and replay perform no authorization,
authentication, reservation, dispatch, reconciliation, or other effect. A confirmed
specialized dispatch does not substitute for represented Task outcome and production
closure.

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
schema, persistence repository, dispatch Action, reconciliation Action, result-ingress
Action, scientific analysis, scientific validation, uncertainty quantification, or
acceptance state. Constructor and replay tests are software verification only.
