Periodic2d topological encoded documents
========================================

Purpose and ownership
---------------------

``Periodic2DTopologicalEncodedDocuments`` preserves exact nonempty input and result
bytes for the retained periodic-2D topological campaign. It is a frozen, slotted
encoded-wire DataObject, not a physical model, topological invariant, scientific
result, numerical oracle, provenance record, or acceptance decision.

The owner does not decode, normalize, copy, discover, or infer meaning from either
payload. Serialization, correlation, independent verification, oracle qualification,
and later typed observation adoption remain separate responsibilities.

Evidence boundary
-----------------

Construction accepts only exact built-in ``bytes`` and rejects empty payloads. The
retained ``topological-input.json`` and ``topological-result.json`` identities are
checked separately by artifact-owned integration evidence against maintained
``SHA256SUMS`` entries. Content identity and encoded expected observations do not
establish execution provenance, decoded correctness, topology, convergence, scientific
validation, uncertainty quantification, or acceptance. The retained result document is
not an independently qualified numerical oracle.

Public API
----------

.. currentmodule:: ksdft2effmass.periodic2d.run.topological

.. autoclass:: Periodic2DTopologicalEncodedDocuments
   :members:
