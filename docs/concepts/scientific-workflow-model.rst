Scientific Task and Workflow model
==================================

The public :mod:`ksdft2effmass.workflows` model separates scientific operation
contracts from generic colored-Petri-net mechanics and from external execution.
It is a software-composition contract, not a claim that a calculation ran or
that a result is scientifically valid.

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
marking, schedule work, persist state, or grant execution authority.  Those remain
separate later boundaries.

Exclusions and evidence
-----------------------

The model defines no calculator implementation, serializer, schema, repository,
WorkflowRun aggregate, dispatch, reconciliation, result ingress, scientific
analysis, validation, uncertainty quantification, or acceptance state.  Its
constructor and protocol tests are software verification only.
