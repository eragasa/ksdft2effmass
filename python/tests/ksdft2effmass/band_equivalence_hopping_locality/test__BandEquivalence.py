"""Ownership contracts for :class:`BandEquivalence`."""

from __future__ import annotations

import pytest

from ksdft2effmass.analysis.model_adequacy.band_equivalence.base import (
    BandEquivalence,
    BandEquivalenceAnalysis,
    BandEquivalenceAnalyzer,
    BandEquivalenceRequest,
    PeriodicBandEquivalence,
    PeriodicBandEquivalenceAnalysis,
    PeriodicBandEquivalenceAnalyzer,
    PeriodicBandEquivalenceRequest,
)
from ksdft2effmass.periodic1d.band_equivalence.base import (
    Periodic1DBandEquivalence,
    Periodic1DBandEquivalenceAnalysis,
    Periodic1DBandEquivalenceAnalyzer,
    Periodic1DBandEquivalenceRequest,
)
from ksdft2effmass.periodic2d.band_equivalence.base import (
    Periodic2DBandEquivalence,
    Periodic2DBandEquivalenceAnalysis,
    Periodic2DBandEquivalenceAnalyzer,
    Periodic2DBandEquivalenceRequest,
)
from ksdft2effmass.periodic3d.band_equivalence.base import (
    Periodic3DBandEquivalence,
    Periodic3DBandEquivalenceAnalysis,
    Periodic3DBandEquivalenceAnalyzer,
    Periodic3DBandEquivalenceRequest,
)

pytestmark = [pytest.mark.unit, pytest.mark.software_verification]


class TestBandEquivalence:
    """Keep nominal band-equivalence ownership separate from composed capabilities."""

    def test_domain_roles_inherit_the_nominal_owner(self) -> None:
        for role in (
            BandEquivalenceRequest,
            BandEquivalenceAnalysis,
            BandEquivalenceAnalyzer,
        ):
            assert issubclass(role, BandEquivalence)

    def test_periodic_roles_inherit_the_periodic_nominal_owner(self) -> None:
        assert issubclass(PeriodicBandEquivalence, BandEquivalence)
        for role in (
            PeriodicBandEquivalenceRequest,
            PeriodicBandEquivalenceAnalysis,
            PeriodicBandEquivalenceAnalyzer,
        ):
            assert issubclass(role, PeriodicBandEquivalence)

    def test_dimensional_roles_inherit_their_nominal_owner(self) -> None:
        for nominal, request, analysis, analyzer in (
            (
                Periodic1DBandEquivalence,
                Periodic1DBandEquivalenceRequest,
                Periodic1DBandEquivalenceAnalysis,
                Periodic1DBandEquivalenceAnalyzer,
            ),
            (
                Periodic2DBandEquivalence,
                Periodic2DBandEquivalenceRequest,
                Periodic2DBandEquivalenceAnalysis,
                Periodic2DBandEquivalenceAnalyzer,
            ),
            (
                Periodic3DBandEquivalence,
                Periodic3DBandEquivalenceRequest,
                Periodic3DBandEquivalenceAnalysis,
                Periodic3DBandEquivalenceAnalyzer,
            ),
        ):
            assert issubclass(nominal, PeriodicBandEquivalence)
            assert issubclass(request, nominal)
            assert issubclass(analysis, nominal)
            assert issubclass(analyzer, nominal)
