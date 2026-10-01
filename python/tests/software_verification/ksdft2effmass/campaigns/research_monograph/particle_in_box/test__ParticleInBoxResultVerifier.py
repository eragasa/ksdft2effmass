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

import subprocess
import sys
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

    def test_method__execute__rejects_invalid_schema_under_optimized_python(
        self, tmp_path: Path
    ) -> None:
        """Evidence ID: SV-MONOGRAPH-PIB-008

        Requirement: Verification requirements remain active when Python removes
        language-level assertions under optimization.

        Acceptance: A retained payload changed to schema version 999 is rejected by a
        ``python -O`` subprocess with a schema-version error.
        """
        root = Path(__file__).resolve().parents[7]
        retained = (
            root
            / "calculations"
            / "research-monograph"
            / "particle-in-box"
            / "result.json"
        )
        invalid = tmp_path / "invalid-result.json"
        invalid.write_bytes(
            retained.read_bytes().replace(
                b'\n  "schema_version": 1,\n',
                b'\n  "schema_version": 999,\n',
                1,
            )
        )
        command = (
            "from pathlib import Path; "
            "from ksdft2effmass.campaigns.research_monograph import "
            "ParticleInBoxResultVerifier; "
            "ParticleInBoxResultVerifier().execute(Path(__import__('sys').argv[1]), "
            "Path(__import__('sys').argv[2]))"
        )

        completed = subprocess.run(
            [sys.executable, "-O", "-c", command, str(invalid), str(root)],
            check=False,
            capture_output=True,
            text=True,
        )

        assert completed.returncode != 0
        assert "schema_version" in completed.stderr

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
