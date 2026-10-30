"""Architecture contracts for the plain scientific locality result graph."""

from __future__ import annotations

import pytest

from ksdft2effmass.analysis.model_adequacy.band_equivalence_locality.analysis import (
    BandEquivalenceLocalityAnalysis,
)
from ksdft2effmass.analysis.model_adequacy.band_equivalence_locality.results import (
    BandEquivalenceLocalityAmplitudeMidpointAnalysis,
    BandEquivalenceLocalityCaseAnalysis,
    BandEquivalenceLocalityErrorChannels,
    BandEquivalenceLocalityFirstPassingDecision,
    BandEquivalenceLocalityFlatAmplitudeResolutionAnalysis,
    BandEquivalenceLocalityPointAnalysis,
    BandEquivalenceLocalityShellAnalysis,
)
from ksdft2effmass.serialization import BaseTypedRecord

pytestmark = [pytest.mark.unit, pytest.mark.software_verification]


class TestBandEquivalenceLocalityAnalysis:
    """Establish separation of scientific results from retained records."""

    def test__scientific_result_graph__does_not_own_serialization(self) -> None:
        scientific_types = (
            BandEquivalenceLocalityAnalysis,
            BandEquivalenceLocalityAmplitudeMidpointAnalysis,
            BandEquivalenceLocalityCaseAnalysis,
            BandEquivalenceLocalityErrorChannels,
            BandEquivalenceLocalityFirstPassingDecision,
            BandEquivalenceLocalityFlatAmplitudeResolutionAnalysis,
            BandEquivalenceLocalityPointAnalysis,
            BandEquivalenceLocalityShellAnalysis,
        )

        assert all(
            not issubclass(scientific_type, BaseTypedRecord)
            for scientific_type in scientific_types
        )
        assert all(
            not hasattr(scientific_type, "to_json")
            for scientific_type in scientific_types
        )
