Periodic-1D blind-alignment campaign
====================================

``ksdft2effmass.periodic1d.campaign.alignment.blind`` is the canonical owner of
the retained synthetic blind-alignment campaign.  It separates exact encoded bytes,
decoded controls, inference-visible observations, construction-only hidden truth,
numerical inference, post hoc evaluation, retained correlation, and independent
verification.

For an anchor cross-covariance :math:`C=L\Sigma R^\dagger`, singular values above
the explicit policy threshold define the identified sector and the inferred map is

.. math::

   \widehat U = L_r R_r^\dagger.

The extracted represented perturbation is

.. math::

   \widehat V = \widehat U H_d \widehat U^\dagger
      - \widehat\delta P - P H_0 P,
   \qquad P=\widehat U\widehat U^\dagger.

A rank-deficient outcome applies only to the identified sector.  The implementation
does not infer a null-space completion, physical-model identity, state-space
compatibility, gauge, energy reference, provenance, or acceptance from dimensions,
spectra, filenames, or hashes.

Supported imports
-----------------

The reviewed facades ``ksdft2effmass.periodic1d.campaign.alignment`` and its ``blind``
leaf expose only ``BlindAlignmentCampaign`` and ``BlindAlignmentEncodedDocuments`` for
this family. The broader campaign facade does not flatten this specialized family.
Lower-level records and Actions are documented from their defining modules for
maintained implementation and evidence code; they are not flattened into the leaf
facade.  The former
``ksdft2effmass.campaigns.periodic_1d.defects.blind_alignment`` route is removed
without a compatibility alias.

Campaign facade and exact documents
-----------------------------------

.. automodule:: ksdft2effmass.periodic1d.campaign.alignment.blind.campaign
   :members:
   :show-inheritance:

.. automodule:: ksdft2effmass.periodic1d.campaign.alignment.blind.encoded_documents
   :members:
   :show-inheritance:

Input, observation, and result records
--------------------------------------

.. automodule:: ksdft2effmass.periodic1d.campaign.alignment.blind.input_records
   :members:
   :show-inheritance:

.. automodule:: ksdft2effmass.periodic1d.campaign.alignment.blind.records
   :members:
   :show-inheritance:

.. automodule:: ksdft2effmass.periodic1d.campaign.alignment.blind.result_records
   :members:
   :show-inheritance:

Authenticated baseline and observation construction
---------------------------------------------------

.. automodule:: ksdft2effmass.periodic1d.campaign.alignment.blind.baseline
   :members:
   :show-inheritance:

.. automodule:: ksdft2effmass.periodic1d.campaign.alignment.blind.construction
   :members:
   :show-inheritance:

Inference and post hoc evaluation
---------------------------------

.. automodule:: ksdft2effmass.periodic1d.campaign.alignment.blind.inference
   :members:
   :show-inheritance:

.. automodule:: ksdft2effmass.periodic1d.campaign.alignment.blind.evaluation
   :members:
   :show-inheritance:

.. automodule:: ksdft2effmass.periodic1d.campaign.alignment.blind.case_execution
   :members:
   :show-inheritance:

Wire adaptation and correlation
-------------------------------

.. automodule:: ksdft2effmass.periodic1d.campaign.alignment.blind.serialization
   :members:
   :show-inheritance:

.. automodule:: ksdft2effmass.periodic1d.campaign.alignment.blind.result_serialization
   :members:
   :show-inheritance:

.. automodule:: ksdft2effmass.periodic1d.campaign.alignment.blind.result_encoding
   :members:
   :show-inheritance:

Workflow and independent verification
-------------------------------------

.. automodule:: ksdft2effmass.periodic1d.campaign.alignment.blind.workflow
   :members:
   :show-inheritance:

.. automodule:: ksdft2effmass.periodic1d.campaign.alignment.blind.verification
   :members:
   :show-inheritance:

Scientific and computational limits
-----------------------------------

Rows 030--032 and 065 now provide canonical represented-operator, finite-fiber,
matched-extraction, and finite-supercell ownership.  The family does not duplicate or
infer missing metadata, and importing it no longer loads ``campaigns.periodic_1d``.

The retained records are synthetic campaign evidence.  Agreement establishes bounded
software and numerical behavior only.  It does not establish material validation,
transferability, convergence, uncertainty quantification, physical adequacy, or
scientific acceptance.  Dense SVD, eigensolver, and matrix-product routes use cubic
time and quadratic storage in represented dimension; no arbitrary size limit is
imposed, and allocation may raise ``MemoryError``.  SHA-256 establishes exact content
identity only.  No Quantum ESPRESSO or Wannier90 execution is performed by this
campaign family.
