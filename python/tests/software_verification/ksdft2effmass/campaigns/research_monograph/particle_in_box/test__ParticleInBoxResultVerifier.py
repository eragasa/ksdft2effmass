r"""Software verification of ``ParticleInBoxResultVerifier``.

Evidence profile: routine

Bounded artifact scope: independent retained/current version-one result verifier.

Facet and represented meaning

The verifier reconstructs finite identities without importing the implementation it
checks and preserves historical runner compatibility explicitly.

Intrinsic and cross-object scope

Historical provenance admission and independent numerical checks are included.

VVUQ and scientific exclusions

A pass establishes only the declared finite numerical identities, not scientific
validation, uncertainty quantification, or human acceptance.
"""

import json
from pathlib import Path

import pytest

from ksdft2effmass.campaigns.research_monograph import ParticleInBoxResultVerifier

pytestmark = pytest.mark.software_verification
SUT = ParticleInBoxResultVerifier


class TestParticleInBoxResultVerifier:
    """Own software evidence for the independent result verifier."""

    def test_method__execute__accepts_retained_historical_result(self) -> None:
        """Evidence ID: SV-MONOGRAPH-PIB-004

        Requirement: The independent verifier admits the immutable historical runner
        identity without requiring current implementation hashes.

        Acceptance: Verification of the maintained retained result completes without
        an exception.
        """
        root = Path(__file__).resolve().parents[7]
        result = (
            root
            / "calculations"
            / "research-monograph"
            / "particle-in-box"
            / "result.json"
        )

        ParticleInBoxResultVerifier().execute(result, root)

    def test_method__execute__rejects_relative_default_masking(
        self, tmp_path: Path
    ) -> None:
        """Evidence ID: SV-MONOGRAPH-PIB-008

        Requirement: Matrix-identity verification uses only the declared
        epsilon-scaled absolute tolerance, not NumPy's comparatively loose default
        relative tolerance.

        Acceptance: A ``1e-8`` perturbation to an order-one projector entry is
        rejected even though it would satisfy NumPy's default relative tolerance.
        """
        root = Path(__file__).resolve().parents[7]
        retained = (
            root
            / "calculations"
            / "research-monograph"
            / "particle-in-box"
            / "result.json"
        )
        payload = json.loads(retained.read_text(encoding="utf-8"))
        payload["matrices"]["spectral_projector_full"][0][0] += 1.0e-8
        perturbed = tmp_path / "result.json"
        perturbed.write_text(json.dumps(payload), encoding="utf-8")

        with pytest.raises(AssertionError):
            ParticleInBoxResultVerifier().execute(perturbed, root)

    def test_artifact__dependency__excludes_particle_in_box_implementation(
        self,
    ) -> None:
        """Evidence ID: SV-MONOGRAPH-PIB-007

        Requirement: The verifier must not import the campaign or model implementation
        whose output it verifies.

        Acceptance: Its source contains no import rooted at the particle-in-a-box
        producer modules.
        """
        root = Path(__file__).resolve().parents[7]
        source = (
            root
            / "python"
            / "src"
            / "ksdft2effmass"
            / "campaigns"
            / "research_monograph"
            / "particle_in_box"
            / "core_verification.py"
        )
        source_text = source.read_text(encoding="utf-8")

        assert "from ksdft2effmass.analysis" not in source_text
        assert "from ksdft2effmass.operators" not in source_text
        assert "from .particle_in_box import" not in source_text
