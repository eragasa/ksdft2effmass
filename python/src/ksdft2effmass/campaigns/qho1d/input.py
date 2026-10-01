"""Version-one input decoding for the harmonic-oscillator study."""

from __future__ import annotations

import json
from typing import cast

import numpy as np

from ksdft2effmass.analysis.model_systems.harmonic_oscillator import (
    HarmonicOscillatorNondimensionalizer,
)

from .records import HarmonicOscillatorStudyDefinition

type JsonValue = (
    None | bool | int | float | str | list[JsonValue] | dict[str, JsonValue]
)


class HarmonicOscillatorStudyInputDeserializer:
    """Deserialize the closed version-one monograph study input.

    The deserializer accepts UTF-8 JSON bytes, rejects unknown fields and unsupported
    versions, and converts exact wire values into a
    ``HarmonicOscillatorStudyDefinition``. Schema success is a wire-format result,
    not numerical or scientific verification.
    """

    __slots__ = ()

    def execute(self, payload: bytes) -> HarmonicOscillatorStudyDefinition:
        """Deserialize one version-one study definition.

        Parameters
        ----------
        payload
            UTF-8 encoded JSON object bytes.

        Returns
        -------
        HarmonicOscillatorStudyDefinition
            Validated immutable study definition.

        Raises
        ------
        UnicodeDecodeError
            If ``payload`` is not valid UTF-8.
        json.JSONDecodeError
            If ``payload`` is not valid JSON.
        TypeError
            If a wire value has the wrong semantic JSON type.
        ValueError
            If fields, version, or values violate the closed contract.
        """
        if not isinstance(payload, bytes):
            raise TypeError("payload must be bytes")
        value = cast(JsonValue, json.loads(payload.decode("utf-8")))
        root = self.mapping(value, "input")
        expected = {
            "schema_version",
            "experiment_id",
            "evidence_status",
            "dimensionless_convention",
            "box_half_widths",
            "grid_spacings",
            "retained_dimensions",
            "spatial_representation",
            "comparison_map",
        }
        if set(root) != expected:
            raise ValueError("study input fields do not match schema version 1")
        if self.integer(root["schema_version"], "schema_version") != 1:
            raise ValueError("unsupported study input schema version")
        constants = self.mapping(
            root["dimensionless_convention"], "dimensionless_convention"
        )
        if set(constants) != {"hbar", "mass", "omega", "oscillator_length"}:
            raise ValueError("dimensionless_convention fields are not closed")
        parameters = HarmonicOscillatorNondimensionalizer().execute(
            hbar=self.real(constants["hbar"], "hbar"),
            mass=self.real(constants["mass"], "mass"),
            omega=self.real(constants["omega"], "omega"),
        )
        oscillator_length = self.real(
            constants["oscillator_length"], "oscillator_length"
        )
        if oscillator_length != parameters.oscillator_length.magnitude:
            raise ValueError("oscillator_length must equal sqrt(hbar/(mass*omega))")
        return HarmonicOscillatorStudyDefinition(
            study_id=self.string(root["experiment_id"], "experiment_id"),
            evidence_status=self.string(root["evidence_status"], "evidence_status"),
            parameters=parameters,
            box_half_widths=self.real_sequence(
                root["box_half_widths"], "box_half_widths"
            ),
            grid_spacings=self.real_sequence(root["grid_spacings"], "grid_spacings"),
            retained_dimensions=self.integer_sequence(
                root["retained_dimensions"], "retained_dimensions"
            ),
            spatial_representation=self.string(
                root["spatial_representation"], "spatial_representation"
            ),
            comparison_map=self.string(root["comparison_map"], "comparison_map"),
        )

    @staticmethod
    def mapping(value: JsonValue, name: str) -> dict[str, JsonValue]:
        """Require one JSON object with string keys."""
        if not isinstance(value, dict) or not all(
            isinstance(key, str) for key in value
        ):
            raise TypeError(f"{name} must be a JSON object")
        return value

    @staticmethod
    def string(value: JsonValue, name: str) -> str:
        """Require one nonempty JSON string."""
        if not isinstance(value, str) or not value:
            raise TypeError(f"{name} must be a nonempty string")
        return value

    @staticmethod
    def real(value: JsonValue, name: str) -> float:
        """Require one finite JSON number excluding Boolean values."""
        if isinstance(value, bool) or not isinstance(value, int | float):
            raise TypeError(f"{name} must be a JSON number")
        result = float(value)
        if not np.isfinite(result):
            raise ValueError(f"{name} must be finite")
        return result

    @staticmethod
    def integer(value: JsonValue, name: str) -> int:
        """Require one JSON integer excluding Boolean values."""
        if isinstance(value, bool) or not isinstance(value, int):
            raise TypeError(f"{name} must be a JSON integer")
        return value

    def real_sequence(self, value: JsonValue, name: str) -> tuple[float, ...]:
        """Convert one JSON array to a built-in-float tuple."""
        if not isinstance(value, list):
            raise TypeError(f"{name} must be a JSON array")
        return tuple(self.real(item, name) for item in value)

    def integer_sequence(self, value: JsonValue, name: str) -> tuple[int, ...]:
        """Convert one JSON array to a built-in-integer tuple."""
        if not isinstance(value, list):
            raise TypeError(f"{name} must be a JSON array")
        return tuple(self.integer(item, name) for item in value)
