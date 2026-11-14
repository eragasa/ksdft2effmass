"""Two-dimensional periodic basis identity."""

from __future__ import annotations

from dataclasses import dataclass
from typing import ClassVar

from ksdft2effmass.periodic.operators.basis import PeriodicBasisIdentity


@dataclass(frozen=True, slots=True)
class Periodic2DBasisIdentity(PeriodicBasisIdentity):
    """Own an ordered basis identity for a two-dimensional periodic problem."""

    SPATIAL_DIMENSION: ClassVar[int] = 2

    @classmethod
    def _required_spatial_dimension(cls) -> int:
        return cls.SPATIAL_DIMENSION


__all__ = ["Periodic2DBasisIdentity"]
