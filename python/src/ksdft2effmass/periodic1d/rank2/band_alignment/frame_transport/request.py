"""Request values for rank-two periodic frame transport."""

from __future__ import annotations

from dataclasses import dataclass

from projectkoios.physkit.units import Unitless

from ksdft2effmass.solidstate.band_frames import ReciprocalBandFramePath1D

from ..configuration import Periodic1DCompositeBandAlignmentConfiguration


@dataclass(frozen=True, slots=True, eq=False)
class Periodic1DRank2TransportAnalysisRequest:
    """Bind the frozen rank-two study configuration to one raw frame path."""

    configuration: Periodic1DCompositeBandAlignmentConfiguration
    source: ReciprocalBandFramePath1D

    def __post_init__(self) -> None:
        if (
            type(self.configuration)
            is not Periodic1DCompositeBandAlignmentConfiguration
        ):
            raise TypeError(
                "configuration must be Periodic1DCompositeBandAlignmentConfiguration"
            )
        if type(self.source) is not ReciprocalBandFramePath1D:
            raise TypeError("source must be ReciprocalBandFramePath1D")
        if self.source.rank != self.configuration.retained_rank:
            raise ValueError("source rank must match the rank-two configuration")
        if self.source.ambient_dimension != len(self.configuration.onsite_numerators):
            raise ValueError("source ambient dimension must match the parent basis")
        if self.source.mesh.point_count != self.configuration.construction_size:
            raise ValueError("source mesh must match the construction inventory")
        reciprocal_period = self.source.mesh.reciprocal_period
        if (
            not isinstance(reciprocal_period.unit, Unitless)
            or reciprocal_period.magnitude != 1.0
        ):
            raise ValueError(
                "source mesh must use the frozen unitless reciprocal period"
            )
        if (
            self.source.orthonormality_absolute_tolerance
            != self.configuration.dimensionless_absolute_tolerance
        ):
            raise ValueError(
                "source orthonormality tolerance must match the configuration"
            )

    @property
    def overlap_singular_value_threshold(self) -> float:
        """Return the frozen neighbor- and closure-overlap threshold."""
        return self.configuration.overlap_singular_value_threshold


__all__ = ["Periodic1DRank2TransportAnalysisRequest"]
