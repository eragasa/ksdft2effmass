"""Rank-two hopping-locality analysis for periodic one dimension."""

from __future__ import annotations

from typing import final

import numpy as np
from projectkoios.physkit.units import ComplexMatrixQuantity

from ksdft2effmass.periodic1d.hopping_locality.base import (
    Periodic1DHoppingLocalityAnalyzer,
)

from .request import Periodic1DRank2HoppingLocalityAnalysisRequest
from .result import (
    Periodic1DRank2HoppingLocalityAnalysis,
    Periodic1DRank2HoppingTailResult,
)


@final
class Periodic1DRank2HoppingLocalityAnalyzer(
    Periodic1DHoppingLocalityAnalyzer[
        Periodic1DRank2HoppingLocalityAnalysisRequest,
        Periodic1DRank2HoppingLocalityAnalysis,
    ]
):
    """Measure one channel's ordinary hopping tails without removing support."""

    __slots__ = ("_request",)

    def __init__(
        self,
        *,
        request: Periodic1DRank2HoppingLocalityAnalysisRequest,
    ) -> None:
        if type(request) is not Periodic1DRank2HoppingLocalityAnalysisRequest:
            raise TypeError("request must be the exact hopping-locality request")
        self._request = request

    @property
    def request(self) -> Periodic1DRank2HoppingLocalityAnalysisRequest:
        """Return the complete immutable hopping-locality request."""
        return self._request

    def execute(self) -> Periodic1DRank2HoppingLocalityAnalysis:
        """Return omitted-block norms for every unchanged diagnostic range."""
        request = self.request
        model = request.ordinary_model
        diagnostic_ranges = (
            request.configuration.hopping_diagnostic_range_inventory.ranges
        )
        tails = tuple(
            Periodic1DRank2HoppingTailResult(
                maximum_range=diagnostic_range.maximum_range,
                ordinary_omitted_block_l2_norm=self._omitted_block_l2_norm(
                    request.ordinary_translation_inventory.translations,
                    model.hopping_blocks,
                    diagnostic_range.maximum_range,
                ),
            )
            for diagnostic_range in diagnostic_ranges
        )
        return Periodic1DRank2HoppingLocalityAnalysis(
            request=request,
            tails=tails,
        )

    @staticmethod
    def _omitted_block_l2_norm(
        representatives: tuple[int, ...],
        hopping_blocks: tuple[ComplexMatrixQuantity, ...],
        maximum_range: int,
    ) -> float:
        omitted_squared = sum(
            float(np.linalg.norm(block.magnitude) ** 2)
            for representative, block in zip(
                representatives,
                hopping_blocks,
                strict=True,
            )
            if abs(representative) > maximum_range
        )
        return float(np.sqrt(omitted_squared))


__all__ = ["Periodic1DRank2HoppingLocalityAnalyzer"]
