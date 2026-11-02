"""Periodic-2D rank-two pointwise Procrustes contracts."""

from __future__ import annotations

import math

import numpy as np
import pytest
from projectkoios.numerics.numpy.typing import Complex128Array
from projectkoios.optimization.alignment.procrustes import (
    ComplexUnitaryProcrustesTolerance,
)

from ksdft2effmass.periodic2d.rank2.gauge_alignment.procrustes.analysis import (
    Periodic2DRank2ProcrustesAnalyzer,
)
from ksdft2effmass.periodic2d.rank2.gauge_alignment.procrustes.request import (
    Periodic2DRank2ProcrustesAnalysisRequest,
)
from ksdft2effmass.periodic2d.rank2.gauge_alignment.procrustes.result import (
    Periodic2DRank2ProcrustesAnalysis,
)

pytestmark = [pytest.mark.unit, pytest.mark.software_verification]


class TestPeriodic2DRank2ProcrustesAnalyzer:
    """Retain polar factors and invariants without canonicalizing SVD vectors."""

    @staticmethod
    def _frames(shape: tuple[int, ...]) -> tuple[Complex128Array, Complex128Array]:
        source = np.broadcast_to(
            np.eye(2, dtype=np.complex128),
            (*shape, 2, 2),
        ).copy()
        angle = 0.27
        right_action = np.asarray(
            (
                (math.cos(angle), -math.sin(angle)),
                (math.sin(angle), math.cos(angle)),
            ),
            dtype=np.complex128,
        )
        return source, source @ right_action

    def test_recovers_the_pointwise_right_action_with_immutable_evidence(self) -> None:
        source, target = self._frames((2, 3))
        request = Periodic2DRank2ProcrustesAnalysisRequest(
            source=source,
            target=target,
            tolerance=ComplexUnitaryProcrustesTolerance(
                rank_absolute=1.0e-12,
                rank_relative=1.0e-10,
            ),
        )
        source[...] = 0.0

        result = Periodic2DRank2ProcrustesAnalyzer(request=request).execute()

        assert type(result) is Periodic2DRank2ProcrustesAnalysis
        assert result.gauge_group == "U(2)"
        assert result.alignment_sample_count == 6
        assert result.owner_result.rank_deficient_count == 0
        assert np.max(result.owner_result.optimal_residual_frobenius_norms) < 1.0e-14
        expected = np.broadcast_to(target[0, 0], (2, 3, 2, 2))
        assert result.owner_result.right_unitary_completions == pytest.approx(
            expected,
            abs=2.0e-15,
        )
        with pytest.raises(ValueError):
            result.owner_result.right_unitary_completions.setflags(write=True)

    def test_rejects_a_three_dimensional_frame_inventory(self) -> None:
        source, target = self._frames((2, 2, 2))
        with pytest.raises(ValueError, match="N1, N2, ambient, 2"):
            Periodic2DRank2ProcrustesAnalysisRequest(
                source=source,
                target=target,
                tolerance=ComplexUnitaryProcrustesTolerance(),
            )
