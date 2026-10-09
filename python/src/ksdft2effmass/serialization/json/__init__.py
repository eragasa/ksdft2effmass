"""Reviewed strict and immutable JSON serialization facade."""

from .decoding import JsonValue, StrictJsonDecoder
from .immutable import (
    ImmutableJsonArray,
    ImmutableJsonCodec,
    ImmutableJsonObject,
    ImmutableJsonScalar,
    ImmutableJsonValue,
)

__all__ = [
    "ImmutableJsonArray",
    "ImmutableJsonCodec",
    "ImmutableJsonObject",
    "ImmutableJsonScalar",
    "ImmutableJsonValue",
    "JsonValue",
    "StrictJsonDecoder",
]
