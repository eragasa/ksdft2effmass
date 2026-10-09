r"""Software verification of ``Periodic1DReductionChallengeCampaignJsonSerializer``.

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

from ksdft2effmass.periodic1d.campaign.reduction_challenge import (
    Periodic1DReductionChallengeCampaignJsonSerializer,
)

pytestmark = pytest.mark.software_verification
SUT = Periodic1DReductionChallengeCampaignJsonSerializer


class TestPeriodic1DReductionChallengeCampaignJsonSerializer:
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
        encoded = serializer.serialize(definition)
        assert b'"stress_band_indices"' in encoded
        assert b'"route_stress_mesh_size"' in encoded

    def test_contract__retired_forwarding_methods_are_absent(self) -> None:
        """Evidence ID: SV-CAMPAIGN-PERIODIC-ONE-D-ROW-060-002.

        Requirement: The canonical codec exposes only nominal ``serialize`` and
        ``deserialize`` operations, without deprecated forwarding aliases.

        Method: Inspect one serializer instance for former method names.

        Oracle: Row-060 no-compatibility-alias policy.

        Acceptance: Neither ``encode`` nor ``decode`` exists.

        Interpretation: A pass establishes a single reviewed codec surface.

        Limitations: Method absence does not establish wire correctness.
        """
        serializer = SUT()

        assert not hasattr(serializer, "encode")
        assert not hasattr(serializer, "decode")
