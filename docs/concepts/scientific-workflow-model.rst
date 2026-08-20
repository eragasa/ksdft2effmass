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
effect, or persist Workflow state.  Those responsibilities belong to later
adapter, control, run, and persistence boundaries.

Exclusions and evidence
-----------------------

The model defines no calculator implementation, serializer, schema, repository,
WorkflowRun aggregate, dispatch, reconciliation, result ingress, scientific
analysis, validation, uncertainty quantification, or acceptance state.  Its
constructor and protocol tests are software verification only.
