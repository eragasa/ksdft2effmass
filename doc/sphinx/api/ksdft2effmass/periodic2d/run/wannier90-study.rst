Periodic2d Wannier90 bounded-study encoded documents
====================================================

Purpose and ownership
---------------------

``Periodic2DWannier90StudyEncodedDocuments`` preserves exact nonempty input and result
wires for a bounded periodic-2D Wannier90 sensitivity study. It is a frozen, slotted
encoded-wire DataObject, not a parameter-space model, native-artifact inventory,
convergence result, localization assessment, numerical oracle, provenance record, or
acceptance decision.

The owner does not decode, normalize, copy, discover, or infer meaning from either
payload. Sensitivity-axis interpretation, native-file authentication, case correlation,
independent numerical reconstruction, convergence assessment, and scientific acceptance
remain separate responsibilities.

Scientific boundary
-------------------

The retained input declares bounded variations of reciprocal-mesh size, plane-wave
cutoff, and auxiliary embedding. These probe different numerical or representation
choices and are not collapsed into one error source. The encoded declarations and
reported case statuses do not by themselves demonstrate completed execution or
convergence along any axis.

Evidence boundary
-----------------

The retained ``wannier90-study-input.json`` and ``wannier90-study-result.json``
identities are checked separately by artifact-owned integration evidence against
maintained ``SHA256SUMS`` entries. Content identity does not establish native-file
presence, execution provenance, case completion, convergence, localization validity,
decoded correctness, scientific validation, uncertainty quantification, or acceptance.

Public API
----------

.. currentmodule:: ksdft2effmass.periodic2d.run.wannier90.study

.. autoclass:: Periodic2DWannier90StudyEncodedDocuments
   :members:
