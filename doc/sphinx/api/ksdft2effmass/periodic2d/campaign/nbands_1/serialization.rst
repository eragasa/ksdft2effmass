Periodic2d isolated-band definition and serialization
=====================================================

Purpose and ownership
---------------------

``Periodic2DIsolatedBandCampaignDefinition`` is the typed DataObject for every
version-one isolated-band input control.  It is separate from:

* ``Periodic2DIsolatedBandEncodedDocuments``, which preserves the exact retained input and
  result bytes for provenance and byte correlation;
* ``Periodic2DIsolatedBandCampaignJsonSerializer``, which owns JSON wire mechanics;
* the calculation Workflow, which consumes the typed definition; and
* the independent verifier, which deliberately does not import the maintained
  serializer or calculation route.

The serializer changes no retained file. Its canonical output is a deterministic,
compact semantic reconstruction and is not claimed to be byte-identical to the
historically authored input formatting.

Version-one contract
--------------------

The JSON root is closed and contains the experiment identity, evidence status,
dimensionless convention, isotropic and anisotropic potential controls, coupling
sequence, plane-wave and finite-difference inventories, parent momenta, comparison
sizes, reciprocal meshes, hopping shells, effective-mass step, and topology
tolerances. Nested objects are also closed. Unknown or missing fields, duplicate keys,
nonfinite constants, invalid UTF-8, and unsupported schema versions fail before a
partial definition is returned.

JSON floating-point controls must use floating-point syntax and decode to exact
built-in ``float`` values. JSON integers are accepted only for documented integer
fields. Booleans, numeric strings, and integers substituted for floating-point fields
are rejected rather than coerced. Inventories become immutable tuples and retain their
declared order.

Units and conventions
---------------------

All real controls are dimensionless binary64 values under the retained convention

.. math::

   a=2\pi,\qquad G=1,\qquad E_G=1,

where :math:`aG=2\pi`. Parent momenta are reduced reciprocal coordinates ordered as
``(first_direction, second_direction)``. Plane-wave indices use first-index-outer,
second-index-inner order, and coordinate grids use the corresponding first-coordinate-
outer convention in the calculation owner. The definition validates the duality
identity, increasing inventories, odd finite-difference meshes, cutoff containment,
full final hopping shell, and topology-overlap range.

Canonical encoding
------------------

``serialize`` emits UTF-8 JSON with lexicographically sorted keys, compact separators,
and one terminal newline. ``deserialize(serialize(record))`` reproduces the complete
typed definition. Canonical encoding establishes deterministic software behavior; it
does not authenticate retained bytes or establish any numerical or scientific claim.
Exact retained identities remain owned by the campaign model and correlation result.

Implementation and evidence mapping
-----------------------------------

* Typed records:
  ``python/src/ksdft2effmass/periodic2d/campaign/nbands_1/definition.py``
* Wire mechanics:
  ``python/src/ksdft2effmass/periodic2d/campaign/nbands_1/serialization/``
* Calculation consumer:
  ``python/src/ksdft2effmass/periodic2d/campaign/nbands_1/calculate.py``
* Software verification:
  ``python/tests/software_verification/ksdft2effmass/periodic2d/campaign/nbands_1/``
* Retained numerical integration evidence:
  ``python/tests/ksdft2effmass/periodic2d/campaign/nbands_1/``

The software evidence checks exact scalar types, immutable inventories, closed nested
objects, duplicate rejection, deterministic encoding, and semantic round trips. The
existing retained integration evidence confirms that the extracted definition still
reproduces the historical result bytes and that the independent numerical verifier
continues to reject representative corruption.

Reference and provenance
------------------------

* Bray, T., *The JavaScript Object Notation (JSON) Data Interchange Format*, RFC 8259
  (2017). DOI: ``10.17487/RFC8259``.
* Field names, evidence labels, dimensionless conventions, and canonical encoding are
  repository-owned version-one contracts documented on this page.

Limitations
-----------

This slice types and serializes the isolated-band input, provenance, and canonical
result-document identity. The detailed result payload remains to be decomposed into
granular typed observation and result records. No calculation is run by serialization,
no retained artifact is rewritten, and no stress, composite, defect, validation, or
uncertainty-quantification claim follows from a successful round trip.

Public API
----------

.. currentmodule:: ksdft2effmass.periodic2d.campaign.nbands_1

.. autoclass:: Periodic2DIsolatedBandCampaignDefinition
   :members:

.. autoclass:: Periodic2DIsolatedBandCampaignJsonSerializer
   :members:

.. autoclass:: Periodic2DIsolatedBandProvenance
   :members:

.. autoclass:: Periodic2DIsolatedBandResultDocument
   :members:
