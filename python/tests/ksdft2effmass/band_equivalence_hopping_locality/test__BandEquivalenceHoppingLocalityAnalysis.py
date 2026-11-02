"""Architecture contracts for the plain scientific locality result graph."""

from __future__ import annotations

import pytest

from ksdft2effmass.band_equivalence_hopping_locality.analysis import (
    BandEquivalenceHoppingLocalityAnalysis,
)
from ksdft2effmass.band_equivalence_hopping_locality.results import (
    BandEquivalenceHoppingLocalityAmplitudeMidpointAnalysis,
    BandEquivalenceHoppingLocalityCaseAnalysis,
    BandEquivalenceHoppingLocalityErrorChannels,
    BandEquivalenceHoppingLocalityFirstPassingDecision,
    BandEquivalenceHoppingLocalityFlatAmplitudeResolutionAnalysis,
    BandEquivalenceHoppingLocalityPointAnalysis,
    BandEquivalenceHoppingLocalityRepresentationEquivalenceAnalysis,
    BandEquivalenceHoppingLocalityShellAnalysis,
)
from ksdft2effmass.serialization import BaseTypedRecord

pytestmark = [pytest.mark.unit, pytest.mark.software_verification]


class TestBandEquivalenceHoppingLocalityAnalysis:
    """Establish separation of scientific results from retained records."""

    def test__scientific_result_graph__does_not_own_serialization(self) -> None:
        scientific_types = (
            BandEquivalenceHoppingLocalityAnalysis,
            BandEquivalenceHoppingLocalityAmplitudeMidpointAnalysis,
            BandEquivalenceHoppingLocalityCaseAnalysis,
            BandEquivalenceHoppingLocalityErrorChannels,
            BandEquivalenceHoppingLocalityFirstPassingDecision,
            BandEquivalenceHoppingLocalityFlatAmplitudeResolutionAnalysis,
            BandEquivalenceHoppingLocalityPointAnalysis,
            BandEquivalenceHoppingLocalityRepresentationEquivalenceAnalysis,
            BandEquivalenceHoppingLocalityShellAnalysis,
        )

        assert all(
            not issubclass(scientific_type, BaseTypedRecord)
            for scientific_type in scientific_types
        )
        assert all(
            not hasattr(scientific_type, "to_json")
            for scientific_type in scientific_types
        )
