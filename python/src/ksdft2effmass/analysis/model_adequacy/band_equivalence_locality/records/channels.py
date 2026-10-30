"""Matrix and ordered-band error-channel result values."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from typing import Self

from ksdft2effmass.serialization import BaseTypedRecord, SerializableValue

from ..results import BandEquivalenceLocalityErrorChannels


@dataclass(frozen=True, slots=True)
class ErrorChannels(BaseTypedRecord):
    """Retain normalized reconstructed-matrix and sorted-band errors."""

    maximum_hamiltonian: float
    rms_hamiltonian: float
    maximum_band: float
    rms_band: float

    @classmethod
    def from_analysis(cls, analysis: BandEquivalenceLocalityErrorChannels) -> Self:
        """Project plain scientific error channels into this retained record."""
        if type(analysis) is not BandEquivalenceLocalityErrorChannels:
            raise TypeError("analysis must be BandEquivalenceLocalityErrorChannels")
        return cls(
            maximum_hamiltonian=analysis.maximum_hamiltonian,
            rms_hamiltonian=analysis.rms_hamiltonian,
            maximum_band=analysis.maximum_band,
            rms_band=analysis.rms_band,
        )

    def _mapping(self) -> Mapping[str, SerializableValue]:
        return {
            "maximum_hamiltonian": self.maximum_hamiltonian,
            "rms_hamiltonian": self.rms_hamiltonian,
            "maximum_band": self.maximum_band,
            "rms_band": self.rms_band,
        }

    @classmethod
    def _from_mapping(cls, values: Mapping[str, SerializableValue]) -> Self:
        required = {
            "maximum_hamiltonian",
            "rms_hamiltonian",
            "maximum_band",
            "rms_band",
        }
        if set(values) != required:
            raise ValueError("ErrorChannels fields do not match")
        maximum_hamiltonian = values["maximum_hamiltonian"]
        rms_hamiltonian = values["rms_hamiltonian"]
        maximum_band = values["maximum_band"]
        rms_band = values["rms_band"]
        if (
            type(maximum_hamiltonian) is not float
            or type(rms_hamiltonian) is not float
            or type(maximum_band) is not float
            or type(rms_band) is not float
        ):
            raise TypeError("float fields must use exact built-in types")
        return cls(
            maximum_hamiltonian=maximum_hamiltonian,
            rms_hamiltonian=rms_hamiltonian,
            maximum_band=maximum_band,
            rms_band=rms_band,
        )
