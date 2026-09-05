Scientific Workflow model
=========================

Use the package-level imports documented here.  These contracts represent
calculator-independent scientific composition; they do not invoke Tasks,
execute calculators, persist Workflow runs, or establish scientific validity.
Generic colored-Petri-net contracts remain under
:mod:`ksdft2effmass.petrinet.colored`.

Protocols
---------

.. currentmodule:: ksdft2effmass.workflows

.. autoclass:: ResultObject
   :members:

.. autoclass:: Task
   :members:

.. autoclass:: Workflow
   :members:

Identities and operation inputs
-------------------------------

.. autoclass:: ResultObjectIdentity
.. autoclass:: TaskDefinitionIdentity
.. autoclass:: TaskInstanceIdentity
.. autoclass:: WorkflowIdentity
.. autoclass:: WorkflowRunIdentity
.. autoclass:: TaskStartGateIdentity
.. autoclass:: TaskStartGateSetIdentity
.. autoclass:: TaskActivationIdentity
.. autoclass:: OperationIdentity
.. autoclass:: AttemptIdentity
.. autoclass:: TaskInputBinding
.. autoclass:: TaskExecutionContext

Workflow-owned artifacts and producer provenance
------------------------------------------------

The closed ``ArtifactProducerProvenance`` type union contains exactly the five
concrete producer records below.  Concrete type and ``ArtifactProducerKind`` must
agree.  These Workflow-owned identities are not aliases of equal-looking records
under :mod:`ksdft2effmass.provenance`.

.. autoclass:: ArtifactIdentity
.. autoclass:: ArtifactManifestIdentity
.. autoclass:: ArtifactManifestEntryIdentity
.. autoclass:: ArtifactManifestSupersessionIdentity
.. autoclass:: ArtifactProducerProvenanceIdentity
.. autoclass:: ResultArtifactRelationIdentity
.. autoclass:: ArtifactContentIdentity
.. autoclass:: ArtifactProducerKind
   :members:
.. autoclass:: ArtifactLineageRelationIdentity
.. autoclass:: ArtifactLineageSourceIdentity
.. autoclass:: ArtifactLineageKind
   :members:
.. autoclass:: ArtifactLineageRelation
.. autoclass:: RepresentedWorkflowProducer
.. autoclass:: ExternalSourceObservation
.. autoclass:: ImportedRetainedFixture
.. autoclass:: HumanAuthoredCompactInput
.. autoclass:: UnknownLegacyProducer
.. autoclass:: ArtifactManifestEntry
.. autoclass:: ArtifactManifest

See :doc:`../concepts/workflow-artifacts` for manifest closure, migration, and
evidence boundaries.

Composition and gates
---------------------

.. autoclass:: TaskStartGateSetMode
   :members:

.. autoclass:: TaskStartGate
.. autoclass:: TaskStartGateSet
   :members:
.. autoclass:: TaskInstance
.. autoclass:: WorkflowComposition

Activation selections
---------------------

``TaskActivationSelection`` is the public union of the three selection records
below.  Using separate records prevents gate-only fields from appearing on a
direct activation.

.. autoclass:: DirectTaskActivationSelection
.. autoclass:: AnyOfTaskActivationSelection
.. autoclass:: AllOfTaskActivationSelection
.. autoclass:: TaskGateSelection
.. autoclass:: TaskActivation

Effect-free colored-Petri-net adaptation
----------------------------------------

The adapter consumes explicit immutable Workflow-owned mapping data and a supplied
predecessor marking.  It may return an activation selection, but it never invokes a
Task or fires a transition. The WorkflowRun records below retain successful firing
inputs and results; replay does not call this adapter or invoke a Task.

.. autoclass:: ColoredPetriNetWorkflowSelectionPolicy
   :members:
.. autoclass:: ColoredPetriNetWorkflowActivationMode
   :members:
.. autoclass:: WorkflowResultTokenMapping
   :members:
.. autoclass:: ColoredPetriNetWorkflowMapping
.. autoclass:: ColoredPetriNetWorkflowActivationRequest
.. autoclass:: ColoredPetriNetWorkflowActivationOutcomeKind
   :members:
.. autoclass:: ColoredPetriNetWorkflowActivationFailureCode
   :members:
.. autoclass:: ColoredPetriNetWorkflowActivationResultIdentity
.. autoclass:: ColoredPetriNetWorkflowActivationResult
   :members:
.. autoclass:: ColoredPetriNetWorkflowAdapter
   :members:

Replayable WorkflowRun aggregate
--------------------------------

``WorkflowRun`` is one concrete colored-Petri-net-semantic immutable
snapshot-plus-history aggregate. Its implementation is organized under
``ksdft2effmass.workflows.runs`` and its supported public names are re-exported from
``ksdft2effmass.workflows``. Its records are calculator-independent and effect-free.
``WorkflowRunReplayer`` receives an exact runtime bundle, reconstructs the marking
sequence with pure colored-Petri-net firing,
and returns a closed replay result. See
:doc:`../concepts/scientific-workflow-model` for ordering, provenance, result-flow,
nesting, control-state, and claim-boundary details.

.. autoclass:: WorkflowDefinitionReferenceIdentity
.. autoclass:: WorkflowDefinitionReference
.. autoclass:: WorkflowRuntimeBundleIdentity
.. autoclass:: WorkflowRuntimeBundle
.. autoclass:: WorkflowRunRevisionIdentity
.. autoclass:: WorkflowRun
.. autoclass:: WorkflowRunReplayResultIdentity
.. autoclass:: WorkflowRunReplayOutcomeKind
   :members:
.. autoclass:: WorkflowRunReplayIssueCode
   :members:
.. autoclass:: WorkflowRunReplayIssue
.. autoclass:: WorkflowRunReplayResult
.. autoclass:: WorkflowRunReplayer
   :members:

Task state, transitions, and nested runs
----------------------------------------

Task-origin state is append-only. One stable ``AttemptIdentity`` may have multiple
state records, each with a distinct ``TaskAttemptRecordIdentity``. Parent runs retain
only child identities, observations, and explicit export admissions; child markings
and histories remain in the child aggregate.

.. autoclass:: TaskWorkflowMembershipIdentity
.. autoclass:: TaskWorkflowMembership
.. autoclass:: TaskAttemptRecordIdentity
.. autoclass:: TaskAttemptStatus
   :members:
.. autoclass:: TaskAttempt
.. autoclass:: TaskInvocationOutcomeIdentity
.. autoclass:: TaskInvocationOutcomeKind
   :members:
.. autoclass:: TaskInvocationOutcome
.. autoclass:: TaskInvocationFailureIdentity
.. autoclass:: TaskInvocationFailure
.. autoclass:: TaskFailureRecordIdentity
.. autoclass:: TaskFailureRecord
.. autoclass:: WorkflowTransitionSequenceIdentity
.. autoclass:: TaskWorkflowTransitionRecordIdentity
.. autoclass:: TaskWorkflowTransitionRecord
.. autoclass:: NestedWorkflowMembershipIdentity
.. autoclass:: NestedWorkflowMembership
.. autoclass:: NestedWorkflowInvocationIdentity
.. autoclass:: NestedWorkflowInvocationKind
   :members:
.. autoclass:: NestedWorkflowObservationIdentity
.. autoclass:: ChildWorkflowCreationIdempotencyIdentity
.. autoclass:: NestedWorkflowInvocation

Result references, production, and dependencies
-----------------------------------------------

Every retained ``ResultObjectReference`` has exactly one closed producer variant.
Represented producers carry exact Workflow identities. Non-Workflow producers carry
actual evidence identities and explicit limitations rather than invented Workflow
lineage. A dependency is independent of Workflow membership.

.. autoclass:: ResultObjectReferenceIdentity
.. autoclass:: ResultObjectContentIdentity
.. autoclass:: ResultObjectTypeIdentity
.. autoclass:: ResultObjectDomainIdentity
.. autoclass:: ResultProducerProvenanceIdentity
.. autoclass:: ResultProducerEvidenceIdentity
.. autoclass:: ResultObjectReference
.. autoclass:: RepresentedTaskResultProducer
.. autoclass:: RepresentedScientificDecisionIngressProducer
.. autoclass:: ExternalResultProducerIdentity
.. autoclass:: ExternalProducerAttemptIdentity
.. autoclass:: ExternalResultProducer
.. autoclass:: RetainedResultSourceIdentity
.. autoclass:: ImportedRetainedResultProducer
.. autoclass:: HumanResultAuthorIdentity
.. autoclass:: HumanAuthoredResultProducer
.. autoclass:: UnknownLegacyResultProducer
.. autoclass:: ResultProductionRecordIdentity
.. autoclass:: ResultProductionRecord
.. autoclass:: ResultDependencyIdentity
.. autoclass:: ResultDependency

Scientific execution control state
----------------------------------

These immutable records represent externally supplied authority and dispatch state.
Constructing or replaying them does not issue a grant, authenticate authority, reserve
or claim a resource, dispatch work, reconcile an effect, or persist state.

.. autoclass:: ExecutionGrantIdentity
.. autoclass:: ExecutionGrantRevisionIdentity
.. autoclass:: ScientificExecutionAuthoritySnapshotIdentity
.. autoclass:: ScientificExecutionAuthorityStateIdentity
.. autoclass:: ScientificExecutionAuthorityReference
.. autoclass:: ScientificExecutorIdentity
.. autoclass:: SimulationExecutionRequestIdentity
.. autoclass:: SimulationExecutionRequestCorrelationIdentity
.. autoclass:: SimulationExecutionAuthorizationResultIdentity
.. autoclass:: SimulationExecutionRequestCorrelation
.. autoclass:: AuthorityReservationOutcomeIdentity
.. autoclass:: AuthorityReservationOutcomeKind
   :members:
.. autoclass:: AuthorityReservationOutcome
.. autoclass:: ObligationIdentity
.. autoclass:: DispatchDestinationIdentity
.. autoclass:: DispatchResourceScopeIdentity
.. autoclass:: DispatchCreationIdempotencyIdentity
.. autoclass:: SimulationDispatchObligation
.. autoclass:: SimulationDispatchOutcomeIdentity
.. autoclass:: DispatchOutcomeRecordIdentity
.. autoclass:: DispatchOutcomeKind
   :members:
.. autoclass:: DispatchOutcomeRecord
.. autoclass:: ObligationDispositionIdentity
.. autoclass:: ObligationDispositionKind
   :members:
.. autoclass:: ObligationDisposition

Scientific-decision state
-------------------------

A scientific-decision transition has no Task, activation, operation, or attempt
lineage. A correction consumes the exact effective predecessor resolution; stale or
branching corrections fail replay correlation.

.. autoclass:: ScientificDecisionRequestIdentity
.. autoclass:: ScientificDecisionOptionIdentity
.. autoclass:: ScientificDecisionOption
.. autoclass:: ResponseSourceIdentity
.. autoclass:: AuthorityContextIdentity
.. autoclass:: BoundaryReceiptIdentity
.. autoclass:: ScientificDecisionRecorderIdentity
.. autoclass:: ScientificDecisionRequest
.. autoclass:: ScientificDecisionTransitionRecordIdentity
.. autoclass:: ScientificDecisionResolution
.. autoclass:: ScientificDecisionWorkflowTransitionRecord
