PIAB1D verification wire decoding
=================================

Purpose and contract
--------------------

``Piab1dResultDecoder`` owns the closed JSON-to-Python mechanics shared
by independent PIAB1D verifiers. It reads an existing UTF-8 JSON object and provides
strict conversions for mappings, arrays, nonempty strings, lowercase SHA-256 digests,
integers, finite real scalars, scalar sequences, and finite binary64 matrices.

The encoded representation is the recursive union ``null | bool | int | float | str |
array | object``. Integer and real conversions reject booleans. Real conversions reject
numeric strings and non-finite values. Matrix conversion applies that same scalar rule
to every nested entry before constructing a NumPy array; it therefore does not inherit
NumPy's Boolean or numeric-string coercions. Rows must form a rectangular two-dimensional
matrix.

Ownership and limitations
-------------------------

Decoding establishes representation conformance only. Campaign-specific versions,
shapes, units, statuses, provenance, mathematical identities, and tolerances remain
owned by their verifier ActionObjects. The decoder does not authenticate source bytes,
run calculations, or establish numerical or scientific validity.

The defining source is
``python/src/ksdft2effmass/campaigns/piab1d/verification/decoder.py``. Negative scalar-
coercion evidence is maintained with ``Piab1dResultsVerifier`` tests under
``python/tests/software_verification/ksdft2effmass/campaigns/piab1d/``. This wire policy
is repository-derived and uses no external scientific reference.

API
---

.. currentmodule:: ksdft2effmass.campaigns.piab1d.verification.decoder

.. autoclass:: Piab1dResultDecoder
   :members:
