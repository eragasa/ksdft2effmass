"""Public abstract contracts for JSON serialization boundaries."""

from __future__ import annotations

from abc import ABC, abstractmethod


class JsonSerializer[RecordT, WireT: (str, bytes)](ABC):
    """Serialize one exact record type to one JSON wire representation type."""

    __slots__ = ()

    @abstractmethod
    def serialize(self, record: RecordT) -> WireT:
        """Serialize one record without performing filesystem effects.

        Parameters
        ----------
        record
            Exact record accepted by the concrete serializer.

        Returns
        -------
        WireT
            JSON text or UTF-8 JSON bytes owned by the concrete wire contract.

        Raises
        ------
        TypeError
            The record does not satisfy the concrete serializer boundary.
        ValueError
            The record contains a value forbidden by the concrete wire contract.
        """


class JsonDeserializer[RecordT, WireT: (str, bytes)](ABC):
    """Deserialize one JSON wire representation to one exact record type."""

    __slots__ = ()

    @abstractmethod
    def deserialize(self, wire: WireT) -> RecordT:
        """Deserialize one wire value without performing filesystem effects.

        Parameters
        ----------
        wire
            JSON text or bytes accepted by the concrete decoder.

        Returns
        -------
        RecordT
            Reconstructed exact record type.

        Raises
        ------
        TypeError
            The wire type or a decoded value has the wrong type.
        ValueError
            The JSON document or decoded record violates the concrete contract.
        """


class JsonCodec[RecordT, WireT: (str, bytes)](
    JsonSerializer[RecordT, WireT],
    JsonDeserializer[RecordT, WireT],
    ABC,
):
    """Combine matching JSON serialization and deserialization contracts."""

    __slots__ = ()
