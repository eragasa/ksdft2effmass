Periodic2d balanced Wannier90 encoded result
============================================

Purpose and ownership
---------------------

``Periodic2DWannier90BalancedEncodedDocuments`` preserves one exact nonempty result
wire for the retained periodic-2D balanced Wannier90 comparison. It is a frozen,
slotted encoded-wire DataObject, not an input document, native-artifact inventory,
physical model, localization result, optimizer result, numerical oracle, provenance
record, or acceptance decision.

The owner does not decode, normalize, copy, discover, or infer meaning from the
payload. Native-file authentication, serialization, correlation, independent numerical
reconstruction, localization assessment, and scientific acceptance remain separate
responsibilities.

Evidence boundary
-----------------

Construction accepts only exact built-in ``bytes`` and rejects an empty payload. The
retained ``wannier90-balanced-result.json`` identity is checked separately by
artifact-owned integration evidence against its maintained ``SHA256SUMS`` entry.
Content identity does not imply a separately retained input, native-file presence,
execution provenance, localization convergence, decoded correctness, scientific
validation, uncertainty quantification, or acceptance.

Public API
----------

.. currentmodule:: ksdft2effmass.periodic2d.run.wannier90.balanced

.. autoclass:: Periodic2DWannier90BalancedEncodedDocuments
   :members:
