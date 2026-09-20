"""Private typed JSON decoding mechanics for periodic-1D campaign serializers."""

from __future__ import annotations

import json

import numpy as np

from ksdft2effmass.operators import ScalarQuantity, Unitless, VectorQuantity


class Periodic1DCampaignJsonDecoder:
    """Decode JSON bytes and exact closed primitive representations."""

    __slots__ = ()

    def document(self, payload: bytes) -> dict[str, object]:
        """Decode one UTF-8 JSON object with built-in string keys."""
        if type(payload) is not bytes:
            raise TypeError("payload must be bytes")
        try:
            decoded: object = json.loads(payload.decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError) as error:
            raise ValueError("payload must be valid UTF-8 JSON") from error
        return self.mapping(decoded, "root")

    def mapping(self, value: object, name: str) -> dict[str, object]:
        """Return one exact string-keyed JSON object representation."""
        if not isinstance(value, dict) or any(type(key) is not str for key in value):
            raise TypeError(f"{name} must be a JSON object with string keys")
        return {str(key): item for key, item in value.items()}

    def array(self, value: object, name: str) -> list[object]:
        """Return one exact JSON array representation."""
        if not isinstance(value, list):
            raise TypeError(f"{name} must be a JSON array")
        return value

    def string(self, value: object, name: str) -> str:
        """Return one exact built-in string."""
        if type(value) is not str:
            raise TypeError(f"{name} must be a string")
        return value

    def integer(self, value: object, name: str) -> int:
        """Return one exact built-in integer while rejecting booleans."""
        if type(value) is not int:
            raise TypeError(f"{name} must be an integer")
        return value

    def real(self, value: object, name: str) -> float:
        """Return a finite built-in real converted to binary64."""
        if isinstance(value, bool) or not isinstance(value, int | float):
            raise TypeError(f"{name} must be a real number")
        converted = float(value)
        if not np.isfinite(converted):
            raise ValueError(f"{name} must be finite")
        return converted

    def scalar(self, value: object, name: str) -> ScalarQuantity:
        """Return one explicitly unitless scalar quantity."""
        return ScalarQuantity(self.real(value, name), Unitless())

    def vector(self, value: object, name: str) -> VectorQuantity:
        """Return one explicitly unitless binary64 vector quantity."""
        return VectorQuantity(
            np.asarray(
                [self.real(item, name) for item in self.array(value, name)],
                dtype=np.float64,
            ),
            Unitless(),
        )

    def integers(self, value: object, name: str) -> tuple[int, ...]:
        """Return one tuple of exact built-in integers."""
        return tuple(self.integer(item, name) for item in self.array(value, name))
