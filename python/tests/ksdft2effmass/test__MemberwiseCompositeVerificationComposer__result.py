"""Tests for memberwise independent-verification composition."""

from __future__ import annotations

from projectkoios.physkit.units import ScalarQuantity, Unitless

from ksdft2effmass.verification import (
    CompositeVerification,
    MemberwiseCompositeVerificationComposer,
    VerificationObservation,
)


class TestMemberwiseCompositeVerificationComposer:
    """Establish stable indexed composition without recomputing member results."""

    def test_result__prefixes_each_independent_member_observation(self) -> None:
        unit = Unitless()
        first = CompositeVerification(
            {
                "defect": VerificationObservation(
                    ScalarQuantity(0.0, unit),
                    ScalarQuantity(1.0e-10, unit),
                )
            }
        )
        second = CompositeVerification(
            {
                "defect": VerificationObservation(
                    ScalarQuantity(2.0e-10, unit),
                    ScalarQuantity(1.0e-10, unit),
                )
            }
        )

        result = MemberwiseCompositeVerificationComposer((first, second)).result()

        assert tuple(result.observations) == ("member_0_defect", "member_1_defect")
        assert result.observations["member_0_defect"].passed
        assert not result.observations["member_1_defect"].passed
