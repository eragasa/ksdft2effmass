"""Periodic-3D rank-two frame-transport request."""

from __future__ import annotations

import numpy as np
from projectkoios.numerics.numpy.typing import Complex128Array
from projectkoios.numerics.numpy.validation import NumpyImmutableArrayConstructor
from projectkoios.optimization.alignment.procrustes import (
    ComplexUnitaryProcrustesTolerance,
)

from .base import Periodic3DRank2FrameTransportAnalysisRequest


class Periodic3DRank2TransportAnalysisRequest(
    Periodic3DRank2FrameTransportAnalysisRequest
):
    """Bind one immutable rank-two frame field and numerical-rank policy."""

    __slots__ = ("_frame", "_rank_absolute", "_rank_relative")

    def __init__(
        self,
        *,
        frame: Complex128Array,
        rank_absolute: float,
        rank_relative: float,
    ) -> None:
        tolerance = ComplexUnitaryProcrustesTolerance(
            rank_absolute=rank_absolute,
            rank_relative=rank_relative,
        )
        admitted = NumpyImmutableArrayConstructor(
            frame,
            "frame",
            np.dtype(np.complex128),
        ).execute()
        if admitted.ndim != 5 or admitted.shape[-1] != 2:
            raise ValueError("frame must have shape (N1, N2, N3, ambient, 2)")
        if admitted.shape[-2] < 2:
            raise ValueError("frame ambient dimension must be at least two")
        if any(size <= 0 for size in admitted.shape[:3]):
            raise ValueError("periodic mesh axes must be nonempty")
        self._frame = admitted
        self._rank_absolute = tolerance.rank_absolute
        self._rank_relative = tolerance.rank_relative

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


__all__ = ["Periodic3DRank2TransportAnalysisRequest"]
