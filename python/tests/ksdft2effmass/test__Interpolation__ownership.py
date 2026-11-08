"""Ownership tests for periodic finite-rank interpolation."""

from importlib.util import find_spec

import pytest

from ksdft2effmass.interpolation import PeriodicRankNInterpolationCapability
from ksdft2effmass.periodic1d.rankN.interpolation import (
    Periodic1DRankNInterpolationAnalysis,
    Periodic1DRankNInterpolationAnalysisRequest,
    Periodic1DRankNInterpolationAnalysisRequestRole,
    Periodic1DRankNInterpolationAnalysisRole,
    Periodic1DRankNInterpolationAnalyzer,
    Periodic1DRankNInterpolationAnalyzerRole,
    Periodic1DRankNInterpolationCapability,
)
from ksdft2effmass.periodic2d.rankN.interpolation import (
    Periodic2DRankNInterpolationCapability,
)
from ksdft2effmass.periodic3d.rankN.interpolation import (
    Periodic3DRankNInterpolationCapability,
)

pytestmark = [pytest.mark.unit, pytest.mark.software_verification]


class TestInterpolationOwnership:
    """Keep interpolation independent from alignment, locality, and truncation."""

    def test__periodic1d_actions__refine_the_interpolation_roles(self) -> None:
        """Require concrete 1D actions to expose their dedicated capability owner."""
        assert issubclass(
            Periodic1DRankNInterpolationAnalysisRequest,
            Periodic1DRankNInterpolationAnalysisRequestRole,
        )
        assert issubclass(
            Periodic1DRankNInterpolationAnalysis,
            Periodic1DRankNInterpolationAnalysisRole,
        )
        assert issubclass(
            Periodic1DRankNInterpolationAnalyzer,
            Periodic1DRankNInterpolationAnalyzerRole,
        )

    def test__dimensions__are_sibling_finite_rank_refinements(self) -> None:
        """Prevent 2D or 3D interpolation ownership from inheriting through 1D."""
        capabilities = (
            Periodic1DRankNInterpolationCapability,
            Periodic2DRankNInterpolationCapability,
            Periodic3DRankNInterpolationCapability,
        )
        assert all(
            issubclass(capability, PeriodicRankNInterpolationCapability)
            for capability in capabilities
        )
        assert not issubclass(
            Periodic2DRankNInterpolationCapability,
            Periodic1DRankNInterpolationCapability,
        )
        assert not issubclass(
            Periodic3DRankNInterpolationCapability,
            Periodic1DRankNInterpolationCapability,
        )

    def test__obsolete_gauge_alignment_owner__is_absent(self) -> None:
        """Do not retain an alias at the former vertically integrated path."""
        assert (
            find_spec("ksdft2effmass.periodic1d.rankN.gauge_alignment.interpolation")
            is None
        )
