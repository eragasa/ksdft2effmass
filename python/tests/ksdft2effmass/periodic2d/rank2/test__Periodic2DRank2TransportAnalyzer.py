"""Periodic-2D rank-two frame-transport action contracts."""

from __future__ import annotations

import numpy as np
import pytest
from projectkoios.numerics.numpy.typing import Complex128Array

from ksdft2effmass.periodic2d.rank2.band_alignment.frame_transport.analysis import (
    Periodic2DRank2TransportAnalyzer,
)
from ksdft2effmass.periodic2d.rank2.band_alignment.frame_transport.request import (
    Periodic2DRank2TransportAnalysisRequest,
)
from ksdft2effmass.periodic2d.rank2.band_alignment.frame_transport.result import (
    Periodic2DRank2TransportDiagnosticAnalysis,
)

pytestmark = [pytest.mark.unit, pytest.mark.software_verification]


class TestPeriodic2DRank2TransportAnalyzer:
    """Bind immutable two-dimensional frame fields to sparse loop diagnostics."""

    @staticmethod
    def _identity_frame(shape: tuple[int, ...]) -> Complex128Array:
        return np.broadcast_to(
            np.eye(2, dtype=np.complex128),
            (*shape, 2, 2),
        ).copy()

    def test_executes_identity_link_closure_and_plaquette_diagnostics(self) -> None:
        frame = self._identity_frame((2, 3))
        request = Periodic2DRank2TransportAnalysisRequest(
            frame=frame,
            rank_absolute=1.0e-12,
            rank_relative=1.0e-10,
        )
        frame[...] = 0.0

        result = Periodic2DRank2TransportAnalyzer(request=request).execute()

        assert type(result) is Periodic2DRank2TransportDiagnosticAnalysis
        assert result.request is request
        assert result.minimum_singular_value == pytest.approx(1.0)
        assert result.rank_deficient_link_count == 0
        assert result.closure_and_plaquette_applicable
        assert result.maximum_absolute_closure_phases == pytest.approx((0.0, 0.0))
        assert result.maximum_plaquette_phase == pytest.approx(0.0)
        assert not request.frame.flags.writeable
        with pytest.raises(ValueError):
            request.frame.setflags(write=True)

    def test_rejects_a_three_dimensional_frame_field(self) -> None:
        with pytest.raises(ValueError, match="N1, N2, ambient, 2"):
            Periodic2DRank2TransportAnalysisRequest(
                frame=self._identity_frame((2, 2, 2)),
                rank_absolute=1.0e-12,
                rank_relative=1.0e-10,
            )
