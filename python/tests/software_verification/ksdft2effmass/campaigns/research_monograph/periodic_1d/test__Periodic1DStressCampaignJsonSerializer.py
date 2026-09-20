r"""Software verification of ``Periodic1DStressCampaignJsonSerializer``.

Evidence profile: claim_bearing

Bounded artifact scope: retained Appendix G stress-study input adaptation.

Facet and represented meaning

The serializer retains stress sweeps, Fourier shapes, route controls, and thresholds.

Intrinsic and cross-object scope

Strict version-one decoding and canonical reconstruction are included.

VVUQ and scientific exclusions

This read-only compatibility test does not execute any stress case.
"""

from pathlib import Path

import numpy as np
import pytest

from ksdft2effmass.campaigns.research_monograph import (
    Periodic1DStressCampaignJsonSerializer,
)

pytestmark = pytest.mark.software_verification
SUT = Periodic1DStressCampaignJsonSerializer


class TestPeriodic1DStressCampaignJsonSerializer:
    """Own compatibility evidence for the retained stress input schema."""

    def test_method__decode_encode__preserves_retained_definition(self) -> None:
        """Evidence ID: SV-CAMPAIGN-PERIODIC-ONE-D-004

        Requirement: The public record represents every retained stress input field.

        Method: Decode the repository input, assert independent named-shape and sweep
        literals, then decode its canonical public reconstruction.

        Oracle: The retained Appendix G stress input and explicit expected identifiers.

        Acceptance: Six shapes and all mesh sizes agree after canonical reconstruction.

        Interpretation: A pass establishes version-one stress-input compatibility.

        Limitations: Stress calculations and scientific conclusions are not assessed.

        Provenance: The retained Appendix G ``stress-input.json`` repository artifact.
        """
        root = Path(__file__).resolve().parents[7]
        payload = root.joinpath(
            "calculations/research-monograph/periodic-1d/stress-input.json"
        ).read_bytes()
        serializer = SUT()

        definition = serializer.deserialize(payload)

        assert tuple(shape.identifier for shape in definition.potential_shapes) == (
            "baseline_cosine",
            "translated_cosine",
            "constant_shifted_cosine",
            "second_harmonic_cosine",
            "inversion_broken",
            "three_harmonic",
        )
        assert definition.reciprocal_mesh_sizes == (8, 16, 32, 64, 128)
        reconstructed = serializer.deserialize(serializer.serialize(definition))
        np.testing.assert_array_equal(
            reconstructed.potential_strengths.magnitude,
            definition.potential_strengths.magnitude,
        )
        assert reconstructed.reciprocal_mesh_sizes == definition.reciprocal_mesh_sizes
