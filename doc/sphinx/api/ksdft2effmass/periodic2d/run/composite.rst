Periodic2d composite encoded documents
======================================

Purpose and ownership
---------------------

``Periodic2DCompositeEncodedDocuments`` preserves exact nonempty input and result bytes
for the retained periodic-2D composite campaign. It is a frozen, slotted encoded-wire
DataObject, not a scientific model, retained band group, frame, represented operator,
serializer, provenance record, or acceptance result.

The owner does not decode, normalize, copy, discover, or infer meaning from either
payload. Serialization, correlation, independent verification, and later typed
scientific-result adoption remain separate responsibilities.

Exact-byte and scientific boundary
----------------------------------

Construction accepts only exact built-in ``bytes`` and rejects empty payloads. The
retained ``composite-input.json`` and ``composite-result.json`` identities are checked
separately by artifact-owned integration evidence against maintained ``SHA256SUMS``
entries. Content identity does not establish execution provenance, retained-space or
frame identity, decoded correctness, convergence, scientific validation, uncertainty
quantification, or acceptance.

Public API
----------

.. currentmodule:: ksdft2effmass.periodic2d.run.composite

.. autoclass:: Periodic2DCompositeEncodedDocuments
   :members:
