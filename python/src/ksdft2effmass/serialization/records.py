"""Final typed-mapping and generic JSON boundaries for immutable records."""

from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import Mapping
from typing import Self, final

from .mapping_json import TypedJsonMappingDeserializer, TypedJsonMappingSerializer
from .typed_values import SerializableValue


class BaseTypedRecord(ABC):
    """Enforce final dictionary and JSON boundaries for one typed record.

    Concrete records explicitly project a ``StringWireEnum`` through its
    ``to_wire()`` method in ``_mapping`` and reconstruct it through ``from_wire()``
    in ``_from_mapping``. Enum conversion remains domain-owned while this base owns
    the final mapping and canonical-JSON pipeline.
    """

    __slots__ = ()

    @abstractmethod
    def _mapping(self) -> Mapping[str, SerializableValue]:
        """Return the concrete record's nested typed mapping.

        Ordinary string-mapped enums are represented by their exact built-in string
        wire values, not by implicit string inheritance.
        """

    @classmethod
    @abstractmethod
    def _from_mapping(
        cls,
        values: Mapping[str, SerializableValue],
    ) -> Self:
        """Reconstruct the concrete record from its typed mapping.

        Concrete owners validate exact string types before invoking a domain enum's
        ``from_wire()`` method.
        """

    @final
    def to_dict(self) -> Mapping[str, SerializableValue]:
        """Return the concrete record as a typed mapping.

        Returns
        -------
        Mapping[str, SerializableValue]
            Domain-owned field mapping before JSON normalization.

        Notes
        -----
        The returned values retain quantities, arrays, explicitly registered enums,
        tuples, and nested records. Concrete records project ``StringWireEnum``
        members to stable built-in strings before this boundary. This method does not
        produce JSON-native lists.
        """
        return self._mapping()

    @classmethod
    @final
    def from_dict(cls, values: Mapping[str, SerializableValue]) -> Self:
        """Reconstruct a concrete record from a typed mapping.

        Parameters
        ----------
        values
            Domain field mapping after generic typed-value decoding.

        Returns
        -------
        Self
            Immutable validated concrete record.

        Raises
        ------
        TypeError
            ``values`` is not a mapping or contains a field with the wrong type.
        ValueError
            The field inventory or a correlated domain invariant is invalid.
        """
        if not isinstance(values, Mapping):
            raise TypeError("values must be a mapping")
        return cls._from_mapping(values)

    @final
    def to_json(self) -> bytes:
        """Serialize the record through the final generic JSON boundary.

        Returns
        -------
        bytes
            Canonical UTF-8 representation of :meth:`to_dict`.

        Notes
        -----
        Concrete records cannot override this method. Domain behavior remains in
        ``_mapping`` and generic normalization remains in the serializer.
        """
        return TypedJsonMappingSerializer().serialize(self.to_dict())

    @classmethod
    @final
    def from_json(cls, wire: bytes) -> Self:
        """Deserialize canonical JSON bytes and validate the concrete record.

        Parameters
        ----------
        wire
            Canonical typed JSON bytes.

        Returns
        -------
        Self
            Immutable reconstructed record.

        Raises
        ------
        TypeError
            The wire or a decoded field has the wrong type.
        ValueError
            Typed metadata or a concrete record invariant is invalid.
        """
        return cls.from_dict(TypedJsonMappingDeserializer().deserialize(wire))
