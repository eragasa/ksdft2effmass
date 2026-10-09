Periodic-1D retained Wannier90 campaign
=======================================

``ksdft2effmass.periodic1d.campaign.wannier90`` is the canonical owner of the
retained Appendix G periodic-1D Wannier90 campaign.  The package preserves exact
result bytes, authenticates their declared composite-input identity before consuming
input-owned controls, adapts Wilson phases and centers, authenticates explicitly
supplied native artifact bytes, and performs bounded independent Wilson-loop
verification.

The campaign does not discover paths, infer native-file presence, execute Quantum
ESPRESSO or Wannier90, or establish physical adequacy, convergence, provenance,
uncertainty quantification, scientific validation, or acceptance.  SHA-256 establishes
exact content identity only.  ``passes`` values are bounded software-verification
dispositions under caller-supplied tolerances.

Supported imports
-----------------

The classes below are supported from ``ksdft2effmass.periodic1d.campaign`` and from
its ``wannier90`` leaf facade.  The former
``ksdft2effmass.campaigns.periodic_1d`` and research-monograph publication facades do
not forward these names.

Document and result records
---------------------------

.. currentmodule:: ksdft2effmass.periodic1d.campaign

.. autoclass:: Periodic1DWannier90EncodedDocuments
   :members:

.. autoclass:: Periodic1DWannier90WilsonGroupResult
   :members:

.. autoclass:: Periodic1DWannier90CampaignResult
   :members:

.. autoclass:: Periodic1DWannier90ResultJsonSerializer
   :members:

Document correlation
--------------------

The campaign Workflow strictly decodes the result first, reads the required composite
input digest from its closed provenance object, hashes the still-opaque input bytes,
and rejects disagreement before deserializing the composite controls.  It then checks
the exact ordered retained-band inventory.

.. autoclass:: Periodic1DWannier90CampaignWorkflowRequest
   :members:

.. autoclass:: Periodic1DWannier90CampaignWorkflowResult
   :members:

.. autoclass:: Periodic1DWannier90CampaignWorkflow
   :members:

Native artifact correlation
---------------------------

Native artifacts are supplied as explicit immutable byte records.  Their logical
names, byte counts, and digests are authenticated against the retained result before
supported scientific text is parsed.  Group identifiers are explicit correlation
keys; they are not inferred model, state-space, basis, gauge, or provenance identities.

.. autoclass:: Periodic1DWannier90NativeArtifactGroup
   :members:

.. autoclass:: Periodic1DWannier90NativeArtifactWorkflowRequest
   :members:

.. autoclass:: Periodic1DWannier90NativeArtifactGroupResult
   :members:

.. autoclass:: Periodic1DWannier90NativeArtifactWorkflowResult
   :members:

.. autoclass:: Periodic1DWannier90NativeArtifactWorkflow
   :members:

Independent Wilson verification
--------------------------------

For each selected positive reciprocal-loop edge, the verifier computes a unitary polar
factor and forms the ordered loop product.  A separate numerical route applies the
retained native gauge matrices before forming the loop.  Circular assignment compares
both reconstructed phase multisets with the retained spectrum and with each other.
Loop unitarity and minimum overlap singular value remain separate diagnostics.

.. autoclass:: Periodic1DWannier90WilsonVerificationRequest
   :members:

.. autoclass:: Periodic1DWannier90WilsonGroupVerificationResult
   :members:

.. autoclass:: Periodic1DWannier90WilsonVerificationResult
   :members:

.. autoclass:: Periodic1DWannier90WilsonVerifier
   :members:

Verified Workflow and integration facade
----------------------------------------

.. autoclass:: Periodic1DWannier90VerifiedNativeWorkflowRequest
   :members:

.. autoclass:: Periodic1DWannier90VerifiedNativeWorkflowResult
   :members:

.. autoclass:: Periodic1DWannier90VerifiedNativeWorkflow
   :members:

.. autoclass:: Periodic1DWannier90IntegrationCorrelationRequest
   :members:

.. autoclass:: Periodic1DWannier90IntegrationCorrelationResult
   :members:

.. autoclass:: Periodic1DWannier90IntegrationCorrelator
   :members:

.. autoclass:: Periodic1DWannier90IntegrationVerificationRequest
   :members:

.. autoclass:: Periodic1DWannier90IntegrationVerificationResult
   :members:

.. autoclass:: Periodic1DWannier90IntegrationVerifier
   :members:

.. autoclass:: Periodic1DWannier90Integration
   :members:
