"""Ownership tests for periodic finite-rank Fourier analysis."""

from importlib.util import find_spec

import pytest

from ksdft2effmass.fourier_analysis import PeriodicRankNFourierAnalysisCapability
from ksdft2effmass.periodic1d.rankN.fourier_analysis import (
    Periodic1DRankNFourierAnalysis,
    Periodic1DRankNFourierAnalysisCapability,
    Periodic1DRankNFourierAnalysisRequest,
    Periodic1DRankNFourierAnalysisRequestRole,
    Periodic1DRankNFourierAnalysisRole,
    Periodic1DRankNFourierAnalyzer,
    Periodic1DRankNFourierAnalyzerRole,
)
from ksdft2effmass.periodic2d.rankN.fourier_analysis import (
    Periodic2DRankNFourierAnalysisCapability,
)
from ksdft2effmass.periodic3d.rankN.fourier_analysis import (
    Periodic3DRankNFourierAnalysisCapability,
)

pytestmark = [pytest.mark.unit, pytest.mark.software_verification]


class TestFourierAnalysisOwnership:
    """Keep Fourier analysis independent from gauge alignment and locality."""

    def test__periodic1d_actions__refine_the_fourier_analysis_roles(self) -> None:
        """Require concrete 1D actions to expose their dedicated capability owner."""
        assert issubclass(
            Periodic1DRankNFourierAnalysisRequest,
            Periodic1DRankNFourierAnalysisRequestRole,
        )
        assert issubclass(
            Periodic1DRankNFourierAnalysis,
            Periodic1DRankNFourierAnalysisRole,
        )
        assert issubclass(
            Periodic1DRankNFourierAnalyzer,
            Periodic1DRankNFourierAnalyzerRole,
        )

    def test__dimensions__are_sibling_finite_rank_refinements(self) -> None:
        """Prevent 2D or 3D Fourier ownership from inheriting through 1D."""
        capabilities = (
            Periodic1DRankNFourierAnalysisCapability,
            Periodic2DRankNFourierAnalysisCapability,
            Periodic3DRankNFourierAnalysisCapability,
        )
        assert all(
            issubclass(capability, PeriodicRankNFourierAnalysisCapability)
            for capability in capabilities
        )
        assert not issubclass(
            Periodic2DRankNFourierAnalysisCapability,
            Periodic1DRankNFourierAnalysisCapability,
        )
        assert not issubclass(
            Periodic3DRankNFourierAnalysisCapability,
            Periodic1DRankNFourierAnalysisCapability,
        )

    def test__obsolete_gauge_alignment_owner__is_absent(self) -> None:
        """Do not retain an alias at the former vertically integrated path."""
        assert (
            find_spec("ksdft2effmass.periodic1d.rankN.gauge_alignment.fourier") is None
        )
