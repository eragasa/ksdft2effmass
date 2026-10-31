"""Plain immutable scientific values for channels analysis."""

from __future__ import annotations

import math
from dataclasses import dataclass

from ksdft2effmass.real_space_support_truncation import (
    OrderedEigenvalueErrors,
    RankNormalizedMatrixFrobeniusErrors,
    RealSpaceSupportTruncationErrors,
)


@dataclass(frozen=True, slots=True)
class BandEquivalenceLocalityErrorChannels:
    """Retain normalized reconstructed-matrix and sorted-band errors."""

    maximum_hamiltonian: float
    rms_hamiltonian: float
    maximum_band: float
    rms_band: float

    def __post_init__(self) -> None:
        for name, value in (
            ("maximum_hamiltonian", self.maximum_hamiltonian),
            ("rms_hamiltonian", self.rms_hamiltonian),
            ("maximum_band", self.maximum_band),
            ("rms_band", self.rms_band),
        ):
            if type(value) is not float:
                raise TypeError(f"{name} must be a built-in float")
            if not math.isfinite(value) or value < 0.0:
                raise ValueError(f"{name} must be finite and nonnegative")

    @property
    def support_truncation_errors(self) -> RealSpaceSupportTruncationErrors:
        """Return these family channels under shared truncation terminology."""
        return RealSpaceSupportTruncationErrors(
            matrix_frobenius=RankNormalizedMatrixFrobeniusErrors(
                maximum_error=self.maximum_hamiltonian,
                root_mean_square_error=self.rms_hamiltonian,
            ),
            ordered_eigenvalues=OrderedEigenvalueErrors(
                maximum_absolute_error=self.maximum_band,
                root_mean_square_error=self.rms_band,
            ),
        )
