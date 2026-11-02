"""Periodic-3D arbitrary-rank hopping-locality request values."""

from __future__ import annotations

from dataclasses import dataclass

from projectkoios.numerics.finite_periodic.numpy.matrix_series import (
    NumpyFiniteFourierMatrixSeries,
)

from ksdft2effmass.periodic3d.hopping_locality.base import (
    Periodic3DHoppingLocalityAnalysisRequest,
)
from ksdft2effmass.serialization.enums import StringWireEnum


class Periodic3DRankNHoppingLocalityChannelEnum(StringWireEnum):
    """Identify one unchanged ordinary-hopping channel."""

    REFERENCE = "reference"
    COMPARISON = "comparison"


@dataclass(frozen=True, slots=True)
class Periodic3DRankNHoppingLocalityAnalysisRequest(
    Periodic3DHoppingLocalityAnalysisRequest
):
    """Bind one periodic-3D arbitrary-rank channel to its metric-shell inventory."""

    retained_rank: int
    channel: Periodic3DRankNHoppingLocalityChannelEnum
    energy_reference: str
    basis_identifier: str
    series: NumpyFiniteFourierMatrixSeries
    shell_indices: tuple[int, ...]

    def __post_init__(self) -> None:
        if type(self.retained_rank) is not int:
            raise TypeError("retained_rank must be a built-in integer")
        if self.retained_rank < 3:
            raise ValueError("retained_rank must be at least three")
        if type(self.channel) is not Periodic3DRankNHoppingLocalityChannelEnum:
            raise TypeError("channel must be the exact periodic-3D channel enum")
        for value, name in (
            (self.energy_reference, "energy_reference"),
            (self.basis_identifier, "basis_identifier"),
        ):
            if type(value) is not str:
                raise TypeError(f"{name} must be a built-in string")
            if not value:
                raise ValueError(f"{name} must be nonempty")
        if type(self.series) is not NumpyFiniteFourierMatrixSeries:
            raise TypeError("series must be NumpyFiniteFourierMatrixSeries")
        if self.series.dimension != 3:
            raise ValueError("series must be periodic three-dimensional")
        if self.series.matrix_coefficients.shape[1:] != (
            self.retained_rank,
            self.retained_rank,
        ):
            raise ValueError("series blocks must match retained_rank")
        if type(self.shell_indices) is not tuple or any(
            type(shell_index) is not int for shell_index in self.shell_indices
        ):
            raise TypeError("shell_indices must contain built-in integers")
        if len(self.shell_indices) != len(self.series.integer_modes):
            raise ValueError("shell_indices must match the Fourier term count")
        if any(shell_index < 0 for shell_index in self.shell_indices):
            raise ValueError("shell_indices must be nonnegative")

    @property
    def identifier(self) -> str:
        """Return the stable calculation-local channel identifier."""
        return f"band-equivalence-{self.channel.value}-ordinary"


__all__ = [
    "Periodic3DRankNHoppingLocalityAnalysisRequest",
    "Periodic3DRankNHoppingLocalityChannelEnum",
]
