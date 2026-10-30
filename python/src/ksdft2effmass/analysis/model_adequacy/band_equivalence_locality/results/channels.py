"""Plain immutable scientific values for channels analysis."""

from __future__ import annotations

import math
from dataclasses import dataclass


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
