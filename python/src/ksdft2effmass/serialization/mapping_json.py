"""Generic JSON actions for mappings of typed scientific values."""

from __future__ import annotations

from collections.abc import Mapping

from .contracts import JsonDeserializer, JsonSerializer
from .typed_values import SerializableValue, TypedJsonValueCodec


class TypedJsonMappingSerializer(
    JsonSerializer[Mapping[str, SerializableValue], bytes]
):
    """Serialize one typed scientific-value mapping to canonical JSON bytes."""

    __slots__ = ("_codec",)

    def __init__(self) -> None:
        """Construct a mapping serializer.

        Notes
        -----
        Construction creates a closed ``TypedJsonValueCodec`` registry. The action
        stores no domain schema and performs no filesystem access.
        """
        self._codec = TypedJsonValueCodec()

    def serialize(self, record: Mapping[str, SerializableValue]) -> bytes:
        """Serialize a typed scientific mapping to canonical JSON bytes.

        Parameters
        ----------
        record
            String-keyed root mapping containing supported typed scientific values.

        Returns
        -------
        bytes
            UTF-8 JSON with sorted keys, two-space indentation, and a terminal
            newline.

        Raises
        ------
        TypeError
            ``record`` is not a mapping or contains an unsupported value.
        ValueError
            A supported value is nonfinite, malformed, or uses reserved metadata.
        """
        if not isinstance(record, Mapping):
            raise TypeError("record must be a mapping")
        return self._codec.serialize_bytes(record)


class TypedJsonMappingDeserializer(
    JsonDeserializer[Mapping[str, SerializableValue], bytes]
):
    """Deserialize canonical JSON bytes to a typed scientific-value mapping."""

    __slots__ = ("_codec",)

    def __init__(self) -> None:
        """Construct a mapping deserializer.

        Notes
        -----
        The deserializer uses the same closed typed-value registry as the serializer.
        It supplies no defaults for absent domain fields.
        """
        self._codec = TypedJsonValueCodec()

    def deserialize(self, wire: bytes) -> Mapping[str, SerializableValue]:
        """Deserialize canonical JSON bytes to a typed scientific mapping.

        Parameters
        ----------
        wire
            UTF-8 JSON bytes produced under the typed-value contract.

        Returns
        -------
        Mapping[str, SerializableValue]
            Reconstructed string-keyed mapping with NumPy arrays, quantities, enums,
            tuples, and sparse values restored.

        Raises
        ------
        TypeError
            ``wire`` is not bytes or its root value is not a mapping.
        ValueError
            JSON syntax, typed metadata, numeric bounds, or sparse structure is
            invalid.
        """
        values = self._codec.deserialize_bytes(wire)
        if not isinstance(values, Mapping):
            raise TypeError("JSON bytes must decode to a mapping")
        return values
