"""Version-two input decoding for the core particle-in-a-box residual study."""

from __future__ import annotations

import json
from typing import cast

import numpy as np
from projectkoios.physkit.qm.piab1d import Piab1D
from projectkoios.physkit.units import UnitSystem

from .records import Piab1dStudyDefinition

type JsonValue = (
    None | bool | int | float | str | list[JsonValue] | dict[str, JsonValue]
)


class Piab1dStudyInputDeserializer:
    """Decode the retained version-two JSON input into a closed definition."""

    __slots__ = ()

    def execute(self, payload: bytes) -> Piab1dStudyDefinition:
        """Decode one retained version-two study definition.

        Parameters
        ----------
        payload
            UTF-8 JSON bytes containing the historical input schema.

        Returns
        -------
        Piab1dStudyDefinition
            Immutable validated historical study definition.

        Raises
        ------
        TypeError
            The payload or a decoded field has the wrong exact type.
        ValueError
            JSON syntax, field inventory, or a study invariant is invalid.
        """
        if not isinstance(payload, bytes):
            raise TypeError("payload must be bytes")
        decoded = cast(JsonValue, json.loads(payload.decode("utf-8")))
        root = self.mapping(decoded, "experiment input")
        expected = {
            "schema_version",
            "experiment_id",
            "evidence_status",
            "dimensionless_parameters",
            "finite_representation",
            "boundary_reference",
        }
        if set(root) != expected:
            raise ValueError("experiment input fields do not match schema version 2")
        parameters = self.mapping(
            root["dimensionless_parameters"], "dimensionless_parameters"
        )
        representation = self.mapping(
            root["finite_representation"], "finite_representation"
        )
        boundary = self.mapping(root["boundary_reference"], "boundary_reference")
        if set(parameters) != {
            "length",
            "mass",
            "interior_points",
            "retained_dimension",
        }:
            raise ValueError("dimensionless_parameters fields do not match schema 2")
        if set(representation) != {"quadrature"}:
            raise ValueError("finite_representation fields do not match schema 2")
        if set(boundary) != {"kind", "interpretation"}:
            raise ValueError("boundary_reference fields do not match schema 2")
        if self.integer(root["schema_version"], "schema_version") != 2:
            raise ValueError("unsupported study input schema version")
        if self.string(root["experiment_id"], "experiment_id") != (
            "research-monograph.particle-in-box.v2"
        ):
            raise ValueError("unsupported PIAB1D experiment identity")
        if self.string(root["evidence_status"], "evidence_status") != (
            "illustrative numerical experiment"
        ):
            raise ValueError("unsupported PIAB1D evidence classification")
        if self.string(boundary.get("kind"), "boundary kind") != (
            "cyclic closure on the same finite coordinate space"
        ):
            raise ValueError("unsupported historical boundary reference")
        if self.string(boundary.get("interpretation"), "boundary interpretation") != (
            "Declared comparison reference only; not a "
            "representation-independent continuum potential."
        ):
            raise ValueError("unsupported historical boundary interpretation")
        return Piab1dStudyDefinition(
            model=Piab1D(
                length=self.positive_real(parameters.get("length"), "length"),
                mass=self.positive_real(parameters.get("mass"), "mass"),
                unit_system=UnitSystem.NONDIMENSIONAL,
            ),
            Nx_pts_interior=self.positive_integer(
                parameters.get("interior_points"), "interior_points"
            ),
            N_retained_eigenpairs=self.positive_integer(
                parameters.get("retained_dimension"), "retained_dimension"
            ),
            quadrature=self.boolean(representation.get("quadrature"), "quadrature"),
        )

    @staticmethod
    def mapping(value: JsonValue, name: str) -> dict[str, JsonValue]:
        """Validate and return a JSON object with string keys.

        Parameters
        ----------
        value
            Decoded JSON value.
        name
            Field name used in failure messages.

        Returns
        -------
        Mapping[str, JsonValue]
            Validated mapping.

        Raises
        ------
        TypeError
            The value is not a string-keyed mapping.
        """
        if not isinstance(value, dict) or not all(
            isinstance(key, str) for key in value
        ):
            raise TypeError(f"{name} must be a JSON object")
        return value

    @staticmethod
    def string(value: JsonValue, name: str) -> str:
        """Validate and return a nonempty JSON string.

        Parameters
        ----------
        value
            Decoded JSON value.
        name
            Field name used in failure messages.

        Returns
        -------
        str
            Nonempty built-in string.

        Raises
        ------
        TypeError
            The value is not a nonempty built-in string.
        """
        if not isinstance(value, str) or not value:
            raise TypeError(f"{name} must be a nonempty string")
        return value

    @staticmethod
    def integer(value: JsonValue, name: str) -> int:
        """Validate and return a built-in integer excluding booleans.

        Parameters
        ----------
        value
            Decoded JSON value.
        name
            Field name used in failure messages.

        Returns
        -------
        int
            Exact built-in integer.

        Raises
        ------
        TypeError
            The value is a Boolean or not a built-in integer.
        """
        if isinstance(value, bool) or not isinstance(value, int):
            raise TypeError(f"{name} must be a JSON integer")
        return value

    @staticmethod
    def boolean(value: JsonValue, name: str) -> bool:
        """Validate and return a JSON Boolean without numeric coercion.

        Parameters
        ----------
        value
            Decoded JSON value.
        name
            Field name used in failure messages.

        Returns
        -------
        bool
            Exact Boolean value.

        Raises
        ------
        TypeError
            The value is not a built-in Boolean.
        """
        if type(value) is not bool:
            raise TypeError(f"{name} must be a JSON Boolean")
        return value

    @classmethod
    def positive_integer(cls, value: JsonValue, name: str) -> int:
        """Validate and return a positive built-in integer.

        Parameters
        ----------
        value
            Decoded JSON value.
        name
            Field name used in failure messages.

        Returns
        -------
        int
            Positive exact integer.

        Raises
        ------
        TypeError
            The value is not an exact integer.
        ValueError
            The integer is not positive.
        """
        result = cls.integer(value, name)
        if result <= 0:
            raise ValueError(f"{name} must be positive")
        return result

    @staticmethod
    def positive_real(value: JsonValue, name: str) -> float:
        """Validate and return a positive finite real excluding booleans.

        Parameters
        ----------
        value
            Decoded JSON value.
        name
            Field name used in failure messages.

        Returns
        -------
        float
            Positive finite built-in floating-point value.

        Raises
        ------
        TypeError
            The value is Boolean or not a built-in integer or float.
        ValueError
            The converted value is nonfinite or nonpositive.
        """
        if isinstance(value, bool) or not isinstance(value, int | float):
            raise TypeError(f"{name} must be a positive JSON number")
        result = float(value)
        if not np.isfinite(result) or result <= 0.0:
            raise ValueError(f"{name} must be positive and finite")
        return result
