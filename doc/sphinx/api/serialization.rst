JSON serialization contracts
============================

.. currentmodule:: ksdft2effmass.serialization

The abstract contracts preserve both the exact record type and the JSON wire type.
Direct codecs use ``serialize`` and ``deserialize``.  ActionObjects whose ``execute``
methods return operational ResultObjects are not raw codecs and do not inherit these
contracts.

.. autoclass:: JsonSerializer
   :members:

.. autoclass:: JsonDeserializer
   :members:

.. autoclass:: JsonCodec
   :members:

Strict and immutable JSON values
--------------------------------

.. currentmodule:: ksdft2effmass.serialization.json

``StrictJsonDecoder`` rejects malformed UTF-8 JSON, duplicate keys, nonfinite
extensions, unsupported values, and erased primitive representations.  The immutable
codec builds recursively frozen arrays and lexically ordered objects and emits compact,
sorted, newline-terminated bytes.  These wire owners assign no domain schema,
scientific identity, provenance, units, or acceptance status.

.. autoclass:: StrictJsonDecoder
   :members:

.. autoclass:: ImmutableJsonArray
   :members:

.. autoclass:: ImmutableJsonObject
   :members:

.. autoclass:: ImmutableJsonCodec
   :members:
