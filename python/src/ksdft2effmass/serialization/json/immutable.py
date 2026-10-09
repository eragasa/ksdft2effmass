"""Immutable JSON values and deterministic byte-wire conversion."""

from __future__ import annotations

import json
import math
from dataclasses import dataclass

from ..contracts import JsonCodec
from .decoding import JsonValue, StrictJsonDecoder


@dataclass(frozen=True, slots=True)
class ImmutableJsonArray:
    """Represent one recursively immutable ordered JSON array.

    Parameters
    ----------
    values
        Exact tuple of supported immutable JSON values.

    Raises
    ------
    TypeError
        If the container or an item has an unsupported exact representation.
    ValueError
        If a float item is nonfinite.
    """

    values: tuple[ImmutableJsonValue, ...]

    def __post_init__(self) -> None:
        """Require an exact immutable value tuple."""
        if type(self.values) is not tuple:
            raise TypeError("values must be an exact tuple")
        allowed_types = {
            bool,
            int,
            float,
            str,
            ImmutableJsonArray,
            ImmutableJsonObject,
        }
        if any(
            item is not None and type(item) not in allowed_types for item in self.values
        ):
            raise TypeError("every item must be an immutable JSON value")
        if any(type(item) is float and not math.isfinite(item) for item in self.values):
            raise ValueError("JSON real values must be finite")


@dataclass(frozen=True, slots=True)
class ImmutableJsonObject:
    """Represent one immutable canonical string-keyed JSON object.

    Parameters
    ----------
    fields
        Exact tuple of unique key-value tuples in lexical key order.

    Raises
    ------
    TypeError
        If a container, key, or value has an unsupported exact representation.
    ValueError
        If keys are repeated or not lexically ordered, or a float is nonfinite.
    """

    fields: tuple[tuple[str, ImmutableJsonValue], ...]

    def __post_init__(self) -> None:
        """Require exact pairs, unique ordered keys, and immutable values."""
        if type(self.fields) is not tuple:
            raise TypeError("fields must be an exact tuple")
        if any(type(field) is not tuple or len(field) != 2 for field in self.fields):
            raise TypeError("each field must be one exact key-value tuple")
        keys = tuple(field[0] for field in self.fields)
        if any(type(key) is not str for key in keys):
            raise TypeError("JSON object keys must be built-in strings")
        if keys != tuple(sorted(set(keys))):
            raise ValueError("JSON object keys must be unique and lexically ordered")
        values = tuple(field[1] for field in self.fields)
        allowed_types = {
            bool,
            int,
            float,
            str,
            ImmutableJsonArray,
            ImmutableJsonObject,
        }
        if any(
            value is not None and type(value) not in allowed_types for value in values
        ):
            raise TypeError("every field must contain an immutable JSON value")
        if any(type(value) is float and not math.isfinite(value) for value in values):
            raise ValueError("JSON real values must be finite")

    def field(self, name: str) -> ImmutableJsonValue:
        """Return one named value.

        Parameters
        ----------
        name
            Exact built-in field name.

        Returns
        -------
        ImmutableJsonValue
            The immutable value owned by ``name``.

        Raises
        ------
        TypeError
            If ``name`` is not an exact built-in string.
        KeyError
            If the field is absent.
        """
        if type(name) is not str:
            raise TypeError("name must be a built-in str")
        for key, value in self.fields:
            if key == name:
                return value
        raise KeyError(name)


type ImmutableJsonScalar = None | bool | int | float | str
type ImmutableJsonValue = ImmutableJsonScalar | ImmutableJsonArray | ImmutableJsonObject


class ImmutableJsonCodec(JsonCodec[ImmutableJsonObject, bytes]):
    """Convert strict JSON object bytes to and from immutable JSON values.

    Deserialization rejects duplicate keys, nonfinite constants, malformed UTF-8, and a
    non-object root. Object fields are placed in lexical order. Serialization emits
    compact, sorted, newline-terminated UTF-8 JSON. Canonical output need not reproduce
    whitespace or field order from source bytes.
    """

    __slots__ = ()

    def deserialize(self, wire: bytes) -> ImmutableJsonObject:
        """Decode one strict JSON object into a recursively immutable tree.

        Parameters
        ----------
        wire
            Exact built-in UTF-8 JSON bytes.

        Returns
        -------
        ImmutableJsonObject
            Complete immutable object tree with lexical field ordering.

        Raises
        ------
        TypeError
            If ``wire`` has the wrong exact representation or the root is not an object.
        ValueError
            If the bytes are malformed, duplicate-keyed, or nonfinite JSON.
        MemoryError
            If Python cannot allocate the decoded tree.
        RecursionError
            If the document exceeds the parser or adapter recursion depth.
        """
        decoded = StrictJsonDecoder().document(wire)
        return self.immutable_object(decoded)

    def serialize(self, record: ImmutableJsonObject) -> bytes:
        """Encode one immutable object as canonical UTF-8 JSON bytes.

        Parameters
        ----------
        record
            Exact immutable JSON object.

        Returns
        -------
        bytes
            Compact, sorted, newline-terminated UTF-8 JSON.

        Raises
        ------
        TypeError
            If ``record`` is not an exact :class:`ImmutableJsonObject`.
        MemoryError
            If Python cannot allocate the encoded representation.
        RecursionError
            If the tree exceeds the adapter or encoder recursion depth.
        """
        if type(record) is not ImmutableJsonObject:
            raise TypeError("record must be ImmutableJsonObject")
        value = self.builtin_value(record)
        return (
            json.dumps(
                value,
                allow_nan=False,
                sort_keys=True,
                separators=(",", ":"),
            )
            + "\n"
        ).encode("utf-8")

    def immutable_value(self, value: JsonValue) -> ImmutableJsonValue:
        """Adapt one already validated JSON value without repeating validation.

        Parameters
        ----------
        value
            Closed JSON value previously validated by :class:`StrictJsonDecoder`.

        Returns
        -------
        ImmutableJsonValue
            Recursively immutable representation of the supplied value.

        Raises
        ------
        AssertionError
            If a caller violates the precondition and supplies a representation outside
            the closed :data:`JsonValue` union.
        MemoryError
            If Python cannot allocate the immutable tree.
        RecursionError
            If the value exceeds adapter recursion depth.
        """
        if value is None:
            return None
        if type(value) is bool:
            return value
        if type(value) is int:
            return value
        if type(value) is float:
            return value
        if type(value) is str:
            return value
        if type(value) is list:
            return ImmutableJsonArray(
                tuple(self.immutable_value(item) for item in value)
            )
        if type(value) is dict:
            return self.immutable_object(value)
        raise AssertionError("StrictJsonDecoder returned an unsupported representation")

    def immutable_object(self, value: dict[str, JsonValue]) -> ImmutableJsonObject:
        """Adapt one already validated JSON object without repeating validation.

        Parameters
        ----------
        value
            String-keyed closed JSON object produced by
            :class:`StrictJsonDecoder`.

        Returns
        -------
        ImmutableJsonObject
            Recursively immutable object with lexical field ordering.

        Raises
        ------
        AssertionError
            If a nested value violates the closed JSON precondition.
        MemoryError
            If Python cannot allocate the immutable tree.
        RecursionError
            If the object exceeds adapter recursion depth.
        """
        return ImmutableJsonObject(
            tuple(
                (key, self.immutable_value(item)) for key, item in sorted(value.items())
            )
        )

    def builtin_value(self, value: ImmutableJsonValue) -> JsonValue:
        """Convert one immutable JSON value to fresh built-in containers.

        Parameters
        ----------
        value
            Closed immutable JSON value to convert recursively.

        Returns
        -------
        JsonValue
            Equivalent JSON value with fresh built-in list and dictionary containers.

        Raises
        ------
        TypeError
            If ``value`` has an unsupported exact representation.
        ValueError
            If a float value is nonfinite.
        MemoryError
            If Python cannot allocate the converted tree.
        RecursionError
            If the value exceeds adapter recursion depth.
        """
        if type(value) is ImmutableJsonArray:
            return [self.builtin_value(item) for item in value.values]
        if type(value) is ImmutableJsonObject:
            return {key: self.builtin_value(item) for key, item in value.fields}
        if value is None:
            return None
        if type(value) is bool:
            return value
        if type(value) is int:
            return value
        if type(value) is float:
            if not math.isfinite(value):
                raise ValueError("JSON real values must be finite")
            return value
        if type(value) is str:
            return value
        raise TypeError("value is not a supported immutable JSON representation")
