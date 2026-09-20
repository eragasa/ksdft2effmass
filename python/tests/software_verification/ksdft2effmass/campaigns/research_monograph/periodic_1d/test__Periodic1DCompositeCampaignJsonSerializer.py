r"""Software verification of ``Periodic1DCompositeCampaignJsonSerializer``.

Evidence profile: claim_bearing

Bounded artifact scope: retained Appendix G composite input schema adaptation.

Facet and represented meaning

The serializer maps the historical version-one JSON to typed unitless campaign data.

Intrinsic and cross-object scope

Strict fields, retained groups, controls, and canonical reconstruction are included.

VVUQ and scientific exclusions

This read-only test does not execute the campaign or strengthen retained evidence.
"""

from pathlib import Path

import pytest

from ksdft2effmass.analysis.periodic_bands import ContiguousBandSelection
from ksdft2effmass.campaigns.research_monograph import (
    Periodic1DCompositeCampaignJsonSerializer,
)

pytestmark = pytest.mark.software_verification
SUT = Periodic1DCompositeCampaignJsonSerializer


class TestPeriodic1DCompositeCampaignJsonSerializer:
    """Own compatibility evidence for the retained composite input schema."""

    def test_method__decode_encode__preserves_retained_definition(self) -> None:
        """Evidence ID: SV-CAMPAIGN-PERIODIC-ONE-D-002

        Requirement: The public contract represents every historical composite input
        field without executing the calculation.

        Method: Decode the authenticated repository input, assert independent literal
        controls, canonically encode it, and decode the canonical bytes again.

        Oracle: Appendix G's retained input and explicit expected group/range literals.

        Acceptance: Expected controls agree and canonical reconstruction equals the
        first immutable DataObject.

        Interpretation: A pass establishes version-one input adaptation compatibility.

        Limitations: Result serialization, calculation behavior, and scientific
        validity are not assessed.

        Provenance: The retained Appendix G ``composite-input.json`` repository
        artifact.
        """
        root = Path(__file__).resolve().parents[7]
        payload = root.joinpath(
            "calculations/research-monograph/periodic-1d/composite-input.json"
        ).read_bytes()
        serializer = SUT()

        definition = serializer.deserialize(payload)

        assert definition.experiment_id == "research-monograph.periodic-1d.composite.v1"
        assert tuple(
            (group.identifier, group.lower_index, group.upper_index)
            for group in definition.retained_band_groups
        ) == (("low_pair", 0, 1), ("higher_pair", 2, 3))
        assert all(
            type(group.selection) is ContiguousBandSelection
            for group in definition.retained_band_groups
        )
        assert definition.hopping_ranges_cells == (0, 1, 2, 3, 4, 6, 8, 12)
        assert serializer.deserialize(serializer.serialize(definition)) == definition
