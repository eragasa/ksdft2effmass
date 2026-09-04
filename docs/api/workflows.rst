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
Task or fires a transition.

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
