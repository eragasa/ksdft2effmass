"""Versioned Appendix G periodic-reduction stress campaign contract."""

from __future__ import annotations

import json
import warnings
from dataclasses import dataclass

import numpy as np

from ksdft2effmass.analysis.model_systems.periodic_1d import (
    PeriodicFourierPotential1D,
)
from ksdft2effmass.operators import ScalarQuantity, Unitless, VectorQuantity
from ksdft2effmass.serialization import JsonCodec

from .serialization import Periodic1DCampaignJsonDecoder


@dataclass(frozen=True, slots=True, eq=False)
class Periodic1DStressPotentialShape:
    """Bind a stable stress-case identifier to one dimensionless Fourier shape."""

    identifier: str
    potential: PeriodicFourierPotential1D

    def __post_init__(self) -> None:
        """Validate identifier and explicitly unitless Fourier model."""
        if type(self.identifier) is not str:
            raise TypeError("identifier must be a built-in str")
        if not self.identifier:
            raise ValueError("identifier must be nonempty")
        if type(self.potential) is not PeriodicFourierPotential1D:
            raise TypeError("potential must be PeriodicFourierPotential1D")
        quantities = (
            self.potential.period,
            self.potential.constant_coefficient,
            self.potential.cosine_coefficients,
            self.potential.sine_coefficients,
        )
        if any(not isinstance(quantity.unit, Unitless) for quantity in quantities):
            raise ValueError("stress potential shapes must be explicitly unitless")


@dataclass(frozen=True, slots=True, eq=False)
class Periodic1DStressCampaignDefinition:
    """Retain the closed version-one Appendix G stress-study controls."""

    experiment_id: str
    potential_strengths: VectorQuantity
    plane_wave_cutoffs: tuple[int, ...]
    plane_wave_reference_cutoff: int
    finite_difference_points: tuple[int, ...]
    compared_band_count: int
    stress_band_indices: tuple[int, ...]
    potential_shapes: tuple[Periodic1DStressPotentialShape, ...]
    reciprocal_mesh_sizes: tuple[int, ...]
    hopping_range_cells: int
    withheld_mesh_size: int
    isolation_gap_threshold: ScalarQuantity
    route_stress_potential_strength: ScalarQuantity
    route_stress_mesh_size: int
    route_stress_hopping_range_cells: int

    def __post_init__(self) -> None:
        """Validate unitless values and deterministic ordered inventories."""
        if type(self.experiment_id) is not str or not self.experiment_id:
            raise ValueError("experiment_id must be a nonempty built-in str")
        if type(self.potential_strengths) is not VectorQuantity:
            raise TypeError("potential_strengths must be VectorQuantity")
        if not isinstance(self.potential_strengths.unit, Unitless):
            raise ValueError("potential_strengths must be unitless")
        if self.potential_strengths.magnitude.size == 0:
            raise ValueError("potential_strengths must be nonempty")
        for quantity_name, quantity in (
            ("isolation_gap_threshold", self.isolation_gap_threshold),
            (
                "route_stress_potential_strength",
                self.route_stress_potential_strength,
            ),
        ):
            if type(quantity) is not ScalarQuantity:
                raise TypeError(f"{quantity_name} must be ScalarQuantity")
            if not isinstance(quantity.unit, Unitless):
                raise ValueError(f"{quantity_name} must be unitless")
        if self.isolation_gap_threshold.magnitude <= 0.0:
            raise ValueError("isolation_gap_threshold must be positive")
        for inventory_name, inventory in (
            ("plane_wave_cutoffs", self.plane_wave_cutoffs),
            ("finite_difference_points", self.finite_difference_points),
            ("stress_band_indices", self.stress_band_indices),
            ("reciprocal_mesh_sizes", self.reciprocal_mesh_sizes),
        ):
            if (
                not isinstance(inventory, tuple)
                or not inventory
                or any(type(item) is not int for item in inventory)
            ):
                raise TypeError(f"{inventory_name} must be a nonempty integer tuple")
            if tuple(sorted(set(inventory))) != inventory:
                raise ValueError(f"{inventory_name} must be unique and increasing")
        for integer_name, integer_value in (
            ("plane_wave_reference_cutoff", self.plane_wave_reference_cutoff),
            ("compared_band_count", self.compared_band_count),
            ("hopping_range_cells", self.hopping_range_cells),
            ("withheld_mesh_size", self.withheld_mesh_size),
            ("route_stress_mesh_size", self.route_stress_mesh_size),
            (
                "route_stress_hopping_range_cells",
                self.route_stress_hopping_range_cells,
            ),
        ):
            if type(integer_value) is not int:
                raise TypeError(f"{integer_name} must be a built-in int")
            if integer_value <= 0:
                raise ValueError(f"{integer_name} must be positive")
        if not isinstance(self.potential_shapes, tuple) or not self.potential_shapes:
            raise TypeError("potential_shapes must be a nonempty tuple")
        if any(
            type(shape) is not Periodic1DStressPotentialShape
            for shape in self.potential_shapes
        ):
            raise TypeError("every potential shape must use the owned record")
        identifiers = tuple(shape.identifier for shape in self.potential_shapes)
        if len(set(identifiers)) != len(identifiers):
            raise ValueError("potential shape identifiers must be unique")
        if self.stress_band_indices[-1] >= self.compared_band_count:
            raise ValueError("stress band index lies outside compared bands")
        if self.plane_wave_cutoffs[0] <= 0:
            raise ValueError("plane_wave_cutoffs must be positive")
        if self.finite_difference_points[0] <= 0:
            raise ValueError("finite_difference_points must be positive")
        if self.reciprocal_mesh_sizes[0] <= 0:
            raise ValueError("reciprocal_mesh_sizes must be positive")
        if self.plane_wave_reference_cutoff <= self.plane_wave_cutoffs[-1]:
            raise ValueError("reference cutoff must exceed every sweep cutoff")
        if self.route_stress_mesh_size not in self.reciprocal_mesh_sizes:
            raise ValueError("route stress mesh must occur in reciprocal mesh sizes")
        if self.route_stress_hopping_range_cells != self.hopping_range_cells:
            raise ValueError("route stress and primary hopping ranges must agree")
        reference_period = self.potential_shapes[0].potential.period.magnitude
        if any(
            not np.isclose(
                shape.potential.period.magnitude,
                reference_period,
                rtol=0.0,
                atol=0.0,
            )
            for shape in self.potential_shapes[1:]
        ):
            raise ValueError("all stress potential shapes must use one period")

    @property
    def period(self) -> ScalarQuantity:
        """Return the explicit common period of all stress potential shapes."""
        return self.potential_shapes[0].potential.period


class Periodic1DStressCampaignJsonSerializer(
    JsonCodec[Periodic1DStressCampaignDefinition, bytes]
):
    """Decode and canonically encode the retained stress input."""

    __slots__ = ()

    decoder = Periodic1DCampaignJsonDecoder()

    def deserialize(self, payload: bytes) -> Periodic1DStressCampaignDefinition:
        """Decode strict version-one JSON without running any stress case."""
        root = self.decoder.document(payload)
        expected = {
            "schema_version",
            "experiment_id",
            "evidence_status",
            "potential_strengths",
            "plane_wave_cutoffs",
            "plane_wave_reference_cutoff",
            "finite_difference_points",
            "compared_band_count",
            "stress_band_indices",
            "potential_shapes",
            "reciprocal_mesh_sizes",
            "hopping_range_cells",
            "withheld_mesh_size",
            "isolation_gap_threshold",
            "route_stress_potential_strength",
            "route_stress_mesh_size",
            "route_stress_hopping_range_cells",
        }
        if set(root) != expected:
            raise ValueError("stress input fields must match schema version one")
        if self.decoder.integer(root["schema_version"], "schema_version") != 1:
            raise ValueError("unsupported stress input schema version")
        if (
            self.decoder.string(root["evidence_status"], "evidence_status")
            != "illustrative numerical stress test"
        ):
            raise ValueError("unexpected evidence_status")
        return Periodic1DStressCampaignDefinition(
            self.decoder.string(root["experiment_id"], "experiment_id"),
            self.decoder.vector(root["potential_strengths"], "potential_strengths"),
            self.decoder.integers(root["plane_wave_cutoffs"], "plane_wave_cutoffs"),
            self.decoder.integer(
                root["plane_wave_reference_cutoff"], "plane_wave_reference_cutoff"
            ),
            self.decoder.integers(
                root["finite_difference_points"], "finite_difference_points"
            ),
            self.decoder.integer(root["compared_band_count"], "compared_band_count"),
            self.decoder.integers(root["stress_band_indices"], "stress_band_indices"),
            tuple(
                self.decode_shape(item)
                for item in self.decoder.array(
                    root["potential_shapes"], "potential_shapes"
                )
            ),
            self.decoder.integers(
                root["reciprocal_mesh_sizes"], "reciprocal_mesh_sizes"
            ),
            self.decoder.integer(root["hopping_range_cells"], "hopping_range_cells"),
            self.decoder.integer(root["withheld_mesh_size"], "withheld_mesh_size"),
            self.decoder.scalar(
                root["isolation_gap_threshold"], "isolation_gap_threshold"
            ),
            self.decoder.scalar(
                root["route_stress_potential_strength"],
                "route_stress_potential_strength",
            ),
            self.decoder.integer(
                root["route_stress_mesh_size"], "route_stress_mesh_size"
            ),
            self.decoder.integer(
                root["route_stress_hopping_range_cells"],
                "route_stress_hopping_range_cells",
            ),
        )

    def serialize(self, value: Periodic1DStressCampaignDefinition) -> bytes:
        """Return canonical version-one UTF-8 JSON."""
        if type(value) is not Periodic1DStressCampaignDefinition:
            raise TypeError("value must be Periodic1DStressCampaignDefinition")
        document = {
            "schema_version": 1,
            "experiment_id": value.experiment_id,
            "evidence_status": "illustrative numerical stress test",
            "potential_strengths": value.potential_strengths.magnitude.tolist(),
            "plane_wave_cutoffs": list(value.plane_wave_cutoffs),
            "plane_wave_reference_cutoff": value.plane_wave_reference_cutoff,
            "finite_difference_points": list(value.finite_difference_points),
            "compared_band_count": value.compared_band_count,
            "stress_band_indices": list(value.stress_band_indices),
            "potential_shapes": [
                self.encode_shape(shape) for shape in value.potential_shapes
            ],
            "reciprocal_mesh_sizes": list(value.reciprocal_mesh_sizes),
            "hopping_range_cells": value.hopping_range_cells,
            "withheld_mesh_size": value.withheld_mesh_size,
            "isolation_gap_threshold": value.isolation_gap_threshold.magnitude,
            "route_stress_potential_strength": (
                value.route_stress_potential_strength.magnitude
            ),
            "route_stress_mesh_size": value.route_stress_mesh_size,
            "route_stress_hopping_range_cells": value.route_stress_hopping_range_cells,
        }
        return (
            json.dumps(document, sort_keys=True, separators=(",", ":")) + "\n"
        ).encode()

    def decode(self, payload: bytes) -> Periodic1DStressCampaignDefinition:
        """Deprecated compatibility alias for :meth:`deserialize`."""
        warnings.warn(
            "decode() is deprecated; use deserialize()",
            DeprecationWarning,
            stacklevel=2,
        )
        return self.deserialize(payload)

    def encode(self, value: Periodic1DStressCampaignDefinition) -> bytes:
        """Deprecated compatibility alias for :meth:`serialize`."""
        warnings.warn(
            "encode() is deprecated; use serialize()",
            DeprecationWarning,
            stacklevel=2,
        )
        return self.serialize(value)

    def decode_shape(self, value: object) -> Periodic1DStressPotentialShape:
        """Decode one named unitless Fourier potential shape."""
        shape = self.decoder.mapping(value, "potential shape")
        if set(shape) != {"id", "constant", "cosine_coefficients", "sine_coefficients"}:
            raise ValueError("potential shape fields are invalid")
        potential = PeriodicFourierPotential1D(
            ScalarQuantity(2.0 * np.pi, Unitless()),
            self.decoder.scalar(shape["constant"], "constant"),
            self.decoder.vector(shape["cosine_coefficients"], "cosine_coefficients"),
            self.decoder.vector(shape["sine_coefficients"], "sine_coefficients"),
        )
        return Periodic1DStressPotentialShape(
            self.decoder.string(shape["id"], "id"), potential
        )

    @staticmethod
    def encode_shape(shape: Periodic1DStressPotentialShape) -> dict[str, object]:
        """Encode one named unitless Fourier potential shape."""
        if type(shape) is not Periodic1DStressPotentialShape:
            raise TypeError("shape must be Periodic1DStressPotentialShape")
        return {
            "id": shape.identifier,
            "constant": shape.potential.constant_coefficient.magnitude,
            "cosine_coefficients": (
                shape.potential.cosine_coefficients.magnitude.tolist()
            ),
            "sine_coefficients": shape.potential.sine_coefficients.magnitude.tolist(),
        }
