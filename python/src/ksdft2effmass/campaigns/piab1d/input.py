"""Version-one input decoding for the core particle-in-a-box residual study."""

from __future__ import annotations

import json
from typing import cast

import numpy as np

from .records import ParticleInBoxStudyDefinition

type JsonValue = (
    None | bool | int | float | str | list[JsonValue] | dict[str, JsonValue]
)


class ParticleInBoxStudyInputDeserializer:
    """Decode the retained version-one JSON input into a closed definition."""

    __slots__ = ()

    def execute(self, payload: bytes) -> ParticleInBoxStudyDefinition:
        """Return one validated definition decoded from UTF-8 JSON bytes."""
        if not isinstance(payload, bytes):
            raise TypeError("payload must be bytes")
        decoded = cast(JsonValue, json.loads(payload.decode("utf-8")))
        root = self.mapping(decoded, "experiment input")
        expected = {
            "schema_version",
            "experiment_id",
            "evidence_status",
            "dimensionless_parameters",
            "boundary_reference",
        }
        if set(root) != expected:
            raise ValueError("experiment input fields do not match schema version 1")
        parameters = self.mapping(
            root["dimensionless_parameters"], "dimensionless_parameters"
        )
        boundary = self.mapping(root["boundary_reference"], "boundary_reference")
        return ParticleInBoxStudyDefinition(
            schema_version=self.integer(root["schema_version"], "schema_version"),
            experiment_id=self.string(root["experiment_id"], "experiment_id"),
            evidence_status=self.string(root["evidence_status"], "evidence_status"),
            length=self.positive_real(parameters.get("length"), "length"),
            mass=self.positive_real(parameters.get("mass"), "mass"),
            hbar=self.positive_real(parameters.get("hbar"), "hbar"),
            interior_points=self.positive_integer(
                parameters.get("interior_points"), "interior_points"
            ),
            retained_dimension=self.positive_integer(
                parameters.get("retained_dimension"), "retained_dimension"
            ),
            boundary_kind=self.string(boundary.get("kind"), "boundary kind"),
            boundary_interpretation=self.string(
                boundary.get("interpretation"), "boundary interpretation"
            ),
        )

    @staticmethod
    def mapping(value: JsonValue, name: str) -> dict[str, JsonValue]:
        """Return a JSON object with string keys."""
        if not isinstance(value, dict) or not all(
            isinstance(key, str) for key in value
        ):
            raise TypeError(f"{name} must be a JSON object")
        return value

    @staticmethod
    def string(value: JsonValue, name: str) -> str:
        """Return a nonempty JSON string."""
        if not isinstance(value, str) or not value:
            raise TypeError(f"{name} must be a nonempty string")
        return value

    @staticmethod
    def integer(value: JsonValue, name: str) -> int:
        """Return a built-in JSON integer excluding booleans."""
        if isinstance(value, bool) or not isinstance(value, int):
            raise TypeError(f"{name} must be a JSON integer")
        return value

    @classmethod
    def positive_integer(cls, value: JsonValue, name: str) -> int:
        """Return a positive built-in JSON integer."""
        result = cls.integer(value, name)
        if result <= 0:
            raise ValueError(f"{name} must be positive")
        return result

    @staticmethod
    def positive_real(value: JsonValue, name: str) -> float:
        """Return a positive finite JSON real excluding booleans."""
        if isinstance(value, bool) or not isinstance(value, int | float):
            raise TypeError(f"{name} must be a positive JSON number")
        result = float(value)
        if not np.isfinite(result) or result <= 0.0:
            raise ValueError(f"{name} must be positive and finite")
        return result
