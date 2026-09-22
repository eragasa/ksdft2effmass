r"""Software verification of ``Periodic1DIsolatedBandCampaignJsonSerializer``.

Evidence profile: claim_bearing

Bounded artifact scope: retained Appendix G isolated-band input adaptation.

Facet and represented meaning

The serializer retains every version-one control with explicit unitless quantities.

Intrinsic and cross-object scope

Strict decoding and canonical reconstruction are included.

VVUQ and scientific exclusions

This read-only compatibility test does not execute the retained campaign.
"""

from pathlib import Path

import numpy as np
import pytest

from ksdft2effmass.campaigns.research_monograph import (
    Periodic1DIsolatedBandCampaignJsonSerializer,
)

pytestmark = pytest.mark.software_verification
SUT = Periodic1DIsolatedBandCampaignJsonSerializer


class TestPeriodic1DIsolatedBandCampaignJsonSerializer:
    """Own compatibility evidence for the isolated-band input schema."""

    def test_method__deserialize_serialize__preserves_retained_definition(self) -> None:
        """Evidence ID: SV-CAMPAIGN-PERIODIC-ONE-D-003

        Requirement: The public record represents every retained isolated-band field.

        Method: Decode the repository input, assert independent literal controls, and
        decode its canonical public reconstruction.

        Oracle: The retained Appendix G input and explicit cutoff/range literals.

        Acceptance: Expected controls agree and reconstructed content is equivalent.

        Interpretation: A pass establishes version-one input compatibility.

        Limitations: Numerical results and scientific validity are not assessed.

        Provenance: The retained Appendix G ``input.json`` repository artifact.
        """
        root = Path(__file__).resolve().parents[7]
        payload = root.joinpath(
            "calculations/research-monograph/periodic-1d/input.json"
        ).read_bytes()
        serializer = SUT()

        definition = serializer.deserialize(payload)

        assert definition.plane_wave_cutoffs == (3, 5, 7, 9, 11)
        assert definition.hopping_ranges == (0, 1, 2, 3, 4, 6, 8)
        reconstructed = serializer.deserialize(serializer.serialize(definition))
        assert reconstructed.plane_wave_cutoffs == definition.plane_wave_cutoffs
        np.testing.assert_array_equal(
            reconstructed.parent_sample_momenta.magnitude,
            definition.parent_sample_momenta.magnitude,
        )

    def test_method__encode_decode__emit_deprecation_warnings(self) -> None:
        """Evidence ID: SV-CAMPAIGN-PERIODIC-ONE-D-009

        Requirement: Legacy ``encode`` and ``decode`` remain temporarily compatible
        but visibly deprecated in favor of the common ABC methods.

        Method: Invoke both aliases around one retained isolated-band definition.

        Oracle: Python's ``DeprecationWarning`` contract and the retained cutoff tuple.

        Acceptance: Both aliases emit ``DeprecationWarning`` and preserve the record.

        Interpretation: A pass confirms visible migration behavior without removal.

        Limitations: Warning behavior does not verify other result formats.

        Provenance: The retained Appendix G ``input.json`` repository artifact.
        """
        root = Path(__file__).resolve().parents[7]
        payload = root.joinpath(
            "calculations/research-monograph/periodic-1d/input.json"
        ).read_bytes()
        serializer = SUT()
        definition = serializer.deserialize(payload)

        with pytest.warns(DeprecationWarning, match="use serialize"):
            legacy_payload = serializer.encode(definition)
        with pytest.warns(DeprecationWarning, match="use deserialize"):
            reconstructed = serializer.decode(legacy_payload)

        assert reconstructed.plane_wave_cutoffs == definition.plane_wave_cutoffs
