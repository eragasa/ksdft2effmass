"""Periodic-3D arbitrary-rank Procrustes and frame-transport contracts."""

from __future__ import annotations

import math

import numpy as np
import pytest
from projectkoios.numerics.numpy.typing import Complex128Array
from projectkoios.optimization.alignment.procrustes import (
    ComplexUnitaryProcrustesTolerance,
)

from ksdft2effmass.periodic3d.rankN.band_alignment.frame_transport.analysis import (
    Periodic3DRankNTransportAnalyzer,
)
from ksdft2effmass.periodic3d.rankN.band_alignment.frame_transport.base import (
    Periodic3DRankNFrameTransportAnalysis,
    Periodic3DRankNFrameTransportAnalysisRequest,
    Periodic3DRankNFrameTransportAnalyzer,
)
from ksdft2effmass.periodic3d.rankN.band_alignment.frame_transport.request import (
    Periodic3DRankNTransportAnalysisRequest,
)
from ksdft2effmass.periodic3d.rankN.band_alignment.frame_transport.result import (
    Periodic3DRankNTransportDiagnosticAnalysis,
)
from ksdft2effmass.periodic3d.rankN.gauge_alignment.analysis import (
    Periodic3DRankNGlobalGaugeAlignmentAnalyzer,
)
from ksdft2effmass.periodic3d.rankN.gauge_alignment.base import (
    Periodic3DRankNGaugeAlignmentAnalysis,
    Periodic3DRankNGaugeAlignmentAnalysisRequest,
    Periodic3DRankNGaugeAlignmentAnalyzer,
    Periodic3DRankNGaugeAlignmentCapability,
)
from ksdft2effmass.periodic3d.rankN.gauge_alignment.procrustes.analysis import (
    Periodic3DRankNProcrustesAnalyzer,
)
from ksdft2effmass.periodic3d.rankN.gauge_alignment.procrustes.request import (
    Periodic3DRankNProcrustesAnalysisRequest,
)
from ksdft2effmass.periodic3d.rankN.gauge_alignment.procrustes.result import (
    Periodic3DRankNProcrustesAnalysis,
)
from ksdft2effmass.periodic3d.rankN.gauge_alignment.request import (
    Periodic3DRankNGlobalGaugeAlignmentAnalysisRequest,
)
from ksdft2effmass.periodic3d.rankN.gauge_alignment.result import (
    Periodic3DRankNGlobalGaugeAlignmentAnalysis,
    Periodic3DRankNGlobalGaugeAlignmentRankDeficient,
    Periodic3DRankNGlobalGaugeAlignmentSelected,
)

pytestmark = [pytest.mark.unit, pytest.mark.software_verification]


class TestPeriodic3DRankNAlignmentCapabilities:
    """Retain explicit finite-rank invariants on three-dimensional meshes."""

    @staticmethod
    def _frames(
        shape: tuple[int, ...], retained_rank: int
    ) -> tuple[Complex128Array, Complex128Array]:
        source = np.broadcast_to(
            np.eye(retained_rank, dtype=np.complex128),
            (*shape, retained_rank, retained_rank),
        ).copy()
        right_action = np.eye(retained_rank, dtype=np.complex128)
        angle = 0.19
        right_action[:2, :2] = np.asarray(
            (
                (math.cos(angle), -math.sin(angle)),
                (math.sin(angle), math.cos(angle)),
            ),
            dtype=np.complex128,
        )
        return source, source @ right_action

    def test_pointwise_procrustes_retains_rank_and_polar_evidence(self) -> None:
        source, target = self._frames((2, 2, 3), retained_rank=3)
        request = Periodic3DRankNProcrustesAnalysisRequest(
            retained_rank=3,
            source=source,
            target=target,
            tolerance=ComplexUnitaryProcrustesTolerance(
                rank_absolute=1.0e-12,
                rank_relative=1.0e-10,
            ),
        )

        analyzer = Periodic3DRankNProcrustesAnalyzer(request=request)
        result = analyzer.execute()

        assert isinstance(request, Periodic3DRankNGaugeAlignmentAnalysisRequest)
        assert isinstance(result, Periodic3DRankNGaugeAlignmentAnalysis)
        assert isinstance(analyzer, Periodic3DRankNGaugeAlignmentAnalyzer)
        assert request.band_subspace_rank == 3
        assert result.band_subspace_rank == 3
        assert analyzer.band_subspace_rank == 3
        assert type(result) is Periodic3DRankNProcrustesAnalysis
        assert result.gauge_group == "U(3)"
        assert result.alignment_sample_count == 12
        assert result.owner_result.rank_deficient_count == 0
        assert np.max(result.owner_result.optimal_residual_frobenius_norms) < 1.0e-14
        expected = np.broadcast_to(target[0, 0, 0], (2, 2, 3, 3, 3))
        assert result.owner_result.right_unitary_completions == pytest.approx(
            expected,
            abs=2.0e-15,
        )

    def test_global_alignment_selects_one_full_rank_right_unitary(self) -> None:
        source, target = self._frames((2, 2, 3), retained_rank=3)
        request = Periodic3DRankNGlobalGaugeAlignmentAnalysisRequest(
            retained_rank=3,
            source=source,
            target=target,
            tolerance=ComplexUnitaryProcrustesTolerance(
                rank_absolute=1.0e-12,
                rank_relative=1.0e-10,
            ),
        )

        analyzer = Periodic3DRankNGlobalGaugeAlignmentAnalyzer(request=request)
        result = analyzer.execute()

        assert isinstance(request, Periodic3DRankNGaugeAlignmentAnalysisRequest)
        assert isinstance(result, Periodic3DRankNGaugeAlignmentAnalysis)
        assert isinstance(analyzer, Periodic3DRankNGaugeAlignmentAnalyzer)
        assert request.band_subspace_rank == 3
        assert result.band_subspace_rank == 3
        assert analyzer.band_subspace_rank == 3
        assert type(result) is Periodic3DRankNGlobalGaugeAlignmentAnalysis
        assert result.gauge_group == "U(3)"
        assert result.alignment_sample_count == 12
        assert result.owner_result.rank_deficient_count == 0
        outcome = result.selection_outcome
        assert type(outcome) is Periodic3DRankNGlobalGaugeAlignmentSelected
        assert isinstance(outcome, Periodic3DRankNGaugeAlignmentCapability)
        assert outcome.band_subspace_rank == 3
        assert outcome.right_unitary == pytest.approx(target[0, 0, 0], abs=2.0e-15)
        assert not outcome.right_unitary.flags.writeable

    def test_global_alignment_does_not_admit_rank_deficient_completion(self) -> None:
        source, target = self._frames((2, 2, 2), retained_rank=3)
        source[..., -1] = 0.0
        target[..., -1] = 0.0
        result = Periodic3DRankNGlobalGaugeAlignmentAnalyzer(
            request=Periodic3DRankNGlobalGaugeAlignmentAnalysisRequest(
                retained_rank=3,
                source=source,
                target=target,
                tolerance=ComplexUnitaryProcrustesTolerance(
                    rank_absolute=1.0e-12,
                    rank_relative=1.0e-10,
                ),
            )
        ).execute()

        assert result.owner_result.rank_deficient_count == 1
        outcome = result.selection_outcome
        assert type(outcome) is Periodic3DRankNGlobalGaugeAlignmentRankDeficient
        assert isinstance(outcome, Periodic3DRankNGaugeAlignmentCapability)
        assert outcome.band_subspace_rank == 3
        assert outcome.retained_rank == 3
        assert outcome.numerical_rank == 2
        assert len(outcome.cross_singular_values) == 3
        assert outcome.applied_rank_cutoff > 0.0

    def test_transport_retains_one_closure_phase_per_retained_state(self) -> None:
        frame, _ = self._frames((2, 2, 2), retained_rank=3)
        request = Periodic3DRankNTransportAnalysisRequest(
            retained_rank=3,
            frame=frame,
            rank_absolute=1.0e-12,
            rank_relative=1.0e-10,
        )

        analyzer = Periodic3DRankNTransportAnalyzer(request=request)
        result = analyzer.execute()

        assert isinstance(request, Periodic3DRankNFrameTransportAnalysisRequest)
        assert isinstance(result, Periodic3DRankNFrameTransportAnalysis)
        assert isinstance(analyzer, Periodic3DRankNFrameTransportAnalyzer)
        assert request.band_subspace_rank == 3
        assert result.band_subspace_rank == 3
        assert analyzer.band_subspace_rank == 3
        assert type(result) is Periodic3DRankNTransportDiagnosticAnalysis
        assert result.minimum_singular_value == pytest.approx(1.0)
        assert result.rank_deficient_link_count == 0
        assert result.closure_and_plaquette_applicable
        assert result.maximum_absolute_closure_phases == pytest.approx((0.0, 0.0, 0.0))
        assert result.maximum_plaquette_phase == pytest.approx(0.0)

    def test_rejects_two_dimensional_meshes_and_rank_two(self) -> None:
        source, target = self._frames((2, 3), retained_rank=3)
        with pytest.raises(ValueError, match="N1, N2, N3, ambient, retained_rank"):
            Periodic3DRankNProcrustesAnalysisRequest(
                retained_rank=3,
                source=source,
                target=target,
                tolerance=ComplexUnitaryProcrustesTolerance(),
            )
        frame, _ = self._frames((2, 2, 2), retained_rank=2)
        with pytest.raises(ValueError, match="at least three"):
            Periodic3DRankNTransportAnalysisRequest(
                retained_rank=2,
                frame=frame,
                rank_absolute=1.0e-12,
                rank_relative=1.0e-10,
            )
