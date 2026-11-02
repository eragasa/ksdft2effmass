"""Periodic-2D arbitrary-rank global unitary-alignment results."""

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import cast

import numpy as np
from projectkoios.numerics.numpy.typing import Complex128Array
from projectkoios.numerics.numpy.validation import NumpyImmutableArrayConstructor
from projectkoios.optimization.alignment.numpy.batched_procrustes import (
    NumpyBatchedComplexUnitaryProcrustesResult,
)

from ksdft2effmass.gauge_alignment.base import GaugeAlignmentAnalysisIdentity
from ksdft2effmass.periodic2d.gauge_alignment.base import (
    Periodic2DGaugeAlignmentAnalysis,
)

from .request import Periodic2DRankNGlobalGaugeAlignmentAnalysisRequest


@dataclass(frozen=True, slots=True, eq=False)
class Periodic2DRankNGlobalGaugeAlignmentSelected:
    """Retain one uniquely selected full-rank right unitary."""

    retained_rank: int
    right_unitary: Complex128Array

    def __post_init__(self) -> None:
        if type(self.retained_rank) is not int:
            raise TypeError("retained_rank must be a built-in integer")
        if self.retained_rank < 3:
            raise ValueError("retained_rank must be at least three")
        right_unitary = NumpyImmutableArrayConstructor(
            self.right_unitary,
            "right_unitary",
            np.dtype(np.complex128),
        ).execute()
        if right_unitary.shape != (self.retained_rank, self.retained_rank):
            raise ValueError("right_unitary must be square with retained-rank size")
        object.__setattr__(self, "right_unitary", right_unitary)


@dataclass(frozen=True, slots=True)
class Periodic2DRankNGlobalGaugeAlignmentRankDeficient:
    """Retain aggregate rank-deficiency evidence without selecting a completion."""

    retained_rank: int
    numerical_rank: int
    applied_rank_cutoff: float
    cross_singular_values: tuple[float, ...]
    optimal_residual_frobenius_norm: float

    def __post_init__(self) -> None:
        for value, name in (
            (self.retained_rank, "retained_rank"),
            (self.numerical_rank, "numerical_rank"),
        ):
            if type(value) is not int:
                raise TypeError(f"{name} must be a built-in integer")
        if self.retained_rank < 3:
            raise ValueError("retained_rank must be at least three")
        if not 0 <= self.numerical_rank < self.retained_rank:
            raise ValueError("numerical_rank must be below retained_rank")
        if type(self.applied_rank_cutoff) is not float:
            raise TypeError("applied_rank_cutoff must be a built-in float")
        if (
            not math.isfinite(self.applied_rank_cutoff)
            or self.applied_rank_cutoff < 0.0
        ):
            raise ValueError("applied_rank_cutoff must be finite and nonnegative")
        if type(self.cross_singular_values) is not tuple or any(
            type(value) is not float for value in self.cross_singular_values
        ):
            raise TypeError("cross_singular_values must contain built-in floats")
        if len(self.cross_singular_values) != self.retained_rank:
            raise ValueError("cross_singular_values must match retained_rank")
        if any(
            not math.isfinite(value) or value < 0.0
            for value in self.cross_singular_values
        ):
            raise ValueError("cross_singular_values must be finite and nonnegative")
        if any(
            left < right
            for left, right in zip(
                self.cross_singular_values,
                self.cross_singular_values[1:],
                strict=False,
            )
        ):
            raise ValueError("cross_singular_values must be nonincreasing")
        if type(self.optimal_residual_frobenius_norm) is not float:
            raise TypeError("optimal_residual_frobenius_norm must be a built-in float")
        if (
            not math.isfinite(self.optimal_residual_frobenius_norm)
            or self.optimal_residual_frobenius_norm < 0.0
        ):
            raise ValueError(
                "optimal_residual_frobenius_norm must be finite and nonnegative"
            )


@dataclass(frozen=True, slots=True, eq=False)
class Periodic2DRankNGlobalGaugeAlignmentAnalysis(Periodic2DGaugeAlignmentAnalysis):
    """Retain one aggregate polar selection and complete invariant evidence."""

    request: Periodic2DRankNGlobalGaugeAlignmentAnalysisRequest
    owner_result: NumpyBatchedComplexUnitaryProcrustesResult

    def __post_init__(self) -> None:
        if type(self.request) is not Periodic2DRankNGlobalGaugeAlignmentAnalysisRequest:
            raise TypeError("request must be the exact periodic-2D rank-N request")
        if type(self.owner_result) is not NumpyBatchedComplexUnitaryProcrustesResult:
            raise TypeError("owner_result must be the exact Project Koios result")
        if self.owner_result.tolerance is not self.request.tolerance:
            raise ValueError("owner result tolerance must be the requested tolerance")
        rank = self.request.retained_rank
        if self.owner_result.right_unitary_completions.shape != (1, rank, rank):
            raise ValueError("owner result must contain one global rank-N completion")

    @property
    def analysis_identity(self) -> GaugeAlignmentAnalysisIdentity:
        """Return the request-bound global alignment identity."""
        return self.request.analysis_identity

    @property
    def selection_outcome(
        self,
    ) -> (
        Periodic2DRankNGlobalGaugeAlignmentSelected
        | Periodic2DRankNGlobalGaugeAlignmentRankDeficient
    ):
        """Return a typed full-rank selection or rank-deficiency diagnostic."""
        rank = self.request.retained_rank
        numerical_rank = int(self.owner_result.numerical_ranks[0])
        if numerical_rank == rank:
            return Periodic2DRankNGlobalGaugeAlignmentSelected(
                retained_rank=rank,
                right_unitary=cast(
                    Complex128Array,
                    self.owner_result.right_unitary_completions[0],
                ),
            )
        return Periodic2DRankNGlobalGaugeAlignmentRankDeficient(
            retained_rank=rank,
            numerical_rank=numerical_rank,
            applied_rank_cutoff=float(self.owner_result.applied_rank_cutoffs[0]),
            cross_singular_values=tuple(
                float(value) for value in self.owner_result.cross_singular_values[0]
            ),
            optimal_residual_frobenius_norm=float(
                self.owner_result.optimal_residual_frobenius_norms[0]
            ),
        )


__all__ = [
    "Periodic2DRankNGlobalGaugeAlignmentAnalysis",
    "Periodic2DRankNGlobalGaugeAlignmentRankDeficient",
    "Periodic2DRankNGlobalGaugeAlignmentSelected",
]
