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
