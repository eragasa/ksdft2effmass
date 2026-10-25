"""Version-one input decoding for the Mathieu1d reduction study."""

from __future__ import annotations

import json
from typing import cast

import numpy as np
from projectkoios.physkit.units import (
    ScalarQuantity,
    Unitless,
    VectorQuantity,
)

from ksdft2effmass.analysis.single_band_reduction import (
    SingleBandHoppingReductionTolerances1D,
)
from ksdft2effmass.model_systems.periodic_1d import PeriodicFourierPotential1D
from ksdft2effmass.periodic1d.model import Periodic1DFourierHamiltonianToyModel

from .records import Mathieu1dStudyDefinition

type JsonValue = (
    None | bool | int | float | str | list[JsonValue] | dict[str, JsonValue]
)


class Mathieu1dStudyInputDeserializer:
    """Deserialize the closed version-one Mathieu1d study input."""

    __slots__ = ()

    def execute(self, payload: bytes) -> Mathieu1dStudyDefinition:
        """Return one validated study definition from UTF-8 JSON bytes."""
        if not isinstance(payload, bytes):
            raise TypeError("payload must be bytes")
        root = self.mapping(
            cast(JsonValue, json.loads(payload.decode("utf-8"))), "input"
        )
        self.exact_fields(
            root,
            {
                "schema",
                "identity",
                "model",
                "parent_representation",
                "reduction",
                "tolerances",
                "scope",
            },
            "input",
        )
        if self.string(root["schema"], "schema") != (
            "ksdft2effmass.campaign.periodic-reduction.periodic1d."
            "single-band-fourier-reduction.v1.input.v1"
        ):
            raise ValueError("unsupported Mathieu1d study input schema")
        self.validate_identity(self.mapping(root["identity"], "identity"))
        self.validate_scope(self.mapping(root["scope"], "scope"))

        model_wire = self.mapping(root["model"], "model")
        self.exact_fields(
            model_wire,
            {
                "identity",
                "model_role",
                "period",
                "constant_coefficient",
                "cosine_coefficients",
                "sine_coefficients",
                "reciprocal_vector",
                "recoil_energy",
                "duality_absolute_tolerance",
            },
            "model",
        )
        if self.string(model_wire["model_role"], "model_role") != "toy":
            raise ValueError("version-one model_role must be toy")
        unit = Unitless()
        potential = PeriodicFourierPotential1D(
            period=self.scalar_quantity(model_wire["period"], "period", unit),
            constant_coefficient=self.scalar_quantity(
                model_wire["constant_coefficient"], "constant_coefficient", unit
            ),
            cosine_coefficients=self.vector_quantity(
                model_wire["cosine_coefficients"], "cosine_coefficients", unit
            ),
            sine_coefficients=self.vector_quantity(
                model_wire["sine_coefficients"], "sine_coefficients", unit
            ),
        )
        model = Periodic1DFourierHamiltonianToyModel(
            identity=self.string(model_wire["identity"], "model identity"),
            potential=potential,
            reciprocal_vector=self.scalar_quantity(
                model_wire["reciprocal_vector"], "reciprocal_vector", unit
            ),
            recoil_energy=self.scalar_quantity(
                model_wire["recoil_energy"], "recoil_energy", unit
            ),
            duality_absolute_tolerance=self.real(
                model_wire["duality_absolute_tolerance"],
                "duality_absolute_tolerance",
            ),
        )

        parent = self.mapping(root["parent_representation"], "parent_representation")
        self.exact_fields(
            parent,
            {
                "plane_wave_cutoffs",
                "plane_wave_reference_cutoff",
                "production_plane_wave_cutoff",
                "finite_difference_points",
                "sample_reduced_momenta",
                "compared_band_count",
            },
            "parent_representation",
        )
        reduction = self.mapping(root["reduction"], "reduction")
        self.exact_fields(
            reduction,
            {
                "selected_band_index",
                "training_reduced_momenta",
                "evaluation_reduced_momenta",
                "hopping_ranges",
                "fitting_weights",
            },
            "reduction",
        )
        training = self.real_sequence(
            reduction["training_reduced_momenta"], "training_reduced_momenta"
        )
        tolerances_wire = self.mapping(root["tolerances"], "tolerances")
        self.exact_fields(
            tolerances_wire,
            {
                "coordinate_absolute",
                "reconstruction_absolute",
                "hermiticity_absolute",
                "parseval_absolute",
                "imaginary_absolute",
            },
            "tolerances",
        )
        definition = Mathieu1dStudyDefinition(
            parent_model=model,
            plane_wave_cutoffs=self.integer_sequence(
                parent["plane_wave_cutoffs"], "plane_wave_cutoffs"
            ),
            plane_wave_reference_cutoff=self.integer(
                parent["plane_wave_reference_cutoff"], "plane_wave_reference_cutoff"
            ),
            production_plane_wave_cutoff=self.integer(
                parent["production_plane_wave_cutoff"],
                "production_plane_wave_cutoff",
            ),
            finite_difference_points=self.integer_sequence(
                parent["finite_difference_points"], "finite_difference_points"
            ),
            parent_sample_reduced_momenta=self.real_sequence(
                parent["sample_reduced_momenta"], "sample_reduced_momenta"
            ),
            compared_band_count=self.integer(
                parent["compared_band_count"], "compared_band_count"
            ),
            selected_band_index=self.integer(
                reduction["selected_band_index"], "selected_band_index"
            ),
            reciprocal_training_mesh_size=len(training),
            evaluation_reduced_momenta=self.real_sequence(
                reduction["evaluation_reduced_momenta"],
                "evaluation_reduced_momenta",
            ),
            hopping_ranges=self.integer_sequence(
                reduction["hopping_ranges"], "hopping_ranges"
            ),
            fitting_weights=self.real_sequence(
                reduction["fitting_weights"], "fitting_weights"
            ),
            tolerances=SingleBandHoppingReductionTolerances1D(
                coordinate_absolute=self.scalar_quantity(
                    tolerances_wire["coordinate_absolute"],
                    "coordinate_absolute",
                    unit,
                ),
                reconstruction_absolute=self.scalar_quantity(
                    tolerances_wire["reconstruction_absolute"],
                    "reconstruction_absolute",
                    unit,
                ),
                hermiticity_absolute=self.scalar_quantity(
                    tolerances_wire["hermiticity_absolute"],
                    "hermiticity_absolute",
                    unit,
                ),
                parseval_absolute=self.scalar_quantity(
                    tolerances_wire["parseval_absolute"],
                    "parseval_absolute",
                    unit,
                ),
                imaginary_absolute=self.scalar_quantity(
                    tolerances_wire["imaginary_absolute"],
                    "imaginary_absolute",
                    unit,
                ),
            ),
        )
        if definition.training_reduced_momenta != training:
            raise ValueError(
                "training_reduced_momenta must be the complete centered mesh"
            )
        return definition

    @staticmethod
    def validate_identity(identity: dict[str, JsonValue]) -> None:
        """Require every frozen identity and convention field."""
        expected = {
            "family_id": (
                "ksdft2effmass.campaign.periodic-reduction.periodic1d."
                "single-band-fourier-reduction"
            ),
            "version_id": (
                "ksdft2effmass.campaign.periodic-reduction.periodic1d."
                "single-band-fourier-reduction.v1"
            ),
            "energy_reference_id": "parent-model-fixed-zero-no-post-fit-shift.v1",
            "fourier_convention_id": (
                "forward-negative-exponent-inverse-positive-exponent.v1"
            ),
            "fourier_normalization_id": ("forward-one-over-n-inverse-unit.v1"),
            "objective_construction_role_id": ("complete-centered-training-mesh.v1"),
            "objective_evaluation_role_id": ("disjoint-staggered-evaluation-mesh.v1"),
        }
        if identity != expected:
            raise ValueError(
                "identity does not match the immutable version-one contract"
            )

    @staticmethod
    def validate_scope(scope: dict[str, JsonValue]) -> None:
        """Require the bounded version-one evidence classification."""
        expected: dict[str, JsonValue] = {
            "evidence_class": "controlled-synthetic-numerical-verification",
            "external_calculator_execution": False,
            "scientific_acceptance": False,
            "material_validation": False,
            "uncertainty_quantification": False,
        }
        if scope != expected:
            raise ValueError("scope does not match the version-one evidence boundary")

    @staticmethod
    def exact_fields(
        value: dict[str, JsonValue], expected: set[str], name: str
    ) -> None:
        """Require one exact closed field inventory."""
        if set(value) != expected:
            raise ValueError(f"{name} fields do not match the closed contract")

    @staticmethod
    def mapping(value: JsonValue, name: str) -> dict[str, JsonValue]:
        """Require one JSON object."""
        if not isinstance(value, dict):
            raise TypeError(f"{name} must be a JSON object")
        return value

    @staticmethod
    def string(value: JsonValue, name: str) -> str:
        """Require one nonempty string."""
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
        """Convert one JSON array to a tuple of built-in floats."""
        if not isinstance(value, list):
            raise TypeError(f"{name} must be a JSON array")
        return tuple(self.real(item, name) for item in value)

    def integer_sequence(self, value: JsonValue, name: str) -> tuple[int, ...]:
        """Convert one JSON array to a tuple of built-in integers."""
        if not isinstance(value, list):
            raise TypeError(f"{name} must be a JSON array")
        return tuple(self.integer(item, name) for item in value)

    def scalar_quantity(
        self, value: JsonValue, name: str, unit: Unitless
    ) -> ScalarQuantity:
        """Decode one version-one dimensionless scalar quantity."""
        quantity = self.mapping(value, name)
        self.exact_fields(quantity, {"magnitude", "unit"}, name)
        if self.string(quantity["unit"], f"{name} unit") != unit.expression:
            raise ValueError(f"{name} must be dimensionless")
        return ScalarQuantity(self.real(quantity["magnitude"], name), unit)

    def vector_quantity(
        self, value: JsonValue, name: str, unit: Unitless
    ) -> VectorQuantity:
        """Decode one version-one dimensionless vector quantity."""
        quantity = self.mapping(value, name)
        self.exact_fields(quantity, {"magnitude", "unit"}, name)
        if self.string(quantity["unit"], f"{name} unit") != unit.expression:
            raise ValueError(f"{name} must be dimensionless")
        return VectorQuantity(
            np.asarray(self.real_sequence(quantity["magnitude"], name)), unit
        )


__all__ = ["Mathieu1dStudyInputDeserializer"]
