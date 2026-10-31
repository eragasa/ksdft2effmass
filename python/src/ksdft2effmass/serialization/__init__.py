"""Public type-preserving JSON serialization contracts.

The dependency-free abstract contracts load eagerly. NumPy- and PhysKit-aware typed
serialization owners load only when their public symbols are requested, so a consumer
of :class:`JsonCodec` does not acquire unrelated numerical runtime dependencies.
"""

from typing import TYPE_CHECKING, TypeAliasType

from .contracts import JsonCodec, JsonDeserializer, JsonSerializer
from .enums import StringWireEnum

if TYPE_CHECKING:
    from .mapping_json import TypedJsonMappingDeserializer, TypedJsonMappingSerializer
    from .records import BaseTypedRecord
    from .typed_values import (
        DictionaryRecord,
        JsonValue,
        SerializableValue,
        TypedJsonValueCodec,
    )

__all__ = [
    "BaseTypedRecord",
    "DictionaryRecord",
    "JsonCodec",
    "JsonDeserializer",
    "JsonSerializer",
    "JsonValue",
    "SerializableValue",
    "StringWireEnum",
    "TypedJsonMappingDeserializer",
    "TypedJsonMappingSerializer",
    "TypedJsonValueCodec",
]


def __getattr__(name: str) -> type | TypeAliasType:
    """Load one typed-serialization public symbol on first access."""
    if name == "BaseTypedRecord":
        from .records import BaseTypedRecord

        return BaseTypedRecord
    if name == "TypedJsonMappingDeserializer":
        from .mapping_json import TypedJsonMappingDeserializer

        return TypedJsonMappingDeserializer
    if name == "TypedJsonMappingSerializer":
        from .mapping_json import TypedJsonMappingSerializer

        return TypedJsonMappingSerializer
    if name == "TypedJsonValueCodec":
        from .typed_values import TypedJsonValueCodec

        return TypedJsonValueCodec
    if name in {"DictionaryRecord", "JsonValue", "SerializableValue"}:
        from .typed_values import DictionaryRecord, JsonValue, SerializableValue

        aliases: dict[str, type | TypeAliasType] = {
            "DictionaryRecord": DictionaryRecord,
            "JsonValue": JsonValue,
            "SerializableValue": SerializableValue,
        }
        return aliases[name]
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
