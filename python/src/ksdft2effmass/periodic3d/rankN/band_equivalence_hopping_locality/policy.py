"""Parent-independent periodic-3D rank-N analysis policy."""

from __future__ import annotations

import math
from dataclasses import dataclass

from projectkoios.optimization.alignment.procrustes import (
    ComplexUnitaryProcrustesTolerance,
)

from ksdft2effmass.periodic3d.rankN.gauge_alignment.definition import (
    Periodic3DRankNGaugeAlignment,
)
from ksdft2effmass.sewing import ReciprocalEndpointSewingInventory


@dataclass(frozen=True, slots=True)
class Periodic3DRankNBandEquivalenceHoppingLocalityPolicy:
    """Bind construction-transform and analysis selections without model parameters.

    ``construction_offsets`` uses the exact centered-mesh convention
    ``-1/2 + (i + offset) / construction_size`` independently on each axis.
    ``norm_energy_scale`` explicitly normalizes matrix and spectrum errors in the
    declared operator unit. Evaluation coordinates belong to the represented fields.
    They may form a tensor product or an arbitrary ordered point inventory. An empty
    ``band_tolerances`` inventory requests support curves without first-passing
    decisions.
    """

    construction_size: int
    construction_offsets: tuple[float, float, float]
    norm_energy_scale: float
    band_tolerances: tuple[float, ...]
    gauge_alignments: tuple[Periodic3DRankNGaugeAlignment, ...]
    shell_cap: int
    procrustes_tolerance: ComplexUnitaryProcrustesTolerance
    transport_rank_absolute: float
    transport_rank_relative: float
    endpoint_sewing: ReciprocalEndpointSewingInventory

    def __post_init__(self) -> None:
        """Validate construction, alignment, threshold, and rank selections."""
        for integer_value, name in (
            (self.construction_size, "construction_size"),
            (self.shell_cap, "shell_cap"),
        ):
            if type(integer_value) is not int:
                raise TypeError(f"{name} must be a built-in integer")
            if integer_value <= 0:
                raise ValueError(f"{name} must be positive")
        if (
            type(self.construction_offsets) is not tuple
            or len(self.construction_offsets) != 3
            or any(type(value) is not float for value in self.construction_offsets)
        ):
            raise TypeError("construction_offsets must contain three built-in floats")
        if any(not math.isfinite(value) for value in self.construction_offsets):
            raise ValueError("construction_offsets must contain finite values")
        if type(self.norm_energy_scale) is not float:
            raise TypeError("norm_energy_scale must be a built-in float")
        if not math.isfinite(self.norm_energy_scale) or self.norm_energy_scale <= 0.0:
            raise ValueError("norm_energy_scale must be finite and positive")
        if type(self.band_tolerances) is not tuple:
            raise TypeError("band_tolerances must be a tuple")
        if any(
            type(value) is not float or not math.isfinite(value) or value < 0.0
            for value in self.band_tolerances
        ):
            raise ValueError("band_tolerances must contain finite nonnegative floats")
        if len(set(self.band_tolerances)) != len(self.band_tolerances):
            raise ValueError("band_tolerances must be unique")
        if type(self.gauge_alignments) is not tuple or not self.gauge_alignments:
            raise TypeError("gauge_alignments must be a nonempty tuple")
        if any(
            type(value) is not Periodic3DRankNGaugeAlignment
            for value in self.gauge_alignments
        ):
            raise TypeError("gauge_alignments must contain exact periodic-3D enums")
        inventory = (
            Periodic3DRankNGaugeAlignment.IDENTITY,
            Periodic3DRankNGaugeAlignment.GLOBAL_UNITARY,
            Periodic3DRankNGaugeAlignment.POINTWISE_UNITARY,
            Periodic3DRankNGaugeAlignment.KNOWN_INVERSE_ORACLE,
        )
        if self.gauge_alignments != tuple(
            value for value in inventory if value in self.gauge_alignments
        ):
            raise ValueError("gauge_alignments must be a unique ordered subsequence")
        if type(self.procrustes_tolerance) is not ComplexUnitaryProcrustesTolerance:
            raise TypeError("procrustes_tolerance must be the exact tolerance type")
        for rank_value, name in (
            (self.transport_rank_absolute, "transport_rank_absolute"),
            (self.transport_rank_relative, "transport_rank_relative"),
        ):
            if type(rank_value) is not float:
                raise TypeError(f"{name} must be a built-in float")
            if not math.isfinite(rank_value) or rank_value < 0.0:
                raise ValueError(f"{name} must be finite and nonnegative")
        if type(self.endpoint_sewing) is not ReciprocalEndpointSewingInventory:
            raise TypeError("endpoint_sewing must be ReciprocalEndpointSewingInventory")
        if self.endpoint_sewing.spatial_dimension != 3:
            raise ValueError("endpoint sewing must contain three axis maps")


__all__ = ["Periodic3DRankNBandEquivalenceHoppingLocalityPolicy"]
