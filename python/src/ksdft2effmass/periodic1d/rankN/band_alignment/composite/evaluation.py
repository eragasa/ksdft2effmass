"""Exact evaluation-mesh independence analysis."""

from __future__ import annotations

from fractions import Fraction
from typing import final

from ksdft2effmass.periodic1d.rankN.band_alignment.calculation import (
    Periodic1DRankNAlignmentCalculationRequest,
)

from ..evaluation_result import Periodic1DRankNEvaluationIndependenceResult


@final
class Periodic1DRankNEvaluationIndependenceAnalyzer:
    """Derive exact mesh separation and selection-input provenance."""

    __slots__ = ("_request",)

    def __init__(
        self,
        request: Periodic1DRankNAlignmentCalculationRequest,
    ) -> None:
        """Bind one complete immutable higher-rank calculation request."""
        if type(request) is not Periodic1DRankNAlignmentCalculationRequest:
            raise TypeError(
                "request must be Periodic1DRankNAlignmentCalculationRequest"
            )
        self._request = request

    @property
    def request(self) -> Periodic1DRankNAlignmentCalculationRequest:
        """Return the exact calculation request bound to this action."""
        return self._request

    def execute(self) -> Periodic1DRankNEvaluationIndependenceResult:
        """Return exact rational mesh and selection provenance."""
        configuration = self._request.configuration
        denominator = configuration.evaluation_shift_denominator
        numerator = configuration.evaluation_shift_numerator
        evaluation_size = configuration.evaluation_mesh_size
        evaluation_coordinates = {
            Fraction(index * denominator + numerator, evaluation_size * denominator)
            for index in range(evaluation_size)
        }
        construction_evaluation_disjoint = all(
            evaluation_coordinates.isdisjoint(
                Fraction(index, mesh_size) for index in range(mesh_size)
            )
            for mesh_size in configuration.construction_mesh_sizes
        )
        evaluation_mesh_excluded_from_selection = (
            evaluation_size != configuration.global_unitary_selection_mesh_size
            and evaluation_size not in configuration.construction_mesh_sizes
        )
        return Periodic1DRankNEvaluationIndependenceResult(
            construction_mesh_sizes=configuration.construction_mesh_sizes,
            evaluation_mesh_size=evaluation_size,
            evaluation_shift_numerator=numerator,
            evaluation_shift_denominator=denominator,
            global_selection_mesh_size=(
                configuration.global_unitary_selection_mesh_size
            ),
            pointwise_selection_mesh_sizes=configuration.construction_mesh_sizes,
            construction_evaluation_disjoint=construction_evaluation_disjoint,
            evaluation_mesh_excluded_from_selection=(
                evaluation_mesh_excluded_from_selection
            ),
        )
