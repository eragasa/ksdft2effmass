"""Canonical retained projection of Ragasa2026a/c finite-rank losses."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from typing import Self

from ksdft2effmass.serialization import BaseTypedRecord, SerializableValue

from ..loss import (
    BandEquivalenceHoppingLocalityComparisonIdentity,
    BandEquivalenceHoppingLocalityLoss,
    BandEquivalenceHoppingLocalityLossDefinition,
    BandEquivalenceHoppingLocalitySampleMeasure,
)


@dataclass(frozen=True, slots=True)
class BandEquivalenceHoppingLocalityLossRecord(BaseTypedRecord):
    """Retain one typed finite-rank loss definition and its calculated values."""

    spatial_dimension: int
    retained_rank: int
    sample_shape: tuple[int, ...]
    sample_weights: tuple[float, ...]
    sample_inventory_identifier: str
    retained_basis_identifier: str
    retained_space_identifier: str
    gauge_identifier: str
    geometry_identifier: str
    energy_unit_identifier: str
    energy_reference_identifier: str
    norm_energy_scale: float
    operator_loss: float
    spectral_loss: float

    def __post_init__(self) -> None:
        """Admit the record by reconstructing its scientific domain value."""
        self.to_analysis()

    @classmethod
    def from_analysis(cls, analysis: BandEquivalenceHoppingLocalityLoss) -> Self:
        """Project the scientific value without recomputing either loss."""
        if type(analysis) is not BandEquivalenceHoppingLocalityLoss:
            raise TypeError("analysis must be BandEquivalenceHoppingLocalityLoss")
        return cls(
            spatial_dimension=analysis.spatial_dimension,
            retained_rank=analysis.retained_rank,
            sample_shape=analysis.sample_shape,
            sample_weights=analysis.sample_weights,
            sample_inventory_identifier=analysis.sample_inventory_identifier,
            retained_basis_identifier=analysis.retained_basis_identifier,
            retained_space_identifier=analysis.retained_space_identifier,
            gauge_identifier=analysis.gauge_identifier,
            geometry_identifier=analysis.geometry_identifier,
            energy_unit_identifier=analysis.energy_unit_identifier,
            energy_reference_identifier=analysis.energy_reference_identifier,
            norm_energy_scale=analysis.norm_energy_scale,
            operator_loss=analysis.operator_loss,
            spectral_loss=analysis.spectral_loss,
        )

    def to_analysis(self) -> BandEquivalenceHoppingLocalityLoss:
        """Return the immutable scientific value represented by this record."""
        return BandEquivalenceHoppingLocalityLoss(
            definition=BandEquivalenceHoppingLocalityLossDefinition(
                retained_rank=self.retained_rank,
                sample_measure=BandEquivalenceHoppingLocalitySampleMeasure(
                    spatial_dimension=self.spatial_dimension,
                    sample_shape=self.sample_shape,
                    sample_weights=self.sample_weights,
                    sample_inventory_identifier=self.sample_inventory_identifier,
                ),
                comparison_identity=BandEquivalenceHoppingLocalityComparisonIdentity(
                    retained_basis_identifier=self.retained_basis_identifier,
                    retained_space_identifier=self.retained_space_identifier,
                    gauge_identifier=self.gauge_identifier,
                    geometry_identifier=self.geometry_identifier,
                    energy_unit_identifier=self.energy_unit_identifier,
                    energy_reference_identifier=self.energy_reference_identifier,
                ),
                norm_energy_scale=self.norm_energy_scale,
            ),
            operator_loss=self.operator_loss,
            spectral_loss=self.spectral_loss,
        )

    def _mapping(self) -> Mapping[str, SerializableValue]:
        return {
            "spatial_dimension": self.spatial_dimension,
            "retained_rank": self.retained_rank,
            "sample_shape": self.sample_shape,
            "sample_weights": self.sample_weights,
            "sample_inventory_identifier": self.sample_inventory_identifier,
            "retained_basis_identifier": self.retained_basis_identifier,
            "retained_space_identifier": self.retained_space_identifier,
            "gauge_identifier": self.gauge_identifier,
            "geometry_identifier": self.geometry_identifier,
            "energy_unit_identifier": self.energy_unit_identifier,
            "energy_reference_identifier": self.energy_reference_identifier,
            "norm_energy_scale": self.norm_energy_scale,
            "operator_loss": self.operator_loss,
            "spectral_loss": self.spectral_loss,
        }

    @classmethod
    def _from_mapping(cls, values: Mapping[str, SerializableValue]) -> Self:
        required = {
            "spatial_dimension",
            "retained_rank",
            "sample_shape",
            "sample_weights",
            "sample_inventory_identifier",
            "retained_basis_identifier",
            "retained_space_identifier",
            "gauge_identifier",
            "geometry_identifier",
            "energy_unit_identifier",
            "energy_reference_identifier",
            "norm_energy_scale",
            "operator_loss",
            "spectral_loss",
        }
        if set(values) != required:
            raise ValueError("finite-rank loss record fields do not match")
        spatial_dimension = values["spatial_dimension"]
        retained_rank = values["retained_rank"]
        sample_shape = values["sample_shape"]
        sample_weights = values["sample_weights"]
        sample_inventory_identifier = values["sample_inventory_identifier"]
        retained_basis_identifier = values["retained_basis_identifier"]
        retained_space_identifier = values["retained_space_identifier"]
        gauge_identifier = values["gauge_identifier"]
        geometry_identifier = values["geometry_identifier"]
        energy_unit_identifier = values["energy_unit_identifier"]
        energy_reference_identifier = values["energy_reference_identifier"]
        norm_energy_scale = values["norm_energy_scale"]
        operator_loss = values["operator_loss"]
        spectral_loss = values["spectral_loss"]
        if type(spatial_dimension) is not int or type(retained_rank) is not int:
            raise TypeError("dimension and rank must decode to built-in integers")
        if type(sample_shape) is not tuple or not all(
            type(size) is int for size in sample_shape
        ):
            raise TypeError("sample_shape must decode to an integer tuple")
        if type(sample_weights) is not tuple or not all(
            type(weight) is float for weight in sample_weights
        ):
            raise TypeError("sample_weights must decode to a float tuple")
        if (
            type(sample_inventory_identifier) is not str
            or type(retained_basis_identifier) is not str
            or type(retained_space_identifier) is not str
            or type(gauge_identifier) is not str
            or type(geometry_identifier) is not str
            or type(energy_unit_identifier) is not str
            or type(energy_reference_identifier) is not str
        ):
            raise TypeError("loss identifiers must decode to built-in strings")
        if (
            type(norm_energy_scale) is not float
            or type(operator_loss) is not float
            or type(spectral_loss) is not float
        ):
            raise TypeError("loss scalars must decode to built-in floats")
        return cls(
            spatial_dimension=spatial_dimension,
            retained_rank=retained_rank,
            sample_shape=sample_shape,
            sample_weights=sample_weights,
            sample_inventory_identifier=sample_inventory_identifier,
            retained_basis_identifier=retained_basis_identifier,
            retained_space_identifier=retained_space_identifier,
            gauge_identifier=gauge_identifier,
            geometry_identifier=geometry_identifier,
            energy_unit_identifier=energy_unit_identifier,
            energy_reference_identifier=energy_reference_identifier,
            norm_energy_scale=norm_energy_scale,
            operator_loss=operator_loss,
            spectral_loss=spectral_loss,
        )


__all__ = ["BandEquivalenceHoppingLocalityLossRecord"]
