Public API reference
====================

Use the documented package-level import paths.  Internal module layout is not a
public compatibility contract.

.. toctree::
   :maxdepth: 1

   operators
   solid-state
   analysis
   model-systems
   research-monograph-campaigns
   ksdft2effmass/campaigns/piab1d/verification/index
   serialization
   base
   application
   units
   plane-wave-calculators
   quantum-espresso
   wannier90
   periodic-records
   petrinet-colored
   workflows
   workflows-v2
   persistence
   provenance

Provenance and external-tool records
------------------------------------

The complete Markdown-first field and invariant contract is included in this
API reference. These generated entries are taken from the implemented public
import surface.

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
