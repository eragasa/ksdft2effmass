"""Periodic-3D rank-two hopping-locality request values."""

from __future__ import annotations

from dataclasses import dataclass

from projectkoios.numerics.finite_periodic.numpy.matrix_series import (
    NumpyFiniteFourierMatrixSeries,
)

from ksdft2effmass.serialization.enums import StringWireEnum

from .base import Periodic3DRank2HoppingLocalityAnalysisRequestRole


class Periodic3DRank2HoppingLocalityChannelEnum(StringWireEnum):
    """Identify one unchanged ordinary-hopping channel."""

    REFERENCE = "reference"
    COMPARISON = "comparison"


@dataclass(frozen=True, slots=True)
class Periodic3DRank2HoppingLocalityAnalysisRequest(
    Periodic3DRank2HoppingLocalityAnalysisRequestRole
):
    """Bind one periodic-3D rank-two channel to its metric-shell inventory."""

    channel: Periodic3DRank2HoppingLocalityChannelEnum
    energy_reference: str
    basis_identifier: str
    series: NumpyFiniteFourierMatrixSeries
    shell_indices: tuple[int, ...]

    def __post_init__(self) -> None:
        if type(self.channel) is not Periodic3DRank2HoppingLocalityChannelEnum:
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
        if self.series.matrix_coefficients.shape[1:] != (2, 2):
            raise ValueError("series blocks must have retained rank two")
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
    "Periodic3DRank2HoppingLocalityAnalysisRequest",
    "Periodic3DRank2HoppingLocalityChannelEnum",
]
