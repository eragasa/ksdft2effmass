"""Periodic-3D arbitrary-rank frame-transport request."""

from __future__ import annotations

import numpy as np
from projectkoios.numerics.numpy.typing import Complex128Array
from projectkoios.numerics.numpy.validation import NumpyImmutableArrayConstructor
from projectkoios.optimization.alignment.procrustes import (
    ComplexUnitaryProcrustesTolerance,
)

from ksdft2effmass.periodic3d.base import Periodic3DCapability


class Periodic3DRankNTransportAnalysisRequest(Periodic3DCapability):
    """Bind one immutable finite-rank frame field and numerical-rank policy."""

    __slots__ = ("_frame", "_rank_absolute", "_rank_relative", "_retained_rank")

    def __init__(
        self,
        *,
        retained_rank: int,
        frame: Complex128Array,
        rank_absolute: float,
        rank_relative: float,
    ) -> None:
        if type(retained_rank) is not int:
            raise TypeError("retained_rank must be a built-in integer")
        if retained_rank < 3:
            raise ValueError("retained_rank must be at least three")
        tolerance = ComplexUnitaryProcrustesTolerance(
            rank_absolute=rank_absolute,
            rank_relative=rank_relative,
        )
        admitted = NumpyImmutableArrayConstructor(
            frame,
            "frame",
            np.dtype(np.complex128),
        ).execute()
        if admitted.ndim != 5 or admitted.shape[-1] != retained_rank:
            raise ValueError(
                "frame must have shape (N1, N2, N3, ambient, retained_rank)"
            )
        if admitted.shape[-2] < retained_rank:
            raise ValueError("frame ambient dimension must be at least retained_rank")
        if any(size <= 0 for size in admitted.shape[:3]):
            raise ValueError("periodic mesh axes must be nonempty")
        self._retained_rank = retained_rank
        self._frame = admitted
        self._rank_absolute = tolerance.rank_absolute
        self._rank_relative = tolerance.rank_relative

    @property
    def retained_rank(self) -> int:
        """Return the exact finite retained rank."""
        return self._retained_rank

    @property
    def frame(self) -> Complex128Array:
        """Return the immutable raw retained-frame field."""
        return self._frame

    @property
    def rank_absolute(self) -> float:
        """Return the absolute numerical-rank cutoff component."""
        return self._rank_absolute

    @property
    def rank_relative(self) -> float:
        """Return the relative numerical-rank cutoff component."""
        return self._rank_relative


__all__ = ["Periodic3DRankNTransportAnalysisRequest"]
