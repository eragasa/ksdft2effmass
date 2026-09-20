r"""Software verification of ``ParticleInBoxStudyInputDeserializer``.

Evidence profile: routine

Bounded artifact scope: version-one particle-in-a-box campaign input adapter.

Facet and represented meaning

The serializer-owned ActionObject converts retained UTF-8 JSON bytes into one closed
immutable study definition.

Intrinsic and cross-object scope

Field closure, numeric admission, and exact retained values are included.

VVUQ and scientific exclusions

This verifies wire adaptation only, not numerical correctness, scientific validation,
uncertainty quantification, or human acceptance.
"""

from pathlib import Path

import pytest

from ksdft2effmass.campaigns.research_monograph import (
    ParticleInBoxStudyInputDeserializer,
)

pytestmark = pytest.mark.software_verification
SUT = ParticleInBoxStudyInputDeserializer


class TestParticleInBoxStudyInputDeserializer:
    """Own software evidence for the particle-in-box input adapter."""

    @staticmethod
    def input_path() -> Path:
        """Return the maintained version-one input path."""
        return (
            Path(__file__).resolve().parents[7]
            / "calculations"
            / "research-monograph"
            / "particle-in-box"
            / "input.json"
        )

    def test_method__execute__decodes_exact_retained_definition(self) -> None:
        """Evidence ID: SV-MONOGRAPH-PIB-001

        Requirement: The public adapter decodes only the closed version-one input.

        Acceptance: The maintained input yields ``L=m=hbar=1``, eight interior points,
        and retained dimension three.
        """
        definition = ParticleInBoxStudyInputDeserializer().execute(
            self.input_path().read_bytes()
        )

        assert definition.length == 1.0
        assert definition.mass == 1.0
        assert definition.hbar == 1.0
        assert definition.interior_points == 8
        assert definition.retained_dimension == 3
