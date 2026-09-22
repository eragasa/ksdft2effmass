Scientific Workflow model
=========================

Use the package-level imports documented here.  These contracts represent
calculator-independent scientific composition. Most records and adapters are
immutable or effect-free; ``SimulationDispatchAdapter`` alone may enter an explicitly
injected application-owned dispatch effect after exact authorization and claim
correlation and complete atomic WorkflowRun persistence. The package does not provide
a calculator implementation or establish scientific validity. Generic colored-Petri-net contracts
remain under :mod:`ksdft2effmass.petrinet.colored`.

Result-value persistence foundations
------------------------------------

The human-selected boundary is an explicitly injected typed outward-domain codec,
not a registry or arbitrary protocol serializer. The Workflow, QE and scalar codecs
and minimal application codec composition implement seven concrete result families.
The complete WorkflowRun serializer now has explicit production traversal and
independent wire evidence. The atomic repository and exact historical claim
reconciliation are implemented with bounded real-SQLite evidence. The distinct
durable entry service is implemented with local race and crash evidence; complete
Task software gates and independent correction recheck are complete. This is
software-verified development work, not human acceptance or a release. The same-v1
nested-history correction has bounded lifecycle evidence. See
:doc:`../concepts/workflow-run-persistence` for exact coverage and limitations.

.. currentmodule:: ksdft2effmass.workflows

.. autoclass:: WorkflowResultValueCodec
   :members:
.. autoclass:: WorkflowResultValueSerializer
   :members:
.. autoclass:: WorkflowEncodedResultValue
.. autoclass:: WorkflowResultValueEncodeResult
.. autoclass:: WorkflowResultValueDecodeResult
.. autoclass:: WorkflowPersistenceFailureCode
   :members:
.. autoclass:: WorkflowPersistenceFailure
.. autoclass:: WorkflowRunCommitBinding

Aggregate boundary records
--------------------------

These immutable records implement intrinsic field and variant checks only. They do
not serialize, validate structural history, load or commit a run, derive receipts,
or confer replay equality or effect permission. Serialization and repository
operations belong to the separate ActionObjects documented below.

.. autoclass:: WorkflowEncodedRun
.. autoclass:: WorkflowRunEncodeResult
.. autoclass:: WorkflowRunDecodeResult
.. autoclass:: WorkflowRunTransaction
   :members:
.. autoclass:: WorkflowRunSnapshot
.. autoclass:: WorkflowRunLoadResult
.. autoclass:: WorkflowRunWriteResult
.. autoclass:: WorkflowRunClaimLoadResult
   :members:

Atomic repository and historical claims
---------------------------------------

``WorkflowRunAtomicRepository(store=..., serializer=..., validator=...)`` requires
an explicit shared store and a validator bound to that same serializer instance.
``load(request)`` performs one read and verifies complete domain representation and
structural closure without replay. ``commit(transaction)`` explicitly reads its
historical predecessor, validates exact immutable extension and submits once.
Shared CAS, idempotency, failure and uncertainty observations are preserved.
``load_claim(request, claimed_reservation_identity)`` requires an explicit revision
and complete expectations; only confirmed exact history yields a deterministic
receipt. Historical commitment never grants effect-entry permission. See
:doc:`../concepts/workflow-run-persistence` for exact derivations and recovery limits.

.. autoclass:: WorkflowRunRepository
   :members:
.. autoclass:: WorkflowRunAtomicRepository
   :members:

Structural transaction validation
----------------------------------

``WorkflowRunTransactionValidator(serializer=...).execute(transaction, predecessor)``
checks the exact candidate representation, retained structural closure and immutable
extension of the explicitly addressed predecessor. ``None`` means genesis, not latest.
The frozen ``WorkflowRunValidationResult`` retains those exact inputs and carries
validated bytes only for ``valid``; ``invalid``, ``incompatible`` and ``error`` carry
structured failure only. This establishes no stored presence or replay equality.

.. autoclass:: WorkflowRunTransactionValidator
   :members:
.. autoclass:: WorkflowRunValidationResult

Complete aggregate serialization
--------------------------------

``WorkflowRunSerializer(result_codec=...)`` receives the explicitly composed outward
codec. ``serialize(run, binding)`` returns complete canonical bytes and content
identity; ``deserialize(payload)`` returns the complete run and persisted binding.
Both use closed represented failures. No store, structural validator, replay,
scientific algorithm or native-file access occurs. Initial fixed genesis and
nonempty scalar/gate/marking wires verify exact bytes and fields. Further literal
facets cover all seven concrete families, rich CPN records, authority variants and
UTC timestamps, dispatch variants, mixed Task/decision records, nested invocations,
memberships/dependencies and all producer variants with native-admission records.
Task-model ordering and typed codec-failure propagation also have bounded evidence.
Independent whole-Task review identified a nested-history lifecycle gap. Its
same-v1 correction is implemented with bounded lifecycle evidence; independent
review requested additional regression and documentation corrections, whose recheck
found no remaining blocking findings.
Codec success alone establishes neither closed history nor authority.

.. autoclass:: WorkflowRunSerializer
   :members:

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

Normalized observations
-----------------------

``NormalizedObservationSource`` is a calculator-independent read-only protocol over
one immutable extracted Kohn--Sham ResultObject. It retains the exact concrete source
rather than copying integration-owned identities. ``NormalizedObservationAssembler``
validates source membership, output/source identity separation, neutral-record
provenance, parser and policy identity shape, and canonical limitations. It returns
``NormalizedObservationSet`` or a closed
``NormalizedObservationAssemblyFailure`` retaining the exact request and no partial
set. Assembly performs no parsing, unit conversion, numerical transformation,
execution, scientific analysis, or acceptance.

.. autoclass:: ObservationCorrelationIdentity
   :members:
.. autoclass:: ObservationNormalizationPolicySource
   :members:
.. autoclass:: NormalizedObservationSource
   :members:
.. autoclass:: NormalizedObservationAssemblyRequest
.. autoclass:: NormalizedObservationSet
.. autoclass:: NormalizedObservationAssemblyFailureCode
   :members:
.. autoclass:: NormalizedObservationAssemblyFailure
.. autodata:: NormalizedObservationAssemblyResult
.. autoclass:: NormalizedObservationAssembler
   :members:

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

Separate immutable intent and first-terminal records are now public. Intent retains
its original STARTED attempt-record identity and no terminal fields. Observation
links nominally to either a new intent or an actual retained combined pending
record; equal identity strings do not merge those alternatives. Confirmed requires
nonempty paired exports/admissions, rejected requires failure only, and indeterminate
requires reconciliation only. Constructors check intrinsic types and values, not
source existence, retained history, child replay or effect permission.

The v1 aggregate, structural validator and serializer now integrate these records.
New observations require their exact intent source in the actual predecessor and
introduce the terminal attempt/outcome atomically. Existing combined pending records
remain unchanged when their separate observation is appended. First-terminal
uniqueness also applies to indeterminate outcomes. Both empty extension tuples are
omitted from the original 34-field wire; either nonempty requires both keys in the
36-field v1 wire. No stored bytes or version identities are rewritten.

Real SQLite evidence covers both intent sources and all three terminal kinds,
including reopen and later unrelated extension. Independent correction recheck
found no blocking findings; the bounded persistence Task is software verified,
not scientifically validated or human accepted.

.. autoclass:: NestedWorkflowInvocationIntentIdentity
.. autoclass:: NestedWorkflowInvocationIntent
.. autoclass:: NestedWorkflowTerminalObservationKind
   :members:
.. autoclass:: NestedWorkflowTerminalObservation

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
.. autoclass:: NativeOutputAdmissionIdentity
.. autoclass:: NativeOutputAdmission
.. autoclass:: ResultDependencyIdentity
.. autoclass:: ResultDependency

Scientific execution control state
----------------------------------

These immutable records represent externally supplied authority and dispatch state.
Constructing or replaying them does not issue a grant, authenticate authority, reserve
or claim a resource, dispatch work, reconcile an effect, or persist state.

The architecture-facing control contracts use software-architecture terminology.
``SimulationExecutionAuthorizer`` is effect-free. ``SimulationDispatchEffect`` is the
application-supplied consumer port selected by the resolved architecture decision;
``SimulationDispatchClaimPreparer`` constructs a replay-verified claimed candidate,
while a reconciled ``WorkflowRunClaimCommitReceipt`` records that exact historical
claim commitment. A supplied receipt container alone is not commitment evidence. On every authorization-valid, exactly
correlated call, ``SimulationDispatchAdapter`` uses the injected persistence-owned
``SimulationDispatchEntryCommitter`` port to
attempt the separate claimed-to-dispatch-entered compare-and-swap. It enters the effect
only for the newly successful result carrying an exact
``SimulationDispatchEntryReceipt``; an already-entered, stale, losing, or erroneous
call performs no effect. Applications may place their own physicist-facing API over
this boundary. The adapter does not implement persistence, discover an executor,
retry, admit results, or fire a generic transition.

``WorkflowRunDispatchEntryCommitter(repository=..., serializer=...,
runtime_bundle=...)`` implements that entry port through the structural WorkflowRun
repository. Composition supplies the same serializer used by the repository and its
validator. Historical receipt reconciliation, exact latest-head agreement and equal
replay of both head and candidate precede a single invocation-local commit. Only
its exact acknowledgement grants entry; uncertainty grants neither permission nor
an automatic retry. The service itself invokes no external effect. See
:doc:`../concepts/workflow-run-persistence` for the full boundary and crash limits.

``SimulationDispatchResultIngressPreparer`` always appends one immutable
``DispatchObservationRecord``. Indeterminate, conflict, and error observations do not
close the started attempt or obligation. One later confirmed or rejected observation
may append the sole terminal record group. The preparer constructs and replay-checks
the successor candidate without persisting it. Confirmed ingress requires the
dedicated ``NativeOutputAdmission`` correlation; every other observation prohibits
native-output admission.

.. autoclass:: ScientificExecutionAuthorityVerificationKind
   :members:
.. autoclass:: ScientificExecutionGrantState
   :members:
.. autoclass:: ScientificExecutionAuthoritySnapshot
.. autoclass:: ScientificExecutionAuthorityGrant
.. autoclass:: SimulationExecutionAuthorizationPhase
   :members:
.. autoclass:: SimulationExecutionAuthorizationRequest
.. autoclass:: SimulationExecutionAuthorizationOutcomeKind
   :members:
.. autoclass:: SimulationExecutionAuthorizationResult
.. autoclass:: SimulationExecutionAuthorizer
   :members:
.. autoclass:: SimulationExecutionRequest
.. autoclass:: SimulationDispatchRequest
.. autoclass:: SimulationDispatchEffectRequest
.. autoclass:: SimulationDispatchEntryOutcomeKind
   :members:
.. autoclass:: SimulationDispatchEntryResult
.. autoclass:: SimulationDispatchEntryCommitter
   :members:
.. autoclass:: WorkflowRunDispatchEntryCommitter
   :members:
.. autoclass:: SimulationDispatchOutcome
.. autoclass:: SimulationDispatchEffect
   :members:
.. autoclass:: SimulationDispatchAdapterResultKind
   :members:
.. autoclass:: SimulationDispatchAdapterResult
.. autoclass:: SimulationDispatchAdapter
   :members:
.. autoclass:: SimulationDispatchPreparationRequest
.. autoclass:: SimulationDispatchPreparationOutcomeKind
   :members:
.. autoclass:: SimulationDispatchPreparationResult
.. autoclass:: SimulationDispatchPreparer
   :members:
.. autoclass:: SimulationDispatchClaimRequest
.. autoclass:: SimulationDispatchClaimOutcomeKind
   :members:
.. autoclass:: SimulationDispatchClaimResult
.. autoclass:: SimulationDispatchClaimPreparer
   :members:
.. autoclass:: SimulationDispatchReconciliationRequest
.. autoclass:: SimulationDispatchReconciliationOutcomeKind
   :members:
.. autoclass:: SimulationDispatchReconciliationResult
.. autoclass:: SimulationDispatchReconciler
   :members:
.. autoclass:: SimulationDispatchResultIngressRequest
.. autoclass:: SimulationDispatchResultIngressOutcomeKind
   :members:
.. autoclass:: SimulationDispatchResultIngressResult
.. autoclass:: SimulationDispatchResultIngressPreparer
   :members:

.. autoclass:: ExecutionGrantIdentity
.. autoclass:: ExecutionGrantRevisionIdentity
.. autoclass:: ScientificExecutionAuthoritySnapshotIdentity
.. autoclass:: ScientificExecutionAuthorityStateIdentity
.. autoclass:: ScientificExecutionAuthorityReference
.. autoclass:: ScientificExecutorIdentity
.. autoclass:: SimulationExecutionRequestIdentity
.. autoclass:: SimulationExecutionRequestCorrelationIdentity
.. autoclass:: SimulationExecutionAuthorizationResultIdentity
.. autoclass:: WorkflowRunClaimCommitReceiptIdentity
.. autoclass:: WorkflowRunClaimCommitReceipt
.. autoclass:: SimulationDispatchEntryIdentity
.. autoclass:: SimulationDispatchEntryReceiptIdentity
.. autoclass:: SimulationDispatchEntry
.. autoclass:: SimulationDispatchEntryReceipt
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
.. autoclass:: SimulationDispatchObservationIdentity
.. autoclass:: DispatchObservationRecordIdentity
.. autoclass:: DispatchObservationKind
   :members:
.. autoclass:: DispatchObservationRecord
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
