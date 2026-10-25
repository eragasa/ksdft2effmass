JSON serialization contracts
============================

.. currentmodule:: ksdft2effmass.serialization

The abstract contracts preserve both the exact record type and the JSON wire type.
Direct codecs use ``serialize`` and ``deserialize``. ``TypedJsonMappingSerializer``
and ``TypedJsonMappingDeserializer`` are the generic byte actions used by final
``to_json`` and ``from_json`` representation boundaries: ``to_json`` delegates
``to_dict`` to the serializer, while ``from_json`` delegates bytes to the deserializer
and then calls ``from_dict``. ActionObjects whose ``execute`` methods return
operational ResultObjects are not raw codecs and do not inherit these contracts.

``TypedJsonValueCodec`` is the reusable KSD incubation boundary for scientific JSON
values. It recursively preserves supported fixed-width NumPy scalars and arrays,
canonical SciPy CSR arrays, PhysKit model-system units and quantities, registered
enums, tuples, mappings, and records exposing typed mappings. Domain packages compose
these values and do not implement NumPy, SciPy, or quantity wire conversion. The
capability is intentionally independent of PIAB1D and is expected to migrate to
PhysKit after its contract stabilizes.

The codec rejects booleans and nonnumeric NumPy dtypes, nonfinite values, unsupported
extended-precision dtypes, integer overflow, duplicate JSON keys, nonstandard JSON
numeric constants, unregistered enums, malformed sparse indices, and ambiguous plain
mappings using its reserved tag key. Serialization emits deterministic UTF-8 bytes
with sorted keys and a final newline.

.. autoclass:: BaseTypedRecord
   :members:

.. autoclass:: JsonSerializer
   :members:

.. autoclass:: JsonDeserializer
   :members:

.. autoclass:: JsonCodec
   :members:

.. autoclass:: TypedJsonValueCodec
   :members:

.. autoclass:: TypedJsonMappingSerializer
   :members:

.. autoclass:: TypedJsonMappingDeserializer
   :members:
