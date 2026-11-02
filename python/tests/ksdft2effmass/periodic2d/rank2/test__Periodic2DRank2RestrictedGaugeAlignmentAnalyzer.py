"""Periodic-2D rank-two restricted gauge-alignment contracts."""

from __future__ import annotations

import math

import numpy as np
import pytest
from projectkoios.numerics.numpy.typing import Complex128Array

from ksdft2effmass.periodic2d.rank2.gauge_alignment.analysis import (
    Periodic2DRank2RestrictedGaugeAlignmentAnalyzer,
)
from ksdft2effmass.periodic2d.rank2.gauge_alignment.request import (
    Periodic2DRank2RestrictedGaugeAlignmentAnalysisRequest,
)
from ksdft2effmass.periodic2d.rank2.gauge_alignment.result import (
    Periodic2DRank2RestrictedGaugeAlignmentAnalysis,
)

pytestmark = [pytest.mark.unit, pytest.mark.software_verification]


class TestPeriodic2DRank2RestrictedGaugeAlignmentAnalyzer:
    """Bind immutable represented fields to the reviewed restricted alignment."""

    @staticmethod
    def _fields(shape: tuple[int, ...]) -> tuple[Complex128Array, Complex128Array]:
        reference = np.zeros((*shape, 2, 2), dtype=np.complex128)
        values = np.arange(math.prod(shape), dtype=np.float64).reshape(shape)
        reference[..., 0, 0] = 1.0 + 0.1 * values
        reference[..., 1, 1] = -1.0 - 0.1 * values
        reference[..., 0, 1] = 0.2
        reference[..., 1, 0] = 0.2
        angle = 0.31
        rotation = np.asarray(
            (
                (math.cos(angle), -math.sin(angle)),
                (math.sin(angle), math.cos(angle)),
            ),
            dtype=np.complex128,
        )
        comparison = rotation.T @ reference @ rotation
        return reference, comparison

    def test_executes_with_immutable_right_action_u2_identity(self) -> None:
        reference, comparison = self._fields((2, 3))
        request = Periodic2DRank2RestrictedGaugeAlignmentAnalysisRequest(
            reference=reference,
            comparison=comparison,
        )
        reference[...] = 0.0

        result = Periodic2DRank2RestrictedGaugeAlignmentAnalyzer(
            request=request
        ).execute()

        assert type(result) is Periodic2DRank2RestrictedGaugeAlignmentAnalysis
        assert result.request is request
        assert result.gauge_group == "U(2)"
        assert result.alignment_sample_count == 6
        assert result.maximum_correlation == pytest.approx(1.0, abs=2.0e-15)
        assert result.minimum_operator_threshold == pytest.approx(0.0, abs=2.0e-15)
        assert not request.reference.flags.writeable
        with pytest.raises(ValueError):
            request.reference.setflags(write=True)

    def test_rejects_a_three_dimensional_matrix_field(self) -> None:
        reference, comparison = self._fields((2, 2, 2))
        with pytest.raises(ValueError, match="N1, N2, 2, 2"):
            Periodic2DRank2RestrictedGaugeAlignmentAnalysisRequest(
                reference=reference,
                comparison=comparison,
            )
