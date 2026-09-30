Evidence-grounded publication authoring
========================================

The public authoring boundary creates only immutable replacement proposals. It does
not retrieve evidence, call a model without an injected local port, read or write a
manuscript, update a bibliography, publish content, or establish scientific or human
acceptance. The implementation architecture and exact prototype target are documented
at :doc:`../architecture/ksdft2effmass/publications/authoring/index`.

.. currentmodule:: ksdft2effmass.publications

Target and external-evidence projection
---------------------------------------

.. autoclass:: ManuscriptTargetContext
.. autoclass:: CitationKeyStatus
.. autoclass:: TranscriptEvidenceSelectionOutcomeProjection
.. autoclass:: TranscriptEvidenceMappingBasis
.. autoclass:: TranscriptEvidenceSelectionReference
.. autoclass:: RetrievedEvidenceExcerpt
.. autoclass:: EvidenceRetrievalOutcomeProjection
.. autoclass:: EvidenceRetrievalProjection

Project Koios owner adapters
----------------------------

.. autoclass:: ProjectedCitationIdentity
.. autoclass:: ProjectKoiosReferencesAdapter
.. autoclass:: ProjectKoiosIngestionAdapter
.. autoclass:: ProjectKoiosSearchAdapter

Requests and local inference
----------------------------

.. autoclass:: ManuscriptAuthoringRequest
.. autoclass:: ProposedCitation
.. autoclass:: ManuscriptInferenceRequest
.. autoclass:: ManuscriptInferenceResponse
.. autoclass:: LocalManuscriptInferencePort

Proposals, results, and composition
-----------------------------------

.. autoclass:: HumanAcceptanceStatus
.. autoclass:: ManuscriptProposal
.. autoclass:: ManuscriptAuthoringOutcome
.. autoclass:: ManuscriptAuthoringIssue
.. autoclass:: ManuscriptAuthoringResult
.. autoclass:: EvidenceGroundedManuscriptAuthor
