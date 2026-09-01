Public API reference
====================

Use the documented package-level import paths.  Internal module layout is not a
public compatibility contract.

.. toctree::
   :maxdepth: 1

   operators
   quantum-espresso
   periodic-records
   petrinet-colored
   workflows
   persistence
   harness-task
   harness-prerequisites
   harness-authority
   harness-adapters
   harness-control

Provenance and external-tool records
------------------------------------

The complete Markdown-first field and invariant contract is available as a
:download:`maintained source page <provenance.md>`.  These generated entries are
taken from the implemented public import surface.

.. currentmodule:: ksdft2effmass.provenance

Artifact, manifest, and lineage records
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. autoclass:: ArtifactIdentity
.. autoclass:: ArtifactSpecification
.. autoclass:: ArtifactReference
.. autoclass:: ArtifactLocation
.. autoclass:: ArtifactLocationKind
.. autoclass:: RunManifest
.. autoclass:: ManifestState
.. autoclass:: ProvenanceRecord
.. autoclass:: LineageRelation
.. autoclass:: LineageKind

External-tool records
~~~~~~~~~~~~~~~~~~~~~

.. autoclass:: ExternalToolIdentity
.. autoclass:: ExternalToolSpecification
.. autoclass:: DeclaredCapability
.. autoclass:: CapabilityKind
.. autoclass:: InstallationObservation
.. autoclass:: VerificationObservation
.. autoclass:: VerificationStatus
.. autoclass:: ExternalExecutionRequest
.. autoclass:: ExternalExecutionResult
.. autoclass:: ExternalExecutionStatus
.. autoclass:: ExternalExecutionFailure
.. autoclass:: ExternalFailureStage
.. autoclass:: ExternalFailureCode

ResultObjects and ActionObjects
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. autoclass:: ArtifactIdentityVerificationResult
.. autoclass:: ArtifactIdentityVerificationStatus
.. autoclass:: ArtifactIdentityVerifier
.. autoclass:: ExecutionCorrelationResult
.. autoclass:: CorrelationStatus
.. autoclass:: CorrelationIssue
.. autoclass:: ExecutionOutcomeCorrelator
.. autoclass:: ProvenanceJsonSerializer
.. autoclass:: ProvenanceJsonError
